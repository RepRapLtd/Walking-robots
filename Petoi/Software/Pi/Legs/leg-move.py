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
    a = a + angleOffsets[servo]
    kit.servo[servo].angle = a
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

def GoToPoint(p)
 p = (l1 + l2 - p[1], p[0])
 angles = AnglesFromPosition(p)
 if angles[0]:
  a = angles[1]
  SetAngle(shoulder, direction[shoulder]*a[0]*180.0/maths.pi)
  SetAngle(foreleg, direction[foreleg]*a[1]*180.0/maths.pi) 
 else:
  print("No can do")
  
def GetPoint():
 a = (direction[shoulder]*angle[shoulder]*maths.pi/180.0, direction[forearm]*angle[forearm]*maths.pi/180.0)
 p = PositionFromAngles(a)
 p = (p[1] - l1 - l2, p[0])
 return p


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
