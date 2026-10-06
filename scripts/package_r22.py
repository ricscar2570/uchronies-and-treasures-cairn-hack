#!/usr/bin/env python3
"""Package a verified R2.2 source checkpoint and its generated table aids."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import argparse, hashlib, re, subprocess

ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={'.ttf','.otf','.woff','.woff2','.eot','.zip','.pyc'}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-commit',required=True)
    ap.add_argument('--output',type=Path,default=ROOT/'CHRONOCAIRN_R2_2_Verified.zip')
    args=ap.parse_args()
    if not re.fullmatch('[0-9a-f]{40}',args.source_commit):ap.error('An exact 40-character GitHub commit SHA is required.')
    tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
    paths={ROOT/name for name in tracked}
    paths.add(ROOT/'CHRONOCAIRN_Final_Complete.pdf')
    paths.update((ROOT/'downloads').glob('CHRONOCAIRN_R2_2_*.pdf'))
    paths.update((ROOT/'reports').glob('r22-*'))
    required=[ROOT/'CHRONOCAIRN_Final_Complete.pdf',ROOT/'reports/r22-tests.txt',ROOT/'reports/r22-pdf-check.json']
    for p in required:
        if not p.is_file():raise SystemExit('Missing validated output: '+str(p))
    manifest=[]
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(args.output,'w',ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(paths):
            rel=p.relative_to(ROOT)
            if not p.is_file() or p.suffix.lower() in EXCLUDED or 'maintenance' in rel.parts or p.name=='r22-bootstrap.yml':continue
            if p.name in {'SOURCE_COMMIT.txt','SHA256SUMS.txt'}:continue
            z.write(p,rel.as_posix())
            manifest.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+rel.as_posix())
        record=(args.source_commit+'\n').encode()
        z.writestr('SOURCE_COMMIT.txt',record)
        manifest.append(hashlib.sha256(record).hexdigest()+'  SOURCE_COMMIT.txt')
        z.writestr('SHA256SUMS.txt','\n'.join(manifest)+'\n')
    with ZipFile(args.output) as z:
        if z.testzip() is not None:raise SystemExit('ZIP integrity failure')
        for row in z.read('SHA256SUMS.txt').decode().splitlines():
            expected,name=row.split('  ',1)
            if hashlib.sha256(z.read(name)).hexdigest()!=expected:raise SystemExit('Manifest mismatch: '+name)
        if any(Path(n).suffix.lower() in EXCLUDED for n in z.namelist()):raise SystemExit('Excluded binary in package')
    print(args.output)
    print('SHA256 '+hashlib.sha256(args.output.read_bytes()).hexdigest())
    print(str(len(manifest))+' independently hashed files; no font binaries')

if __name__=='__main__':main()
