#!/usr/bin/env python3

"""
ultrasonics_api
Used as a proxy server for ultrasonics to forward api requests to various services which require private api keys.

All api requests should be made to /api/<service>/<subpath>
where <subpath> is the same as sending directly to the respective api.

XDGFX, 2020
"""

import os

from flask import Flask, jsonify, redirect, request

from ultrasonics_api import core
from ultrasonics_api.services import spotify
from ultrasonics_api.tools import api_key


def create_app():
    # Configure Flask app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev_key',
    )
    app.url_map.strict_slashes = False

    limiter = core.limiter
    limiter.init_app(app)

    # Register all services
    app.register_blueprint(spotify.bp)

    # Add auth middleware if requested
    @app.before_request
    def check_api_auth():
        if os.environ.get('REQUIRE_API_AUTH') == "True" or False:
            print("Checking")

            if request.values.get("ultrasonics_auth_hash") not in api_key.get_hash(False):
                return "Invalid auth hash received.", 403

        else:
            print("not checking")

    # Setup general routes and handlers
    @app.before_request
    def clear_trailing():
        """
        Clear any trailing '/' on path names.
        """
        rp = request.path
        if rp != '/' and rp.endswith('/'):
            return redirect(rp[:-1])

    @app.route('/api')
    def index():
        """
        General information about the api.
        """
        import os
        import re

        # Return files in services folder with .py extension, with '.py' removed
        supported_services = [module[0:-3] for module in os.listdir(
            "ultrasonics_api/services") if re.match("([\w\W]+)\.py$", module)]

        return jsonify({
            "name": "ultrasonics_api",
            "description": "Welcome to the official ultrasonics_api! You can use this endpoint in your ultrasonics instance to allow connection to all the supported services listed below. Please note, rate limits apply to this api, so if you receive a 429 error, just try again later 🪂.",
            "supported services": supported_services
        })

    @app.errorhandler(429)
    def error_too_many_requests(e):
        """
        When request limit is reached, return custom error page.
        """
        return "ultrasonics: Too many requests, try again later", 429

    return app
