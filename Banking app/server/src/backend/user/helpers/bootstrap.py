from ..services.messagebus  import MessageBus
from ..core.domain.events import MoneySend, CashWithdrawn, CashDeposit
from ..services.handlers import (
    send_transfer_email,
    send_withdraw_email,
    send_deposit_email,
)


def bootstrap() -> None:
    MessageBus.register(MoneySend, send_transfer_email)
    MessageBus.register(CashWithdrawn, send_withdraw_email)
    MessageBus.register(CashDeposit, send_deposit_email)
