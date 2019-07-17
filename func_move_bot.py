import time
import RPi.GPIO as GPIO
import var_declaration as vd
from time import sleep
import serial
import smbus
import struct
import ast
import binascii

def gpio_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(vd.wrist1_pins[0], GPIO.OUT)
    GPIO.setup(vd.wrist1_pins[1], GPIO.OUT)
##    GPIO.setup(vd.wrist1_pins[2], GPIO.OUT)

    GPIO.setup(vd.wrist2_pins[0], GPIO.OUT)
    GPIO.setup(vd.wrist2_pins[1], GPIO.OUT)
##    GPIO.setup(vd.wrist2_pins[2], GPIO.OUT)

    GPIO.setup(vd.link2_pins[0], GPIO.OUT)
    GPIO.setup(vd.link2_pins[1], GPIO.OUT)
##    GPIO.setup(vd.link2_pins[2], GPIO.OUT)

    GPIO.setup(vd.base_pins[0], GPIO.OUT)
    GPIO.setup(vd.base_pins[1], GPIO.OUT)
##    GPIO.setup(vd.base_pins[2], GPIO.OUT)

    GPIO.setup(vd.link1_pins[0], GPIO.OUT)
    GPIO.setup(vd.link1_pins[1], GPIO.OUT)
    
    GPIO.setup(vd.prox_pins[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(vd.prox_pins[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(vd.prox_pins[2], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(vd.prox_pins[3], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(vd.prox_pins[4], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(vd.prox_pins[5], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#    GPIO.setup(relay1, GPIO.OUT)
#    GPIO.setup(relay2, GPIO.OUT)
    
 
def i2c_setup():
#   vd.bus.write_byte(vd.address_mega, 0xFF)
#   vd.bus.write_byte(vd.address_nano,0xFF)
    time.sleep(1)

def read_i2c(address):
   return (vd.bus.read_i2c_block_data(address, 1))

def writeNumber(address, value):
   vd.bus.write_byte(address, value)
   # bus.write_byte(address_2, value)
#    # bus.write_byte_data(address, 0, value)
   return -1

def write_i2c(angle, direc, homing, address):
   data = "<a" + str(angle) + 'd' + str(direc) + 'h' + str(homing) + '>'
   data_list = list(data)
   
   for i in data_list:
       #Sends to the Slaves 
       writeNumber(address, int(ord(i)))
       sleep(.1)
   
   writeNumber(address, int(0x0A))

# def read_nano_i2c():
#    return (vd.bus.read_i2c_block_data(vd.address_nano, 1))

def base_read_encoder():
    block = read_i2c(vd.address_mega)
    byte_encoder = binascii.hexlify(bytearray(block[0:4]))
    encoder_pulse = struct.unpack('f', bytes.fromhex(byte_encoder.decode("utf-8")))[0]
    return ((encoder_pulse * 360)/vd.base_encoder_total_pulse)

def link2_read_encoder():
    block = read_i2c(vd.address_mega)
    byte_encoder = binascii.hexlify(bytearray(block[4:8]))
    encoder_pulse = (struct.unpack('f', bytes.fromhex(byte_encoder.decode("utf-8")))[0])
    return ((encoder_pulse * 360)/vd.link2_encoder_total_pulse)

def link1_read_encoder():
    block = read_i2c(vd.address_nano)
    byte_encoder = binascii.hexlify(bytearray(block[0:4]))
    encoder_pulse = (struct.unpack('f', bytes.fromhex(byte_encoder.decode("utf-8")))[0])
    return ((encoder_pulse * 360)/vd.link1_encoder_total_pulse)

def angle_calculate_w(gear_ratio, angle):
    input_angle = angle * gear_ratio
    return ((input_angle/360) * 6400)
#    return ((input_angle/360) * vd.driver_setup_pulses)
def angle_calculate(gear_ratio, angle):
    input_angle = angle * gear_ratio
    return ((input_angle/360) * vd.driver_setup_pulses)

def time_pulse_calculate(time, total_pulses):
    if (total_pulses == 0):
        return 0
    return (time/total_pulses)

def wrist_direction(direction):
    if (direction == vd.wrist_dir_up):
        GPIO.output(vd.wrist1_pins[1], GPIO.LOW)
        GPIO.output(vd.wrist2_pins[1], GPIO.HIGH)
    elif(direction == vd.wrist_dir_down):
        GPIO.output(vd.wrist1_pins[1], GPIO.HIGH)
        GPIO.output(vd.wrist2_pins[1], GPIO.LOW)
    elif(direction == vd.wrist_dir_left):
        GPIO.output(vd.wrist1_pins[1], GPIO.HIGH)
        GPIO.output(vd.wrist2_pins[1], GPIO.HIGH)
    elif(direction == vd.wrist_dir_right):
        GPIO.output(vd.wrist1_pins[1], GPIO.LOW)
        GPIO.output(vd.wrist2_pins[1], GPIO.LOW)

def wrist_run(angle, time, direction):
    total_pulses = angle_calculate_w(vd.wrist_gear, angle)
    time_pulses = time_pulse_calculate(time, total_pulses)
    wrist_direction(direction)

    i = 0
    while (i < total_pulses):
        GPIO.output(vd.wrist1_pins[0], GPIO.HIGH)
        GPIO.output(vd.wrist2_pins[0], GPIO.HIGH)
        sleep(time_pulses/2)
        GPIO.output(vd.wrist1_pins[0], GPIO.LOW)
        GPIO.output(vd.wrist2_pins[0], GPIO.LOW)
        sleep(time_pulses/2)
        i += 1
    
def wrist1_run(angle, time, direction):
    total_pulses = angle_calculate(vd.wrist_gear, angle)
    time_pulses = time_pulse_calculate(time, total_pulses)
    GPIO.output(vd.wrist1_pins[1], direction)
    
    i = 0
    while (i < total_pulses):
        GPIO.output(vd.wrist1_pins[0], GPIO.HIGH)
        sleep(time_pulses/2)
        GPIO.output(vd.wrist1_pins[0], GPIO.LOW)
        sleep(time_pulses/2)
        i += 1

def wrist2_run(angle, time, direction):
    total_pulses = angle_calculate(vd.wrist_gear, angle)
    time_pulses = time_pulse_calculate(time, total_pulses)
    GPIO.output(vd.wrist2_pins[1], direction)
    
    i = 0
    while (i < total_pulses):
        GPIO.output(vd.wrist2_pins[0], GPIO.HIGH)
        sleep(time_pulses/2)
        GPIO.output(vd.wrist2_pins[0], GPIO.LOW)
        sleep(time_pulses/2)
        i += 1

def wrist1_direction(angle_vert, angle_horiz):
    if ((angle_vert + angle_horiz) >= 0):
        return vd.wrist1_right_dir_up
    else:
        return vd.wrist1_right_dir_down

def wrist2_direction(angle_vert, angle_horiz):
    if ((angle_vert + angle_horiz) >= 0):
        return vd.wrist1_right_dir_up
    else:
        return vd.wrist1_right_dir_down

def link2_run(angle, time, direction):
    total_pulses = angle_calculate(vd.link2_gear, angle)
#    input_angle = angle * vd.link2_gear
#    total_pulses = ((input_angle/360) * vd.l2_driver_setup_pulse)
    time_pulses = time_pulse_calculate(time, total_pulses)
    GPIO.output(vd.link2_pins[1], direction)
    
    i = 0

    while (i < total_pulses):
        GPIO.output(vd.link2_pins[0], GPIO.HIGH)
        sleep(time_pulses/2)
        GPIO.output(vd.link2_pins[0], GPIO.LOW)
        sleep(time_pulses/2)
        i += 1
        
def base_run(angle, time, direction):
    total_pulses = angle_calculate(vd.base_gear, angle)
    time_pulses = time_pulse_calculate(time, total_pulses)
    GPIO.output(vd.base_pins[1], direction)
    
    i = 0

    while (i < total_pulses):
        GPIO.output(vd.base_pins[0], GPIO.HIGH)
#        GPIO.output(vd.wrist2_pins[0], GPIO.LOW)
        sleep(time_pulses/2)
        GPIO.output(vd.base_pins[0], GPIO.LOW)
#        GPIO.output(vd.wrist2_pins[0], GPIO.HIGH)
        sleep(time_pulses/2)
        i += 1

def link1_run(angle, direction, homing):
    data = "<a" + str(angle) + 'd' + str(direction) + 'h' + str(homing) + '>'
    ArduinoSerial.write(data.encode())
#    write_i2c(angle, direction, homing, vd.address_nano)


def stepper_run(pins, gear_ratio, angle, time, direction):
    total_pulses = angle_calculate(gear_ratio, angle)
    if (total_pulses == 0):
        time_pulses = 0
    else:
        time_pulses = time_pulse_calculate(time, total_pulses)
    GPIO.output(pins[1], direction)
    
    i = 0

    while (i < total_pulses):
        GPIO.output(pins[0], GPIO.HIGH)
        sleep(time_pulses/2)
        
        with open("/home/pi/Documents/new-paint-bot/pause.txt") as file:
            pa=ast.literal_eval(file.read()) #This whole things helps in working of pause and resume control of GUI
        while str(pa)=='0': # if pa=0, i.e pause button is pressed, so program will keep iterating inside of while loop, thereby practically being stopped until and unless resume button is pressed in the GUI which will make pa=1
            print(" While ... PAUSE ...")
            with open("/home/pi/Documents/new-paint-bot/pause.txt") as file:
                pa=ast.literal_eval(file.read()) # Checking each time in the while loop, waiting for the pa to become 1 i.e. for user to press resume
        
        GPIO.output(pins[0], GPIO.LOW)
        sleep(time_pulses/2)
        i += 1

def wrist_vertical_prox_read():
    return (GPIO.input(vd.prox_pins[0]))

def wrist_horizontal_prox_read():
    return (GPIO.input(vd.prox_pins[1]))

def base_left_prox_read():
    return (GPIO.input(vd.prox_pins[5]))

def base_right_prox_read():
    return (GPIO.input(vd.prox_pins[4]))

def link1_prox_read():
    return (GPIO.input(vd.prox_pins[3]))

def link2_prox_read():
    return (GPIO.input(vd.prox_pins[2]))

def homing_base():
    total_pulses = angle_calculate(vd.base_gear, 70)
    time_pulses = time_pulse_calculate(9, total_pulses)
    GPIO.output(vd.base_pins[1], vd.base_dir_left)
    
    while (base_left_prox_read() != 0):
        GPIO.output(vd.base_pins[0], GPIO.HIGH)
        sleep(time_pulses/2)
        GPIO.output(vd.base_pins[0], GPIO.LOW)
        sleep(time_pulses/2)
    
    GPIO.output(vd.base_pins[1], vd.base_dir_right)
    i = 0
    while (i < total_pulses):
        GPIO.output(vd.base_pins[0], GPIO.HIGH)
        sleep(time_pulses/2)
        GPIO.output(vd.base_pins[0], GPIO.LOW)
        sleep(time_pulses/2)
        i += 1

def homing_wrist():
    total_pulses = angle_calculate(vd.wrist_gear, 42)
    time_pulses = time_pulse_calculate(3.5, total_pulses)
    
    wrist_direction(vd.wrist_dir_up)
    
    while (wrist_vertical_prox_read() != 0):
        GPIO.output(vd.wrist1_pins[0], GPIO.HIGH)
        GPIO.output(vd.wrist2_pins[0], GPIO.HIGH)
        sleep(time_pulses/2)
        GPIO.output(vd.wrist1_pins[0], GPIO.LOW)
        GPIO.output(vd.wrist2_pins[0], GPIO.LOW)
        sleep(time_pulses/2)
    
    wrist_direction(vd.wrist_dir_down)
    i = 0
    while (i < total_pulses):
        GPIO.output(vd.wrist1_pins[0], GPIO.HIGH)
        GPIO.output(vd.wrist2_pins[0], GPIO.HIGH)
        sleep(time_pulses/2)
        GPIO.output(vd.wrist1_pins[0], GPIO.LOW)
        GPIO.output(vd.wrist2_pins[0], GPIO.LOW)
        sleep(time_pulses/2)
        i += 1
        
    total_pulses = angle_calculate(vd.wrist_gear, 36)
    time_pulses = time_pulse_calculate(4.5, total_pulses)    
    wrist_direction(vd.wrist_dir_right)
    
    while (wrist_horizontal_prox_read() != 0):
        GPIO.output(vd.wrist1_pins[0], GPIO.HIGH)
        GPIO.output(vd.wrist2_pins[0], GPIO.HIGH)
        sleep(time_pulses/2)
        GPIO.output(vd.wrist1_pins[0], GPIO.LOW)
        GPIO.output(vd.wrist2_pins[0], GPIO.LOW)
        sleep(time_pulses/2)
    
    wrist_direction(vd.wrist_dir_left)
    
    i = 0
    while (i < total_pulses):
        GPIO.output(vd.wrist1_pins[0], GPIO.HIGH)
        GPIO.output(vd.wrist2_pins[0], GPIO.HIGH)
        sleep(time_pulses/2)
        GPIO.output(vd.wrist1_pins[0], GPIO.LOW)
        GPIO.output(vd.wrist2_pins[0], GPIO.LOW)
        sleep(time_pulses/2)
        i += 1 
        
def homing_link2():
    total_pulses = angle_calculate(vd.link2_gear, 50)
    time_pulses = time_pulse_calculate(5, total_pulses)
    GPIO.output(vd.link2_pins[1], vd.l2_dir_down)

    while (link2_prox_read() != 0):
        GPIO.output(vd.link2_pins[0], GPIO.HIGH)
        sleep(time_pulses/2)
        GPIO.output(vd.link2_pins[0], GPIO.LOW)
        sleep(time_pulses/2)

def homing_link1():
##    send the data to the arduino for homing the link1 using i2c and then wait until we get the data back
##    back when the link1 reached the required home position by checking the encoder data.
    write_i2c(0, 0, 1, vd.address_nano)
    print("Using I2C")

def relay_on():
    GPIO.output(relay1, on)
    GPIO.output(relay2, on)

def relay_off():
    GPIO.output(relay1, off)
    GPIO.output(relay2, off)

def homing():
    homing_base()
    homing_wrist()
    homing_link2()
    homing_link1()         

gpio_setup()
##homing()
##homing()
i2c_setup()
#homing_link1()
##print(base_read_encoder())
##write_i2c(10, 25, vd.address_mega)
##print(base_read_encoder() + 12)
##write_i2c(15, 10, vd.address_mega)
##wrist2_run(4, 0.5, vd.wrist2_left_dir_up)
#wrist_run(8, 1, vd.wrist_dir_right)
##base_run(30, 5, vd.base_dir_right)
#while True:
#    base_run(30, 2, vd.base_dir_left)
##    print(GPIO.input(vd.prox_pins[1]))
#    link2_run(20, 2, vd.l2_dir_down)
#    wrist1_run(8, 1, vd.wrist_dir_down)

#while True:
#    print(wrist_vertical_prox_read())
#    print(wrist_horizontal_prox_read())
#    print(base_left_prox_read())
#    print(base_right_prox_read())
##    print(link1_prox_read())
#    print(link2_prox_read())
#    time.sleep(1)
#    print("--------------------------------\n")

#write_i2c(5, 0, 0, vd.address_nano)
#print(link1_read_encoder())

#wrist_run(30, 0.5, vd.wrist_dir_down)
#ArduinoSerial = serial.Serial(vd.port, 9600)