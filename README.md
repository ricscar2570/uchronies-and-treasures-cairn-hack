# Uchronies & Treasures - Cairn Hack

A time-crime horror roleplaying game by **Riccardo Scaringi**.

This repository is the canonical Markdown and rule-data source for the current **0.11.14-osr-conformance-suite** baseline and its five A5 publication profiles. The game text is not duplicated inside the A5 builder: every PDF is generated from the declared Markdown manifests and `_data/rules.yml`.

## Step 18 status

Step 18 implements the first P0/P1 block of the 10/10 revision plan: a canonical rule matrix and an explicit information hierarchy.

- 73 active mechanical/procedural rules now have stable canonical codes and one authoritative source location;
- the registry lives in `_data/canonical-rule-matrix.yml`;
- RULE, PRINCIPLE, EXAMPLE, and WARNING are visually distinct in the Large A5 profile;
- the front matter explains how the four labels work;
- the source markers remain non-rendering Markdown comments and are validated independently of pagination;
- `validate_canonical_rule_matrix.py` rejects duplicate IDs, missing canonical sections, orphan markers, and authoritative rules outside the Large profile;
- four unit tests cover registry uniqueness, exact marker/source alignment, active-profile coverage, and marker-set parity;
- Step 17 advancement consistency, OSR Gates A-D, profile separation, navigation, font, page-box, and PDF checks remain in force.

The information hierarchy is deliberately rendered only in **Large**. Other profiles preserve their Step 17 reader-facing output; their source preprocessing removes Step 18 marker comments and the Large-only legend before typesetting.

Automated OSR Gates A-D pass. **Gate E remains pending real human and blind-playtest evidence.** The source baseline is still 0.11.14; no claim is made that the unavailable 0.11.15 fieldwork delta is present.

## Build and release check

Install the pinned Python dependencies and the external PDF toolchain listed in `.github/workflows/build-pdf.yml`, then run:

```bash
python -m pip install -r scripts/requirements.txt
python scripts/release_check.py
```

The release gate validates the manuscript, advancement equivalence, OSR conformance, mutation coverage, publication manifests, PDF structure, fonts, A5 page boxes, navigation, profile separation, and Ghostscript rendering.

## Current A5 profiles

The profile index is `_data/publication-profiles-a5.yml`.

```text
dist/Uchronies & Treasures: Large.pdf
dist/Uchronies and Treasures Adventures.pdf
dist/Uchronies and Treasures Operational.pdf
dist/Uchronies and Treasures Table Reference Pack.pdf
dist/Uchronies and Treasures Design and Hacking Companion.pdf
```

- **Large** is the principal reader-facing rulebook. It excludes the adventures, table worksheets, extended FAQ, design notes, Monte Carlo methodology, and hacking guide.
- **Adventures** contains *The Chicago Loop* and *The First Four Weeks*.
- **Operational** preserves the long-form operational material and printable tools for audit and comprehensive use.
- **Table Reference Pack** contains the checklists, references, sheets, and worksheets.
- **Design and Hacking Companion** contains the extended FAQ, design notes, Monte Carlo transparency, and hacking guidance.

Build one profile directly with:

```bash
python scripts/build_a5_two_column.py --manifest _data/manual-a5-two-column.yml
```

Build all five with:

```bash
python scripts/build_a5_profiles.py
```

## Release integrity

- `CHECKSUMS_STEP18.sha256` records the five Step 18 package PDF hashes.
- `MANIFEST_STEP18.sha256` is the authoritative integrity manifest for this Step 18 repository snapshot.
- Historical manifests through Step 17 are retained only as evidence of prior checkpoints.

## Automated conformance

```bash
python scripts/validate_osr_conformance.py
python scripts/test_osr_regressions.py
python scripts/validate_advancement_consistency.py
python -m unittest discover -s tests -v
python scripts/validate.py
python scripts/validate_canonical_rule_matrix.py
python scripts/validate_a5_step18.py
```

The advancement consistency gate compares:

- `game-systems/economy.md`;
- `wardens-guide/campaign-management.md`;
- `_data/rules.yml`.

It verifies that operation credit does not require completion of the primary objective, that Recruit-to-Agent retains every canonical requirement, and that Agent-to-Veteran is four of six criteria rather than ten operations plus four more conditions.

## Source layout

- `_data/rules.yml`: canonical mechanical values;
- `_data/publication-profiles-a5.yml`: current A5 profile index and acceptance ranges;
- `_data/manual-*.yml`: profile manifests and archived historical manifests;
- `players-guide/`: player-facing rules and the compact Large example;
- `game-systems/`: economy, contamination, Quirks, and faction trackers;
- `setting/`: Las Vegas 2080 and adventure-site procedures;
- `wardens-guide/`: facilitation, campaign, opponents, and generators;
- `adventures/`: playable expeditions;
- `reference/`: reference material, sheets, appendices, and credits;
- `layout/a5/`: XeLaTeX publication style;
- `scripts/`: conformance, build, PDF, simulation, and release tooling;
- `tests/`: regression tests, including cross-chapter advancement mutations;
- `audit/`: machine-readable OSR and editorial evidence;
- `reports/a5-step18/`: generated Step 18 matrix, build, source-parity, and validation evidence.

## Rights and asset scope

Except where another source or exclusion is named, the game manuscript and canonical rule data are licensed under **CC BY-SA 4.0**. Original repository code is licensed under the **MIT License**.

The five A5 profiles use code-generated abstract covers and do not embed the unresolved legacy `img/cover.png`, `img/logo.svg`, or favicon files. Those files remain subject to `ASSET_PROVENANCE.md` and must not be reintroduced into a publication until cleared or replaced. See `LICENSE`, `THIRD_PARTY_NOTICES.md`, and `ASSET_PROVENANCE.md`.

## Remaining publication gates

Step 18 closes the canonical-rule-home and information-hierarchy blockers while preserving the Step 17 structural fixes. It does **not** close:

- import and reconciliation of the later 0.11.15 fieldwork repository;
- Gate E human and blind playtesting;
- post-playtest proofreading and rules freeze;
- legacy asset clearance or replacement;
- a printer-specific wraparound cover with bleed and calculated spine;
- printer OutputIntent/ICC requirements and a bound physical proof;
- full tagged-PDF/PDF-UA accessibility work.

See `PRODUCTION_BLOCKERS_STEP18.md` for the evidence required to close each remaining gate.
