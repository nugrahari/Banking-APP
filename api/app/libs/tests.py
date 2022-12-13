from json import JSONDecodeError
from typing import Tuple

from fastapi.testclient import TestClient
from pydantic import BaseModel


class UserTest(BaseModel):
    name: str
    initial_deposit: float = 8005.42
    phone_number: str
    email_address: str
    tax_id: str
    address: str
    role: str
    password: str
    password2: str


def set_auth_headers(**kwargs):
    if 'auth' in kwargs:
        kwargs.setdefault('headers', {})
        kwargs['headers'].update(
            {'Authorization': f"bearer {kwargs.get('auth')}"})
        del kwargs['auth']
    return kwargs


class MyTestClient(TestClient):
    def get_parsed(self, *args, **kwargs):
        kwargs = set_auth_headers(**kwargs)

        response = self.get(*args, **kwargs)
        return parse_response(response)

    def post_parsed(self, *args, **kwargs):
        kwargs = set_auth_headers(**kwargs)

        response = self.post(*args, **kwargs)
        return parse_response(response)

    def patch_parsed(self, *args, **kwargs):
        kwargs = set_auth_headers(**kwargs)

        response = self.patch(*args, **kwargs)
        return parse_response(response)

    def put_parsed(self, *args, **kwargs):
        kwargs = set_auth_headers(**kwargs)

        response = self.put(*args, **kwargs)
        return parse_response(response)

    def delete_parsed(self, *args, **kwargs):
        kwargs = set_auth_headers(**kwargs)

        response = self.delete(*args, **kwargs)
        return parse_response(response)


def parse_response(response) -> Tuple[dict, int]:
    try:
        response_json_or_raw = response.json()
    except JSONDecodeError:
        response_json_or_raw = response
    return response_json_or_raw, response.status_code
