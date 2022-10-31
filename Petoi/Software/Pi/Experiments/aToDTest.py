import smbus
import time
bus = smbus.SMBus(1)
address = 0x77

def AtoDRead(a):
 v = bus.read_byte_data(address,a)
 return v

bus.write_byte(address, 0xff)
for a in range(0, 16):
 v = AtoDRead(a)
 print(hex(a) + ' ' + hex(v))

