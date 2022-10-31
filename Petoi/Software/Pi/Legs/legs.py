#
# Petoi Bittle Control Program For a Raspberry Pi
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

import time
import math as maths
from adafruit_servokit import ServoKit
import smbus

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

# Time

toNanoseconds = 1e9

# Convert (a1, a2) between degrees and radians

def ToDegrees(a):
 return (a[0]*toDegrees, a[1]*toDegrees)

def ToRadians(a):
 return (a[0]*toRadians, a[1]*toRadians)
 
###########################################################################################
#
# The LTC 2990 Quad I2C Voltage, Current and Temperature Monitor is used to
# measure the output from the Hall effect sensors that determine if a foot is touching a 
# surface or not.
#

# 
# LTC 2990 Quad I2C Voltage, Current and Temperature Monitor
# Retrieves LTC2990 register and performs some basic operations.
# Specs: http://www.linear.com/product/LTC2990
# Source: https://github.com/rfrht/ltc2990
#
# Copyright (C) 2015 Rodrigo A B Freire
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.
#
#--------------------------------------------------------
#
# Updated to Python3 and made into a class by
#
# Adrian Bowyer
# RepRap Ltd
# https://reprapltd.com
#
# 26 May 2022
#


class AToD:
 
 def __init__(self):
  self.bus = smbus.SMBus(1)   # 512-MB RPi the bus is 1. Otherwise, bus is 0.

# Pro tip: Ensure that ADR0 and ADR1 are grounded. Do not let them
# open. Otherwise, the i2c address will randomly change.

  self.address = 0x4c         # I2C chip address
#  self.mode = 0x5f            # Register 0x01 mode select - single aquisition
  self.mode = 0x1f            # Register 0x01 mode select - repeated aquisition
  err = ""

  try:
   if self.bus.read_byte_data(self.address, 0x01) != self.mode: # If current IC mode != program mode
    self.bus.write_byte_data(self.address, 0x01, self.mode)    # Initializes the IC and set mode
    self.bus.write_byte_data(self.address, 0x02, 0x00)    # Trigger a initial data collection
    time.sleep(1)				# Wait a sec, just for init
  except (IOError, err):
   print(err)
   
# Check for a specific bit value
   
 def GetBit(self, number, bit):
  return (number >> bit) & 1 
  
# 2 bytes to Chip temperature

 def GetTemperature(self, msb, lsb):
  msb = format(msb, '08b')
  msb = msb[3:]
  lsb = format(lsb, '08b')
  temp = msb + lsb
  temp = int(temp, 2)/16
  return temp

# 2 bytes to voltage
 
 def GetVoltage(self, msb, lsb):
  msb = format(msb, '08b')
  msb = msb[1:]
  lsb = format(lsb, '08b')
  signal = self.GetBit(int(msb, 2),6)
  #print "positive:0 negative:1 %s" %signal
  volt = msb[1:] + lsb
  volt = int(volt, 2) * 0.00030518
  return volt

# Return everything the chip knows as a printable string

 def GetAllValues(self):
  if self.mode is 0x5f:
   self.bus.write_byte_data(self.address, 0x02, 0x00) # Trigger a data collection
   time.sleep(0.1)
  r0 = self.bus.read_byte_data(self.address, 0x00) # Status
  r1 = self.bus.read_byte_data(self.address, 0x01) # Control - mode select
  r4 = self.bus.read_byte_data(self.address, 0x04) # Temp. Int. MSB
  r5 = self.bus.read_byte_data(self.address, 0x05) # Temp. Int. LSB
  r6 = self.bus.read_byte_data(self.address, 0x06) # V1, V1 - V2 or TR1 MSB
  r7 = self.bus.read_byte_data(self.address, 0x07) # V1, V1 - V2 or TR1 LSB
  r8 = self.bus.read_byte_data(self.address, 0x08) # V2, V1 - V2 or TR1 MSB
  r9 = self.bus.read_byte_data(self.address, 0x09) # V2, V1 - V2 or TR1 LSB
  ra = self.bus.read_byte_data(self.address, 0x0a) # V3, V3 - V4 or TR2 MSB
  rb = self.bus.read_byte_data(self.address, 0x0b) # V3, V3 - V4 or TR2 LSB
  rc = self.bus.read_byte_data(self.address, 0x0c) # V4, V3 - V4 or TR2 MSB
  rd = self.bus.read_byte_data(self.address, 0x0d) # V4, V3 - V4 or TR2 LSB
  re = self.bus.read_byte_data(self.address, 0x0e) # Vcc MSB
  rf = self.bus.read_byte_data(self.address, 0x0f) # Vcc LSB
  result = "Status register: " + hex(r0) + "\n"
  result += "Control register: " + hex(r1) + "\n"
  result += "Int. Temp. : " + str(self.GetTemperature(r4,r5)) + " Celsius\n"
  result += "Voltage V0 : " + str(self.GetVoltage(r6,r7)) + " V\n"
  result += "Voltage V1 : " + str(self.GetVoltage(r8,r9)) + " V\n"
  result += "Voltage V2 : " + str(self.GetVoltage(ra,rb)) + " V\n"
  result += "Voltage V3 : " + str(self.GetVoltage(rc,rd)) + " V\n" 
  result += "Supply: " + str(self.GetVoltage(re,rf) + 2.5) + " V\n"

  # If you want to use TR, use the temperature(msb,lsb) function to get the
  # value. I.e., if you have set the mode TR1 & TR2 (mode 0x5d),
  # Comment the print "Voltage" lines and uncomment these ones:
  # TR1
  # print "Temperature TR1: %s Celsius" %temperature(r6,r7)
  # TR2
  # print "Temperature TR2: %s Celsius" %temperature(ra,rb)
  
  return result

#
# Voltage on one of the four channels.
#

 def Voltage(self, channel):
  msb = channel*2 + 0x06
  lsb = msb + 1
  if self.mode is 0x5f:
   self.bus.write_byte_data(self.address, 0x02, 0x00) # Trigger a data collection
   time.sleep(0.1) # 100 ms is horribly long...
  msb = self.bus.read_byte_data(self.address, msb)
  lsb = self.bus.read_byte_data(self.address, lsb)  
  return self.GetVoltage(msb, lsb)

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
# Get the offsets from the file zero-angles.
#

 def LoadZeros(self):
  with open('zero-angles') as file:
   for line in file:
    l = line.split()
    servo = int(l[0])
    a = float(l[1])
    d = float(l[2])
    self.angleOffsets[servo] = a
    self.direction[servo] = d
    
#
# Move the servos to their zero positions
#     
     
 def GoToZeros(self):
  for servo in range(servoCount):
   self.angle[servo] = 0.0
   if self.angleOffsets[servo] < 0.0:
    # No servo at this location - disable the PWM
    self.kit.servo[servo]._pwm_out.duty_cycle = 0
   else:
     self.kit.servo[servo].angle = self.angleOffsets[servo]
  

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

 def __init__(self, servos, shoulder, foreleg, aToD, foot):
  self.servos = servos
  self.shoulder = shoulder
  self.foreleg = foreleg
  self.aToD = aToD
  self.foot = foot
  self.l1 = humerus
  self.l2 = ulna
  self.p = (0.0, 0.0)
  self.step = 1.0
  self.lineActive = False
  self.rowActive = False
  self.lineWasActive = False
  self.rowWasActive = False

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
# Move in a straight line to p at v mm/s.
# The first function sets up the needed variables.
# Everything works in nanoseconds, which is a bit OTT,
# but that's what the Python time class gives us.
#

 def StraightToPoint(self, p, v):
  diff = (p[0] - self.p[0], p[1] - self.p[1])
  d = maths.sqrt(diff[0]*diff[0] + diff[1]*diff[1])
  if d < resolution:
   return
  self.lineStepsRemaining = int(0.5 + d/self.step)
  dStep = d/self.lineStepsRemaining
  self.dInc = (dStep*diff[0]/d, dStep*diff[1]/d)
  self.tStep = toNanoseconds*dStep/v
  self.nextLineStepTime = time.monotonic_ns()
  self.lineActive = True
  self.lineWasActive = True

#
# This moves the leg a step at a time. If it's not time to
# move it returns immediately.
#
  
 def StepLine(self):
  if not self.lineActive:
   return
  t = time.monotonic_ns()
  if t < self.nextLineStepTime:
   return
  p = (self.p[0] + self.dInc[0], self.p[1] + self.dInc[1])
  self.QuickToPoint(p)
  self.lineStepsRemaining -= 1
  if self.lineStepsRemaining <= 0:
   self.lineActive = False
   self.lineWasActive = False
   return
  self.nextLineStepTime += self.tStep

#
# Set up a loop of lines representing a row.
#
   
 def Row(self, rowPoints):
  self.rowPoints = rowPoints
  self.nextRowSegment = 0
  self.rowActive = True
  self.rowWasActive = True

#
# This increments the row to the next line segment if the last
# is finished
#
 
 def StepRow(self):
  if not self.rowActive:
   return
  if self.lineActive:
   return
  pv = self.rowPoints[self.nextRowSegment]
  self.StraightToPoint(pv[0], pv[1])
  self.nextRowSegment = (self.nextRowSegment + 1) % len(self.rowPoints)
  
#
# Is the leg doing anything?
#
  
 def Active(self):
  return self.lineActive or self.RowActive

#
# Crude timesharing. This function should be called in
# a tight loop all the time.
#
  
 def Spin(self):
  self.StepLine()
  self.StepRow()
   
#
# Stop anything that the leg is doing immediately.
#
   
 def Stop(self):
  self.lineWasActive = self.lineActive
  self.rowWasActive = self.rowActive
  self.lineActive = False
  self.rowActive = False

#
# Resume whatever was being done, if anything
#

 def Resume(self):
  self.lineActive = self.lineWasActive
  if self.lineActive:
   self.nextLineStepTime = time.monotonic_ns() 
  self.rowActive = self.rowWasActive
   
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
# The voltage on the foot Hall sensor
#

 def FootVoltage(self):
  return self.aToD.Voltage(self.foot)
  
#
############################################################################################
#
# Test program
#

def Prompt():
    print("Commands: ")
    print(" n - set servo number")
    print(" a - set servo angle")
    print(" p - print servo angles")
    print(" g - quick to x, y position")
    print(" l - straight line to position")
    print(" r - set row points")
    print(" s - spin the line for N seconds")
    print(" S - stop all movement")
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
    elif c == 'S':
    	leg.Stop()
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

