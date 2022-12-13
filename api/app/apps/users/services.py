
import time
from passlib.hash import sha256_crypt

import fastapi as fa

import sqlalchemy as sa
from sqlalchemy.exc import NoResultFound


from . import models as user_models
from apps.transactions import models as transaction_models


class UserService():
    def __init__(self, db_: sa.orm.Session, data_id=None):
        self.db: sa.orm.Session = db_
        self.data_id = data_id
        self.query: sa.orm.Query = self.db.query(user_models.UserDB)
        self.query_transaction = self.db.query(
            transaction_models.TransactionDB)

    def read_all(self):
        return self.query.filter(user_models.UserDB.role == user_models.RoleEnum.user).all()

    def register(self, form_data):
        encript_password = sha256_crypt.encrypt(form_data.password)
        user_data = form_data.dict()
        del user_data['password2']
        del user_data['initial_deposit']
        user_data['password'] = encript_password
        user_data['account_number'] = ''.join(str(time.time()).split('.'))
        try:
            data_db = user_models.UserDB(**user_data)
            self.db.add(data_db)
            self.db.commit()
            tran_db = transaction_models.TransactionDB(
                type="deposit", user_id=data_db.id, amount=form_data.initial_deposit)
            self.db.add(tran_db)
            self.db.commit()
        except Exception as err:
            raise fa.HTTPException(400, detail=F'error : {err}')

        return data_db

    def read_user_by_id(self):
        try:
            data_db = self.query.filter(
                user_models.UserDB.id == self.data_id).one()
        except NoResultFound as exc:
            raise fa.HTTPException(404, detail="User not found") from exc
        return data_db
