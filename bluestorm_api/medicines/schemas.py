from marshmallow import validates, ValidationError, fields, pre_dump, post_dump
from flask_marshmallow.sqla import ModelSchema

from phonenumbers import parse as parse_phone, is_valid_number, phonenumberutil

from .models import Medicine
from ..providers.schemas import ProviderSchema


class MedicineSchema(ModelSchema):
    class Meta:
        model = Medicine

    @post_dump(pass_original=True)
    def represent_kind(self, data, original_data):
        data["kind"] = original_data.kind.value
        return data

    @classmethod
    def json(cls):
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "kind": {"type": "string"},
                "dosage": {"type": "string"},
                "measure": {"type": "string"},
                "amount": {"type": "number"},
                "provider_id": {"type": "integer"},
            },
            "required": ["name", "type", "dosage", "measure", "amount", "provider_id"],
        }


class MedicineWithProviderSchema(MedicineSchema):

    provider = fields.Nested(ProviderSchema, exclude=["medicines"])

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
