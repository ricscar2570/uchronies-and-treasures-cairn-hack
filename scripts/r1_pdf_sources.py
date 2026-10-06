"""Render audited R1 chapters from their Markdown sources, not duplicate prose.

A deliberately small parser for the repository's headings, paragraphs, lists,
blockquotes and pipe tables. Unsupported embedded HTML fails closed except for
Jekyll's navigation-only details block and attributes.
"""
import re
from pathlib import Path
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer, HRFlowable

ROOT = Path(__file__).resolve().parents[1]


def strip_source(text):
    text = re.sub(r'\A---\s*\n.*?\n---\s*\n', '', text, flags=re.S)
    text = re.sub(r'<details\b.*?</details>', '', text, flags=re.S)
    text = re.sub(r'^\{:[^\n]*\}\s*$', '', text, flags=re.M)
    if re.search(r'</?[A-Za-z][^>]*>', text):
        raise ValueError('Unexpected HTML in R1 Markdown source')
    return text.strip()


def inline(text, ns):
    text = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', text)
    return ns['md'](text)


def render_chapter(relative_path, ns):
    path = ROOT / relative_path
    text = strip_source(path.read_text(encoding='utf-8'))
    lines = text.splitlines()
    flow = []
    styles = ns['STYLES']
    body = ParagraphStyle('r1-body', parent=styles['body'], fontSize=9, leading=12.4,
                          spaceAfter=4, splitLongWords=True)
    if relative_path == 'reference/r1-economy-validation.md':
        body.fontSize, body.leading = 8.5, 11.5
    quote = ParagraphStyle('r1-note', parent=body, fontName='SerI', textColor=ns['NAVY'],
                           leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=6)
    item = ParagraphStyle('r1-item', parent=body, leftIndent=12, firstLineIndent=-9,
                          alignment=0, spaceAfter=3)
    table_cell = ParagraphStyle('r1-cell', parent=styles['td'], fontSize=8, leading=10.5)
    table_head = ParagraphStyle('r1-head', parent=styles['th'], fontSize=7.5, leading=10)
    width = ns['FW'] - 12  # ReportLab full-frame default left/right padding.
    first_heading = True
    base_heading = None
    i = 0
    def paragraph(t, st=body):
        return Paragraph(inline(t, ns), st)
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        heading = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading:
            level, title = len(heading[1]), heading[2]
            if first_heading:
                base_heading = level
                flow.extend([ns['h1'](title), ns['rule']()])
                first_heading = False
            else:
                depth = max(1, level - base_heading)
                flow.append(ns['h2'](title) if depth == 1 else ns['h3'](title))
            i += 1
            continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                raw = lines[i].strip().strip('|')
                cells = [c.strip().replace('\\|', '|') for c in re.split(r'(?<!\\)\|', raw)]
                if not all(re.fullmatch(r':?-{2,}:?', c) for c in cells):
                    rows.append(cells)
                i += 1
            count = len(rows[0])
            if any(len(row) != count for row in rows):
                raise ValueError(f'Unequal column counts in {relative_path}: {rows[0]}')
            # Wide descriptive columns receive more room; numeric columns retain
            # an explicit minimum instead of squeezing to their shortest value.
            weights = []
            for c in range(count):
                lengths = sorted(min(60, len(re.sub(r'\*|`', '', row[c]))) for row in rows)
                weights.append(max(10, lengths[int((len(lengths)-1)*.75)]))
            if rows[0][0].lower() in ('d6', 'd10'):
                weights[0] = 6
            widths = [width*w/sum(weights) for w in weights]
            data = [[paragraph(c, table_head if r == 0 else table_cell) for c in row]
                    for r, row in enumerate(rows)]
            table = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), ns['SLATE']),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [ns['WHITE'], ns['LGREY']]),
                ('GRID', (0,0), (-1,-1), .25, ns['MGREY']),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
                ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ]))
            flow.extend([table, Spacer(1, 7)])
            continue
        if re.fullmatch(r'[-*_]{3,}', line):
            flow.append(ns['rule']())
            i += 1
            continue
        if line.startswith('>'):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            flow.append(paragraph(' '.join(quote_lines), quote))
            continue
        if line.startswith('```'):
            raise ValueError(f'Code fence requires an explicit rendering policy: {relative_path}')
        bullet = re.match(r'^([-*]|\d+\.)\s+(.*)$', line)
        if bullet:
            prefix = '\u2022 ' if bullet[1] in ('-', '*') else bullet[1] + ' '
            flow.append(paragraph(prefix + bullet[2], item))
            i += 1
            continue
        paragraph_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(?:#|\||>|[-*] |\d+\. |\{:) ', lines[i].strip()):
            # Structural lines normally follow a blank line. Do not eat them
            # even if an author removes that separator.
            if re.match(r'^(#{1,6}\s|\||>|[-*]\s|\d+\.\s|\{:) ', lines[i].strip()):
                break
            if lines[i].strip().startswith(('# ', '## ', '### ', '|', '>')):
                break
            paragraph_lines.append(lines[i].strip())
            i += 1
        flow.append(paragraph(' '.join(paragraph_lines)))
    return flow


def normalize_breaks(flowables):
    """Move a template switch before the preceding chapter-end page break.

    Preserve the intentional front-matter blank, collapse only redundant body
    breaks. Source sections do not need to know how the preceding chapter ends.
    """
    from reportlab.platypus import NextPageTemplate, PageBreak
    out = []
    body_started = False
    for flow in flowables:
        if isinstance(flow, Paragraph) and flow.style.name == 'h1':
            body_started = True
        if body_started and isinstance(flow, NextPageTemplate) and out and isinstance(out[-1], PageBreak):
            last_break = out.pop()
            # Replace a superseded template switch immediately before the break.
            if out and isinstance(out[-1], NextPageTemplate):
                out.pop()
            out.extend([flow, last_break])
        elif body_started and isinstance(flow, PageBreak) and out and isinstance(out[-1], PageBreak):
            continue
        else:
            out.append(flow)
    return out
