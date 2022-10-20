import time
import sys
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

servoCount = 16
angle = [0]* servoCount

def SetAngle(servo, a):
    kit.servo[servo].angle = a
    angle[servo] = a

def Prompt():
    print("Commands: ")
    print(" s - set servo number")
    print(" a - set servo angle")
    print(" p - print angles and servos")
    print(" q - quit")

for servo in range(servoCount):
    SetAngle(servo, 0.0)
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
        for s in range(servoCount):
            print("Servo "  + str(s) + " has angle " + str(angle[s]))
    elif c == 'q':
        pass
    else:
        Prompt()
