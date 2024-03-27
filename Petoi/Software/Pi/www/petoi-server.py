#
# Petoi Bittle Control Program For a Raspberry Pi - server version
#
# This runs a socket through which commands can be sent to the robot
# and responses returned. When run it allows other software talking to
# that socket (principally a web browser interface) to control the robot.
#
# Written by
#
# Adrian Bowyer
# RepRap Ltd
#
# https://reprapltd.com
#
# 24 January 2023
#
# Licence: GPL
#
#
# Joint servo numbers and foot sensors (top view)
#
#    V0                      V1
#     |                      |
#     |           H          |
#    15          12           8
#    |                        |
#    |                        |
#   14                         9
#
#
#    V2                     V3 
#     |                     |
#     |                     |
#    1                       7
#    |                       |
#    |                       |
#    0                       6
#
# Vn are Hall effect foot voltages. A foot on the ground is about 0.1V less than one in
# the air. H is the head (servo 12). The other numbers are the shoulder and elbow servo
# numbers.
#
# For socket info see:
# https://docs.python.org/3/library/socketserver.html#socketserver-tcpserver-example
#
# The Raspberry Pi Camera server was written by GPT4, not me.
#
# The camera stream can be embedded in a web page with
#
# <?php include 'camera_ip.php'; ?>
# <img src="http://<?= $camera_ip; ?>:8000/stream.mjpg" width="640" height="480">
#
############################################################################################


debug = True



import sys
import time
import math as maths
from flask import Flask, Response
import picamera
import io
from time import sleep
import socket
import socketserver
import threading

# Are we running as a simulator, or for real?

if len(sys.argv) == 1:
 import rrlpetoi as rrlp
elif sys.argv[1] == "s":
 import rrlpetoisim as rrlp
else:
 print("Invalid argument: " + sys.argv[1])
 sys.exit(1)


# Set up the robot

encoding = "utf-8"

robot = rrlp.Robot()
if debug:
 print("Robot initialised")
 
#########################################################################################

# The camera server

app = Flask(__name__)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def generate_php_script(ip_address):
    php_content = f"""<?php
// Auto-generated IP address for camera stream
$camera_ip = "{ip_address}";
?>
"""
    with open("camera_ip.php", "w") as php_file:
        php_file.write(php_content)

def generate_camera_stream():
    with picamera.PiCamera() as camera:
        # Camera warm-up time
        sleep(2)

        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            stream.seek(0)
            frame = stream.read()

            # Use a multipart response format (MJPEG)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            stream.seek(0)
            stream.truncate()

@app.route('/stream.mjpg')
def stream_mjpg():
    return Response(generate_camera_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def runCameraServer():
  app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)


#########################################################################################

# The robot server

def GetLegNames():
 reply = ""
 for leg in robot.legs:
  reply += leg.name + " "
 return reply


def GetLegDescription(legName):
 leg = robot.GetLegFromName(legName)
 lastLeg = leg
 v = leg.FootVoltage()
 hit = leg.FootHit()
 reply = "Leg " + legName + " is at (x, y) = " + str(leg.point[0]) + ". Its foot is "
 if hit:
  reply += "touching"
 else:
  reply += "not touching"
 reply += " (foot voltage = " + str(v) + ")."
 return reply
 
 
def GetServoAngle(servoNumber):
 servo = int(servoNumber)
 return "{:.1f}".format(robot.servos.angle[servo])
 
def GetVoltages():
 return robot.aToD.GetAllValues()
 
def GetRange():
 return str(robot.range.Distance()) + "mm"
 
def GetAccelerometer():
 return robot.accelerometer.GetAllValues()
 
def GetActiveServos():
 reply = ""
 for servo in robot.servos.activeServos:
  reply += str(servo) + " "
 return reply


# ChangeServo servo option [angle]

def ChangeServo(tokens):
 servo = int(tokens[1])
 lastServo = servo
 option = tokens[2]
 if option == "changeBy":
  angle = float(tokens[3])
  robot.servos.SetAngle(servo, robot.servos.angle[servo] + angle)
 elif option == "zero":
  robot.servos.SetAngle(servo, 0)
 elif option == "setAngle":
  angle = float(tokens[3])
  robot.servos.SetAngle(servo, angle)
 elif option == "negateDirection":
  robot.servos.InvertDirection(servo)
 elif option == "saveCurrentAngleAsOffset":
  robot.servos.MakeCurrentPositionZero(servo)
 else:
  reply = "EditServo - dud option: " + option
  return reply
 robot.UpdateAllLegs()
 reply = str(robot.servos.angle[servo])
 return reply
 
 
def GetLegPosition(legName):
 leg = robot.GetLegFromName(legName)
 p = leg.Position()
 reply = "{:.1f}".format(p[0]) + " " + "{:.1f}".format(p[1])
 return reply
 

# MoveLegFast name x y

def MoveLegFast(tokens):
 leg = robot.GetLegFromName(tokens[1])
 x = float(tokens[2])
 y = float(tokens[3])
 point = [(x, y), 1, False]
 leg.QuickToPoint(point)
 reply = GetLegPosition(tokens[1])
 return reply
 
# MoveLegStraight name x y v

def MoveLegStraight(tokens):
 leg = robot.GetLegFromName(tokens[1])
 x = float(tokens[2])
 y = float(tokens[3])
 v = float(tokens[4])
 point = [(x, y), v, True]
 t = leg.StraightToPoint(point) + 1
 robot.SpinForTime(t)
 reply = GetLegPosition(tokens[1])
 return reply
 

 
def Interpret(command):
 tokens = command.split()
 reply = ""
 if tokens[0] == "ChangeServo":
  # ChangeServo servo option [angle]
  reply = ChangeServo(tokens)
 elif tokens[0] == "GetLegDescription":
  # GetLegDescription name
  reply = GetLegDescription(tokens[1])
 elif tokens[0] == "GetLegNames":
  # GetLegNames
  reply = GetLegNames()
 elif tokens[0] == "GetServoAngle":
  # GetServoAngle servo
  reply = GetServoAngle(tokens[1])
 elif tokens[0] == "GetVoltages":
  # GetVoltages
  reply = GetVoltages()
 elif tokens[0] == "GetAccelerometer":
  # GetAccelerometer
  reply = GetAccelerometer()
 elif tokens[0] == "GetRange":
  # GetRange
  reply = GetRange() 
 elif tokens[0] == "GetActiveServos":
  # GetActiveServos
  reply = GetActiveServos()
 elif tokens[0] == "ZeroServos":
  robot.servos.GoToZeros()
 elif tokens[0] == "SaveCurrentPositionAsZeros":
  robot.servos.SaveZeros()  
 elif tokens[0] == "GetLegPosition":
  # GetLegPosition legNmae
  reply = GetLegPosition(tokens[1])
 elif tokens[0] == "MoveLegFast":
  # MoveLegFast name x y
  reply = MoveLegFast(tokens) 
 elif tokens[0] == "MoveLegStraight":
  # MoveLegStraight name x y v
  reply = MoveLegStraight(tokens)
 elif tokens[0] == "GetLegRow":
  # GetLegRow legName
  reply = robot.GetRowValues(tokens[1])
 elif tokens[0] == "Exit":
  robot.Shutdown()
  sys.exit(0)
 else:
  print("Dud command: " + command)
 
 return reply
 



class TCPHandler(socketserver.StreamRequestHandler):

 def handle(self):
  # self.rfile is a file-like object created by the handler;
  # we can now use e.g. readline() instead of raw recv() calls
  self.data = self.rfile.readline().strip()
  received = self.data.decode(encoding)
 # print("{} wrote:".format(self.client_address[0]))
  if debug:  
   print("received: "+received)
  # Likewise, self.wfile is a file-like object used to write back
  # to the client
  reply = Interpret(received)
  if debug:  
   print("sent: "+reply)
  self.wfile.write(bytes(reply + "\n", encoding))

# Launch the two servers

if __name__ == '__main__':

# Camera

    ip_address = get_ip_address()
    generate_php_script(ip_address)
    if debug:
      print('Starting camera server')
    cameraThread = threading.Thread(target=runCameraServer)
    cameraThread.start()

# Robot

 # Create the robot server, binding to localhost on port 9999
 HOST, PORT = "localhost", 9999
 with socketserver.TCPServer((HOST, PORT), TCPHandler) as robotServer:
  if debug:
   print('Starting robot server')
  robotServer.serve_forever()


