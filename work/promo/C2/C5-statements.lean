/- CX-PROMO-2 scratch (NOT landed): the C5 statements over `selectHole`, elaborated with `sorry` to measure that they
state with no hypothesis beyond the deployed objects. -/
import Lang.LiveHoles
import Lang.Proofs.Check

namespace Nanodregg.Lang
open Nanodregg.Kernel.Receive

variable {D : Type} {digestOf : ByteArray → Option D} {look : Pinned D} {rv : RowView D} {self : D}
  {h : HoleROM} {s : HoleSelection}

/-- T2 (successor of `strengthening_sound` + `suspended_sound`'s used-hypothesis arm): a selection strengthens
away EXACTLY the hypotheses whose pins do not hold, and the selected code uses none of them. -/
theorem selectHole_hypotheses (hs : selectHole digestOf look rv self h = .ok s) :
    ∃ c, h.code[s.index]? = some c ∧ s.original = c.body ∧
      ∀ x p, h.hypotheses[x]? = some (some p) →
        (x ∈ s.strengthened ↔ supportLive digestOf look rv self p = false) ∧
        (supportLive digestOf look rv self p = false → Term.usesVar x c.body = false) := sorry

/-- T3 (transport; successor of `strengthening_sound`'s factor clause, `CalculusLaws.strengthen_lemma` and
`strengthen_factor` at the deployed runtime): on an installed ROM, the strengthened filling types at the
strengthened context, and its re-embedding is exactly the ROM code. -/
theorem selectHole_factor {Δ : List Ty} (hchk : h.check Δ = .ok ())
    (hs : selectHole digestOf look rv self h = .ok s) :
    HasType Δ s.context s.filling h.ty ∧ s.body = s.original := sorry

/-- T4 (completeness; successor of `judge_verified_iff`'s ← direction and `select_ok`): when the row names `i`,
every support of code `i` is observed and holds, every hypothesis pin is observed and every USED one holds, and
the guard runs to `true` on its observed pin, the hole selects `i`. -/
theorem selectHole_live_selects {amount ver i used : Nat} {bytes : ByteArray} {c : HoleCode}
    (hrow : holeRow rv self h.selectionRel h.selectionKey = .ok (some (.row amount bytes ver)))
    (hdec : Wire.decodeData .nat bytes = .ok (.nat i)) (hc : h.code[i]? = some c)
    (hsup : ∀ p ∈ c.supports, supportObserved digestOf look p = true ∧
      supportLive digestOf look rv self p = true)
    (hhyp : ∀ x p, h.hypotheses[x]? = some (some p) →
      supportPinned digestOf look rv self p = .ok () ∧
      (Term.usesVar x c.body = true → supportLive digestOf look rv self p = true))
    (hgp : ∀ p, h.guardPin = some p → supportPinned digestOf look rv self p = .ok ())
    (hguard : run [] Bounds.stackMax Bounds.holeGuardFuel 0
      (State.init h.guard [.bool (h.guardPin.all (supportLive digestOf look rv self))]) = .value (.bool true) used) :
    ∃ s, selectHole digestOf look rv self h = .ok s ∧ s.index = i ∧ s.version = ver := sorry

end Nanodregg.Lang
