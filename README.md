---
layout: default
title: Home
nav_order: 1
permalink: /
---

# CHRONOCAIRN
{: .no_toc }

**Time-Crime Horror Roleplaying**

Riccardo Scaringi

**A Cairn hack of temporal heists and financial desperation.**

*"Breaking Bad meets Cairn meets Looper"*

---

You play as agents of the Temporal Division, a government agency in Las Vegas 2080. You enter unstable time zones to recover artifacts, neutralize threats, and maintain the timeline. The pay is terrible. The rent is worse. And Madame Zhou is always ready with an offer you can't refuse.

The game uses the [Cairn](https://cairnrpg.com) engine by Yochai Gal. Character creation takes 15 minutes. Combat is fast and deadly. The real danger isn't the bullets: it's the debt.

The full text is licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Based on [Cairn](https://cairnrpg.com) by Yochai Gal (CC-BY-SA 4.0) and [CHRONOCAIRN](https://github.com/ricscar2570/ucronie-e-tesori) by Riccardo Scaringi (CC BY 4.0).

Design, writing and simulation by Riccardo Scaringi. The R1 economy has a reproducible, assumption-bound ledger simulation, not full-game or human-playtest validation; the method and limits are documented in the [Monte Carlo Transparency](reference/monte-carlo-transparency.md) appendix.

## R1B checkpoint — 6 October 2026

The main/manual economy is corrected through R1B. See [R1 Economy Verification](reference/r1-economy-validation.md) and [the settlement worksheet](reference/weekly-settlement-r1.md). This is not a full-game rules freeze or printer certification.

Build and repeat: `python -m unittest discover -s tests -v`; `python scripts/economy_sim.py`; `python scripts/r1_report.py`; `python scripts/build-pdf.py`.

The separate `integration/omnibus-rc1` branch has not been reconciled with this R1 economy. See `R1B_CHECKPOINT.md` before resuming. Do not substitute its $300 Cash / $1,200 Debt baseline for this line's $500 / $500.
