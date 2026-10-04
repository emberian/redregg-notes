from pathlib import Path
root=Path('/home/hbox/workbox/codex-unified-integration-20261003/src/Host')
p=root/'ClientConsentSession.lean';s=p.read_text()
s=s.replace('import Kernel.NativeLifecycleConsent\n','')
s=s.replace('namespace Minidregg.Host.ClientConsentSession','namespace Minidregg.Host.ClientConsentCore',1)
a='''def specialized (settings : Settings) (config : NativeHost.Config) (session : Session config)'''
b='''abbrev ExtraExpected := (settings : Settings) → (config : NativeHost.Config) →
  Session config → UInt8 → List UInt8 → IO (List UInt8)

def specialized (extraExpected : ExtraExpected) (settings : Settings) (config : NativeHost.Config) (session : Session config)'''
assert s.count(a)==1;s=s.replace(a,b)
a='''  else if NativeLifecycleConsent.supported operation then
    NativeLifecycleConsent.expectedPlanBytes config session.2 operation request
  else if NativeLifecycleConsent.managedSupported operation then do
    let some management := settings.lifecycleManagement
      | throw (IO.userError "local lifecycleManagement pin required before signing")
    NativeLifecycleConsent.expectedManagedPlanBytes config session.2
      management.managementSubject management.managementKeyId operation request
  else throw (IO.userError "unsupported specialized consent adapter")'''
b='''  else extraExpected settings config session operation request'''
assert s.count(a)==1;s=s.replace(a,b)
s=s.replace('partial def serve (settings : Settings)','partial def serve (extraExpected : ExtraExpected) (settings : Settings)',1)
s=s.replace('then specialized settings config updated','then specialized extraExpected settings config updated',1)
s=s.replace('  serve settings config updated input output','  serve extraExpected settings config updated input output',1)
s=s.replace('def run (arguments : List String)','def run (extraExpected : ExtraExpected) (arguments : List String)',1)
s=s.replace('        serve settings config session','        serve extraExpected settings config session',1)
s=s[:s.index('end Minidregg.Host.ClientConsentSession')]+'end Minidregg.Host.ClientConsentCore\n'
(root/'ClientConsentCore.lean').write_text(s)
full='''/- Full-peer consent entry with source-native lifecycle adapters. -/
import Host.ClientConsentCore
import Host.NativeLifecycleConsent
open Minidregg.Kernel
namespace Minidregg.Host.ClientConsentSession
private def lifecycleExpected : ClientConsentCore.ExtraExpected := fun settings config session operation request => do
  if NativeLifecycleConsent.supported operation then
    NativeLifecycleConsent.expectedPlanBytes config session.2 operation request
  else if NativeLifecycleConsent.managedSupported operation then do
    let some management := settings.lifecycleManagement
      | throw (IO.userError "local lifecycleManagement pin required before signing")
    NativeLifecycleConsent.expectedManagedPlanBytes config session.2
      management.managementSubject management.managementKeyId operation request
  else throw (IO.userError "unsupported specialized consent adapter")
def run (arguments : List String) : IO UInt32 :=
  ClientConsentCore.run lifecycleExpected arguments
end Minidregg.Host.ClientConsentSession
def main (arguments : List String) : IO UInt32 := do
  try Minidregg.Host.ClientConsentSession.run arguments
  catch error =>
    IO.eprintln s!"minidregg-client-consent: {error}"
    pure 1
'''
p.write_text(full)
base='''/- Independent full-peer ordinary/money/enrollment/fleet consent entry.
Higher lifecycle families refuse explicitly until the full entry is available. -/
import Host.ClientConsentCore
namespace Minidregg.Host.ClientConsentSpecializedSession
private def unsupported : ClientConsentCore.ExtraExpected := fun _ _ _ _ _ =>
  throw (IO.userError "this consent entry has no adapter for the selected lifecycle family")
def run (arguments : List String) : IO UInt32 :=
  ClientConsentCore.run unsupported arguments
end Minidregg.Host.ClientConsentSpecializedSession
def main (arguments : List String) : IO UInt32 := do
  try Minidregg.Host.ClientConsentSpecializedSession.run arguments
  catch error =>
    IO.eprintln s!"minidregg-client-consent: {error}"
    pure 1
'''
(root/'ClientConsentSpecializedSession.lean').write_text(base)
owned=Path('/home/hbox/workbox/codex-client-consent-20261003/src/Host')
for name in ['ClientConsentCore','ClientConsentSession','ClientConsentSpecializedSession']:(owned/(name+'.lean')).write_text((root/(name+'.lean')).read_text())
