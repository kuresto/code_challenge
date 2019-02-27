from time import sleep

import pytest

from bluestorm_api.medicines.models import Medicine


def test_medicines_model_creation(medicine):
    db_medicine = Medicine.query.first()

    assert medicine == db_medicine


def test_medicines_model_update(db, medicine):
    old_updated = Medicine.updated

    new_data = {"name": "another"}
    sleep(1)  # Test was running too fast :/
    medicine.update(**new_data)

    db_medicine = Medicine.query.first()

    assert db_medicine.name == "another"
    assert db_medicine.updated != old_updated


def test_medicines_model_removal(db, medicine):
    medicine.delete()
    assert Medicine.query.count() == 0


def test_medicines_model_representation(medicine):
    assert str(medicine) == "<Medicine 1>"

