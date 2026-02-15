from .guest import Guest
from .. import db
from sqlalchemy import func


class Admin(Guest):
    __tablename__ = "admins"

    id = db.Column(db.Integer, db.ForeignKey("guests.id"), primary_key=True)

    def __init__(
        self,
        first_name: str,
        second_name: str,
        username: str,
        email: str,
        password: str,
    ) -> None:
        super().__init__(first_name, second_name, username, email, password)

    def __repr__(self) -> str:  
        return f"<Admin id={self.id}>" 
