#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def login():
    """
    login
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or len(email.split()) == 0:
        return jsonify({"error": "email missing"}), 400
    if not password or len(password.split()) == 0:
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    if len(user) != 0:
        if user[0].is_valid_password(password):
            user = user[0]
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            res = jsonify(user.to_json())
            res.set_cookie(getenv('SESSION_NAME', '_my_session_id'),
                           session_id)
            return res
        else:
            return jsonify({"error": "wrong password"}), 401
    return jsonify({"error": "no user found for this email"}), 404


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """
    logout
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({})
    else:
        abort(404)
