import RPi.GPIO as GPIO
import time
import os


GPIO.setmode(GPIO.BCM)

PIN_TRIGGER = 23
PIN_ECHO = 24

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)


def is_there_object_near():

    GPIO.output(PIN_TRIGGER, False)

    time.sleep(1)

    GPIO.output(PIN_TRIGGER, True)

    time.sleep(0.00001)

    GPIO.output(PIN_TRIGGER, False)

    while GPIO.input(PIN_ECHO) == 0:
        pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)

    return distance < float(os.environ.get("DISTANCE", "15.0"))
