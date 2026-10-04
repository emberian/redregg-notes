from pathlib import Path
base=Path('/home/hbox/workbox/codex-unified-integration-20261003/src/native/resource-client/src')
p=base/'client_consent.rs';s=p.read_text()
a='''    let bytes=invoke(host,config,op,&payload)?;write_new(Path::new(destination),&bytes)?;'''
b='''    let frame=codec_frame(host,config,op,&payload)?;
    let bytes=frame[1..].to_vec();write_new(Path::new(destination),&bytes)?;'''
assert s.count(a)==1;s=s.replace(a,b)
a='''    let body=invoke(host,config,operation,payload)?;
    Ok([vec![operation],body].concat())
}'''
b='''    local_frame(host, config, operation, payload)
}

/// Full native pure codec authority is selected independently of the remote
/// operator. Specialized grammars remain authored/decoded by that real image.
/// This process never receives keys, and these operations never mutate source.
fn local_frame(host:&Path,config:&Path,operation:u8,payload:&[u8])->Result<Vec<u8>> {
    let executable=pure_host(host)?;
    let settings=PINS.get().map(|pins|pins.config.clone())
        .or_else(||std::env::var_os("MINI_CONSENT_CONFIG").map(PathBuf::from))
        .unwrap_or_else(||config.to_path_buf());
    if !settings.is_absolute(){return Err("local native settings must be absolute".into());}
    let settings_bytes=bounded(&settings)?;
    let mut child=Command::new(&executable).arg(&settings).arg("stdio")
        .stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::inherit())
        .spawn().map_err(|e|format!("cannot start local native codec: {e}"))?;
    let input=child.stdin.take().ok_or("local codec stdin missing")?;
    let output=child.stdout.take().ok_or("local codec stdout missing")?;
    let mut session=Session{child,input,output,executable,settings_bytes:settings_bytes.clone()};
    let body=round_trip(&mut session,operation,payload)?;
    if bounded(&settings)?!=settings_bytes{return Err("local native settings changed during codec operation".into());}
    Ok([vec![operation],body].concat())
}

pub(crate) fn plan_operation(operation:u8)->bool {
    matches!(operation,32|36|44|48|50|52|58|66|68|70|74|78|80|82|86|92|96|103|108|113|117|123|126|140|160|170|183|201|206)
}
/// Always check adapted operator-authored plans before returning bytes to any
/// signing consumer. A native refusal or dead verifier never falls back to the
/// remotely proposed plan.
pub(crate) fn operator_plan(host:&Path,config:&Path,operation:u8,request:&[u8],candidate:&[u8])->Result<()> {
    let request=[vec![operation],request.to_vec()].concat();
    let expected=invoke(host,config,224,&pair(&request,candidate)?)?;
    if expected!=candidate{return Err("local native specialized consent returned a different plan".into());}
    Ok(())
}
'''
assert s.count(a)==1;s=s.replace(a,b);p.write_text(s)
p=base/'main.rs';s=p.read_text()
a='''    let selected_sha = host_image_sha256(host)?;
    if let Some(sha) = EXPECTED_HOST_SHA.get() {'''
b='''    if (7..=11).contains(&operation) {
        return client_consent::codec_frame(host, config, operation, payload);
    }
    let selected_sha = host_image_sha256(host)?;
    if let Some(sha) = EXPECTED_HOST_SHA.get() {'''
assert s.count(a)==1;s=s.replace(a,b)
a='''    transport::invoke_pinned(socket, config, &selected_sha, operation, payload)
}'''
b='''    let reply = transport::invoke_pinned(socket, config, &selected_sha, operation, payload)?;
    if client_consent::plan_operation(operation) && reply.first()==Some(&operation) {
        client_consent::operator_plan(host, config, operation, payload, &reply[1..])?;
    }
    Ok(reply)
}'''
assert s.count(a)==1;s=s.replace(a,b);p.write_text(s)
