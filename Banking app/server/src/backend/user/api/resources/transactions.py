from typing import Any
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...services import TransactionService
from ...helpers import get_user_account
from .... import db

class SendMoney(Resource):
    @jwt_required()
    def post(self) -> tuple[dict[str, Any], int]:
        data = request.get_json()

        user_id = int(get_jwt_identity())
        sender_account = get_user_account(user_id)

        if not sender_account:
            return {"message": "Account not found"}, 404

        to_account = data.get("to_account")
        amount = data.get("amount")
        currency = data.get("currency", "EUR")

        if not to_account or not amount:
            return {"message": "to_account and amount are required"}, 400

        return TransactionService.send_money(
            db.session,
            sender_account=sender_account,
            to_account_number=to_account,
            amount=amount,
            currency=currency,
        )


class CashDeposit(Resource):
    @jwt_required()
    def post(self) -> tuple[dict[str, Any], int]:
        data = request.get_json()

        user_id = int(get_jwt_identity())
        account = get_user_account(user_id)

        if not account:
            return {"message": "Account not found"}, 404

        return TransactionService.cash_deposit(
            db.session,
            account,
            data.get("amount"),
        )


class CashWithdraw(Resource):
    @jwt_required()
    def post(self) -> tuple[dict[str, Any], int]:
        data = request.get_json()

        user_id = int(get_jwt_identity())
        account = get_user_account(user_id)

        if not account:
            return {"message": "Account not found"}, 404

        return TransactionService.cash_withdraw(
            db.session,
            account,
            data.get("amount"),
        )


class UserTransactions(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())

        operation = request.args.get("operation")
        sort = request.args.get("sort", "desc")

        return TransactionService.list_user_transactions(
            user_id=user_id, operation=operation, sort=sort
        )
