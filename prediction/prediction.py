import os
from abc import ABC, abstractmethod

import requests

from common import tostring
from hardware.camera import Photo


@tostring
class TrashClassified:
    def __init__(self, label, photo: Photo):
        self.label = label
        self.photo = photo


@tostring
class Prediction(ABC):
    @abstractmethod
    def predict(self, photo: Photo) -> TrashClassified:
        pass


class PredictionException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)


class RestPrediction(Prediction):

    def predict(self, photo: Photo) -> TrashClassified:
        try:
            with open(photo.filename, 'rb') as f:
                response = requests.post(os.environ.get('SERVICE_ENDPOINT'), files={'photo': f})
                response.raise_for_status()

                return TrashClassified(response.text, photo)

        except Exception as e:
            raise PredictionException(e)


class LocalPrediction(Prediction):
    def __init__(self):
        from model.image_model import FirstTryModel
        self._model = FirstTryModel()
        self._model.load_weights(os.environ.get("MODEL_FILE"))

    def predict(self, photo: Photo) -> TrashClassified:
        return TrashClassified(self._model.classifier(photo.filename), photo)
