from typing import Any
from ...models.user import User
from ...models.account import Account
from ...models.transaction import Transaction


class AdminDashboardService:

    @staticmethod
    def list_users() -> tuple[list[dict[str, Any]], int]:
        users = User.query.order_by(User.id.desc()).all()
        return [
            {
                "id": u.id,
                "first_name": u.first_name,
                "second_name": u.second_name,
                "username": u.username,
                "email": u.email,
                "birth_number": u.birth_number,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in users
        ], 200

    @staticmethod
    def list_accounts() -> tuple[list[dict[str, Any]], int]:
        accounts = Account.query.order_by(Account.id.desc()).all()
        return [
            {
                "id": a.id,
                "account_number": a.account_number,
                "balance": float(a.balance),
                "created_at": a.created_at.isoformat() if a.created_at else None,
            }
            for a in accounts
        ], 200

    @staticmethod
    def list_transactions() -> tuple[list[dict[str, Any]], int]:
        txs = Transaction.query.order_by(Transaction.id.desc()).all()
        return [
            {
                "id": t.id,
                "account_id": t.account_id,
                "from_account": t.from_account,
                "to_account": t.to_account,
                "amount": float(t.amount),
                "balance": float(t.balance) if t.balance is not None else None,
                "currency": t.currency,
                "type": t.type,
                "operation": t.operation,
                "date": t.date.isoformat() if t.date else None,
            }
            for t in txs
        ], 200
