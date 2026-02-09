# backend/admin/api/routes.py
from flask import Blueprint
from flask_restful import Api

from .resources import AdminRegister, AdminLogin, AdminLogout
from .resources import AdminUsers
from .resources import AdminAccounts
from .resources import AdminTransactions

admin_bp = Blueprint("admin", __name__)
api = Api(admin_bp)

api.add_resource(AdminRegister, "/register")
api.add_resource(AdminLogin, "/login")
api.add_resource(AdminLogout, "/logout")

api.add_resource(AdminUsers, "/users")
api.add_resource(AdminAccounts, "/accounts")
api.add_resource(AdminTransactions, "/transactions")
