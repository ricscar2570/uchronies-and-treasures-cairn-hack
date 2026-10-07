#!/usr/bin/env python3
"""Assemble the corrective digital Omnibus without flattening its three A4 forms."""
from pathlib import Path
import argparse, hashlib, importlib.util, io, json
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5
import fitz

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'CHRONOCAIRN_R2_2_1_'
SHEETS = ['Character_Sheet', 'Accounting_Sheet', 'Warden_Mission_Sheet']


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--manual', type=Path, default=ROOT/'CHRONOCAIRN_Final_Complete.pdf')
    ap.add_argument('--output', type=Path, default=ROOT/'CHRONOCAIRN_OMNIBUS_R2_2_1.pdf')
    args = ap.parse_args()
    spec = importlib.util.spec_from_file_location('skin', ROOT/'scripts/build-pdf.py')
    skin = importlib.util.module_from_spec(spec); spec.loader.exec_module(skin)
    with fitz.open(args.manual) as doc:
        chapters = {title: page for level, title, page in doc.get_toc() if level == 1}
        manual_pages = len(doc)
        if doc[1].get_text().strip():
            raise ValueError('Expected an unused verso on page 2, not existing content.')
    def chapter_page(fragment):
        matches = [page for title, page in chapters.items() if fragment in title]
        if len(matches) != 1: raise ValueError(f'Ambiguous navigation target: {fragment}: {matches}')
        return matches[0]
    nav = [
        ('Complete chapter contents', 3),
        ('Rules and player guide', 4),
        ('Las Vegas and adventure sites', chapter_page('Las Vegas')),
        ('Warden tools and guidance', chapter_page("The Warden's Guide")),
        ('The Chicago Loop', chapter_page('The Chicago Loop')),
        ('Ten Weeks in Vegas', chapter_page('Ten Weeks in Vegas')),
        ('Quick references and appendices', chapter_page('Character Creation Checklist')),
        ('Character Sheet - fillable A4', manual_pages+1),
        ('Accounting Sheet - fillable A4', manual_pages+2),
        ('Warden Mission Sheet - fillable A4', manual_pages+3),
    ]
    width, height = A5
    buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=A5)
    x, right = 40, width-40
    c.setFillColor(skin.GOLD); c.setFont('SanB',8); c.drawString(x,548,'COMPLETE COLLECTION')
    c.setFillColor(skin.NAVY); c.setFont('SanB',23); c.drawString(x,514,'OMNIBUS / R2.2.1')
    c.setFont('San',9); c.drawString(x,494,'CHRONOCAIRN - Time-Crime Horror Roleplaying')
    c.setFont('San',8.5); c.drawString(x,478,'Riccardo Scaringi')
    c.setStrokeColor(skin.GOLD); c.line(x,464,right,464)
    c.setFont('San',8)
    for y,t in [(443,'The complete corrective manual and all three table sheets in one volume.'),
                (431,'Rules, examples and appendices come from the same canonical sources.'),
                (419,'No new subsystem; corrections and clarifications are recorded separately.')]:
        c.drawString(x,y,t)
    c.setFont('SanB',8.5);c.drawString(x,396,'QUICK NAVIGATION')
    nav_rects=[]
    for i,(label,page) in enumerate(nav):
        y=378-i*16
        c.setFont('San',8);c.drawString(x,y,label)
        c.setFont('SanB',8);c.drawRightString(right,y,str(page))
        nav_rects.append((x,y-3,right,y+10,page))
    c.line(x,218,right,218)
    c.setFont('San',7.5)
    lines=[
        f'Page formats. Pages 1-{manual_pages} are A5. Pages {manual_pages+1}-{manual_pages+3} retain their original A4 size.',
        'Forms. All 162 fields remain editable. Save a copy, close it and reopen it',
        'before printing. The accounting sheet is manual, not an automatic calculator.',
        'Print the three sheets separately at actual size to preserve writing space.',
        '',
        'Edition record. R2.2.1 Corrective Consolidation, 7 October 2026.',
        'Based on R2.2: d2126ff54bf097bdba1085df7bfb8315c1952a71.',
        'The delivery archive records its exact source revision and file hashes.',
        '',
        'Status. Technical checks do not replace human playtests, native-speaker',
        'proofing or testing in each reader. Script licensing remains an authorial',
        'decision; this digital collection is not a print-production certification.',
    ]
    y=198
    for t in lines:
        c.drawString(x,y,t);y-=11
    c.setStrokeColor(skin.GOLD);c.line(x,35,right,35)
    c.setFillColor(skin.GOLD);c.setFont('San',7);c.drawCentredString(width/2,24,'2')
    c.showPage();c.save();buf.seek(0)
    writer=PdfWriter();writer.append(PdfReader(args.manual),import_outline=True)
    writer.pages[1].merge_page(PdfReader(buf).pages[0])
    for sheet in SHEETS:
        writer.append(PdfReader(ROOT/'downloads'/f'{PREFIX}{sheet}.pdf'),import_outline=False)
    writer.add_outline_item('Omnibus navigation',1)
    root=writer.add_outline_item('Printable and fillable A4 sheets',manual_pages)
    for i,sheet in enumerate(SHEETS):writer.add_outline_item(sheet.replace('_',' '),manual_pages+i,parent=root)
    from pypdf.annotations import Link
    for x0,y0,x1,y1,page in nav_rects:
        writer.add_annotation(1,Link(rect=(x0,y0,x1,y1),target_page_index=page-1))
    # A4 footer: number and return link occupy clear space to the right of the original footer.
    for i in range(manual_pages,manual_pages+3):
        b=io.BytesIO(); page=writer.pages[i]; w=float(page.mediabox.width);h=float(page.mediabox.height)
        cv=canvas.Canvas(b,pagesize=(w,h));cv.setFont('San',7);cv.setFillColor(skin.NAVY)
        cv.drawRightString(w-36,18,f'Omnibus {i+1} | Contents: 2');cv.save();b.seek(0)
        page.merge_page(PdfReader(b).pages[0]);page[NameObject('/Tabs')]=NameObject('/R')
        writer.add_annotation(i,Link(rect=(w-180,12,w-36,26),target_page_index=1))
    writer._root_object[NameObject('/Lang')]=TextStringObject('en-US')
    writer.add_metadata({'/Title':'CHRONOCAIRN OMNIBUS R2.2.1','/Author':'Riccardo Scaringi',
                         '/Subject':'Time-Crime Horror Roleplaying - Corrective Consolidation'})
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('wb') as handle:writer.write(handle)
    with fitz.open(args.output) as doc:
        record={'edition':'R2.2.1','pages':len(doc),'a5_pages':manual_pages,'a4_pages':3,
                'fields':sum(len(list(pg.widgets() or [])) for pg in doc),'bookmarks':len(doc.get_toc()),
                'links':sum(len(pg.get_links()) for pg in doc),'navigation':nav,
                'sha256':hashlib.sha256(args.output.read_bytes()).hexdigest()}
    if record['fields']!=162:raise ValueError('Form field count changed during assembly')
    (ROOT/'reports/r221-omnibus.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))

if __name__=='__main__':main()
