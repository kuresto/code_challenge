import pytest

from flask import url_for
from webtest.app import AppError
from hamcrest import assert_that, has_entries, has_key

from bluestorm_api.medicines.models import Medicine


def test_medicine_resource_create(user_client, provider):
    data = {
        "measure": "ml",
        "name": "panacea",
        "dosage": "10",
        "amount": 10.5,
        "kind": "tablet",
        "provider_id": provider.id,
    }

    response = user_client.post_json(url_for("medicine.create"), data)

    assert response.status_code == 201

    assert_that(
        response.json,
        has_entries(
            {
                "measure": "ml",
                "name": "panacea",
                "dosage": 10,
                "amount": "10.5000",
                "kind": "tablet",
                "provider": has_entries(
                    {
                        "name": provider.name,
                        "id": provider.id,
                        "phone": str(provider.phone),
                    }
                ),
            }
        ),
    )
    assert_that(response.json, has_key("id"))
    assert_that(response.json, has_key("created"), has_key("updated"))


def test_medicine_resource_create_without_required_fields(user_client, provider):
    data = {}

    response = user_client.post_json(
        url_for("medicine.create"), data, expect_errors=True
    )

    assert response.status_code == 400

    assert_that(response.json, has_entries({"error": "'name' is a required property"}))


def test_medicine_resource_create_invalid_value(user_client, provider):
    data = {
        "measure": "ml",
        "name": "panacea",
        "dosage": "10",
        "amount": 10.5,
        "kind": "fake",
        "provider_id": provider.id,
    }

    response = user_client.post_json(
        url_for("medicine.create"), data, expect_errors=True
    )

    assert response.status_code == 400

    assert_that(response.json, has_entries({"error": "invalid kind"}))


def test_medicine_resource_fetch(user_client, medicine):
    response = user_client.get(url_for("medicine.fetch", id=medicine.id))

    assert response.status_code == 200

    assert_that(
        response.json,
        has_entries(
            {
                "measure": medicine.measure,
                "name": medicine.name,
                "dosage": medicine.dosage,
                "amount": str(medicine.amount),
                "kind": medicine.kind.value,
                "provider": has_entries(
                    {
                        "name": medicine.provider.name,
                        "id": medicine.provider.id,
                        "phone": str(medicine.provider.phone),
                    }
                ),
            }
        ),
    )
    assert_that(response.json, has_key("id"))
    assert_that(response.json, has_key("created"), has_key("updated"))


def test_medicine_resource_fetch_non_existing(user_client, provider):
    response = user_client.get(url_for("medicine.fetch", id=1), expect_errors=True)

    assert response.status_code == 404


def test_medicine_resource_listing(user_client, medicines):
    response = user_client.get(url_for("medicine.listing"))
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


def test_medicine_resource_update(user_client, medicine):
    data = {
        "measure": "ml",
        "name": "another",
        "dosage": "10",
        "amount": 10.5,
        "kind": "tablet",
        "provider_id": medicine.provider.id,
    }

    response = user_client.put_json(url_for("medicine.update", id=medicine.id), data)

    assert response.status_code == 200

    assert_that(
        response.json,
        has_entries(
            {
                "measure": medicine.measure,
                "name": "another",
                "dosage": medicine.dosage,
                "amount": str(medicine.amount),
                "kind": medicine.kind.value,
                "provider": has_entries(
                    {
                        "name": medicine.provider.name,
                        "id": medicine.provider.id,
                        "phone": str(medicine.provider.phone),
                    }
                ),
            }
        ),
    )
    assert_that(response.json, has_key("id"))
    assert_that(response.json, has_key("created"), has_key("updated"))


def test_medicine_resource_update_passing_non_existing_field(user_client, medicine):
    data = {
        "measure": "ml",
        "name": "panacea",
        "dosage": "10",
        "amount": 10.5,
        "kind": "tablet",
        "provider_id": medicine.provider.id,
        "non-existing": True,
    }

    response = user_client.put_json(
        url_for("medicine.update", id=medicine.id), data, expect_errors=True
    )

    assert response.status_code == 200

    assert_that(
        response.json,
        has_entries(
            {
                "measure": medicine.measure,
                "name": medicine.name,
                "dosage": medicine.dosage,
                "amount": str(medicine.amount),
                "kind": medicine.kind.value,
                "provider": has_entries(
                    {
                        "name": medicine.provider.name,
                        "id": medicine.provider.id,
                        "phone": str(medicine.provider.phone),
                    }
                ),
            }
        ),
    )
    assert_that(response.json, has_key("id"))
    assert_that(response.json, has_key("created"), has_key("updated"))


def test_medicine_resource_destroy(user_client, medicine):
    response = user_client.delete(url_for("medicine.destroy", id=medicine.id))

    assert response.status_code == 204
    assert medicine.query.count() == 0
