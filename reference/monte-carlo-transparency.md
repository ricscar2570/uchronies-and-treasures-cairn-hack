---
layout: default
title: Monte Carlo Transparency
parent: Reference
nav_order: 5
---

# Monte Carlo Transparency

This appendix collects the simulation evidence behind the game's numbers. It lives here, separate from the rules and the design notes, on purpose: these figures are how the design was *checked*, not a promise about what will happen at your table. The whole point of the economy and the contamination system is that the choices stay the players'. The simulations describe consequences under explicit assumptions; they cannot establish what choices feel like at a real table.

## Why this is an appendix and not a sales pitch

Early drafts put the headline percentages in the marketing and the design commentary: "92% of agents accept Zhou's first offer by session 4." That framing is corrosive. Told in advance that the system will break them, players stop treating the dilemma as a real decision and start treating it as a cutscene. So the percentages moved here, where a Warden or a designer can audit the reasoning without it pre-spoiling the table's agency.

## The original validation (UeT v2.2.3, Italian edition)

The Italian edition was balanced with **300,000 simulated 15-session campaigns**. The early rule set produced a death spiral; a small set of mechanical adjustments pulled it back to a survivable but genuinely lethal baseline.

| Metric | Before adjustment | After adjustment |
|---|---|---|
| Total party kill rate | 53.8% | 3.0% |
| Echo transformation rate | 71.3% | 24.9% |
| Average character progression | level 1.8 | level 3.6 |

The decisive fix was capping contamination damage at half current WIL (rounded up), which turns a runaway spiral into a slow, decelerating decline. The contamination damage die (d4), the suit reduction (1 point), and the zone intensity table all derive from this work.

The original economic-pressure check used a single negative balance and an earlier bonus model. R1 supersedes that accounting model. Its historical result is development context, not evidence for the current rules. The current edition treats Cash, Debt, and Certificates separately and no longer claims that corruption is mathematically inevitable.

## R1 economy subsystem diagnostic (historical model)

R1 was checked with **100,000 simulated 15-week ledgers** using fixed seed 42026. This is a pressure test, not a forecast of player behavior. Baseline assumptions: one field mission per week, 65% mission success, one non-cumulative performance band, the published unexpected-expense table, a $200 emergency Cash reserve before voluntary repayments, and Agent promotion after 8 successful missions.

| Strategy | Median Debt, Week 15 | 90th Percentile Debt | Ever Reaches $700 Debt | Median First $700 Week |
|---|---:|---:|---:|---:|
| Honest | $622 | $2,568 | 78.8% | 7 |
| Accept first Zhou offer | $0 | $308 | 78.9% before accepting | 7 |

The reproducible historical model is `scripts/economy_sim.py`. **These R1 statistics do not validate R2.2 economics:** the model does not implement the clarified Loyalty band improvement and Hero base-pay benefit. R2.2 verifies the ten-week worked ledger separately; a new coupled economy/faction simulation and human observations remain open. Do not present the 78.8% result as a current-edition campaign prediction.

## R2.1 contamination diagnostic

The former subsystem script described itself as calibrated to a historical echo rate. R2.1 instead derives periodic checks from stated zone exposure and reports its actual results without fitting them to that number. Historical Italian-edition figures above have not been independently reproduced and are not validation of this edition.

The canonical accumulation penalty is capped at -3. Quirks require 3+ damage from one hit after temporal protection and the half-current-WIL cap. Echoes from WIL 0 and from a sixth Quirk are recorded separately. Ordinary Armor does not protect against contamination.

### Ten expedition/care cycles

| Exposure per expedition | Checks | Mean Quirks, all starters | Echo loss | Care |
|---|---|---|---|---|
| Yellow, 4 hours | 0 | 0.00 | 0.00% | d6 |
| Yellow, 8 hours | 1 | 1.21 | 0.21% | d6 |
| Orange, 6 hours | 1 | 1.21 | 0.14% | d6 |
| Red, 6 hours | 2 | 2.33 | 15.01% | d6 |
| Red, 9 hours | 3 | 2.61 | 59.22% | d6 |
| Black, 1 hour | 1 | 2.55 | 5.01% | d6 |
| Red, 6h, heavy suit | 2 | 0.00 | 2.14% | d6 |
| Yellow, 8h, no treatment | 1 | 0.83 | 58.54% | None |

Each row uses 20,000 trials, fresh 3d6 WIL, no starting Quirks and standard suit except the heavy-suit row. Every cycle starts after adequate Green rest. Medicine is supplied. The d6 rows include one actually completed medical treatment before the next expedition; this is not automatic healing at session end. Differences between identical check schedules reflect Monte Carlo sampling, not a hidden Orange/Yellow modifier.

**These cycles are not ten weeks or ten sessions by definition.** Division care requires its full week, or 3 days and d8 at Loyalty 7+; black-market d6 care requires 2 days and payment. The diagnostic does not model these scheduling and financial constraints. A mission spread across several sessions does not generate extra checks merely because the real-world session changed.

### What the averages do not say

The all-starter mean includes Quirks acquired before an echo, including a sixth. It is not the number carried by a surviving character. In the 6-hour Red row the survivor mean is 2.24; 11.02% of starters became echoes through WIL 0 and 3.99% through a sixth Quirk. In the 9-hour Red row the survivor mean is 2.62, with 52.76% WIL-zero echoes and 6.46% sixth-Quirk echoes. More prolonged exposure mainly increases loss; it does not reliably deliver 3-4 playable Quirks.

The low mean in the no-treatment row is not safety: WIL exhaustion removes characters before they accumulate many mutations. Heavy protection prevents the d4-zone mutation trigger but not WIL-zero loss. Black exposure is not safer than Red: the displayed rows contain different numbers of checks and hours.

### Fifteen-cycle sensitivity

Using the 6-hour Red schedule, completed d6 treatment and 20,000 trials per configuration: no Quirk penalty gives 24.28% echo loss; cap -2 gives 32.95%; canonical cap -3 gives 34.66%; historical uncapped -5 gives 35.67%. The cap alone is not a solution to excessive exposure. These absolute rates are not universal campaign predictions.

### Reproduction and open evidence

Run `python scripts/contamination_sim.py --runs 20000 --seed 42026` from the repository root. The default output is `reports/r2-contamination.json` plus a Markdown report. It records profile seeds, survivor denominators, cause-specific losses, WIL bands, first-Quirk timing and source hashes. Rules values live in `_data/contamination.json`; the tested resolution procedure is `scripts/contamination_rules.py`.

No tactical choices, combat, Quirk-specific secondary effects, surgery, retirement, missed medicine, special bonuses, or the coupled economy are simulated. Averages cannot validate fear, comprehensibility or agency. The former 3-4-Quirk Red pacing target remains unestablished; the human protocol is not rewritten to make it pass. Human sessions added by this checkpoint: **0**.

## Locate and Reproduce the Evidence

**Edition:** CHRONOCAIRN R2.2.1, corrective consolidation, 7 October 2026. The unchanged contamination diagnostic comes from the verified **R2.1 source commit** below, run on 6 October 2026 with seed 42026 and 20,000 paths per profile. R2.2.1 adds no human sessions. The underlying R2.2 arithmetic and R2.1 contamination engine are unchanged.

- [Repository](https://github.com/ricscar2570/uchronies-and-treasures-cairn-hack)
- [Exact R2.1 diagnostic source](https://github.com/ricscar2570/uchronies-and-treasures-cairn-hack/tree/d4b13099c8b530b0d717396df72c5f41aa9e197b)
- [R2.1 machine-readable results](https://github.com/ricscar2570/uchronies-and-treasures-cairn-hack/blob/d4b13099c8b530b0d717396df72c5f41aa9e197b/reports/r2-contamination.json)

Source commit: `d4b13099c8b530b0d717396df72c5f41aa9e197b`. The game text declares **CC BY-SA 4.0**. The root `LICENSE` instead describes the site's **GPLv3 theme**; a separate, unambiguous grant for the diagnostic scripts has not been identified. Code-licensing clarification remains an authorial publication task. No new blanket license is invented here; third-party dependencies retain their own licenses. The delivery archive includes source hashes and its source-commit record. This records provenance, not commercial or human-play validation.

The Scars clarification was checked against the [Cairn first-edition SRD](https://cairnrpg.com/first-edition/cairn-srd/): damage taken indexes the table. R2.2 explicitly states after-Armor damage and the cap at entry 12 rather than adding a random d12 selection.

R2.2.1 records licensing scope and the pending authorial decision in [Licensing scope](https://github.com/ricscar2570/uchronies-and-treasures-cairn-hack/blob/development/r221-corrective-20261007/docs/LICENSING_SCOPE.md). Its correction and PDF-form checks are documented in [R2.2.1 checkpoint](https://github.com/ricscar2570/uchronies-and-treasures-cairn-hack/blob/development/r221-corrective-20261007/docs/R221_CHECKPOINT_2026-10-07.md). These checks are not native-speaker proofing, an accessibility certification, or testing in every PDF reader.
