from pathlib import Path
import hashlib,json
r=Path('/home/hbox/workbox/codex-client-consent-20261003')
c=Path('/home/hbox/workbox/codex-unified-integration-20261003/src/native/resource-client/src')
out=r/'receipt-rust-r1';out.mkdir(exist_ok=True)
changes=[]
for name in ['client_consent.rs','job.rs']:
 p=c/name;old=p.read_text();(out/(name+'.pre')).write_text(old)
 if name=='client_consent.rs':
  anchor='/// Enrollment possession is a source-independent native domain frame'
  block='''/// Retained job outcomes are accepted only after source lookup binds the
/// original ingress and all native receipt coordinates. Source absence is a
/// lookup result; it never certifies a failed new submission.
pub(crate) fn job_outcome(host: &Path, config: &Path, operation: u8,
    original_ingress: &[u8], candidate: &[u8]) -> Result<Vec<u8>> {
    if !matches!(operation, 162 | 163) || original_ingress.is_empty() {
        return Err("invalid retained job receipt request".into());
    }
    let retained = [vec![operation], original_ingress.to_vec()].concat();
    let checked = invoke(host, config, 225, &pair(&retained, candidate)?)?;
    if checked != candidate {
        return Err("verified source returned another job outcome".into());
    }
    Ok(checked)
}

'''
  assert old.count(anchor)==1;new=old.replace(anchor,block+anchor,1)
 else:
  anchor='    let outcome = inspect(ws, "outcome", &invoke(ws, 162, ingress)?)?;'
  assert old.count(anchor)==1
  new=old.replace(anchor,'    let offered = invoke(ws, 162, ingress)?;\n    let checked = crate::client_consent::job_outcome(&ws.host, &ws.config, 162, ingress, &offered)?;\n    let outcome = inspect(ws, "outcome", &checked)?;',1)
  anchor='    let outcome = inspect(ws, "outcome", &invoke(ws, 163, &ingress)?)?;'
  assert new.count(anchor)==1
  new=new.replace(anchor,'    let offered = invoke(ws, 163, &ingress)?;\n    let checked = crate::client_consent::job_outcome(&ws.host, &ws.config, 163, &ingress, &offered)?;\n    let outcome = inspect(ws, "outcome", &checked)?;',1)
  new=new.replace('    // Receipt-only lookup cannot create another effect. Absence permits only\n    // the exact original ingress, whose current admission/replay stays native.', '    // Verified receipt-only lookup binds the original ingress. Only its\n    // source-derived absence permits resubmission of those same bytes.',1)
 (out/name).write_text(new)
 changes.append({'name':name,'preSha256':hashlib.sha256(old.encode()).hexdigest(),'postSha256':hashlib.sha256(new.encode()).hexdigest()})
(out/'SOURCE.json').write_text(json.dumps({'status':'AUTHORED_UNQUALIFIED','files':changes},indent=2)+'\n')
print(json.dumps(changes))
