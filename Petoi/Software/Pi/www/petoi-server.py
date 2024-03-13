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
############################################################################################


debug = True



import sys
import time
import math as maths
import socketserver

import io
import picamera
import logging
from threading import Condition
from http import server


if len(sys.argv) == 1:
 import rrlpetoi as rrlp
elif sys.argv[1] == "s":
 import rrlpetoisim as rrlp
else:
 print("Invalid argument: " + sys.argv[1])
 sys.exit(1)


#from tendo import singleton

encoding = "utf-8"

robot = rrlp.Robot()
if debug:
 print("Robot initialised")


#---------------------------------------------------------------------------------

# Handle the camera
 
class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

#--------------------------------------------------------------------------------------

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
 
def run_server(server):
 server.serve_forever()



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

if __name__ == "__main__":

 #me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running

 # Create the robot server, binding to localhost on port 9999
 HOST, PORT = "localhost", 9999
 robotServer = socketserver.TCPServer((HOST, PORT), TCPHandler)
 
 # Create the camera server binding to localhost on port 8000
 camera = picamera.PiCamera(resolution='640x480', framerate=24)
 output = StreamingOutput()
 #Uncomment the next line to change the Pi's Camera rotation (in degrees)
 #camera.rotation = 90
 camera.start_recording(output, format='mjpeg')
 address = ('', 8000)
 CameraServer = StreamingServer(address, StreamingHandler)
 
 robotThread = threading.Thread(target=run_server, args=(RobotServer,))
 cameraThread = threading.Thread(target=run_server, args=(CameraServer,))
 
 if debug:  
  print("Starting robot server thread.")  
 robotThread.start()
 
 if debug:  
  print("Starting camera server thread.")  
 cameraThread.start()


