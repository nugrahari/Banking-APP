
import fastapi as fa
from passlib.hash import sha256_crypt


import sqlalchemy as sa
from sqlalchemy.exc import NoResultFound

from apps.users import models as user_models


class AuthService():
    def __init__(self, db_: sa.orm.Session, data_id=None) -> None:
        self.db: sa.orm.Session = db_
        self.data_id = data_id
        self.query: sa.orm.Query = self.db.query(user_models.UserDB)

    def read_one_by_id(self, data_id):
        try:
            data_db = self.query.filter(user_models.UserDB.id == data_id).one()
        except NoResultFound as exc:
            raise fa.HTTPException(
                fa.status.HTTP_404_NOT_FOUND, detail='user not found') from exc
        return data_db

    def read_by_phone(self, phone_number):
        try:
            return self.query.filter(user_models.UserDB.phone_number == phone_number).one()
        except NoResultFound as exc:
            raise fa.HTTPException(
                fa.status.HTTP_404_NOT_FOUND, detail='user not found') from exc

    def login(self, form_data):
        data_db = self.read_by_phone(form_data.phone_number)

        if sha256_crypt.verify(form_data.password, data_db.password):
            return {'sub': 'auth', 'user': {'id': data_db.id, 'role': data_db.role}}, data_db
        else:
            raise fa.HTTPException(401, detail='invalid username or password')
