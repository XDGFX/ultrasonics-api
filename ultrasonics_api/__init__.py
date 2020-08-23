import os

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from . import ultrasonics_api


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev_key'
    )

    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )

    app.register_blueprint(ultrasonics_api.bp)
    return app
