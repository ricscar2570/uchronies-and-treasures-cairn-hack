# CHRONOCAIRN R2.2 — build and verification

All 26 manual chapters are rendered from the canonical Markdown paths in `_data/manual-chapters.json`. There is no parallel embedded rule/scenario manuscript. The PDF is a development consolidation, not a typesetter's final print approval.

## Reproduce

Run from the repository root. Tested locally with Python 3.13; the workflow is configured for Python 3.11. Install Liberation fonts through the operating system; font binaries are not distributed in source archives.

```bash
sudo apt install fonts-liberation
python -m pip install -r scripts/requirements.txt
python scripts/contamination_sim.py --runs 20000 --seed 42026 --output reports/r22-contamination-reproduction.json
python scripts/build-pdf.py
python scripts/build_sheets_r22.py
python -m unittest discover -s scripts -p 'test_*.py' -v
python scripts/check_pdf_r22.py CHRONOCAIRN_Final_Complete.pdf
```

On macOS, set `BASE` in `build-pdf.py` to the installed Liberation font directory. The PDF defaults to the working directory; `--output` accepts another path. Sheet files go to `downloads/`, overridable with `--output-dir`.

## Evidence and scope

`test_contamination_r2.py` retains 29 tests; its source-wiring assertion now checks the manifest rather than obsolete literal calls. `test_procedures_r22.py` adds 49 tests: monetary examples, Loyalty timing, Instability bounds, damage/Scars, ammunition, text invariants, source provenance, PDF navigation and sample form round-trip.

`procedures_r22.py` is an executable reference for declared examples, **not a coupled campaign simulator**. Its whole-dollar bounty helper deliberately accepts multiples of ten only; this is an input limitation of the example helper, not a new game restriction.

The contamination reproduction must match `reports/r2-contamination.json` exactly. Its 12 rows total 240,000 synthetic paths. No human sessions are added. `economy_sim.py` is an unchanged historical R1 diagnostic and does **not** implement the new Loyalty benefits; its results do not validate R2.2 economics.

## Output and visual review

The PDF is A5, body 8 pt, with mixed column/full-width layouts, 26 chapter destinations, 299 hierarchical bookmarks, a linked contents page and 57 links. Liberation fonts are embedded. Three separate one-page A4 PDFs provide character, accounting and mission forms (43, 109 and 10 fields). The accounting form is not an automatic spreadsheet.

`check_pdf_r22.py` checks bounds, selected forbidden/required text, internal destinations and all 26 source hashes. It cannot prove every rule interpretation, PDF/UA compliance, print-provider approval or human usability. Render with Poppler or PDFium and inspect all pages; `reports/r22-visual-review.json` records this checkpoint's review.

## Packaging

```bash
python scripts/package_r22.py --source-commit <exact-github-commit-sha>
```

The ZIP contains the source repository, the built manual, the three forms, reports, `SOURCE_COMMIT.txt`, and individual SHA-256 hashes. Font files, transport parts, caches, .git and old generated archive files are excluded. A source file's presence in the package does not resolve its copyright license; see the explicit script-licensing qualification in the diagnostic appendix.
