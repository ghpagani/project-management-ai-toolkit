"""Build deterministic allowlisted packages; never include arbitrary files."""
import argparse, hashlib, os, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PLUGIN=ROOT/'plugins/project-management-ai'
SKILL=PLUGIN/'skills/project-management-ai'
VERSION='0.1.0'
SKILL_FILES=('SKILL.md','LICENSE','scripts/review.py','examples/project.json','references/data-contract.md','references/methodology.md','references/security.md','templates/review-report.md')
PLUGIN_FILES=('LICENSE','plugin.json','.claude-plugin/plugin.json')+tuple('skills/project-management-ai/'+p for p in SKILL_FILES)

def build(out):
    out=Path(out); out.mkdir(parents=True,exist_ok=False)
    sums=[]
    for kind,base,paths in [('skill',SKILL,SKILL_FILES),('plugin',PLUGIN,PLUGIN_FILES)]:
        dest=out/f'project-management-ai-{kind}-{VERSION}.zip'
        with zipfile.ZipFile(dest,'x',compression=zipfile.ZIP_STORED) as z:
            for p in sorted(paths):
                source=base/p
                if source.resolve()!=source or not source.is_file(): raise ValueError('Unsafe package source')
                info=zipfile.ZipInfo('project-management-ai/'+p,(2026,1,1,0,0,0))
                info.create_system=3; info.external_attr=0o100644<<16
                z.writestr(info,source.read_bytes())
        sums.append(f'{hashlib.sha256(dest.read_bytes()).hexdigest()}  {dest.name}')
    (out/'SHA256SUMS').write_bytes(('\n'.join(sorted(sums))+'\n').encode())

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--out-dir',required=True); args=parser.parse_args(); build(args.out_dir)
