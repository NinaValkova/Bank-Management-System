from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from flask_sqlalchemy.query import Query

T = TypeVar("T")


class ISpecification(ABC, Generic[T]):
    @abstractmethod
    def apply(self, query: Query):
        pass
