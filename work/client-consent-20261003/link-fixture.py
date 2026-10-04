from pathlib import Path
import json,hashlib,subprocess
base=Path('/tank/dregg-build/codex-client-consent-core-native-20261003');cap=Path('/home/hbox/workbox/codex-client-consent-20261003');out=Path('/tank/dregg-build/codex-client-consent-fixture-native-20261003');tool=Path('/home/hbox/.elan/toolchains/leanprover--lean4---v4.30.0')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
out.mkdir(exist_ok=True)
receipt=json.loads((base/'NATIVE-CONSENT-CORE.json').read_text());assert receipt['binarySha256']=='4e1d1feb4f4cf4ce0873ea1cb3315c792ef02c5735091f71872330c3f538a363'
rows=(base/'objects.rsp').read_text().splitlines();rows=[x for x in rows if not x.endswith('/ClientConsentSpecializedSession.o')];assert len(rows)==3404
c=cap/'c/SpecializedFixture.c';obj=out/'SpecializedFixture.o';owned=out/'SpecializedFixture.c';owned.write_bytes(c.read_bytes())
flags=['-I',str(tool/'include'),'-fstack-clash-protection','-fdata-sections','-ffunction-sections','-fvisibility=hidden','-Wno-unused-command-line-argument','--sysroot',str(tool),'-nostdinc','-isystem',str(tool/'include/clang'),'-O3','-DNDEBUG','-DLEAN_EXPORTING']
with (out/'compile.log').open('w') as log:subprocess.run([str(tool/'bin/clang'),'-c','-o',str(obj),str(owned),*flags],stdout=log,stderr=log,check=True)
rows.append(str(obj));rsp=out/'objects.rsp';rsp.write_text(''.join(x+'\n' for x in rows));binary=out/'specialized-fixture'
assert not binary.exists()
with (out/'link.log').open('w') as log:subprocess.run([str(tool/'bin/leanc'),'-o',str(binary),'@'+str(rsp)],stdout=log,stderr=log,check=True)
fixture=cap/'evidence/specialized-native-r1'
result=subprocess.run([str(binary),'/home/hbox/workbox/codex-agreement-20261003/evidence/four-source-operator-r1/host-settings-0.json',str(fixture)],capture_output=True,timeout=90)
(out/'fixture.stdout').write_bytes(result.stdout);(out/'fixture.stderr').write_bytes(result.stderr);assert result.returncode==0,result.stderr[-1500:]
value={'binary':str(binary),'binarySha256':sha(binary),'sourceSha256':sha(cap/'src/Host/SpecializedFixture.lean'),'oleanSha256':sha(cap/'olean/Host/SpecializedFixture.olean'),'cSha256':sha(c),'objectSha256':sha(obj),'baseReceiptSha256':sha(base/'NATIVE-CONSENT-CORE.json'),'sourceMutation':False,'signaturesCreated':False,'fixture':str(fixture)}
(out/'NATIVE-FIXTURE.json').write_text(json.dumps(value,indent=2)+'\n');print('NATIVE FIXTURE PASS '+json.dumps(value),flush=True)
