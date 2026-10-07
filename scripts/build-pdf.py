"""
CHRONOCAIRN: development manual
A5 mixed full-width / two-column layout
All manual chapters are rendered from the canonical Markdown manifest.
No embedded duplicate rule or scenario text remains in this builder.
"""

import os
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    NextPageTemplate, Table, TableStyle, HRFlowable, KeepTogether, CondPageBreak
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re

# Font path (Linux default). On macOS change to your Liberation fonts directory.
# Install on Ubuntu/Debian: sudo apt install fonts-liberation
BASE = "/usr/share/fonts/truetype/liberation/"
import os as _os
if not _os.path.isdir(BASE):
    # Try common macOS Homebrew path
    _mac = "/opt/homebrew/share/fonts/liberation-fonts/"
    if _os.path.isdir(_mac):
        BASE = _mac
    else:
        raise FileNotFoundError(
            f"Liberation fonts not found at {BASE}\n"
            "Install with: sudo apt install fonts-liberation\n"
            "Or set BASE manually at the top of this script."
        )
pdfmetrics.registerFont(TTFont("Ser",    BASE+"LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("SerB",   BASE+"LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("SerI",   BASE+"LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("SerBI",  BASE+"LiberationSerif-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("San",    BASE+"LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("SanB",   BASE+"LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("SanI",   BASE+"LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Mono",   BASE+"LiberationMono-Bold.ttf"))
pdfmetrics.registerFontFamily("Ser", normal="Ser", bold="SerB",
    italic="SerI", boldItalic="SerBI")

# ── COLORS ───────────────────────────────────────────────────────────────────
CRIMSON  = colors.HexColor("#8B0000")
AMBER    = colors.HexColor("#C0392B")
NAVY     = colors.HexColor("#1a1a2e")
GOLD     = colors.HexColor("#C9A96E")
CREAM    = colors.HexColor("#FDF6EC")
LGREY    = colors.HexColor("#F5F5F0")
SLATE    = colors.HexColor("#2C3E50")
MGREY    = colors.HexColor("#CCCCCC")
WHITE    = colors.white
BLACK    = colors.black

# ── GEOMETRY ─────────────────────────────────────────────────────────────────
PW, PH = A5
ML, MR, MT, MB = 14*mm, 12*mm, 14*mm, 14*mm
GAP  = 4*mm
CW   = (PW - ML - MR - GAP) / 2   # ~59mm per column
FW   = PW - ML - MR               # ~122mm full width

# ── STYLES ───────────────────────────────────────────────────────────────────
S = ParagraphStyle

STYLES = {
  "h1":  S("h1",  fontName="SanB",  fontSize=13, textColor=CRIMSON,
           spaceBefore=8, spaceAfter=4, leading=17, keepWithNext=1),
  "h2":  S("h2",  fontName="SanB",  fontSize=10, textColor=NAVY,
           spaceBefore=6, spaceAfter=3, leading=13, keepWithNext=1),
  "h3":  S("h3",  fontName="SanB",  fontSize=8.5, textColor=SLATE,
           spaceBefore=4, spaceAfter=2, leading=12, keepWithNext=1),
  "body":S("body",fontName="Ser",   fontSize=8,  textColor=BLACK,
           alignment=TA_JUSTIFY, spaceBefore=1, spaceAfter=1, leading=11.5, allowWidows=0, allowOrphans=0),
  "bi":  S("bi",  fontName="SerI",  fontSize=8,  textColor=BLACK,
           alignment=TA_JUSTIFY, spaceBefore=1, spaceAfter=1, leading=11.5, allowWidows=0, allowOrphans=0),
  "bul": S("bul", fontName="Ser",   fontSize=8,  textColor=BLACK,
           leftIndent=9, firstLineIndent=-6,
           spaceBefore=1, spaceAfter=1, leading=11),
  "note":S("note",fontName="SerI",  fontSize=7.5, textColor=NAVY,
           leftIndent=5, rightIndent=3, alignment=TA_JUSTIFY,
           spaceBefore=3, spaceAfter=3, leading=10.5),
  "th":  S("th",  fontName="SanB",  fontSize=7,  textColor=WHITE,
           alignment=TA_CENTER, leading=9),
  "td":  S("td",  fontName="Ser",   fontSize=7.5, textColor=BLACK,
           alignment=TA_LEFT,   leading=10),
  "tdc": S("tdc", fontName="Ser",   fontSize=7.5, textColor=BLACK,
           alignment=TA_CENTER, leading=10),
  "stat":S("stat",fontName="SerB",  fontSize=8,  textColor=NAVY,
           spaceBefore=1, spaceAfter=1, leading=11),
  "foot":S("foot",fontName="San",   fontSize=6.5, textColor=GOLD,
           alignment=TA_CENTER),
  "hdr": S("hdr", fontName="SanI",  fontSize=6.5, textColor=GOLD),
  "toc0":S("toc0",fontName="SanB",  fontSize=8.5, textColor=NAVY,
           leftIndent=0, spaceBefore=0, spaceAfter=1, leading=10),
  "toc1":S("toc1",fontName="Ser",   fontSize=7.5, textColor=SLATE,
           leftIndent=9,  spaceAfter=2,  leading=11),
  "toc2":S("toc2",fontName="SerI",  fontSize=7,   textColor=SLATE,
           leftIndent=16, spaceAfter=1,  leading=10),
  "covertitle": S("covertitle", fontName="SanB", fontSize=22,
           textColor=WHITE, alignment=TA_CENTER, leading=28),
  "coversub":   S("coversub",   fontName="SanI", fontSize=9.5,
           textColor=GOLD,  alignment=TA_CENTER, leading=14),
  "covertag":   S("covertag",   fontName="SerI", fontSize=8.5,
           textColor=WHITE, alignment=TA_CENTER, leading=13),
}

# ── HELPERS ──────────────────────────────────────────────────────────────────

def sp(h=3): return Spacer(1, h*mm)
def pb():    return PageBreak()
def npb():   return NextPageTemplate("TwoCol")
def nfull(): return NextPageTemplate("Full")

def rule(c=GOLD, t=0.5):
    return HRFlowable(width="100%", thickness=t, color=c,
                      spaceBefore=2*mm, spaceAfter=2*mm)

ROOT = __import__('pathlib').Path(__file__).resolve().parents[1]
CHAPTER_CONFIG = __import__('json').loads((ROOT / '_data/manual-chapters.json').read_text())
CHAPTER_IDS = {item['path']: 'chapter-' + str(i) for i, item in enumerate(CHAPTER_CONFIG['chapters'])}
CURRENT_SOURCE = ''


def md(text):
    """Escape text, preserve supported inline styling, and resolve real links."""
    from xml.sax.saxutils import escape, quoteattr
    from pathlib import PurePosixPath
    import posixpath
    links = []
    def link(match):
        label, target = match.groups()
        if target.startswith(('https://', 'http://', 'mailto:')):
            href = target
        else:
            target_path = target.split('#', 1)[0]
            resolved = posixpath.normpath(str(PurePosixPath(CURRENT_SOURCE).parent / target_path))
            href = '#' + CHAPTER_IDS[resolved] if resolved in CHAPTER_IDS else None
        value = ('<link href=' + quoteattr(href) + ' color="#1a1a2e"><u>' + escape(label) + '</u></link>') if href else escape(label)
        links.append(value)
        return 'ZZLINKTOKEN' + str(len(links)-1) + 'ZZ'
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, str(text))
    text = escape(text).replace('\\|', '|')
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'`(.+?)`', r'<font name="Mono">\1</font>', text)
    text = text.replace('\u2014', ' - ')
    for i, value in enumerate(links):
        text = text.replace('ZZLINKTOKEN' + str(i) + 'ZZ', value)
    return text

def p(text, style="body"):
    return Paragraph(md(text), STYLES[style])

def b(text):
    return Paragraph("<bullet>&bull;</bullet>" + md(text), STYLES["bul"])

def note(text):
    return KeepTogether([
        Table([[Paragraph(md(text), STYLES["note"])]],
            colWidths=[CW-3*mm],
            style=TableStyle([
                ("BOX",         (0,0),(-1,-1), 0.5, GOLD),
                ("LEFTPADDING", (0,0),(-1,-1), 5),
                ("RIGHTPADDING",(0,0),(-1,-1), 5),
                ("TOPPADDING",  (0,0),(-1,-1), 4),
                ("BOTTOMPADDING",(0,0),(-1,-1),4),
                ("BACKGROUND",  (0,0),(-1,-1), CREAM),
            ]))
    ])

def fullnote(text):
    return KeepTogether([
        Table([[Paragraph(md(text), STYLES["note"])]],
            colWidths=[FW-3*mm],
            style=TableStyle([
                ("BOX",         (0,0),(-1,-1), 0.5, GOLD),
                ("LEFTPADDING", (0,0),(-1,-1), 6),
                ("RIGHTPADDING",(0,0),(-1,-1), 6),
                ("TOPPADDING",  (0,0),(-1,-1), 5),
                ("BOTTOMPADDING",(0,0),(-1,-1),5),
                ("BACKGROUND",  (0,0),(-1,-1), CREAM),
            ]))
    ])

class CheckedTable(Table):
    """Reject a full-width table accidentally placed in a narrow frame."""
    def wrap(self, availWidth, availHeight):
        if sum(self._argW) > availWidth + 0.1:
            raise ValueError(f"Table width {sum(self._argW):.2f} exceeds frame {availWidth:.2f}")
        return super().wrap(availWidth, availHeight)


def T(headers, rows, widths, full=False):
    """Build a styled table."""
    base = FW if full else CW
    data = [[Paragraph(md(h), STYLES["th"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(md(str(c)), STYLES["td"]) for c in row])
    ts = TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  SLATE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LGREY]),
        ("GRID",          (0,0),(-1,-1), 0.25, MGREY),
        ("TOPPADDING",    (0,0),(-1,-1), 2),
        ("BOTTOMPADDING", (0,0),(-1,-1), 2),
        ("LEFTPADDING",   (0,0),(-1,-1), 3),
        ("RIGHTPADDING",  (0,0),(-1,-1), 3),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ])
    return CheckedTable(data, colWidths=widths, style=ts, hAlign="LEFT", repeatRows=1)


def clean_markdown(path):
    text = (ROOT / path).read_text()
    text = re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S)
    text = re.sub(r"<details\b.*?</details>", "", text, flags=re.S)
    text = re.sub(r"^\{:[^}]*\}\s*$", "", text, flags=re.M)
    return text


def table_widths(rows, width):
    n = len(rows[0])
    headers = [c.lower() for c in rows[0]]
    if n == 2:
        weights = [.16, .84] if headers[0] in ('d6','d10','d12','2d6','damage taken') else [.36,.64]
    elif n == 3:
        weights = [.08,.28,.64] if headers[0] in ('d6','d10','d12') else [.29,.22,.49]
    elif n == 5:
        weights = [.34,.165,.165,.165,.165]
    elif n == 6:
        weights = [.075,.185,.185,.185,.185,.185]
    else:
        weights = [1/n]*n
    return [width*w for w in weights]


def markdown_chapter(path, layout='Full'):
    """Compile one canonical chapter; rule text is never embedded in this code."""
    global CURRENT_SOURCE
    CURRENT_SOURCE = path
    text = clean_markdown(path)
    lines, out, paragraph = text.splitlines(), [], []
    headings = [len(m.group(1)) for m in re.finditer(r'^(#{1,6}) +', text, re.M)]
    base_level = min(headings) if headings else 1
    heading_count = 0
    width = FW if layout == 'Full' else CW
    def flush():
        if paragraph:
            out.append(p(' '.join(paragraph)))
            paragraph.clear()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            flush(); i += 1; continue
        if line.startswith('|'):
            flush(); rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [c.strip().replace('\\|', '|') for c in re.split(r'(?<!\\)\|', lines[i].strip().strip('|'))]
                if not all(re.fullmatch(r'[:\- ]+', c) for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                if any(len(row) != len(rows[0]) for row in rows):
                    raise ValueError(f'Inconsistent table at {path}:{i}')
                table = T(rows[0], rows[1:], table_widths(rows, width), full=layout=='Full')
                _, height = table.wrap(width, PH-MT-MB)
                # Keeps Speech result 10 with its table, but permits long rules tables to split.
                if height < (PH-MT-MB)*.55:
                    block = [table]
                    if out and isinstance(out[-1], Paragraph) and hasattr(out[-1], '_bookmark_name'):
                        block.insert(0, out.pop())
                    out += [KeepTogether(block), sp(2)]
                else:
                    out += [table, sp(2)]
            continue
        if line.startswith('#'):
            flush(); level = min(2, max(0, len(line)-len(line.lstrip('#'))-base_level))
            title = line.lstrip('# ')
            para = p(title, ['h1','h2','h3'][level])
            para._outline_level = level
            para._bookmark_name = CHAPTER_IDS[path] if heading_count == 0 else CHAPTER_IDS[path]+'-h'+str(heading_count)
            out.append(para); heading_count += 1
        elif line.startswith('- '):
            flush(); out.append(b(line[2:]))
        elif re.match(r'^\d+\. ', line):
            flush(); out.append(p(line, 'bul'))
        elif line.startswith('>'):
            flush()
            quote = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                q = lines[i].strip()[1:].strip()
                if q: quote.append(q)
                i += 1
            if quote: out.append(p(' '.join(quote), 'note'))
            continue
        elif line.startswith('```'):
            flush(); i += 1; code=[]
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code.append(lines[i]);i += 1
            for code_line in code: out.append(p('`'+code_line+'`'))
        elif line != '---':
            paragraph.append(line)
        i += 1
    flush()
    return out

def statblock(text):
    return Paragraph(md(text), STYLES["stat"])

def h1(t): return Paragraph(md(t), STYLES["h1"])
def h2(t): return Paragraph(md(t), STYLES["h2"])
def h3(t): return Paragraph(md(t), STYLES["h3"])

# ── DOC CLASS ────────────────────────────────────────────────────────────────

class UeTDoc(BaseDocTemplate):
    def __init__(self, fn):
        super().__init__(fn, pagesize=A5,
            leftMargin=ML, rightMargin=MR,
            topMargin=MT, bottomMargin=MB)
        self._chapter = ""
        self.toc = TableOfContents()
        self.toc.levelStyles = [STYLES["toc0"], STYLES["toc1"], STYLES["toc2"]]
        self._setup()

    def _setup(self):
        cov = Frame(0, 0, PW, PH, leftPadding=0, rightPadding=0,
                    topPadding=0, bottomPadding=0, id="cov")
        blk = Frame(ML, MB, FW, PH-MT-MB, id="blk")
        toc = Frame(ML, MB, FW, PH-MT-MB, id="toc")
        L   = Frame(ML,           MB, CW, PH-MT-MB, id="L", leftPadding=0, rightPadding=0)
        R   = Frame(ML+CW+GAP,    MB, CW, PH-MT-MB, id="R", leftPadding=0, rightPadding=0)
        F   = Frame(ML,           MB, FW, PH-MT-MB, id="F", leftPadding=0, rightPadding=0)

        self.addPageTemplates([
            PageTemplate(id="Cover", frames=[cov]),
            PageTemplate(id="Blank", frames=[blk], onPage=self._pg_blank),
            PageTemplate(id="TOC",   frames=[toc],  onPage=self._pg_toc),
            PageTemplate(id="TwoCol",frames=[L,R],   onPageEnd=self._pg_run),
            PageTemplate(id="Full",  frames=[F],     onPageEnd=self._pg_run),
        ])

    def afterFlowable(self, f):
        from xml.sax.saxutils import escape
        if isinstance(f, Paragraph) and hasattr(f, '_bookmark_name'):
            title = f.getPlainText()
            level = f._outline_level
            if level == 0:
                self._chapter = title
            self.canv.bookmarkPage(f._bookmark_name)
            self.canv.addOutlineEntry(title, f._bookmark_name, level=level, closed=level>0)
            if level == 0:
                self.notify('TOCEntry', (0, escape(title), self.page, f._bookmark_name))

    def _pg_blank(self, c, d): pass

    def _pg_toc(self, c, d):
        self._footer(c, d, show=False)

    def _pg_run(self, c, d):
        self._footer(c, d, show=True)

    def _footer(self, c, d, show=True):
        c.saveState()
        c.setStrokeColor(GOLD); c.setLineWidth(0.4)
        c.line(ML, MB-3.5*mm, PW-MR, MB-3.5*mm)
        c.setFont("San", 6.5); c.setFillColor(GOLD)
        c.drawCentredString(PW/2, MB-7*mm, str(d.page))
        if show and self._chapter:
            c.setFont("SanI", 6)
            c.drawString(ML, MB-7*mm, self._chapter[:29])
            c.drawRightString(PW-MR, MB-7*mm, "CHRONOCAIRN")
        c.restoreState()


# ── COVER BUILDER ────────────────────────────────────────────────────────────

def make_cover_pdf():
    from reportlab.pdfgen import canvas as cv
    import io
    buf = io.BytesIO()
    c = cv.Canvas(buf, pagesize=A5)
    mm_pt = 72/25.4

    # Background: cover image stretched to full A5 page
    import os as _os
    _cover_path = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "img", "cover.png")
    if _os.path.exists(_cover_path):
        c.drawImage(_cover_path, 0, 0, PW, PH, preserveAspectRatio=False, mask="auto")
    else:
        c.setFillColor(NAVY); c.rect(0,0,PW,PH,fill=1,stroke=0)
    # Dark overlay on top band for readability
    from reportlab.lib.colors import Color as _Color
    _overlay = _Color(0, 0, 0, alpha=0.62)
    c.setFillColor(_overlay); c.rect(0, PH-34*mm_pt, PW, 34*mm_pt, fill=1, stroke=0)
    # Dark overlay on bottom band
    c.setFillColor(_overlay); c.rect(0, 0, PW, 20*mm_pt, fill=1, stroke=0)
    # Separator lines
    c.setStrokeColor(GOLD); c.setLineWidth(0.8)
    c.line(14*mm_pt, PH-34*mm_pt, PW-12*mm_pt, PH-34*mm_pt)
    c.line(14*mm_pt, 20*mm_pt,    PW-12*mm_pt, 20*mm_pt)
    c.setLineWidth(0.3)
    c.line(14*mm_pt, PH-36.5*mm_pt, PW-12*mm_pt, PH-36.5*mm_pt)
    c.line(14*mm_pt, 22.5*mm_pt,    PW-12*mm_pt, 22.5*mm_pt)

    # Titles
    c.setFont("SanB", 21); c.setFillColor(WHITE)
    c.drawCentredString(PW/2, PH-19*mm_pt, "CHRONOCAIRN")
    c.setFont("San", 10)
    c.drawCentredString(PW/2, PH-27*mm_pt, "Time-Crime Horror Roleplaying")
    c.setFont("SanI", 9.5); c.setFillColor(GOLD)
    c.drawCentredString(PW/2, PH-40*mm_pt, "Riccardo Scaringi")

    # Rule
    c.setStrokeColor(GOLD); c.setLineWidth(0.4)
    c.line(PW/2-28*mm_pt, PH-45*mm_pt, PW/2+28*mm_pt, PH-45*mm_pt)

    # Genre label
    c.setFont("SanB", 7); c.setFillColor(GOLD)
    c.drawCentredString(PW/2, PH-49*mm_pt, "Powered by Cairn")

    # Taglines
    c.setFont("SerI", 8.5); c.setFillColor(WHITE)
    lines = [
        "Las Vegas, 2080.",
        "",
        "You work for the Temporal Division.",
        "Pay: $800 a week.",
        "Expenses: $900 a week.",
        "The math does not add up.",
        "",
        "Madame Zhou is waiting.",
    ]
    y = PH - 62*mm_pt
    for ln in lines:
        if ln: c.drawCentredString(PW/2, y, ln)
        y -= 10.5

    # Separator
    c.setStrokeColor(GOLD); c.setLineWidth(0.3)
    c.line(PW/2-20*mm_pt, y-4*mm_pt, PW/2+20*mm_pt, y-4*mm_pt)

    # Three pillars
    c.setFont("SanB", 6.5); c.setFillColor(GOLD)
    px = [PW/2-34*mm_pt, PW/2, PW/2+34*mm_pt]
    for txt, x in zip(["ECONOMIC PRESSURE","MORAL CORRUPTION","CONTAMINATION"], px):
        c.drawCentredString(x, y-10*mm_pt, txt)

    # Description block - positioned in middle section
    y2 = y - 24*mm_pt
    c.setFont("SerI", 7.5); c.setFillColor(colors.HexColor("#8899BB"))
    lower_lines = [
        "A game about desperate people in impossible situations.",
        "About the slow math of debt and the faster math of corruption.",
        "About the permanent cost of every choice you make.",
        "",
        "Requires: 2-5 players, one Warden, polyhedral dice,",
        "and a willingness to ask hard questions.",
        "",
        "15 minutes to create a character.",
        "One session to feel the pressure.",
        "Ten sessions to see who you have become.",
    ]
    for ln in lower_lines:
        if ln: c.drawCentredString(PW/2, y2, ln)
        y2 -= 9.5

    # Bottom decorative border box with final tagline
    box_y = 30*mm_pt
    box_h = 20*mm_pt
    box_x = 18*mm_pt
    box_w = PW - 36*mm_pt
    c.setStrokeColor(GOLD); c.setLineWidth(0.5)
    c.rect(box_x, box_y, box_w, box_h, fill=0, stroke=1)
    # thin inner rule
    c.setLineWidth(0.2)
    c.rect(box_x+1.5*mm_pt, box_y+1.5*mm_pt,
           box_w-3*mm_pt, box_h-3*mm_pt, fill=0, stroke=1)
    # quote text
    c.setFont("SerI", 7); c.setFillColor(GOLD)
    c.drawCentredString(PW/2, box_y + box_h*0.62,
        "\"Vegas was never an honest city.")
    c.drawCentredString(PW/2, box_y + box_h*0.35,
        "But at least before, the rules were clear. Now? Time itself is rigged.\"")

    # Bottom rule and credits
    c.setStrokeColor(GOLD); c.setLineWidth(0.4)
    c.line(14*mm_pt, 24*mm_pt, PW-12*mm_pt, 24*mm_pt)
    c.setFont("San", 6.5); c.setFillColor(WHITE)
    c.drawCentredString(PW/2, 11*mm_pt, "Based on Cairn by Yochai Gal  |  CC BY-SA 4.0")
    c.drawCentredString(PW/2, 7*mm_pt, "R2.2.1 - Corrective Consolidation - 7 October 2026")

    c.showPage(); c.save()
    buf.seek(0)
    return buf


# ── CONTENT ──────────────────────────────────────────────────────────────────

def story():
    s = [NextPageTemplate('Blank'), pb(), p(''), NextPageTemplate('TOC'), pb()]
    title_style = ParagraphStyle('toc_page_title', fontName='SanB', fontSize=13,
        textColor=CRIMSON, spaceBefore=8, spaceAfter=6, leading=17)
    s += [Paragraph('Contents', title_style), rule(), p('CHRONOCAIRN R2.2.1 - Time-Crime Horror Roleplaying'),
          p('Riccardo Scaringi. Corrective consolidation, 7 October 2026. This development edition does not claim final human-play or commercial validation.'),
          sp(3), TableOfContents()]
    for chapter in CHAPTER_CONFIG['chapters']:
        s += [NextPageTemplate(chapter['layout']), pb()]
        s += markdown_chapter(chapter['path'], chapter['layout'])
    return s


def main():
    from pypdf import PdfReader, PdfWriter
    import argparse, hashlib, json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='CHRONOCAIRN_Final_Complete.pdf')
    args = parser.parse_args()
    target = __import__('pathlib').Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    intermediate = target.with_name('_CHRONOCAIRN_body.pdf')
    doc = UeTDoc(str(intermediate))
    content = story()
    content = [doc.toc if isinstance(item, TableOfContents) else item for item in content]
    doc.multiBuild(content)
    # Import the document, including destinations and outline; overlay the blank cover placeholder.
    writer = PdfWriter()
    writer.append(PdfReader(str(intermediate)), import_outline=True)
    writer.pages[0].merge_page(PdfReader(make_cover_pdf()).pages[0])
    writer.add_metadata({'/Title':'CHRONOCAIRN R2.2.1', '/Author':'Riccardo Scaringi',
                         '/Subject':'Time-Crime Horror Roleplaying - Corrective Consolidation'})
    with target.open('wb') as handle: writer.write(handle)
    intermediate.unlink()
    report = {'edition':'R2.2.1','chapters':[], 'pdf':target.name,
              'pages':len(writer.pages),'pdf_sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
    for chapter in CHAPTER_CONFIG['chapters']:
        path=ROOT/chapter['path']
        report['chapters'].append({**chapter,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    (ROOT/'reports/r22-build-sources.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'{target}: {len(writer.pages)} A5 pages; {len(report["chapters"])} canonical source chapters')


if __name__ == '__main__':
    main()
