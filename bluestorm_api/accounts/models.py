from sqlalchemy_utils import PhoneNumberType
from flask_bcrypt import generate_password_hash, check_password_hash

from ..common.models import BaseModel
from ..db import db


class User(BaseModel):
    login = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.Binary(128), nullable=False)
    is_active = db.Column(db.Boolean, default=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        password = kwargs.get("password")

        self.set_password(password) if password else None

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)
