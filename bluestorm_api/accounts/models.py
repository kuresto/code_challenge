from sqlalchemy_utils import PhoneNumberType

from ..common.models import BaseModel
from ..db import db


class User(BaseModel):
    login = db.Column(db.String(32), nullable=False)
    password = db.Column(db.Binary(128), nullable=False)
    is_active = db.Column(db.Boolean, default=1)
