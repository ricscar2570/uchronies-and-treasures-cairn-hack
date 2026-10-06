#!/usr/bin/env python3
"""CHRONOCAIRN R2.1 reproducible diagnostic; NOT human validation or a forecast.
Run from repository root: python scripts/contamination_sim.py --runs 20000
All rows assume supplied medicine and a fresh, safely rested expedition clock.
A cycle is an expedition plus any stated completed care, not a session or week.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
from statistics import mean, median
from contamination_rules import RULES, ExposureClock, resolve_check, recover

PROFILES = [
    {"id":"yellow_short", "zone":"yellow", "minutes":240, "suit":1, "therapy":6},
    {"id":"yellow_standard", "zone":"yellow", "minutes":480, "suit":1, "therapy":6},
    {"id":"orange_standard", "zone":"orange", "minutes":360, "suit":1, "therapy":6},
    {"id":"red_standard", "zone":"red", "minutes":360, "suit":1, "therapy":6},
    {"id":"red_extended", "zone":"red", "minutes":540, "suit":1, "therapy":6},
    {"id":"black_short", "zone":"black", "minutes":60, "suit":1, "therapy":6},
    {"id":"red_heavy", "zone":"red", "minutes":360, "suit":2, "therapy":6},
    {"id":"yellow_no_care", "zone":"yellow", "minutes":480, "suit":1, "therapy":0},
]

def simulate(profile: dict, runs: int, cycles: int, seed: int, cap: int = 3) -> dict:
    if runs < 1 or cycles < 1:
        raise ValueError("runs and cycles must be positive")
    rng = random.Random(seed)
    checks = ExposureClock().advance(profile["zone"], profile["minutes"])
    causes, distribution = Counter(), Counter()
    all_quirks, survivor_quirks, first_gains, checks_taken = [], [], [], []
    wil_groups = {"3-8":Counter(), "9-12":Counter(), "13-18":Counter()}
    for _ in range(runs):
        maximum = sum(rng.randint(1, 6) for _ in range(3))
        wil, quirks, echo, first, taken = maximum, frozenset(), None, None, 0
        for cycle in range(1, cycles + 1):
            for die in checks:
                outcome = resolve_check(wil, quirks, die, rng, profile["suit"], cap)
                wil, quirks, echo = outcome.wil, outcome.quirks, outcome.echo_cause
                taken += 1
                if outcome.gained is not None and first is None:
                    first = cycle
                if echo:
                    break
            if echo:
                break
            if profile["therapy"]:
                wil = recover(wil, maximum, rng.randint(1, profile["therapy"]))
        causes[echo or "survived"] += 1
        group = wil_groups["3-8" if maximum <= 8 else "9-12" if maximum <= 12 else "13-18"]
        group["n"] += 1
        group["echo"] += int(echo is not None)
        all_quirks.append(len(quirks))
        checks_taken.append(taken)
        distribution[str(len(quirks))] += 1
        if echo is None:
            survivor_quirks.append(len(quirks))
        if first is not None:
            first_gains.append(first)
    return {"profile":profile, "runs":runs, "cycles":cycles, "seed":seed,
            "penalty_cap":cap, "scheduled_checks_per_expedition":len(checks),
            "mean_checks_taken":mean(checks_taken), "outcome_counts":dict(causes),
            "echo_percent":100*(runs-causes["survived"])/runs,
            "echo_wil_percent":100*causes["wil_zero"]/runs,
            "echo_sixth_percent":100*causes["sixth_quirk"]/runs,
            "quirks_all_mean":mean(all_quirks),
            "quirks_survivors_mean":mean(survivor_quirks) if survivor_quirks else None,
            "quirks_survivors_median":median(survivor_quirks) if survivor_quirks else None,
            "quirk_distribution_all":dict(distribution),
            "ever_quirk_percent":100*len(first_gains)/runs,
            "first_quirk_cycle_median_among_gainers":median(first_gains) if first_gains else None,
            "wil_groups":{k:dict(v) for k,v in wil_groups.items()}}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=42026)
    parser.add_argument("--output", type=Path, default=Path("reports/r2-contamination.json"))
    args = parser.parse_args()
    if args.runs < 1:
        parser.error("--runs must be positive")
    rows = []
    for index, profile in enumerate(PROFILES):
        rows.append(simulate(profile, args.runs, 10, args.seed + 1009*index))
    # Fifteen-cycle sensitivity: canonical -3 against historical uncapped -5.
    for cap in (0, 2, 3, 5):
        rows.append(simulate(PROFILES[3], args.runs, 15, args.seed+15015, cap))
    report = {"rules_version":RULES["version"], "evidence_type":"synthetic_subsystem_diagnostic",
              "human_playtests_added":0,
              "rules_sha256":hashlib.sha256((Path(__file__).resolve().parents[1]/"_data/contamination.json").read_bytes()).hexdigest(),
              "assumptions":["Initial WIL is 3d6; no starting Quirks.",
                "Fixed exposure per expedition; no extra hazard checks, combat or discretionary bonuses.",
                "One completed d6 treatment after each surviving expedition except no-care profile.",
                "Medicine supplied; no Deprivation; care timing and money NOT modeled.",
                "Each expedition starts after at least 8 hours of rest in Green.",
                "No Quirk-specific secondary effects, surgery, retirement decisions or tactical adaptation.",
                "Ten or fifteen expedition/care cycles are NOT automatically sessions or campaign weeks.",
                "All-character mean includes up to six Quirks acquired before loss; survivor mean is separate.",
                "Paired cap runs reuse the seed but do not preserve identical later random draws.",
                "No historical percentage is used as a calibration target."],
              "source_sha256":{name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()
                               for name in ("contamination_rules.py", "contamination_sim.py")},
              "rows":rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    lines = ["# CHRONOCAIRN R2.1 — Contamination diagnostic", "", "Synthetic subsystem evidence only. Human playtests added: **0**.", ""]
    lines += ["- "+x for x in report["assumptions"]]
    lines += ["", "| Profile | Cycles | Checks/expedition | Cap | Mean Quirks, all | Mean, survivors | Echo % | WIL-zero % | Sixth-Quirk % |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for row in rows:
        survivor = "n/a" if row["quirks_survivors_mean"] is None else f'{row["quirks_survivors_mean"]:.2f}'
        lines.append(f'| {row["profile"]["id"]} | {row["cycles"]} | {row["scheduled_checks_per_expedition"]} | -{row["penalty_cap"]} | {row["quirks_all_mean"]:.2f} | {survivor} | {row["echo_percent"]:.2f} | {row["echo_wil_percent"]:.2f} | {row["echo_sixth_percent"]:.2f} |')
    lines += ["", f'{args.runs:,} trials per row. Seeds and full distributions are recorded in the adjacent JSON.',
              "", "No confidence interval or mean here validates human usability, emotional pacing, or the coupled economy."]
    args.output.with_suffix(".md").write_text("\n".join(lines)+"\n")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
