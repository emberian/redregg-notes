"""Actual mini possession consumer with native-produced whole-command frames."""
from pathlib import Path
import json,os,subprocess
root=Path('/home/hbox/workbox/codex-client-consent-20261003/evidence/possession-client-r1');root.mkdir(exist_ok=True)
fixture=Path('/home/hbox/workbox/codex-client-consent-20261003/evidence/specialized-native-r1')
public=Path('/home/hbox/workbox/codex-runtime-lieutenant-20261003/evidence/four-source-r1/subject-7.pub').read_bytes()
command=(fixture/'possession-command.bin').read_bytes();frame=(fixture/'possession-frame.bin').read_bytes()
config='/home/hbox/workbox/codex-agreement-20261003/evidence/four-source-operator-r1/host-settings-0.json'
key='/home/hbox/workbox/codex-runtime-lieutenant-20261003/evidence/four-source-keys-r1/subject-7.seed'
mini='/tank/dregg-build/codex-client-consent-rust-20261003/target/release/mini'
env={**os.environ,'MINI_LOCAL_HOST':'/tank/dregg-build/codex-runtime-reader-native-20261003/minidregg-source-agreement-reader-r2','MINI_CONSENT_HOST':'/tank/dregg-build/codex-client-consent-core-native-20261003/minidregg-client-consent','MINI_CONSENT_CONFIG':config}
results=[]
for mode in ['altered-header','wrong-subject','honest']:
 directory=root/mode;directory.mkdir(mode=0o700,exist_ok=True)
 header=frame if mode!='altered-header' else frame[:-1]+bytes([frame[-1]^1])
 data={'command.bin':command,'command.json':json.dumps({'type':'participant-key-enrollment-v1','canonical':command.hex(),'key':{'publicKey':public.hex(),'subject':'7'}}).encode(),'plan.json':json.dumps({'type':'participant-key-enrollment-plan-v1','commandBytes':command.hex(),'possessionHeader':header.hex()}).encode()}
 for name,body in data.items():p=directory/name;p.write_bytes(body);p.chmod(0o600)
 output=directory/'possession-signature.bin'
 result=subprocess.run([mini,'enroll','--action','possess','--dir',str(directory),'--key',key,'--subject','8' if mode=='wrong-subject' else '7','--output',str(output)],env=env,capture_output=True,timeout=90)
 (directory/'stdout').write_bytes(result.stdout);(directory/'stderr').write_bytes(result.stderr)
 if mode=='honest':assert result.returncode==0 and output.stat().st_size==64,result.stderr
 else:assert result.returncode!=0 and not output.exists(),result.stderr
 if mode=='altered-header':assert b'local consent refused before signing' in result.stderr,result.stderr
 results.append({'case':mode,'exit':result.returncode,'signatureCreated':output.exists()})
(root/'RESULTS.json').write_text(json.dumps({'results':results,'sourceMutation':False,'scope':'native whole-command fixture; selected-key possession only; no enrollment admission or submit'},indent=2)+'\n')
print('ACTUAL RUST POSSESSION CONSUMER PASS '+str(len(results)))
for row in results:print('PASS '+str(row))
