import json
import csv
from decimal import Decimal
from io import StringIO

from werkzeug.utils import secure_filename

from flask import g, Blueprint, Response, request, jsonify
from flask_expects_json import expects_json
from flask_jwt_extended import jwt_required, current_user

from .models import Medicine
from .schemas import MedicineSchema, MedicineWithProviderSchema
from .csv import validate_csv
from .uploads import minio_upload, minio_get

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


upload_blueprint = Blueprint("upload", __name__, url_prefix="/uploads")
medicine_blueprint = Blueprint("medicine", __name__, url_prefix="/medicines")
schema_write = MedicineSchema()
schema = MedicineWithProviderSchema()
csv_schema = {
    "type": "object",
    "properties": {"file": {"type": "string"}},
    "required": ["file"],
}


@upload_blueprint.route("/", methods=["POST"])
@jwt_required
def upload():
    """Uploads a csv file
    ---
    description: "Receives a file from a form"
    responses:
      201:
        content:
          application/json:
            schema:
              type: object
              properties:
                file:
                  type: string
    """
    if "csv" not in request.files:
        return response_bad_request(jsonify({"error": "no key in request"}))

    upload_file = request.files["csv"]

    if upload_file.filename == "":
        return response_bad_request(jsonify({"error": "no file selected"}))

    upload_file.filename = secure_filename(upload_file.filename)

    filepath = minio_upload(upload_file)
    return response_created(jsonify({"file": filepath}))


@upload_blueprint.route("/process_csv", methods=["POST"])
@jwt_required
@expects_json(csv_schema)
def process_csv():
    """Imports from csv medications
    ---
    parameters:
      - name: file
        in: json
        type: string
        required: true
        description: "Full filepath"
    responses:
      200:
        description: OK.
    """

    request_data = g.data
    csv_path = request_data.get("file")

    # TODO: This should be a task (celery)
    uploaded_csv = minio_get(csv_path)

    f = StringIO(uploaded_csv.data.decode())
    reader_validation = csv.reader(f, delimiter=",", quoting=csv.QUOTE_ALL)

    f = StringIO(uploaded_csv.data.decode())
    reader = csv.reader(f, delimiter=",", quoting=csv.QUOTE_ALL)

    has_errors = validate_csv(reader_validation)

    if has_errors:
        return response_bad_request(jsonify({"error": "invalid csv format"}))

    records = []

    next(reader, None)
    for row in reader:
        provider_id = row[0]
        kind = row[1]
        name = row[2]
        dosage = row[3]
        measure = row[4]
        amount = Decimal(row[5])

        medicine = Medicine(
            provider_id=provider_id,
            kind=kind,
            name=name,
            dosage=dosage,
            measure=measure,
            amount=amount,
        )

        records.append(medicine)

    if len(records) >= 1:
        db.session.bulk_save_objects(records)

    return response_ok()


@medicine_blueprint.route("/", methods=["GET"])
@jwt_required
def listing():
    paginate = Medicine.query.paginate()
    data = schema.jsonify(paginate.items, many=True)
    return response_listing(paginate, data)


@medicine_blueprint.route("/<int:id>", methods=["GET"])
@jwt_required
def fetch(id):
    instance = Medicine.query.filter_by(id=id).first()

    if not instance:
        return response_not_found()

    data = schema.jsonify(instance)
    return response_ok(data)


@medicine_blueprint.route("/", methods=["POST"])
@expects_json(MedicineSchema.json())
@jwt_required
def create():
    request_data = g.data

    errors = schema_write.validate(request_data)
    if errors:
        raise InvalidUsage(errors)

    instance = Medicine.create(**request_data)

    data = schema.jsonify(instance)
    return response_created(data)


@medicine_blueprint.route("/<int:id>", methods=["PUT"])
@expects_json(MedicineSchema.json())
@jwt_required
def update(id):
    """Updates instance
    ---
    parameters:
      - name: name
        in: json
        type: string
        required: true
      - name: kind
        in: json
        type: string
        enum: [tablet, syrup, drops, capsule, eyedrops, solution, suspension, cream, ointment, injection]
        required: true
      - name: amount
        in: json
        type: number
        required: true
      - name: measure
        in: json
        type: string
        required: true
      - name: dosage
        in: json
        type: numer
        required: true
      - name: provider
        in: json
        type: object
        required: true
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

    errors = schema_write.validate(request_data)
    if errors:
        raise InvalidUsage(errors)

    instance = Medicine.query.filter_by(id=id).first()

    if not instance:
        return response_not_found()

    instance.update(**request_data)

    data = schema.jsonify(instance)

    return response_ok(data)


@medicine_blueprint.route("/<int:id>", methods=["DELETE"])
@jwt_required
def destroy(id):
    """Removes instance
    ---
    responses:
      204:
        description: "Removed"
    """
    instance = Medicine.query.filter_by(id=id).first()
    instance.delete()
    return response_no_content()
