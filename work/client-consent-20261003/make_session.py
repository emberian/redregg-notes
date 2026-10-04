from pathlib import Path
root=Path('/Users/ember/dev/redregg/work/client-consent-20261003')
reader=(root/'reader.lean').read_text()
settings=reader[reader.index('structure JointConsensusSettings'):reader.index('\ndef profileDescription')]
settings=settings.replace('namespace Minidregg.Host.SourceAgreementReader','namespace Minidregg.Host.ClientConsentSession')
settings=settings.replace('  unless settings.jointConsensus.isSome do\n    throw (IO.userError "source-agreement reader requires an explicit consensus pin")\n','')
settings=settings.replace('ordinary source-agreement reader','client consent provider')
# These fields are interpreted by the native Config; service selectors do not
# belong to this reader and are rejected rather than silently ignored.
settings=settings.replace('structure Settings where','''structure GatewayPinSettings where
  application : String
  subject : Nat
  target : Nat
  capability : Nat
  policyAddress : String
  deriving FromJson, ToJson

structure GrainBirthTariffSettings where
  base : Nat
  perBirth : Nat
  deriving FromJson, ToJson

structure Settings where''')
settings=settings.replace('  jointConsensus : Option JointConsensusSettings := none','''  jointConsensus : Option JointConsensusSettings := none
  fnGateway : Option GatewayPinSettings := none
  grainBirthTariff : Option GrainBirthTariffSettings := none
  completionCustodianKey : Option String := none''')
settings=settings.replace('  jointConsensus := settings.jointConsensus.map JointConsensusSettings.context','''  jointConsensus := settings.jointConsensus.map JointConsensusSettings.context
  fnGateway := settings.fnGateway.map fun pin =>
    ⟨pin.application.toUTF8.toList, ⟨pin.subject⟩, pin.target,
      ⟨pin.capability⟩, ⟨pin.policyAddress.toNat!.toNat⟩⟩
  grainBirthTariff := settings.grainBirthTariff.map fun tariff => ⟨tariff.base, tariff.perBirth⟩
  completionCustodianKey := settings.completionCustodianKey.map fun key =>
    (SourceAgreementJson.decodeHex "completionCustodianKey" (.str key)).toOption.getD []''')
settings=settings.replace('pin.policyAddress.toNat!.toNat','pin.policyAddress.toNat!')
settings=settings.replace('"jointConsensus", "nockFSync", "disabledEvaluators"]','"jointConsensus", "nockFSync", "disabledEvaluators", "fnGateway",\n    "grainBirthTariff", "completionCustodianKey"]')
settings=settings.replace('  IO.ofExcept settings.checkDisabledEvaluators','''  if let some pin := settings.fnGateway then
    let some address := pin.policyAddress.toNat? | throw (IO.userError "invalid gateway policy address")
    unless toString address == pin.policyAddress do
      throw (IO.userError "noncanonical gateway policy address")
  if let some tariff := settings.grainBirthTariff then
    unless 0 < tariff.base do throw (IO.userError "grain birth tariff base must be positive")
  if let some key := settings.completionCustodianKey then
    let bytes ← IO.ofExcept (SourceAgreementJson.decodeHex "completionCustodianKey" (.str key))
    unless bytes.length == 32 && SourceAgreementJson.encodeHex bytes == key do
      throw (IO.userError "noncanonical completion custodian key")
  IO.ofExcept settings.checkDisabledEvaluators''')
transport=reader[reader.index('def splitKind'):reader.index('\ndef opened')]
body='''
/-- The retained proof is updated only by independent native admission. The
physical Store/MAC is merely an input reader, never a semantic trust source. -/
abbrev Session (config : NativeHost.Config) := Sigma (NativeHostReplay.Verified config)

def verifyInitial (config : NativeHost.Config) : IO (Session config) := do
  let target ← IO.ofExcept (← DurableReceiverIO.load config.transport ResourceBirthCodec.rootBytes)
  match ← NativeHostReplay.verifyLoaded config target with
  | .error failure => throw (IO.userError s!"consent prefix refused at {failure.index}: {failure.detail}")
  | .ok verified => pure ⟨target, verified⟩

def refresh (config : NativeHost.Config) (old : Session config) : IO (Session config) := do
  let target ← IO.ofExcept (← DurableReceiverIO.load config.transport ResourceBirthCodec.rootBytes)
  match ← NativeHostReplay.extendVerified config old.2 target with
  | .error failure => throw (IO.userError s!"consent extension refused at {failure.index}: {failure.detail}")
  | .ok verified => pure ⟨target, verified⟩

def headersBytes (headers : List (List UInt8)) : List UInt8 :=
  (Lean.toJson (headers.map SourceAgreementJson.encodeHex)).compress.toUTF8.toList

def consent (config : NativeHost.Config) (session : Session config) (operation : UInt8)
    (payload : List UInt8) : IO (List UInt8) := do
  let (intentBytes, rest) ← splitPair payload
  let some wanted := NativeObservationCodec.intentCodec.decode intentBytes
    | throw (IO.userError "noncanonical retained local intent")
  match operation with
  | 220 =>
      -- Before even the first intent signature, bind subject/current key to
      -- locally chosen custody, rather than a remote JSON subject label.
      let key ← IO.ofExcept ((NativeObservationController.intentKey
        (NativeHost.observationContext config session.2.opened) wanted.subject).mapError
        (fun _ => "local intent subject has no current signing key"))
      unless rest.length == 32 && key == rest do
        throw (IO.userError "local intent subject differs from custody signer")
      pure intentBytes
  | 221 =>
      let (signature, candidate) ← splitPair rest
      let checked ← IO.ofExcept (NativeClientConsent.checkObservation config session.2 wanted signature candidate)
      pure (headersBytes checked.headers)
  | 222 =>
      let headers ← IO.ofExcept (NativeClientConsent.checkIntentPlan config session.2 wanted rest)
      pure (headersBytes headers)
  | _ => throw (IO.userError "unsupported consent operation")

partial def serve (config : NativeHost.Config) (session : Session config)
    (input output : IO.FS.Stream) : IO Unit := do
  let first ← input.read 1
  if first.isEmpty then return
  let lengthWire ← readExactly input 4 first
  let length := frameLength lengthWire
  unless 0 < length && length ≤ maxFrame do throw (IO.userError "consent frame exceeds bound")
  let body ← readExactly input length
  let operation := body[0]!
  -- A failed refresh terminates the provider: no cached success may survive
  -- an observed rollback, rewritten prefix, or failed semantic suffix.
  let updated ← refresh config session
  let answer ← try pure (operation, ← consent config updated operation (body.toList.drop 1))
    catch error => pure (255, error.toString.toUTF8.toList)
  writeSessionFrame output answer.1 answer.2
  serve config updated input output

def run (arguments : List String) : IO UInt32 := do
  match arguments with
  | [path, "stdio"] =>
      let settings ← loadSettings path
      withPinnedSignature settings.config fun config => do
        let session ← verifyInitial config
        serve config session (← IO.getStdin) (← IO.getStdout)
        pure 0
  | _ => throw (IO.userError "usage: minidregg-client-consent CONFIG stdio")
end Minidregg.Host.ClientConsentSession

def main (arguments : List String) : IO UInt32 := do
  try Minidregg.Host.ClientConsentSession.run arguments
  catch error =>
    IO.eprintln s!"minidregg-client-consent: {error}"
    pure 1
'''
header='''/- Local full-peer consent process. Settings and executable are selected by
local custody. The operator supplies proposed frames only. Initial history is
independently re-admitted once; later frames verify only an exact source suffix.
No protected Store is transmitted by this process. Thin peers need a separate
selective authenticated witness producer; this executable is not that producer.
-/
import Kernel.NativeClientConsent
import Kernel.NativeHostGenesis
import Compiler.GenericSimplexSourceAnchor
import Compiler.FnEvidenceCodec
import Host.SourceAgreementJson
import Host.RequestRefusal
import Lean.Data.Json

open Lean Minidregg.Compiler Minidregg.Compiler.NativeHostCodec
open Minidregg.Compiler.Tower256ConcreteBackend Minidregg.Kernel
namespace Minidregg.Host.ClientConsentSession
'''
(root/'ClientConsentSession.lean').write_text(header+settings+'\n'+transport+'\n'+body)
