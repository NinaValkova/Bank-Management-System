from typing import Any
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt

from ...services import AdminAuthService


class AdminRegister(Resource):

    def post(self) -> tuple[dict[str, Any], int]:
        data = request.get_json() or {}
        return AdminAuthService.register(data)


class AdminLogin(Resource):

    def post(self) -> tuple[dict[str, Any], int]:
        data = request.get_json() or {}
        return AdminAuthService.login(data.get("username"), data.get("password"))


class AdminLogout(Resource):
    @jwt_required()
    def post(self) -> tuple[dict[str, Any], int]:
        jti = get_jwt()["jti"]
        return AdminAuthService.logout(jti)
