import math
##import _thread
import time
import RPi.GPIO as GPIO 
from time import sleep

class run_stepper_bot():
    def __init__(self):
        print("Starting motor...")
        
    def move_stepper(pins, gear_ratio, angle, time, direction):
       stepper_run(pins, gear_ratio, angle, time, direction)
    
##    def wrist_stepper(angle, time, direction):
##        wrist_run(angle, time, direction)
    
    def link1_dc():
        print("link1 linear actuator motor starting...")