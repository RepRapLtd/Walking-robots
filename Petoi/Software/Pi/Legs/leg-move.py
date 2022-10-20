import math as maths
from adafruit_servokit import ServoKit

servoCount = 16
kit = ServoKit(channels=servoCount)

angle = [0]*servoCount
angleOffsets = [0]*servoCount
direction = [1.0]*servoCount

l1 = 45
l2 = 49

shoulder = 9
foreleg = 8


# Forward kinematics (radians)

def PositionFromAngles(angles):
 x = l1*maths.cos(angles[0]) + l2*maths.cos(angles[0]+angles[1])
 y = l1*maths.sin(angles[0]) + l2*maths.sin(angles[0]+angles[1])
 return (x,y)

# Reverse kinematics (radians)

def AnglesFromPosition(position):
 l12 = l1*l1
 l22 = l2*l2
 xp2 = position[0]*position[0]
 yp2 = position[1]*position[1]
 sigma = -l12*l12 + 2*l12*l22 +2*l12*xp2 + 2*l12*yp2 - l22*l22 +2*l22*xp2 + 2*l22*yp2 - xp2*xp2 -2*xp2*yp2 -yp2*yp2
 if sigma < 0.0:
  print("No reverse kinematic solution for position " + str(position))
  return [False, (0, 0), (0, 0)]
 sigma = maths.sqrt(sigma)
 div = l12 + 2*l1*position[0] - l22 + xp2 + yp2
 a1p = 2*maths.atan2(2*l1*position[1] + sigma, div)
 a1m = 2*maths.atan2(2*l1*position[1] - sigma, div)
 sigma = (-l12 + 2*l1*l2 - l22 + xp2 + yp2)*(l12 + 2*l1*l2 + l22 - xp2 - yp2)
 if sigma < 0.0:
  print("No reverse kinematic solution for position " + str(position))
  return [False, (0, 0), (0, 0)]
 sigma = maths.sqrt(sigma)
 div = -l12 + 2*l1*l2 - l22 + xp2 + yp2
 a2p = 2*maths.atan2(sigma, div)
 return [True, (a1p, -a2p), (a1m, a2p)]

def LoadZeros():
 with open('zero-angles') as file:
  for line in file:
   l = line.split()
   servo = int(l[0])
   a = float(l[1])
   d = float(l[2])
   if a < 0.0:
    kit.servo[servo]._pwm_out.duty_cycle = 0
   else:
    kit.servo[servo].angle = a
    angleOffsets[servo] = a
    angle[servo] = 0.0
    direction[servo] = d

# degrees

def SetAngle(servo, a):
    a1 = direction[servo]*a + angleOffsets[servo]
    kit.servo[servo].angle = a1
    angle[servo] = a

def Prompt():
    print("Commands: ")
    print(" s - set servo number")
    print(" a - set servo angle")
    print(" p - print servos, angles and directions")
    print(" g - go to x, y position")
    print(" x - what is the position")
    print(" d - set servo direction")
    print(" q - quit")

def ToDegrees(a):
 return (a[0]*180.0/maths.pi, a[1]*180.0/maths.pi)

def ToRadians(a):
 return (a[0]*maths.pi/180.0, a[1]*maths.pi/180.0)

def RobotToLegCoordinates(p):
 return (l1 + l2 - p[1], p[0])

def LegToRobotCoordinates(p):
 return (p[1], l1 + l2 - p[0])

def GoToPoint(p):
 p = RobotToLegCoordinates(p)
 #print("To: " + str(p))
 angles = AnglesFromPosition(p)
 if angles[0]:
  a = ToDegrees(angles[2])
  #print("Angles: " + str(a[0]) + " " + str(a[1]))
  SetAngle(shoulder, a[0])
  SetAngle(foreleg, a[1]) 
 else:
  print("No can do")
  
def GetPoint():
 a = ToRadians((angle[shoulder], angle[foreleg]))
 p = PositionFromAngles(a)
 return LegToRobotCoordinates(p)


LoadZeros() 
c = ' '
servo = 0
Prompt()
while c != 'q':
    c = input("Command: ")
    if c == 's':
        servo = int(input("Set servo to: "))
    elif c == 'a':
        SetAngle(servo, float(input("Set servo " + str(servo) + " angle to: ")))
    elif c == 'p':
        print("Servo Angle Direction")
        for s in range(servoCount):
            print(str(s) + " " + str(angle[s]) + " " + str(direction[s]))
    elif c == 'g':
    	p = input("Desired x, y position: ")
    	p = tuple(float(x) for x in p.split(","))
    	GoToPoint(p)
    elif c == 'd':
    	d = float(input("Servo " + str(servo) + " direction: "))
    	direction[servo] = d
    elif c == 'x':
    	print("At " + str(GetPoint()))
    elif c == 'q':
        pass
    else:
        Prompt()

for servo in range(16):
    kit.servo[servo]._pwm_out.duty_cycle = 0
