#!/usr/bin/env python3
"""Package current R2.2.1 outputs plus buildable sources, without fonts or test samples."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import argparse,hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={'.ttf','.otf','.woff','.woff2','.eot','.zip','.pyc'}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source-commit',required=True)
    ap.add_argument('--output',type=Path,default=ROOT/'CHRONOCAIRN_R2_2_1_Verified.zip');args=ap.parse_args()
    if not re.fullmatch('[0-9a-f]{40}',args.source_commit):ap.error('Provide an exact commit SHA')
    report=json.loads((ROOT/'reports/r221-technical-check.json').read_text())
    assert report['pass'],'Technical check must pass before packaging'
    tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
    paths={ROOT/p for p in tracked}
    current={ROOT/'CHRONOCAIRN_Final_Complete.pdf',ROOT/'CHRONOCAIRN_OMNIBUS_R2_2_1.pdf'}
    current.update((ROOT/'downloads').glob('CHRONOCAIRN_R2_2_1_*.pdf'))
    paths.update(current);paths.update(p for p in (ROOT/'reports').glob('r221-*') if p.is_file())
    manifest=[]
    with ZipFile(args.output,'w',ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(paths):
            rel=p.relative_to(ROOT)
            if not p.is_file() or p.suffix.lower() in EXCLUDED or 'maintenance' in rel.parts or 'r221-form-samples' in rel.parts:continue
            if p.name in {'SOURCE_COMMIT.txt','SHA256SUMS.txt','r221-bootstrap.yml'}:continue
            if p.suffix.lower()=='.pdf' and p not in current:continue
            z.write(p,rel.as_posix());manifest.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+rel.as_posix())
        b=(args.source_commit+'\n').encode();z.writestr('SOURCE_COMMIT.txt',b);manifest.append(hashlib.sha256(b).hexdigest()+'  SOURCE_COMMIT.txt')
        z.writestr('SHA256SUMS.txt','\n'.join(manifest)+'\n')
    with ZipFile(args.output) as z:
        assert z.testzip() is None
        for row in z.read('SHA256SUMS.txt').decode().splitlines():
            h,n=row.split('  ',1);assert hashlib.sha256(z.read(n)).hexdigest()==h,n
        assert not any(Path(n).suffix.lower() in EXCLUDED for n in z.namelist())
    print(args.output);print(hashlib.sha256(args.output.read_bytes()).hexdigest());print(len(manifest),'hashed files')
if __name__=='__main__':main()
