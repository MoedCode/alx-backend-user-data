#!/usr/bin/env python3
import json
from flask import (
    Flask, jsonify, request
)
from markupsafe import escape
from local_storage import LocalStorage

app = Flask(__name__)
storage = LocalStorage("app.json")
storage.caching()
print("--------------------------------")


@app.route('/')
def hello_world():
    return 'Hello, World!q'


@app.route('/user/<username>')
def show_user_profile(username):
    # Show the user profile for that user
    return 'User %s --' % escape(username)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

#
@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)

# ▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐ POST ▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐


@app.route('/example_endpoint', methods=['POST'])
def example_endpoint():
    # Get the data from the request
    data = request.json
    storage.save(data)
    storage.commit()
    # Process the data (if needed)
    # In this example, we're just returning the received data
    return jsonify(data)
