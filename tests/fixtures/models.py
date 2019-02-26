import pytest

from bluestorm_api.db import db
from bluestorm_api.common.models import BaseModel


class FakeModel(BaseModel):
    name = db.Column(db.String(16), default="fake")
