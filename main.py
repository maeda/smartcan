import cv2
from PIL import Image
import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import numpy as np

K.set_image_dim_ordering('th')

classes_types = {0: 'nonrecyclable', 1: 'reciclable'}

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(3, 150, 150)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(
    loss='binary_crossentropy',
    optimizer='rmsprop',
    metrics=['accuracy'])

model.load_weights('first_try.h5')

def classifier_img(x):
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    classes = model.predict_classes(images, batch_size=10, verbose=0)
    
    return classes_types[np.asscalar(classes[0][0])]

cap = cv2.VideoCapture(0)
cap.set(10, 200)

while(True):
    ret, frame = cap.read()
    
    img = Image.fromarray(frame)
    img_resized = img.resize((150,150))
    img = np.asarray(img)
    class_generated = classifier_img(np.asarray(img_resized).reshape((3,150,150)))
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, class_generated, (10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # out = cv2.imwrite('capture.jpg', frame)
        break
    
cap.release()
cv2.destroyAllWindows()

