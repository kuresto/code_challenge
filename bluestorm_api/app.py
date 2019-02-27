from os import environ

from flask import Flask
from flask_migrate import Migrate

from .db import db

from .providers.views import provider_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(environ.get("FLASK_SETTINGS_MODULE"))

    # database and migrations
    db.init_app(app)
    Migrate(app, db)

    # blueprints
    app.register_blueprint(provider_blueprint)

    return app
