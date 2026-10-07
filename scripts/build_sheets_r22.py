#!/usr/bin/env python3
"""Create three independent A4 printable/fillable R2.2.1 table aids."""
from pathlib import Path
import argparse, importlib.util, json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('chronocairn_pdf',ROOT/'scripts/build-pdf.py')
skin=importlib.util.module_from_spec(spec);spec.loader.exec_module(skin)
W,H=A4; M=36; FW=W-2*M


def sheet(path:Path, title:str):
    c=canvas.Canvas(str(path),pagesize=A4)
    c.setTitle('CHRONOCAIRN R2.2.1 - '+title);c.setAuthor('Riccardo Scaringi')
    c.setFillColor(skin.NAVY);c.setFont('SanB',17);c.drawString(M,H-39,'CHRONOCAIRN')
    c.setFont('San',10);c.drawString(M,H-57,title)
    c.setFont('San',8);c.drawRightString(W-M,H-39,'R2.2.1 | Time-Crime Horror Roleplaying')
    c.setStrokeColor(skin.GOLD);c.line(M,H-69,W-M,H-69)
    return c


def text(c,x,y,t,size=8,bold=False):
    c.setFillColor(skin.NAVY);c.setFont('SanB' if bold else 'San',size);c.drawString(x,y,t)


def field(c,name,label,x,y,w,h=23,multi=False,size=9):
    if label:text(c,x,y+h+4,label,7.2,True)
    tooltip=label or name.replace('_',' ')
    if name.startswith('week_'):
        _,row,col=name.split('_')
        names=['week','opening Cash','opening Debt','Income','Costs','Unpaid costs','Repayment','Clemency','closing Cash','closing Debt']
        tooltip=f'Row {row}: {names[int(col)]}'
    c.acroForm.textfield(name=name,tooltip=tooltip,x=x,y=y,width=w,height=h,
        fontName='Helvetica',fontSize=size,borderWidth=.45,borderStyle='solid',
        fillColor=colors.white,borderColor=colors.HexColor('#A3ACB5'),textColor=colors.black,
        forceBorder=True,fieldFlags='multiline' if multi else '', maxlen=2000 if multi else 120)


def footer(c,t):
    c.setStrokeColor(skin.GOLD);c.line(M,43,W-M,43)
    text(c,M,30,t,7)
    text(c,M,18,'Riccardo Scaringi | A table aid, not an extra rule system.',6.5)
    c.showPage();c.save()


def character(path):
    c=sheet(path,'CHARACTER SHEET | finances recorded separately')
    field(c,'name','Agent / player',M,738,290);field(c,'background','Background',M+302,738,FW-302)
    widths=[120,72,72,120,99];labels=['Rank','Loyalty (0-10)','Corruption (0-10)','Conditions / Deprived','Quirks (0-5)']
    x=M
    for n,w,l in zip(['rank','loyalty','corruption','conditions','quirk_count'],widths,labels):
        field(c,n,l,x,691,w);x+=w+10
    for i,ability in enumerate(['STR','DEX','WIL','HP']):
        x=M+i*(FW/4);text(c,x,668,ability,10,True)
        field(c,ability+'_current','Current',x,631,52);field(c,ability+'_max','Maximum',x+60,631,52)
    field(c,'armor','Armor (max 3)',M,584,100)
    field(c,'temporal_protection','Temporal protection (separate)',M+112,584,160)
    field(c,'medical_completion','Current treatment / completion time',M+284,584,FW-284)
    text(c,M,563,'INVENTORY | 10 slots; bulky items use 2',8,True)
    text(c,M+275,563,'PERMANENT QUIRKS | the sixth is an echo',8,True)
    for i in range(10):
        y=537-i*20;text(c,M,y+7,str(i+1),8)
        field(c,f'inventory_{i+1}','',M+18,y,235,18)
    for i in range(5):
        field(c,f'quirk_{i+1}',str(i+1),M+275,526-i*35,FW-275,24)
    text(c,M+275,370,'Fatigue occupies inventory slots.',7)
    text(c,M+275,357,'Record the occupied slots, not a second total.',7)
    for i,y in enumerate([302,256],1):
        field(c,f'weapon_{i}','Weapon / damage',M,y,165)
        field(c,f'magazine_{i}','Current: ready / low / empty',M+177,y,147)
        field(c,f'reloads_{i}','Compatible spare reloads',M+336,y,FW-336)
    field(c,'zone','Current zone',M,211,95)
    field(c,'exposure_fraction','Exposure fraction filled',M+107,211,124)
    field(c,'next_check','Time until next periodic check',M+243,211,FW-243)
    text(c,M,194,'Yellow 8h | Orange 6h | Red 3h | Black 1h | carry the fraction; no exit check',7)
    field(c,'ties','Why the Division? What keeps you desperate? Who matters to you?',M,75,FW,92,True)
    footer(c,'Save: d20 <= current attribute. Damage overflow tests reduced STR. No automatic recovery at session end.')


def accounting(path):
    c=sheet(path,'ACCOUNTING SHEET | Cash, Debt and Certificates are separate')
    field(c,'agent','Agent',M,738,250);field(c,'period','Weeks / campaign dates',M+262,738,FW-262)
    for i,(n,l) in enumerate([('cash','Opening Cash'),('debt','Opening Debt'),('certificates','Opening Certificates')]):
        field(c,n,l,M+i*(FW/3),691,FW/3-12)
    field(c,'weekly_status','Start-of-week rank, Loyalty and Instability; dated payroll conditions',M,620,FW,44,True,8)
    heads=['Week','Start\nCash','Start\nDebt','Income','Costs','Unpaid','Repay','Clem.','End\nCash','End\nDebt']
    weights=[.055,.105,.105,.105,.105,.105,.095,.095,.11,.12]
    widths=[FW*w for w in weights];y=587;x=M
    c.setFillColor(skin.NAVY);c.rect(M,y,FW,24,fill=1,stroke=0)
    for head,w in zip(heads,widths):
        c.setFillColor(colors.white);c.setFont('SanB',6.6)
        for k,line in enumerate(head.split('\n')):c.drawCentredString(x+w/2,y+15-k*8,line)
        x+=w
    for row in range(10):
        y=560-row*27;x=M
        for col,w in enumerate(widths):
            field(c,f'week_{row+1}_{col}','',x+.5,y,w-1,25,size=7.5);x+=w
    text(c,M,306,'Available Cash = max(0, Start Cash + Income - Costs).',7.1)
    text(c,M,296,'Unpaid = max(0, Costs - Start Cash - Income). Clemency is not Cash.',7.1)
    text(c,M,286,'Require 0 <= Repayment <= min(Available Cash, Start Debt + Unpaid); reject excess.',7.1)
    text(c,M,276,'End Cash = max(0, Available Cash - Repayment). Fields do not calculate automatically.',7.1)
    text(c,M,266,'End Debt = round UP [1.05 x max(0, Start Debt + Unpaid - Repayment - Clemency)].',7.1)
    text(c,M,254,'From opening Cash: list each dated receipt ONCE; do not credit it again at close.',7.1,True)
    field(c,'transactions','Transactions: Cash / Certificates separately; Raines jobs, information sales, costs and receipts',M,150,FW,92,True,8)
    field(c,'obligations','Named creditors, explicit team obligations, disputed claims and promises',M,75,FW-157,50,True,8)
    field(c,'closing_certificates','Closing Certificates',W-M-145,102,145,23)
    text(c,W-M-145,88,'Whole Certificates only;',6.7)
    text(c,W-M-145,77,'1 = $800 Cash; +1 Corruption / cash-out.',6.7)
    footer(c,'One allowance + one performance band. Hero benefit multiplies base pay only. Debt never repays itself.')


def warden(path):
    c=sheet(path,'WARDEN MISSION SHEET | prepare situations, not solutions')
    field(c,'title','Mission / patron',M,738,335);field(c,'date','Session / fictional week',M+347,738,FW-347)
    field(c,'objectives','Objective, evidence of completion and NPC interests',M,647,FW,61,True,8)
    field(c,'pay','Performance-band criteria / gross and net / one allowance / alternatives',M,571,FW,49,True,8)
    field(c,'costs','Visible economic cost, payer, payment timing and no-double-charge note',M,496,FW,48,True,8)
    field(c,'routes','Approach routes, visible danger, retreat and what happens if nobody intervenes',M,419,FW,50,True,8)
    field(c,'clock','Time log: entry / zone / elapsed fraction / next check / fixed deadline / changes',M,331,FW,61,True,8)
    field(c,'hazards','Named EXTRA hazards and warnings (separate from periodic checks)',M,266,FW,38,True,8)
    field(c,'factions','NPC knowledge, deals, faction consequences and room for a third approach',M,173,FW,66,True,8)
    field(c,'debrief','Actual outcome, pay ONCE, Loyalty/Corruption changes, witnesses and future obligations',M,75,FW,71,True,8)
    footer(c,'At extraction: resolve checks actually reached. No forced fight, death, Quirk, allegiance or ending.')


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-dir',type=Path,default=ROOT/'downloads');args=ap.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    products=[('Character_Sheet',character),('Accounting_Sheet',accounting),('Warden_Mission_Sheet',warden)]
    result=[]
    import fitz,hashlib
    for label,fn in products:
        p=args.output_dir/f'CHRONOCAIRN_R2_2_1_{label}.pdf';fn(p)
        from pypdf import PdfReader,PdfWriter
        from pypdf.generic import NameObject,TextStringObject
        writer=PdfWriter(clone_from=str(p))
        writer._root_object[NameObject('/Lang')]=TextStringObject('en-US')
        for page in writer.pages:page[NameObject('/Tabs')]=NameObject('/R')
        with p.open('wb') as handle:writer.write(handle)
        with fitz.open(p) as d: result.append({'file':p.name,'pages':len(d),'fields':sum(len(list(pg.widgets() or [])) for pg in d),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    (ROOT/'reports/r22-sheets.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
