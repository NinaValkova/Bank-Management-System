import json
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.backend import app, db
from src.backend.models.account import Account


def seed_from_json(json_path: str) -> None:
    path = Path(json_path)

    if not path.exists():
        raise FileNotFoundError(f"Seed file not found: {path.resolve()}")

    data = json.loads(path.read_text(encoding="utf-8"))

    with app.app_context():

        for item in data:
            account_number = item.get("account_number")
            balance = item.get("balance", "0.00")

            if not account_number:
                continue

            exists = Account.query.filter_by(account_number=account_number).first()
            if exists:
                continue

            account = Account(
                account_number=account_number,
                balance=Decimal(str(balance)),
            )

            db.session.add(account)

        db.session.commit()


if __name__ == "__main__":
    seed_from_json("data/accounts.json")
