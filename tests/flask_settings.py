from bluestorm_api.settings.base import *  # noqa

TESTING = True

SQLALCHEMY_DATABASE_URI = env(
    "SQLALCHEMY_DATABASE_URI", default="mysql://root:password@bluestorm_db:3306/test"
)
