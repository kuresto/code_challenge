from marshmallow import validates, ValidationError
from flask_marshmallow.sqla import ModelSchema

from phonenumbers import parse as parse_phone, is_valid_number, phonenumberutil

from .models import Provider


class ProviderSchema(ModelSchema):
    class Meta:
        model = Provider

    @validates("phone")
    def validate_phone(self, value):
        try:
            parse_phone(value)
        except phonenumberutil.NumberParseException:
            raise ValidationError("invalid phone number", "phone")

    @classmethod
    def json(cls):
        return {
            "type": "object",
            "properties": {"name": {"type": "string"}, "phone": {"type": "string"}},
            "required": ["name", "phone"],
        }
