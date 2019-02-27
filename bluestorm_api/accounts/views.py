import json

from flask import g, Blueprint, Response, request
from flask_expects_json import expects_json
from flask_jwt_extended import (
    jwt_required,
    jwt_optional,
    create_access_token,
    current_user,
)

from .models import User
from .schemas import UserSchema, AuthSchema

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


user_blueprint = Blueprint("accounts", __name__, url_prefix="/accounts")
auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")
user_schema = UserSchema()
auth_schema = AuthSchema()


@auth_blueprint.route("/", methods=["POST"])
@expects_json(AuthSchema.json())
@jwt_optional
def login():
    request_data = g.data
    login = g.data.get("login")
    password = g.data.get("password")

    user = User.query.filter((User.login == login) & (User.is_active == True)).first()

    if not user or user.validate_password(password) is False:
        return response_not_found()

    token = create_access_token(identity=user, fresh=True)

    data = auth_schema.jsonify({"token": token})
    return response_ok(data)


@user_blueprint.route("/", methods=["GET"])
@jwt_required
def listing():
    paginate = User.query.paginate()
    data = user_schema.jsonify(paginate.items, many=True)
    return response_listing(paginate, data)


@user_blueprint.route("/<int:id>", methods=["GET"])
@jwt_required
def fetch(id):
    instance = User.query.filter_by(id=id).first()

    if not instance:
        return response_not_found()

    data = user_schema.jsonify(instance)
    return response_ok(data)


@user_blueprint.route("/", methods=["POST"])
@expects_json(UserSchema.json())
@jwt_required
def create():
    request_data = g.data

    errors = user_schema.validate(request_data)
    if errors:
        raise InvalidUsage(errors)

    instance = User(**request_data)
    instance.save()

    instance.token = create_access_token(identity=instance, fresh=True)

    data = user_schema.jsonify(instance)
    return response_created(data)


@user_blueprint.route("/<int:id>", methods=["PUT"])
@expects_json(UserSchema.json())
@jwt_required
def update(id):
    request_data = g.data

    instance = User.query.filter_by(id=id).first()

    if not instance:
        return response_not_found()

    user_schema.instance = instance

    errors = user_schema.validate(request_data)
    if errors:
        raise InvalidUsage(errors)

    request_data.pop("password")
    instance.update(**request_data, commit=False)

    data = user_schema.jsonify(instance)

    return response_ok(data)


@user_blueprint.route("/<int:id>", methods=["DELETE"])
@jwt_required
def destroy(id):
    instance = User.query.filter_by(id=id).first()
    instance.delete()
    return response_no_content()
