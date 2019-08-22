import unittest

from PIL import Image

from hardware.camera import Photo, Resolution
from storage.datastore import LocalDataStore


class PhotoTest(unittest.TestCase):

    def setUp(self) -> None:
        self.storage = LocalDataStore()

    def test_image_resizing(self):
        photo = Photo('./resources/raspiberry.jpg', Resolution(1000, 1000), 300)
        photo_resized = photo.resize(ratio=0.5)

        image = Image.open(photo_resized.filename)
        self.assertEqual(image.size, Resolution(500, 500))

    def test_change_jpeg_compression(self):
        photo = Photo('./resources/raspiberry.jpg', Resolution(1000, 1000), 300)
        photo_resized = photo.resize(ratio=1, quality=60)
        image = Image.open(photo_resized.filename)
        self.assertEqual(image.size, Resolution(1000, 1000))
