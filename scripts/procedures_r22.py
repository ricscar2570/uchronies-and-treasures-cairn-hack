#!/usr/bin/env python3
"""Executable reference examples for R2.2, not a coupled campaign simulator."""
from dataclasses import dataclass
from typing import Literal


def integer(value: int, name: str, low: int = 0, high: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < low or (high is not None and value > high):
        raise ValueError(f'{name}: invalid integer {value!r}')
    return value


def unstable(loyalty: int, corruption: int) -> bool:
    integer(loyalty, 'loyalty', 0, 10); integer(corruption, 'corruption', 0, 10)
    return loyalty >= 3 and corruption >= 3 and abs(loyalty - corruption) <= 2


def base_pay(tier: str, loyalty: int, is_unstable: bool = False, probation: bool = False) -> int:
    integer(loyalty, 'loyalty', 0, 10)
    if tier not in {'Recruit', 'Agent', 'Veteran'}: raise ValueError('unknown rank')
    pay = {'Recruit': 800, 'Agent': 1200, 'Veteran': 1800}[tier]
    if loyalty >= 9 and not is_unstable: pay = pay * 3 // 2
    return pay // 2 if probation else pay


def mission_pay(outcome: str, loyalty: int, is_unstable: bool = False,
                uplift_used: bool = False, bounty_gross: int | None = None) -> int:
    """Values are all dollars. No assignment = no allowance; one award otherwise."""
    integer(loyalty, 'loyalty', 0, 10)
    bands = ['Failure', 'Standard', 'Strong', 'Exceptional']
    if outcome == 'None':
        if bounty_gross is not None: raise ValueError('bounty without assignment')
        return 0
    if outcome not in bands: raise ValueError('unknown performance band')
    if bounty_gross is not None:
        integer(bounty_gross, 'bounty', 300, 1000)
        if bounty_gross % 10: raise ValueError('whole-dollar example model requires bounty multiples of $10')
        return 50 + bounty_gross * 70 // 100
    idx = bands.index(outcome)
    if idx > 0 and loyalty >= 7 and not is_unstable and not uplift_used:
        idx = min(3, idx + 1)
    return [50, 190, 260, 400][idx]


@dataclass(frozen=True)
class Close:
    cash: int
    debt: int
    unpaid: int
    interest: int


def weekly_close(cash: int, debt: int, income: int, costs: int,
                 repayment: int = 0, clemency: int = 0) -> Close:
    for name, value in locals().copy().items(): integer(value, name)
    available = cash + income
    unpaid = max(0, costs - available)
    after_costs = max(0, available - costs)
    if repayment > after_costs or repayment > debt + unpaid:
        raise ValueError('repayment exceeds available Cash or Debt')
    principal = max(0, debt + unpaid - repayment - clemency)
    closing_debt = (105 * principal + 99) // 100  # exact upward dollar rounding
    return Close(after_costs - repayment, closing_debt, unpaid, closing_debt - principal)


def scar_result(hp_before: int, damage_roll: int, armor: int) -> int | None:
    integer(hp_before, 'HP'); integer(damage_roll, 'damage'); integer(armor, 'Armor', 0, 3)
    taken = max(0, damage_roll - armor)
    return min(12, taken) if hp_before > 0 and taken == hp_before else None


def attack(hp: int, strength: int, damage_roll: int, armor: int) -> dict:
    integer(strength, 'STR'); integer(hp, 'HP')
    scar = scar_result(hp, damage_roll, armor)
    damage = max(0, damage_roll - armor)
    overflow = max(0, damage - hp)
    reduced = max(0, strength - overflow)
    return {'hp': max(0, hp-damage), 'str': reduced, 'scar': scar,
            'save_target': reduced if overflow and reduced > 0 else None, 'dead': reduced == 0}


@dataclass(frozen=True)
class Ammunition:
    state: Literal['ready', 'low', 'empty'] = 'ready'
    spares: int = 2

    def __post_init__(self):
        if self.state not in {'ready', 'low', 'empty'}: raise ValueError('unknown magazine state')
        integer(self.spares, 'spares')

    @property
    def can_fire(self) -> bool:
        return self.state != 'empty'

    @property
    def spare_slots(self) -> int:
        return (self.spares + 1) // 2

    def after_firefight(self, die: int) -> 'Ammunition':
        integer(die, 'usage die', 1, 6)
        if not self.can_fire: raise ValueError('an empty weapon could not have fired')
        if die == 1 or (die == 2 and self.state == 'low'): state = 'empty'
        elif die == 2: state = 'low'
        else: state = self.state
        return Ammunition(state, self.spares)

    def reload(self) -> 'Ammunition':
        if self.state != 'empty' or self.spares == 0: raise ValueError('no empty magazine or no spare')
        return Ammunition('ready', self.spares-1)


def ten_week_ledger() -> list[dict]:
    outcomes = ['Standard','None','Standard','None','Strong','None','Standard','Exceptional','None','Standard']
    costs = [950,1000,1050,1200,1000,950,1100,950,950+50,1050]
    loyalty, cash, debt, successes = 5, 500, 500, 0
    result=[]
    for week, (outcome, cost) in enumerate(zip(outcomes, costs), 1):
        income = base_pay('Recruit', loyalty) + mission_pay(outcome, loyalty)
        close = weekly_close(cash, debt, income, cost)
        result.append({'week':week,'loyalty_start':loyalty,'income':income,'costs':cost,
                       'cash':close.cash,'debt':close.debt})
        if outcome != 'None':
            loyalty = min(10, loyalty+1); successes += 1
        cash, debt = close.cash, close.debt
    return result
