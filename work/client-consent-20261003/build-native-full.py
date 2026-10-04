import concurrent.futures,hashlib,json,os,subprocess
from pathlib import Path
root=Path('/tank/dregg-build/codex-client-consent-full-native-20261003');base=Path('/tank/dregg-build/codex-client-consent-core-native-20261003');cap=Path('/home/hbox/workbox/codex-client-consent-20261003');receipt=Path('/home/hbox/workbox/scenario-consent-lifecycle-20261003/qualified-lifecycle15-r1.json');tool=Path('/home/hbox/.elan/toolchains/leanprover--lean4---v4.30.0')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def identity(p):s=Path(p).stat();return [s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns]
assert sha(receipt)=='2fe95c5e8dec2a91565fd57814b53d27216d96cf2fba1c23bfa7cdffd4354c93'
lifecycle=json.loads(receipt.read_text());core=json.loads((base/'NATIVE-CONSENT-CORE.json').read_text());assert sha(core['binary'])==core['binarySha256']
for pin in core['newInputs']:
 for kind in ['source','olean','c']:assert sha(pin[kind])==pin[kind+'Sha256']
for pin in lifecycle['matchedImmediateProducerClosure']:
 assert sha(pin['olean'])==pin['oleanSha256'];module=pin['module'].replace('.','/')+'.olean'
 assert sha(cap/'deps'/module)==pin['oleanSha256'], 'core dependency ABI mismatch '+module
new=lifecycle['newQualifiedProducerClosure']+[{ 'module':'Host.ClientConsentSession','source':str(cap/'src/Host/ClientConsentSession.lean'),'olean':str(cap/'olean/Host/ClientConsentSession.olean'),'c':str(cap/'c/ClientConsentSession.c')}]
for pin in new:
 for kind in ['source','olean','c']:
  current=sha(pin[kind]);expected=pin.get(kind+'Sha256',current);assert current==expected,pin['module']+' changed '+kind;pin[kind+'Sha256']=current
assert len(new)==31 and len({p['module'] for p in new})==31
for name in ['objects','c']:(root/name).mkdir(parents=True,exist_ok=True)
base_before={str(p):identity(p) for p in [base/'NATIVE-CONSENT-CORE.json',base/'NEW-INPUTS.json',base/'objects.rsp']};reused=[];objects=[]
for n,line in enumerate((base/'objects.rsp').read_text().splitlines()):
 source=Path(line)
 if source.name=='ClientConsentSpecializedSession.o':continue
 dest=root/'objects'/f'core-{n}.o';before=identity(source)
 if not dest.exists():os.link(source,dest)
 assert identity(dest)==before
 objects.append(dest);reused.append({'source':str(source),'ownedLink':str(dest),'identity':before})
(root/'NEW-INPUTS.json').write_text(json.dumps(new,indent=2)+'\n')
flags=['-I',str(tool/'include'),'-fstack-clash-protection','-fdata-sections','-ffunction-sections','-fvisibility=hidden','-Wno-unused-command-line-argument','--sysroot',str(tool),'-nostdinc','-isystem',str(tool/'include/clang'),'-O3','-DNDEBUG','-DLEAN_EXPORTING']
def compile(pin):
 stem=pin['module'].replace('.','_');c=root/'c'/(stem+'.c');obj=root/'objects'/(stem+'.o');c.write_bytes(Path(pin['c']).read_bytes())
 with (root/'c'/(stem+'.log')).open('w') as log:subprocess.run([str(tool/'bin/clang'),'-c','-o',str(obj),str(c),*flags],stdout=log,stderr=log,check=True)
 pin['object']=str(obj);pin['objectSha256']=sha(obj);print('C PASS '+pin['module'],flush=True);return obj
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:objects.extend(pool.map(compile,new))
rsp=root/'objects.rsp';rsp.write_text(''.join(str(p)+'\n' for p in objects));binary=root/'minidregg-client-consent'
assert not binary.exists(),'refuse native artifact overwrite'
with (root/'link.log').open('w') as log:subprocess.run([str(tool/'bin/leanc'),'-o',str(binary),'@'+str(rsp)],stdout=log,stderr=log,check=True)
usage=subprocess.run([str(binary)],capture_output=True,timeout=20);assert usage.returncode==1 and b'client-consent CONFIG stdio' in usage.stderr
for pin in new:
 for kind in ['source','olean','c']:assert sha(pin[kind])==pin[kind+'Sha256']
for row in reused:assert identity(row['source'])==row['identity'] and identity(row['ownedLink'])==row['identity']
for p,before in base_before.items():assert identity(p)==before
result={'binary':str(binary),'binarySha256':sha(binary),'objects':len(objects),'compiled':len(new),'newInputs':new,'reusedCoreObjects':reused,'baseMetadataPrePost':base_before,'lifecycleReceipt':str(receipt),'lifecycleReceiptSha256':sha(receipt),'scope':'full-peer ordinary +13 specialized +15 lifecycle families, 201 explicitly refused; native link only, receiving lifecycle cases pending'}
(root/'NATIVE-CONSENT-FULL.json').write_text(json.dumps(result,indent=2)+'\n');print('NATIVE CONSENT FULL PASS '+result['binarySha256'],flush=True)
