import pytest

from flask_bcrypt import generate_password_hash

from bluestorm_api.accounts.models import User


@pytest.fixture(name="user")
def fixture_user(mixer):
    return mixer.blend(
        User, login=mixer.FAKE, password=generate_password_hash("102030")
    )


@pytest.fixture(name="users")
def fixture_users(mixer):
    return mixer.cycle(5).blend(
        User, login=mixer.FAKE, password=generate_password_hash("102030")
    )
