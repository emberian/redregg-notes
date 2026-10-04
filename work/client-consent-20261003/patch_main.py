from pathlib import Path
import sys
p=Path(sys.argv[1]);s=p.read_text();old=s
# Add module next to existing private client modules, scope owned new source.
if 'mod client_consent;' not in s:
 idx=s.index('mod workspace;');s=s[:idx]+'mod client_consent;\n'+s[idx:]
start=s.index('fn process(host: &Path');end=s.index('\n#[cfg(unix)]\nfn socket_process',start)
orig=s[start:end]
orig=orig.replace('    if let Some(socket) = SOCKET.get() {','''    let pure = arguments.first().and_then(|word| word.to_str()).is_some_and(|verb|
        matches!(verb, "author" | "inspect" | "signatures" | "observe-assemble" | "assemble"));
    if pure {
        let local = client_consent::pure_host(host)?;
        return local_process(&local, config, arguments);
    }
    if let Some(socket) = SOCKET.get() {''',1)
localstart=orig.index('    let mut command = Command::new(host);')
local=orig[localstart:]
orig=orig[:localstart]+'''    local_process(host, config, arguments)
}

fn local_process(host: &Path, config: &Path, arguments: &[&OsStr]) -> Result<Output> {
'''+local
s=s[:start]+orig+s[end:]
needle='''    // The Host answers an observation only for a request its subject signed: the
    // signature over the intent's own framed bytes is checked before any target is read.
    let intent_bytes = fs::read(&intent_bin)
        .map_err(|error| format!("cannot read {}: {error}", intent_bin.display()))?;'''
replace='''    // The local native verifier binds the retained intent and current subject
    // to custody before even the observation's initial signature is released.
    let intent_bytes = client_consent::intent(host, config, &intent_bin, signing)?;'''
assert s.count(needle)==1;s=s.replace(needle,replace)
s=s.replace('''        challenge_headers(&presentation)?,
        &signatures_json,''','''        client_consent::observation(host, config, &intent_bin, &intent_signature, &challenge_bin)?,
        &signatures_json,''',1)
# Keep local rendered evidence but use only native-consented ordered headers.
s=s.replace('''    let presentation = inspect(host, config, "challenge", &challenge_bin, &challenge_json)?;''','''    inspect(host, config, "challenge", &challenge_bin, &challenge_json)?;''',1)
needle='''        plan_headers(&presentation)?,
        &signatures_json,'''
assert s.count(needle)==1;s=s.replace(needle,'''        client_consent::plan(host, &retained_config, &directory.join("intent.bin"), &plan_bin)?,
        &signatures_json,''',1)
needle='''        plan_headers(&presentation)?,
        &directory.join("transaction-signatures.json"),'''
assert s.count(needle)==1;s=s.replace(needle,'''        client_consent::plan(host, &retained_config, &directory.join("intent.bin"), &plan_bin)?,
        &directory.join("transaction-signatures.json"),''',1)
needle='''        let bytes = fs::read(&binary).map_err(|e| e.to_string())?;
        let signature = signing.sign(&bytes).to_bytes();'''
assert s.count(needle)==1;s=s.replace(needle,'''        let bytes = client_consent::intent(host, &retained_config, &binary, &signing)?;
        let signature = signing.sign(&bytes).to_bytes();''',1)
needle='''            challenge_headers(&presented)?, &child.join("observation-signatures.json"),'''
assert s.count(needle)==1;s=s.replace(needle,'''            client_consent::observation(host, &retained_config, &child.join("intent.bin"),
                &child.join("intent-signature.bin"), &binary)?, &child.join("observation-signatures.json"),''',1)
assert s!=old;p.write_text(s)
