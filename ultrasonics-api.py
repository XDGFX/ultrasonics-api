#!/usr/bin/env python3

"""
ultrasonics-api

Used as a proxy server to forward API requests to various services which require private API keys.

XDGFX, 2020
"""

import os
from flask import Flask

app = Flask(__name__)
app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key'
    )

@app.route('/')
def hello_world():
    return 'Hello, World!'