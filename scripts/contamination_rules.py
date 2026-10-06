"""CHRONOCAIRN R2.1: deterministic, testable contamination procedure.
This is a rules implementation, not evidence from a human playtest.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path
from typing import Protocol

RULES = json.loads((Path(__file__).resolve().parents[1] / "_data/contamination.json").read_text())
ZONES = RULES["zones"]

class Dice(Protocol):
    def randint(self, a: int, b: int) -> int: ...
    def choice(self, values: list[int]) -> int: ...

def integer(value: int, low: int, high: int, name: str) -> int:
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{name} must be an integer in [{low}, {high}]")
    return value

def effective_wil(wil: int, quirks: int, penalty_cap: int | None = None) -> int:
    integer(wil, 1, 1000, "wil")
    integer(quirks, 0, 5, "quirks")
    cap = RULES["penalty_cap"] if penalty_cap is None else integer(penalty_cap, 0, 5, "penalty_cap")
    return wil - min(quirks, cap)

def save_succeeds(roll: int, target: int) -> bool:
    integer(roll, 1, 20, "roll")
    return roll == 1 or (roll != 20 and roll <= target)

def net_damage(wil: int, raw: int, reduction: int = 1) -> int:
    integer(wil, 1, 1000, "wil")
    integer(raw, 1, 1000, "raw")
    integer(reduction, 0, 1000, "reduction")
    return min(max(RULES["minimum_damage"], raw - reduction), (wil + 1) // 2)

@dataclass(frozen=True)
class Outcome:
    wil: int
    quirks: frozenset[int]
    damage: int
    gained: int | None
    echo_cause: str | None

def resolve_check(wil: int, quirks: frozenset[int], die: int, rng: Dice,
                  reduction: int = 1, penalty_cap: int | None = None) -> Outcome:
    if len(quirks) > 5 or any(type(q) is not int or not 1 <= q <= RULES["quirk_table_size"] for q in quirks):
        raise ValueError("A living character must have 0-5 distinct Quirks numbered 1-12")
    integer(die, 2, 1000, "die")
    integer(reduction, 0, 1000, "reduction")
    target = effective_wil(wil, len(quirks), penalty_cap)
    if save_succeeds(rng.randint(1, 20), target):
        return Outcome(wil, quirks, 0, None, None)
    damage = net_damage(wil, rng.randint(1, die), reduction)
    remaining = wil - damage
    if remaining == 0:
        return Outcome(remaining, quirks, damage, None, "wil_zero")
    gained = None
    if damage >= RULES["quirk_threshold"]:
        # Uniform choice over unused entries is exactly equivalent to rerolling duplicates.
        gained = rng.choice([q for q in range(1, RULES["quirk_table_size"] + 1) if q not in quirks])
        quirks = quirks | {gained}
    cause = "sixth_quirk" if len(quirks) == RULES["echo_quirks"] else None
    return Outcome(remaining, frozenset(quirks), damage, gained, cause)

def recover(wil: int, maximum: int, roll: int, *, deprived: bool = False,
            completed: bool = True, echo: bool = False) -> int:
    integer(wil, 0, 1000, "wil")
    integer(maximum, wil, 1000, "maximum")
    integer(roll, 1, 8, "recovery roll")
    return wil if deprived or not completed or echo else min(maximum, wil + roll)

@dataclass
class ExposureClock:
    """Fraction of one interval, preserved on zone changes and brief Green pauses.
    One uninterrupted 8-hour Green rest clears residual exposure, never WIL/Quirks.
    A sheltered contaminated room is not Green. Scripted checks are separate.
    """
    dose: Fraction = Fraction(0)
    green_rest_minutes: int = 0

    def advance(self, zone: str, minutes: int, *, resting: bool = False) -> list[int]:
        if zone not in ZONES:
            raise ValueError(f"Unknown zone: {zone}")
        integer(minutes, 0, 10**9, "minutes")
        if minutes == 0:
            return []
        interval = ZONES[zone]["interval_minutes"]
        if interval is None:
            self.green_rest_minutes = self.green_rest_minutes + minutes if resting else 0
            if self.green_rest_minutes >= RULES["safe_reset_hours"] * 60:
                self.dose = Fraction(0)
            return []
        self.green_rest_minutes = 0
        self.dose += Fraction(minutes, interval)
        checks = int(self.dose)
        self.dose -= checks
        return [ZONES[zone]["damage_die"]] * checks
