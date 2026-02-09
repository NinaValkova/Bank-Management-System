from abc import ABC, abstractmethod
from typing import Optional
from ....models.user import User
from . import IGenericRepository


class IAuthenticationRepository(IGenericRepository[User], ABC):
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[User]:
        pass
