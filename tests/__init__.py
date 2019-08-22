from gpiozero import Device
from gpiozero.pins.mock import MockFactory

factory = MockFactory()

Device.pin_factory = factory