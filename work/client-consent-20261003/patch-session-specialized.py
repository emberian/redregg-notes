from pathlib import Path
p=Path('/home/hbox/workbox/codex-unified-integration-20261003/src/Host/ClientConsentSession.lean');s=p.read_text()
s=s.replace('import Kernel.NativeClientConsent\n','import Kernel.NativeClientConsent\nimport Kernel.NativeSpecializedConsent\nimport Kernel.NativeLifecycleConsent\n',1)
a='structure Settings where\n';b='''structure LifecycleManagementSettings where
  managementSubject : Nat
  managementKeyId : Nat
  deriving ToJson
instance : FromJson LifecycleManagementSettings where
  fromJson? json := do
    let object ← json.getObj?
    let expected := ["managementSubject", "managementKeyId"]
    let actual := object.foldl (init := []) (fun fields key _ => key :: fields)
    unless actual.length == expected.length && actual.all expected.contains do
      throw "lifecycleManagement has missing or unknown fields"
    pure ⟨← json.getObjValAs? Nat "managementSubject", ← json.getObjValAs? Nat "managementKeyId"⟩

structure Settings where
''';assert s.count(a)==1;s=s.replace(a,b)
s=s.replace('  disabledEvaluators : Option (List String) := none\n','  disabledEvaluators : Option (List String) := none\n  lifecycleManagement : Option LifecycleManagementSettings := none\n',1)
s=s.replace('    "grainBirthTariff", "completionCustodianKey"]','    "grainBirthTariff", "completionCustodianKey", "lifecycleManagement"]',1)
a='''partial def serve (config : NativeHost.Config) (session : Session config)
    (input output : IO.FS.Stream) : IO Unit := do'''
b='''def specialized (settings : Settings) (config : NativeHost.Config) (session : Session config)
    (payload : List UInt8) : IO (List UInt8) := do
  let (retained, candidate) ← splitPair payload
  let operation :: request := retained | throw (IO.userError "missing retained specialized operation")
  let expected ← if NativeSpecializedConsent.supported operation then
    NativeSpecializedConsent.expectedPlanBytes config session.2 operation request
  else if NativeLifecycleConsent.supported operation then
    NativeLifecycleConsent.expectedPlanBytes config session.2 operation request
  else if NativeLifecycleConsent.managedSupported operation then do
    let some management := settings.lifecycleManagement
      | throw (IO.userError "local lifecycleManagement pin required before signing")
    NativeLifecycleConsent.expectedManagedPlanBytes config session.2
      management.managementSubject management.managementKeyId operation request
  else throw (IO.userError "unsupported specialized consent adapter")
  let _ ← IO.ofExcept (NativeSpecializedConsent.checkExact expected candidate)
  pure candidate

partial def serve (settings : Settings) (config : NativeHost.Config) (session : Session config)
    (input output : IO.FS.Stream) : IO Unit := do'''
assert s.count(a)==1;s=s.replace(a,b)
a='''      codec config operation (body.toList.drop 1)
    else consent config updated operation (body.toList.drop 1))'''
b='''      codec config operation (body.toList.drop 1)
    else if operation == 224 then specialized settings config updated (body.toList.drop 1)
    else consent config updated operation (body.toList.drop 1))''';assert s.count(a)==1;s=s.replace(a,b)
s=s.replace('  serve config updated input output','  serve settings config updated input output',1)
s=s.replace('        serve config session (← IO.getStdin) (← IO.getStdout)','        serve settings config session (← IO.getStdin) (← IO.getStdout)',1)
p.write_text(s)
q=Path('/home/hbox/workbox/codex-client-consent-20261003/src/Host/ClientConsentSession.lean');q.write_text(s)
