from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from types import SimpleNamespace

import pytest
import src.backend.admin.services.dashboard_service as svc

from .mocks.mock_id import MockId
from .mocks.mock_query import MockQuery

def test_list_users(monkeypatch) -> None:
    fake_users = [
        SimpleNamespace(
            id=1,
            first_name="Nina",
            second_name="Valkova",
            username="nina",
            email="nina@test.com",
            birth_number="123",
            created_at=datetime(2026, 2, 7, 10, 0, 0),
        )
    ]

    fake_id = MockId(desc_value="USERS_DESC")
    fake_query = MockQuery(fake_users)

    class FakeUser:
        id = fake_id
        query = fake_query

    monkeypatch.setattr(svc, "User", FakeUser, raising=False)

    body, status = svc.AdminDashboardService.list_users()

    assert status == 200
    assert fake_id.desc_called == 1
    assert fake_query.order_by_called == 1
    assert fake_query.last_order_by_arg == "USERS_DESC"

    assert body[0]["id"] == 1
    assert body[0]["first_name"] == "Nina"
    assert body[0]["second_name"] == "Valkova"
    assert body[0]["username"] == "nina"
    assert body[0]["email"] == "nina@test.com"
    assert body[0]["birth_number"] == "123"
    assert body[0]["created_at"] == "2026-02-07T10:00:00"


def test_list_users_created_at_none(monkeypatch) -> None:
    fake_users = [
        SimpleNamespace(
            id=10,
            first_name="NoDate",
            second_name="User",
            username="nodate",
            email="nodate@test.com",
            birth_number=None,
            created_at=None,
        )
    ]

    fake_id = MockId(desc_value="USERS_DESC")
    fake_query = MockQuery(fake_users)

    class FakeUser:
        id = fake_id
        query = fake_query

    monkeypatch.setattr(svc, "User", FakeUser, raising=False)

    body, status = svc.AdminDashboardService.list_users()

    assert status == 200
    assert body == [
        {
            "id": 10,
            "first_name": "NoDate",
            "second_name": "User",
            "username": "nodate",
            "email": "nodate@test.com",
            "birth_number": None,
            "created_at": None,
        }
    ]


def test_list_users_empty(monkeypatch) -> None:
    fake_id = MockId(desc_value="USERS_DESC")
    fake_query = MockQuery([])

    class FakeUser:
        id = fake_id
        query = fake_query

    monkeypatch.setattr(svc, "User", FakeUser, raising=False)

    body, status = svc.AdminDashboardService.list_users()

    assert status == 200
    assert body == []


def test_list_accounts(monkeypatch) -> None:
    fake_accounts = [
        SimpleNamespace(
            id=2,
            account_number="ACC-1",
            balance=Decimal("12.50"),
            created_at=None,
        )
    ]

    fake_id = MockId(desc_value="ACCOUNTS_DESC")
    fake_query = MockQuery(fake_accounts)

    class FakeAccount:
        id = fake_id
        query = fake_query

    monkeypatch.setattr(svc, "Account", FakeAccount, raising=False)

    body, status = svc.AdminDashboardService.list_accounts()

    assert status == 200
    assert fake_id.desc_called == 1
    assert fake_query.order_by_called == 1
    assert fake_query.last_order_by_arg == "ACCOUNTS_DESC"

    assert body == [
        {"id": 2, "account_number": "ACC-1", "balance": 12.5, "created_at": None}
    ]


def test_list_accounts_created_at_iso(monkeypatch) -> None:
    fake_accounts = [
        SimpleNamespace(
            id=5,
            account_number="ACC-5",
            balance=Decimal("0.00"),
            created_at=datetime(2026, 2, 8, 9, 30, 0),
        )
    ]

    fake_id = MockId(desc_value="ACCOUNTS_DESC")
    fake_query = MockQuery(fake_accounts)

    class FakeAccount:
        id = fake_id
        query = fake_query

    monkeypatch.setattr(svc, "Account", FakeAccount, raising=False)

    body, status = svc.AdminDashboardService.list_accounts()

    assert status == 200
    assert body[0]["created_at"] == "2026-02-08T09:30:00"


def test_list_transactions(monkeypatch) -> None:
    fake_txs = [
        SimpleNamespace(
            id=3,
            account_id=2,
            from_account="A",
            to_account="B",
            amount=Decimal("10.00"),
            balance=None,
            currency="EUR",
            type="DEBIT",
            operation="TRANSFER",
            date=None,
        )
    ]

    fake_id = MockId(desc_value="TX_DESC")
    fake_query = MockQuery(fake_txs)

    class FakeTransaction:
        id = fake_id
        query = fake_query

    monkeypatch.setattr(svc, "Transaction", FakeTransaction, raising=False)

    body, status = svc.AdminDashboardService.list_transactions()

    assert status == 200
    assert fake_id.desc_called == 1
    assert fake_query.order_by_called == 1
    assert fake_query.last_order_by_arg == "TX_DESC"

    assert body[0]["id"] == 3
    assert body[0]["account_id"] == 2
    assert body[0]["from_account"] == "A"
    assert body[0]["to_account"] == "B"
    assert body[0]["amount"] == 10.0
    assert body[0]["balance"] is None
    assert body[0]["currency"] == "EUR"
    assert body[0]["type"] == "DEBIT"
    assert body[0]["operation"] == "TRANSFER"
    assert body[0]["date"] is None


def test_list_transactions_date_iso_and_balance_float(monkeypatch) -> None:
    fake_txs = [
        SimpleNamespace(
            id=99,
            account_id=7,
            from_account="X",
            to_account=None,
            amount=Decimal("123.45"),
            balance=Decimal("999.99"),
            currency="BGN",
            type="CREDIT",
            operation="CASH_DEPOSIT",
            date=datetime(2026, 2, 8, 8, 0, 0),
        )
    ]

    fake_id = MockId(desc_value="TX_DESC")
    fake_query = MockQuery(fake_txs)

    class FakeTransaction:
        id = fake_id
        query = fake_query

    monkeypatch.setattr(svc, "Transaction", FakeTransaction, raising=False)

    body, status = svc.AdminDashboardService.list_transactions()

    assert status == 200
    assert body == [
        {
            "id": 99,
            "account_id": 7,
            "from_account": "X",
            "to_account": None,
            "amount": 123.45,
            "balance": 999.99,
            "currency": "BGN",
            "type": "CREDIT",
            "operation": "CASH_DEPOSIT",
            "date": "2026-02-08T08:00:00",
        }
    ]


def test_list_users_multiple(monkeypatch) -> None:
    fake_users = [
        SimpleNamespace(
            id=2,
            first_name="B",
            second_name="User",
            username="b",
            email="b@test.com",
            birth_number=None,
            created_at=None,
        ),
        SimpleNamespace(
            id=1,
            first_name="A",
            second_name="User",
            username="a",
            email="a@test.com",
            birth_number=None,
            created_at=None,
        ),
    ]

    fake_id = MockId(desc_value="USERS_DESC")
    fake_query = MockQuery(fake_users)

    class FakeUser:
        id = fake_id
        query = fake_query

    monkeypatch.setattr(svc, "User", FakeUser, raising=False)

    body, status = svc.AdminDashboardService.list_users()

    assert status == 200
    assert len(body) == 2
    assert body[0]["id"] == 2
    assert body[1]["id"] == 1


def test_list_accounts_balance_is_float(monkeypatch) -> None:
    fake_accounts = [
        SimpleNamespace(
            id=1,
            account_number="ACC-X",
            balance=Decimal("100.00"),
            created_at=None,
        )
    ]

    fake_id = MockId()
    fake_query = MockQuery(fake_accounts)

    class FakeAccount:
        id = fake_id
        query = fake_query

    monkeypatch.setattr(svc, "Account", FakeAccount, raising=False)

    body, status = svc.AdminDashboardService.list_accounts()

    assert status == 200
    assert isinstance(body[0]["balance"], float)
