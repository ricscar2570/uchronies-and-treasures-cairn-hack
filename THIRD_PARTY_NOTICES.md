# Third-Party Notices

This file identifies direct sources and dependencies known to the project. It does not replace their complete upstream license texts. Transitive package versions are recorded in `Gemfile.lock`; Python build versions are pinned in `scripts/requirements.txt`.

## Cairn First Edition SRD v1.0

*Uchronies & Treasures* is based on *Cairn First Edition System Reference Document v1.0* by Yochai Gal.

- Source: `https://cairnrpg.com/first-edition/cairn-srd/`
- License: Creative Commons Attribution-ShareAlike 4.0 International
- License text: `https://creativecommons.org/licenses/by-sa/4.0/`
- Changes: new setting, economy, backgrounds, exploration procedures, contamination, Quirks, relics, faction trackers, advancement, campaign structure, examples, references, and adventures.

This is an independent production and is not affiliated with or endorsed by Yochai Gal or the Cairn project.

## Ucronie e Tesori

The project adapts *Ucronie e Tesori* by Riccardo Scaringi, identified by the author as licensed under Creative Commons Attribution 4.0 International.

- License: `https://creativecommons.org/licenses/by/4.0/`
- Changes: English-language Cairn conversion and substantial system, setting, campaign, example, reference, and editorial revisions.

## Direct Python Build Dependencies

These packages are installed separately and are not vendored into the repository.

| Package | Pinned build version | Upstream license |
|---|---:|---|
| ReportLab | 4.4.9 | BSD-style license; consult the package `LICENSE.txt` |
| pypdf | 5.9.0 | BSD-3-Clause |
| PyYAML | 6.0.3 | MIT |

A distributor who bundles these packages must include any notices required by the exact distributed package versions.

## Website Toolchain

The website uses Jekyll through the `github-pages` dependency set and the remote `just-the-docs` theme. Direct dependencies are listed in `Gemfile`; exact resolved versions are listed in `Gemfile.lock`.

- Jekyll: MIT License.
- Just the Docs: MIT License.
- Jekyll plugins and transitive Ruby gems: each remains under its own upstream license.

The repository does not relicense those packages. A built static site contains generated output and theme-derived presentation; a distributor of theme or gem source must preserve upstream notices as required.

## System Fonts Used by the PDF Builder

The A5 PDF builder requires **Noto Serif**, **Noto Sans**, and **Noto Sans Mono**. These fonts are installed by the build environment and are not vendored or redistributed as font files in this repository. The generated PDFs embed subset copies required to display the publication.

The Noto families are distributed under the SIL Open Font License 1.1. The continuous-integration workflow verifies the required family names before building, so the release does not silently substitute Liberation or DejaVu fonts on another system.

A distributor who packages font files separately must preserve the upstream license and notices. The PDF release gate verifies that every font used in the five publication profiles is embedded and subset.

## Visual Assets and Branding

The repository includes cover, logo, and favicon files. Their source and grant are not yet documented to publication standard. They are excluded from the manuscript and code license allocation until cleared.

See `ASSET_PROVENANCE.md` for the exact inventory and release blocker.
