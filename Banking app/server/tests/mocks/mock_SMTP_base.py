from typing import Any


class MockSMTPBase:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

        self.logged_in = False
        self.sent_messages: list[Any] = []
        self.ehlo_called = 0
        self.starttls_called = 0

    def login(self, user: str, password: str) -> None:
        self.logged_in = True
        self.login_user = user
        self.login_password = password

    def send_message(self, msg: Any) -> None:
        self.sent_messages.append(msg)

    def ehlo(self) -> None:
        self.ehlo_called += 1

    def starttls(self, context: Any = None) -> None:
        self.starttls_called += 1
        self.starttls_context = context

    def __enter__(self) -> "MockSMTPBase":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        return None
