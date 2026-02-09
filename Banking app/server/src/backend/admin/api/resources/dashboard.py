# backend/admin/api/resources/users.py
from typing import Any
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from ...services import AdminDashboardService
from ...helpers import admin_required


class AdminUsers(Resource):
    @admin_required
    def get(self) -> tuple[list[dict[str, Any]], int]:
        return AdminDashboardService.list_users()


class AdminAccounts(Resource):
    @admin_required
    def get(self) -> tuple[list[dict[str, Any]], int]:
        return AdminDashboardService.list_accounts()


class AdminTransactions(Resource):
    @admin_required
    def get(self) -> tuple[list[dict[str, Any]], int]:
        return AdminDashboardService.list_transactions()
