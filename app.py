from flask import Flask
from flask import request
from model.image_model import classifier
app = Flask(__name__)


@app.route('/image', methods=['POST'])
def index():
    if request.method == 'POST':
        f = request.files['photo']
        f.save('./photo.jpg')
    return classifier('./photo.jpg')
