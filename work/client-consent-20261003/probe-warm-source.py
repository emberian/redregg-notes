"""Adversarial changes occur ONLY in owned sqlite backup fixtures."""
import json, sqlite3, struct, subprocess, os
from pathlib import Path
root=Path('/home/hbox/workbox/codex-client-consent-20261003/evidence/warm-source-r1'); root.mkdir(mode=0o700, parents=True, exist_ok=True)
original=Path('/home/hbox/workbox/codex-agreement-20261003/evidence/four-source-operator-r1/host-settings-0.json')
settings=json.loads(original.read_text()); fixture=root.parent/'specialized-native-r1'
public=Path('/home/hbox/workbox/codex-runtime-lieutenant-20261003/evidence/four-source-r1/subject-7.pub').read_bytes()
command=(fixture/'possession-command.bin').read_bytes(); candidate=(fixture/'possession-frame.bin').read_bytes()
def pair(a,b): return struct.pack('<I',len(a))+a+b
payload=pair(command,pair(json.dumps({'subject':'7','publicKey':public.hex()}).encode(),candidate))
def request(p):
 wire=bytes([226])+payload; p.stdin.write(struct.pack('<I',len(wire))+wire); p.stdin.flush()
 first=p.stdout.read(4)
 if not first: return None
 assert len(first)==4
 n=struct.unpack('<I',first)[0]; data=b''
 while len(data)<n:
  part=p.stdout.read(n-len(data)); assert part; data+=part
 return data
results=[]
for case in ['rollback','prefix-rewrite','invalid-suffix']:
 directory=root/case; directory.mkdir(mode=0o700,exist_ok=True); source=directory/'source'; source.mkdir(mode=0o700,exist_ok=True)
 database=source/'forward-link.sqlite3'
 with sqlite3.connect('file:'+settings['storageRoot']+'/forward-link.sqlite3?mode=ro',uri=True) as origin, sqlite3.connect(database) as copy: origin.backup(copy)
 os.chmod(database,0o600)
 anchor=directory/'source.head-anchor'; anchor.write_bytes(Path(settings['storageRoot']+'.head-anchor').read_bytes()); os.chmod(anchor,0o600)
 config={**settings,'storageRoot':str(source)}; path=directory/'config.json'; path.write_text(json.dumps(config)); os.chmod(path,0o600)
 error=(directory/'stderr.log').open('wb')
 p=subprocess.Popen(['/tank/dregg-build/codex-client-consent-core-native-20261003/minidregg-client-consent',str(path),'stdio'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=error)
 try:
  assert request(p)==bytes([226])+candidate, case+' initial verified fixture failed'
  with sqlite3.connect(database) as c:
   lo,hi,count=c.execute('select min(height),max(height),count(*) from durable_log').fetchone(); assert count>0
   if case=='rollback':
    c.execute('delete from durable_log where height=?',(hi,)); c.execute('delete from durable_checkpoint where height>=?',(hi,))
   elif case=='prefix-rewrite':
    record=c.execute('select record from durable_log where height=?',(lo,)).fetchone()[0]; changed=bytes([record[0]^1])+record[1:]
    c.execute('update durable_log set record=? where height=?',(changed,lo))
   else: c.execute('insert into durable_log(height,record,tag) values(?,?,?)',(hi+1,b'not-a-native-entry',b'not-a-source-tag'))
  assert request(p) is None, case+' returned signable bytes after changed source'
  p.stdin.close(); code=p.wait(timeout=20); assert code!=0
  results.append({'case':case,'initialAccepted':True,'postChangeSignableResponse':False,'providerExit':code})
 finally:
  if p.poll() is None: p.kill(); p.wait()
  error.close()
(root/'RESULTS.json').write_text(json.dumps({'results':results,'liveSourceMutation':False,'fixtureCopiesOnly':True,'agreementClaim':False},indent=2)+'\n')
print('NATIVE WARM SOURCE REFUSERS PASS',len(results))
for row in results: print('PASS',row)
