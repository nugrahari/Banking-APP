import enum

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as sql_UUID

from libs import db


class TransactionEnum(enum.Enum):
    deposit: str = 'deposit'
    withdraw: str = 'withdraw'


class TransactionDB(db.Base):
    __tablename__ = 'transactions'
    id = sa.Column(sql_UUID(as_uuid=True), primary_key=True,
                   server_default=sa.text("gen_random_uuid()"))
    user_id = sa.Column(sql_UUID(as_uuid=True), sa.ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    type = sa.Column(sa.Enum(TransactionEnum), nullable=False)
    amount = sa.Column(sa.Numeric(precision=20, scale=2,
                       asdecimal=True), nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    updated_at = sa.Column(
        sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
