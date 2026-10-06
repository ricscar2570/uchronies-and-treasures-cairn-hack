#!/usr/bin/env python3
"""Machine checks of the built review PDF; visual inspection is separate."""
import json
from pathlib import Path
import fitz
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


def main():
    path = ROOT / 'CHRONOCAIRN_Final_Complete.pdf'
    doc = fitz.open(path)
    text = '\n'.join(p.get_text() for p in doc)
    normalized = ' '.join(text.split())
    required = ['Weekly Settlement Worksheet', 'R1 Economy Verification',
                'only unposted', "Zhou's Debt thresholds", 'Hero salary', 'Cash', 'Debt',
                'Certificates', '$330', '$735', '$1,121', 'following week']
    missing = [s for s in required if s.lower() not in normalized.lower()]
    forbidden = ['Why the Economy Is Unsustainable', 'the month breaks even.',
                 '$150 base (net)', 'Every delay increases the debt.',
                 'If players are not worried about rent, something has gone wrong.']
    stale = [s for s in forbidden if s in normalized]
    offpage, glyphs = [], []
    for i, page in enumerate(doc):
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    r = fitz.Rect(span['bbox'])
                    if r.x0 < -.5 or r.y0 < -.5 or r.x1 > page.rect.width+.5 or r.y1 > page.rect.height+.5:
                        offpage.append([i+1, span['text'], list(r)])
                    if '\ufffd' in span['text'] or '\u25a0' in span['text']:
                        glyphs.append([i+1, span['text']])
    reader = PdfReader(path)
    font_status = {}
    for page in reader.pages:
        for name, font_ref in page['/Resources'].get('/Font', {}).items():
            font = font_ref.get_object()
            desc = font.get('/FontDescriptor')
            embedded = bool(desc and any(k in desc.get_object() for k in ('/FontFile', '/FontFile2', '/FontFile3')))
            font_status[str(font.get('/BaseFont'))] = embedded
    a5 = all(abs(p.rect.width-419.5276)<.1 and abs(p.rect.height-595.2756)<.1 for p in doc)
    blank = [i+1 for i,p in enumerate(doc) if len(p.get_text().strip()) < 40]
    report = {'pages': len(doc), 'chapter_bookmarks': len(doc.get_toc()),
              'A5_all_pages': a5, 'missing_required': missing, 'stale_r1_passages': stale,
              'off_page_text_spans': offpage, 'replacement_or_black_square_glyphs': glyphs,
              'font_embedding': font_status, 'sparse_pages': blank,
              'intentional_blank': 'Page 2 is the preserved blank cover verso.',
              'visual_review': 'Separate local rendered-page review; not asserted by this script.'}
    report['pass'] = bool(a5 and not missing and not stale and not offpage and not glyphs
                          and all(font_status.values()) and len(doc.get_toc()) >= 20 and blank == [2])
    (ROOT/'reports/r1b/pdf_check.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    if not report['pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
