from pathlib import Path
import sys
p=Path(sys.argv[1]);s=p.read_text()
start=s.index('pub(crate) fn transform(');end=s.index('\npub(crate) fn inspect(',start);part=s[start:end]
part=part.replace('    socket: &Path,','    _socket: &Path,',1)
part=part.replace('''    let frame = if frame_path.exists() {
        bounded(&frame_path, transport::HOST_MAX_FRAME)?''','''    let local = crate::client_consent::codec_frame(host, config, operation, &payload)?;
    let frame = if frame_path.exists() {
        let retained = bounded(&frame_path, transport::HOST_MAX_FRAME)?;
        if retained != local {
            return Err("retained enrollment codec frame differs from local native derivation".into());
        }
        retained''')
part=part.replace('''        let frame = session_invoke(host, socket, config, operation, &payload)?;''','''        let frame = local;''')
s=s[:start]+part+s[end:]
needle='''    let query_bytes = private_bytes(&input.directory.join("query.bin"), LIMIT)?;'''
assert s.count(needle)==1;s=s.replace(needle,'''    let query_bytes = crate::client_consent::intent(input.host, input.config,
        &input.directory.join("query.bin"), signing)?;''')
needle='''    let intent_signature = signing.sign(&query_bytes).to_bytes();'''
assert s.count(needle)==1;s=s.replace(needle,needle+'''
    let intent_signature_path = observation.join("intent-signature.bin");
    retain_exact(&intent_signature_path, &intent_signature)?;''')
needle='''    let challenge_json = inspect(
        input.host,'''
assert s.count(needle)==1;s=s.replace(needle,'''    inspect(
        input.host,''')
needle='''    let headers = challenge_headers(&challenge_json)?;'''
assert s.count(needle)==1;s=s.replace(needle,'''    let headers = crate::client_consent::observation(input.host, input.config,
        &input.directory.join("query.bin"), &intent_signature_path,
        &observation.join("challenge.bin"), signing)?;''')
p.write_text(s)
