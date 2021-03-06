import json

from flask import g, Blueprint, Response, request
from flask_expects_json import expects_json
from flask_jwt_extended import jwt_required, current_user

from .models import Provider
from .schemas import ProviderSchema

from ..common.exceptions import InvalidUsage
from ..common.responses import (
    response_created,
    response_no_content,
    response_not_found,
    response_ok,
    response_bad_request,
    response_listing,
)
from ..db import db


provider_blueprint = Blueprint("provider", __name__, url_prefix="/providers")
schema = ProviderSchema()


@provider_blueprint.route("/", methods=["GET"])
@jwt_required
def listing():
    paginate = Provider.query.paginate()
    data = schema.jsonify(paginate.items, many=True)
    return response_listing(paginate, data)


@provider_blueprint.route("/<int:id>", methods=["GET"])
@jwt_required
def fetch(id):
    instance = Provider.query.filter_by(id=id).first()

    if not instance:
        return response_not_found()

    data = schema.jsonify(instance)
    return response_ok(data)


@provider_blueprint.route("/", methods=["POST"])
@expects_json(ProviderSchema.json())
@jwt_required
def create():
    request_data = g.data

    errors = schema.validate(request_data)
    if errors:
        raise InvalidUsage(errors)

    instance = Provider.create(**request_data)

    data = schema.jsonify(instance)
    return response_created(data)


@provider_blueprint.route("/<int:id>", methods=["PUT"])
@expects_json(ProviderSchema.json())
@jwt_required
def update(id):
    request_data = g.data

    errors = schema.validate(request_data)
    if errors:
        raise InvalidUsage(errors)

    instance = Provider.query.filter_by(id=id).first()

    if not instance:
        return response_not_found()

    instance.update(**request_data)

    data = schema.jsonify(instance)

    return response_ok(data)


@provider_blueprint.route("/<int:id>", methods=["DELETE"])
@jwt_required
def destroy(id):
    instance = Provider.query.filter_by(id=id).first()
    instance.delete()
    return response_no_content()
