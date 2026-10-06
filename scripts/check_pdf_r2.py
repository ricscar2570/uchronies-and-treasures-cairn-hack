#!/usr/bin/env python3
"""Geometric PDF checks for the R2.1 build. Visual review is a separate human/vision step."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import fitz

def inspect(path: Path) -> dict:
    with fitz.open(path) as pdf:
        outside, empty_body, all_text = [], [], []
        for index, page in enumerate(pdf):
            all_text.append(page.get_text())
            body = page.get_text(clip=fitz.Rect(0, 0, page.rect.width, page.rect.height-50)).strip()
            if not body:
                empty_body.append(index+1)
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    for span in line['spans']:
                        x0,y0,x1,y1 = span['bbox']
                        if x0 < -.5 or y0 < -.5 or x1 > page.rect.width+.5 or y1 > page.rect.height+.5:
                            outside.append({'page':index+1, 'text':span['text'], 'bbox':span['bbox']})
        text = re.sub(r'\s+', ' ', ' '.join(all_text))
        anchors = ['maximum penalty of -3', 'Five distinct Quirks are survivable',
                   'R2.1 contamination diagnostic', 'The First Four Weeks (Mini-Campaign)']
        missing = [anchor for anchor in anchors if anchor not in text]
        result = {'file':path.name, 'pages':len(pdf), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                  'spans_outside_page':outside, 'pages_without_body':empty_body,
                  'intentional_blank_verso':2, 'missing_content_anchors':missing,
                  'pass':not outside and empty_body==[2] and not missing,
                  'scope':'Geometry and selected text anchors; not proof of editorial completeness.'}
        return result

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--output', type=Path, default=Path('reports/r2-pdf-check.json'))
    args=parser.parse_args()
    result=inspect(args.pdf)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    if not result['pass']:
        raise SystemExit(1)

if __name__=='__main__':
    main()
