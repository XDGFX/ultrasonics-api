# 1. Get javascript from https://a-v2.sndcdn.com/assets/47-d100329e-3.js
# 2. Search for regex client_id:"([\w\d]{32})"
# 3. Use capture group $1 for client id

#!/usr/bin/env python3

"""
ultrasonics_api soundcloud
Proxy for SoundCloud api requests.

XDGFX, 2020
"""

import os
import re

import requests
from flask import Blueprint, request

from ultrasonics_api import core

bp = Blueprint('soundcloud', __name__, url_prefix="/api/soundcloud")
limiter = core.limiter


@bp.route('/<path:subpath>', methods=["GET"])
@limiter.limit("20 per second;200 per minute")
def api_lastfm(subpath):
    """
    SoundCould api proxy. Adds an api key to all requests.
    The API key is found either by scraping the SoundCloud website or an environment variable.
    """

    base_url = "https://api-v2.soundcloud.com/"
    url = base_url + subpath
    params = {**request.values.to_dict()}

    params["client_id"] = os.environ.get('SOUNDCLOUD_CLIENT_ID')

    r = requests.get(url, params=params)

    if r.status_code == 401:
        # Invalid client_id
        renew_url = "https://a-v2.sndcdn.com/assets/47-d100329e-3.js"
        r = requests.get(renew_url)

        if r.status_code == 200:
            search_regex = 'client_id:"([\w\d]{32})'

            search = re.search(search_regex, r.text)

            if search:
                # Try again with this new client_id
                params["client_id"] = search.group(1)
                r = requests.get(url, params=params)

    # Any error status codes should be handled on the client.
    return r.content, r.status_code
