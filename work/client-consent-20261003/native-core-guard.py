import os,fcntl,json,time,subprocess
from pathlib import Path
root=Path('/home/hbox/workbox/codex-client-consent-20261003')
lock=(root/'native-core.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
pid=os.fork()
if pid:
 lock.close();_,status=os.waitpid(pid,0);raise SystemExit(os.waitstatus_to_exitcode(status))
os.setsid()
state={'guardianPid':os.getpid(),'owner':'client_consent_construction-native-six-C','memory':'8G','swap':0,'jobs':2,'seconds':180,'startedUTC':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'state':'running'}
(root/'NATIVE-CORE-GUARD-01.json').write_text(json.dumps(state,indent=2)+'\n')
env={**os.environ,'SWARM_MEM_MAX':'8G','CARGO_BUILD_JOBS':'2'}
child=subprocess.Popen(['/usr/local/bin/swarm-build','timeout','--kill-after=10s','180s','bash',str(root/'native-core.sh')],env=env,pass_fds=(lock.fileno(),))
state['childPid']=child.pid;(root/'NATIVE-CORE-GUARD-01.json').write_text(json.dumps(state,indent=2)+'\n')
code=child.wait();state.update(state='released',exitCode=code,finishedUTC=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()));(root/'NATIVE-CORE-GUARD-01.json').write_text(json.dumps(state,indent=2)+'\n');print('NATIVE CORE RELEASED',code,flush=True);os._exit(code if code>=0 else 128-code)
