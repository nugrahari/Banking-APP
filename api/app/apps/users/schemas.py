
import phonenumbers
from uuid import UUID

from typing import Optional, List
from pydantic import BaseModel, constr, validator

from libs import schemas
from . import models as user_models


class TransactionInit(BaseModel):
    initial_deposit: float

    @validator('initial_deposit')
    def minimum_deposit(value, values):
        if value < 5000:
            raise ValueError(
                f'Initial deposit amount must be more than or equal to 5000')
        if len(str(value).split('.')[-1]) >= 3:
            raise ValueError(f'max two digits after decimal points')

        return value


class UserIn(BaseModel):
    name: constr(min_length=1, max_length=25, regex=r'^[a-zA-Z][\sa-zA-Z]*$')
    phone_number: str = '+62'
    email_address: constr(min_length=1, max_length=25,
                          regex=r'[a-zA-Z0-9_\-\.]+[@][a-z]+[\.][a-z]{2,3}')
    tax_id: constr(min_length=1, max_length=6, regex=r'[0-9]*$')
    address: str
    role: user_models.RoleEnum = user_models.RoleEnum.user

    @validator('phone_number')
    def phone_must_valid(cls, value) -> str:
        try:
            phone_parse = phonenumbers.parse(value)
            phone_formatted = phonenumbers.format_number(
                phone_parse, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.phonenumberutil.NumberParseException as exception:
            raise ValueError(str(exception)) from exception
        return phone_formatted

    class Config:
        orm_mode = True


class RegisterIn(TransactionInit, UserIn):
    password: str
    password2: str

    @validator('password2')
    def password_required(value, values):
        if value != values.get('password'):
            raise ValueError(f'Password not same')
        return value


class User(UserIn):
    id: UUID
    account_number: str


class UserOut(schemas.ResponseMessageDataItemOut):
    data: User


class UsersOut(schemas.ResponseMessageDataListOut):
    data: Optional[List[User]]
