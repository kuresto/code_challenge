import pytest

from flask import url_for
from webtest.app import AppError
from hamcrest import assert_that, has_entries, has_key

from bluestorm_api.providers.models import Provider


def test_provider_resource_create(user_client):
    data = {"name": "test", "phone": "+5516981784444"}

    response = user_client.post_json(url_for("provider.create"), data)

    assert response.status_code == 201

    assert_that(
        response.json, has_entries({"name": "test", "phone": "(16) 98178-4444"})
    )
    assert_that(response.json, has_key("id"))
    assert_that(response.json, has_key("created"), has_key("updated"))


def test_provider_resource_create_without_required_fields(user_client):
    data = {}

    response = user_client.post_json(
        url_for("provider.create"), data, expect_errors=True
    )

    assert response.status_code == 400

    assert_that(response.json, has_entries({"error": "'name' is a required property"}))


def test_provider_resource_create_invalid_value(user_client):
    data = {"name": "invalid", "phone": "invalid"}

    response = user_client.post_json(
        url_for("provider.create"), data, expect_errors=True
    )

    assert response.status_code == 400

    assert_that(response.json, has_entries({"error": "invalid phone number"}))


def test_provider_resource_fetch(user_client, provider):
    response = user_client.get(url_for("provider.fetch", id=provider.id))

    assert response.status_code == 200

    assert_that(
        response.json, has_entries({"name": provider.name, "phone": "(16) 97122-2222"})
    )
    assert_that(response.json, has_key("id"))
    assert_that(response.json, has_key("created"), has_key("updated"))


def test_provider_resource_fetch_non_existing(user_client):
    response = user_client.get(url_for("provider.fetch", id=1), expect_errors=True)

    assert response.status_code == 404


def test_provider_resource_listing(user_client, providers):
    response = user_client.get(url_for("provider.listing"))
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
                "total": 5,
                "total_pages": 1,
            }
        ),
        has_key("results"),
    )

    assert len(response.get("results")) == 5


def test_provider_resource_update(user_client, provider):
    data = {"name": "new-name", "phone": "+55 16 97122-2222"}

    response = user_client.put_json(url_for("provider.update", id=provider.id), data)

    assert response.status_code == 200

    assert_that(
        response.json, has_entries({"name": "new-name", "phone": "(16) 97122-2222"})
    )
    assert_that(response.json, has_key("id"))
    assert_that(response.json, has_key("created"), has_key("updated"))


def test_provider_resource_update_passing_non_existing_field(user_client, provider):
    data = {"name": "new-name", "phone": "+55 16 97122-2222", "non-existing": True}

    response = user_client.put_json(
        url_for("provider.update", id=provider.id), data, expect_errors=True
    )

    assert response.status_code == 200

    assert_that(
        response.json, has_entries({"name": "new-name", "phone": "(16) 97122-2222"})
    )
    assert_that(response.json, has_key("id"))
    assert_that(response.json, has_key("created"), has_key("updated"))


def test_provider_resource_destroy(user_client, provider):
    response = user_client.delete(url_for("provider.destroy", id=provider.id))

    assert response.status_code == 204
    assert Provider.query.count() == 0
