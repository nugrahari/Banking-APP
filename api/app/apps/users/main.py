from uuid import UUID

import fastapi as fa

from libs import schemas, db
from apps.auth import libs as auth_libs
from apps.transactions import schemas as trans_schemas, services as trans_services
from . import schemas as user_schemas, services as user_services


app = fa.FastAPI(
    title='Asklora Bank APP Versi 0.0.0 - Admin Users',
    dependencies=[fa.Depends(auth_libs.AuthAdmin)]
)


@app.post('/', status_code=201, tags=['users'], response_model=user_schemas.UserOut)
async def create_account(form_data: user_schemas.RegisterIn):
    with db.session() as db_:
        service_db = user_services.UserService(db_)
        data_db = service_db.register(form_data)
        response = schemas.ResponseMessageDataItemOut(
            data=user_schemas.User.from_orm(data_db)
        )

    return response


@app.get('/', tags=['users'], response_model=user_schemas.UsersOut)
async def get_accounts():
    with db.session() as db_:
        service_db = user_services.UserService(db_)
        data_db = service_db.read_all()

        response = user_schemas.UsersOut(
            data=data_db
        )

    return response


@app.post('/transactions/withdraw', tags=['user transaction'], response_model=trans_schemas.TransactionOut)
async def post_transactions_withdraw(form_data: trans_schemas.WithdrawTransaction):
    with db.session() as db_:
        service_tran = trans_services.TransactionService(
            db_, user_id=form_data.user_id, data_id=None)
        service_user = user_services.UserService(
            db_, data_id=form_data.user_id)
        data_user = service_user.read_user_by_id()
        data_tran, previous_balance = service_tran.withdraw(form_data)
        total_balance = service_tran.total_amount()
        response = trans_schemas.TransactionOut(
            user_data=trans_schemas.UserData(
                id=data_user.id, name=data_user.name, account_number=data_user.account_number),
            transaction_data=data_tran,
            previous_balance=previous_balance,
            total_balance=total_balance
        )

    return response


@app.post('/transactions/deposit', tags=['user transaction'], response_model=trans_schemas.TransactionOut)
async def post_transactions_of_deposit(form_data: trans_schemas.DepositTransaction):
    with db.session() as db_:
        service_tran = trans_services.TransactionService(
            db_, user_id=form_data.user_id, data_id=None)
        service_user = user_services.UserService(
            db_, data_id=form_data.user_id)
        data_user = service_user.read_user_by_id()
        data_tran, previous_balance = service_tran.deposit(form_data)
        total_balance = service_tran.total_amount()
        response = trans_schemas.TransactionOut(
            user_data=trans_schemas.UserData(
                id=data_user.id, name=data_user.name, account_number=data_user.account_number),
            transaction_data=data_tran,
            previous_balance=previous_balance,
            total_balance=total_balance
        )

    return response


@app.get('/balance-details/{user_id}', tags=['user transaction'], response_model=schemas.ResponseMessageDataItemOut)
async def get_balance_details(user_id: UUID):
    with db.session() as db_:
        service_tran = trans_services.TransactionService(
            db_, user_id=user_id, data_id=None)
        service_user = user_services.UserService(db_, data_id=user_id)
        data_user = service_user.read_user_by_id()
        total_balance = service_tran.total_amount()
        response = schemas.ResponseMessageDataItemOut(
            data=trans_schemas.UserBalanceDetails(
                name=data_user.name,
                email_address=data_user.email_address,
                address=data_user.address,
                phone_number=data_user.phone_number,
                total_balance=total_balance
            )
        )

    return response
