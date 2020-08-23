#!/usr/bin/env python3

"""
ultrasonics_api

Used as a proxy server to forward API requests to various services which require private API keys.

XDGFX, 2020
"""

import os

from flask import Blueprint, jsonify, request

import requests

bp = Blueprint('ultrasonics_api', __name__)

@bp.route('/api')
def index():
    return jsonify({
        "name": "ultrasonics_api",
        "api_version": "v1"
    })

@bp.route('/api/v1/spotify/<path:subpath>', methods=["GET", "POST", "PUT", "DELETE"])
def api_v1_spotify(subpath):
    """
    Spotify API proxy. Adds a 
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
