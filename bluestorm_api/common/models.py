from sqlalchemy_utils import Timestamp, TimezoneType

from ..db import db


class BaseModel(db.Model, Timestamp):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"
