#!/usr/bin/env python3
from pathlib import Path
import re,yaml,sys
ROOT=Path(__file__).resolve().parents[1]
m=yaml.safe_load((ROOT/'_data/canonical-rule-matrix.yml').read_text())
reg={e['id']:e for e in m['entries']}
text=(ROOT/'players-guide/example-of-play-compact.md').read_text()
expected={
'Player-led expedition':['CAMP-02'],
'Information and preparation':['WARDEN-02','TIME-03'],
'Failure stands':['CORE-01','WARDEN-03'],
'Site Check':['TIME-04','TIME-05'],
'Contamination and Quirk acquisition':['CONT-05','CONT-06'],
'Retreat and position':['CORE-21'],
'Custody and evidence':['RELIC-02'],
}
errors=[]
for label,codes in expected.items():
    line=next((x for x in text.splitlines() if f'| {label} |' in x),None)
    if not line: errors.append(f'missing row: {label}'); continue
    found=re.findall(r'\b[A-Z]+-\d+\b',line)
    if found!=codes: errors.append(f'{label}: expected {codes}, found {found}')
    for code in found:
        if code not in reg: errors.append(f'undefined code {code}')
# taxonomy
g=(ROOT/'reference/glossary.md').read_text()
if 'Immediate, Professional, Examined, Contested, or Absent' not in g: errors.append('Information Layer taxonomy mismatch')
if errors:
    print('STEP22 semantic reference validation: FAIL')
    print('\n'.join('- '+e for e in errors)); sys.exit(1)
print(f'STEP22 semantic reference validation: PASS ({sum(len(v) for v in expected.values())} expected references)')
