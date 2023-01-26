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

import sys
import time
import math as maths
import rrlpetoi as rrlp

import socketserver
#from tendo import singleton


robot = rrlp.Robot()

servos = robot.servos
activeServos = servos.activeServos

aToD = robot.aToD
if aToD.err != "":
 print("A to D initialisation error: " + aToD.err)

legs = robot.legs

def EditServo(servo, option, angle=""):
 reply = ""
 options = ["+1", "-1", "+10", "-10", "set angle", "negate direction", "save current angle as offset"]
 if option == options[0]:
  servos.SetAngle(servo, servos.angle[servo] + 1)
 elif option == options[1]:
  servos.SetAngle(servo, servos.angle[servo] - 1)
 elif option == options[2]:
  servos.SetAngle(servo, servos.angle[servo] + 10)
 elif option == options[3]:
  servos.SetAngle(servo, servos.angle[servo] - 10)
 elif option == options[4]:
  if angle != "":
   a = float(angle)
   servos.SetAngle(servo, a)
 elif option == options[5]:
  servos.InvertDirection(servo)
 elif option == options[6]:
  servos.MakeCurrentPositionZero(servo)
 else:
  reply = "EditServo - dud option: " + option)
 return reply



class TCPHandler(socketserver.StreamRequestHandler):

 def handle(self):
  # self.rfile is a file-like object created by the handler;
  # we can now use e.g. readline() instead of raw recv() calls
  self.data = self.rfile.readline().strip()
  print("{} wrote:".format(self.client_address[0]))
  print(self.data)
  # Likewise, self.wfile is a file-like object used to write back
  # to the client
  reply = EditServo(0, "+10")
  self.wfile.write(reply + "\n")

if __name__ == "__main__":

 #me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running

 HOST, PORT = "localhost", 9999

 # Create the server, binding to localhost on port 9999
 with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
  # Activate the server; this will keep running until you
  # interrupt the program with Ctrl-C
  server.serve_forever()
