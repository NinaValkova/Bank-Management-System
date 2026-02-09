from flask import session
from ..interfaces.ITransactionRepository import ITransactionRepository
from ....models.transaction import Transaction
from .GenericRepository import GenericRepository

class TransactionRepository(GenericRepository[Transaction], ITransactionRepository):

    def __init__(self, session) -> None:
        super().__init__(session, Transaction)
