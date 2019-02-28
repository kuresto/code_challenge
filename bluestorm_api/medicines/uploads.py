import os

from flask import current_app

from minio import Minio
from minio.error import ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists


def minio_client():
    client = Minio(
        current_app.config.get("MINIO_ENDPOINT"),
        access_key=current_app.config.get("MINIO_ACCESS_KEY"),
        secret_key=current_app.config.get("MINIO_SECRET_KEY"),
        secure=current_app.config.get("MINIO_SECURE"),
    )

    return client


def minio_upload(upload_file):
    bucket = "uploads"
    filepath = os.path.join("/tmp/", upload_file.filename)

    upload_file.save(filepath)

    client = minio_client()

    try:
        client.make_bucket(bucket, location="us-east-1")
    except BucketAlreadyOwnedByYou as err:
        pass
    except BucketAlreadyExists as err:
        pass
    except ResponseError as err:
        raise

    response = client.fput_object(bucket, upload_file.filename, filepath)

    return os.path.join(bucket, upload_file.filename)


def minio_get(filepath):
    bucket, filename = filepath.split("/")
    client = minio_client()

    response = client.get_object(bucket, filename)

    return response
