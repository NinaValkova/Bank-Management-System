from typing import Optional, cast
from flask_sqlalchemy.query import Query
from sqlalchemy.sql.elements import ColumnElement

from ..interfaces import ISpecification
from ....models.transaction import Transaction


class TransactionSpecification(ISpecification):

    def __init__(
        self, account_id: int, operation: Optional[str] = None, sort: str = "desc"
    ) -> None:
        self.account_id = account_id
        self.operation = operation
        self.sort = (sort or "desc").lower()

    def apply(self, query: Query) -> Query:
        query = query.filter(
            cast(ColumnElement[bool], Transaction.account_id == self.account_id)
        )

        if self.operation is not None:
            query = query.filter(
                cast(ColumnElement[bool], Transaction.operation == self.operation)
            )

        if self.sort == "asc":
            return self.order_by_ascending(query)

        return self.order_by_descending(query)

    def order_by_descending(self, query: Query) -> Query:
        return query.order_by(Transaction.date.desc(), Transaction.id.desc())

    def order_by_ascending(self, query: Query) -> Query:
        return query.order_by(Transaction.date.asc(), Transaction.id.asc())
