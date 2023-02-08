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
lastServo = robot.servos.activeServos[0]
lastLeg = robot.legs[0]
if debug:
 print("Robot initialised")



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
 lastServo = servo
 return str(robot.servos.angle[servo])
 
def GetVoltages():
 return robot.aToD.GetAllValues()
 
def GetActiveServos():
 reply = ""
 for servo in robot.servos.activeServos:
  reply += str(servo) + " "
 return reply
 
def GetLastServo():
 return str(lastServo)
 
def GetLastLeg():
 return lastLeg.name 


# ChangeServo servo option [angle]

def ChangeServo(tokens):
 servo = int(tokens[1])
 lastServo = servo
 option = tokens[2]
 if option == "+1":
  robot.servos.SetAngle(servo, robot.servos.angle[servo] + 1)
 elif option == "-1":
  robot.servos.SetAngle(servo, robot.servos.angle[servo] - 1)
 elif option == "+10":
  robot.servos.SetAngle(servo, robot.servos.angle[servo] + 10)
 elif option == "-10":
  robot.servos.SetAngle(servo, robot.servos.angle[servo] - 10)
 elif option == "zero":
  robot.servos.SetAngle(servo, 0)
 elif option == "setAngle":
  angle = float(tokens[3])
  robot.servos.SetAngle(servo, a)
 elif option == "negateDirection":
  robot.servos.InvertDirection(servo)
 elif option == "saveCurrentAngleAsOffset":
  robot.servos.MakeCurrentPositionZero(servo)
 else:
  reply = "EditServo - dud option: " + option
  return reply
 reply = str(robot.servos.angle[servo])
 return reply
 

# MoveLegFast name x y

def MoveLegFast(tokens):
 reply = ""
 leg = robot.GetLegFromName(tokens[1])
 x = float(tokens[2])
 y = float(tokens[3])
 point = [(x, y), 1, True]
 leg.QuickToPoint(point)
 return reply
 
# MoveLegStraight name x y v

def MoveLegStraight(tokens):
 reply = ""
 leg = robot.GetLegFromName(tokens[1])
 x = float(tokens[2])
 y = float(tokens[3])
 v = float(tokens[4])
 point = [(x, y), v, True]
 t = leg.StraightToPoint(point) + 1
 robot.SpinForTime(t)
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
 elif tokens[0] == "GetActiveServos":
  # GetActiveServos
  reply = GetActiveServos()
 elif tokens[0] == "GetLastServo":
  # GetLastServo
  reply = GetLastServo()
 elif tokens[0] == "GetLastLeg":
  # GetLastLeg
  reply = GetLastLeg()   
 elif tokens[0] == "MoveLegFast":
  # MoveLegFast name x y
  reply = MoveLegFast(tokens) 
 elif tokens[0] == "MoveLegStraight":
  # MoveLegStraight name x y v
  reply = MoveLegStraight(tokens)
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

if __name__ == "__main__":

 #me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running

 HOST, PORT = "localhost", 9999

 # Create the server, binding to localhost on port 9999
 with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
  # Activate the server; this will keep running until you
  # interrupt the program with Ctrl-C or send "Exit"
  if debug:  
   print("Starting server.")
  server.serve_forever()
