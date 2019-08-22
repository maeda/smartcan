from time import sleep

RECYCLABLE_LED_PIN = 15
NON_RECYCLABLE_LED_PIN = 7
CONTROL_LED_PIN = 25


class LedPanel:
    def __init__(self):
        from gpiozero import LED
        self._control = LED(CONTROL_LED_PIN)
        self._recyclable = LED(RECYCLABLE_LED_PIN)
        self._non_recyclable = LED(NON_RECYCLABLE_LED_PIN)

    def control(self):
        self._control.on()
        sleep(1)
        self._control.off()

    def recyclable(self):
        self._recyclable.on()
        sleep(1)
        self._recyclable.off()

    def non_recyclable(self):
        self._non_recyclable.on()
        sleep(1)
        self._non_recyclable.off()

    def led_check(self):
        self.control()
        self.recyclable()
        self.non_recyclable()
        self.blink_all()

    def blink_all(self):
        self._control.on()
        self._recyclable.on()
        self._non_recyclable.on()
        sleep(1)
        self._control.off()
        self._recyclable.off()
        self._non_recyclable.off()
