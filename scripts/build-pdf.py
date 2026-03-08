#!/usr/bin/env python3
"""
Uchronies & Treasures - Cairn Edition
PDF Manual Generator

Usage:
    python scripts/build-pdf.py                    # Output: UeT_Cairn_Manual.pdf
    python scripts/build-pdf.py -o my_manual.pdf   # Custom output path

Requirements:
    pip install reportlab pypdf
"""

import re, os, sys, argparse
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    Paragraph, Spacer, PageBreak, Table, TableStyle,
    Frame, PageTemplate, BaseDocTemplate, NextPageTemplate,
    Flowable
)

# === COLORS (Division Dossier theme - light parchment) ===
CRIMSON     = HexColor('#8B1A1A')
AMBER       = HexColor('#996515')
TEAL        = HexColor('#1a6e5c')
PARCHMENT   = HexColor('#f5f0e8')
INK         = HexColor('#2c2417')
INK_LIGHT   = HexColor('#6b5d4a')
BORDER      = HexColor('#b8a880')
BG_ELEVATED = HexColor('#ebe4d5')

# === PAGE GEOMETRY (A5, generous margins) ===
PAGE_W, PAGE_H = A5
MARGIN_TOP     = 20 * mm
MARGIN_BOTTOM  = 18 * mm
MARGIN_LEFT    = 14 * mm
MARGIN_RIGHT   = 14 * mm
COL_GAP        = 6 * mm

CONTENT_W = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT
COL_W     = (CONTENT_W - COL_GAP) / 2
FRAME_H   = PAGE_H - MARGIN_TOP - MARGIN_BOTTOM

# === CONTENT FILES (reading order, grouped by part) ===
PARTS = [
    ("PLAYER'S GUIDE", "Everything you need to play", [
        "players-guide/overview-and-principles.md",
        "players-guide/character-creation.md",
        "players-guide/core-rules.md",
        "players-guide/exploration-and-time.md",
        "players-guide/temporal-relics.md",
        "players-guide/example-of-play.md",
    ]),
    ("GAME SYSTEMS", "The machinery beneath the fiction", [
        "game-systems/economy.md",
        "game-systems/contamination.md",
        "game-systems/temporal-quirks.md",
        "game-systems/loyalty-corruption.md",
    ]),
    ("SETTING", "Las Vegas, 55 years after the Oculus Event", [
        "setting/las-vegas-2080.md",
        "setting/adventure-sites.md",
    ]),
    ("ADVENTURES", "Ready to play tonight", [
        "adventures/the-chicago-loop.md",
        "adventures/the-first-four-weeks.md",
    ]),
    ("WARDEN'S GUIDE", "Running the game", [
        "wardens-guide/running-the-game.md",
        "wardens-guide/tables-and-generators.md",
        "wardens-guide/campaign-management.md",
        "wardens-guide/creating-enemies.md",
        "wardens-guide/faq.md",
        "wardens-guide/design-notes.md",
    ]),
    ("REFERENCE", "Quick lookup", [
        "reference/warden-cheat-sheet.md",
        "reference/character-creation-checklist.md",
    ]),
]


# === STYLES ===
def make_styles():
    return {
        'body': ParagraphStyle(
            'body', fontName='Helvetica', fontSize=8.5,
            textColor=INK, leading=12.5, alignment=TA_JUSTIFY,
            spaceBefore=4, spaceAfter=5),
        'h1': ParagraphStyle(
            'h1', fontName='Helvetica-Bold', fontSize=16,
            textColor=CRIMSON, spaceBefore=16, spaceAfter=10,
            leading=19, alignment=TA_LEFT),
        'h2': ParagraphStyle(
            'h2', fontName='Helvetica-Bold', fontSize=11,
            textColor=CRIMSON, spaceBefore=14, spaceAfter=6,
            leading=14, alignment=TA_LEFT),
        'h3': ParagraphStyle(
            'h3', fontName='Helvetica-Bold', fontSize=9.5,
            textColor=INK, spaceBefore=10, spaceAfter=5,
            leading=12, alignment=TA_LEFT),
        'h4': ParagraphStyle(
            'h4', fontName='Helvetica-BoldOblique', fontSize=8.5,
            textColor=INK_LIGHT, spaceBefore=8, spaceAfter=4,
            leading=11, alignment=TA_LEFT),
        'quote': ParagraphStyle(
            'quote', fontName='Helvetica', fontSize=8,
            textColor=INK_LIGHT, leading=11.5,
            leftIndent=8, rightIndent=4, backColor=BG_ELEVATED,
            spaceBefore=6, spaceAfter=6, borderPadding=(6, 6, 6, 6)),
        'bullet': ParagraphStyle(
            'bullet', fontName='Helvetica', fontSize=8.5,
            textColor=INK, leading=12, leftIndent=14,
            bulletIndent=4, spaceBefore=2, spaceAfter=3),
        'code': ParagraphStyle(
            'code', fontName='Courier', fontSize=6.5,
            textColor=TEAL, backColor=BG_ELEVATED,
            leftIndent=6, rightIndent=6,
            spaceBefore=4, spaceAfter=4, leading=9),
        'title': ParagraphStyle(
            'title', fontName='Helvetica-Bold', fontSize=26,
            textColor=CRIMSON, alignment=TA_CENTER,
            spaceBefore=0, spaceAfter=6, leading=30),
        'subtitle': ParagraphStyle(
            'subtitle', fontName='Helvetica-Oblique', fontSize=10,
            textColor=AMBER, alignment=TA_CENTER,
            spaceBefore=3, spaceAfter=3, leading=14),
        'footer': ParagraphStyle(
            'footer', fontName='Helvetica', fontSize=6,
            textColor=INK_LIGHT, alignment=TA_CENTER),
        'part_title': ParagraphStyle(
            'part_title', fontName='Helvetica-Bold', fontSize=20,
            textColor=CRIMSON, alignment=TA_CENTER,
            spaceBefore=50, spaceAfter=10, leading=24),
        'part_sub': ParagraphStyle(
            'part_sub', fontName='Helvetica-Oblique', fontSize=9,
            textColor=INK_LIGHT, alignment=TA_CENTER,
            spaceBefore=6, spaceAfter=30, leading=12),
    }

ST = make_styles()


# === FLOWABLES ===
class HRule(Flowable):
    def __init__(self, width, color=CRIMSON, thickness=0.5):
        Flowable.__init__(self)
        self.width = width
        self.height = 8
        self.color = color
        self.thickness = thickness
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 4, self.width, 4)


# === MARKDOWN PARSER ===
def strip_frontmatter(text):
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            text = text[end + 3:].strip()
    text = re.sub(r'\{:\s*\.no_toc\s*\}', '', text)
    text = re.sub(r'<details.*?</details>', '', text, flags=re.DOTALL)
    return text.strip()

def md_inline(text):
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    text = re.sub(r'`(.*?)`', r'<font name="Courier" size="7" color="#1a6e5c">\1</font>', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    return text

def parse_pipe_table(lines):
    rows = []
    for line in lines:
        line = line.strip()
        if line.startswith('|') and not re.match(r'\|[\s\-\|:]+\|$', line):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if cells:
                rows.append(cells)
    return rows

def make_table(rows, col_width):
    if not rows:
        return None
    ncols = max(len(r) for r in rows)
    cell_st = ParagraphStyle('tc', fontName='Helvetica', fontSize=7, leading=9.5, textColor=INK)
    hdr_st  = ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=6.5, leading=8.5, textColor=white)
    data = []
    for ri, row in enumerate(rows):
        while len(row) < ncols:
            row.append('')
        st = hdr_st if ri == 0 and len(rows) > 1 else cell_st
        data.append([Paragraph(md_inline(c), st) for c in row])
    cw = col_width / ncols
    t = Table(data, colWidths=[cw] * ncols)
    cmds = [
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'), ('FONTSIZE', (0,0), (-1,-1), 7),
        ('LEADING', (0,0), (-1,-1), 9.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [PARCHMENT, BG_ELEVATED]),
        ('GRID', (0,0), (-1,-1), 0.3, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]
    if len(rows) > 1:
        cmds += [('BACKGROUND', (0,0), (-1,0), CRIMSON), ('TEXTCOLOR', (0,0), (-1,0), white),
                 ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,0), 6.5)]
    t.setStyle(TableStyle(cmds))
    return t

def md_to_flowables(text, col_width):
    text = strip_frontmatter(text)
    lines = text.split('\n')
    out = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1; continue
        # Headers
        for lvl, prefix, style_key in [(1,'# ','h1'),(2,'## ','h2'),(3,'### ','h3'),(4,'#### ','h4')]:
            if line.startswith(prefix):
                if lvl <= 2:
                    out.append(Spacer(1, 6))
                    if lvl == 2:
                        out.append(HRule(col_width, BORDER, 0.3))
                out.append(Paragraph(md_inline(line[len(prefix):]), ST[style_key]))
                if lvl == 1:
                    out.append(Spacer(1, 2))
                i += 1; break
        else:
            # HR
            if line in ('---', '***', '___'):
                out.append(HRule(col_width)); i += 1; continue
            # Code block
            if line.startswith('```'):
                code = []; i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code.append(lines[i].rstrip()); i += 1
                i += 1
                ct = '<br/>'.join(l.replace(' ','&nbsp;').replace('\t','&nbsp;&nbsp;') for l in code[:25])
                out += [Spacer(1,2), Paragraph(ct, ST['code']), Spacer(1,2)]; continue
            # Pipe table
            if '|' in line and i+1 < len(lines) and ('---' in lines[i+1] or '|' in lines[i+1]):
                tl = []
                while i < len(lines) and ('|' in lines[i] or re.match(r'\s*[\-\|:]+\s*$', lines[i].strip())):
                    tl.append(lines[i]); i += 1
                t = make_table(parse_pipe_table(tl), col_width)
                if t: out += [Spacer(1,5), t, Spacer(1,5)]
                continue
            # Pandoc simple table
            if re.match(r'\s*-{3,}\s+-{3,}', line):
                i += 1
                while i < len(lines) and lines[i].strip() and not re.match(r'\s*-{3,}\s+-{3,}', lines[i]):
                    if lines[i].strip(): out.append(Paragraph(md_inline(lines[i].strip()), ST['body']))
                    i += 1
                if i < len(lines) and re.match(r'\s*-{3,}', lines[i]): i += 1
                continue
            # Blockquote
            if line.startswith('>'):
                ql = []
                while i < len(lines) and (lines[i].strip().startswith('>') or
                        (lines[i].strip() and ql and not lines[i].strip().startswith('#') and not lines[i].strip().startswith('-'))):
                    q = lines[i].strip()
                    if q.startswith('>'): q = q[1:].strip()
                    ql.append(q); i += 1
                out += [Spacer(1,2), Paragraph(md_inline(' '.join(ql)), ST['quote']), Spacer(1,2)]; continue
            # Bullet
            if line.startswith('- ') or line.startswith('* '):
                bt = line[2:]; i += 1
                while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith(('-','*','#','>','|','```')):
                    if lines[i].startswith('  '): bt += ' ' + lines[i].strip(); i += 1
                    else: break
                out.append(Paragraph(md_inline(bt), ST['bullet'], bulletText='\u2022')); continue
            # Paragraph
            pl = [line]; i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith(('#','-','*','>','|','```','---')):
                pl.append(lines[i].strip()); i += 1
            out.append(Paragraph(md_inline(' '.join(pl)), ST['body']))
    return out


# === PAGE BACKGROUNDS ===
def page_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PARCHMENT)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    y = PAGE_H - MARGIN_TOP + 8
    canvas.setStrokeColor(CRIMSON); canvas.setLineWidth(0.8)
    canvas.line(MARGIN_LEFT, y, PAGE_W - MARGIN_RIGHT, y)
    canvas.setStrokeColor(AMBER); canvas.setLineWidth(0.3)
    canvas.line(MARGIN_LEFT, y - 3, PAGE_W - MARGIN_RIGHT, y - 3)
    canvas.setFont('Helvetica', 6); canvas.setFillColor(INK_LIGHT)
    canvas.drawCentredString(PAGE_W/2, MARGIN_BOTTOM - 10, f"Uchronies & Treasures  \u2022  {doc.page}")
    canvas.restoreState()

def cover_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PARCHMENT); canvas.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0)
    canvas.setFillColor(CRIMSON)
    canvas.rect(MARGIN_LEFT, PAGE_H*0.56, CONTENT_W, 2.5, fill=1, stroke=0)
    canvas.rect(MARGIN_LEFT, PAGE_H*0.34, CONTENT_W, 0.8, fill=1, stroke=0)
    canvas.setFillColor(AMBER)
    canvas.rect(MARGIN_LEFT, PAGE_H*0.555, CONTENT_W, 0.5, fill=1, stroke=0)
    canvas.restoreState()

def blank_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PARCHMENT); canvas.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0)
    canvas.restoreState()


# === BUILD ===
def find_repo_root():
    for candidate in [
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        os.path.dirname(os.path.abspath(__file__)),
        os.getcwd(),
    ]:
        if os.path.isfile(os.path.join(candidate, '_config.yml')):
            return candidate
    print("ERROR: Cannot find repo root (_config.yml not found).")
    print("  Run from the repo root or from scripts/.")
    sys.exit(1)

def build_pdf(output_path=None):
    repo = find_repo_root()
    if output_path is None:
        output_path = os.path.join(repo, 'UeT_Cairn_Manual.pdf')
    print(f"Repo:   {repo}")
    print(f"Output: {output_path}")
    print()

    kw = dict(leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    templates = [
        PageTemplate(id='Cover',  frames=[Frame(MARGIN_LEFT,MARGIN_BOTTOM,CONTENT_W,FRAME_H,id='cover',**kw)], onPage=cover_bg),
        PageTemplate(id='Blank',  frames=[Frame(MARGIN_LEFT,MARGIN_BOTTOM,CONTENT_W,FRAME_H,id='blank',**kw)], onPage=blank_bg),
        PageTemplate(id='TwoCol', frames=[
            Frame(MARGIN_LEFT,MARGIN_BOTTOM,COL_W,FRAME_H,id='left',**kw),
            Frame(MARGIN_LEFT+COL_W+COL_GAP,MARGIN_BOTTOM,COL_W,FRAME_H,id='right',**kw)
        ], onPage=page_bg),
        PageTemplate(id='OneCol', frames=[Frame(MARGIN_LEFT,MARGIN_BOTTOM,CONTENT_W,FRAME_H,id='single',**kw)], onPage=page_bg),
    ]
    doc = BaseDocTemplate(output_path, pagesize=A5, title="Uchronies & Treasures", author="Riccardo Sgaringi")
    doc.addPageTemplates(templates)

    story = []

    # Cover
    story.append(Spacer(1, PAGE_H * 0.22))
    story.append(Paragraph("UCHRONIES", ST['title']))
    story.append(Paragraph("&amp; TREASURES", ParagraphStyle('t2',parent=ST['title'],fontSize=20,textColor=AMBER,spaceBefore=0,leading=24)))
    story.append(Spacer(1, 12))
    story.append(Paragraph("A Cairn Hack of Temporal Heists<br/>and Financial Desperation", ST['subtitle']))
    story.append(Spacer(1, 30))
    story.append(Paragraph("<i>Breaking Bad meets Cairn meets Looper</i>", ParagraphStyle('tag',fontName='Helvetica-Oblique',fontSize=8,textColor=INK_LIGHT,alignment=TA_CENTER,leading=11)))
    story.append(Spacer(1, PAGE_H * 0.12))
    story.append(Paragraph("by Riccardo Sgaringi", ParagraphStyle('auth',fontName='Helvetica',fontSize=9,alignment=TA_CENTER,textColor=INK)))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Based on Cairn by Yochai Gal  |  CC-BY-SA 4.0", ParagraphStyle('lic',fontName='Helvetica',fontSize=6.5,alignment=TA_CENTER,textColor=INK_LIGHT)))

    # Blank
    story.append(NextPageTemplate('Blank')); story.append(PageBreak()); story.append(Spacer(1,1))

    # Content
    story.append(NextPageTemplate('TwoCol')); story.append(PageBreak())

    for part_name, part_desc, files in PARTS:
        story.append(NextPageTemplate('OneCol')); story.append(PageBreak())
        story.append(Spacer(1, PAGE_H * 0.2))
        story.append(Paragraph(part_name, ST['part_title']))
        story.append(HRule(CONTENT_W, CRIMSON, 1))
        story.append(Paragraph(part_desc, ST['part_sub']))
        story.append(NextPageTemplate('TwoCol')); story.append(PageBreak())

        for fi, fname in enumerate(files):
            fp = os.path.join(repo, fname)
            if not os.path.isfile(fp):
                print(f"  WARNING: {fp} not found, skipping"); continue
            print(f"  {fname}")
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
            story.extend(md_to_flowables(content, COL_W))
            if fi < len(files) - 1:
                story += [Spacer(1,10), HRule(COL_W, BORDER, 0.3), Spacer(1,6)]

    # Back cover
    story.append(NextPageTemplate('Cover')); story.append(PageBreak())
    story.append(Spacer(1, PAGE_H * 0.28))
    story.append(Paragraph("Your stipend is $800.<br/>Your expenses are $900.<br/><br/>Do the math.",
        ParagraphStyle('back',fontName='Helvetica-Oblique',fontSize=12,textColor=INK,alignment=TA_CENTER,leading=18)))
    story.append(Spacer(1, 30))
    story.append(Paragraph("cairnrpg.com  |  CC-BY-SA 4.0", ST['footer']))

    print("\nBuilding PDF...")
    doc.build(story)

    sz = os.path.getsize(output_path) / 1024
    try:
        from pypdf import PdfReader
        pg = len(PdfReader(output_path).pages)
    except ImportError:
        pg = '?'
    print(f"\n  {output_path}")
    print(f"  {pg} pages, {sz:.0f} KB")
    print("\nDone.")
    return output_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build the UeT PDF manual.')
    parser.add_argument('-o', '--output', default=None, help='Output PDF path')
    build_pdf(parser.parse_args().output)
