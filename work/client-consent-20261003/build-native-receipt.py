import concurrent.futures,hashlib,json,os,subprocess
from pathlib import Path
root=Path('/tank/dregg-build/codex-client-consent-receipt-native-20261003')
base=Path('/tank/dregg-build/codex-client-consent-full-native-20261003')
corebase=Path('/tank/dregg-build/codex-client-consent-core-native-20261003')
cap=Path('/home/hbox/workbox/codex-client-consent-20261003')
tool=Path('/home/hbox/.elan/toolchains/leanprover--lean4---v4.30.0')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def identity(p):s=Path(p).stat();return [s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns]
manifest=base/'NATIVE-CONSENT-FULL.json';full=json.loads(manifest.read_text())
assert sha(full['binary'])==full['binarySha256']=='4c1b02b1bbede27d6fcd3f60b20c7fe29685fc14e562d3d1a9885d844af223f4'
oldcore=corebase/'objects/ClientConsentCore.o';oldentry=base/'objects/Host_ClientConsentSession.o'
excluded={identity(oldcore)[1],identity(oldentry)[1]}
for name in ['objects','c','src','olean']:(root/name).mkdir(parents=True,exist_ok=True)
reused=[];objects=[]
for n,line in enumerate((base/'objects.rsp').read_text().splitlines()):
 source=Path(line);before=identity(source)
 if before[1] in excluded:continue
 dest=root/'objects'/('reuse-'+str(n)+'.o')
 if not dest.exists():os.link(source,dest)
 assert identity(dest)==before
 objects.append(dest);reused.append({'source':str(source),'ownedLink':str(dest),'identity':before})
assert len(reused)==full['objects']-2
new=[]
for module,cstem in [('Kernel.NativeReceiptConsent','NativeReceiptConsent'),('Host.ClientConsentCore','ClientConsentCore'),('Host.ClientConsentSession','ClientConsentSession')]:
 rel=module.replace('.','/')
 pin={'module':module}
 for kind,path in [('source',cap/'src'/(rel+'.lean')),('olean',cap/'olean'/(rel+'.olean')),('c',cap/'c'/(cstem+'.c'))]:
  frozen=root/('src' if kind=='source' else kind)/(rel+('.lean' if kind=='source' else '.'+kind))
  frozen.parent.mkdir(parents=True,exist_ok=True);data=path.read_bytes()
  if frozen.exists():assert frozen.read_bytes()==data
  else:frozen.write_bytes(data)
  pin[kind]=str(frozen);pin[kind+'Sha256']=sha(frozen)
 new.append(pin)
metadata={str(p):identity(p) for p in [manifest,base/'NEW-INPUTS.json',base/'objects.rsp']}
(root/'NEW-INPUTS.json').write_text(json.dumps(new,indent=2)+'\n')
flags=['-I',str(tool/'include'),'-fstack-clash-protection','-fdata-sections','-ffunction-sections','-fvisibility=hidden','-Wno-unused-command-line-argument','--sysroot',str(tool),'-nostdinc','-isystem',str(tool/'include/clang'),'-O3','-DNDEBUG','-DLEAN_EXPORTING']
def compile(pin):
 obj=root/'objects'/(pin['module'].replace('.','_')+'.o')
 with (root/'c'/(pin['module'].replace('.','_')+'.log')).open('w') as log:subprocess.run([str(tool/'bin/clang'),'-c','-o',str(obj),pin['c'],*flags],stdout=log,stderr=log,check=True)
 pin['object']=str(obj);pin['objectSha256']=sha(obj);print('C PASS '+pin['module'],flush=True);return obj
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:objects.extend(pool.map(compile,new))
rsp=root/'objects.rsp';rsp.write_text(''.join(str(p)+'\n' for p in objects));binary=root/'minidregg-client-consent'
assert not binary.exists(),'refuse artifact overwrite'
with (root/'link.log').open('w') as log:subprocess.run([str(tool/'bin/leanc'),'-o',str(binary),'@'+str(rsp)],stdout=log,stderr=log,check=True)
usage=subprocess.run([str(binary)],capture_output=True,timeout=20);assert usage.returncode==1 and b'client-consent CONFIG stdio' in usage.stderr
for pin in new:
 for kind in ['source','olean','c']:assert sha(pin[kind])==pin[kind+'Sha256']
for row in reused:assert identity(row['source'])==row['identity'] and identity(row['ownedLink'])==row['identity']
for p,before in metadata.items():assert identity(p)==before
result={'binary':str(binary),'binarySha256':sha(binary),'objects':len(objects),'compiled':3,'newInputs':new,'reusedFullObjects':reused,'baseMetadataPrePost':metadata,'baseManifestSha256':sha(manifest),'scope':'same old full-peer profile/cohort plus verified-source job outcome225; receiving pending; Objective227 remains absent'}
(root/'NATIVE-CONSENT-RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print('NATIVE RECEIPT CONSENT PASS '+result['binarySha256'],flush=True)
