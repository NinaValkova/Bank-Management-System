from .guest import Guest
from .. import db
from sqlalchemy import DateTime, func


class User(Guest):
    __tablename__ = "users"

    id = db.Column(db.Integer, db.ForeignKey("guests.id"), primary_key=True)

    birth_number = db.Column(db.String(20), nullable=True, index=True)

    def __init__(self, first_name: str, second_name: str, username: str, email: str, password: str, birth_number: str) -> None:
        super().__init__(first_name, second_name, username, email, password)
        self.birth_number = birth_number

    def __repr__(self) -> str:
        return f"<User id={self.id}>"
