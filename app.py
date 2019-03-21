from flask import Flask
from flask import request

import tensorflow as tf
import time
import os

import datastore

from model.image_model import TrashVggModel, TrashModel, SimpleModel


graph = tf.get_default_graph()

app = Flask(__name__)

model = TrashModel()

DATASET_PATH = os.environ.get('DATASET_PATH', './data-collection')


@app.route('/image', methods=['POST'])
def index():
    if request.method == 'POST':
        filename = 'photo_' + str(int(time.time())) + '.jpg'
        f = request.files['photo']
        f.save(filename)

        global graph

        with graph.as_default():
            class_output = model.classifier(filename)

            print(class_output)

            if class_output == 'recyclable':
                datastore.move_object(filename, 'data-collection/recyclable/' + filename)
            if class_output == 'nonrecyclable':
                datastore.move_object(filename, 'data-collection/nonrecyclable/' + filename)

            return class_output
    return ""


if __name__ == '__main__':
    app.run()
