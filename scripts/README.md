# Build Scripts

## PDF Generation

Generates the complete development manual PDF. Publication and human-playtest gates remain open.

### Requirements

```bash
pip install -r scripts/requirements.txt
```

On Ubuntu/Debian, also install Liberation fonts if not present:

```bash
sudo apt install fonts-liberation
```

On macOS: update the `BASE` variable at the top of `build-pdf.py` to your local font path.

### Usage

Run from the repository root:

```bash
python scripts/build-pdf.py
```

Output: `CHRONOCAIRN_Final_Complete.pdf` in the current directory.

### What the script produces

- A5 format (148 x 210 mm); printer-specific approval is not claimed
- Two-column layout with full-width tables where needed
- Cover page: navy/crimson/gold color scheme
- Automatic TOC with page numbers
- Running headers and footers
- Liberation Serif / Liberation Sans fonts (embedded)
- Page count depends on the current source and is reported by the build

### Notes

The generator mixes legacy embedded text with source-driven Markdown blocks; it is a development build, not a completed publication copyedit.
The markdown files in the repository are the source of truth for the web version;
the PDF script still contains legacy print text outside the R2 source-driven contamination chapter, introductory mini-campaign and diagnostic appendix. R3 must complete the remaining cross-format consistency audit.

## R2.1 regression and diagnostic

```bash
python -m unittest discover -s scripts -p 'test_contamination_r2.py' -v
python scripts/contamination_sim.py --runs 20000 --seed 42026
```

The diagnostic is synthetic evidence only. It adds no human playtest sessions. The JSON includes exact profiles, source hashes and cause-specific echo counts; an expedition/care cycle is not automatically a campaign week or a session.

### Repeat the PDF geometry check

```bash
pip install PyMuPDF==1.26.7
python scripts/check_pdf_r2.py CHRONOCAIRN_Final_Complete.pdf
```

The checkpoint was built with Python 3, ReportLab 4.4.9 and pypdf 5.9.0.
Geometry and selected text checks do not replace visual review or publication proofreading.
No font binaries are included in the downloadable source package; install fonts through the system as above.
