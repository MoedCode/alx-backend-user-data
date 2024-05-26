#!/usr/bin/env python3
from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route("/")
@app.route("/home")
@app.route("/home/")
def home():
    return "<h1>Home page</h1>"

@app.route('/useless/', defaults={'number': None, 'string': None, 'tag': None, 'sprt_tag': None})
@app.route('/useless/<int:number>/<string:string>/<string:tag>/<string:sprt_tag>')
def useless(number: int = None, string: str = None, tag: str = None, sprt_tag: str = None):
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

    # Generate the output string
    rendered_string = (f"<{tag}> {string} </{tag}> {'<hr>' if sprt_tag else ''}") * number
    return render_template_string(rendered_string)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
