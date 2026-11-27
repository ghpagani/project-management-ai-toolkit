"""Deterministic project review. No network, no external dependencies."""
import argparse
import heapq
import json
import os
import re
import stat
import sys
import tempfile
from decimal import Decimal, localcontext, ROUND_HALF_UP
from pathlib import Path

VERSION = '0.1.0'
MAX_BYTES = 1_000_000
MAX_ROWS = 2000
MAX_EDGES = 20000
MAX_CENTS = 10**14

class Invalid(ValueError):
    pass

def require(ok, code):
    if not ok:
        raise Invalid(code)

def keys(obj, expected):
    require(type(obj) is dict and set(obj) == set(expected.split()), 'INVALID_FIELDS')

def integer(value, lo, hi):
    require(type(value) is int and lo <= value <= hi, 'INVALID_INTEGER')
    return value

def identifier(value, prefix):
    require(type(value) is str and re.fullmatch(prefix + r'[0-9]{3,6}', value) is not None, 'INVALID_ID')
    return value

def rows(value):
    require(type(value) is list and len(value) <= MAX_ROWS, 'INVALID_LIST')
    return value

def unique(items):
    require(len(items) == len(set(items)), 'DUPLICATE_ID')

def object_pairs(pairs):
    result = {}
    for k,v in pairs:
        require(k not in result, 'DUPLICATE_JSON_KEY')
        result[k] = v
    return result

def reject_number(_):
    raise Invalid('NON_INTEGER_JSON_NUMBER')

def parse(raw):
    require(len(raw) <= MAX_BYTES, 'INPUT_TOO_LARGE')
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=object_pairs,
                          parse_float=reject_number, parse_constant=reject_number)
    except (UnicodeError, ValueError, RecursionError) as e:
        if isinstance(e, Invalid):
            raise
        raise Invalid('INVALID_JSON') from None

def safe_input(path):
    # A trusted, access-controlled directory is still required; this is not a sandbox.
    path = Path(path)
    require(not path.is_symlink(), 'INPUT_NOT_REGULAR')
    flags = os.O_RDONLY | getattr(os, 'O_BINARY', 0) | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    require(stat.S_ISREG(path.stat().st_mode), 'INPUT_NOT_REGULAR')
    fd = os.open(path, flags)
    with os.fdopen(fd, 'rb') as f:
        require(stat.S_ISREG(os.fstat(f.fileno()).st_mode), 'INPUT_NOT_REGULAR')
        return parse(f.read(MAX_BYTES + 1))

def schedule(tasks):
    taskmap, deps, children = {}, {}, {}
    edges = 0
    for t in rows(tasks):
        keys(t, 'id duration_days predecessors')
        i = identifier(t['id'], 'T')
        require(i not in taskmap, 'DUPLICATE_ID')
        taskmap[i] = integer(t['duration_days'], 0, 36500)
        ds = [identifier(x,'T') for x in rows(t['predecessors'])]
        unique(ds)
        edges += len(ds)
        require(edges <= MAX_EDGES, 'TOO_MANY_EDGES')
        deps[i] = ds
        children[i] = []
    require(bool(taskmap), 'EMPTY_SCHEDULE')
    for i, ds in deps.items():
        for d in ds:
            require(d in taskmap and d != i, 'INVALID_DEPENDENCY')
            children[d].append(i)
    indegree = {i:len(ds) for i,ds in deps.items()}
    q = [i for i,n in indegree.items() if n==0]; heapq.heapify(q)
    order, es, ef = [], {}, {}
    while q:
        i = heapq.heappop(q); order.append(i)
        es[i] = max((ef[d] for d in deps[i]), default=0)
        ef[i] = es[i] + taskmap[i]
        for c in children[i]:
            indegree[c] -= 1
            if indegree[c]==0: heapq.heappush(q,c)
    require(len(order)==len(taskmap), 'SCHEDULE_CYCLE')
    finish = max(ef.values()); ls,lf = {},{}
    for i in reversed(order):
        lf[i] = min((ls[c] for c in children[i]),default=finish)
        ls[i] = lf[i] - taskmap[i]
    return {'duration_days':finish,'tasks':[{'id':i,'early_start':es[i],'early_finish':ef[i],
        'late_start':ls[i],'late_finish':lf[i],'total_float':ls[i]-es[i],
        'critical':ls[i]==es[i]} for i in sorted(taskmap)]}

def evm(data):
    keys(data, 'currency bac pv ev ac')
    require(type(data['currency']) is str and data['currency'] in ('BRL','USD','EUR'), 'INVALID_CURRENCY')
    bac,pv,ev,ac = [integer(data[k],0,MAX_CENTS) for k in ('bac','pv','ev','ac')]
    require(bac>0 and pv<=bac and ev<=bac, 'INVALID_BASELINE')
    with localcontext() as ctx:
        ctx.prec=50; ctx.rounding=ROUND_HALF_UP
        def ratio(a,b):
            return None if not b else format((Decimal(a)/Decimal(b)).quantize(Decimal('0.0001')), 'f')
        # Calculate from exact amounts, not the rounded displayed CPI.
        eac = None if not ev or not ac else int((Decimal(bac)*Decimal(ac)/Decimal(ev)).quantize(Decimal('1')))
        return {'currency':data['currency'],'unit':'minor_currency_unit','bac':bac,'pv':pv,'ev':ev,'ac':ac,
                'cv':ev-ac,'sv':ev-pv,'cpi':ratio(ev,ac),'spi':ratio(ev,pv),'eac_cpi':eac,
                'etc_cpi':None if eac is None else eac-ac,'vac_cpi':None if eac is None else bac-eac,
                'eac_assumption':'remaining_work_at_current_cost_efficiency'}

def risks(data):
    keys(data,'high_threshold items'); threshold=integer(data['high_threshold'],1,25)
    out=[]
    for r in rows(data['items']):
        keys(r,'id probability impact response_assigned')
        i=identifier(r['id'],'R'); p=integer(r['probability'],1,5); v=integer(r['impact'],1,5)
        require(type(r['response_assigned']) is bool,'INVALID_BOOLEAN')
        out.append({'id':i,'score':p*v,'high':p*v>=threshold,'response_missing':p*v>=threshold and not r['response_assigned']})
    unique([r['id'] for r in out]); return sorted(out,key=lambda r:r['id'])

def raci(data):
    result=[]; ids=[]
    for r in rows(data):
        keys(r,'task_id assignments'); i=identifier(r['task_id'],'T'); ids.append(i)
        people=[]; roles=[]
        for a in rows(r['assignments']):
            keys(a,'role_id code'); people.append(identifier(a['role_id'],'U'))
            require(type(a['code']) is str and a['code'] in ('R','A','C','I','RA'),'INVALID_RACI_CODE'); roles.append(a['code'])
        unique(people)
        nr=sum('R' in x for x in roles); na=sum('A' in x for x in roles)
        result.append({'task_id':i,'responsible_count':nr,'accountable_count':na,'needs_review':nr<1 or na!=1})
    unique(ids); return sorted(result,key=lambda r:r['task_id'])

def review(data):
    keys(data,'schema_version classification project_id schedule evm risks raci')
    require(type(data['schema_version']) is int and data['schema_version']==1,'INVALID_SCHEMA_VERSION')
    require(type(data['classification']) is str and data['classification'] in ('synthetic','public_authorized'),'CLASSIFICATION_BLOCKED')
    pid=identifier(data['project_id'],'P')
    s=schedule(data['schedule']); e=evm(data['evm']); r=risks(data['risks']); a=raci(data['raci'])
    require({x['task_id'] for x in a} <= {x['id'] for x in s['tasks']},'UNKNOWN_RACI_TASK')
    missing=sorted({x['id'] for x in s['tasks']} - {x['task_id'] for x in a})
    return {'engine_version':VERSION,'schema_version':1,'classification':data['classification'],
            'project_id':pid,'schedule':s,'evm':e,'risks':r,'raci':a,'raci_missing_tasks':missing,
            'limitations':['PREVIEW_NOT_CERTIFICATION','DECLARED_CLASSIFICATION_NOT_DLP','CPM_FINISH_START_ZERO_LAG_SINGLE_CALENDAR','HUMAN_REVIEW_REQUIRED']}

def write_report(path, report):
    # Same directory temporary file and atomic hard-link publication, no overwrite.
    # Fail closed if hard links are unsupported. Directory must be trusted/private.
    path=Path(path); require(path.suffix.lower()=='.json','OUTPUT_EXTENSION')
    if path.exists() or path.is_symlink(): raise Invalid('OUTPUT_EXISTS')
    fd,tmp=tempfile.mkstemp(prefix='.pm-review-',dir=path.parent)
    try:
        with os.fdopen(fd,'w',encoding='utf-8',newline='\n') as f:
            json.dump(report,f,indent=2,sort_keys=True,ensure_ascii=True); f.write('\n'); f.flush(); os.fsync(f.fileno())
        os.link(tmp,path)
    finally:
        os.unlink(tmp)

def main(argv=None):
    parser=argparse.ArgumentParser(description='Offline preview; synthetic or authorized public data only. Never use confidential data.')
    parser.add_argument('--input',required=True); parser.add_argument('--out',required=True)
    args=parser.parse_args(argv)
    try:
        result=review(safe_input(args.input)); write_report(args.out,result)
    except Invalid as e:
        print('Review blocked: '+str(e),file=sys.stderr); return 2
    except (OSError,RecursionError,ValueError,TypeError):
        print('Review blocked: IO_OR_INPUT_ERROR',file=sys.stderr); return 3
    print('Report written. Human review required.'); return 0

if __name__=='__main__': sys.exit(main())
