#!/usr/bin/env python

import cv2
from time import sleep
import RPi.GPIO as GPIO 

INPUT_PIN = 4

counter = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_PIN, GPIO.IN)


def capture(file_path):
	cap = cv2.VideoCapture(0)
	cap.set(10, 200)

	ret, frame = cap.read()

	out = cv2.imwrite(file_path, frame)

	cap.release()
	cv2.destroyAllWindows()


while True: 
    if (GPIO.input(INPUT_PIN) == True):
        capture('photo_' + str(counter) + '.jpg')
        counter += 1
        sleep(.3)

    sleep(.01);
