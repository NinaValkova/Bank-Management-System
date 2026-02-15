from __future__ import annotations

from typing import Callable, ClassVar, Dict, List, Type, TypeVar

from ..core.interfaces import IUnitOfWorks
from ..core.domain.events import Event

E = TypeVar("E", bound=Event)
Handler = Callable[[E, IUnitOfWorks], None]


class MessageBus:
    _bootstrapped: ClassVar[bool] = False
    _handlers: ClassVar[Dict[Type[Event], List[Handler]]] = {}

    @classmethod
    def _ensure_bootstrapped(cls) -> None:
        if cls._bootstrapped:
            return
        from ..helpers.bootstrap import bootstrap

        bootstrap()
        cls._bootstrapped = True

    @classmethod
    def register(cls, event_type: Type[E], handler: Handler[E]) -> None:
        cls._handlers.setdefault(event_type, []).append(handler)

    @classmethod
    def handle(cls, event: Event, uow: IUnitOfWorks) -> None:
        cls._ensure_bootstrapped()
        for handler in cls._handlers.get(type(event), []):
            handler(event, uow)
