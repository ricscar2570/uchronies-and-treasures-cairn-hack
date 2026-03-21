# Build Scripts

## PDF Generation

Generates the complete KDP-ready manual PDF.

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

Output: `UeT_Final_Complete.pdf` in the current directory.

### What the script produces

- A5 format (148 x 210 mm), KDP-compatible
- Two-column layout with full-width tables where needed
- Cover page: navy/crimson/gold color scheme
- Automatic TOC with page numbers
- Running headers and footers
- Liberation Serif / Liberation Sans fonts (embedded)
- Approximately 59 pages

### Notes

Content is embedded directly in the script and has been copy-edited for print.
The markdown files in the repository are the source of truth for the web version;
the PDF script is maintained separately for print layout control.
