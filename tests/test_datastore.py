import io
import tempfile
import unittest
from os import path

from storage.datastore import LocalDataStore


class LocalDataStoreTest(unittest.TestCase):

    def setUp(self) -> None:
        self.storage = LocalDataStore()

    def test_put_object(self):

        file = io.BytesIO(b"blabla")
        temp_file = tempfile.NamedTemporaryFile(mode="w+t", suffix='.txt')

        with file as f:
            self.storage.put_object(f, temp_file.name)

        with open(temp_file.name) as f:
            self.assertEqual(f.read(), "blabla")

    def test_move_object(self):
        origin = tempfile.NamedTemporaryFile(mode="w+t", delete=False, suffix='.txt')
        destination = tempfile.NamedTemporaryFile(mode="w+t", suffix='.txt')

        with open(origin.name, 'wb') as f:
            f.write(b"blabla")

        self.storage.move_object(origin.name, destination.name)

        with open(destination.name, 'rb') as f:
            self.assertEqual(f.read(), b'blabla')

        self.assertFalse(path.exists(origin.name))

    def test_delete_object(self):
        origin = tempfile.NamedTemporaryFile(mode="w+t", delete=False, suffix='.txt')

        with open(origin.name, 'wb') as f:
            f.write(b"blabla")

        self.assertTrue(path.exists(origin.name))

        self.storage.delete_object(origin.name)

        self.assertFalse(path.exists(origin.name))
