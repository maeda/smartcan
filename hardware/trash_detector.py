import os
from gpiozero import DistanceSensor

PIN_TRIGGER = 23
PIN_ECHO = 24


class TrashDetector:

    def wait_for_detection(self):
        return self._sensor().wait_for_inactive()

    def _sensor(self):
        return DistanceSensor(PIN_ECHO, PIN_TRIGGER,
                              max_distance=1,
                              threshold_distance=float(os.environ.get("DISTANCE", 15.0)) / 100)
