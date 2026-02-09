from decimal import Decimal
from ... import db
from ...models.user import User
from ...models.account import Account
from ...models.disposition import Disposition
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from ..helpers import get_balance_value
from ..core.repositories.UnitOfWorks import UnitOfWork


def get_free_account():
    return Account.query.outerjoin(Disposition).filter(Disposition.id == None).first()


class UserAuthService:

    @staticmethod
    def register(session_factory, data):
        with UnitOfWork(session_factory) as uow:
            if User.query.filter(
                (User.email == data["email"]) | (User.username == data["username"])
            ).first():
                return {"message": "User already exists"}, 409

            user = User(
                first_name=data["first_name"],
                second_name=data["second_name"],
                username=data["username"],
                email=data["email"],
                password=generate_password_hash(data["password"]),
                birth_number=data.get("birth_date"),
            )

            uow.authentication.add(user)
            uow.flush()

            account = get_free_account()
            if not account:
                return {"message": "No available accounts"}, 400

            disposition = Disposition(
                user_id=user.id, account_id=account.id, type="OWNER"
            )

            uow.authentication.add(disposition)
            uow.commit()

            return {
                "message": "User registered",
                "account_number": account.account_number,
            }, 201

    @staticmethod
    def login(username, password):
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            return {"message": "Invalid credentials"}, 401

        token = create_access_token(
            identity=str(user.id), expires_delta=timedelta(minutes=300)
        )

        return {"access_token": token}, 200

    @staticmethod
    def get_user_balance(user_id: int):

        balance = get_balance_value(user_id)

        if balance is None:
            return {"message": "Account not found"}, 404

        return {"balance": str(balance)}, 200

    @staticmethod
    def get_user_info(user_id: int):
        user = User.query.get(user_id)

        if not user:
            return {"message": "User not found"}, 404

        balance = get_balance_value(user_id)

        if balance is None:
            return {"message": "Account not found"}, 404

        return {
            "first_name": user.first_name,
            "second_name": user.second_name,
            "email": user.email,
            "birth_number": user.birth_number,
            "balance": str(balance),
        }, 200

    @staticmethod
    def update_user(session_factory, user_id, data):
        with UnitOfWork(session_factory) as uow:
            user = User.query.get(user_id)

            if not user:
                return {"message": "User not found"}, 404

            allowed_fields = {
                "first_name",
                "second_name",
                "email",
                "birth_number",
            }

            for key, value in data.items():
                if key in allowed_fields:
                    setattr(user, key, value)

            try:
                uow.commit()
                return {"message": "User updated successfully"}, 200
            except Exception as e:
                uow.rollback()
                print(e)
                return {"message": "Update failed"}, 500
