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


def create_app():
    # Configure Flask app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev_key',
    )
    app.url_map.strict_slashes = False

    limiter = core.limiter

    # Register all services
    app.register_blueprint(spotify.bp)

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
        import os, re
        
        # Return files in services folder with .py extension, with '.py' removed
        supported_services = [module[0:-3] for module in os.listdir("ultrasonics_api/services") if re.match("([\w\W]+)\.py$", module)]
        
        return jsonify({
            "name": "ultrasonics_api",
            "supported services": supported_services
        })

    @app.errorhandler(429)
    def error_too_many_requests(e):
        """
        When request limit is reached, return custom error page.
        """
        return "ultrasonics: Too many requests, try again later", 429

    return app
