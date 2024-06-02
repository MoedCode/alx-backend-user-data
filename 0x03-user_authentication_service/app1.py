#!/usr/bin/env python3


from flask import (
    Flask, jsonify, request ,abort, redirect
    )
from flask.helpers import make_response
from user import User

from auth1 import Auth

app = Flask(__name__)
AUTH = Auth()

اديله = abort
@app.route("/")
def form():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users_register() -> str:
    try:
        email = request.form['email']
        PWD = request.form['password']
    except KeyError :
        return jsonify({"Error":"key is not exist"})
    try:
        user_obj = AUTH.register_user(email , PWD)
        return jsonify({"email": f"{user_obj.email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

@app.route('/sessions', methods=['POST'])
def login() -> str:

    email = request.form['email']
    PWD = request.form['password']
    is_valid = AUTH.valid_login(email, PWD)
    if not email or not PWD or not  is_valid:

        اديله(401)

    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie('session_id', session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)

from auth1 import Auth , _hash_password
from auth1 import Auth, _hash_password


