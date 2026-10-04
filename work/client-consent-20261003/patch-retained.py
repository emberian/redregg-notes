from pathlib import Path
base=Path('/home/hbox/workbox/codex-unified-integration-20261003/src/native/resource-client/src')
p=base/'agent_reserve.rs';s=p.read_text();a='''    let slots = inspected
        .get("slots")''';b='''    // Unsigned retained plans also require current native reconstruction;
    // an old operator frame or its local inspection is not signing consent.
    crate::client_consent::operator_plan(&pin.host, &pin.config, 58, &pin.request, &pin.plan)?;
    let slots = inspected
        .get("slots")''';assert s.count(a)==1;s=s.replace(a,b);p.write_text(s)
p=base/'participant_enrollment.rs';s=p.read_text();a='''    let sponsor_header = decode_hex(field(&plan_view["sponsorHeader"], "canonical")?)?;''';b='''    let observation = private_bytes(&directory.join("observation/signed-observation.bin"), LIMIT)?;
    crate::client_consent::operator_plan(&pin.host, &pin.config, 86,
        &pair(&observation, &pin.command)?, &pin.plan)?;
    let sponsor_header = decode_hex(field(&plan_view["sponsorHeader"], "canonical")?)?;''';assert s.count(a)==1;s=s.replace(a,b)
a='''    let header = decode_hex(field(&plan_view, "possessionHeader")?)?;
    let signature = signing.sign(&header).to_bytes();''';b='''    let candidate = decode_hex(field(&plan_view, "possessionHeader")?)?;
    let command = private_bytes(&directory.join("command.bin"), LIMIT)?;
    if field(&command_view, "canonical")? != hex(&command) {
        return Err("enrollment possession command differs from retained bytes".into());
    }
    let header = crate::client_consent::possession(Path::new(""), &directory.join("config.json"),
        &command, &subject, &signing, &candidate)?;
    let signature = signing.sign(&header).to_bytes();''';assert s.count(a)==1;s=s.replace(a,b);p.write_text(s)
p=base/'client_consent.rs';s=p.read_text();s+='''
/// Enrollment possession is a source-independent native domain frame over the
/// complete retained command, with the selected new custody key and subject.
pub(crate) fn possession(host:&Path,config:&Path,command:&[u8],subject:&str,key:&SigningKey,candidate:&[u8])->Result<Vec<u8>> {
    let subject:u64=subject.parse().map_err(|_|"possession subject must fit the native subject bound")?;
    let selected=serde_json::to_vec(&json!({"subject":subject.to_string(),"publicKey":hex(key.verifying_key().as_bytes())})).map_err(|e|e.to_string())?;
    let checked=invoke(host,config,226,&pair(command,&pair(&selected,candidate)?)?)?;
    if checked!=candidate{return Err("native possession frame changed".into());}Ok(checked)
}
''';p.write_text(s)
p=Path('/home/hbox/workbox/codex-unified-integration-20261003/src/Host/ClientConsentSession.lean');s=p.read_text();a='''partial def serve (settings : Settings)''';b='''def possession (config : NativeHost.Config) (payload : List UInt8) : IO (List UInt8) := do
  let (commandBytes, rest) ← splitPair payload
  let (selectedBytes, candidate) ← splitPair rest
  let some command := ParticipantKeyEnrollment.commandCodec.decode commandBytes
    | throw (IO.userError "noncanonical retained possession command")
  let some selectedText := String.fromUTF8? selectedBytes.toByteArray
    | throw (IO.userError "possession custody selection is not UTF-8")
  let selected ← IO.ofExcept (SourceAgreementJson.parse selectedText)
  let subjectValue ← IO.ofExcept (selected.getObjVal? "subject")
  let subject ← IO.ofExcept (SourceAgreementJson.nat "subject" subjectValue)
  let publicValue ← IO.ofExcept (selected.getObjVal? "publicKey")
  let publicKey ← IO.ofExcept (SourceAgreementJson.decodeHex "publicKey" publicValue)
  unless command.key.subject.value == subject && command.key.publicKey == publicKey do
    throw (IO.userError "retained enrollment command selects another possession subject or key")
  let expected := ParticipantKeyEnrollment.possessionFrame config.deployment.domain config.profile.semantics command
  let _ ← IO.ofExcept (NativeSpecializedConsent.checkExact expected candidate)
  pure expected

partial def serve (settings : Settings)''';assert s.count(a)==1;s=s.replace(a,b)
s=s.replace('    else if operation == 224 then specialized settings config updated (body.toList.drop 1)','    else if operation == 224 then specialized settings config updated (body.toList.drop 1)\n    else if operation == 226 then possession config (body.toList.drop 1)',1);p.write_text(s)
Path('/home/hbox/workbox/codex-client-consent-20261003/src/Host/ClientConsentSession.lean').write_text(s)
