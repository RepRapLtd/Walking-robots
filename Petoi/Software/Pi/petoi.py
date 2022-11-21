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
import imageToASCII as iToA

w = Whiptail(title="RepRap Ltd Quadruped Robot Control Program", backtitle="https://reprapltd.com")

robot = rrlp.Robot()

servos = robot.servos
activeServos = servos.activeServos

aToD = robot.aToD
if aToD.err != "":
 w.msgbox("A to D initialisation error: " + aToD.err)


legs = robot.legs
 
def EditServo(servo):
 loop = True
 options = ["+1", "-1", "+10", "-10", "set angle", "negate direction", "save current angle as offset"]
 while loop:
  menu = w.menu("Servo " + str(servo) + ", angle: " + str(servos.angle[servo]), options)
  loop = menu[1] is 0
  if loop:
   symbol = menu[0]
   if symbol == options[0]:
    servos.SetAngle(servo, servos.angle[servo] + 1)
   elif symbol == options[1]:
    servos.SetAngle(servo, servos.angle[servo] - 1)
   elif symbol == options[2]:
    servos.SetAngle(servo, servos.angle[servo] + 10)
   elif symbol == options[3]:
    servos.SetAngle(servo, servos.angle[servo] - 10)
   elif symbol == options[4]:
    a = str(servos.angle[servo])
    response = w.inputbox("Current angle is " + a + ", set it to: ", default = a)
    if response[1] is 0:
     a = float(response[0])
     servos.SetAngle(servo, a)
   elif symbol == options[5]:
    servos.InvertDirection(servo)
   elif symbol == options[6]:
    servos.MakeCurrentPositionZero(servo)
   else:
    w.msgbox("Dud option: " + symbol)
   
   
def ChooseServo():
 loop = True
 options = ["Zero servos", "Save current positions as zeros"]
 for s in activeServos:
  options.append(str(s))
 while loop:
  menu = w.menu("Choose servo", options)
  loop = menu[1] is 0
  if loop:
   symbol = menu[0]
   if symbol == options[0]:
    servos.GoToZeros()
   elif symbol == options[1]:
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
 options = ["move to position", "row", "load row", "calibrate foot", "calibrate horizontal"]
 while loop:
  p = str(leg.point[0])
  menu = w.menu(leg.name + " leg, at (x, y): " + p, options)
  loop = menu[1] is 0
  if loop:
   symbol = menu[0]
   if symbol == options[0]:
    response = w.inputbox("Currently at " + p + ". Move to a point at a velocity, Type - X Y V: ", default = p + " 20")
    if response[1] is 0:
     response = response[0].split()
     p = (float(response[0]), float(response[1]))
     v = float(response[2])
     spinFor = leg.StraightToPoint([p, v, False])
     t = time.time() + 0.1 + spinFor
     while time.time() < t:
      robot.Spin()
   elif symbol == options[1]:
    response = w.inputbox("Row for how many cycles? ", default = "1")
    if response[1] is 0:
     cycles = int(response[0])
     spinFor = leg.row.RowCycleTime()*cycles
     t = time.time() + 2 + spinFor
     leg.Row()
     while time.time() < t:
      robot.Spin()
     leg.Stop()
   elif symbol == options[2]:
    pass
   elif symbol == options[3]:
    w.msgbox("Lift the " + leg.name + " foot")
    v0 = leg.FootVoltage()
    w.msgbox("Release the" + leg.name + " foot")
    v1 = leg.FootVoltage()
    v = (v0 + v1)*0.5
    leg.SetFootThreshold(v)
    w.msgbox(leg.name + " foot threshold set to " + str(v) + "V from " + str(v0) + "V (lifted) and " + str(v1) + "V (released).")
   else:
    w.msgbox(leg.name + " calibrate horizontal.")
    
    
def ChooseLeg():
 loop = True
 names = []
 for leg in legs:
  names.append(leg.name)
 while loop:
  menu = w.menu("Choose leg", names)
  loop = menu[1] is 0
  if loop:
   EditLeg(GetLegFromName(menu[0]))
   
def DoCamera():
 loop = True
 options = ["Take picture", "Take and save picture"]
 while loop:
  menu = w.menu("Camera", options)
  loop = menu[1] is 0
  if loop:
   if menu[0] == options[0]:
    image = robot.camera.Snap()
    aImage = iToA.CovertImageToAscii(image)
    w.msgbox(aImage)
   elif menu[0] == options[1]: 
    response = w.inputbox("Picture file name (must end in .jpg):", default = "snap.jpg")
    if response[1] is 0:
    response = response[0]
    robot.camera.SnapToFile(response)
    w.msgbox("Image saved in " + response)
   else:
    w.msgbox("Dud option: " + menu[0])

def DoAccelerometer():
 a = robot.accelerometer.Accelerations()
 g = robot.accelerometer.Gyro()
 t = robot.accelerometer.Temperature()
 w.msgbox("Accelerations: " + str(a) + "\nGyros: " + str(g) + "\nChip temp: " + str(t) + " C")

def DoRange():
 d = robot.range.Distance()
 w.msgbox("Range is " + str(d) + "mm") 
 
def DoVoltages():
 w.msgbox(robot.aToD.GetAllValues()) 

loop = True
options = ["servos", "legs", "camera", "accelerometer", "range", "voltages"]
while loop:
 menu = w.menu("Control", options)
 loop = menu[1] is 0
 if loop:
  if menu[0] == options[0]:
   ChooseServo()
  elif menu[0] == options[1]:
   ChooseLeg()
  elif menu[0] == options[2]:
   DoCamera()
  elif menu[0] == options[3]:
   DoAccelerometer()
  elif menu[0] == options[4]:
   DoRange()
  elif menu[0] == options[5]:
   DoVoltages()
  else:      
   w.msgbox("Dud option: " + menu[0])

robot.Shutdown()


