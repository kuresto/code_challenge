#!/bin/sh

export PYTHONUNBUFFERED=0
export FLASK_SETTINGS_MODULE=bluestorm_api.settings.development
export FLASK_APP=./bluestorm_api/
export MINIO_ACCESS_KEY=X0UPMLLFW54LALL86ND6
export MINIO_SECRET_KEY=F3evyDre0kr4x4u8QFtR6iUmQc+0RVyB/m171TGI
export MINIO_ENDPOINT=http://bluestorm_minio:9000/

pip install -r ./requirements/development.txt

flask run