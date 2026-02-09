# backend/admin/services/auth_service.py
from typing import Any
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta, timezone, datetime

from ... import db
from ...models.admin import Admin
from ...models.token_blocklist import TokenBlocklist


class AdminAuthService:

    @staticmethod
    def register(data) -> tuple[dict[str, Any], int]:
        exists = Admin.query.filter(
            (Admin.email == data["email"]) | (Admin.username == data["username"])
        ).first()

        if exists:
            return {"message": "Admin already exists"}, 409

        admin = Admin(
            first_name=data.get("first_name"),
            second_name=data.get("second_name"),
            username=data["username"],
            email=data["email"],
            password=generate_password_hash(data["password"]),
        )

        db.session.add(admin)
        db.session.commit()

        return {"message": "Admin registered"}, 201

    @staticmethod
    def login(username, password) -> tuple[dict[str, Any], int]:
        admin = Admin.query.filter_by(username=username).first()
        if not admin or not check_password_hash(admin.password, password):
            return {"message": "Invalid credentials"}, 401

        token = create_access_token(
            identity=str(admin.id),
            additional_claims={"role": "admin"},
            expires_delta=timedelta(minutes=10),
        )
        return {"access_token": token}, 200

    @staticmethod
    def logout(jti) -> tuple[dict[str, Any], int]:

        now = datetime.now(timezone.utc)

        token = TokenBlocklist(jti=jti, created_at=now)

        db.session.add(token)
        db.session.commit()

        return {"message": "Logged out"}, 200
