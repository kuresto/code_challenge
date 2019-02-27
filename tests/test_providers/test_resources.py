import pytest

from flask import url_for
from webtest.app import AppError
from hamcrest import assert_that, has_entries, has_key

from bluestorm_api.providers.models import Provider


def test_provider_resource_create(testapp):
    data = {"name": "test", "phone": "+5516981784444"}

    response = testapp.post_json(url_for("provider.create"), data)

    assert response.status_code == 201

    assert_that(
        response.json, has_entries({"name": "test", "phone": "(16) 98178-4444"})
    )
    assert_that(response.json, has_key("id"))
    assert_that(response.json, has_key("created"), has_key("updated"))


def test_provider_resource_fetch(testapp, provider):
    response = testapp.get(url_for("provider.fetch", id=provider.id))

    assert response.status_code == 200

    assert_that(
        response.json, has_entries({"name": provider.name, "phone": "(16) 97122-2222"})
    )
    assert_that(response.json, has_key("id"))
    assert_that(response.json, has_key("created"), has_key("updated"))


def test_provider_resource_fetch_non_existing(testapp):
    response = testapp.get(url_for("provider.fetch", id=1), expect_errors=True)

    assert response.status_code == 404


def test_provider_resource_listing(testapp, providers):
    response = testapp.get(url_for("provider.listing"))

    assert response.status_code == 200
    assert len(response.json) == 5


def test_provider_resource_update(testapp, provider):
    data = {"name": "new-name"}

    response = testapp.put_json(url_for("provider.update", id=provider.id), data)

    assert response.status_code == 200

    assert_that(
        response.json, has_entries({"name": "new-name", "phone": "(16) 97122-2222"})
    )
    assert_that(response.json, has_key("id"))
    assert_that(response.json, has_key("created"), has_key("updated"))


def test_provider_resource_destroy(testapp, provider):
    response = testapp.delete(url_for("provider.destroy", id=provider.id))

    assert response.status_code == 204
    assert Provider.query.count() == 0
