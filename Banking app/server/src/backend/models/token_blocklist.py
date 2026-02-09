from datetime import date, datetime
from .. import db
from sqlalchemy import DateTime


class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.Integer, primary_key=True)

    jti = db.Column(db.String(255), nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, jti: str, created_at: datetime) -> None:
        self.jti = jti
        self.created_at = created_at

    def __repr__(self) -> str:
        return f"<TokenBlocklist jti={self.jti}>"
