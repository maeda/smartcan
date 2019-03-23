#!/usr/bin/env python

import atexit
from picamera import PiCamera
import RPi.GPIO as GPIO 
from time import sleep

INPUT_PIN = 18
OUTPUT_PIN = 25


def cleanup_gpio():
    print('Cleaning up GPIO and exiting...')
    GPIO.cleanup()


def init_pins():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(OUTPUT_PIN, GPIO.OUT)


def main():
    atexit.register(cleanup_gpio)
    init_pins()

    # Give feedback to user of camera initialization and warm up. 
    GPIO.output(OUTPUT_PIN, GPIO.HIGH)
    
    camera = PiCamera()
    sleep(2)
    
    print('Camera ready!')
    GPIO.output(OUTPUT_PIN, GPIO.LOW)

    counter = 0
    while True:
        if GPIO.input(INPUT_PIN) == False:
            GPIO.output(OUTPUT_PIN, GPIO.HIGH)
            filename = 'photo_' + str(counter) + '.jpg'
            print(filename)
            camera.capture(filename)
            GPIO.output(OUTPUT_PIN, GPIO.LOW)
            counter += 1
            sleep(.3)
    
        sleep(.01)


if __name__ == '__main__':
    main()
