from .. import db
from sqlalchemy import func


class Guest(db.Model):
    __tablename__ = "guests"

    id = db.Column(db.Integer, primary_key=True)
    
    first_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))

    username = db.Column(db.String(32), index = True)
    email = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(255))
    
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __init__(self, first_name: str, second_name: str, username: str, email: str, password: str) -> None:
        self.first_name = first_name
        self.second_name = second_name
        self.username = username
        self.email = email
        self.password = password

