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
# Control program
#


from whiptail import Whiptail
import time
import rrlpetoi as rrlp

w = Whiptail(title="RepRap Ltd Quadruped Robot Control Program", backtitle="RepRap Ltd Quadruped Robot Control Program")

servos = rrlp.Servos()
servos.LoadZeros('zero-angles')
servos.GoToZeros()
activeServos = servos.activeServos
aToD = rrlp.AToD()
flLeg = rrlp.Leg(servos, 14, 15, aToD, 0)
frLeg = rrlp.Leg(servos, 9, 8, aToD, 1)
blLeg = rrlp.Leg(servos, 0, 1, aToD, 2)
brLeg = rrlp.Leg(servos, 6, 7, aToD, 3)

legs = ["front left", "front right","back left", "back right"]
 
def EditServo(servo):
 loop = True
 options = ["+1", "-1", "+10", "-10", "negate direction", "save current angle as offset"]
 while loop:
  menu = w.menu("Servo " + str(servo), options)
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
   
def SaveZeros():
 w.msgbox("saved")
   
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
    
def EditLeg(leg):
 loop = True
 while loop:
  menu = w.menu(leg + " leg", ["step", "fold", "b"])
  loop = menu[1] is 0
  if loop:
   symbol = menu[0]
   w.msgbox(symbol + " selected")   
    
def ChooseLeg(legs):
 loop = True
 while loop:
  menu = w.menu("Choose leg", legs)
  loop = menu[1] is 0
  if loop:
   EditLeg(menu[0])
   

loop = True
while loop:
 menu = w.menu("Control", ["servos", "legs"])
 loop = menu[1] is 0
 if loop:
  if menu[0] == "servos":
   ChooseServo(activeServos)
  else:
   ChooseLeg(legs)
 


'''
menu_descriptions = w.menu(
		"This is a menu with descriptions.",
		[("Option 1", "Does Something"), ("Option 2", "Does Something Else")],
		)[0]
print(f"You selected '{menu_descriptions}'")

radiolist = w.radiolist("Choose One", ["Spam, spam, spam, spam", "Egg", "Chips"])[0]
print(f"You selected: '{radiolist}'!")

checklist = w.checklist("Choose Multiple", ["Spam, spam, spam, spam", "Egg", "Chips"])[0]
checklist_str = "' and '".join(checklist)
print(f"You selected: '{checklist_str}'!")

textbox = w.textbox(__file__)
print(textbox)




import time
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


servos = rrlp.Servos()
servos.LoadZeros('zero-angles')
servos.GoToZeros()
aToD = rrlp.AToD()
leg = rrlp.Leg(servos, 9, 8, aToD, 1) 
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
    	tEnd = rrlp.toNanoseconds*int(input("Seconds to spin: ")) + time.monotonic_ns()
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

'''

