import os
import pytest

from flask import url_for
from webtest.app import AppError
from hamcrest import assert_that, has_entries, has_key

from bluestorm_api.medicines.models import Medicine


CSV_FILE = os.path.abspath("/code/tests/fixtures/medicine.csv")


def test_medicine_csv_resource_upload(user_client):
    csv_fp = open(CSV_FILE, "rb")

    response = user_client.post(
        url_for("upload.upload"), upload_files=[("csv", "import.csv", csv_fp.read())]
    )

    assert response.status_code == 201

    assert_that(response.json, has_entries({"file": "uploads/import.csv"}))


def test_medicine_csv_process_csv(user_client, provider):
    csv_fp = open(CSV_FILE, "rb")

    response = user_client.post(
        url_for("upload.upload"), upload_files=[("csv", "import.csv", csv_fp.read())]
    )

    assert response.status_code == 201

    data = {"file": response.json.get("file")}
    response = user_client.post_json(url_for("upload.process_csv"), data)

    assert response.status_code == 200

    assert Medicine.query.count() == 5
