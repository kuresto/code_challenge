from time import sleep

import pytest

from phonenumbers import parse as parse_phonenumber

from bluestorm_api.providers.models import Provider


@pytest.fixture(name="provider")
def fixture_provider(mixer):
    return mixer.blend(Provider, name=mixer.FAKE, phone="+55 16 97122 2222")


def test_provider_model_creation(provider):
    db_provider = Provider.query.first()

    assert provider == db_provider


def test_provider_model_update(db, provider):
    old_updated = provider.updated

    provider.name = "another"
    sleep(1)
    db.session.commit()

    db_provider = Provider.query.first()

    assert db_provider.name == "another"
    assert db_provider.updated != old_updated


def test_provider_model_removal(db, provider):
    db.session.delete(provider)
    assert Provider.query.count() == 0


def test_provider_model_representation(provider):
    assert str(provider) == "<Provider 1>"

