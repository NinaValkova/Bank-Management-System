from abc import ABC, abstractmethod
from ....models.transaction import Transaction
from . import IGenericRepository


class ITransactionRepository(IGenericRepository[Transaction], ABC):
    pass
