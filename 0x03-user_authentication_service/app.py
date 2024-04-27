#!/usr/bin/env python3
"""
flask
"""
from flask import Flask, jsonify, request, abort
from flask import redirect, url_for
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def Index():
    """
    doc
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users',  methods=['POST'], strict_slashes=False)
def register_user():
    """
    registers user
    """
    form = request.form
    email = form.get("email")
    passwd = form.get("password")
    try:
        AUTH.register_user(email, passwd)
    except ValueError as e:
        return jsonify({"message": "email already registered"})
    return jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    user login
    """
    form = request.form
    email = form.get("email")
    passwd = form.get("password")
    if not AUTH.valid_login(email, passwd):
        abort(401)
    session_id = AUTH.create_session(email)
    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie("session_id", session_id)
    return res


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    user login
    """
    session_id = request.cookies["session_id"]
    if not session_id:
        abort(403)
    try:
        user = AUTH.get_user_from_session_id(session_id=session_id)
    except Exception as e:
        abort(403)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    user login
    """
    session_id = request.cookies["session_id"]
    if not session_id:
        abort(403)
    try:
        user = AUTH.get_user_from_session_id(session_id=session_id)
    except Exception as e:
        abort(403)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
