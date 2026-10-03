#!/usr/bin/env python3
"""Refresh locator metadata only. Never imports prompt/transcript bodies or writes archives."""
import hashlib, json
from pathlib import Path
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parents[1]
WORKBOX = Path('/Users/ember/workbox/mini-private-capacity-review-20261002')
ARCHIVE = ROOT / 'archive/2026-10-03'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path, data): path.write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n')
files = ['intent-may-june-inventory-all.json', 'intent-may-june-unique-prompts.json', 'intent-may-june-text-dedup.json', 'intent-may-june-undated-prompts.json', 'intent-pre-may-origin-leads.json', 'july-august-session-inventory.json', 'july-august-unique-prompt-groups.json', 'july-august-domain-prompt-groups.json', 'july-august-read-core-evidence.json', 'july-august-session-ancestry.json', 'july-august-prior-history-echoes.json', 'july-august-index-only-sources.json', 'sept-oct-session-inventory-all.json', 'sept-oct-prompt-extraction-results.json', 'DOCUVERSE-DEOS-CONSTRUCTION-20261003.txt', 'docuverse-deos-native-results.json']
files += [p.name for p in sorted(WORKBOX.glob('intent-context-*.json'))]
records=[]
for name in files:
 p=WORKBOX/name
 records.append({'path':str(p),'exists':p.exists(),'bytes':p.stat().st_size if p.exists() else None,'sha256':sha(p) if p.exists() else None,'custody':'external_private; reference only; not imported','read_status':'metadata inventory; no claim full semantic reading'})
dirs=[]
for name in ['intent-may-june-prompts','july-august-prompts','sept-oct-prompts','docuverse-deos-source']:
 p=WORKBOX/name; fs=[f for f in p.rglob('*') if f.is_file()] if p.exists() else []
 dirs.append({'path':str(p),'exists':p.exists(),'files':len(fs),'bytes':sum(f.stat().st_size for f in fs),'read_status':'file names/sizes inspected; not all bodies read'})
save(ROOT/'catalog/corpora.json',{'generated_utc':datetime.now(timezone.utc).isoformat(),'files':records,'directories':dirs,'warning':'Prompt bodies remain external. File availability proves custody, not truth or authorship.'})
periods={}
sets={}
for period in ['MAY-JUNE','JULY-AUGUST','SEPTEMBER-OCTOBER']:
 p=ARCHIVE/f'INTENT-{period}-COVERAGE-20261003.json'; d=json.loads(p.read_text()); rows=d.get('sessions',d.get('sources_and_sessions',[])); keys={s.get('cv_id',s.get('cv_locator',s.get('harness','')+':'+str(s.get('id','')))) for s in rows}; sets[period]=keys
 raw=[s.get('path',s.get('source_path')) for s in rows]
 if period=='MAY-JUNE': ext=[str(WORKBOX/'intent-may-june-prompts'/f"{s['harness']}-{s['id']}.json") for s in rows]
 else: ext=[s.get('prompt_extraction_path',s.get('extracted_prompts_file')) for s in rows]
 periods[period]={'coverage_artifact':str(p),'sha256':sha(p),'catalog_rows':len(rows),'distinct_session_keys':len(keys),'source_paths_declared':sum(bool(x) for x in raw),'source_paths_existing':sum(bool(x) and Path(x).exists() for x in raw),'extraction_paths_declared_or_derived':sum(bool(x) for x in ext),'extraction_paths_existing':sum(bool(x) and Path(x).exists() for x in ext),'declared_counts':d.get('counts',d.get('totals')),'declared_limits':d.get('limitations',d.get('limits',d.get('gaps')))}
union=set.union(*sets.values()); overlaps=[]
for k in sorted(union):
 ps=[p for p,ks in sets.items() if k in ks]
 if len(ps)>1: overlaps.append({'cv_locator':k,'period_inventories':ps,'meaning':'same catalog source overlaps discovery windows; no independent human endorsement inferred'})
# Exact body identity is only navigation. It is not deduplication of independent human acts.
may=json.loads((WORKBOX/'intent-may-june-unique-prompts.json').read_text()); july=json.loads((WORKBOX/'july-august-domain-prompt-groups.json').read_text())
bodysets={'MAY-JUNE':{hashlib.sha256(x['text'].encode()).hexdigest() for x in may},'JULY-AUGUST':{hashlib.sha256(x['text'].encode()).hexdigest() for x in july}}
septd=json.loads((ARCHIVE/'INTENT-SEPTEMBER-OCTOBER-COVERAGE-20261003.json').read_text()); bodies=set(); counted_rows=0
for s in septd['sessions']:
 if s['disposition']!='core development intent': continue
 p=Path(s['prompt_extraction_path']); excluded={x['index'] for x in s['excluded_rows']}; dup={x['index'] for x in s['duplicates'] if 'index' in x}
 for x in json.loads(p.read_text()):
  if x['index'] in excluded or x['index'] in dup: continue
  bodies.add(hashlib.sha256(x['text'].encode()).hexdigest()); counted_rows+=1
bodysets['SEPTEMBER-OCTOBER']=bodies
pairs=[]
for i,a in enumerate(bodysets):
 for b in list(bodysets)[i+1:]: pairs.append({'periods':[a,b],'same_exact_body_hashes':len(bodysets[a]&bodysets[b]),'meaning':'literal text recurrence only, no certified common ancestry or independent authorship'})
save(ROOT/'coverage/consolidated.json',{'generated_utc':datetime.now(timezone.utc).isoformat(),'basis':'immutable initial reports plus external file availability/body hash navigation; metadata audit only','periods':periods,'catalog_union_distinct_session_keys':len(union),'catalog_overlapping_session_keys':len(overlaps),'body_identity_intersections':pairs,'sept_core_candidate_rows_after_explicit_exclusions':counted_rows,'warning':'Different relevance/selection/dedup/read units forbid adding historical prompt counts. Candidate rows do not certify human authorship; no new full-corpus reading claimed.'})
save(ROOT/'coverage/session-overlap.json',overlaps)
print('Updated corpora/consolidated/session-overlap metadata. Unique catalog sources:',len(union),'overlapping:',len(overlaps))
