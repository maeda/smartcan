#!/home/pi/smartcan/venv/bin/python

from time import sleep

import atexit
import os
import requests

from time import sleep, time

import datastore as datastore

import proximity_sensor

import RPi.GPIO as GPIO

from model.image_model import TrashModel

from dotenv import load_dotenv
load_dotenv()

class AppConfig:
    def __init__(self, pinout={
        'BTN_INPUT_PIN': 18,
        'LED_CTRL_OUTPUT_PIN': 25,
        'LED_RECYCLABLE_OUTPUT_PIN': 15,
        'LED_NON_RECYCLABLE_OUTPUT_PIN': 7
    }):
        self.pinout = pinout

        self._setup()

    def _cleanup_gpio(self):
        print('Cleaning up GPIO and exiting...')
        GPIO.cleanup()

    def _init_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pinout['BTN_INPUT_PIN'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pinout['LED_CTRL_OUTPUT_PIN'], GPIO.OUT)
        GPIO.setup(self.pinout['LED_RECYCLABLE_OUTPUT_PIN'], GPIO.OUT)
        GPIO.setup(self.pinout['LED_NON_RECYCLABLE_OUTPUT_PIN'], GPIO.OUT)

    def _setup(self):
        atexit.register(self._cleanup_gpio)
        self._init_pins()

        # Give feedback to user of camera initialization and warm up.
        GPIO.output(self.pinout['LED_CTRL_OUTPUT_PIN'], GPIO.HIGH)

        from picamera import PiCamera

        self.camera = PiCamera()
        sleep(2)

        print('Camera ready!')
        GPIO.output(self.pinout['LED_CTRL_OUTPUT_PIN'], GPIO.LOW)
        GPIO.output(self.pinout['LED_RECYCLABLE_OUTPUT_PIN'], GPIO.LOW)
        GPIO.output(self.pinout['LED_NON_RECYCLABLE_OUTPUT_PIN'], GPIO.LOW)

    def __del__(self):
        self._cleanup_gpio()

    def run(self, app):
        if proximity_sensor.is_there_object_near():
            GPIO.output(self.pinout['LED_CTRL_OUTPUT_PIN'], GPIO.HIGH)
            filename = 'photo_' + str(int(time())) + '.jpg'
            self.camera.capture(filename)
            class_output = app.classify(filename)
            print(class_output)
            GPIO.output(self.pinout['LED_CTRL_OUTPUT_PIN'], GPIO.LOW)
            if class_output == 'recyclable':
                GPIO.output(self.pinout['LED_RECYCLABLE_OUTPUT_PIN'], GPIO.HIGH)
                sleep(1)
                GPIO.output(self.pinout['LED_RECYCLABLE_OUTPUT_PIN'], GPIO.LOW)

                app.store_file(filename, 'data-collection/recyclable/' + filename)
            if class_output == 'nonrecyclable':
                GPIO.output(self.pinout['LED_NON_RECYCLABLE_OUTPUT_PIN'], GPIO.HIGH)
                sleep(1)
                GPIO.output(self.pinout['LED_NON_RECYCLABLE_OUTPUT_PIN'], GPIO.LOW)

                app.store_file(filename, 'data-collection/nonrecyclable/' + filename)

            sleep(.3)


class OfflineApp:
    def __init__(self):
        super().__init__()
        self.model = TrashModel()
        self.model.load_weights('/home/pi/trashclassifier/model/first_try.h5')

    def classify(self, filename):
        return self.model.classifier(filename)

    def store_file(self, origin, dest):
        os.rename(origin, dest)


class OnlineApp:
    def __init__(self):
        super().__init__()

    def classify(self, filename):
        with open(filename, 'rb') as f:
            return requests.post(os.environ.get('SERVICE_ENDPOINT'), files={'pic.jpg': f})

    def store_file(self, origin, dest):
        datastore.move_object(origin, dest)


def run(app, online_app, offline_app):

    try:
        app.run(online_app)

    except:
        app.run(offline_app)


if __name__ == '__main__':

    app = AppConfig()
    online_app = OnlineApp()
    offline_app = OfflineApp()

    while True:
        run(app, online_app, offline_app)
        sleep(.1)
