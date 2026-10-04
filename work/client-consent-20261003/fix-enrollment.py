from pathlib import Path
p=Path('/home/hbox/workbox/codex-unified-integration-20261003/src/native/resource-client/src/participant_enrollment.rs')
s=p.read_text()
a='''    inspect(
        input.host,
        input.socket,
        input.config,
        "challenge",'''
b='''    let challenge_json = inspect(
        input.host,
        input.socket,
        input.config,
        "challenge",'''
assert s.count(a)==1;s=s.replace(a,b)
a='''    let frame = if frame_path.exists() {
        let retained = bounded(&frame_path, transport::HOST_MAX_FRAME)?;
        if operation == 86 || operation == 92 {'''
b='''    let local_codec = matches!(operation, 7 | 8 | 9 | 10 | 11);
    let frame = if frame_path.exists() {
        let retained = bounded(&frame_path, transport::HOST_MAX_FRAME)?;
        if local_codec {
            let current = crate::client_consent::codec_frame(host, config, operation, payload)?;
            if current != retained {
                return Err("retained enrollment codec frame differs from local native derivation".into());
            }
        }
        if operation == 86 || operation == 92 {'''
assert s.count(a)==1;s=s.replace(a,b)
a='''        session_invoke(host, socket, config, operation, payload)?
    };
    retained_frame(directory, stem, &frame, operation)'''
b='''        if local_codec {
            crate::client_consent::codec_frame(host, config, operation, payload)?
        } else {
            session_invoke(host, socket, config, operation, payload)?
        }
    };
    retained_frame(directory, stem, &frame, operation)'''
assert s.count(a)==1;s=s.replace(a,b)
p.write_text(s)
snapshot=Path('/tank/dregg-build/codex-client-consent-rust-20261003/src/native/resource-client/src/participant_enrollment.rs');snapshot.write_text(s)
