---
layout: default
title: R1 Economy Verification
parent: Reference
nav_order: 7
---

# R1 Economy Verification

**R1B checkpoint, 6 October 2026.** This is a reproducible ledger and sensitivity study, not a forecast of player behaviour, proof of full-game balance, or a substitute for human playtesting.

The study runs **100,000 paths per policy for 15 weeks**, seed **42026**. Policies use the same generated mission outcomes and expenses, so differences are not caused by changing random samples. Week 10 and Week 15 results and a complete example trace for each policy are in the accompanying JSON/CSV reports.

## Results at Week 15

| Modelled policy | Median Cash | Median Debt | 90th percentile Debt | Ever reaches $700 Debt |
|---|---:|---:|---:|---:|
| Isolated ledger, refuses Zhou | $200 | $622 | $2,568 | 78.76% |
| Isolated ledger, one completed courier job | $1,171 | $0 | $313 | 78.76% |
| Loyalty progression and Hero salary | $4,216 | $0 | $0 | 40.15% |
| Loyalty + briefed Trusted assignments | $4,532 | $0 | $0 | 30.11% |
| Loyalty + Trusted assignments + clemency | $4,330 | $0 | $0 | 16.79% |

## What the Earlier 78.8% Result Actually Meant

The earlier result is reproducible for the **isolated ledger**: ordinary tier salaries, no Loyalty salary modifier, no Trusted assignments, no clemency and no side work. It must not be presented as the probability that an honest character under all published rules will reach Zhou's threshold. A percentage of modelled paths is not a probability of player acceptance.

Including the existing Hero salary benefit changes the result substantially. Honest financial stability is possible, and in the favourable Loyalty-policy scenarios it is common by Week 15. This checkpoint preserves that benefit rather than quietly deleting it to force a desired percentage. Whether economic pressure should remain strong beyond high Loyalty is a design decision still requiring campaign-level testing.

The first-offer case is deliberately optimistic about Zhou: it assumes the courier job is completed immediately and paid in full, without modelling time, discovery, danger or later leverage. It therefore demonstrates liquidity, not the true overall superiority of a corrupt strategy.

## Reproducible Assumptions

1. One field mission per week; independent 65% success, not observed playtest data.
2. Successful outcome bands: 70% standard, 25% strong, 5% exceptional.
3. Uniform d6 expenses; on six, uniform nine costs $100-$500 in $50 steps.
4. $200 reserve repayment policy; financed shortfalls with supplies delivered.
5. Loyalty starts 5; evolving cases grant +1 only on mission success; no penalties except requested clemency.
6. Hero salary +50% from next week; Trusted assignment +$200 gross only in enabled scenario, at opening Loyalty 7-8.
7. Clemency policy requests at weeks 4, 8, 12 if opening debt is positive; -1 Loyalty paid even if forgiveness is partly unused.
8. Promotion requires eight successes, eight completed weeks and Loyalty >=4; first Agent salary next week.
9. First-offer case assumes successful immediate courier completion after settlement: $1500, +1 Corruption; no risk/time/other consequences simulated.
10. No side gigs, extra dependents, injury, missed pay, skipped medicine, death, certificates, equipment expenses beyond the expense table, or full faction simulation.

## Measurement Details

Debt percentiles use the nearest-rank definition. The first-threshold week is calculated only among paths that reach the threshold. A first-threshold median is not the week when half of all characters necessarily cross it.

The model distinguishes being paid as an Agent during Week 15 from becoming eligible after Week 15. In the isolated baseline these rates are 81.60% and 88.71% respectively. The earlier label combined these different events.

The arithmetic uses whole-dollar integer operations. Weekly interest is principal divided by 20, rounded upward, then added to principal. No binary floating-point multiplication is used. The four-week and eight-week published ledgers, repayment caps, clemency, receipt duplication, payout bands and promotion timing are covered by automated tests.

## Edition Boundary

These results and corrections apply to the **R1 main-manual/web line**, starting at $500 Cash and $500 Debt. The separate Omnibus RC1 source line has different starting values, advancement and credit procedures. It has not been silently overwritten or declared aligned by this checkpoint. Do not combine their economic procedures in one campaign.

## Repeat the Check

Run `python -m unittest discover -s tests -v`, then `python scripts/economy_sim.py`, then `python scripts/r1_report.py`. Rebuild the manual with `python scripts/build-pdf.py`. The complete simulator assumptions and source hashes are stored in `reports/r1b/economy_results.json`.
