from flask import Flask
from camera import capture 
from multiprocessing import Value
import json

counter = Value('i', 0)
app = Flask(__name__)

@app.route('/capture', methods=['GET'])
def capture_route():
    with counter.get_lock():
        counter.value += 1

    capture('photo_' + str(counter.value) + '.jpg')

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
