from abc import ABC, abstractmethod
from keras.preprocessing import image
import numpy as np


class TrashModel(ABC):
    def __init__(self):
        self.classes_types = {0: 'nonrecyclable', 1: 'recyclable'}
        self._model, self._input_shape = self._compile()

    @abstractmethod
    def _compile(self):
        pass

    def load_weights(self, weight_file):
        print(self._model)
        self._model.load_weights(weight_file)

    def classifier(self, filename):
        return self.classifier_img(
            image.img_to_array(image.load_img(filename, target_size=(self._input_shape[1], self._input_shape[2]))))

    def classifier_img(self, x):
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])
        self._model._make_predict_function()
        classes = self._model.predict_classes(images, batch_size=10, verbose=0)

        return self.classes_types[np.asscalar(classes[0][0])]
