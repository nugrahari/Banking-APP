import fastapi as fa


import sqlalchemy as sa
from sqlalchemy.exc import NoResultFound
from sqlalchemy import func


from . import models as transaction_models


class TransactionService():
    def __init__(self, db_: sa.orm.Session, user_id=None, data_id=None):
        self.db: sa.orm.Session = db_
        self.data_id = data_id
        self.user_id = user_id
        self.query: sa.orm.Query = self.db.query(
            transaction_models.TransactionDB)

    def total_amount(self):
        # return self.db.execute(sa.func.sum(transaction_models.TransactionDB.amount)).fetchall()[0][0]
        deposit = self.query.filter(transaction_models.TransactionDB.user_id == self.user_id, transaction_models.TransactionDB.type ==
                                    transaction_models.TransactionEnum.deposit).with_entities(func.sum(transaction_models.TransactionDB.amount)).scalar()
        withdraw = self.query.filter(transaction_models.TransactionDB.user_id == self.user_id, transaction_models.TransactionDB.type ==
                                     transaction_models.TransactionEnum.withdraw).with_entities(func.sum(transaction_models.TransactionDB.amount)).scalar()
        deposit = deposit if deposit is not None else 0
        withdraw = withdraw if withdraw is not None else 0
        return deposit - withdraw

    def read_all(self):
        return self.query.all()

    def read_transaction_by_user_id(self,):
        return self.query.filter(transaction_models.TransactionDB.user_id == self.user_id).all()

    def read_by_id(self):
        try:
            data_db = self.query.filter(
                transaction_models.TransactionDB.id == self.data_id).one()
        except NoResultFound as exc:
            raise fa.HTTPException(
                404, detail="Transaction not found") from exc
        return data_db

    def withdraw(self, form_data):
        previous_amount = self.total_amount()
        if (previous_amount-10) < form_data.amount:
            raise fa.HTTPException(
                400, detail="Your minimum deposit saldo must be more or equal to 10 ")
        try:
            data_db = transaction_models.TransactionDB(
                type="withdraw", **form_data.dict())
            self.db.add(data_db)
            self.db.commit()
        except Exception as err:
            raise fa.HTTPException(400, detail=F'error : {err}')
        return data_db, previous_amount

    def deposit(self, form_data):
        previous_amount = self.total_amount()
        try:
            data_db = transaction_models.TransactionDB(
                type="deposit", **form_data.dict())
            self.db.add(data_db)
            self.db.commit()
        except Exception as err:
            raise fa.HTTPException(400, detail=F'error : {err}')
        return data_db, previous_amount
