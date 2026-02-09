from typing import Generic, Optional, TypeVar
from ..interfaces.IGenericRepository import IGenericRepository

T = TypeVar("T")

class GenericRepository(IGenericRepository[T], Generic[T]):

    def __init__(self, session, model) -> None:
        self.session = session
        self.model = model
        self.seen = set()

    def get_by_id(self, id):
        entity = self.session.get(self.model, id)

        if entity:
            self.seen.add(entity)

        return entity

    def list_all(self) -> list[T]:
        return self.session.query(self.model).all() 

    def add(self, entity) -> None:
        self.seen.add(entity)
        return self.session.add(entity)

    def remove(self, entity) -> None:
        return self.session.delete(entity)
