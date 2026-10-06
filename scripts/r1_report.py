#!/usr/bin/env python3
"""Publish the measured R1 results and their limits into canonical Markdown."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    payload = json.loads((ROOT / 'reports/r1b/economy_results.json').read_text())
    results = payload['results']
    labels = {
        'isolated_honest': 'Isolated ledger, refuses Zhou',
        'isolated_first_offer': 'Isolated ledger, one completed courier job',
        'loyalty_honest': 'Loyalty progression and Hero salary',
        'loyalty_trusted_honest': 'Loyalty + briefed Trusted assignments',
        'loyalty_trusted_clemency_honest': 'Loyalty + Trusted assignments + clemency',
    }
    lines = ['---', 'layout: default', 'title: R1 Economy Verification',
             'parent: Reference', 'nav_order: 7', '---', '',
             '# R1 Economy Verification', '',
             '**R1B checkpoint, 6 October 2026.** This is a reproducible ledger and sensitivity study, not a forecast of player behaviour, proof of full-game balance, or a substitute for human playtesting.', '',
             f'The study runs **{payload["trials_per_scenario"]:,} paths per policy for 15 weeks**, seed **{payload["seed"]}**. Policies use the same generated mission outcomes and expenses, so differences are not caused by changing random samples. Week 10 and Week 15 results and a complete example trace for each policy are in the accompanying JSON/CSV reports.', '',
             '## Results at Week 15', '',
             '| Modelled policy | Median Cash | Median Debt | 90th percentile Debt | Ever reaches $700 Debt |',
             '|---|---:|---:|---:|---:|']
    for r in results:
        lines.append(f'| {labels[r["scenario"]]} | ${r["median_cash_week_15"]:,.0f} | ${r["median_debt_week_15"]:,.0f} | ${r["debt_p90_week_15"]:,.0f} | {100*r["ever_debt_700"]:.2f}% |')
    lines += ['', '## What the Earlier 78.8% Result Actually Meant', '',
        'The earlier result is reproducible for the **isolated ledger**: ordinary tier salaries, no Loyalty salary modifier, no Trusted assignments, no clemency and no side work. It must not be presented as the probability that an honest character under all published rules will reach Zhou\'s threshold. A percentage of modelled paths is not a probability of player acceptance.', '',
        'Including the existing Hero salary benefit changes the result substantially. Honest financial stability is possible, and in the favourable Loyalty-policy scenarios it is common by Week 15. This checkpoint preserves that benefit rather than quietly deleting it to force a desired percentage. Whether economic pressure should remain strong beyond high Loyalty is a design decision still requiring campaign-level testing.', '',
        'The first-offer case is deliberately optimistic about Zhou: it assumes the courier job is completed immediately and paid in full, without modelling time, discovery, danger or later leverage. It therefore demonstrates liquidity, not the true overall superiority of a corrupt strategy.', '',
        '## Reproducible Assumptions', '']
    lines += [f'{i}. {a}' for i, a in enumerate(payload['assumptions'], 1)]
    lines += ['', '## Measurement Details', '',
        'Debt percentiles use the nearest-rank definition. The first-threshold week is calculated only among paths that reach the threshold. A first-threshold median is not the week when half of all characters necessarily cross it.', '',
        'The model distinguishes being paid as an Agent during Week 15 from becoming eligible after Week 15. In the isolated baseline these rates are ' +
        f'{100*results[0]["agent_paid_week_15"]:.2f}% and {100*results[0]["eligible_for_agent_after_week_15"]:.2f}% respectively. The earlier label combined these different events.', '',
        'The arithmetic uses whole-dollar integer operations. Weekly interest is principal divided by 20, rounded upward, then added to principal. No binary floating-point multiplication is used. The four-week and eight-week published ledgers, repayment caps, clemency, receipt duplication, payout bands and promotion timing are covered by automated tests.', '',
        '## Edition Boundary', '',
        'These results and corrections apply to the **R1 main-manual/web line**, starting at $500 Cash and $500 Debt. The separate Omnibus RC1 source line has different starting values, advancement and credit procedures. It has not been silently overwritten or declared aligned by this checkpoint. Do not combine their economic procedures in one campaign.', '',
        '## Repeat the Check', '',
        'Run `python -m unittest discover -s tests -v`, then `python scripts/economy_sim.py`, then `python scripts/r1_report.py`. Rebuild the manual with `python scripts/build-pdf.py`. The complete simulator assumptions and source hashes are stored in `reports/r1b/economy_results.json`.', '']
    text = '\n'.join(lines)
    (ROOT / 'reference/r1-economy-validation.md').write_text(text)
    p = ROOT / 'reference/monte-carlo-transparency.md'
    old = p.read_text()
    a = old.index('## R1 economy subsystem validation')
    b = old.index('## Re-validating the Cairn-edition changes', a)
    replacement = '''## R1 economy subsystem validation

**Superseded scope statement:** the old 78.8% result describes an isolated ledger without high-Loyalty pay benefits, Trusted assignments, clemency or side work. It is not a whole-rules prediction for honest agents. The updated [R1 Economy Verification](r1-economy-validation.md) gives the rerun, five matched-path policies, actual assumptions, Week 10/15 outputs and the distinction between promotion eligibility and salary timing.

The original full-campaign simulation has not been recovered or rerun. Historical results below are not evidence that R1B or the complete current game is playtest-validated.

'''
    p.write_text(old[:a]+replacement+old[b:])
    p = ROOT / 'README.md'
    old = p.read_text()
    if '## R1B checkpoint' in old:
        old = old[:old.index('## R1B checkpoint')]
    p.write_text(old.rstrip()+'''

## R1B checkpoint — 6 October 2026

The main/manual economy is corrected through R1B. See [R1 Economy Verification](reference/r1-economy-validation.md) and [the settlement worksheet](reference/weekly-settlement-r1.md). This is not a full-game rules freeze or printer certification.

Build and repeat: `python -m unittest discover -s tests -v`; `python scripts/economy_sim.py`; `python scripts/r1_report.py`; `python scripts/build-pdf.py`.

The separate `integration/omnibus-rc1` branch has not been reconciled with this R1 economy. See `R1B_CHECKPOINT.md` before resuming. Do not substitute its $300 Cash / $1,200 Debt baseline for this line's $500 / $500.
''')
    (ROOT / 'scripts/README.md').write_text('''# CHRONOCAIRN build and R1 verification

Install the repository Python requirements and Liberation fonts. Run commands from the repository root.

- `python -m unittest discover -s tests -v`: mechanical and source regression tests.
- `python scripts/economy_sim.py`: 100,000 paths per each of five explicit policies; fixed seed 42026; 15 weeks. Use `--trials` for a smaller smoke check and `--output` to keep it separate from published results.
- `python scripts/r1_report.py`: regenerate the measured evidence appendix from the JSON results.
- `python scripts/build-pdf.py`: rebuild `CHRONOCAIRN_Final_Complete.pdf`.
- `python scripts/r1_pdf_check.py`: structural/content checks of the generated PDF (not visual certification).

The economy, design/FAQ, mini-campaign and R1 evidence/worksheet sections are sourced directly from Markdown through `r1_pdf_sources.py`. Other chapters still use the legacy embedded builder; their complete migration is not claimed. `r1_finalize_sources.py` is an idempotent guarded migration from the recovered 32dd003 checkpoint. Do not apply it to the Omnibus line.

The manual is a review build, not KDP/POD-ready by certification. The PDF contains embedded rendering fonts; font binaries are not redistributed in the delivery patch.
''')
    print('Measured R1B appendix and build notes generated.')


if __name__ == '__main__':
    main()
