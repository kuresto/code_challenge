import os
from environs import Env

env = Env()
env.read_env()


ENV = env("FLASK_ENV", "development")
DEBUG = env("FLASK_DEBUG", True)

SQLALCHEMY_DATABASE_URI = env(
    "SQLALCHEMY_DATABASE_URI",
    default="mysql://root:password@bluestorm_db:3306/bluestorm_api",
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
