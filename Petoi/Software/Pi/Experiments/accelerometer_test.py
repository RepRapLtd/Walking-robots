import time
import board
import adafruit_mpu6050

i2c = board.I2C()
mpu = adafruit_mpu6050.MPU6050(i2c)
for n in range(1, 20):
 print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
 print("Gyro X:%.2f, Y: %.2f, Z: %.2f rad/s" % (mpu.gyro))
 print("Temperature: %.2f C" % mpu.temperature)
 print("")
 time.sleep(1)

