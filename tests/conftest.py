import pytest
from webtest import TestApp

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token

from mixer.backend.flask import mixer

from bluestorm_api.accounts.models import User
from bluestorm_api.app import create_app
from bluestorm_api.db import db as _db


@pytest.yield_fixture(name="app", scope="function")
def fixture_app():
    app = create_app()

    ctx = app.test_request_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.yield_fixture(name="token", autouse=True, scope="function")
def fixture_token():
    user = User.create(**{"login": "developer", "password": "developer"})
    token = create_access_token(identity=user, fresh=True)

    return ("Bearer", token)


@pytest.fixture(scope="function")
def testapp(app):
    return TestApp(app)


@pytest.fixture(name="user_client")
def fixture_user_client(app, token):
    client = TestApp(app)
    client.set_authorization(token)

    return client


@pytest.yield_fixture(name="db", autouse=True, scope="function")
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

