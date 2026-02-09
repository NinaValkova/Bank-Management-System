from .. import db

class Disposition(db.Model):
    __tablename__ = "dispositions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False, index=True)

    type = db.Column(db.String(20), nullable=False)  

    user = db.relationship("User", backref="dispositions")
    account = db.relationship("Account", backref="dispositions")

    def __init__(self, user_id: int, account_id: int, type: str) -> None:
        self.user_id = user_id
        self.account_id = account_id
        self.type = type

    def __repr__(self) -> str:
        return f"<Disposition id={self.id}>"
