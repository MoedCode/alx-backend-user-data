#!/usr/bin/env python3
""" Module of Session authentication views
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session() -> str:
    """ POST /auth_session/login
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    if not User.search({'email': email}):
        return jsonify({"error": "no user found for this email"}), 404
    user = User.search({'email': email})[0]

    from api.v1.app import auth
    if user.is_valid_password(password):
        session_id = auth.create_session(user.id)
        response = jsonify(user.to_json())
        SESSION_NAME = getenv('SESSION_NAME')
        response.set_cookie(SESSION_NAME, session_id)
        return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def auth_session_logout() -> str:
    """ DELETE /auth_session/logout
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
