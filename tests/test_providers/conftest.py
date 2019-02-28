import pytest

from bluestorm_api.providers.models import Provider


@pytest.fixture(name="provider")
def fixture_provider(mixer):
    return mixer.blend(Provider, name=mixer.FAKE, phone="+55 16 97122 2222")


@pytest.fixture(name="providers")
def fixture_providers(mixer):
    return mixer.cycle(5).blend(Provider, name=mixer.FAKE, phone="+55 16 97122 2222")
