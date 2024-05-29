#!/usr/bin/env python3
import json
from flask import (
    Flask, jsonify, render_template_string, request
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

@app.route('/about__api__', methods=['GET'])
def about_us_api():

    return jsonify({ "a7na men":"al da3 men 3mrna snen" }), 200

@app.route('/about')
def about_us():

    return  "<h1>a7na men...<br>al da3 men 3mrna snen</h1>"

# ▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐ POST ▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐

@app.route('/useless/', defaults={'number': None, 'string': None, 'tag': None, 'sprt_tag': None})
@app.route('/useless/<int:number>/<string:string>/<string:tag>/<string:sprt_tag>')
def useless(number: int = 1, string: str = None, tag: str = None, sprt_tag: str = None):
    # Check if query parameters are provided
    if number is None:
        number = request.args.get('number')
    if string is None:
        string = request.args.get('str')  # Use 'str' to match the query parameter
    if tag is None:
        tag = request.args.get('tag')
    if sprt_tag is None:
        sprt_tag = request.args.get('sprt_tag')

    # Ensure 'number' is provided and convert it to int
    if number is None:
        return "Missing 'number' parameter", 400
    try:
        number = int(number)
    except (ValueError, TypeError):
        return "Invalid 'number' parameter", 400

    # Ensure all required parameters are provided
    if not all([number, string, tag]):
        return "Missing required parameters", 400
    i = int(number)
    # Generate the output string
    rendered_string = (f"<{tag}> {i - 1}{string} </{tag}> {'<hr>' if sprt_tag else ''}") * number
    return render_template_string(rendered_string)

@app.route('/example_endpoint', methods=['POST'])
def example_endpoint():
    # Get the data from the request
    data = request.json
    print(f"{__file__}  :  {data}")
    storage.save(data)
    storage.commit()
    # Process the data (if needed)
    # In this example, we're just returning the received data
    return jsonify(data)

