import unittest

from hardware.camera import Photo, Resolution
from storage.datastore import LocalDataStore


class LocalDataStoreTest(unittest.TestCase):

    def test_save_binary_content(self):
        storage = LocalDataStore()

        photo = Photo('./resources/raspiberry.jpg', Resolution(1024, 924), 300)
        photo_resized = photo.resize(ratio=0.5)

        storage.store_object(photo_resized, './resources/raspiberry_smaller.jpg')
