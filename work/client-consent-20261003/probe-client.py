"""Actual mini consumer: fake operator changes genuine native frames, never submits."""
import json,os,struct,subprocess,socket,threading,hashlib
from pathlib import Path
root=Path('/home/hbox/workbox/codex-client-consent-20261003/evidence/client-r1');root.mkdir(parents=True,exist_ok=True)
config=Path('/home/hbox/workbox/codex-agreement-20261003/evidence/four-source-operator-r1/host-settings-0.json')
consent='/tank/dregg-build/codex-client-consent-native-20261003/minidregg-client-consent'
reader='/tank/dregg-build/codex-runtime-reader-native-20261003/minidregg-source-agreement-reader-r2'
mini='/tank/dregg-build/codex-client-consent-rust-20261003/target/release/mini'
key='/home/hbox/workbox/codex-runtime-lieutenant-20261003/evidence/four-source-keys-r1/subject-7.seed'
source=Path('/home/hbox/workbox/codex-resident-context-20261003/evidence/native-context-four-source-r1/workspace/sources/create-context-workdesk.authoring/g0001/source.json')
def exact(stream,n):
 out=bytearray()
 while len(out)<n:
  b=stream.recv(n-len(out)) if isinstance(stream,socket.socket) else stream.read(n-len(out))
  if not b:raise EOFError()
  out.extend(b)
 return bytes(out)
def kind(name,body):return struct.pack('<H',len(name))+name.encode()+body
def nat(n):
 out=bytearray()
 while n:out.append(n%255);n//=255
 return bytes(out)+b'\xff'
class Native:
 def __init__(self,exe,label):
  self.log=(root/(label+'.stderr')).open('wb');self.p=subprocess.Popen([exe,str(config),'stdio'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.log)
 def call(self,op,body):
  wire=bytes([op])+body;self.p.stdin.write(struct.pack('<I',len(wire))+wire);self.p.stdin.flush()
  return exact(self.p.stdout,struct.unpack('<I',exact(self.p.stdout,4))[0])
 def close(self):self.p.stdin.close();self.p.wait(timeout=10);self.log.close()
results=[]
for mode in ['challenge-header','challenge-profile','plan-header','plan-profile','plan-role','honest']:
 directory=root/mode;directory.mkdir(exist_ok=True)
 address=Path('/tmp/consent-'+str(os.getpid())+'-'+mode+'.sock')
 server=socket.socket(socket.AF_UNIX);server.bind(str(address));server.listen();server.settimeout(.5)
 native=Native(reader,mode+'-operator');codec=Native(consent,mode+'-codec');ops=[];failures=[];stop=threading.Event()
 def inspect(name,b):
  frame=codec.call(8,kind(name,b));assert frame[0]==8,frame[:200];return json.loads(frame[1:])
 def change_field(b,name,field,value,new):
  old=nat(value);at=0
  while True:
   at=b.find(old,at)
   if at<0:raise RuntimeError('cannot mutate native metadata')
   altered=b[:at]+nat(new)+b[at+len(old):]
   try:
    if int(inspect(name,altered)[field])==new:return altered
   except Exception:pass
   at+=len(old)
 def serve():
  try:
   while not stop.is_set():
    try:connection,_=server.accept()
    except socket.timeout:continue
    with connection:
     n=struct.unpack('<I',exact(connection,4))[0];envelope=exact(connection,n)
     width=struct.unpack('<I',envelope[1:5])[0];end=5+width
     assert envelope[0]==2 and envelope[5:end]==config.read_bytes()
     assert envelope[end:end+32]==hashlib.sha256(Path(reader).read_bytes()).digest()
     op=envelope[end+32];payload=envelope[end+33:];ops.append(op)
     assert op in [4,1],('pure codec or submit reached operator',op)
     frame=native.call(op,payload);assert frame[0]==op,frame[:300]
     body=frame[1:]
     if op==4 and mode.startswith('challenge'):
      view=inspect('challenge',body)
      if mode=='challenge-profile':body=change_field(body,'challenge','semantics',int(view['semantics']),int(view['semantics'])+1)
      else:
       header=bytes.fromhex(view['headers'][0]);assert body.count(header)==1
       body=body.replace(header,header[:-1]+bytes([header[-1]^1]),1)
     if op==1 and mode.startswith('plan'):
      view=inspect('plan',body)
      if mode=='plan-profile':body=change_field(body,'plan','semantics',int(view['semantics']),int(view['semantics'])+1)
      else:
       slot=next(s for s in view['slots'] if int(s['role'])>0);header=bytes.fromhex(slot['header'])
       if mode=='plan-header':body=body.replace(header,header[:-1]+bytes([header[-1]^1]),1)
       else:
        old=nat(int(slot['role']))+nat(int(slot['index']))+nat(len(header))+header
        new=nat(int(slot['role'])+10)+nat(int(slot['index']))+nat(len(header))+header
        assert body.count(old)==1;body=body.replace(old,new,1);assert inspect('plan',body)['slots']!=view['slots']
     frame=bytes([op])+body;connection.sendall(struct.pack('<I',len(frame))+frame)
  except Exception as error:failures.append(repr(error))
 worker=threading.Thread(target=serve);worker.start()
 env={**os.environ,'MINI_LOCAL_HOST':reader,'MINI_CONSENT_HOST':consent,'MINI_CONSENT_CONFIG':str(config)}
 try:
  result=subprocess.run([mini,'submit','--host',reader,'--config',str(config),'--intent',str(source),'--intent-kind','birth-intent','--prepare-only','true','--key',key,'--dir',str(directory/'attempt'),'--socket',str(address)],env=env,capture_output=True,timeout=90)
  (directory/'stdout').write_bytes(result.stdout);(directory/'stderr').write_bytes(result.stderr)
  assert not failures,failures
  attempt=directory/'attempt'
  assert not any(op in ops for op in [7,8,9,10,11,2]),ops
  if mode=='honest':
   assert result.returncode==0,result.stderr[-1500:];assert (attempt/'call.bin').exists()
  else:
   assert result.returncode!=0 and b'local consent refused before signing' in result.stderr,result.stderr[-1500:]
   assert not (attempt/'call.bin').exists() and not (attempt/'transaction-signatures.bin').exists()
   if mode.startswith('challenge'):assert not (attempt/'observation-signatures.bin').exists() and not (attempt/'observation-signatures.json').exists()
  results.append({'case':mode,'exit':result.returncode,'remoteOperations':ops,'callCreated':(attempt/'call.bin').exists(),'transactionSignaturesCreated':(attempt/'transaction-signatures.bin').exists(),'observationSignaturesCreated':(attempt/'observation-signatures.bin').exists()})
 finally:
  stop.set();worker.join(timeout=2);server.close();address.unlink();native.close();codec.close()
(root/'RESULTS.json').write_text(json.dumps({'results':results,'sourceMutation':False,'nativeOnlySemantics':True},indent=2)+'\n')
print('ACTUAL RUST CONSUMER PASS '+str(len(results))+' cases')
for row in results:print('PASS '+row['case']+' '+str(row))
