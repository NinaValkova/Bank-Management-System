from flask_restful import Resource
from flask import request
from ...services import UserAuthService
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from .... import db


class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        return UserAuthService.register(db.session, data)


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        return UserAuthService.login(data["username"], data["password"])


class FetchUser(Resource):
    @jwt_required()
    def get(self):
        users = UserAuthService()

        user_id = int(get_jwt_identity())
        response = users.get_user_info(user_id)
        return response


class FetchBalance(Resource):
    @jwt_required()
    def get(self):
        users = UserAuthService()

        user_id = int(get_jwt_identity())
        response = users.get_user_balance(user_id)
        return response


class ManageUser(Resource):
    @jwt_required()
    def put(self, **kwargs):
        data = request.get_json()
        if not data:
            return {"statuse": 2, "message": "Invalid request"}, 400

        user = UserAuthService()
        user_id = int(get_jwt_identity())
        response = user.update_user(db.session, user_id, data)
        return response


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        return UserAuthService.logout(jti)
