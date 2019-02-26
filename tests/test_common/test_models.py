from time import sleep

import pytest

from ..fixtures.models import FakeModel


def test_base_model_creation(db, mixer):
    fake_model = mixer.blend(FakeModel)

    db_fake_model = FakeModel.query.first()

    assert fake_model == db_fake_model


def test_base_model_update(db, mixer):
    fake_model = mixer.blend(FakeModel)
    old_updated = fake_model.updated

    fake_model.name = "fake-2"

    sleep(1)
    db.session.commit()

    db_fake_model = FakeModel.query.first()

    assert db_fake_model.name == "fake-2"
    assert db_fake_model.updated != old_updated


def test_base_model_removal(db, mixer):
    fake_model = mixer.blend(FakeModel)

    db.session.delete(fake_model)
    assert FakeModel.query.count() == 0


def test_base_model_representation(mixer):
    fake_model = mixer.blend(FakeModel)

    assert str(fake_model) == "<FakeModel 1>"

