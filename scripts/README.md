# CHRONOCAIRN R2.2.1 — build and verification

All 26 chapters come from `_data/manual-chapters.json`. The historical filename `build_sheets_r22.py` now generates the current R2.2.1 aids; `r22-build-sources.json` is the rolling source-hash record retained for compatibility with the original regression tests. Its edition field states the actual version.

Run from the repository root with Python 3.11 or later and installed Liberation fonts:

```bash
python -m pip install -r scripts/requirements.txt
python scripts/build-pdf.py
python scripts/build_sheets_r22.py
python scripts/build_omnibus_r221.py
python -m unittest discover -s scripts -p 'test_*.py' -v
python scripts/check_r221.py
python scripts/package_r221.py --source-commit <exact-github-commit-sha>
```

On Debian/Ubuntu, `sudo apt install fonts-liberation` supplies the fonts. Font files are not shipped. The complete manual is `CHRONOCAIRN_Final_Complete.pdf`; the digital collection is `CHRONOCAIRN_OMNIBUS_R2_2_1.pdf`; separate current forms are `downloads/CHRONOCAIRN_R2_2_1_*.pdf`.

## Regressions and evidence

101 tests: 29 contamination regressions, 49 R2.2 regressions (the artifact filenames only are updated), and 23 R2.2.1 corrective/round-trip guards. Rules engines and the ten-week ledger remain unchanged. `check_r221.py` checks all 162 fields, separately and merged: fill/save/reopen, values in MuPDF and pypdf, reset, geometry, names, tooltips and row tab declarations. No automatic spreadsheet calculations are embedded.

For a fresh 240,000-path contamination diagnostic, without changing the historical report:

```bash
python scripts/contamination_sim.py --runs 20000 --seed 42026 --output reports/r221-contamination-reproduction.json
```

Its parsed JSON must equal `reports/r2-contamination.json`. This reproduces a frozen subsystem, not human play or a coupled faction/economy campaign. `economy_sim.py` remains historical R1 evidence.

## Rendering and limits

Render the final Omnibus with Poppler and inspect it. For sample filled forms, use Poppler and PDFium with form rendering enabled. `check_r221.py --sample-dir <directory>` writes disposable filled/reset samples: these contain synthetic test strings and are not worked game ledgers. Do not include them as blank player sheets.

Testing both renderers is not testing the UI of Acrobat, Chromium, Firefox, Preview or a mobile app. Tagging/reading-order certification, native-speaker proofing, playtests and rights clearance remain separate. Licensing scope is in `docs/LICENSING_SCOPE.md`; no new script license has been selected on the author's behalf.

The package excludes fonts, caches, temporary transport and superseded PDF outputs, but retains the complete buildable source tree and historical text reports. `SOURCE_COMMIT.txt` plus SHA-256 manifest identify the exact committed source and actual built files. A packet is not automatically a public release.
