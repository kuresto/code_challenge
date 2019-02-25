from os import environ
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object(environ.get("FLASK_SETTINGS_MODULE"))

    return app
