import math as maths
from adafruit_servokit import ServoKit

servoCount = 16

# Leg humerus and radius/ulna lengths

humerus = 45
ulna = 49

toDegrees = 180.0/maths.pi
toRadians = 1.0/toDegrees

# Convert (a1, a2) between degrees and radians

def ToDegrees(a):
 return (a[0]*toDegrees, a[1]*toDegrees)

def ToRadians(a):
 return (a[0]*toRadians, a[1]*toRadians)

 
class Servos:

 def __init__(self):
  self.kit = ServoKit(channels=servoCount)
  self.angle = [0]*servoCount
  self.angleOffsets = [0]*servoCount
  self.direction = [1.0]*servoCount

 def LoadZeros(self):
  with open('zero-angles') as file:
   for line in file:
    l = line.split()
    servo = int(l[0])
    a = float(l[1])
    d = float(l[2])
    if a < 0.0:
     self.kit.servo[servo]._pwm_out.duty_cycle = 0
    else:
     self.kit.servo[servo].angle = a
     self.angleOffsets[servo] = a
     self.angle[servo] = 0.0
     self.direction[servo] = d

 # degrees

 def SetAngle(self, servo, a):
    a1 = self.direction[servo]*a + self.angleOffsets[servo]
    self.kit.servo[servo].angle = a1
    self.angle[servo] = a
    
 def Angle(self, servo):
  return self.angle[servo]
  
 def Relax(self):
 for servo in range(servoCount):
    self.kit.servo[servo]._pwm_out.duty_cycle = 0
  

    
class Leg:

 def __init__(self, shoulder, foreleg, foot, servos):
  self.shoulder = shoulder
  self.foreleg = foreleg
  self.foot = foot
  self.servos = servos
  self.l1 = humerus
  self.l2 = ulna
  
 def RobotToLegCoordinates(p):
  return (self.l1 + self.l2 - p[1], p[0])

 def LegToRobotCoordinates(p):
  return (p[1], self.l1 + self.l2 - p[0])
  
 # Forward kinematics; uses radians

 def PositionFromAngles(self, angles):
  x = self.l1*maths.cos(angles[0]) + self.l2*maths.cos(angles[0]+angles[1])
  y = self.l1*maths.sin(angles[0]) + self.l2*maths.sin(angles[0]+angles[1])
  return (x,y)

 # Reverse kinematics; uses radians

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

 def GoToPoint(self, p):
  p = self.RobotToLegCoordinates(p)
  angles = AnglesFromPosition(p)
  if angles[0]:
   a = ToDegrees(angles[2])
   self.servos.SetAngle(self.shoulder, a[0])
   self.servos.SetAngle(self.foreleg, a[1]) 
  else:
   print("No can do")
  
 def GetPoint(self):
  a = ToRadians((self.servos.Angle(self.shoulder), self.servos.Angle(self.foreleg)))
  p = PositionFromAngles(a)
  return LegToRobotCoordinates(p)
  
def Prompt():
    print("Commands: ")
    print(" s - set servo number")
    print(" a - set servo angle")
    print(" p - print servo angles")
    print(" g - go to x, y position")
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
    	p = tuple(float(x) for x in p.split(","))
    	leg.GoToPoint(p)
    elif c == 'd':
    	d = float(input("Servo " + str(servo) + " direction: "))
    	direction[servo] = d
    elif c == 'x':
    	print("At " + str(leg.GetPoint()))
    elif c == 'q':
        pass
    else:
        Prompt()

servos.Relax()

