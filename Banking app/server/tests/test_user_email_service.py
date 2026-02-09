from __future__ import annotations

from typing import Any, Dict, Callable

import pytest
from flask import Flask

import src.backend.user.services.email_service as svc

from .mocks.mock_SMTP import MockSMTP
from .mocks.mock_SMTP_SSL import MockSMTP_SSL

@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    app.config.update(
        SMTP_HOST="smtp.test.com",
        SMTP_PORT=587,
        SMTP_USER="noreply@test.com",
        SMTP_PASSWORD="secret",
        SUPPORT_EMAIL="support@test.com",
    )
    return app


def patch_smtp(monkeypatch: pytest.MonkeyPatch, *, ssl: bool) -> Dict[str, Any]:
    captured: Dict[str, Any] = {}

    def smtp_factory(*args: Any, **kwargs: Any) -> MockSMTP:
        captured["smtp"] = MockSMTP(*args, **kwargs)
        return captured["smtp"]

    def smtp_ssl_factory(*args: Any, **kwargs: Any) -> MockSMTP_SSL:
        captured["smtp_ssl"] = MockSMTP_SSL(*args, **kwargs)
        return captured["smtp_ssl"]

    if ssl:
        monkeypatch.setattr(svc.smtplib, "SMTP_SSL", smtp_ssl_factory)
    else:
        monkeypatch.setattr(svc.smtplib, "SMTP", smtp_factory)

    return captured


def patch_ssl_context(monkeypatch: pytest.MonkeyPatch) -> Dict[str, Any]:
    captured: Dict[str, Any] = {}

    def fake_create_default_context() -> object:
        ctx = object()
        captured["context"] = ctx
        return ctx

    monkeypatch.setattr(svc.ssl, "create_default_context", fake_create_default_context)
    return captured


def run_in_app_ctx(app: Flask, fn: Callable[[], None]) -> None:
    with app.app_context():
        fn()


def test_send_email_tls_success(monkeypatch: pytest.MonkeyPatch, app: Flask) -> None:
    captured_smtp = patch_smtp(monkeypatch, ssl=False)
    captured_ssl = patch_ssl_context(monkeypatch)

    run_in_app_ctx(
        app,
        lambda: svc.EmailService.send_email(
            user_email="user@test.com",
            subject="Hello",
            text="Test message",
        ),
    )

    smtp: MockSMTP = captured_smtp["smtp"]
    assert smtp.logged_in is True
    assert smtp.ehlo_called == 2
    assert smtp.starttls_called == 1
    assert getattr(smtp, "starttls_context", None) == captured_ssl["context"]
    assert len(smtp.sent_messages) == 1

    msg = smtp.sent_messages[0]
    assert msg["To"] == "user@test.com"
    assert msg["Subject"] == "Hello"
    assert "Bank App <noreply@test.com>" in msg["From"]


def test_send_email_ssl_success(monkeypatch: pytest.MonkeyPatch, app: Flask) -> None:
    app.config["SMTP_PORT"] = 465
    captured_smtp = patch_smtp(monkeypatch, ssl=True)
    patch_ssl_context(monkeypatch)  

    run_in_app_ctx(
        app,
        lambda: svc.EmailService.send_email(
            user_email="user@test.com",
            subject="Secure",
            text="SSL message",
        ),
    )

    smtp: MockSMTP_SSL = captured_smtp["smtp_ssl"]
    assert smtp.logged_in is True
    assert len(smtp.sent_messages) == 1

    msg = smtp.sent_messages[0]
    assert msg["To"] == "user@test.com"
    assert msg["Subject"] == "Secure"


def test_send_email_missing_config_raises(app: Flask) -> None:
    app.config.pop("SMTP_USER")

    with app.app_context():
        with pytest.raises(RuntimeError) as exc:
            svc.EmailService.send_email(
                user_email="user@test.com",
                subject="Fail",
                text="Should fail",
            )

    assert "Missing SMTP configuration" in str(exc.value)
    assert "SMTP_USER" in str(exc.value)


def test_send_to_support_tls_success(
    monkeypatch: pytest.MonkeyPatch, app: Flask
) -> None:
    captured_smtp = patch_smtp(monkeypatch, ssl=False)
    patch_ssl_context(monkeypatch)

    run_in_app_ctx(
        app,
        lambda: svc.EmailService.send_to_support(
            user_email="user@test.com",
            subject="Help",
            text="Need support",
        ),
    )

    smtp: MockSMTP = captured_smtp["smtp"]
    assert smtp.logged_in is True
    assert len(smtp.sent_messages) == 1

    msg = smtp.sent_messages[0]
    assert msg["To"] == "support@test.com"
    assert msg["Subject"] == "Help"


def test_send_to_support_ssl_success(
    monkeypatch: pytest.MonkeyPatch, app: Flask
) -> None:
    app.config["SMTP_PORT"] = 465
    captured_smtp = patch_smtp(monkeypatch, ssl=True)
    patch_ssl_context(monkeypatch)

    run_in_app_ctx(
        app,
        lambda: svc.EmailService.send_to_support(
            user_email="user@test.com",
            subject="Secure Help",
            text="SSL support",
        ),
    )

    smtp: MockSMTP_SSL = captured_smtp["smtp_ssl"]
    assert smtp.logged_in is True
    assert len(smtp.sent_messages) == 1

    msg = smtp.sent_messages[0]
    assert msg["To"] == "support@test.com"
    assert msg["Subject"] == "Secure Help"


def test_send_to_support_missing_support_email_raises(app: Flask) -> None:
    app.config["SUPPORT_EMAIL"] = "   "

    with app.app_context():
        with pytest.raises(RuntimeError) as exc:
            svc.EmailService.send_to_support(
                user_email="user@test.com",
                subject="Fail",
                text="Missing support email",
            )

    assert "Missing SMTP configuration" in str(exc.value)
    assert "SUPPORT_EMAIL" in str(exc.value)
