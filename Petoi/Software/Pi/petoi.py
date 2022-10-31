#
# Petoi Bittle Library For a Raspberry Pi
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
# Test program
#

import rrlpetoi as rrlp

def Prompt():
    print("Commands: ")
    print(" n - set servo number")
    print(" a - set servo angle")
    print(" p - print servo angles")
    print(" g - quick to x, y position")
    print(" l - straight line to position")
    print(" r - set row points")
    print(" s - spin the line for N seconds")
    print(" P - pause all movement")
    print(" R - resume all movement")
    print(" x - what is the position")
    print(" z - zero the servos")
    print(" d - print all A to D data")
    print(" v - print the leg foot voltage")
    print(" q - quit")


servos = Servos()
servos.LoadZeros()
servos.GoToZeros()
aToD = AToD()
leg = Leg(servos, 9, 8, aToD, 1) 
c = ' '
servo = 0
Prompt()
while c != 'q':
    c = input("Command: ")
    if c == 'n':
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
    elif c == 'r':
    	v = 1
    	rowPoints = []
    	while v > 0:
    	 p = input("x, y, v (-v to end): ")
    	 p = p.split(",")
    	 v = float(p[2])
    	 if v > 0:
    	  rowPoints.append( ((float(p[0]), float(p[1])), v) )
    	leg.Row(rowPoints)
    elif c == 's':
    	tEnd = toNanoseconds*int(input("Seconds to spin: ")) + time.monotonic_ns()
    	leg.nextLineStepTime = time.monotonic_ns()
    	while time.monotonic_ns() < tEnd:
    	 leg.Spin()
    elif c == 'P':
    	leg.Pause()
    elif c == 'R':
    	leg.Resume()
    elif c == 'x':
    	print("At " + str(leg.GetPoint()))
    elif c == 'z':
    	servos.GoToZeros()
    elif c == 'd':
    	print(aToD.GetAllValues())
    elif c == 'v':
    	print(str(leg.FootVoltage()))
    elif c == 'q':
        pass
    else:
        Prompt()

servos.Relax()

