from decimal import Decimal
from flask.json import JSONEncoder

from .models import User


def jwt_identity(payload):
    return User.query.get(payload)


def identity_loader(user):
    return user.id


class DecimalJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)
