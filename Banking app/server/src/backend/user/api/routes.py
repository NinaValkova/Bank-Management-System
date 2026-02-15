from flask import Blueprint
from flask_restful import Api
from .resources import UserRegister, UserLogin, FetchUser, FetchBalance, ManageUser, UserLogout
from .resources import SendMoney, CashDeposit, CashWithdraw, UserTransactions
from .resources import HelpSupport

user_bp = Blueprint("user", __name__)
api = Api(user_bp)

api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(SendMoney, "/transfer")
api.add_resource(FetchUser, "/user-info")
api.add_resource(FetchBalance, "/user-balance")
api.add_resource(ManageUser, '/update-user')
api.add_resource(CashDeposit, "/cash-deposit")
api.add_resource(CashWithdraw, "/cash-withdraw")
api.add_resource(UserTransactions, "/transactions")
api.add_resource(HelpSupport, "/help-support")
api.add_resource(UserLogout, "/logout")
