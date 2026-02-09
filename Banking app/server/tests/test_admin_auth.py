from __future__ import annotations

from flask import Flask
import pytest

import src.backend.admin.api.resources.auth as res


@pytest.fixture
def app() -> Flask:
    return Flask(__name__)


def test_admin_register_post_calls_service_with_json(monkeypatch, app) -> None:
    captured = {}

    class FakeAdminAuthService:
        @staticmethod
        def register(data):
            captured["data"] = data
            return {"message": "Admin registered"}, 201

    monkeypatch.setattr(res, "AdminAuthService", FakeAdminAuthService, raising=False)

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


def test_admin_register_post_when_json_null_uses_empty_dict(monkeypatch, app) -> None:
    captured = {}

    class FakeAdminAuthService:
        @staticmethod
        def register(data):
            captured["data"] = data
            return {"message": "ok"}, 201

    monkeypatch.setattr(res, "AdminAuthService", FakeAdminAuthService, raising=False)

    with app.test_request_context(
        path="/api/admin/register",
        method="POST",
        data="null",
        content_type="application/json",
    ):
        resource = res.AdminRegister()
        body, status = resource.post()

    assert status == 201
    assert body == {"message": "ok"}
    assert captured["data"] == {}


def test_admin_login_post_calls_service_with_username_password(
    monkeypatch, app
) -> None:
    captured = {}

    class FakeAdminAuthService:
        @staticmethod
        def login(username, password):
            captured["username"] = username
            captured["password"] = password
            return {"access_token": "TOKEN"}, 200

    monkeypatch.setattr(res, "AdminAuthService", FakeAdminAuthService, raising=False)

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


def test_admin_login_post_missing_keys_passes_none(monkeypatch, app) -> None:
    captured = {}

    class FakeAdminAuthService:
        @staticmethod
        def login(username, password):
            captured["username"] = username
            captured["password"] = password
            return {"message": "Invalid credentials"}, 401

    monkeypatch.setattr(res, "AdminAuthService", FakeAdminAuthService, raising=False)

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


def test_admin_logout_post_calls_service_with_jti(monkeypatch, app) -> None:
    captured = {}

    class FakeAdminAuthService:
        @staticmethod
        def logout(jti):
            captured["jti"] = jti
            return {"message": "Logged out"}, 200

    monkeypatch.setattr(res, "AdminAuthService", FakeAdminAuthService, raising=False)

    monkeypatch.setattr(res, "get_jwt", lambda: {"jti": "JTI-123"}, raising=False)

    with app.test_request_context(path="/api/admin/logout", method="POST"):
        resource = res.AdminLogout()
        
        post_fn = getattr(res.AdminLogout.post, "__wrapped__", None)
        assert post_fn is not None, "jwt_required() wrapper did not expose __wrapped__"

        body, status = post_fn(resource)

    assert status == 200
    assert body == {"message": "Logged out"}
    assert captured["jti"] == "JTI-123"
