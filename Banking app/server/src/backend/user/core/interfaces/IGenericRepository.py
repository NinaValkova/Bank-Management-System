from abc import ABC, abstractmethod
from typing import Generic, Iterable, Optional, TypeVar

T = TypeVar("T")


class IGenericRepository(ABC, Generic[T]):
    @abstractmethod
    def get_by_id(self, id) -> Optional[T]:
        pass

    @abstractmethod
    def list_all(self) -> Iterable[T]:
        pass

    @abstractmethod
    def add(self, entity) -> None:
        pass

    @abstractmethod
    def remove(self) -> None:
        pass
