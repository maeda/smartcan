import unittest

from presentation.led_panel import LedPanel, CONTROL_LED_PIN, RECYCLABLE_LED_PIN, NON_RECYCLABLE_LED_PIN
from tests import factory


class LedPanelTest(unittest.TestCase):

    def setUp(self) -> None:
        self.led_panel = LedPanel()

    @classmethod
    def tearDownClass(cls) -> None:
        factory.reset()

    def test_control_led(self):
        led_pin = factory.pin(CONTROL_LED_PIN)

        self.led_panel.control()

        self._assertLedPanelCall(led_pin.states)

    def test_recyclable_led(self):
        led_pin = factory.pin(RECYCLABLE_LED_PIN)

        self.led_panel.recyclable()

        self._assertLedPanelCall(led_pin.states)

    def test_non_recyclable_led(self):
        led_pin = factory.pin(NON_RECYCLABLE_LED_PIN)

        self.led_panel.non_recyclable()

        self._assertLedPanelCall(led_pin.states)

    def _assertLedPanelCall(self, states):
        self.assertIs(len(states), 3)
        self.assertFalse(states[0].state)
        self.assertTrue(states[1].state)
        self.assertFalse(states[2].state)
