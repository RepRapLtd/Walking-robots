#
# Petoi Bittle Control Program
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

import time
import math as maths
from adafruit_servokit import ServoKit

# Number of servos potentially controllable by the PCA9685 PWM controller in the robot

servoCount = 16

# How small in mm is close enough to zero?

resolution = 0.01

# Leg humerus and radius/ulna lengths in mm

humerus = 45
ulna = 49

# Radians to/from degrees

toDegrees = 180.0/maths.pi
toRadians = 1.0/toDegrees

# Convert (a1, a2) between degrees and radians

def ToDegrees(a):
 return (a[0]*toDegrees, a[1]*toDegrees)

def ToRadians(a):
 return (a[0]*toRadians, a[1]*toRadians)



##########################################################################################
#
# Class to control the servos, using the Adafruit Servo Kit
#
#  sudo pip3 install adafruit-circuitpython-servokit
#
#  https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/using-the-adafruit-library
#
# self.angle - the angles the robot thinks the servos are at
# self.angleOffsets - added to self.angle to get the angles to send to the servos
# self.direction - +/-1 multiplies self.angle to get the servo moving the right way
#
# Servos work in degrees.
 
class Servos:

 def __init__(self):
  self.kit = ServoKit(channels=servoCount)
  self.angle = [0]*servoCount
  self.angleOffsets = [0]*servoCount
  self.direction = [1.0]*servoCount

#
# Get the offsets from the file zero-angles and apply them.
#

 def LoadZeros(self):
  with open('zero-angles') as file:
   for line in file:
    l = line.split()
    servo = int(l[0])
    a = float(l[1])
    d = float(l[2])
    if a < 0.0:
     # No servo at this location - disable the PWM
     self.kit.servo[servo]._pwm_out.duty_cycle = 0
    else:
     self.kit.servo[servo].angle = a
     self.angleOffsets[servo] = a
     self.angle[servo] = 0.0
     self.direction[servo] = d

#
# Actually turn a servo; expects an angle in degrees.
#

 def SetAngle(self, servo, a):
    a1 = self.direction[servo]*a + self.angleOffsets[servo]
    self.kit.servo[servo].angle = a1
    self.angle[servo] = a

#    
# Where am I?
#

 def Angle(self, servo):
  return self.angle[servo]

# Turn all servos off (used at shutdown).
  
 def Relax(self):
  for servo in range(servoCount):
    self.kit.servo[servo]._pwm_out.duty_cycle = 0

#
#############################################################################################  
#
# A robot leg
#
# shoulder and foreleg are the servo numbers for those.
# foot is the analogue channel for the foot hall-effect sensor
# servos is the class above.
#
# self.p is the current foot position in robot coordinates.
# self.step is the increment in mm used for moving in a straight line.
#
# Legs work in radians.
    
class Leg:

 def __init__(self, shoulder, foreleg, foot, servos):
  self.shoulder = shoulder
  self.foreleg = foreleg
  self.foot = foot
  self.servos = servos
  self.l1 = humerus
  self.l2 = ulna
  self.p = (0.0, 0.0)
  self.step = 1.0

# The leg kinematic coordinate system has x down the straight leg,
# y forward parallel to the ground. But the robot deals with the
# coordinates of the foot with x forward and y up the straight leg.

 def RobotToLegCoordinates(self, p):
  return (self.l1 + self.l2 - p[1], p[0])

 def LegToRobotCoordinates(self, p):
  return (p[1], self.l1 + self.l2 - p[0])
  
# Forward kinematics; expects radians. Given the two servo angles, this returns the position
# of the foot in leg coordinates.

 def PositionFromAngles(self, angles):
  x = self.l1*maths.cos(angles[0]) + self.l2*maths.cos(angles[0]+angles[1])
  y = self.l1*maths.sin(angles[0]) + self.l2*maths.sin(angles[0]+angles[1])
  return (x,y)

# Reverse kinematics; returns radians. Given the position of the foot in leg coordinates
# this gives the angles needed to put it there. The output is
#
#  [Success/fail, (a1, a2), (a3, a4)]
#
# The first is a boolean that tells you if the position is atainable. The second and third
# are pairs of angles for the shoulder and forearm servos. There are always two solutions of none.
# The robot uses the second returned solution, which is the one where the knee points backwards.
#
# Derived from:
#
#  https://uk.mathworks.com/help/symbolic/derive-and-apply-inverse-kinematics-to-robot-arm.html


 def AnglesFromPosition(self, position):
  l12 = self.l1*self.l1
  l22 = self.l2*self.l2
  xp2 = position[0]*position[0]
  yp2 = position[1]*position[1]
  sigma = -l12*l12 + 2*l12*l22 +2*l12*xp2 + 2*l12*yp2 - l22*l22 +2*l22*xp2 + 2*l22*yp2 - xp2*xp2 -2*xp2*yp2 -yp2*yp2
  if sigma < 0.0:
   print("No reverse kinematic solution for position " + str(position))
   return [False, (0, 0), (0, 0)]
  sigma = maths.sqrt(sigma)
  div = l12 + 2*self.l1*position[0] - l22 + xp2 + yp2
  a1p = 2*maths.atan2(2*self.l1*position[1] + sigma, div)
  a1m = 2*maths.atan2(2*self.l1*position[1] - sigma, div)
  sigma = (-l12 + 2*self.l1*self.l2 - l22 + xp2 + yp2)*(l12 + 2*self.l1*self.l2 + l22 - xp2 - yp2)
  if sigma < 0.0:
   print("No reverse kinematic solution for position " + str(position))
   return [False, (0, 0), (0, 0)]
  sigma = maths.sqrt(sigma)
  div = -l12 + 2*self.l1*self.l2 - l22 + xp2 + yp2
  a2p = 2*maths.atan2(sigma, div)
  return [True, (a1p, -a2p), (a1m, a2p)]

#
# Go fast to a point in robot coordinates.
#

 def QuickToPoint(self, p):
  p1 = self.RobotToLegCoordinates(p)
  angles = self.AnglesFromPosition(p1)
  if angles[0]:
   a = ToDegrees(angles[2])
   self.servos.SetAngle(self.shoulder, a[0])
   self.servos.SetAngle(self.foreleg, a[1])
   self.p = p
  else:
   print("No can do")
   
#
# Move in a straight line to p at v mm/s
#

 def StraightToPoint(self, p, v):
  diff = (p[0] - self.p[0], p[1] - self.p[1])
  d = maths.sqrt(diff[0]*diff[0] + diff[1]*diff[1])
  if d < resolution:
   return
  steps = int(0.5 + d/self.step)
  dStep = d/steps
  dInc = (dStep*diff[0]/d, dStep*diff[1]/d)
  tStep = dStep/v
  for s in range(steps):
   p = (self.p[0] + dInc[0], self.p[1] + dInc[1])
   self.QuickToPoint(p)
   time.sleep(tStep)
   
#
# Where is the foot?
#

 def Position(self):
  return self.p

#
# Where is the foot, given the servo angles? Mainly for debugging.
#

 def GetPoint(self):
  a = ToRadians((self.servos.Angle(self.shoulder), self.servos.Angle(self.foreleg)))
  p = self.PositionFromAngles(a)
  return self.LegToRobotCoordinates(p)
  
#
############################################################################################
#
# Test program
#

def Prompt():
    print("Commands: ")
    print(" s - set servo number")
    print(" a - set servo angle")
    print(" p - print servo angles")
    print(" g - quick to x, y position")
    print(" l - straight line to position")
    print(" x - what is the position")
    print(" q - quit")


servos = Servos()
servos.LoadZeros()
leg = Leg(9, 8, 1, servos) 
c = ' '
servo = 0
Prompt()
while c != 'q':
    c = input("Command: ")
    if c == 's':
        servo = int(input("Set servo to: "))
    elif c == 'a':
        servos.SetAngle(servo, float(input("Set servo " + str(servo) + " angle to: ")))
    elif c == 'p':
        print("Servo Angle")
        for s in range(servoCount):
            print(str(s) + " " + str(servos.Angle(s)))
    elif c == 'g':
    	p = input("Desired x, y position: ")
    	p = p.split(",")
    	p = (float(p[0]), float(p[1]))
    	leg.QuickToPoint(p)
    elif c == 'l':
    	p = input("Go straight tp x, y position at velocity: ")
    	p = p.split(",")
    	v = float(p[2])
    	p = (float(p[0]), float(p[1]))
    	leg.StraightToPoint(p, v)
    elif c == 'x':
    	print("At " + str(leg.GetPoint()))
    elif c == 'q':
        pass
    else:
        Prompt()

servos.Relax()

