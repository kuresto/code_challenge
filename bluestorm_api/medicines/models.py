from sqlalchemy_utils import ChoiceType

from ..common.models import BaseModel
from ..db import db


class Medicine(BaseModel):
    KIND = [
        ("tablet", "tablet"),
        ("syrup", "syrup"),
        ("drops", "drops"),
        ("capsule", "capsule"),
        ("eyedrops", "eye drops"),
        ("solution", "solution"),
        ("suspension", "suspension"),
        ("cream", "cream"),
        ("ointment", "ointment"),
        ("injection", "injection"),
    ]

    kind = db.Column(ChoiceType(KIND))
    name = db.Column(db.String(120), nullable=False)
    dosage = db.Column(db.Integer, nullable=False)
    measure = db.Column(db.String(16), nullable=False)
    amount = db.Column(db.Numeric(precision=19, scale=4), default=0)

    provider_id = db.Column(db.Integer, db.ForeignKey("provider.id"), nullable=False)
