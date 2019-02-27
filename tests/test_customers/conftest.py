import pytest

from bluestorm_api.customers.models import Customer


@pytest.fixture(name="customer")
def fixture_customer(mixer):
    return mixer.blend(Customer, name=mixer.FAKE, phone="+55 16 97122 2222")


@pytest.fixture(name="customers")
def fixture_customers(mixer):
    return mixer.cycle(5).blend(Customer, name=mixer.FAKE, phone="+55 16 97122 2222")
