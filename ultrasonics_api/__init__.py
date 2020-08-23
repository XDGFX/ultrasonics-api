import os

from flask import Flask


from . import ultrasonics_api, core


def create_app():
    app = Flask(__name__)
    core.limiter.init_app(app)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev_key'
    )

    # limiter = Limiter(
    #     app,
    #     key_func=get_remote_address,
    #     default_limits=["200 per day", "50 per hour"]
    # )

    app.register_blueprint(ultrasonics_api.bp)
    return app
