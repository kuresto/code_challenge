from flask_marshmallow.sqla import ModelSchema

from .models import Provider


class ProviderSchema(ModelSchema):
    class Meta:
        model = Provider

