"""Native canonical fixtures -> real warm native consent consumer; no source submit."""
import json,struct,subprocess
from pathlib import Path
root=Path('/home/hbox/workbox/codex-client-consent-20261003/evidence/specialized-native-r1')
config='/home/hbox/workbox/codex-agreement-20261003/evidence/four-source-operator-r1/host-settings-0.json'
exe='/tank/dregg-build/codex-client-consent-core-native-20261003/minidregg-client-consent'
public=Path('/home/hbox/workbox/codex-runtime-lieutenant-20261003/evidence/four-source-r1/subject-7.pub').read_bytes()
def pair(a,b):return struct.pack('<I',len(a))+a+b
def exact(s,n):
 b=bytearray()
 while len(b)<n:
  chunk=s.read(n-len(b))
  if not chunk:raise EOFError('consent provider ended')
  b.extend(chunk)
 return bytes(b)
log=(root/'consumer.stderr').open('wb');p=subprocess.Popen([exe,config,'stdio'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=log);results=[]
def call(op,body,accepted,label):
 wire=bytes([op])+body;p.stdin.write(struct.pack('<I',len(wire))+wire);p.stdin.flush()
 frame=exact(p.stdout,struct.unpack('<I',exact(p.stdout,4))[0])
 assert frame[0]==(op if accepted else 255),(label,frame[:500])
 results.append(label);return frame[1:]
try:
 request=(root/'clock-request.bin').read_bytes();plan=(root/'clock-plan.bin').read_bytes()
 checked=call(224,pair(bytes([126])+request,plan),True,'canonical current-source native clock plan accepted');assert checked==plan
 for filename,label in [('clock-changed-profile.bin','changed specialized profile refused'),('clock-changed-header.bin','changed specialized header refused')]:call(224,pair(bytes([126])+request,(root/filename).read_bytes()),False,label)
 call(224,pair(bytes([126])+(root/'clock-changed-request.bin').read_bytes(),plan),False,'changed retained specialized request refused')
 call(224,pair(bytes([42])+request,plan),False,'unsupported specialized family refused without fallback')
 command=(root/'possession-command.bin').read_bytes();candidate=(root/'possession-frame.bin').read_bytes()
 selected=json.dumps({'subject':'7','publicKey':public.hex()}).encode()
 checked=call(226,pair(command,pair(selected,candidate)),True,'native possession frame bound to selected key subject domain profile and whole command');assert checked==candidate
 call(226,pair(command,pair(selected,candidate[:-1]+bytes([candidate[-1]^1]))),False,'changed raw possession header refused')
 wrong=json.dumps({'subject':'8','publicKey':public.hex()}).encode();call(226,pair(command,pair(wrong,candidate)),False,'wrong possession subject refused')
 wrong=json.dumps({'subject':'7','publicKey':bytes([public[0]^1]).hex()+public[1:].hex()}).encode();call(226,pair(command,pair(wrong,candidate)),False,'wrong possession key refused')
 (root/'CONSENT-RESULTS.json').write_text(json.dumps({'results':results,'sourceMutation':False,'signaturesCreated':False,'scope':'typed production native fixture/planner plus real native consent consumer; not admission or submit'},indent=2)+'\n')
 print('NATIVE SPECIALIZED CONSUMER PASS '+str(len(results)))
 for result in results:print('PASS '+result)
finally:p.stdin.close();p.wait(timeout=10);log.close()
