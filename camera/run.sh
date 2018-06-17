#!/bin/bash

export FLASK_APP=camera_app.py
flask run

# curl -X GET localhost:5000/capture
