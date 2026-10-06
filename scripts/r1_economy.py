"""Integer-dollar reference implementation for the R1 weekly ledger.

This is an executable rules reference, not a campaign or player-behaviour model.
"""
from dataclasses import dataclass
from typing import Optional

START_CASH, START_DEBT = 500, 500
BASE_PAY = {"Recruit": 800, "Agent": 1200, "Veteran": 1800}
GROSS_BANDS = {"failure": 0, "standard": 200, "strong": 300, "exceptional": 500}
THRESHOLDS = (700, 1300, 2200, 4000)


def money(value: int, name: str = "amount") -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{name} must be a non-negative whole-dollar integer")
    return value


def interest(principal: int) -> int:
    """Interest dollars only; exact ceiling of principal / 20, no floats."""
    return (money(principal, "principal") + 19) // 20


def salary(tier: str, loyalty: int = 5, benefits: bool = True) -> int:
    if tier not in BASE_PAY or type(loyalty) is not int or not 0 <= loyalty <= 10:
        raise ValueError("invalid tier or Loyalty")
    pay = BASE_PAY[tier]
    return pay * 3 // 2 if benefits and loyalty >= 9 else pay


def mission_pay(outcome: str, *, bounty: Optional[int] = None,
                trusted_assignment: bool = False, loyalty: int = 5) -> int:
    """$50 allowance plus one net performance award.

    A briefed bounty REPLACES the band. Trusted +$200 is a gross adjustment
    to a briefed successful assignment, not a second award, and cannot be
    added to a replacement bounty. Failure retains only the allowance.
    """
    if outcome not in GROSS_BANDS:
        raise ValueError("unknown outcome")
    if type(loyalty) is not int or not 0 <= loyalty <= 10:
        raise ValueError("invalid Loyalty")
    if bounty is not None:
        money(bounty, "bounty")
        if not 300 <= bounty <= 1000:
            raise ValueError("briefed bounty must be $300-$1,000")
        if trusted_assignment:
            raise ValueError("do not stack a replacement bounty and Trusted adjustment")
    if trusted_assignment and loyalty not in (7, 8):
        raise ValueError("Trusted assignment adjustment requires Loyalty 7-8")
    if outcome == "failure":
        return 50
    gross = bounty if bounty is not None else GROSS_BANDS[outcome]
    if trusted_assignment:
        gross += 200
    return 50 + gross * 7 // 10


@dataclass(frozen=True)
class Settlement:
    cash: int
    debt: int
    shortfall: int
    repayment: int
    clemency: int
    interest: int


def settle_week(cash: int, debt: int, income: int, expenses: int, *,
                repayment: int = 0, clemency: int = 0,
                reserve: Optional[int] = None) -> Settlement:
    """Close a week. Income contains ONLY receipts not already in opening Cash.

    Expenses are incurred obligations. A shortfall is recorded against a named
    creditor; this arithmetic does not grant credit or conjure undelivered goods.
    Explicit repayment is clamped to available Cash and Debt. Alternatively,
    reserve implements a simulation policy, NOT compulsory player behaviour.
    """
    for name, value in locals().copy().items():
        if value is not None:
            money(value, name)
    if reserve is not None and repayment:
        raise ValueError("choose explicit repayment OR reserve policy")
    available = cash + income
    shortfall = max(0, expenses - available)
    cash = max(0, available - expenses)
    principal = debt + shortfall
    desired = max(0, cash - reserve) if reserve is not None else repayment
    paid = min(desired, cash, principal)
    cash -= paid
    principal -= paid
    forgiven = min(clemency, principal)
    principal -= forgiven
    charge = interest(principal)
    return Settlement(cash, principal + charge, shortfall, paid, forgiven, charge)


def clemency_amount(loyalty: int, week: int, last_used: Optional[int] = None) -> int:
    if type(loyalty) is not int or not 0 <= loyalty <= 10:
        raise ValueError("invalid Loyalty")
    if type(week) is not int or week < 1:
        raise ValueError("week must be positive")
    if last_used is not None and (type(last_used) is not int or last_used < 1 or last_used > week):
        raise ValueError("invalid last-used week")
    if last_used is not None and week - last_used < 4:
        return 0
    return 400 if loyalty >= 7 else 300 if loyalty >= 5 else 0


def can_promote(successes: int, completed_recruit_weeks: int, loyalty: int) -> bool:
    money(successes, "successes")
    money(completed_recruit_weeks, "completed Recruit weeks")
    if type(loyalty) is not int or not 0 <= loyalty <= 10:
        raise ValueError("invalid Loyalty")
    return successes >= 8 and completed_recruit_weeks >= 8 and loyalty >= 4


def cash_out(certificates: int) -> tuple[int, int]:
    money(certificates, "certificates")
    return certificates * 800, int(certificates > 0)


class ReceiptBook:
    """Minimal duplicate-posting guard for examples and external ledger tools."""
    def __init__(self, cash: int = START_CASH):
        self.cash = money(cash, "cash")
        self.posted: set[str] = set()

    def credit(self, receipt_id: str, amount: int) -> None:
        if not isinstance(receipt_id, str) or not receipt_id.strip():
            raise ValueError("a non-empty receipt ID is required")
        money(amount)
        if receipt_id in self.posted:
            raise ValueError(f"income already posted: {receipt_id}")
        self.cash += amount
        self.posted.add(receipt_id)
