#!/usr/bin/env python3

"""
ultrasonics_api last.fm
Proxy for Last.fm api requests.

XDGFX, 2020
"""

import os
from urllib.parse import urlencode

import redis
import requests
from flask import Blueprint, Response, jsonify, redirect, request, render_template

from ultrasonics_api import core

bp = Blueprint('lastfm', __name__, url_prefix="/api/lastfm")
limiter = core.limiter


def auth_headers():
    """
    Encode client_id and client_secret into required authorisation header.
    """
    import base64
    data_string = os.environ.get(
        'SPOTIFY_CLIENT_ID') + ":" + os.environ.get('SPOTIFY_CLIENT_SECRET')
    data_bytes = data_string.encode()
    data_encoded = base64.urlsafe_b64encode(data_bytes)
    auth_headers = {
        "Authorization": f"Basic {data_encoded.decode()}"
    }

    return auth_headers


@bp.route('/', methods=["GET"])
def api_lastfm():
    """
    Last.fm api proxy. Adds an api key to all requests.
    """
    url = "https://ws.audioscrobbler.com/2.0/"
    params = {**request.values.to_dict()}
    params["api_key"] = os.environ.get('LASTFM_API_KEY')
    headers = {
        "User-Agent": "xdgfx/ultrasonics-api",
    }

    r = requests.get(url=url, params=params, headers=headers)

    return r.text()
