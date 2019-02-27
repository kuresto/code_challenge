from os import environ

from http import HTTPStatus

from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS


def create_app():
    from .db import db

    from .common.exceptions import InvalidUsage
    from .common.handlers import bad_request_handler
    from .providers.views import provider_blueprint
    from .accounts.views import user_blueprint, auth_blueprint
    from .accounts.utils import jwt_identity, identity_loader

    app = Flask(__name__)
    app.config.from_object(environ.get("FLASK_SETTINGS_MODULE"))

    # database and migrations
    db.init_app(app)
    Migrate(app, db)

    # marshmallow
    ma = Marshmallow(app)
    ma.init_app(app)

    # jwt extended
    jwt = JWTManager(app)
    jwt.init_app(app)
    jwt.user_identity_loader(identity_loader)
    jwt.user_loader_callback_loader(jwt_identity)

    # bcrypt
    bcrypt = Bcrypt()
    bcrypt.init_app(app)

    # CORs
    cors = CORS()
    cors.init_app(app)

    # error handlers
    app.register_error_handler(InvalidUsage, bad_request_handler)
    app.register_error_handler(HTTPStatus.BAD_REQUEST, bad_request_handler)

    # blueprints
    app.register_blueprint(auth_blueprint)  # Authentication
    app.register_blueprint(provider_blueprint)  # Provider
    app.register_blueprint(user_blueprint)  # Users

    return app
