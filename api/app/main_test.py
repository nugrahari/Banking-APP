
from main import app
from libs import tests

client = tests.MyTestClient(app)


def test_get_root() -> None:
    _, status = client.get_parsed('/')
    assert status == 200
