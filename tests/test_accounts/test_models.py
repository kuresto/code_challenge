from time import sleep

import pytest

from bluestorm_api.accounts.models import User


def test_account_model_creation(user):
    db_user = User.query.order_by(User.id.desc()).first()

    assert user == db_user


def test_account_model_update(db, user):
    old_updated = user.updated

    new_data = {"login": "another"}
    sleep(1)  # Test was running too fast :/
    user.update(**new_data)

    db_user = User.query.order_by(User.id.desc()).first()

    assert db_user.login == "another"
    assert db_user.updated != old_updated


def test_account_model_removal(db, user):
    user.delete()
    assert User.query.count() == 1  # Api Client User still exists


def test_account_model_representation(user):
    assert str(user) == "<User 2>"

