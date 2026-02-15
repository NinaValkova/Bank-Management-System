from __future__ import annotations

from abc import ABC, abstractmethod

from .IAccountRepository import IAccountRepository
from .ITransactionRepository import ITransactionRepository
from .IAuthenticationRepository import IAuthenticationRepository


class IUnitOfWorks(ABC):
    authentication: IAuthenticationRepository
    transaction: ITransactionRepository
    account: IAccountRepository

    @abstractmethod
    def __enter__(self) -> IUnitOfWorks:
        return self

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def flush(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass 
