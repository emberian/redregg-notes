from pathlib import Path
import hashlib,json
r=Path('/home/hbox/workbox/codex-client-consent-20261003')
old=(r/'src/Host/ClientConsentCore.lean').read_text()
new=old
anchor='partial def serve (extraExpected : ExtraExpected)'
assert new.count(anchor)==1
block='''/-- An entry's locally trusted source adapter consumes the independently
retained original request, reproduces its quote/execution from this exact
Verified prefix, compares the entire canonical plan, and binds the selected
current key and source-defined role. It returns only its derived headers.
This interface alone is not a producer or an admission proof. -/
abbrev ExtraObjective := (settings : Settings) → (config : NativeHost.Config) →
  Session config → List UInt8 → List UInt8 → String → List UInt8 → IO (List (List UInt8))

private def refuseObjective : ExtraObjective := fun _ _ _ _ _ _ _ =>
  throw (IO.userError "no source-derived Objective consent adapter is installed")

def objectiveHeaders (extraObjective : ExtraObjective) (settings : Settings)
    (config : NativeHost.Config) (session : Session config)
    (payload : List UInt8) : IO (List UInt8) := do
  let (originalRequest, rest) ← splitPair payload
  let (selectionBytes, candidate) ← splitPair rest
  unless !originalRequest.isEmpty && !candidate.isEmpty do
    throw (IO.userError "missing original Objective request or proposed plan")
  let some text := String.fromUTF8? selectionBytes.toByteArray
    | throw (IO.userError "Objective custody selection is not UTF-8")
  let selected ← IO.ofExcept (SourceAgreementJson.parse text)
  let object ← IO.ofExcept selected.getObj?
  unless object.foldl (init := true) (fun valid key _ =>
      valid && (key == "publicKey" || key == "role")) do
    throw (IO.userError "unexpected Objective custody selection field")
  let publicValue ← IO.ofExcept (selected.getObjVal? "publicKey")
  let publicText ← IO.ofExcept publicValue.getStr?
  let publicKey ← IO.ofExcept (SourceAgreementJson.decodeHex "publicKey" publicValue)
  unless publicKey.length == 32 && SourceAgreementJson.encodeHex publicKey == publicText do
    throw (IO.userError "noncanonical Objective custody public key")
  let roleValue ← IO.ofExcept (selected.getObjVal? "role")
  let role ← IO.ofExcept roleValue.getStr?
  unless !role.isEmpty && role.toUTF8.size ≤ 128 do
    throw (IO.userError "invalid Objective custody role")
  let headers ← extraObjective settings config session originalRequest publicKey role candidate
  unless !headers.isEmpty && headers.length ≤ 32 do
    throw (IO.userError "source-derived Objective adapter returned invalid header count")
  pure (headersBytes headers)

'''
new=new.replace(anchor,block+'partial def serve (extraExpected : ExtraExpected) (extraObjective : ExtraObjective)',1)
new=new.replace('    else if operation == 226 then possession config (body.toList.drop 1)','    else if operation == 226 then possession config (body.toList.drop 1)\n    else if operation == 227 then objectiveHeaders extraObjective settings config updated (body.toList.drop 1)',1)
new=new.replace('  serve extraExpected settings config updated input output','  serve extraExpected extraObjective settings config updated input output',1)
new=new.replace('def run (extraExpected : ExtraExpected) (arguments : List String) : IO UInt32 := do','def run (extraExpected : ExtraExpected) (arguments : List String)\n    (extraObjective : ExtraObjective := refuseObjective) : IO UInt32 := do',1)
new=new.replace('        serve extraExpected settings config session','        serve extraExpected extraObjective settings config session',1)
out=r/'objective-core-r1';out.mkdir(exist_ok=True)
(out/'ClientConsentCore.lean').write_text(new)
(out/'SOURCE.json').write_text(json.dumps({'status':'AUTHORED_UNQUALIFIED_INTERFACE_ONLY','preSha256':hashlib.sha256(old.encode()).hexdigest(),'postSha256':hashlib.sha256(new.encode()).hexdigest(),'nativeAcceptingProducer':False,'default':'mandatory refusal; no fallback'},indent=2)+'\n')
print(hashlib.sha256(new.encode()).hexdigest())
