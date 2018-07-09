from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import numpy as np

K.set_image_dim_ordering('th')


class TrashModel:
    def __init__(self):
        self.classes_types = {0: 'nonrecyclable', 1: 'recyclable'}
        self._compile()

    def _compile(self):
        self.model = Sequential()
        self.model.add(Conv2D(32, (3, 3), input_shape=(3, 150, 150)))
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

    def load_weights(self, weight_file):
        print(self.model)
        self.model.load_weights(weight_file)

    def classifier(self, filename):
        return self.classifier_img(image.img_to_array(image.load_img(filename, target_size=(150, 150))))

    def classifier_img(self, x):
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])
        classes = self.model.predict_classes(images, batch_size=10, verbose=0)

        return self.classes_types[np.asscalar(classes[0][0])]
