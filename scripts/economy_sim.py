#!/usr/bin/env python3
"""Reproducible R1 sensitivity study; no prediction of actual player behaviour."""
import argparse
import csv
import hashlib
import json
import random
import statistics
from pathlib import Path
from r1_economy import (START_CASH, START_DEBT, salary, mission_pay,
                        settle_week, can_promote, clemency_amount)

SEED, TRIALS, WEEKS = 42026, 100_000, 15
SCENARIOS = {
    "isolated_honest": (False, False, False, False),
    "isolated_first_offer": (False, False, False, True),
    "loyalty_honest": (True, False, False, False),
    "loyalty_trusted_honest": (True, True, False, False),
    "loyalty_trusted_clemency_honest": (True, True, True, False),
}


def unexpected_expense(rng):
    roll = rng.randint(1, 6)
    return [0, 50, 100, 150, 200][roll - 1] if roll < 6 else rng.randrange(100, 501, 50)


def mission_outcome(rng):
    if rng.random() >= 0.65:
        return "failure"
    u = rng.random()
    return "standard" if u < .70 else "strong" if u < .95 else "exceptional"


def simulate(draws, scenario):
    evolve_loyalty, trusted, use_clemency, first_offer = SCENARIOS[scenario]
    cash, debt, loyalty, successes = START_CASH, START_DEBT, 5, 0
    accepted, first_700, last_clemency = False, None, None
    ever_1300, trace, tier = False, [], "Recruit"
    for week, (outcome, unexpected) in enumerate(draws, 1):
        # Pay and access are locked at week opening. Promotion applies NEXT week.
        opening_loyalty, opening_tier = loyalty, tier
        base = salary(tier, loyalty, benefits=evolve_loyalty)
        bonus = mission_pay(outcome, trusted_assignment=trusted and loyalty in (7, 8), loyalty=loyalty)
        success = outcome != "failure"
        successes += int(success)
        if evolve_loyalty and success:
            loyalty = min(10, loyalty + 1)
        # Policy: request clemency only at week 4, 8, 12,... when debt exists.
        forgiveness = 0
        if use_clemency and week % 4 == 0 and debt > 0:
            forgiveness = clemency_amount(loyalty, week, last_clemency)
            if forgiveness:
                loyalty -= 1
                last_clemency = week
        closed = settle_week(cash, debt, base + bonus, 900 + unexpected,
                             reserve=200, clemency=forgiveness)
        cash, debt = closed.cash, closed.debt
        trigger_debt = debt
        if debt >= 700 and first_700 is None:
            first_700 = week
        ever_1300 |= debt >= 1300
        offer_cash = 0
        if first_offer and not accepted and debt >= 700:
            # Optimistic money-only offer: completion, delay and consequences
            # are NOT simulated. It is not merely money for accepting an offer.
            accepted = True
            offer_cash = 1500
            cash += offer_cash
            paid = min(max(0, cash - 200), debt)
            cash, debt = cash - paid, debt - paid
        eligible = can_promote(successes, week, loyalty)
        if eligible:
            tier = "Agent"
        trace.append({"week": week, "tier_paid": opening_tier,
                      "opening_loyalty": opening_loyalty, "closing_loyalty": loyalty,
                      "outcome": outcome, "salary": base, "mission_pay": bonus,
                      "unexpected": unexpected, "shortfall": closed.shortfall,
                      "repayment": closed.repayment, "clemency": closed.clemency,
                      "interest": closed.interest, "trigger_debt": trigger_debt,
                      "offer_cash": offer_cash, "cash": cash, "debt": debt,
                      "eligible_for_agent_next_week": eligible})
    return trace, first_700, ever_1300, accepted


def summary(rows, scenario, trials):
    result = {"scenario": scenario, "trials": trials}
    for week in (10, 15):
        debt = sorted(r[0][week]["debt"] for r in rows)
        cash = [r[0][week]["cash"] for r in rows]
        result[f"median_debt_week_{week}"] = statistics.median(debt)
        result[f"debt_p90_week_{week}"] = debt[(9 * trials + 9) // 10 - 1]
        result[f"median_cash_week_{week}"] = statistics.median(cash)
    first = [r[1] for r in rows if r[1] is not None]
    result.update(ever_debt_700=len(first) / trials,
                  ever_debt_1300=sum(r[2] for r in rows) / trials,
                  median_first_700_week=statistics.median(first) if first else None,
                  agent_paid_week_15=sum(r[0][15]["tier_paid"] == "Agent" for r in rows) / trials,
                  eligible_for_agent_after_week_15=sum(r[0][15]["eligible_for_agent_next_week"] for r in rows) / trials,
                  mean_corruption_from_modelled_offer=sum(r[3] for r in rows) / trials)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=TRIALS)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--output", type=Path, default=Path("reports/r1b"))
    parser.add_argument("--scenario", choices=tuple(SCENARIOS), action="append")
    args = parser.parse_args()
    if args.trials < 1:
        parser.error("--trials must be at least 1")
    args.output.mkdir(parents=True, exist_ok=True)
    results = []
    # Reinitialize RNG for each policy: identical mission/expense paths per trial.
    for scenario in args.scenario or SCENARIOS:
        rng = random.Random(args.seed)
        rows = []
        for trial in range(args.trials):
            draws = [(mission_outcome(rng), unexpected_expense(rng)) for _ in range(WEEKS)]
            trace, first, ever, accepted = simulate(draws, scenario)
            rows.append(({10: trace[9], 15: trace[14]}, first, ever, accepted))
            if trial == 0:
                with (args.output / f"trace_{scenario}.csv").open("w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=list(trace[0]))
                    writer.writeheader()
                    writer.writerows(trace)
        results.append(summary(rows, scenario, args.trials))
        print(json.dumps(results[-1], ensure_ascii=False), flush=True)
    base = Path(__file__).resolve().parent
    payload = {"model": "R1B-2026-10-06", "seed": args.seed, "weeks": WEEKS,
               "trials_per_scenario": args.trials, "quantile": "nearest rank",
               "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (base / "r1_economy.py", base / "economy_sim.py")},
               "assumptions": [
                   "One field mission per week; independent 65% success, not observed playtest data.",
                   "Successful outcome bands: 70% standard, 25% strong, 5% exceptional.",
                   "Uniform d6 expenses; on six, uniform nine costs $100-$500 in $50 steps.",
                   "$200 reserve repayment policy; financed shortfalls with supplies delivered.",
                   "Loyalty starts 5; evolving cases grant +1 only on mission success; no penalties except requested clemency.",
                   "Hero salary +50% from next week; Trusted assignment +$200 gross only in enabled scenario, at opening Loyalty 7-8.",
                   "Clemency policy requests at weeks 4, 8, 12 if opening debt is positive; -1 Loyalty paid even if forgiveness is partly unused.",
                   "Promotion requires eight successes, eight completed weeks and Loyalty >=4; first Agent salary next week.",
                   "First-offer case assumes successful immediate courier completion after settlement: $1500, +1 Corruption; no risk/time/other consequences simulated.",
                   "No side gigs, extra dependents, injury, missed pay, skipped medicine, death, certificates, equipment expenses beyond the expense table, or full faction simulation."
               ], "results": results}
    (args.output / "economy_results.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    with (args.output / "economy_results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0]))
        w.writeheader()
        w.writerows(results)


if __name__ == "__main__":
    main()
