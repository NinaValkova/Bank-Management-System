from typing import Any
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from ...services import EmailService
from ....models.user import User


class HelpSupport(Resource):
    @jwt_required()
    def post(self) -> tuple[dict[str, Any], int]:
        data = request.get_json(silent=True) or {}
        message = (data.get("message") or "").strip()
        if not message:
            return {"message": "Message is required"}, 400

        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        try:
            EmailService.send_to_support(
                user_email=user.email,
                subject="Banking App - Support Request",
                text=message,
            )
        except Exception as e:
            return {"message": f"Failed to send email: {str(e)}"}, 500

        return {"message": "Support request sent successfully"}, 200
