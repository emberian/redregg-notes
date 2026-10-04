import concurrent.futures,hashlib,json,os,subprocess
from pathlib import Path
root=Path('/tank/dregg-build/codex-client-consent-core-native-20261003');cap=Path('/home/hbox/workbox/codex-client-consent-20261003');base=Path('/tank/dregg-build/codex-runtime-reader-native-20261003');tool=Path('/home/hbox/.elan/toolchains/leanprover--lean4---v4.30.0')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['objects','c']:(root/name).mkdir(parents=True,exist_ok=True)
assert sha(base/'qualified-inputs.json')=='07866f113908d30fc21af4d92ab24410204c35b4022e8a06d0de1f8153a56390'
inputs=json.loads((base/'qualified-inputs.json').read_text());rows=(base/'objects.rsp').read_text().splitlines();assert len(inputs)==len(rows)
objects=[];receipts=[];base_before={str(p):[p.stat().st_dev,p.stat().st_ino,p.stat().st_size,p.stat().st_mtime_ns] for p in [base/'qualified-inputs.json',base/'objects.rsp',base/'NATIVE-READER.json']}
for n,(row,entry) in enumerate(zip(rows,inputs)):
 if '/Host/SourceAgreementReader.olean' in entry['olean']:continue
 source=Path(row);dest=root/'objects'/f'base-{n}.o'
 if not dest.exists():os.link(source,dest)
 a=source.stat();b=dest.stat()
 if (a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns)!=(b.st_dev,b.st_ino,b.st_size,b.st_mtime_ns):raise RuntimeError('immutable reader object identity changed')
 objects.append(dest);receipts.append({**entry,'reusedObject':str(source),'localObject':str(dest),'identity':[a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns]})
# Previously compiled exact native helper, attested quiet own output, no global main.
old=Path('/tank/dregg-build/codex-client-consent-native-20261003')
old_receipt=json.loads((old/'NATIVE-CONSENT.json').read_text());pin=next(x for x in old_receipt['newInputs'] if x['c'].endswith('NativeClientConsent.c'))
assert sha(cap/'c/NativeClientConsent.c')==pin['cSha'] and sha(old/'objects/NativeClientConsent.o')==pin['objectSha']
p=old/'objects/NativeClientConsent.o';dest=root/'objects/NativeClientConsent.o'
if not dest.exists():os.link(p,dest)
objects.append(dest)
names=['PayClaimQuote','PayClaimStatus','NativeHostPayClaims','NativeSpecializedConsent','ClientConsentCore','ClientConsentSpecializedSession']
new=[(cap/'c'/(name+'.c'),root/'objects'/(name+'.o')) for name in names]
new_pins=[]
for name,(c,obj) in zip(names,new):
 tier='Host' if name.startswith('ClientConsent') else 'Kernel'
 source=cap/'src'/tier/(name+'.lean');olean=cap/'olean'/tier/(name+'.olean')
 new_pins.append({'module':tier+'.'+name,'source':str(source),'sourceSha256':sha(source),'olean':str(olean),'oleanSha256':sha(olean),'c':str(c),'cSha256':sha(c)})
(root/'NEW-INPUTS.json').write_text(json.dumps(new_pins,indent=2)+'\n')
flags=['-I',str(tool/'include'),'-fstack-clash-protection','-fdata-sections','-ffunction-sections','-fvisibility=hidden','-Wno-unused-command-line-argument','--sysroot',str(tool),'-nostdinc','-isystem',str(tool/'include/clang'),'-O3','-DNDEBUG','-DLEAN_EXPORTING']
def compile(job):
 c,obj=job;owned=root/'c'/c.name;owned.write_bytes(c.read_bytes())
 with (root/'c'/(c.stem+'.log')).open('w') as log:subprocess.run([str(tool/'bin/clang'),'-c','-o',str(obj),str(owned),*flags],stdout=log,stderr=log,check=True)
 print('C PASS '+c.stem,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(compile,new))
objects.extend(obj for _,obj in new)
rsp=root/'objects.rsp';rsp.write_text(''.join(str(p)+'\n' for p in objects));binary=root/'minidregg-client-consent'
if binary.exists():raise RuntimeError('refuse existing executable overwrite')
with (root/'link.log').open('w') as log:subprocess.run([str(tool/'bin/leanc'),'-o',str(binary),'@'+str(rsp)],stdout=log,stderr=log,check=True)
usage=subprocess.run([str(binary)],capture_output=True,timeout=20);assert usage.returncode==1 and b'client-consent CONFIG stdio' in usage.stderr
for p,identity in base_before.items():
 stat=Path(p).stat();assert [stat.st_dev,stat.st_ino,stat.st_size,stat.st_mtime_ns]==identity
for pin,(c,obj) in zip(new_pins,new):assert sha(c)==pin['cSha256'];pin['objectSha256']=sha(obj)
(root/'qualified-inputs.json').write_text(json.dumps(receipts,indent=2)+'\n')
receipt={'binary':str(binary),'binarySha256':sha(binary),'objects':len(objects),'compiled':len(new),'newInputs':new_pins,'readerInputsSha256':sha(base/'qualified-inputs.json'),'baseArtifactIdentityPrePost':base_before,'scope':'independent full-peer ordinary and13specialized native plans; lifecycle families explicitly refused; no source mutation'}
(root/'NATIVE-CONSENT-CORE.json').write_text(json.dumps(receipt,indent=2)+'\n');print('NATIVE CONSENT CORE PASS '+json.dumps(receipt),flush=True)
