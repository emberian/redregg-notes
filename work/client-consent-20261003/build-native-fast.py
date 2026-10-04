import concurrent.futures,hashlib,json,os,subprocess
from pathlib import Path
root=Path('/tank/dregg-build/codex-client-consent-native-20261003');cap=Path('/home/hbox/workbox/codex-client-consent-20261003');base=Path('/tank/dregg-build/codex-runtime-reader-native-20261003');tool=Path('/home/hbox/.elan/toolchains/leanprover--lean4---v4.30.0')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
assert sha(base/'qualified-inputs.json')=='07866f113908d30fc21af4d92ab24410204c35b4022e8a06d0de1f8153a56390'
inputs=json.loads((base/'qualified-inputs.json').read_text());rows=(base/'objects.rsp').read_text().splitlines();assert len(inputs)==len(rows)
objects=[];receipts=[]
# Containment follows the actual direct-import contract: Reader imports every
# Session direct dependency except NativeClientConsent, which imports NativeHost.
# The exact same reader-pass-r2 namespace qualified Session r4. Reader's global
# entry object is excluded; no unrelated module initializer is invoked by ours.
for n,(row,entry) in enumerate(zip(rows,inputs)):
 if '/Host/SourceAgreementReader.olean' in entry['olean']:continue
 source=Path(row);dest=root/'objects'/f'base-{n}.o'
 if not dest.exists():os.link(source,dest)
 if source.stat().st_ino!=dest.stat().st_ino or source.stat().st_dev!=dest.stat().st_dev:raise RuntimeError('warm immutable object identity changed')
 objects.append(dest);receipts.append({**entry,'reusedObject':str(source),'localObject':str(dest)})
new=[(cap/'c/NativeClientConsent.c',root/'objects/NativeClientConsent.o'),(cap/'c/ClientConsentSession.c',root/'objects/ClientConsentSession.o')]
flags=['-I',str(tool/'include'),'-fstack-clash-protection','-fdata-sections','-ffunction-sections','-fvisibility=hidden','-Wno-unused-command-line-argument','--sysroot',str(tool),'-nostdinc','-isystem',str(tool/'include/clang'),'-O3','-DNDEBUG','-DLEAN_EXPORTING']
def compile(job):
 source,obj=job;owned=root/'c'/source.name;owned.write_bytes(source.read_bytes())
 with (root/'c'/(source.stem+'.log')).open('w') as log:subprocess.run([str(tool/'bin/clang'),'-c','-o',str(obj),str(owned),*flags],stdout=log,stderr=log,check=True)
 print('C PASS '+source.stem,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(compile,new))
objects.extend(obj for _,obj in new)
rsp=root/'objects.rsp';rsp.write_text(''.join(str(p)+'\n' for p in objects));binary=root/'minidregg-client-consent'
if binary.exists():raise RuntimeError('refuse existing executable overwrite')
with (root/'link.log').open('w') as log:subprocess.run([str(tool/'bin/leanc'),'-o',str(binary),'@'+str(rsp)],stdout=log,stderr=log,check=True)
usage=subprocess.run([str(binary)],capture_output=True,timeout=20);(root/'usage.txt').write_bytes(usage.stdout+usage.stderr)
assert usage.returncode==1 and b'client-consent CONFIG stdio' in usage.stderr
(root/'qualified-inputs.json').write_text(json.dumps(receipts,indent=2))
receipt={'binary':str(binary),'binarySha':sha(binary),'objects':len(objects),'compiled':2,'sourceSha':sha(cap/'src/Host/ClientConsentSession.lean'),'newInputs':[{"c":str(c),"cSha":sha(c),"objectSha":sha(o)} for c,o in new],'readerInputsSha':sha(base/'qualified-inputs.json'),'scope':'Reader qualified import superset excluding Reader entry; Session r4 same exact dependencies; no dependency compilation'}
(root/'NATIVE-CONSENT.json').write_text(json.dumps(receipt,indent=2)+'\n');print('NATIVE CONSENT PASS '+json.dumps(receipt),flush=True)
