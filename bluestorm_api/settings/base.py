import os
from environs import Env

env = Env()
env.read_env()

# Flask
ENV = env("FLASK_ENV", "development")
DEBUG = env("FLASK_DEBUG", True)

# SQL Alchemy
SQLALCHEMY_DATABASE_URI = env(
    "SQLALCHEMY_DATABASE_URI",
    default="mysql://root:password@bluestorm_db:3306/bluestorm_api",
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT
JWT_SECRET_KEY = "secret-key"  # Change it on production!

# CORS
CORS_ORIGIN_WHITELIST = "*"

# MINIO
MINIO_ENDPOINT = "172.18.0.4:9000"
MINIO_ACCESS_KEY = env("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = env("MINIO_SECRET_KEY")
MINIO_SECURE = env("MINIO_SECURE", False)
