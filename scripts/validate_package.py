import json, re
from build_release import ROOT,PLUGIN,SKILL,VERSION,SKILL_FILES,PLUGIN_FILES

def validate():
    a=json.loads((PLUGIN/'plugin.json').read_text()); b=json.loads((PLUGIN/'.claude-plugin/plugin.json').read_text())
    if a!=b or a['version']!=VERSION or a['name']!=SKILL.name: raise ValueError('Manifest mismatch')
    if f'# Project Management AI Toolkit v{VERSION}' not in (SKILL/'SKILL.md').read_text(encoding='utf-8').splitlines(): raise ValueError('Heading mismatch')
    if f"VERSION = '{VERSION}'" not in (SKILL/'scripts/review.py').read_text().splitlines(): raise ValueError('Engine mismatch')
    for p in PLUGIN_FILES:
        x=PLUGIN/p
        if x.resolve()!=x or not x.is_file(): raise ValueError('Invalid package file')
    for p in SKILL_FILES:
        if p.endswith('.md'):
            for ref in re.findall(r'`((?:references|scripts|templates|examples)/[A-Za-z0-9_.\-/]+)`',(SKILL/p).read_text(encoding='utf-8')):
                if ref not in SKILL_FILES: raise ValueError('Missing reference')
    for path in ('.agents/plugins/marketplace.json','.claude-plugin/marketplace.json'):
        item=json.loads((ROOT/path).read_text())['plugins'][0]; src=item['source']; src=src['path'] if isinstance(src,dict) else src
        if item['name']!=SKILL.name or (ROOT/src).resolve()!=PLUGIN: raise ValueError('Marketplace mismatch')

if __name__=='__main__': validate(); print('Package structure passed (not host certification).')
