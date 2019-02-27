from marshmallow import ValidationError, fields, validates
from flask_marshmallow.sqla import Schema, ModelSchema

from phonenumbers import parse as parse_phone, is_valid_number, phonenumberutil

from .models import User


class UserSchema(ModelSchema):

    token = fields.Method("get_token")

    class Meta:
        model = User

    def get_token(self, obj):
        return getattr(obj, "token", None)

    @validates("login")
    def validate_login(self, value):
        login_exists = User.query.filter_by(login=value)

        if self.instance:
            login_exists = login_exists.filter(User.login != value)

        login_exists = login_exists.first()
        if login_exists:
            raise ValidationError("login already registered", "login")

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
        fields = ["token"]

    @classmethod
    def json(cls):
        return {
            "type": "object",
            "properties": {"login": {"type": "string"}, "password": {"type": "string"}},
            "required": ["login", "password"],
        }
