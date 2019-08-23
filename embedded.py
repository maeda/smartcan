import logging
from time import time

from dotenv import load_dotenv

from hardware.camera import Photo
from hardware.camera.drivers import CameraDriver, PiCameraDriver
from hardware.trash_detector import TrashDetector
from prediction.prediction import Prediction, LocalPrediction
from presentation.led_panel import LedPanel
from storage.datastore import DataStore, Storage

load_dotenv()

log = logging.getLogger('app.embedded')


class EmbeddedRuntime:
    def __init__(self,
                 camera: CameraDriver,
                 prediction: Prediction,
                 presentation: LedPanel,
                 trash_detector: TrashDetector,
                 storage: DataStore
                 ):
        self._presentation = presentation
        self._prediction = prediction
        self._camera = camera
        self._trash_detector = trash_detector
        self._storage = storage

    def run(self):
        self._trash_detector.wait_for_detection()

        log.info('Trash detected!')

        self._presentation.control()

        photo = self._camera.capture()

        class_output = self._prediction.predict(photo)
        if class_output.label == 'recyclable':
            self._presentation.recyclable()
            self._storage.move_object(photo.source, 'data-collection/recyclable/' + 'photo_' + str(int(time())) + '.jpg')

        if class_output.label == 'nonrecyclable':
            self._presentation.non_recyclable()
            self._storage.move_object(photo.source, 'data-collection/nonrecyclable/' + 'photo_' + str(int(time())) + '.jpg')

        return class_output


def runtime():
    presentation = LedPanel()

    presentation.led_check()

    embedded_runtime = EmbeddedRuntime(
        camera=PiCameraDriver(),
        prediction=LocalPrediction(),
        presentation=presentation,
        trash_detector=TrashDetector(),
        storage=Storage()
    )

    presentation.blink_all()

    return embedded_runtime


if __name__ == '__main__':

    embedded_runtime = runtime()

    while True:
        embedded_runtime.run()
