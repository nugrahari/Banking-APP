from uuid import UUID

from typing import Optional
from pydantic import BaseModel, validator

from libs import schemas
from . import models as trans_models


class UserBalanceDetails(BaseModel):
    name: str
    email_address: str
    address: str
    phone_number: str
    total_balance: float


class UserData(BaseModel):
    id: UUID
    name: str
    account_number: str


class GetTransaction(BaseModel):
    user_id: UUID


class TransactionIn(GetTransaction):
    amount: float


class WithdrawTransaction(TransactionIn):

    @validator('amount')
    def minimum_withdraw(value, values):
        if value < 10:
            raise ValueError(
                f'Initial withdraw amount must be more than or equal to 10')
        if len(str(value).split('.')[-1]) >= 3:
            raise ValueError(f'max two digits after decimal points')

        if value < 5000 and value > 500:
            value += 10
        elif value > 5000:
            value += 20
        return value


class DepositTransaction(TransactionIn):

    @validator('amount')
    def minimum_deposit(value, values):
        if value < 500:
            raise ValueError(
                f'Value deposit amount must be more than or equal to 500')
        if len(str(value).split('.')[-1]) >= 3:
            raise ValueError(f'max two digits after decimal points')

        return value


class Transaction(TransactionIn):
    id: UUID
    type: trans_models.TransactionEnum

    class Config:
        orm_mode = True


class TransactionOut(schemas.ResponseMessageOut):
    user_data: UserData
    transaction_data: Transaction
    previous_balance: Optional[float]
    total_balance: float
