from marshmallow import validates, ValidationError
from flask_marshmallow.sqla import ModelSchema

from phonenumbers import parse as parse_phone, is_valid_number, phonenumberutil

from .models import Medicine


class MedicineSchema(ModelSchema):
    class Meta:
        model = Medicine

    @classmethod
    def json(cls):
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "type": {"type": "string"},
                "dosage": {"type": "string"},
                "measure": {"type": "string"},
                "amount": {"type": "number"},
                "provider_id": {"type": "integer"},
            },
            "required": ["name", "type", "dosage", "measure", "amount", "provider_id"],
        }
