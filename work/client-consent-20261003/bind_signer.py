from pathlib import Path
root=Path('/Users/ember/dev/redregg/work/client-consent-20261003')
p=root/'ClientConsentSession.lean';s=p.read_text();needle='''  match operation with
  | 220 =>
      -- Before even the first intent signature, bind subject/current key to
      -- locally chosen custody, rather than a remote JSON subject label.
      let key ← IO.ofExcept ((NativeObservationController.intentKey
        (NativeHost.observationContext config session.2.opened) wanted.subject).mapError
        (fun _ => "local intent subject has no current signing key"))
      unless rest.length == 32 && key == rest do
        throw (IO.userError "local intent subject differs from custody signer")
      pure intentBytes'''
replace='''  let (signer, rest) ← splitPair rest
  -- Bind the selected custody key at EACH source extension, including a key
  -- change between intent signing and observation/transaction signing.
  let key ← IO.ofExcept ((NativeObservationController.intentKey
    (NativeHost.observationContext config session.2.opened) wanted.subject).mapError
    (fun _ => "local intent subject has no current signing key"))
  unless signer.length == 32 && key == signer do
    throw (IO.userError "local intent subject differs from custody signer")
  match operation with
  | 220 =>
      unless rest.isEmpty do throw (IO.userError "intent consent has unexpected trailing bytes")
      pure intentBytes'''
assert needle in s;s=s.replace(needle,replace);p.write_text(s)
p=root/'client_consent.rs';s=p.read_text();s=s.replace('220,&pair(&bytes,signing.verifying_key().as_bytes())?', '220,&pair(&bytes,&pair(signing.verifying_key().as_bytes(),&[])?)?')
s=s.replace('signature:&Path,challenge:&Path)->Result<Vec<Vec<u8>>>','signature:&Path,challenge:&Path,signing:&SigningKey)->Result<Vec<Vec<u8>>>')
s=s.replace('pair(&bounded(intent)?,&pair(&bounded(signature)?,&bounded(challenge)?)?)?', 'pair(&bounded(intent)?,&pair(signing.verifying_key().as_bytes(),&pair(&bounded(signature)?,&bounded(challenge)?)?)?)?')
s=s.replace('intent:&Path,plan:&Path)->Result<Vec<Vec<u8>>>','intent:&Path,plan:&Path,signing:&SigningKey)->Result<Vec<Vec<u8>>>')
s=s.replace('222,&pair(&bounded(intent)?,&bounded(plan)?)?', '222,&pair(&bounded(intent)?,&pair(signing.verifying_key().as_bytes(),&bounded(plan)?)?)?')
p.write_text(s)
