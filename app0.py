#!/usr/bin/env python3
from flask import Flask, request, make_response
from functools import wraps
import uuid

app = Flask(__name__)

users = {"user1": "password1", "user2": "password2"}  # Sample user database
sessions = {}  # Dictionary to store session data

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = request.cookies.get('session_id')
        if not session_id or session_id not in sessions:
            return "Unauthorized", 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return "<h1>Welcome to the session authentication project!</h1>"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username in users and users[username] == password:
        session_id = str(uuid.uuid4())
        sessions[session_id] = username
        response = make_response(f"Logged in as {username}")
        response.set_cookie('session_id', session_id)
        print(f" response => {response.__dict__}")
        return response
    else:
        return "Invalid credentials", 401

@app.route('/useless')
def useless_end_point() -> str:
    """Print all query parameters"""
    str4rend = "<h1>Welcome to Useless Page</h1>"
    query_parameters = request.args

    if not query_parameters:  # Check if query_parameters is empty
        return str4rend

    for param in query_parameters:
        str4rend += f"<h2>{param} : {query_parameters.get(param)}</h2>"
        str4rend += str(type(param))

    return str4rend

@app.route('/dashboard')
@login_required
def dashboard():
    session_id = request.cookies.get('session_id')
    username = sessions[session_id]
    return f"Welcome to your dashboard, {username}!"

if __name__ == '__main__':
    app.run(debug=True)
'''
{
    'headers': Headers([
            (
                'Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', '18'),
            ('Set-Cookie', 'session_id=eddce8b8-514e-40ff-8931-02c000916c3b; Path=/')
        ]),
    '_status': '200 OK',
    '_status_code': 200,
    'direct_passthrough': False, '_on_close': [],
    'response': [b'Logged in as user1' ]
}
'''