import math as maths

# Leg (i.e. 2-bar linkage) kinematics

# From https://uk.mathworks.com/help/symbolic/derive-and-apply-inverse-kinematics-to-robot-arm.html

l1 = 58
l2 = 58

# Forward kinematics

def PositionFromAngles(angles):
 x = l1*maths.cos(angles[0]) + l2*maths.cos(angles[0]+angles[1])
 y = l1*maths.sin(angles[0]) + l2*maths.sin(angles[0]+angles[1])
 return (x,y)

# Reverse kinematics

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


while True:
    p = input("Desired x, y position: ")
    pin = tuple(float(x) for x in p.split(","))
    print("Given position: " + str(pin))
    r = AnglesFromPosition(pin)
    if r[0]:
     print("Angles: " + str(r[1]) + " and " + str(r[2]))
     p = PositionFromAngles(r[1])
     print("Recovered position 1: " + str(p))
     p = PositionFromAngles(r[2])
     print("Recovered position 2: " + str(p))
    else:
     print("No solution")
