from marshmallow import pre_load, ValidationError
from flask_marshmallow.sqla import ModelSchema

from phonenumbers import parse as parse_phone, is_valid_number, phonenumberutil

from .models import Provider


class ProviderSchema(ModelSchema):
    class Meta:
        model = Provider

    @pre_load
    def validate_phone(self, in_data):
        try:
            parse_phone(in_data.get("phone"))
        except phonenumberutil.NumberParseException:
            raise ValidationError("invalid phone number", "phone")

        return in_data

    @classmethod
    def json(cls):
        return {
            "type": "object",
            "properties": {"name": {"type": "string"}, "phone": {"type": "string"}},
            "required": ["name", "phone"],
        }
