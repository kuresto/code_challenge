import pytest

from flask import url_for
from webtest.app import AppError
from hamcrest import assert_that, has_entries, has_key

from bluestorm_api.accounts.models import User


def test_account_resource_login(user_client):
    data = {"login": "developer", "password": "developer"}

    response = user_client.post_json(url_for("auth.login"), data)
    assert response.status_code == 200

    assert_that(response.json, has_key("token"))


def test_account_resource_create(user_client):
    data = {"login": "login", "password": "password", "is_active": True}

    response = user_client.post_json(url_for("accounts.create"), data)

    assert response.status_code == 201

    assert_that(response.json, has_entries({"login": "login"}))
    assert_that(response.json, has_key("id"), has_key("token"))
    assert_that(response.json, has_key("created"), has_key("updated"))


def test_account_resource_duplicate(user_client):
    data = {"login": "developer", "password": "password", "is_active": True}

    response = user_client.post_json(
        url_for("accounts.create"), data, expect_errors=True
    )

    assert response.status_code == 400
    assert_that(response.json, has_entries({"error": "login already registered"}))


def test_account_resource_create_without_required_fields(user_client):
    data = {}

    response = user_client.post_json(
        url_for("accounts.create"), data, expect_errors=True
    )

    assert response.status_code == 400

    assert_that(response.json, has_entries({"error": "'login' is a required property"}))


def test_account_resource_fetch(user_client, user):
    response = user_client.get(url_for("accounts.fetch", id=user.id))

    assert response.status_code == 200

    assert_that(response.json, has_entries({"login": user.login, "is_active": True}))
    assert_that(response.json, has_key("id"))
    assert_that(response.json, has_key("created"), has_key("updated"))


def test_account_resource_fetch_non_existing(user_client):
    response = user_client.get(url_for("accounts.fetch", id=0), expect_errors=True)

    assert response.status_code == 404


def test_account_resource_listing(user_client, users):
    response = user_client.get(url_for("accounts.listing"))
    assert response.status_code == 200

    response = response.json

    assert_that(
        response,
        has_entries(
            {
                "current_page": 1,
                "next_page": None,
                "per_page": 20,
                "prev_page": None,
                "total": 6,
                "total_pages": 1,
            }
        ),
        has_key("results"),
    )

    assert len(response.get("results")) == 6


def test_account_resource_update(user_client, user):
    data = {"login": "new-name", "password": user.password.decode(), "is_active": True}

    response = user_client.put_json(url_for("accounts.update", id=user.id), data)

    assert response.status_code == 200

    assert_that(response.json, has_entries({"login": "new-name", "is_active": True}))
    assert_that(response.json, has_key("id"))
    assert_that(response.json, has_key("created"), has_key("updated"))


def test_account_resource_update_same_login(user_client, user):
    data = {"login": user.login, "password": user.password.decode(), "is_active": True}

    response = user_client.put_json(url_for("accounts.update", id=user.id), data)

    assert response.status_code == 200

    assert_that(response.json, has_entries({"login": user.login, "is_active": True}))
    assert_that(response.json, has_key("id"))
    assert_that(response.json, has_key("created"), has_key("updated"))


def test_account_resource_update_passing_non_existing_field(user_client, user):
    data = {
        "login": "new-name",
        "password": "password",
        "non-existing": True,
        "is_active": True,
    }

    response = user_client.put_json(
        url_for("accounts.update", id=user.id), data, expect_errors=True
    )

    assert response.status_code == 200

    assert_that(response.json, has_entries({"login": "new-name"}))
    assert_that(response.json, has_key("id"), has_key("is_active"))
    assert_that(response.json, has_key("created"), has_key("updated"))


def test_account_resource_destroy(user_client, user):
    response = user_client.delete(url_for("accounts.destroy", id=user.id))

    assert response.status_code == 204
    assert user.query.count() == 1
