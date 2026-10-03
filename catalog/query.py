#!/usr/bin/env python3
"""Navigate external prompt evidence. Default output has locators, never prompt bodies."""
import argparse, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
W=Path('/Users/ember/workbox/mini-private-capacity-review-20261002')
a=argparse.ArgumentParser(description=__doc__)
a.add_argument('--period',choices=['may','july','sept','all'],default='all')
a.add_argument('--term',help='case-insensitive literal search of external bodies')
a.add_argument('--session',help='harness:UUID or unique UUID prefix')
a.add_argument('--index',type=int,help='cv message index; requires --session')
a.add_argument('--hash',help='exact body SHA256 prefix')
a.add_argument('--limit',type=int,default=12)
a.add_argument('--text',action='store_true',help='print matching external prompt body (private terminal output only)')
args=a.parse_args()
if not (args.term or args.session or args.hash): a.error('give --term, --session, or --hash')
if args.index is not None and not args.session: a.error('--index requires --session')
def groups():
 if args.period in ['may','all']:
  path=W/'intent-may-june-unique-prompts.json'
  for number,x in enumerate(json.loads(path.read_text())):
   ls=[{'session':s['harness']+':'+s['id'],'index':s['index'],'timestamp':x['timestamp']} for s in x['sources']]
   yield 'may',path,number,x['text'],ls,'exact timestamp+text group; selected bodies/excerpts only; authorship unaudited'
 if args.period in ['july','all']:
  path=W/'july-august-domain-prompt-groups.json'
  read=set(json.loads((ROOT/'archive/2026-10-03/INTENT-JULY-AUGUST-COVERAGE-20261003.json').read_text())['read_groups_full'])
  for x in json.loads(path.read_text()):
   yield 'july',path,x['num'],x['text'],x['locators'],'historical full body read' if x['num'] in read else 'not in historical conservative full-read set'
 if args.period in ['sept','all']:
  coverage=json.loads((ROOT/'archive/2026-10-03/INTENT-SEPTEMBER-OCTOBER-COVERAGE-20261003.json').read_text())
  for s in coverage['sessions']:
   if s['disposition'] not in ['core development intent','adjacent; scoped relevance review']: continue
   path=Path(s['prompt_extraction_path']); excluded={x['index'] for x in s['excluded_rows']}
   for number,x in enumerate(json.loads(path.read_text())):
    yield 'sept',path,number,x['text'],[{'session':s['cv_locator'],'index':x['index'],'timestamp':x.get('timestamp')}], 'explicitly excluded row; inspect reason in coverage' if x['index'] in excluded else s['read_scope']
count=0
for period,path,group,body,locators,read in groups():
 if args.term and args.term.lower() not in body.lower(): continue
 h=hashlib.sha256(body.encode()).hexdigest()
 if args.hash and not h.startswith(args.hash): continue
 if args.session:
  locators=[x for x in locators if args.session in x['session'] and (args.index is None or x['index']==args.index)]
  if not locators: continue
 # Stop with metadata only by default; text is never copied into this repository.
 out={'period':period,'external_artifact':str(path),'group_or_row':group,'body_sha256':h,'body_characters':len(body),'locator_count':len(locators),'locators':locators[:8],'declared_read_scope':read}
 if args.text: out['external_body']=body
 print(json.dumps(out,ensure_ascii=False)); count+=1
 if count>=max(1,args.limit): break
if not count: print('No matching extracted project groups. This is not proof of absence from history.')
