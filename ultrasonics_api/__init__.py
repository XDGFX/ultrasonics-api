import os

from flask import Flask

from . import ultrasonics_api


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key'
    )

    app.register_blueprint(ultrasonics_api.bp)

    return app
