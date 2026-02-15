from decimal import Decimal
from datetime import datetime
from typing import Any

from ..core.repositories.UnitOfWorks import UnitOfWork
from ... import db
from ...models.account import Account
from ...models.transaction import Transaction
from ..helpers import get_user_account
from ..core.specifications import TransactionSpecification
from ..core.repositories.UnitOfWorks import UnitOfWork
from ..core.domain.events import MoneySend, CashWithdrawn, CashDeposit


class TransactionService:

    @staticmethod
    def send_money(
        session_factory, sender_account, to_account_number, amount, currency="EUR"
    ) -> tuple[dict[str, Any], int]:
        with UnitOfWork(session_factory) as uow:
            sender = uow.account.get_by_id(sender_account.id)
            receiver = uow.account.get_by_number(to_account_number)

            if not sender:
                return {"message": "Sender acco unt not found"}, 404

            if not receiver:
                return {"message": "Receiver not found"}, 404

            amount = Decimal(amount)

            if amount <= 0:
                return {"message": "Invalid amount"}, 400

            if sender.balance < amount:
                return {"message": "Insufficient funds"}, 400

            sender.balance -= amount
            receiver.balance += amount

            sender.events.append(
                MoneySend(
                    from_account=sender.account_number,
                    to_account=receiver.account_number,
                    amount=amount,
                    currency=currency,
                )
            )

            tx = Transaction(
                account_id=sender.id,
                from_account=sender.account_number,
                to_account=receiver.account_number,
                amount=amount,
                balance=sender.balance,
                currency=currency,
                type="DEBIT",
                operation="TRANSFER",
            )

            uow.transaction.add(tx)

        return {"message": "Transfer successful"}, 200

    @staticmethod
    def cash_withdraw(session_factory, account, amount) -> tuple[dict[str, Any], int]:
        with UnitOfWork(session_factory) as uow:
            acc = uow.account.get_by_id(account.id)
            amount = Decimal(amount)

            if not acc:
                return {"message": "Sender account not found"}, 404

            if amount <= 0:
                return {"message": "Invalid amount"}, 400

            if acc.balance < amount:
                return {"message": "Insufficient funds"}, 400

            balance = acc.balance - amount

            Account.query.filter_by(id=acc.id).update({"balance": balance})

            acc.events.append(
                CashWithdrawn(
                    account_number=acc.account_number,
                    amount=amount,
                )
            )

            tx = Transaction(
                account_id=acc.id,
                from_account=acc.account_number,
                to_account=None,
                amount=amount,
                balance=balance,
                currency="EUR",
                type="DEBIT",
                operation="CASH_WITHDRAW",
            )

            uow.transaction.add(tx)

        return {
            "message": "Cash withdrawn successfully",
            "balance": str(balance),
        }, 200

    @staticmethod
    def cash_deposit(session_factory, account, amount) -> tuple[dict[str, Any], int]:
        with UnitOfWork(session_factory) as uow:
            acc = uow.account.get_by_id(account.id)
            amount = Decimal(amount)

            if not acc:
                return {"message": "Sender account not found"}, 404

            if amount <= 0:
                return {"message": "Invalid amount"}, 400

            balance = acc.balance + amount

            Account.query.filter_by(id=acc.id).update({"balance": balance})

            acc.events.append(
                CashDeposit(
                    account_number=acc.account_number,
                    amount=amount,
                )
            )

            tx = Transaction(
                account_id=acc.id,
                from_account=acc.account_number,
                to_account=None,
                amount=amount,
                balance=balance,
                currency="EUR",
                type="CREDIT",
                operation="CASH_DEPOSIT",
            )

            uow.transaction.add(tx)

        return {
            "message": "Cash deposited successfully",
            "balance": str(balance),
        }, 200

    @staticmethod
    def list_user_transactions(
        user_id: int, operation=None, sort: str = "desc"
    ) -> tuple[list[dict[str, Any]], int] | tuple[dict[str, Any], int]:

        account = get_user_account(user_id)
        if not account:
            return {"message": "Account not found"}, 404

        spec = TransactionSpecification(
            account_id=account.id, operation=operation, sort=sort
        )
        txs = spec.apply(Transaction.query).all()

        return [
            {
                "id": t.id,
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
