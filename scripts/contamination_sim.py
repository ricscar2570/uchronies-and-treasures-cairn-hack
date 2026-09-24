#!/usr/bin/env python3
"""
Contamination / Temporal Quirk subsystem Monte Carlo for CHRONOCAIRN.

Validates the relative effect of the accumulation penalty (D2): each Quirk lowers
the contamination save target by 1. Calibrated so the no-penalty case reproduces
the documented ~25% echo baseline. Subsystem only -- not the full campaign model.

Usage:  python3 contamination_sim.py
"""
import random
from math import ceil

CHECKS_PER_SESSION = 2     # calibration: orange-zone exposure per 15-session campaign
THERAPY_RESTORE    = 6     # between-session recovery die (Division / black-market therapy)
SESSIONS           = 15
N                  = 200_000
SEED               = 42


def run(penalty_cap):
    """penalty_cap = max contamination-save penalty from Quirks (None = no penalty)."""
    max_wil = sum(random.randint(1, 6) for _ in range(3))
    wil = max_wil
    quirks = 0
    have = set()
    for _ in range(SESSIONS):
        for _ in range(CHECKS_PER_SESSION):
            penalty = 0 if penalty_cap is None else min(quirks, penalty_cap)
            eff = wil - penalty
            r = random.randint(1, 20)
            success = (r == 1) or (r <= eff and r != 20)
            if not success:
                dmg = max(1, random.randint(1, 4) - 1)   # orange d4, suit -1
                dmg = min(dmg, ceil(wil / 2))            # anti-spiral damage cap
                wil -= dmg
                if wil <= 0:
                    return "echo"
                if dmg >= 3:                             # significant exposure -> Quirk
                    q = random.randint(1, 12)
                    guard = 0
                    while q in have and guard < 40:
                        q = random.randint(1, 12); guard += 1
                    if q not in have:
                        have.add(q); quirks += 1
                        if quirks >= 6:
                            return "echo"
        wil = min(max_wil, wil + random.randint(1, THERAPY_RESTORE))
    return "survive"


def echo_rate(penalty_cap):
    random.seed(SEED)
    return sum(run(penalty_cap) == "echo" for _ in range(N)) / N * 100


if __name__ == "__main__":
    print(f"Contamination subsystem MC  (N={N:,}, seed={SEED}, {SESSIONS} sessions)\n")
    print(f"  no penalty (baseline)     echo = {echo_rate(None):5.1f}%")
    print(f"  D2 penalty cap -2         echo = {echo_rate(2):5.1f}%")
    print(f"  D2 penalty cap -3 (rec.)  echo = {echo_rate(3):5.1f}%")
    print(f"  D2 penalty uncapped       echo = {echo_rate(5):5.1f}%")
