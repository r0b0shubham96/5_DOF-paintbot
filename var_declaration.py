import RPi.GPIO as GPIO
import smbus
import serial

base_gear = 110/15
link1_gear = 1/1
link2_gear = 50/12
wrist_gear = 1/1

l1_dir_up = 1
l1_dir_down = 0

wrist_dir_up = 0
wrist_dir_down = 1
wrist_dir_left = 2
wrist_dir_right = 3

wrist1_right_dir_up = GPIO.LOW
wrist1_right_dir_down = GPIO.HIGH

wrist2_left_dir_up = GPIO.HIGH
wrist2_left_dir_down = GPIO.LOW

base_dir_left = GPIO.LOW
base_dir_right = GPIO.HIGH

l2_dir_up = GPIO.HIGH
l2_dir_down = GPIO.LOW

on = GPIO.HIGH
off = GPIO.LOW

driver_setup_pulses = 1600
l2_driver_setup_pulse = 400

## pin numbers [Pulse, Direction,  Enable]
wrist1_pins = [17, 27, 22]    # Rpi pins 11, 13, 15
wrist2_pins = [10, 9, 11]    # Rpi pins 19, 21, 23
link2_pins = [5, 6, 12]    # Rpi pins 29, 31, 32
base_pins = [13, 19, 26]    # Rpi pins 33, 35, 37
link1_pins = [23, 24, 24]    # Rpi pins 16, 18
prox_pins = [25, 8, 7, 16, 20, 21]    # Rpi pins 22, 24, 26, 36, 38, 40
relay1 = 14                   # Rpi pin 8
relay2 = 15					  # Rpi pin 9

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(link1_pins[0], GPIO.OUT)
link1_pin0 = GPIO.PWM(link1_pins[0], 100)
link1_pin0.start(0)

address_mega = 0x04
address_nano = 0x05

bus = smbus.SMBus(1)

base_encoder_total_pulse = 1440
link1_encoder_total_pulse = 10000
link2_encoder_total_pulse = 1440

port = "/dev/ttyUSB0"