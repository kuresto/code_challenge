from sqlalchemy_utils import PhoneNumberType

from ..common.models import BaseModel
from ..db import db

tags = db.Table(
    "customer_x_medicines",
    db.Column(
        "customer_id", db.Integer, db.ForeignKey("customer.id"), primary_key=True
    ),
    db.Column(
        "medicine_id", db.Integer, db.ForeignKey("medicine.id"), primary_key=True
    ),
)


class Customer(BaseModel):
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(PhoneNumberType, nullable=False)

    medicines = db.relationship(
        "Medicine",
        secondary=tags,
        lazy="subquery",
        backref=db.backref("customers", lazy=True),
    )
