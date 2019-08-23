import threading

from flask import Flask, request

import tensorflow as tf
import time
import os

from model.image_model import SimpleModel
from storage.datastore import RemoteDataStore, LocalDataStore

graph = tf.get_default_graph()

app = Flask(__name__)

model = SimpleModel()

model.load_weights('./model/simple_model_weights.h5')

DATASET_PATH = os.environ.get('DATASET_PATH', './data-collection')


@app.route('/image', methods=['POST'])
def index():
    if request.method == 'POST':
        filename = 'photo_{}.jpg'.format(str(int(time.time())))
        f = request.files['photo']
        f.save(filename)

        global graph

        with graph.as_default():

            class_output = model.classifier(filename)
            app.logger.info("Class predicted: {}.".format(class_output))

            threading.Thread(target=_upload_file, args=(filename, class_output)).start()

            return class_output


def _upload_file(filename, class_output):
    target = 'data-collection/{}_{}_{}'.format(str(int(time.time())), class_output, filename)
    storage_remote = RemoteDataStore()
    storage_local = LocalDataStore()

    storage_remote.put_object(filename, target)
    storage_local.delete_object(filename)

    app.logger.info('File moved to {}'.format(target))


if __name__ == '__main__':
    app.run()
