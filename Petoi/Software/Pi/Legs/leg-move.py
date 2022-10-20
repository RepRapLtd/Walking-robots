from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

servoCount = 16
angle = [0]*servoCount
angleOffsets = [0]*servoCount

def LoadZeros():
 with open('zero-angles') as file:
  for line in file:
   l = line.split()
   servo = int(l[0])
   a = float(l[1])
   if a < 0.0:
    kit.servo[servo]._pwm_out.duty_cycle = 0
   else:
    kit.servo[servo].angle = a
    angleOffsets[servo] = a
    angle[servo] = 0.0


def SetAngle(servo, a):
    a = a + angleOffsets[servo]
    kit.servo[servo].angle = a
    angle[servo] = a

def Prompt():
    print("Commands: ")
    print(" s - set servo number")
    print(" a - set servo angle")
    print(" p - print angles and servos")
    print(" q - quit")

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
        for s in range(servoCount):
            print("Servo "  + str(s) + " has angle " + str(angle[s]))
    elif c == 'q':
        pass
    else:
        Prompt()

for servo in range(16):
    kit.servo[servo]._pwm_out.duty_cycle = 0
