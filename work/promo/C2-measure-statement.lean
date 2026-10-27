/- CX-PROMO scratch (NOT landed): the D.2 measurement of PROGRAM-20261022 §3 P2 C2. `selectHole_judge` written
as a STATEMENT at nano 4916f3a (+ the C9 prototype), elaborated with `sorry` only to confirm it is well-typed.
Every hypothesis the statement needs beyond "the World is `kernelWorld`" is a named binder below, counted (a). -/
import Lang.LiveHoles
import Lang.Contextual.LangInstance

namespace C2Measure
open Nanodregg.Lang Nanodregg.Lang.Contextual Nanodregg.Kernel Nanodregg.Kernel.Receive

variable {D : Type} [DecidableEq D]

/-- (a1) The closure's `Token` is `⟨id : Nat, ver : Nat⟩`; a deployed pin is a row slot (`rel`, key BYTES,
`ver`) or a cell id (BYTES). A `World`'s `live : Token → Bool` must be decided from a token, so a decode is
needed, and the encode must be injective: two binders and one hypothesis. -/
def kernelWorld (dec : Token → Option SupportPin) (digestOf : ByteArray → Option D) (look : Pinned D)
    (rv : RowView D) (self : D) (env : Bool) : Contextual.World Bool where
  live t := match dec t with
    | some p => supportLive digestOf look rv self p
    | none => false
  env := env

/-- (a3) The deployed guard reads the guard pin's liveness (`present`), never the filling; `judge`'s guard is
`E → Tm → Bool`. Encoded with `E := Bool` (= present) and the guard run under its fixed fuel; a run that
faults (`guardFault`) has no Bool, so it is mapped to `false` here and the iff needs (a4). -/
def romGuard (h : HoleROM) (present : Bool) (_filling : Term) : Bool :=
  match run [] Bounds.stackMax Bounds.holeGuardFuel 0 (State.init h.guard [.bool present]) with
  | .value (.bool b) _ => b
  | _ => false

/-- The ROM as an interface. `hyps` keeps the positions with a pin; `hyps_real` needs the context to
have them (true of a checked ROM: `HoleROM.check`'s `hypotheses.length = ctx.length`): a proof obligation
on construction, (a5). Budget: HoleROM has none, so `cost ≤ budget` is forced by budget := cost := 0. -/
def romIface (enc : SupportPin → Token) (h : HoleROM)
    (hreal : ∀ x ∈ (h.hypotheses.zipIdx.filterMap fun pi => pi.1.map fun p => (pi.2, enc p)),
      (langData.lookup h.ctx x.1).isSome = true) : Iface langData Bool where
  name := h.name
  ctx := h.ctx
  ty := h.ty
  hyps := h.hypotheses.zipIdx.filterMap fun pi => pi.1.map fun p => (pi.2, enc p)
  hyps_real := hreal
  guard := romGuard h
  budget := 0
  chooser := 0
  acceptor := 0

/-- Candidate `i`: its body, its supports encoded; no blockers and no cost exist in a HoleROM. -/
def romCandidate (enc : SupportPin → Token) (c : HoleCode) : Candidate langData :=
  ⟨c.body, c.supports.map enc, [], 0, 0, .verified⟩

/-- **The statement** (sorry: a measurement, never landed). Binders/hypotheses beyond `kernelWorld`:
(a1) `enc`/`dec` with `hdec` (token encoding); (a2) `hsel`: the selection row is present and decodes to `i`
with `h.code[i]? = some c` (selectionAbsent / selectionType / selectionIndex are PRE-judgment);
(a3) the guard encoding `romGuard`, (a4) `hfuel`: the guard does not fault (guardFault has no Status);
(a5) `hreal`; (a6) `hpinned`: every pin of the ROM observed (unpinned is pre-judgment);
(a7) `hchecked`: the candidate types at `Δ = []`, because `langData.check` is `Lang.infer [] Ψ M` while the
deployed check is at the imports' interfaces `Δ` (`HoleROM.check Δ`). -/
theorem selectHole_judge (enc : SupportPin → Token) (dec : Token → Option SupportPin)
    (hdec : ∀ p, dec (enc p) = some p)
    (digestOf : ByteArray → Option D) (look : Pinned D) (rv : RowView D) (self : D) (h : HoleROM)
    (i : Nat) (c : HoleCode) (amount : Nat) (bytes : ByteArray) (ver : Nat)
    (hsel : holeRow rv self h.selectionRel h.selectionKey = .ok (some (.row amount bytes ver)) ∧
      Wire.decodeData .nat bytes = .ok (.nat i) ∧ h.code[i]? = some c)
    (hfuel : ∀ b, ∃ v used, run [] Bounds.stackMax Bounds.holeGuardFuel 0 (State.init h.guard [.bool b]) =
      .value (.bool v) used)
    (hreal : ∀ x ∈ (h.hypotheses.zipIdx.filterMap fun pi => pi.1.map fun p => (pi.2, enc p)),
      (langData.lookup h.ctx x.1).isSome = true)
    (hpinned : (∀ p ∈ c.supports, supportObserved digestOf look p = true) ∧
      (∀ o ∈ h.hypotheses, ∀ p, o = some p → supportPinned digestOf look rv self p = .ok ()) ∧
      (∀ p, h.guardPin = some p → supportPinned digestOf look rv self p = .ok ()))
    (hchecked : langData.check h.ctx c.body h.ty = true) :
    (∃ s, selectHole digestOf look rv self h = .ok s) ↔
      judge (romIface enc h hreal)
        (kernelWorld dec digestOf look rv self (h.guardPin.all (supportLive digestOf look rv self)))
        (romCandidate enc c) = .verified := by
  sorry

end C2Measure
