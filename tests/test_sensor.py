import unittest

from gpiozero.pins.mock import MockFactory, MockTriggerPin
from gpiozero import Device

from hardware.trash_detector import TrashDetector, PIN_TRIGGER, PIN_ECHO

factory = MockFactory()

Device.pin_factory = factory


class ProximityTest(unittest.TestCase):
    def test_if_object_was_detected(self):
        trash_detector = TrashDetector()
        factory.pin(PIN_TRIGGER, pin_class=MockTriggerPin,
                    echo_pin=factory.pin(PIN_ECHO), echo_time=0.0001)

        self.assertTrue(trash_detector.wait_for_detection())


if __name__ == "__main__":
    unittest.main()
