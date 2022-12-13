from apps.auth.conftest import *

from .main import app
from libs import tests

client = tests.MyTestClient(app)


def get_data(user, admin1_token):
    response, _ = client.post_parsed(
        '/', json=user.dict(), auth=admin1_token)
    return response.get('data')


@pytest.fixture(name="user1_data")
def fixture_user1_data(user1, admin1_token):
    return get_data(user1, admin1_token)


@pytest.fixture(name="user2_data")
def fixture_user2_data(user2, admin1_token):
    return get_data(user2, admin1_token)


@pytest.fixture(name="user3_data")
def fixture_user3_data(user3, admin1_token):
    return get_data(user3, admin1_token)


@pytest.fixture(name="user4_data")
def fixture_user4_data(user4, admin1_token):
    return get_data(user4, admin1_token)
