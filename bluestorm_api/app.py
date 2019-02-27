from os import environ

from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow


def create_app():
    from .db import db
    from .providers.views import provider_blueprint

    app = Flask(__name__)
    app.config.from_object(environ.get("FLASK_SETTINGS_MODULE"))

    # database and migrations
    db.init_app(app)
    Migrate(app, db)

    # marshmallow
    ma = Marshmallow(app)
    ma.init_app(app)

    # blueprints
    app.register_blueprint(provider_blueprint)

    return app
