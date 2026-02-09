from typing import Optional
from . import GenericRepository
from ....models.user import User
from ..interfaces.IAuthenticationRepository import IAuthenticationRepository
from .GenericRepository import GenericRepository

class AuthenticationRepository(GenericRepository[User], IAuthenticationRepository):

    def __init__(self, session) -> None:
        super().__init__(session, User)

    def get_by_name(self, name) -> Optional[User]:
        return self.session.query(User).filter_by(username=name).first()
