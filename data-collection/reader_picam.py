#!/usr/bin/env python

import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO 

INPUT_PIN = 18
counter = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
camera = PiCamera()

# Allow camera to warm up.
sleep(2)

print('Camera ready!')

while True:
    if GPIO.input(INPUT_PIN) == False:
        filename = 'photo_' + str(counter) + '.jpg'
        print(filename)
        camera.capture(filename)
        counter += 1
        sleep(.3)

    sleep(.01)

