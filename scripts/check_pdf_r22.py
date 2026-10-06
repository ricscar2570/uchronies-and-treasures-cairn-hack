#!/usr/bin/env python3
"""Geometric, navigation and source-provenance checks; not semantic or press certification."""
from pathlib import Path
import argparse,hashlib,json,re
import fitz
ROOT=Path(__file__).resolve().parents[1]


def inspect(path:Path)->dict:
    outside=[];blank=[];bad_links=[];unknown=[]
    with fitz.open(path) as pdf:
        toc=pdf.get_toc(); texts=[]
        for n,page in enumerate(pdf):
            texts.append(page.get_text())
            if not page.get_text(clip=fitz.Rect(0,0,page.rect.width,page.rect.height-50)).strip():blank.append(n+1)
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines',[]):
                    for span in line['spans']:
                        x0,y0,x1,y1=span['bbox']
                        if x0<-.5 or y0<-.5 or x1>page.rect.width+.5 or y1>page.rect.height+.5:
                            outside.append({'page':n+1,'text':span['text'],'bbox':span['bbox']})
                        if '\ufffd' in span['text']:unknown.append({'page':n+1,'text':span['text']})
            for link in page.get_links():
                if link['kind']==fitz.LINK_GOTO and not 0<=link.get('page',-1)<len(pdf):bad_links.append({'page':n+1,'link':link})
        text=re.sub(r'\s+',' ',' '.join(texts))
        patterns=[r'\bXP\b',r'\(intended\)',r'failure state',r'No choice: it',r'a PC probably dies',r"team.s shared debt",r'\+1 Exposure']
        forbidden=[pattern for pattern in patterns if re.search(pattern,text,re.I)]
        anchors=['Ten Weeks in Vegas','Rules Interactions and Edge Cases','Do not roll d12','Emergency Clinic Contract','Causal Distortions','R2.2 economics','Cash','Certificates']
        missing=[a for a in anchors if a not in text]
        result={'file':path.name,'pages':len(pdf),'a5':all(abs(pg.rect.width-419.528)<1 and abs(pg.rect.height-595.276)<1 for pg in pdf),
                'outline_entries':len(toc),'chapter_bookmarks':sum(1 for t in toc if t[0]==1),
                'links':sum(len(pg.get_links()) for pg in pdf),'outside_page':outside,'blank_body_pages':blank,
                'broken_internal_links':bad_links,'replacement_glyphs':unknown,'forbidden_active_text':forbidden,'missing_anchors':missing,
                'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    manifest=json.loads((ROOT/'reports/r22-build-sources.json').read_text())
    result['source_hash_mismatches']=[entry['path'] for entry in manifest['chapters'] if hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()!=entry['sha256']]
    result['pass']=not any([outside,bad_links,unknown,forbidden,missing,result['source_hash_mismatches']]) and blank==[2] and result['a5'] and result['chapter_bookmarks']==26
    result['scope']='Page bounds, declared text anchors, imported navigation and all 26 source hashes. Not proof of complete semantic, accessibility or commercial readiness.'
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('pdf',type=Path);ap.add_argument('--output',type=Path,default=ROOT/'reports/r22-pdf-check.json');a=ap.parse_args()
    r=inspect(a.pdf);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
    if not r['pass']:raise SystemExit(1)
if __name__=='__main__':main()
