#!/usr/bin/env python3
"""Modules that contains views that hanldes all Session authentication routes.
"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    res = jsonify(user.to_json())
    res.set_cookie(os.getenv("SESSION_NAME"), session_id)
    return res


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """ POST /api/v1/auth_session/logout
    Deletes session
    """
    from api.v1.app import auth

    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
