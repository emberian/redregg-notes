"""Adversarial frame driver: semantics/codecs remain the two native Lean ELFs."""
import json,os,struct,subprocess
from pathlib import Path
root=Path('/home/hbox/workbox/codex-client-consent-20261003/evidence/native-r3');root.mkdir(parents=True,exist_ok=True)
config='/home/hbox/workbox/codex-agreement-20261003/evidence/four-source-operator-r1/host-settings-0.json'
consent='/tank/dregg-build/codex-client-consent-native-20261003/minidregg-client-consent'
reader='/tank/dregg-build/codex-runtime-reader-native-20261003/minidregg-source-agreement-reader-r2'
key=Path('/home/hbox/workbox/codex-runtime-lieutenant-20261003/evidence/four-source-keys-r1/subject-7.pkcs8')
public=Path('/home/hbox/workbox/codex-runtime-lieutenant-20261003/evidence/four-source-r1/subject-7.pub').read_bytes()
def pair(a,b):return struct.pack('<I',len(a))+a+b
def kind(name,b):return struct.pack('<H',len(name))+name.encode()+b
def exact(stream,n):
 b=bytearray()
 while len(b)<n:
  chunk=stream.read(n-len(b))
  if not chunk:raise RuntimeError('native provider ended')
  b.extend(chunk)
 return bytes(b)
class Session:
 def __init__(self,exe):
  self.log=(root/(Path(exe).name+'.stderr')).open('wb');self.p=subprocess.Popen([exe,config,'stdio'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.log)
 def call(self,op,data,accept=True):
  wire=bytes([op])+data;self.p.stdin.write(struct.pack('<I',len(wire))+wire);self.p.stdin.flush()
  n=struct.unpack('<I',exact(self.p.stdout,4))[0];reply=exact(self.p.stdout,n)
  if accept and reply[0]!=op:raise RuntimeError('native refusal '+str(op)+' '+repr(reply[:500]))
  if not accept and reply[0]!=255:raise RuntimeError('altered native frame received consent')
  return reply[1:]
 def close(self):self.p.stdin.close();self.p.wait(timeout=10);self.log.close()
c=Session(consent);r=Session(reader);results=[]
def author(name,value):return c.call(7,kind(name,json.dumps(value,separators=(',',':')).encode()))
def inspect(name,value):return json.loads(c.call(8,kind(name,value)))
def sign(data,stem):
 source=root/(stem+'.bin');source.write_bytes(data);signature=root/(stem+'.signature')
 subprocess.run(['openssl','pkeyutl','-sign','-rawin','-keyform','DER','-inkey',str(key),'-in',str(source),'-out',str(signature)],check=True,capture_output=True)
 return signature.read_bytes()
def refuse(op,data,label):c.call(op,data,False);results.append(label)
def nat(value):
 out=bytearray()
 while value:out.append(value%255);value//=255
 return bytes(out)+b'\xff'
def change_field(data,kind_name,field,value,new):
 old=nat(value);offset=0
 while True:
  offset=data.find(old,offset)
  if offset<0:raise RuntimeError('cannot isolate native metadata field')
  changed=data[:offset]+nat(new)+data[offset+len(old):]
  try:
   if int(inspect(kind_name,changed)[field])==new:return changed
  except Exception:pass
  offset+=len(old)
def observe(wanted,stem):
 assert c.call(220,pair(wanted,pair(public,b'')))==wanted
 sig=sign(wanted,stem+'-intent')
 challenge=r.call(4,pair(wanted,sig));headers=json.loads(c.call(221,pair(wanted,pair(public,pair(sig,challenge)))))
 view=inspect('challenge',challenge)
 refuse(221,pair(wanted,pair(public,pair(sig,challenge[:-1]+bytes([challenge[-1]^1])))),stem+' changed challenge bytes refused')
 modified=change_field(challenge,'challenge','semantics',int(view['semantics']),int(view['semantics'])+1)
 changed_view=inspect('challenge',modified);assert changed_view['semantics']!=view['semantics']
 refuse(221,pair(wanted,pair(public,pair(sig,modified))),stem+' changed profile refused')
 if headers:
  header=bytes.fromhex(headers[0]);assert challenge.count(header)==1
  altered=challenge.replace(header,header[:-1]+bytes([header[-1]^1]),1)
  refuse(221,pair(wanted,pair(public,pair(sig,altered))),stem+' changed ordered header refused')
 refuse(220,pair(wanted,pair(bytes([public[0]^1])+public[1:],b'')),stem+' wrong custody key refused')
 signatures=[sign(bytes.fromhex(h),stem+'-observe-'+str(n)).hex() for n,h in enumerate(headers)]
 sigs=c.call(9,json.dumps(signatures).encode());signed=c.call(10,pair(challenge,sigs));return sig,challenge,signed
try:
 query={'subject':'7','nonce':'98765001','purpose':{'type':'query','kind':'object','target':'10','view':'resource'},'grants':[{'kind':'object','target':'10','capability':'46'}]}
 wanted=author('intent',query);sig,challenge,signed=observe(wanted,'query')
 changed={**query,'nonce':'98765002'};foreign=author('intent',changed);foreign_sig=sign(foreign,'foreign-author')
 foreign_challenge=r.call(4,pair(foreign,foreign_sig))
 refuse(221,pair(wanted,pair(public,pair(sig,foreign_challenge))),'changed author intent refused')
 results.append('legitimate query consent and native assembly accepted')
 birth_source=json.loads(Path('/home/hbox/workbox/codex-resident-context-20261003/evidence/native-context-four-source-r1/workspace/sources/create-context-workdesk.authoring/g0001/source.json').read_text())
 wanted=author('birth-intent',birth_source);sig,challenge,signed=observe(wanted,'birth')
 plan=r.call(1,signed);headers=json.loads(c.call(222,pair(wanted,pair(public,plan))));view=inspect('plan',plan)
 modified=change_field(plan,'plan','semantics',int(view['semantics']),int(view['semantics'])+1);assert inspect('plan',modified)['semantics']!=view['semantics']
 refuse(222,pair(wanted,pair(public,modified)),'birth changed plan profile refused')
 chosen=next(slot for slot in view['slots'] if int(slot['role'])>0);header=bytes.fromhex(chosen['header'])
 altered=plan.replace(header,header[:-1]+bytes([header[-1]^1]),1);assert altered!=plan
 refuse(222,pair(wanted,pair(public,altered)),'birth changed transaction header refused')
 slot=nat(int(chosen['role']))+nat(int(chosen['index']))+nat(len(header))+header
 assert plan.count(slot)==1
 changedslot=nat(int(chosen['role'])+10)+nat(int(chosen['index']))+nat(len(header))+header
 altered=plan.replace(slot,changedslot);alteredview=inspect('plan',altered)
 assert alteredview['slots']!=view['slots']
 refuse(222,pair(wanted,pair(public,altered)),'birth changed role/index incidence refused')
 signatures=[sign(bytes.fromhex(h),'birth-transaction-'+str(n)).hex() for n,h in enumerate(headers)]
 sigs=c.call(9,json.dumps(signatures).encode());call=c.call(11,pair(plan,sigs));(root/'birth-call.bin').write_bytes(call)
 results.append('legitimate birth finalization whole-plan consent and native call assembly accepted')
 # Preparation of an ordinary source operation exercises the non-birth planner.
 ordinary={'subject':'7','nonce':'98765003','purpose':{'type':'prepare','draft':{'type':'renounce-source','command':{'subject':'7','nonce':'98765003','kind':'account','capability':'41'}}},'grants':[]}
 wanted=author('intent',ordinary);sig,challenge,signed=observe(wanted,'ordinary')
 plan=r.call(1,signed);headers=json.loads(c.call(222,pair(wanted,pair(public,plan))));assert headers
 results.append('legitimate ordinary renunciation whole-plan consent accepted; not submitted')
 (root/'RESULTS.json').write_text(json.dumps({'results':results,'sourceMutation':False,'scope':'actual Lean provider/read-only reader; no submit; full-peer only'},indent=2)+'\n')
 print('NATIVE ADVERSARIAL CONSENT PASS '+str(len(results))+' cases')
 for result in results:print('PASS '+result)
finally:c.close();r.close()
