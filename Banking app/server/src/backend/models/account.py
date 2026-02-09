from decimal import Decimal
from .. import db
from sqlalchemy import DateTime, func
from sqlalchemy.orm import reconstructor

class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True) 

    account_number = db.Column(db.String(64), unique=True, index=True, nullable=True)
    balance = db.Column(db.Numeric(12, 2), nullable=False, default=0)

    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    def __init__(self, account_number: str, balance: Decimal) -> None:
        self.account_number = account_number
        self.balance = balance
        self.events = []

    @reconstructor
    def init_on_load(self) -> None:
        # called when SQLAlchemy loads object from DB
        self.events = []

    def __repr__(self) -> str:
        return f"<Account id={self.id}>"
