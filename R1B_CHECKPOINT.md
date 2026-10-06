# CHRONOCAIRN — R1B checkpoint

Time-Crime Horror Roleplaying — Riccardo Scaringi

Date: 6 October 2026. Status: R1 main-manual ledger corrected and tested; not a full-game freeze, not an Omnibus migration, not a publication certification.

## Exact recovery point

Repository: `ricscar2570/uchronies-and-treasures-cairn-hack`.
Main baseline: `32dd003b70a403d19de121f8156bffe009bd38d8` (R1 economy PDF full-width layout).
Recovered separate Omnibus branch: `integration/omnibus-rc1`, `54854d5313f978921291369b6d4650f175d09eb9`.
Development checkpoint: `development/r1-economy-2026-10-06`.

## What changed

Cash/Debt/Certificates remain separate. Interest is integer-safe and applied once after repayment/clemency. Paid mission receipts cannot be counted twice. Incurred liabilities are distinguished from goods not supplied. Payout bands, replacement bounties, the Trusted gross adjustment, Hero base salary, clemency timing and promotion pay timing are explicit. Old Warden pay and threshold values are removed. Personal Debt is not automatically inherited by a replacement character; an explicitly joint liability must be agreed.

The PDF reads the economy, design/FAQ, mini-campaign, R1 validation appendix and settlement worksheet from Markdown rather than maintaining separate copies. Other chapters still contain embedded manuscript text. Specific residual financial passages in those chapters were patched; full source migration is not claimed.

The final local review PDF is 77 A5 pages with 25 chapter bookmarks. All listed fonts are embedded; no text spans outside page boundaries were found. The only sparse page is the retained blank cover verso. These checks are not a printer-specific proof or a PDF/UA certification.

## Evidence and interpretation

Run `python -m unittest discover -s tests -v`: 42 tests in the local checkpoint, including exhaustive interest checks for principals $0-$100,000 and 10,000 deterministic random ledger invariants.

Run `python scripts/economy_sim.py`: five policies, 100,000 matched mission/expense paths each, 15 weeks, seed 42026. The isolated honest ledger reaches $700 Debt in 78.758% of paths. Hero salary reduces this to 40.149%; also granting briefed Trusted assignments reduces it to 30.112%; adding the stated clemency policy reduces it to 16.793%. These are model outputs under optimistic fixed assumptions, not observed play or predictions of player acceptance.

High-Loyalty salary was preserved, not secretly removed to recover a desired pressure percentage. Whether pressure should remain strong at high Loyalty remains a campaign-design/playtest question.

Measured JSON, CSV and sample traces are in `reports/r1b/`. `reference/r1-economy-validation.md` explains assumptions and limits. `scripts/r1_pdf_check.py` produces structural/content checks; inspect rendered pages separately.

## Resume here — do not start R2 yet

The next open step is **R1C: reconcile the separate Omnibus economy without losing its developed procedures**. Its $300 Cash / $1,200 Debt baseline, advancement, team funds and certificate handling are not equivalent to main's $500 / $500 rules. The recovered branch also lacks the complete A5 build/test toolchain named in its README. Recover the authorized complete Omnibus sources or deliberately reconstruct and test the missing build chain before claiming a regenerated Omnibus.

Do not relabel the 77-page main manual as the 322-page Omnibus. Do not flatten the Omnibus into the main edition or silently overwrite its advanced rules. Prepare an explicit rule-by-rule migration matrix and then update all its manifests, examples, tools and tests together.

After R1C and any agreed balancing decision, proceed to R2 Contamination, R3 procedural consistency, R4 player agency/scenarios, R5 campaign loop, R6 editorial. Existing contamination/Quirk, scenario-agency and broader cross-chapter issues are not closed by R1B.
