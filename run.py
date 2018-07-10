#!/home/pi/trashclassifier/venv/bin/python

import atexit
from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
import os
import time


class TrashApp(object):
    def __init__(self, dataset_path, model_weights_file, model, pinout={
        'BTN_INPUT_PIN': 18,
        'LED_CTRL_OUTPUT_PIN': 25,
        'LED_RECYCLABLE_OUTPUT_PIN': 15,
        'LED_NON_RECYCLABLE_OUTPUT_PIN': 7
    }):
        self.dataset_path = dataset_path
        self.model_weights_file = model_weights_file
        self.model = model
        self.model.load_weights(model_weights_file)
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

        self.camera = PiCamera()
        sleep(2)

        print('Camera ready!')
        GPIO.output(self.pinout['LED_CTRL_OUTPUT_PIN'], GPIO.LOW)
        GPIO.output(self.pinout['LED_RECYCLABLE_OUTPUT_PIN'], GPIO.LOW)
        GPIO.output(self.pinout['LED_NON_RECYCLABLE_OUTPUT_PIN'], GPIO.LOW)

    def __del__(self):
        self._cleanup_gpio()

    def run(self):

        if GPIO.input(self.pinout['BTN_INPUT_PIN']) == False:
            GPIO.output(self.pinout['LED_CTRL_OUTPUT_PIN'], GPIO.HIGH)
            filename = 'photo_' + str(int(time.time())) + '.jpg'
            self.camera.capture(filename)
            class_output = self.model.classifier(filename)
            print(class_output)
            GPIO.output(self.pinout['LED_CTRL_OUTPUT_PIN'], GPIO.LOW)
            if class_output == 'recyclable':
                GPIO.output(self.pinout['LED_RECYCLABLE_OUTPUT_PIN'], GPIO.HIGH)
                sleep(1)
                GPIO.output(self.pinout['LED_RECYCLABLE_OUTPUT_PIN'], GPIO.LOW)
                os.rename(filename, self.dataset_path + '/recyclable/' + filename)
            if class_output == 'nonrecyclable':
                GPIO.output(self.pinout['LED_NON_RECYCLABLE_OUTPUT_PIN'], GPIO.HIGH)
                sleep(1)
                GPIO.output(self.pinout['LED_NON_RECYCLABLE_OUTPUT_PIN'], GPIO.LOW)
                os.rename(filename, self.dataset_path + '/nonrecyclable/' + filename)

            sleep(.3)


if __name__ == '__main__':
    from model.image_model import TrashModel, TrashVggModel

    trash_app = TrashApp('/home/pi/trashclassifier/data-collection', '/home/pi/trashclassifier/model/pretrained_vgg.h5',
                         TrashVggModel())
    while (True):
        trash_app.run()
        sleep(.1)
