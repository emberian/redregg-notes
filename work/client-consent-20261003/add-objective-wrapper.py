from pathlib import Path
import hashlib,json,difflib
p=Path('/home/hbox/workbox/codex-unified-integration-20261003/src/native/resource-client/src/client_consent.rs');s=p.read_text();before=s
assert 'fn objective_headers(' not in s
s+='''
/// Objective-only source WIP. Endpoint 227 must reconstruct the complete
/// expected typed plan from independently retained intent and Verified source,
/// bind the selected custody key to this role, and return its own ordered
/// headers after whole-plan equality. An older provider refuses this endpoint;
/// callers must never fall back to the offered plan's inspected headers.
pub(crate) fn objective_headers(host: &Path, config: &Path, retained_intent: &[u8],
    selected_public_key: &[u8], role: &str, candidate_plan: &[u8]) -> Result<Vec<Vec<u8>>> {
    if selected_public_key.len() != 32 || role.is_empty() || role.len() > 128 {
        return Err("invalid local Objective custody selection".into());
    }
    let selection = serde_json::to_vec(&json!({"publicKey":hex(selected_public_key),"role":role}))
        .map_err(|error|error.to_string())?;
    let payload = pair(retained_intent, &pair(&selection, candidate_plan)?)?;
    headers(&invoke(host, config, 227, &payload)?)
}
'''
p.write_text(s)
out=Path('/home/hbox/workbox/codex-client-consent-20261003');(out/'objective-wrapper.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),s.splitlines(True),fromfile='a/native/resource-client/src/client_consent.rs',tofile='b/native/resource-client/src/client_consent.rs')));(out/'OBJECTIVE-WRAPPER-SOURCE.json').write_text(json.dumps({'path':str(p),'before':hashlib.sha256(before.encode()).hexdigest(),'sha256':hashlib.sha256(s.encode()).hexdigest(),'nativeEndpoint':227,'nativeProducer':'pending actual typed World intent/Verified private constructor; old4c provider refuses'},indent=2)+'\n');print(hashlib.sha256(s.encode()).hexdigest())
