import pytest

from flask_sqlalchemy import SQLAlchemy

from mixer.backend.flask import mixer

from bluestorm_api.app import create_app
from bluestorm_api.db import db as _db


@pytest.fixture(name="app", scope="function")
def fixture_app():
    app = create_app()

    return app


@pytest.yield_fixture(name="db", scope="function")
def fixture_db(app):
    connect = _db.engine.connect()
    connect.execute("COMMIT")
    connect.execute("CREATE DATABASE IF NOT EXISTS test")
    connect.close()

    with app.app_context():
        _db.drop_all()
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture(name="mixer")
def fixture_mixer(app, db):
    mixer.init_app(app)
    return mixer

