#!/usr/bin/env python3

"""Basic flask app
In this task, you will set up a basic Flask app.

Create a Flask app that has a single GET route ("/")
and use flask.jsonify to return a JSON payload of the form:
"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
app.url_map.strict_slashes = False
auth = Auth()


@app.route('/', methods=['GET'])
def basic_route() -> str:
    """Basic route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """Users route
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = auth.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """User Login
    Returns:
        str: [JSON payload]
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not auth.valid_login(email, password):
        abort(401)
    session_id = auth.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """Log user out and destroy session
    Returns:
        str: [redirect to GET /]
    """
    session_id = request.cookies.get('session_id')
    user = auth.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    auth.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """User profile
    Returns:
        str: [JSON payload]
    """
    session_id = request.cookies.get('session_id')
    user = auth.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """Reset password token
    Returns:
        str: [JSON payload]
    """
    email = request.form.get('email')
    try:
        reset_token = auth.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """Update password
    Returns:
        str: [JSON payload]
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        auth.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
