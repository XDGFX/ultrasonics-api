#!/usr/bin/env python3

"""
ultrasonics_api last.fm
Proxy for Last.fm api requests.

XDGFX, 2020
"""

import os

import requests
from flask import Blueprint, request

from ultrasonics_api import core

bp = Blueprint('lastfm', __name__, url_prefix="/api/lastfm")
limiter = core.limiter


@bp.route('/', methods=["GET"])
@limiter.limit("20 per second;200 per minute")
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

    return r.text
