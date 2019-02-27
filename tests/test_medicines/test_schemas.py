import pytest

from hamcrest import assert_that, has_entries, has_key

from bluestorm_api.medicines.models import Medicine
from bluestorm_api.medicines.schemas import MedicineSchema, MedicineWithProviderSchema


def test_medicine_schema_dump(medicine):
    schema = MedicineSchema(exclude=["customers"])
    data = schema.dump(medicine).data

    assert_that(
        data,
        has_entries(
            {
                "measure": medicine.measure,
                "name": medicine.name,
                "id": 1,
                "dosage": medicine.dosage,
                "amount": medicine.amount,
                "kind": medicine.kind.value,
                "provider": medicine.provider_id,
            }
        ),
    )

    assert_that(data, has_key("created"), has_key("updated"))


def test_medicine_with_provider_schema_dump(medicine):
    schema = MedicineWithProviderSchema(exclude=["customers"])
    data = schema.dump(medicine).data

    assert_that(
        data,
        has_entries(
            {
                "measure": medicine.measure,
                "name": medicine.name,
                "id": 1,
                "dosage": medicine.dosage,
                "amount": medicine.amount,
                "kind": medicine.kind.value,
                "provider": has_entries(
                    {
                        "name": medicine.provider.name,
                        "id": medicine.provider.id,
                        "phone": str(medicine.provider.phone),
                    }
                ),
            }
        ),
    )

    assert_that(data, has_key("created"), has_key("updated"))
