from .models import Provider
from .. import marshmallow


class ProviderSchema(marshmallow.ModelSchema):
    class Meta:
        model = Provider

