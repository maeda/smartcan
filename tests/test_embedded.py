import unittest
from unittest.mock import Mock

from embedded import EmbeddedRuntime
from hardware.camera import Photo, Resolution
from prediction.prediction import TrashClassified
from presentation.led_panel import LedPanel
from tests import factory


class EmbeddedRuntimeTest(unittest.TestCase):

    def test_local_prediction(self):
        camera_driver = Mock()
        trash_detector = Mock()
        storage = Mock()
        prediction = Mock()

        camera_driver.capture.return_value = Photo('./resources/raspiberry.jpg', Resolution(1024, 924), 300)
        prediction.predict.return_value = TrashClassified("recyclable",
                                                          Photo('./resources/raspiberry.jpg', Resolution(1024, 924), 300))

        embedded = EmbeddedRuntime(camera_driver, prediction, LedPanel(), trash_detector, storage)

        trash_classified = embedded.run()
        self.assertEqual(trash_classified.label, "recyclable")

        prediction.predict.return_value = TrashClassified("nonrecyclable",
                                                          Photo('./resources/raspiberry.jpg', Resolution(1024, 924), 300))

        trash_classified = embedded.run()
        self.assertEqual(trash_classified.label, "nonrecyclable")

    def test_remote_prediction(self):
        pass
