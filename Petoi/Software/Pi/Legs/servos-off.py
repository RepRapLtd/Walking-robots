
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

for servo in range(16):
    kit.servo[servo]._pwm_out.duty_cycle = 0

