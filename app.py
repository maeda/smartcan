from flask import Flask
from flask import request

import tensorflow as tf
import time
import os

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
                os.rename(filename, DATASET_PATH + '/recyclable/' + filename)
            if class_output == 'nonrecyclable':
                os.rename(filename, DATASET_PATH + '/nonrecyclable/' + filename)
            return class_output
    return ""


if __name__ == '__main__':
    app.run()
