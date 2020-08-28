#!/usr/bin/env python3

"""
app.py ultrasonics_api
Used to manually start the Flask app, as an alternative to `flask run`.

XDGFX, 2020
"""

from ultrasonics_api import create_app

app = create_app()

app.run(debug=True, host="0.0.0.0")
