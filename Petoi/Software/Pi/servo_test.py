import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

for s in range(0, 15):
 print("Servo " + str(s))
 print(kit.servo[s]._pwm_out.duty_cycle)
 time.sleep(1)
 kit.servo[s].angle = 20
 time.sleep(1)
 kit.servo[s].angle = 0
 time.sleep(1)


