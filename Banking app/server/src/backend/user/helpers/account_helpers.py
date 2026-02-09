from decimal import Decimal
from typing import Optional
from ...models.account import Account
from ...models.disposition import Disposition
from ...models.transaction import Transaction


def get_user_account(user_id):
    return (
        Account.query.join(Disposition).filter(Disposition.user_id == user_id).first()
    )


def get_overview(user):
    account = get_user_account(user.id)

    if not account:
        return {"message": "No account linked to user"}, 404

    transactions = (
        Transaction.query.filter(
            (Transaction.from_account == account.account_number)
            | (Transaction.to_account == account.account_number)
        )
        .order_by(Transaction.id.desc())
        .all()
    )

    return {
        "account_details": {
            "username": user.username,
            "accountNumber": account.account_number,
            "balance": float(account.balance),
        },
        "transactions": transactions,
    }


def get_balance_value(user_id: int) -> Optional[Decimal]:
    disposition = Disposition.query.filter_by(user_id=user_id).first()

    if not disposition:
        return None

    return disposition.account.balance
