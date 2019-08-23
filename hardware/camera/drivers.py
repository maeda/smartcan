import tempfile
from abc import ABC, abstractmethod
from time import sleep, time

from hardware.camera import Photo, Resolution


class CameraDriver(ABC):

    @abstractmethod
    def capture(self) -> Photo:
        pass


class PiCameraDriver(CameraDriver):

    def __init__(self, resolution=Resolution(1024, 768), iso=300):
        from picamera import PiCamera

        self.resolution = resolution
        self.iso = iso
        self._camera = PiCamera(resolution=resolution)
        self._camera.iso = iso
        sleep(2)

        print('Camera ready!')

    def capture(self) -> Photo:
        origin = tempfile.NamedTemporaryFile(mode="w+t", delete=False, suffix='.jpg')

        self._camera.capture(origin.name)

        return Photo(origin.name, resolution=self.resolution, iso=self.iso)
