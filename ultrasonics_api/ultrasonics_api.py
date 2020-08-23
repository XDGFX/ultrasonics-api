#!/usr/bin/env python3

"""
ultrasonics_api

Used as a proxy server to forward API requests to various services which require private API keys.

XDGFX, 2020
"""

from flask import Blueprint, request

bp = Blueprint('ultrasonics_api', __name__)

@bp.route('/')
def hello_world():
    return 'Hello, World!'