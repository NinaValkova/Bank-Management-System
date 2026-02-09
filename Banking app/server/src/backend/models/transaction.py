from decimal import Decimal
from .. import db
from sqlalchemy import DateTime, func
from typing import Optional


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    account = db.relationship("Account", backref="transactions")

    from_account = db.Column(db.String(18), nullable=False)
    to_account = db.Column(db.String(18), nullable=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    balance = db.Column(db.Numeric(12, 2))
    currency = db.Column(db.String(3))

    date = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    type = db.Column(db.String(20), nullable=True)
    operation = db.Column(db.String(50), nullable=True)  

    def __init__(self, account_id: int, from_account: str,to_account: Optional[str], amount: Decimal, balance: Decimal, currency:str, type:str, operation:str)-> None:
        self.account_id = account_id
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount
        self.balance = balance
        self.currency = currency
        self.type = type
        self.operation = operation

    def __repr__(self) -> str:
        return f"<Transaction id={self.id}>"
