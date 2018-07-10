from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import numpy as np
from abc import ABC, abstractmethod

from keras import layers, models, optimizers

K.set_image_dim_ordering('th')


class AbstractTrashModel(ABC):
    def __init__(self):
        self.classes_types = {0: 'nonrecyclable', 1: 'recyclable'}
        self._compile()

    @abstractmethod
    def _compile(self):
        pass

    def load_weights(self, weight_file):
        print(self.model)
        self.model.load_weights(weight_file)

    def classifier(self, filename):
        return self.classifier_img(
            image.img_to_array(image.load_img(filename, target_size=(self.input_shape[1], self.input_shape[2]))))

    def classifier_img(self, x):
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])
        classes = self.model.predict_classes(images, batch_size=10, verbose=0)

        return self.classes_types[np.asscalar(classes[0][0])]


class TrashVggModel(AbstractTrashModel):

    def _compile(self):
        self.input_shape = (3, 320, 213)
        from keras.applications import VGG16

        conv_base = VGG16(weights='imagenet',
                          include_top=False,
                          input_shape=self.input_shape)
        from keras import models, layers

        self.model = models.Sequential()
        self.model.add(conv_base)
        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(256, activation='relu'))
        self.model.add(layers.Dense(1, activation='sigmoid'))
        # Train only the dense layers.
        conv_base.trainable = False


class TrashModel(AbstractTrashModel):

    def _compile(self):
        self.input_shape = (3, 150, 150)
        self.model = Sequential()
        self.model.add(Conv2D(32, (3, 3), input_shape=self.input_shape))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(32, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(64, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Flatten())
        self.model.add(Dense(64))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(1))
        self.model.add(Activation('sigmoid'))
