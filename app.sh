#!/bin/sh

gunicorn 'ultrasonics_api:create_app()' -w 1 --threads 1 -b 0.0.0.0:8003