import smbus
import time
import struct
import binascii
# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x05

bus.write_byte(address,0xFF)

while (1):
    #block=bus.read_byte(address)
    block = bus.read_i2c_block_data(address, 0, 4)
    block2 = bus.read_i2c_block_data(address, 1)[4:8]
    print ("binary value received is:",block)
    print ("binary value received of block2 is: ", block2)
    a = binascii.hexlify(bytearray(block))
    b = binascii.hexlify(bytearray(block2))
    var = struct.unpack('f', a.decode('hex'))[0]
    var2 = struct.unpack('f', b.decode('hex'))[0]
    print ("converted float is:",var)
    print ("converted float var2 is: ", var2)
    print ("")
    print ("")
    time.sleep(1)
