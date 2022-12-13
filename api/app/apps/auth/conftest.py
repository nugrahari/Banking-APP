import pytest

from .main import app
from libs import tests

client = tests.MyTestClient(app)


def get_token(user):
    data = {"phone_number": user.phone_number, "password": user.password}
    response, _ = client.post_parsed('/login', json=data)
    return response.get('token')


@pytest.fixture(name="admin1_token")
def fixture_admin1_token(admin1):
    return get_token(admin1)
