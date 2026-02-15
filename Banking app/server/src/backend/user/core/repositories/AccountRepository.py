from typing import Optional

from ..interfaces import IAccountRepository
from ....models.account import Account
from .GenericRepository import GenericRepository


class AccountRepository(GenericRepository[Account], IAccountRepository):

    def __init__(self, session) -> None:
        super().__init__(session, Account)

    def get_by_number(self, number: str) -> Optional[Account]:
        acc = self.session.query(Account).filter_by(account_number=number).first()
        if acc:
            self.seen.add(acc)
        return acc
