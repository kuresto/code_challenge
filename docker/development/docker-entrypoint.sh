#!/usr/bin/env bash
set -e

dockerize -wait tcp://bluestorm_minio:9000

mc config host add minio $MINIO_ENDPOINT $MINIO_ACCESS_KEY $MINIO_SECRET_KEY

exec "$@"
