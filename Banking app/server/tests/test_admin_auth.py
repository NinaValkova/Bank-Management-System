from __future__ import annotations

from flask import Flask
import pytest

import src.backend.admin.api.resources.auth as res


@pytest.fixture
def app() -> Flask:
    return Flask(__name__)

@pytest.fixture
def fake_admin_auth_service(monkeypatch):
    captured: dict = {}

    class FakeAdminAuthService:
        register_result = ({"message": "ok"}, 201)
        login_result = ({"access_token": "TOKEN"}, 200)
        logout_result = ({"message": "Logged out"}, 200)

        @staticmethod
        def register(data):
            captured["data"] = data
            return FakeAdminAuthService.register_result

        @staticmethod
        def login(username, password):
            captured["username"] = username
            captured["password"] = password
            return FakeAdminAuthService.login_result

        @staticmethod
        def logout(jti):
            captured["jti"] = jti
            return FakeAdminAuthService.logout_result

    monkeypatch.setattr(res, "AdminAuthService", FakeAdminAuthService, raising=False)
    return FakeAdminAuthService, captured


def test_admin_register_success(app, fake_admin_auth_service) -> None:
    Fake, captured = fake_admin_auth_service
    Fake.register_result = ({"message": "Admin registered"}, 201)

    payload = {
        "first_name": "Nina",
        "second_name": "Valkova",
        "username": "nina",
        "email": "nina@test.com",
        "password": "secret",
    }

    with app.test_request_context(
        path="/api/admin/register", method="POST", json=payload
    ):
        resource = res.AdminRegister()
        body, status = resource.post()

    assert status == 201
    assert body == {"message": "Admin registered"}
    assert captured["data"] == payload


def test_admin_login_success(app, fake_admin_auth_service) -> None:
    Fake, captured = fake_admin_auth_service
    Fake.login_result = ({"access_token": "TOKEN"}, 200)

    with app.test_request_context(
        path="/api/admin/login",
        method="POST",
        json={"username": "admin", "password": "pass"},
    ):
        resource = res.AdminLogin()
        body, status = resource.post()

    assert status == 200
    assert body == {"access_token": "TOKEN"}
    assert captured["username"] == "admin"
    assert captured["password"] == "pass"


def test_admin_login_fail(app, fake_admin_auth_service) -> None:
    Fake, captured = fake_admin_auth_service
    Fake.login_result = ({"message": "Invalid credentials"}, 401)

    with app.test_request_context(
        path="/api/admin/login",
        method="POST",
        json={},
    ):
        resource = res.AdminLogin()
        body, status = resource.post()

    assert status == 401
    assert body == {"message": "Invalid credentials"}
    assert captured["username"] is None
    assert captured["password"] is None


def test_admin_logout_success(monkeypatch, app, fake_admin_auth_service) -> None:
    Fake, captured = fake_admin_auth_service
    Fake.logout_result = ({"message": "Logged out"}, 200)

    monkeypatch.setattr(res, "get_jwt", lambda: {"jti": "JTI-123"}, raising=False)

    with app.test_request_context(path="/api/admin/logout", method="POST"):
        resource = res.AdminLogout()

        post_fn = getattr(res.AdminLogout.post, "__wrapped__", None)
        assert post_fn is not None, "jwt_required() wrapper did not expose __wrapped__"

        body, status = post_fn(resource)

    assert status == 200
    assert body == {"message": "Logged out"}
    assert captured["jti"] == "JTI-123"
