import Kernel.NativeHost
open Minidregg.Kernel Minidregg.Kernel.DurableDataIntent Minidregg.Kernel.DurableCheckpoint
open Minidregg.Compiler.NativeHostCodec (outcomeCodec outcomeFrame Outcome)
open Minidregg.Theory.TypedAuthorization (Digest)

def d : Digest := ⟨0⟩
def ev : StableEvent := ⟨1, d, d, []⟩
def nul (i : Nat) : StableNullifier := ⟨1, d, ⟨i + 1⟩, [UInt8.ofNat i]⟩
def wr (p : Nat × Nat) : DataWrite := ⟨⟨100 + p.1⟩, d, d, List.replicate p.2 0⟩

def mk (sizes : List Nat) (nulls : List StableNullifier) : DataIntent (fun _ => d) :=
  { transactionId := ⟨7⟩, writes := ((List.range sizes.length).zip sizes).map wr, readGuards := [],
    nullifiers := nulls, exactCharge := fun _ => 0, event := ev, subject := none,
    postRootsBound := by intro w h; simp only [List.mem_map] at h; obtain ⟨p, _, rfl⟩ := h; rfl
    guardsReadOnly := by intro g h; simp at h }

def image : DurableReceiver.Image := ⟨⟨[], [], fun _ => 10⟩, []⟩

/-- The real durable admission (`DurableCheckpoint.prepare`) on a genesis image, its rejection
mapped as the receiver maps it (`NativeHost.durableRefusal`), encoded and decoded by the
outcome codec: what a client reads on the wire. -/
def run (label : String) (intent : DataIntent (fun _ => d)) : IO Unit := do
  let state := State.ofSeed image.seed
  match h : resume (fun _ => d) image 0 state with
  | none => IO.println s!"{label}: resume refused"
  | some before =>
    match prepare image 0 state before (Nat.zero_le _) h intent with
    | .inl _ => IO.println s!"{label}: prepared (within every bound; the executor accepted)"
    | .inr (.rejected r@(.overBound ..)) =>
      let bytes := outcomeCodec.encode (NativeHost.durableRefusal r)
      let tag := String.fromUTF8! ⟨(bytes.take outcomeFrame.length).toArray⟩
      match outcomeCodec.decode bytes with
      | some (.refused reason phase detail _) =>
        IO.println s!"{label}: wire {tag} reason-byte-prefix {(bytes.drop outcomeFrame.length).take 4} -> refused {reason.name} phase {String.fromUTF8! ⟨phase.toArray⟩} detail {String.fromUTF8! ⟨detail.toArray⟩}"
      | _ => IO.println s!"{label}: DID NOT DECODE"
    | .inr (.rejected r) => IO.println s!"{label}: past the bound check; rejected later by {repr r}"
    | .inr _ => IO.println s!"{label}: past the bound check; other outcome"

def main : IO Unit := do
  run "plant nullifiers 65" (mk [] ((List.range 65).map nul))
  run "control nullifiers 64" (mk [] ((List.range 64).map nul))
  run "plant post 8388609 B" (mk [Bounds.cellBytesMax + 1] [])
  run "control post 8388608 B" (mk [Bounds.cellBytesMax] [])
  run "old bound post 1048577 B (accepted since ruling 2)" (mk [1048577] [])
  run "plant writes 257" (mk (List.replicate 257 1) [])
  run "control writes 256" (mk (List.replicate 256 1) [])

#eval main
