from abc import ABC, abstractmethod
from typing import TypeVar
from . import ISpecification


T = TypeVar("T")


class IOrderSpecification(ISpecification[T]):
    @abstractmethod
    def order_by_ascending(self, query) -> T:
        pass

    @abstractmethod
    def order_by_descending(self, query) -> T:
        pass
