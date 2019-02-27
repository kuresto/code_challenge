from marshmallow import pre_load, ValidationError
from flask_marshmallow.sqla import SchemaModel, Schema

from phonenumbers import parse as parse_phone, is_valid_number, phonenumberutil

from .models import User


class UserSchema(ModelSchema):
    class Meta:
        model = User

    @classmethod
    def json(cls):
        return {
            "type": "object",
            "properties": {
                "login": {"type": "string"},
                "password": {"type": "string"},
                "is_active": {"type": "boolean"},
            },
            "required": ["login", "password", "is_active"],
        }


class AuthSchema(Schema):
    class Meta:
        fields = ("login", "password")

    @classmethod
    def json(cls):
        return {
            "type": "object",
            "properties": {
                "login": {"type": "string"},
                "password": {"type": "string"},
                "is_active": {"type": "boolean"},
            },
            "required": ["login", "password", "is_active"],
        }
