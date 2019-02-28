import pytest

from hamcrest import assert_that, has_entries, has_key

from bluestorm_api.providers.models import Provider
from bluestorm_api.providers.schemas import ProviderSchema


def test_provider_schema_dump(provider):
    schema = ProviderSchema()
    data = schema.dump(provider).data

    assert_that(
        data,
        has_entries(
            {"id": provider.id, "name": provider.name, "phone": str(provider.phone)}
        ),
    )

    assert_that(data, has_key("created"), has_key("updated"))
