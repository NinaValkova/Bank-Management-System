from ...models.disposition import Disposition
from ..core.domain.events import MoneySend, CashWithdrawn, CashDeposit
from .email_service import EmailService


def send_transfer_email(event: MoneySend, uow) -> None:
    account = uow.account.get_by_number(event.from_account)
    disp = (
        uow.session.query(Disposition)
        .filter_by(account_id=account.id, type="OWNER")
        .first()
    )

    email = disp.user.email

    EmailService.send_email(
        user_email=email,
        subject="Transfer completed",
        text=(f"You sent {event.amount} " f"to account {event.to_account}"),
    )


def send_withdraw_email(event: CashWithdrawn, uow) -> None:
    account = uow.account.get_by_number(event.account_number)
    disp = (
        uow.session.query(Disposition)
        .filter_by(account_id=account.id, type="OWNER")
        .first()
    )

    email = disp.user.email

    EmailService.send_email(
        user_email=email,
        subject="Cash withdrawal",
        text=f"You withdrew {event.amount}",
    )


def send_deposit_email(event: CashDeposit, uow) -> None:
    account = uow.account.get_by_number(event.account_number)
    disp = (
        uow.session.query(Disposition)
        .filter_by(account_id=account.id, type="OWNER")
        .first()
    )

    email = disp.user.email

    EmailService.send_email(
        user_email=email,
        subject="Cash deposit",
        text=f"You deposited {event.amount}",
    )
