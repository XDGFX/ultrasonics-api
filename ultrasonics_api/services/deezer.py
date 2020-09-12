#!/usr/bin/env python3

"""
ultrasonics_api deezer
Proxy for Deezer api requests.

XDGFX, 2020
"""

import os
from urllib.parse import urlencode

import redis
import requests
from flask import Blueprint, Response, jsonify, redirect, request, render_template

from ultrasonics_api import core

bp = Blueprint('deezer', __name__, url_prefix="/api/deezer")
limiter = core.limiter

if os.environ.get("USE_REDIS") and os.environ.get("USE_REDIS").lower() in ["true", "1", "y", "yes"]:
    # Do use redis for data storage

    db = redis.from_url(os.environ.get("REDIS_URL"))

    def push_valid_state(state):
        """
        Add state to list of valid states.
        """
        db.lpush('deezer_valid_states', state)

    def remove_valid_state(state):
        """
        Try to remove state from list of valid states.
        Returns True if successful, else False.
        """
        return db.lrem('deezer_valid_states', 0, state)

else:
    # Don't use redis for data storage

    valid_states = []

    def push_valid_state(state):
        """
        Add state to list of valid states.
        """
        valid_states.append(state)

    def remove_valid_state(state):
        """
        Try to remove state from list of valid states.
        Returns True if successful, else False.
        """
        if state in valid_states:
            valid_states.remove(state)
            return True
        else:
            return False


@bp.route('/auth/request')
@limiter.limit("2 per day")
def api_deezer_auth_request():
    """
    Requests authorisation from the Deezer API.
    """
    from uuid import uuid4

    base_url = "https://connect.deezer.com/oauth/auth.php/?"

    params = {
        "app_id": os.environ.get('DEEZER_APP_ID'),
        "redirect_uri": "https://ultrasonics-api.herokuapp.com/api/deezer/auth",
        "state": str(uuid4()),
        "perms": ",".join([
            "basic_access",
            "offline_access",
            "manage_library",
            "delete_library"
        ])
    }

    push_valid_state(params["state"])

    url = base_url + urlencode(params)

    return redirect(url, 302)


@bp.route('/auth')
@limiter.exempt
def api_deezer_auth():
    """
    Redirect endpoint from Deezer after authentication attempt.
    """
    code = request.args.get("code", None)
    error = request.args.get("error_reason", None)
    state = request.args.get("state")

    if error:
        return error

    # Try to remove from database, return error if not exist
    if not remove_valid_state(state):
        return jsonify({
            "error": "State returned was not valid"
        }), 500

    url = "https://connect.deezer.com/oauth/access_token.php"

    data = {
        "app_id": os.environ.get('DEEZER_APP_ID'),
        "secret": os.environ.get('DEEZER_APP_SECRET'),
        "code": code
    }

    r = requests.post(url=url, data=data)

    return render_template("auth_return.html", data=r.text)
