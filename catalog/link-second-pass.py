#!/usr/bin/env python3
"""Index peer-owned research and reading metadata without changing it or summing counts."""
import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1]
records=[]
for sub in ['intent','replays','landscape','designs']:
 for p in sorted((R/sub).glob('*')):
  if not p.is_file(): continue
  record={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'catalog_read_scope':'existence/hash/JSON metadata only; substantive reading belongs to author'}
  if p.suffix=='.json':
   data=json.loads(p.read_text()); record['metadata_keys']=list(data) if isinstance(data,dict) else None
   if isinstance(data,dict):
    for k in ['owner','method','focal_windows_read','limits','source_pins']: 
     if k in data: record[k]=data[k]
    if isinstance(data.get('focal_windows'),list):
     pairs={(x['session'],x['focal_index']) for x in data['focal_windows']}
     record['focal_unique_session_index_pairs']=len(pairs)
     record['focal_locators']=[{'cv_locator':s,'cv_index':i} for s,i in sorted(pairs)]
  records.append(record)
(R/'coverage/second-pass-links.json').write_text(json.dumps({'generated_utc':datetime.now(timezone.utc).isoformat(),'warning':'Author-owned mutable research hash pins at this time only. Different read units are preserved; counts are never summed. File hashing is not semantic reading.','records':records},indent=2)+'\n')
print('Linked',len(records),'peer artifacts without modifying them.')
