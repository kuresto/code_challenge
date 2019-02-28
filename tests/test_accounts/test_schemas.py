import pytest

from hamcrest import assert_that, has_entries, has_key

from bluestorm_api.accounts.models import User
from bluestorm_api.accounts.schemas import UserSchema, AuthSchema


def test_user_schema_dump(user):
    schema = UserSchema()
    data = schema.dump(user).data

    assert_that(
        data,
        has_entries(
            {
                "id": user.id,
                "login": user.login,
                "password": user.password.decode(),
                "is_active": True,
            }
        ),
    )

    assert_that(data, has_key("created"), has_key("updated"))


def test_auth_schema_dump():
    schema = AuthSchema()
    data = schema.dump({"token": "102030"}).data

    assert_that(data, has_entries({"token": "102030"}))

