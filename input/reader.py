#!/usr/bin/env python

from time import sleep
import RPi.GPIO as GPIO 

GPIO.setmode(GPIO.BCM)
INPUT_PIN = 4
GPIO.setup(INPUT_PIN, GPIO.IN)

while True: 
    if (GPIO.input(INPUT_PIN) == True):
        print('3.3')
    else:
        print('0')
    sleep(1);   
