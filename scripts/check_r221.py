#!/usr/bin/env python3
"""Structural PDF checks and every-field fill/save/reopen/reset in two parsers.
This is not Acrobat/Preview/Firefox/mobile testing, PDF/UA certification or a playtest.
"""
from pathlib import Path
import argparse,hashlib,json,re,tempfile
import fitz
from pypdf import PdfReader
from check_pdf_r22 import inspect as inspect_manual
ROOT=Path(__file__).resolve().parents[1]
OMNI=ROOT/'CHRONOCAIRN_OMNIBUS_R2_2_1.pdf'
SHEETS=[('Character_Sheet',43),('Accounting_Sheet',109),('Warden_Mission_Sheet',10)]
FORBIDDEN=['final contamination check','Fail = lose first turn','PCs then enemies alternating',
'game over for that PC','Telegraph That Combat Is the Wrong Choice','meant to avoid',
'the way the scene goes wrong','cannot survive on legitimate income alone',
'corruption or corrosion fully consumes','Contamination check (forced, regardless of timer)']


def normalized(doc):return re.sub(r'\s+',' ',' '.join(pg.get_text() for pg in doc))


def sample(name,multi):
    if name in {'name','agent','title'}:return 'Élodie — Caffè à Noël'.replace('—','-')
    if multi:return 'Élodie: caffè, città, Noël.\nSaved notes: line two.'
    if name.startswith('week_') or name in {'cash','debt','certificates','closing_certificates','loyalty','corruption','armor','quirk_count'}:return '12'
    return 'Test 12'


def form_roundtrip(path:Path,output_dir:Path):
    expected={};rects={};filled=output_dir/(path.stem+'-all-filled.pdf');reset=output_dir/(path.stem+'-reset.pdf')
    with fitz.open(path) as d:
        for page in d:
            for widget in page.widgets() or []:
                if widget.field_name in expected:raise AssertionError('Duplicate form name: '+widget.field_name)
                value=sample(widget.field_name, bool(widget.field_flags&4096))
                expected[widget.field_name]=value;rects[widget.field_name]=(page.number,tuple(widget.rect))
                widget.field_value=value;widget.update()
        d.save(filled)
    with fitz.open(filled) as d:
        got={w.field_name:w.field_value for pg in d for w in pg.widgets() or []}
        assert got==expected,'MuPDF did not preserve every value'
        for pg in d:
            for w in pg.widgets() or []:
                assert rects[w.field_name]==(pg.number,tuple(w.rect))
                w.reset()
        d.save(reset)
    got={name:str(value.get('/V','')) for name,value in PdfReader(filled).get_fields().items()}
    assert got==expected,'pypdf did not preserve every value'
    with fitz.open(reset) as d:
        assert sum(len(list(pg.widgets() or [])) for pg in d)==len(expected)
        assert all(not w.field_value for pg in d for w in pg.widgets() or []),'Reset left data behind'
    assert all(not v.get('/V') for v in PdfReader(reset).get_fields().values())
    return {'file':path.name,'fields':len(expected),'all_values_roundtrip':True,'reset_all_values':True,
            'parsers':['MuPDF','pypdf'],'samples_include':'accented Latin characters and multiline notes',
            'filled_file':filled.name,'reset_file':reset.name}


def inspect_omnibus(path:Path):
    out=[];links=[];bad_toc=[];bounds=[];names=[];nav=[]
    with fitz.open(path) as d:
        n=len(d);a5=n-3
        for i,pg in enumerate(d):
            target=(419.528,595.276) if i<a5 else (595.276,841.89)
            if abs(pg.rect.width-target[0])>1 or abs(pg.rect.height-target[1])>1:bounds.append(i+1)
            for b in pg.get_text('dict')['blocks']:
                for ln in b.get('lines',[]):
                    for span in ln['spans']:
                        r=fitz.Rect(span['bbox'])
                        if not (pg.rect+(-.5,-.5,.5,.5)).contains(r):out.append({'page':i+1,'text':span['text']})
            for link in pg.get_links():
                if link['kind']==fitz.LINK_GOTO and not 0<=link.get('page',-1)<n:links.append({'page':i+1,'link':link})
            for widget in pg.widgets() or []:
                names.append(widget.field_name)
                if i<a5 or not pg.rect.contains(widget.rect):out.append({'page':i+1,'field':widget.field_name})
        for level,title,page in d.get_toc():
            if not 1<=page<=n:bad_toc.append(title)
        alltext=normalized(d)
        forbidden=[x for x in FORBIDDEN if x.casefold() in alltext.casefold()]
        expected='New Debt = ceil(1.05 x max(0, Old Debt + unpaid costs - repayments - clemency))'
        assert expected in alltext, 'Both subtraction signs must remain present in rendered formula'
        assert len(names)==len(set(names))==162
        assert not bounds and not out and not links and not bad_toc and not forbidden,(bounds,out,links,bad_toc,forbidden)
        nav=d[1].get_links();assert len(nav)==10
        assert all(pg.get_text().strip() for pg in d),'Unintended blank page in Omnibus'
        count={'pages':n,'a5_pages':a5,'a4_pages':3,'bookmarks':len(d.get_toc()),'links':sum(len(pg.get_links()) for pg in d),'fields':len(names),
               'broken_links':links,'broken_bookmarks':bad_toc,'out_of_page':out,'forbidden_residues':forbidden,'formula_subtractions_present':True}
    reader=PdfReader(path);assert len(reader.get_fields())==162
    for pg in reader.pages[-3:]:
        assert pg.get('/Tabs')=='/R'
        for ref in pg.get('/Annots',[]):
            obj=ref.get_object()
            if obj.get('/Subtype')=='/Widget':
                assert obj.get('/TU'),'Missing descriptive tooltip'
                assert '/AP' in obj and '/N' in obj['/AP'],'Missing widget appearance'
    count['lang']=reader.trailer['/Root'].get('/Lang')
    count['tagged_pdf']=bool(reader.trailer['/Root'].get('/StructTreeRoot'))
    count['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    # All original rule pages are unaltered by assembly (verso page 2 is intentionally replaced).
    with fitz.open(ROOT/'CHRONOCAIRN_Final_Complete.pdf') as manual,fitz.open(path) as omnibus:
        assert len(omnibus)==len(manual)+3
        for i in range(len(manual)):
            if i==1:continue
            assert manual[i].get_text()==omnibus[i].get_text(),('Assembly altered rule text',i+1)
        count['manual_text_preserved_during_assembly']=True
    return count


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--sample-dir',type=Path,default=ROOT/'reports/r221-form-samples');args=ap.parse_args()
    args.sample_dir.mkdir(parents=True,exist_ok=True)
    r={'edition':'R2.2.1','manual':inspect_manual(ROOT/'CHRONOCAIRN_Final_Complete.pdf'),
       'omnibus':inspect_omnibus(OMNI),'roundtrips':[],
       'limits':['No manual Acrobat, Chromium viewer, Firefox, Preview or mobile execution',
                 'No native-speaker proofing or human playtests', 'No tagged-PDF / PDF-UA certification',
                 'No embedded accounting calculation or repayment validator in PDF widgets']}
    assert r['manual']['pass']
    for label,n in SHEETS:
        result=form_roundtrip(ROOT/'downloads'/f'CHRONOCAIRN_R2_2_1_{label}.pdf',args.sample_dir)
        assert result['fields']==n;r['roundtrips'].append(result)
    r['roundtrips'].append(form_roundtrip(OMNI,args.sample_dir))
    r['pass']=True
    (ROOT/'reports/r221-technical-check.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='roundtrips'},indent=2))
if __name__=='__main__':main()
