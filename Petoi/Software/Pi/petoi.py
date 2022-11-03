#
# Petoi Bittle Control Program For a Raspberry Pi
#
# This uses the whiptail menu interface so you can just ssh into the robot via
# WiFi and control it from a terminal window.
#
# Written by
#
# Adrian Bowyer
# RepRap Ltd
#
# https://reprapltd.com
#
# 21 October 2022
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
#
############################################################################################
#
# Control program
#


from whiptail import Whiptail
import time
import rrlpetoi as rrlp

w = Whiptail(title="RepRap Ltd Quadruped Robot Control Program", backtitle="https://reprapltd.com")

servos = rrlp.Servos()
servos.LoadZeros('zero-angles')
servos.GoToZeros()
activeServos = servos.activeServos
aToD = rrlp.AToD()
legs = [rrlp.Leg(servos, 14, 15, aToD, 0, "front left"), rrlp.Leg(servos, 9, 8, aToD, 1, "front right"), rrlp.Leg(servos, 0, 1, aToD, 2, "back left"), rrlp.Leg(servos, 6, 7, aToD, 3, "back right")]
 
def EditServo(servo):
 loop = True
 options = ["+1", "-1", "+10", "-10", "negate direction", "save current angle as offset"]
 while loop:
  menu = w.menu("Servo " + str(servo) + ", angle: " + str(servos.angle[servo]), options)
  loop = menu[1] is 0
  if loop:
   symbol = menu[0]
   if symbol == "+1":
    servos.SetAngle(servo, servos.angle[servo] + 1)
   elif symbol == "-1":
    servos.SetAngle(servo, servos.angle[servo] - 1)
   elif symbol == "+10":
    servos.SetAngle(servo, servos.angle[servo] + 10)
   elif symbol == "-10":
    servos.SetAngle(servo, servos.angle[servo] - 10)
   elif symbol == "negate direction":
    servos.InvertDirection(servo)
   elif symbol == "save current angle as offset":
    servos.MakeCurrentPositionZero(servo)
   else:
    w.msgbox("Dud option: " + symbol)
   
   
def ChooseServo(active):
 loop = True
 a = ["Save current positions as zeros"]
 for s in active:
  a.append(str(s))
 while loop:
  menu = w.menu("Choose servo", a)
  loop = menu[1] is 0
  if loop:
   symbol = menu[0]
   if symbol == a[0]:
    for servo in range(rrlp.servoCount):
     servos.MakeCurrentPositionZero(servo)
    servos.SaveZeros()
    w.msgbox("Zero positions saved")
   else:
    servo = int(symbol)
    EditServo(servo)
 for leg in legs:
  leg.SetFromServoAngles()
  
def GetLegFromName(name):
 for leg in legs:
  if leg.name == name:
   return leg
 w.message("There's no leg called " + name + ". Returning legs[0].")
 return legs[0]
    
def EditLeg(leg):
 loop = True
 while loop:
  menu = w.menu(leg.name + " leg, at (x, y): " + str(leg.p), ["move to position", "set horizontal", "b"])
  loop = menu[1] is 0
  if loop:
   symbol = menu[0]
   if symbol == "move to position":
    posAndV = w.inputbox("Move to point at a velocity, Type - X Y V: ", default = "0 0 10").split()
    p = (float(posAndV[0]), float(posAndV[1]))
    v = float(posAndV[2])
    spinFor = leg.StraightToPoint(p, v)
    t = time.time() + 0.1 + spinFor
    while time.time() < t:
     leg.spin()
   else:
    pass
     
    
def ChooseLeg(legs):
 loop = True
 names = []
 for leg in legs:
  names.append(leg.name)
 while loop:
  menu = w.menu("Choose leg", names)
  loop = menu[1] is 0
  if loop:
   EditLeg(GetLegFromName(menu[0]))
   

loop = True
while loop:
 menu = w.menu("Control", ["servos", "legs"])
 loop = menu[1] is 0
 if loop:
  if menu[0] == "servos":
   ChooseServo(activeServos)
  else:
   ChooseLeg(legs)
 
 
 
servos.Relax()


