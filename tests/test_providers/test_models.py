from time import sleep

import pytest

from bluestorm_api.providers.models import Provider


def test_provider_model_creation(provider):
    db_provider = Provider.query.first()

    assert provider == db_provider


def test_provider_model_update(db, provider):
    old_updated = provider.updated

    new_data = {"name": "another"}
    sleep(1)  # Test was running too fast :/
    provider.update(**new_data)

    db_provider = Provider.query.first()

    assert db_provider.name == "another"
    assert db_provider.updated != old_updated


def test_provider_model_removal(db, provider):
    provider.delete()
    assert Provider.query.count() == 0


def test_provider_model_representation(provider):
    assert str(provider) == "<Provider 1>"

