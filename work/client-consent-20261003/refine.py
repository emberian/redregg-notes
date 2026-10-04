from pathlib import Path
root=Path('/Users/ember/dev/redregg/work/client-consent-20261003');p=root/'ClientConsentSession.lean';s=p.read_text()
s=s.replace('def consent (config', '''def selectedHeaders (config : NativeHost.Config) (session : Session config)
    (wanted : NativeObservationCodec.Intent) (headers : List (List UInt8)) : IO (List UInt8) := do
  let some key := CredentialAuthorityState.currentSigningKey session.2.opened.authority.snapshot.logical wanted.subject
    | throw (IO.userError "local custody subject has no current key")
  for bytes in headers do
    let some header := CredentialSignedEnvelopeController.headerCodec.decode bytes
      | throw (IO.userError "local planner produced a noncanonical header")
    unless header.keyId == key.keyId && header.keyEpoch == key.keyEpoch &&
        header.algorithm == key.algorithm do
      throw (IO.userError "prepared role selects another custody signer")
  pure (headersBytes headers)

def consent (config''')
s=s.replace('''      pure (headersBytes checked.headers)''','''      selectedHeaders config session wanted checked.headers''')
s=s.replace('''      pure (headersBytes headers)''','''      selectedHeaders config session wanted headers''')
p.write_text(s)
