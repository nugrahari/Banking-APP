
import phonenumbers
from pydantic import BaseModel, constr, validator


class LogIn(BaseModel):
    phone_number: constr(strip_whitespace=True,
                         to_lower=True, min_length=1) = '+62'
    password: str

    @validator('phone_number')
    def phone_must_valid(cls, value) -> str:  # pylint: disable=no-self-argument
        try:
            phone_parse = phonenumbers.parse(value)
            phone_formatted = phonenumbers.format_number(
                phone_parse, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.phonenumberutil.NumberParseException as exception:
            raise ValueError(str(exception)) from exception
        return phone_formatted


class RegisterLoginDataOut(BaseModel):
    token: str
