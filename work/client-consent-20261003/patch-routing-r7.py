from pathlib import Path
import hashlib,json
root=Path('/home/hbox/workbox/codex-unified-integration-20261003/src/native/resource-client/src');out=Path('/home/hbox/workbox/codex-client-consent-20261003');changes=[]
def edit(name,transform):
 p=root/name;s=p.read_text();new=transform(s);assert new!=s,name
 before=hashlib.sha256(s.encode()).hexdigest();(out/('r7-preimage-'+name.replace('/','_'))).write_text(s);p.write_text(new);changes.append({'path':str(p),'before':before,'sha256':hashlib.sha256(new.encode()).hexdigest()})
def transport(s):
 s=s.replace('invoke_inner(socket, config, None, operation, payload)','invoke_inner(Path::new(""), socket, config, None, operation, payload)').replace('invoke_inner(socket, config, Some(&expected), operation, payload)','invoke_inner(Path::new(""), socket, config, Some(&expected), operation, payload)')
 anchor='/// Public read workflows use one absolute deadline across connect, write and read.'
 insert='''/// The main caller has an independently selected local Host; direct remote
/// callers must instead select their local consent pins explicitly.
pub(crate) fn invoke_pinned_with_local(
    local_host: &Path, socket: &Path, config: &Path, expected_host_sha256: &str,
    operation: u8, payload: &[u8],
) -> Result<Vec<u8>, String> {
    let expected = parse_host_sha256(expected_host_sha256)?;
    invoke_inner(local_host, socket, config, Some(&expected), operation, payload)
}

fn check_signing_plan_reply(local_host: &Path, config: &Path, operation: u8,
    payload: &[u8], reply: &[u8]) -> Result<(), String> {
    if crate::client_consent::plan_operation(operation) && reply.first() == Some(&operation) {
        crate::client_consent::operator_plan(local_host, config, operation, payload, &reply[1..])?;
    }
    Ok(())
}

'''
 assert anchor in s;s=s.replace(anchor,insert+anchor,1)
 s=s.replace('fn invoke_inner(\n    socket:', 'fn invoke_inner(\n    local_host: &Path,\n    socket:',1)
 start=s.index('fn invoke_inner(');end=s.index('/// One framed request',start);chunk=s[start:end]
 chunk=chunk.replace('    let config = read_config(config)?;','    let config_path = config;\n    let config = read_config(config)?;',1)
 assert '    Ok(reply)\n}' in chunk;chunk=chunk.replace('    Ok(reply)\n}', '    check_signing_plan_reply(local_host, config_path, operation, payload, &reply)?;\n    Ok(reply)\n}',1);s=s[:start]+chunk+s[end:]
 start=s.index('pub(crate) fn invoke_pinned_deadline(');end=s.index('fn connect_unix_deadline',start);chunk=s[start:end]
 chunk=chunk.replace('    let config = read_config(config)?;','    let config_path = config;\n    let config = read_config(config)?;',1)
 chunk=chunk.replace('    Ok(reply)\n}', '    check_signing_plan_reply(Path::new(""), config_path, operation, payload, &reply)?;\n    Ok(reply)\n}',1);return s[:start]+chunk+s[end:]
edit('transport.rs',transport)
def main(s):
 old='''    let reply = transport::invoke_pinned(socket, config, &selected_sha, operation, payload)?;
    if client_consent::plan_operation(operation) && reply.first()==Some(&operation) {
        client_consent::operator_plan(host, config, operation, payload, &reply[1..])?;
    }
    Ok(reply)'''
 new='''    transport::invoke_pinned_with_local(host, socket, config, &selected_sha, operation, payload)'''
 assert old in s;return s.replace(old,new,1)
edit('main.rs',main)
def claim(s):
 old='''            Endpoint::Bootstrap(_) => self.http(operation, payload),'''
 new='''            Endpoint::Bootstrap(_) => {
                let reply = self.http(operation, payload)?;
                if crate::client_consent::plan_operation(operation) && reply.first() == Some(&operation) {
                    crate::client_consent::operator_plan(&self.host, &self.config, operation, payload, &reply[1..])?;
                }
                Ok(reply)
            },'''
 assert old in s;return s.replace(old,new,1)
edit('pay_claim.rs',claim)
for name in ['agent_lifetime_grant.rs','agent_reserve/lifetime_v3.rs']:
 def seal(s):
  needle='    let slots =';start=s.index('fn grant_seal(' if name.startswith('agent_lifetime') else 'fn lifetime_seal(');loc=s.index(needle,start)
  guard='''    crate::client_consent::operator_plan(&pinned.host, &pinned.config, PLAN_OPERATION,
        &pinned.request, &pinned.plan)?;
'''
  return s[:loc]+guard+s[loc:]
 edit(name,seal)
def provision(s):
 start=s.index('fn seal(');needle='    let header = decode_hex';loc=s.index(needle,start)
 guard='''    let signed = private_bytes(&directory.join("observation/signed-observation.bin"), LIMIT)?;
    crate::client_consent::operator_plan(grant.host, &config, PLAN_OPERATION,
        &pair(&signed, command)?, plan)?;
'''
 return s[:loc]+guard+s[loc:]
edit('participant_provisioning.rs',provision)
def possession(s):
 needle='    let signature = signing.sign(&header).to_bytes();';start=s.index('fn possess_at(');loc=s.index(needle,start)
 receipt='''    // This explicit action accepts the operator's offered command. Retain
    // exactly what custody accepted before producing the possession signature.
    let local = crate::client_consent::configured_record()?
        .ok_or("possession requires independently retained local consent selection")?;
    let local_config = Path::new(field(&local, "config")?);
    let acceptance = json!({"type":"minidregg-participant-possession-acceptance-v1",
        "origin":"operator-offered-command", "action":"possess",
        "subject":subject,"publicKey":public_key,"commandHex":hex(&command),
        "commandSha256":digest(&command),"possessionHeaderSha256":digest(&header),
        "localConsent":local,"localConfigSha256":digest(&private_bytes(local_config,65_536)?) });
    retain_exact(&directory.join("possession-acceptance.json"),
        &serde_json::to_vec_pretty(&acceptance).map_err(|error|error.to_string())?)?;
'''
 return s[:loc]+receipt+s[loc:]
edit('participant_enrollment.rs',possession)
(out/'SOURCE-ROUTING-07.json').write_text(json.dumps(changes,indent=2)+'\n');print(json.dumps(changes,indent=2))
