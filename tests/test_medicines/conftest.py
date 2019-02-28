import pytest

from bluestorm_api.providers.models import Provider
from bluestorm_api.medicines.models import Medicine


@pytest.fixture(name="provider")
def fixture_provider(mixer):
    return mixer.blend(Provider, name=mixer.FAKE, phone="+55 16 97122 2222")


@pytest.fixture(name="medicine")
def fixture_medicine(mixer, provider):
    return mixer.blend(
        Medicine,
        name=mixer.FAKE,
        kind="tablet",
        dosage=mixer.FAKE,
        measure=mixer.FAKE,
        amount=mixer.FAKE,
        provider=provider,
    )


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
