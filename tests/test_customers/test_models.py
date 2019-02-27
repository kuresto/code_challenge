from time import sleep

import pytest

from bluestorm_api.customers.models import Customer


def test_customer_model_creation(customer):
    db_customer = Customer.query.first()

    assert customer == db_customer


def test_customer_model_update(db, customer):
    old_updated = customer.updated

    new_data = {"name": "another"}
    sleep(1)  # Test was running too fast :/
    customer.update(**new_data)

    db_customer = Customer.query.first()

    assert db_customer.name == "another"
    assert db_customer.updated != old_updated


def test_customer_model_removal(db, customer):
    customer.delete()
    assert Customer.query.count() == 0


def test_customer_model_representation(customer):
    assert str(customer) == "<Customer 1>"

