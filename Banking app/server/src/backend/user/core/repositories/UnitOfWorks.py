from __future__ import annotations

from ..interfaces.IUnitOfWorks import IUnitOfWorks
from .AuthenticationRepository import AuthenticationRepository
from .TransactionRepository import TransactionRepository
from ...services.messagebus import MessageBus
from .AccountRepository import AccountRepository


class UnitOfWork(IUnitOfWorks):

    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    def __enter__(self) -> UnitOfWork:
        self.session = self.session_factory()

        self.authentication = AuthenticationRepository(self.session)
        self.transaction = TransactionRepository(self.session)
        self.account = AccountRepository(self.session)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            self.session.rollback()
        else:
            self.commit()

        self.session.close()

    def commit(self) -> None:
        self.session.commit()
        self._publish_events()

    def flush(self) -> None:
        self.session.flush()

    def rollback(self) -> None:
        self.session.rollback()

    def _publish_events(self) -> None:
        for r in (self.authentication, self.transaction, self.account):
            for entity in getattr(r, "seen", []):
                if hasattr(entity, "events"):
                    while entity.events:
                        event = entity.events.pop(0)
                        MessageBus.handle(event, self)
