import enum

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as sql_UUID

from libs import db


class RoleEnum(enum.Enum):
    administrator: str = 'administrator'
    user: str = 'user'


class UserDB(db.Base):
    __tablename__ = 'users'
    id = sa.Column(sql_UUID(as_uuid=True), primary_key=True,
                   server_default=sa.text("gen_random_uuid()"))
    name = sa.Column(sa.String(25), nullable=False)
    account_number = sa.Column(sa.String(50), nullable=False)
    phone_number = sa.Column(sa.String(20), nullable=False, unique=True)
    email_address = sa.Column(sa.String, nullable=False, unique=True)
    tax_id = sa.Column(sa.String(6), nullable=False, unique=True)
    address = sa.Column(sa.String, nullable=False)
    role = sa.Column(sa.Enum(RoleEnum), server_default="user")
    password = sa.Column(sa.String(255), nullable=False)

    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    updated_at = sa.Column(
        sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
