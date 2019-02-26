from os import environ

from flask import Flask
from flask_migrate import Migrate

from .db import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(environ.get("FLASK_SETTINGS_MODULE"))

    db.init_app(app)
    Migrate(app, db)

    return app
