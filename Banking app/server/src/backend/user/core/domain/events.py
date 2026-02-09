from dataclasses import dataclass
from decimal import Decimal
from locale import currency

class Event:
    pass

@dataclass(frozen=True)
class MoneySend(Event):
    from_account: str
    to_account: str
    amount: Decimal
    currency: str

@dataclass(frozen=True)
class CashDeposit(Event):
    account_number: str
    amount: Decimal    

@dataclass(frozen=True)    
class CashWithdrawn(Event):
    account_number: str
    amount: Decimal

