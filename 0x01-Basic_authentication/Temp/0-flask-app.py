#!/usr/bin/env python3
# save this as app.py
from flask import Flask, request
from markupsafe import escape
import os
import json
app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    with open("Out", 'w') as F:
        json.dump(request)
    return f'Hello, {escape(name)}!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)