#!/usr/bin/env python3

"""
ultrasonics_api

Used as a proxy server to forward api requests to various services which require private api keys.

All api requests should be made to /api/<service>/<subpath>
where <subpath> is the same as sending directly to the respective api.

XDGFX, 2020
"""

import os
from urllib.parse import urlencode

import requests
from flask import Blueprint, Response, jsonify, redirect, request

bp = Blueprint('ultrasonics_api', __name__)

@bp.route('/api')
def index():
    return jsonify({
        "name": "ultrasonics_api",
        "supported apis": [
            "spotify"
        ]
    })

class Spotify():
    valid_states = []

@bp.route('/api/spotify/<path:subpath>', methods=["GET", "POST", "PUT", "DELETE"])
def api_spotify(subpath):
    """
    Spotify api proxy. Adds an app client secret key to all requests.
    """
    base_url = "https://api.spotify.com/"
    url = base_url + subpath
    method = request.method
    params = {**request.values.to_dict()}

    if method == "GET":
        r = requests.get(url = url, params = params)
    elif method == "POST":
        r = requests.post(url = url, params = params)
    elif method == "PUT":
        r = requests.put(url = url, params = params)
    elif method == "DELETE":
        r = requests.delete(url = url, params = params)

    return r.json()

@bp.route('/api/spotify_auth_request')
def api_spotify_auth_request():
    """
    Spotify api proxy specifically for the app auth endpoint.
    """
    from uuid import uuid4

    base_url = "https://accounts.spotify.com/authorize/?"

    params = {
        "client_id": os.environ.get('SPOTIFY_CLIENT_ID'),
        "response_type": "code",
        "redirect_uri": "https://ultrasonics-api.herokuapp.com/api/spotify_auth",
        "state": uuid4()
    }

    Spotify.valid_states.append(params["state"])

    url = base_url + urlencode(params)

    return redirect(url, 302)


@bp.route('/api/spotify_auth')
def api_spotify_auth():
    code = request.args.get("code", None)
    error = request.args.get("error", None)
    state = request.args.get("state")

    if state not in Spotify.valid_states:
        return jsonify({
            "error": "State returned was not valid",
            "states": Spotify.valid_states,
            "state": state
        }), 500

    if error:
        return error
    else:
        return code