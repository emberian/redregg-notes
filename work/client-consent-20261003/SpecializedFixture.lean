/- Read-only typed fixture producer. Production native codecs and loaded planners
encode its locally chosen requests and plans; no source or key mutation occurs. -/
import Host.ClientConsentCore
open Minidregg.Kernel Minidregg.Compiler
open Minidregg.Compiler.Tower256ConcreteBackend
open Minidregg.Host

def main (args : List String) : IO UInt32 := do
  match args with
  | [configPath, outputPath] =>
      let settings ← ClientConsentCore.loadSettings configPath
      ClientConsentCore.withPinnedSignature settings.config fun config => do
        let session ← ClientConsentCore.verifyInitial config
        let output : System.FilePath := outputPath
        IO.FS.createDirAll output
        let command : ClockTickReceiver.Command :=
          ⟨⟨7⟩, ⟨43⟩, 98765109, session.2.opened.authority.snapshot.cell.root, ⟨0⟩, 1, 1⟩
        let request := ClockTickReceiver.commandCodec.encode command
        let plan ← IO.ofExcept (NativeHost.clockPlanLoaded config session.2.opened request)
        let save := fun (name : String) (bytes : List UInt8) => IO.FS.writeBinFile (output / name) bytes.toByteArray
        save "clock-request.bin" request
        save "clock-plan.bin" (ClockTickReceiver.signingPlanCodec.encode plan)
        save "clock-changed-profile.bin" (ClockTickReceiver.signingPlanCodec.encode
          { plan with semantics := ⟨plan.semantics.value + 1⟩ })
        save "clock-changed-header.bin" (ClockTickReceiver.signingPlanCodec.encode
          { plan with header := plan.header ++ [0] })
        let changed := { command with nonce := command.nonce + 1 }
        save "clock-changed-request.bin" (ClockTickReceiver.commandCodec.encode changed)
        let some selected := Minidregg.Theory.CredentialAuthorityState.currentSigningKey
            session.2.opened.authority.snapshot.logical ⟨7⟩
          | throw (IO.userError "fixture custody key unavailable")
        let enrollment : ParticipantKeyEnrollment.Command :=
          ⟨⟨7⟩, ⟨43⟩, 98765110, ⟨0⟩, session.2.opened.authority.snapshot.cell.root, selected⟩
        save "possession-command.bin" (ParticipantKeyEnrollment.commandCodec.encode enrollment)
        save "possession-frame.bin" (ParticipantKeyEnrollment.possessionFrame config.deployment.domain config.profile.semantics enrollment)
        IO.println "SOURCE NATIVE SPECIALIZED FIXTURES PASS"
        pure 0
  | _ => throw (IO.userError "usage: fixture CONFIG OUTPUT")
