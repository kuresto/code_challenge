from flask import Blueprint, Response, request
from .models import Provider
from .schemas import ProviderSchema

from ..common.responses import (
    response_created,
    response_no_content,
    response_not_found,
    response_ok,
)
from ..db import db


provider_blueprint = Blueprint("provider", __name__, url_prefix="/providers")
schema = ProviderSchema()


@provider_blueprint.route("/", methods=["GET"])
def listing():
    instances = Provider.query.all()

    data = schema.jsonify(instances, many=True)
    return response_ok(data)


@provider_blueprint.route("/<int:id>", methods=["GET"])
def fetch(id):
    instance = Provider.query.filter_by(id=id).first()

    if not instance:
        return response_not_found()

    data = schema.jsonify(instance)
    return response_ok(data)


@provider_blueprint.route("/", methods=["POST"])
def create():
    request_data = request.get_json(force=True)

    instance = Provider.create(**request_data)

    data = schema.jsonify(instance)
    return response_created(data)


@provider_blueprint.route("/<int:id>", methods=["PUT"])
def update(id):
    request_data = request.get_json(force=True)

    instance = Provider.query.filter_by(id=id).first()

    if not instance:
        return response_not_found()

    instance.update(**request_data)

    data = schema.jsonify(instance)

    return response_ok(data)


@provider_blueprint.route("/<int:id>", methods=["DELETE"])
def destroy(id):
    instance = Provider.query.filter_by(id=id).first()
    instance.delete()
    return response_no_content()
