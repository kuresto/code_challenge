from sqlalchemy_utils import PhoneNumberType

from ..common.models import BaseModel
from ..db import db


class Provider(BaseModel):
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(PhoneNumberType, nullable=False)
