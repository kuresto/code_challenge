import pytest

from bluestorm_api.customers.models import Customer
from bluestorm_api.providers.models import Provider
from bluestorm_api.medicines.models import Medicine


@pytest.fixture(name="provider")
def fixture_provider(mixer):
    return mixer.blend(Provider, name=mixer.FAKE, phone="+55 16 97122 2222")


@pytest.fixture(name="medicines")
def fixture_medicines(mixer, provider):
    return mixer.cycle(5).blend(
        Medicine,
        name=mixer.FAKE,
        kind="tablet",
        dosage=mixer.FAKE,
        measure=mixer.FAKE,
        amount=mixer.FAKE,
        provider=provider,
    )


@pytest.fixture(name="customer")
def fixture_customer(mixer):
    return mixer.blend(Customer, name=mixer.FAKE, phone="+55 16 97122 2222")


@pytest.fixture(name="customer_with_medicines")
def fixture_customer_with_medicines(mixer, medicines):
    customer = mixer.blend(Customer, name=mixer.FAKE, phone="+55 16 97122 2222")
    customer.medicines = customer.medicines + medicines
    customer.save()

    return customer


@pytest.fixture(name="customers")
def fixture_customers(mixer):
    return mixer.cycle(5).blend(Customer, name=mixer.FAKE, phone="+55 16 97122 2222")
