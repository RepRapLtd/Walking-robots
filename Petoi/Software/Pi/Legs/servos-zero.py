
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

with open('zero-angles') as file:
 for line in file:
  l = line.split()
  servo = int(l[0])
  angle = float(l[1])
  if angle < 0.0:
   kit.servo[servo]._pwm_out.duty_cycle = 0
  else:
   kit.servo[servo].angle = angle


