from abc import ABC, abstractmethod
from typing import Optional
from ....models.account import Account
from . import IGenericRepository


class IAccountRepository(IGenericRepository[Account], ABC):
    @abstractmethod
    def get_by_number(self, number: str) -> Optional[Account]:
        pass