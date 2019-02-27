from time import sleep

import pytest

from ..fixtures.models import FakeModel


def test_base_model_creation(db):
    fake_model = FakeModel.create(**{"name": "fake-name"})

    db_fake_model = FakeModel.query.first()

    assert fake_model == db_fake_model


def test_base_model_save(db):
    fake_model = FakeModel(**{"name": "fake-name"})
    fake_model.save()

    db_fake_model = FakeModel.query.first()

    assert fake_model == db_fake_model


def test_base_model_update(db, mixer):
    fake_model = mixer.blend(FakeModel)
    old_updated = fake_model.updated

    data = {"name": "fake-2"}
    sleep(1)  # Test was running too fast :/
    fake_model.update(**data)

    db_fake_model = FakeModel.query.first()

    assert db_fake_model.name == "fake-2"
    assert db_fake_model.updated != old_updated


def test_base_model_removal(db, mixer):
    fake_model = mixer.blend(FakeModel)
    fake_model.delete()

    assert FakeModel.query.count() == 0


def test_base_model_representation(mixer):
    fake_model = mixer.blend(FakeModel)

    assert str(fake_model) == "<FakeModel 1>"

