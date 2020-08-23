#!/usr/bin/env python3

"""
ultrasonics_api

Used as a proxy server to forward API requests to various services which require private API keys.

XDGFX, 2020
"""

from flask import Blueprint, request, jsonify

bp = Blueprint('ultrasonics_api', __name__)

@bp.route('/api')
def index():
    return jsonify({
        "name": "ultrasonics_api",
        "api_version": "v1"
    })

@bp.route('/api/v1/spotify')
def api_v1_spotify():
    return jsonify({
        "name": "spotify"
    })