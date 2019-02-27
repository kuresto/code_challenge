import pytest

from hamcrest import assert_that, has_entries, has_key

from bluestorm_api.customers.models import Customer
from bluestorm_api.customers.schemas import CustomerSchema


def test_customer_schema_dump(customer):
    schema = CustomerSchema()
    data = schema.dump(customer).data

    assert_that(
        data,
        has_entries(
            {"id": customer.id, "name": customer.name, "phone": str(customer.phone)}
        ),
    )

    assert_that(data, has_key("created"), has_key("updated"))
