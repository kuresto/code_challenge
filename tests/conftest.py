import pytest
from bluestorm_api.app import create_app


@pytest.fixture(name="app", autouse=True)
def fixture_app():
    return create_app()
