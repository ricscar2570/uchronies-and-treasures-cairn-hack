#!/usr/bin/env python3
"""CHRONOCAIRN R1 economy subsystem validation.

This is a pressure test, not a forecast of player behaviour.
"""
import math
import random
import statistics

SEED = 42026
TRIALS = 100_000
WEEKS = 15
FIXED_EXPENSES = 900
PAY = {"Recruit": 800, "Agent": 1200}

def unexpected_expense(rng):
    roll = rng.randint(1, 6)
    if roll < 6:
        return [0, 50, 100, 150, 200][roll - 1]
    return rng.randrange(100, 501, 50)

def mission_bonus(rng):
    bonus = 50
    success = rng.random() < 0.65
    if success:
        u = rng.random()
        gross = 200 if u < 0.70 else 300 if u < 0.95 else 500
        bonus += round(gross * 0.70)
    return bonus, success

def settle_week(cash, debt, income, expenses, reserve=200):
    cash += income
    unpaid = max(0, expenses - cash)
    cash = max(0, cash - expenses)
    debt += unpaid
    repayment = min(max(0, cash - reserve), debt)
    cash -= repayment
    debt -= repayment
    if debt:
        debt = math.ceil(debt * 1.05)
    return cash, debt

def run(strategy, rng):
    cash, debt = 500, 500
    corruption = 0
    successes = 0
    accepted = set()
    ever_700 = ever_1300 = False
    first_700 = None

    for week in range(1, WEEKS + 1):
        tier = "Agent" if successes >= 8 else "Recruit"
        bonus, success = mission_bonus(rng)
        successes += int(success)
        cash, debt = settle_week(
            cash, debt,
            PAY[tier] + bonus,
            FIXED_EXPENSES + unexpected_expense(rng),
        )

        if debt >= 700:
            ever_700 = True
            if first_700 is None:
                first_700 = week
        if debt >= 1300:
            ever_1300 = True

        for idx, (threshold, payment, cost) in enumerate(
            [(700, 1500, 1), (1300, 2500, 2), (2200, 5000, 3)]
        ):
            if debt >= threshold and idx not in accepted:
                take = strategy == "corrupt" or (strategy == "mixed" and idx == 0)
                if take:
                    cash += payment
                    corruption += cost
                    accepted.add(idx)
                    repayment = min(max(0, cash - 200), debt)
                    cash -= repayment
                    debt -= repayment
                break

    return cash, debt, corruption, successes, ever_700, ever_1300, first_700

def summarize(strategy):
    rng = random.Random(SEED + {"honest": 0, "mixed": 1, "corrupt": 2}[strategy])
    rows = [run(strategy, rng) for _ in range(TRIALS)]
    debts = [r[1] for r in rows]
    cash = [r[0] for r in rows]
    first = [r[6] for r in rows if r[6] is not None]
    return {
        "strategy": strategy,
        "median_cash_week_15": statistics.median(cash),
        "median_debt_week_15": statistics.median(debts),
        "debt_p90_week_15": statistics.quantiles(debts, n=10)[8],
        "ever_debt_700": sum(r[4] for r in rows) / TRIALS,
        "ever_debt_1300": sum(r[5] for r in rows) / TRIALS,
        "median_first_700_week": statistics.median(first) if first else None,
        "agent_by_week_15": sum(r[3] >= 8 for r in rows) / TRIALS,
        "mean_corruption": statistics.mean(r[2] for r in rows),
    }

if __name__ == "__main__":
    print(f"trials={TRIALS:,} weeks={WEEKS} seed={SEED}")
    for strategy in ("honest", "mixed", "corrupt"):
        print(summarize(strategy))
