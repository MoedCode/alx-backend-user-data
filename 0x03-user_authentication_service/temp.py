#!/usr/bin/env python3
from flask import Flask
app = Flask(__name__)
print("--------------------------------")
@app.route('/')
def hello_world():
    return 'Hello,'

# flask run --host=0.0.0.0 --port=5005 --debug