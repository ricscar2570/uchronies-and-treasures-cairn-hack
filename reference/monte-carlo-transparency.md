---
layout: default
title: Monte Carlo Transparency
parent: Reference
nav_order: 5
---

# Monte Carlo Transparency

This appendix collects the simulation evidence behind the game's numbers. It lives here, separate from the rules and the design notes, on purpose: these figures are how the design was *checked*, not a promise about what will happen at your table. The whole point of the economy and the contamination system is that the choices stay the players'. The simulations only confirm that the choices have weight.

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

The economic-pressure check used the same engine: at $800 pay against $900 expenses, the large majority of simulated agents took Zhou's first offer within the first few sessions; at a balanced $1,000 budget, only a minority did. The deficit, not the writing, is what makes corruption feel inevitable. Those exact offer-acceptance figures are evidence for the designer and are deliberately not printed in the player-facing text.

## Re-validating the Cairn-edition changes (this release)

Two changes in this edition postdate the original 300,000-campaign run and therefore need their own validation:

- **The honest-economy ceiling (D1):** honest income is capped at break-even at Recruit tier; only corruption produces structural surplus.
- **The accumulation penalty (D2):** each Quirk lowers the contamination save target by 1.

The original campaign simulator is not part of this repository, so it has not been re-run in full. What follows is a **subsystem** simulation of contamination and Quirk accumulation only, calibrated so that the no-penalty case reproduces the documented ~25% echo baseline. Treat the absolute numbers as direction, not gospel; the relative effect is the robust part.

| Configuration | Echo rate (15-session subsystem sim) |
|---|---|
| No accumulation penalty (calibrated baseline) | ~24% |
| D2 penalty, capped at -2 | ~32% |
| D2 penalty, capped at -3 (recommended) | ~34% |
| D2 penalty, uncapped (rule as written) | ~36% |

**Reading the result honestly.** The accumulation penalty does what it is meant to do: it makes every Quirk cost something and removes the "net-positive mutation" loophole. It also raises the echo rate by roughly 8 to 12 points. The uncapped rule lands near 36%; capping the penalty at -3 holds it closer to the documented "rare but real" target while preserving the intent. Which echo rate is correct is a design decision, and the authoritative figure for full campaign pacing requires re-running the original simulator (a Phase 4 task). The subsystem model assumes orange-zone exposure, the half-WIL damage cap, anti-rejection medicine taken, and between-session recovery; changing those assumptions moves the absolute numbers, not the direction.

## Method, in brief

Pure Python, standard library `random`, fixed seed (42) for reproducibility. Each trial draws 3d6 WIL, runs a fixed number of contamination checks per session across 15 sessions, applies the suit reduction and the half-WIL damage cap, triggers a Quirk on significant exposure (3+ damage after the cap), and ends in an echo on the 6th Quirk or on WIL reaching 0 from contamination. Recovery between sessions models therapy and the no-degrade effect of anti-rejection medicine. The script is short enough to re-run and re-tune as the rules settle.
