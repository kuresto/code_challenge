import json
import csv

from io import StringIO

from flask import g, Blueprint, Response, request, make_response
from flask_expects_json import expects_json
from flask_jwt_extended import jwt_required, current_user

from .models import Customer
from .schemas import CustomerSchema

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


customer_blueprint = Blueprint("customer", __name__, url_prefix="/customers")
schema = CustomerSchema()


@customer_blueprint.route("/", methods=["GET"])
@jwt_required
def listing():
    """List costumers
    ---
    responses:
      200:
        description: Token
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                phone:
                  type: string
                created:
                  type: datetime
                uppdated:
                  type: datetime
    """
    paginate = Customer.query.paginate()
    data = schema.jsonify(paginate.items, many=True)
    return response_listing(paginate, data)


@customer_blueprint.route("/<int:id>", methods=["GET"])
@jwt_required
def fetch(id):
    """Fetch costumer
    ---
    responses:
      200:
        description: Token
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                phone:
                  type: string
                created:
                  type: datetime
                uppdated:
                  type: datetime
    """
    instance = Customer.query.filter_by(id=id).first()

    if not instance:
        return response_not_found()

    data = schema.jsonify(instance)
    return response_ok(data)


@customer_blueprint.route("/", methods=["POST"])
@expects_json(CustomerSchema.json())
@jwt_required
def create():
    """Create costumer
    ---
    parameters:
      - name: name
        in: json
        type: string
        required: true
      - name: phone
        in: json
        type: string
        required: true
        description: "Use format: +55 16 98754-3210"
    responses:
      200:
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                phone:
                  type: string
                created:
                  type: datetime
                uppdated:
                  type: datetime
    """
    request_data = g.data

    errors = schema.validate(request_data)
    if errors:
        raise InvalidUsage(errors)

    instance = Customer.create(**request_data)

    data = schema.jsonify(instance)
    return response_created(data)


@customer_blueprint.route("/<int:id>", methods=["PUT"])
@expects_json(CustomerSchema.json())
@jwt_required
def update(id):
    """Updates costumer
    ---
    parameters:
      - name: name
        in: json
        type: string
        required: true
      - name: phone
        in: json
        type: string
        required: true
        description: "Use format: +55 16 98754-3210"
    responses:
      200:
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                phone:
                  type: string
                created:
                  type: datetime
                uppdated:
                  type: datetime
    """
    request_data = g.data

    errors = schema.validate(request_data)
    if errors:
        raise InvalidUsage(errors)

    instance = Customer.query.filter_by(id=id).first()

    if not instance:
        return response_not_found()

    instance.update(**request_data)

    data = schema.jsonify(instance)

    return response_ok(data)


@customer_blueprint.route("/<int:id>", methods=["DELETE"])
@jwt_required
def destroy(id):
    """Removes single costumer
    ---
    responses:
      204:
        description: "Removed"
    """
    instance = Customer.query.filter_by(id=id).first()
    instance.delete()
    return response_no_content()


@customer_blueprint.route("/<int:id>/export/", methods=["GET"])
@jwt_required
def export_csv(id):
    """Exports all costumer medications
    ---
    responses:
      Download:
        description: Downloads a csv file
    """
    instance = Customer.query.filter_by(id=id).first()

    if not instance:
        return response_not_found()

    rows = [["user_id", "user_name", "medicine_id", "medicine_name"]]
    for medicine in instance.medicines:
        rows.append([instance.id, instance.name, medicine.id, medicine.name])

    string_io = StringIO()

    writer = csv.writer(string_io)
    writer.writerows(rows)
    response = make_response(string_io.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    response.headers["Content-type"] = "text/csv"

    return response
