import concurrent.futures,hashlib,json,os,subprocess
from pathlib import Path
root=Path('/tank/dregg-build/codex-client-consent-native-20261003');cap=Path('/home/hbox/workbox/codex-client-consent-20261003');base=Path('/tank/dregg-build/codex-runtime-reader-native-20261003');tool=Path('/home/hbox/.elan/toolchains/leanprover--lean4---v4.30.0')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def checked(path,expected):
 if digest(path)!=expected:raise RuntimeError('changed qualified input '+str(path))
root.mkdir(parents=True,exist_ok=True)
for p in ['objects','c']: (root/p).mkdir(exist_ok=True)
expected='07866f113908d30fc21af4d92ab24410204c35b4022e8a06d0de1f8153a56390';checked(base/'qualified-inputs.json',expected)
inputs=json.loads((base/'qualified-inputs.json').read_text());rows=(base/'objects.rsp').read_text().splitlines();assert len(inputs)==len(rows)
lookup={str(Path(x['olean']).resolve()):(x,Path(y)) for x,y in zip(inputs,rows)}
lookup_sha={x['oleanSha']:(x,Path(y)) for x,y in zip(inputs,rows)}
link=cap/'deps/Host/ClientConsentSession.olean'
if not link.exists():link.symlink_to(cap/'olean/Host/ClientConsentSession.olean')
env=os.environ.copy();env['PATH']=str(tool/'bin')+':'+env.get('PATH','');env['LEAN_PATH']=str(cap/'deps')+':'+':'.join(str(p) for p in Path('/tank/dregg-build/claude-hostnext-r1/main-build/src/.lake/packages').glob('*/.lake/build/lib/lean'));env['LEAN_NUM_THREADS']='2'
closure=subprocess.check_output([str(tool/'bin/lean'),'--run',str(base/'closure.lean'),'Host.ClientConsentSession'],env=env,text=True)
(root/'olean-closure.txt').write_text(closure)
new={str((cap/'olean/Host/ClientConsentSession.olean').resolve()):cap/'c/ClientConsentSession.c',str((cap/'deps/Kernel/NativeClientConsent.olean').resolve()):cap/'c/NativeClientConsent.c'}
objects=[];manifest=[];jobs=[]
for n,row in enumerate(closure.splitlines()):
 olean=Path(row).resolve()
 if olean.is_relative_to(tool):continue
 target=root/'objects'/f'{n}.o'
 if str(olean) in new:
  c=new[str(olean)];ownc=root/'c'/c.name;ownc.write_bytes(c.read_bytes());jobs.append((ownc,target));manifest.append({'olean':str(olean),'oleanSha':digest(olean),'c':str(c),'cSha':digest(c),'new':True})
 else:
  prior,obj=lookup.get(str(olean),lookup_sha.get(digest(olean),(None,None)))
  if prior is None:raise RuntimeError('missing matching qualified import '+str(olean))
  checked(olean,prior['oleanSha'])
  if 'c' in prior: checked(Path(prior['c']),prior['cSha'])
  if not target.exists():os.link(obj,target)
  if digest(obj)!=digest(target):raise RuntimeError('changed copied object')
  manifest.append({**prior,'object':str(obj),'objectSha':digest(obj),'new':False})
 objects.append(target)
if len(jobs)!=2:raise RuntimeError('expected exactly2 newC files')
(root/'qualified-inputs.json').write_text(json.dumps(manifest,indent=2))
flags=['-I',str(tool/'include'),'-fstack-clash-protection','-fdata-sections','-ffunction-sections','-fvisibility=hidden','-Wno-unused-command-line-argument','--sysroot',str(tool),'-nostdinc','-isystem',str(tool/'include/clang'),'-O3','-DNDEBUG','-DLEAN_EXPORTING']
def compile(job):
 c,obj=job
 with (root/'c'/(c.stem+'.log')).open('w') as log:subprocess.run([str(tool/'bin/clang'),'-c','-o',str(obj),str(c),*flags],stdout=log,stderr=log,check=True)
 print('C PASS '+c.stem,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(compile,jobs))
rsp=root/'objects.rsp';rsp.write_text(''.join(str(p)+'\n' for p in objects));binary=root/'minidregg-client-consent'
if binary.exists():raise RuntimeError('refuse overwriting executable')
with (root/'link.log').open('w') as log:subprocess.run([str(tool/'bin/leanc'),'-o',str(binary),'@'+str(rsp)],stdout=log,stderr=log,check=True)
usage=subprocess.run([str(binary)],capture_output=True,timeout=20);(root/'usage.txt').write_bytes(usage.stdout+usage.stderr)
assert usage.returncode==1 and b'client-consent CONFIG stdio' in usage.stderr
receipt={'binary':str(binary),'binarySha':digest(binary),'objects':len(objects),'compiled':2,'sourceSha':digest(cap/'src/Host/ClientConsentSession.lean'),'inputsSha':digest(root/'qualified-inputs.json')}
(root/'NATIVE-CONSENT.json').write_text(json.dumps(receipt,indent=2)+'\n');print('NATIVE CONSENT PASS '+json.dumps(receipt),flush=True)
