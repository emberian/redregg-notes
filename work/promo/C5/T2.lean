import Lang.LiveHoles
import Lang.Proofs.Check

namespace Nanodregg.Lang
open Nanodregg.Kernel.Receive

variable {D : Type} {digestOf : ByteArray → Option D} {look : Pinned D} {rv : RowView D} {self : D}

/-- The positions `changedHypotheses` strengthens: every observed hypothesis whose pin does not hold. -/
private def deadPositions (digestOf : ByteArray → Option D) (look : Pinned D) (rv : RowView D) (self : D)
    (zs : List (Option SupportPin × Nat)) : List Nat :=
  zs.filterMap fun pi => match pi.1 with
    | some p => if supportLive digestOf look rv self p then none else some pi.2
    | none => none

/-- `changedHypotheses`'s step, named so its fold can be reasoned about one element at a time. -/
private def chStep (digestOf : ByteArray → Option D) (look : Pinned D) (rv : RowView D) (self : D)
    (h : HoleROM) (c : HoleCode) (removed : List Nat) (pi : Option SupportPin × Nat) :
    Except HoleRefusal (List Nat) :=
  match pi.1 with
  | none => .ok removed
  | some pin => do
    supportPinned digestOf look rv self pin
    if supportLive digestOf look rv self pin then .ok removed
    else if Term.usesVar pi.2 c.body then .error (.supportMoved h.name pi.2)
    else .ok (removed ++ [pi.2])

private theorem changedHypotheses_eq (h : HoleROM) (c : HoleCode) :
    changedHypotheses digestOf look rv self h c =
      h.hypotheses.zipIdx.foldlM (chStep digestOf look rv self h c) [] := rfl

private theorem changed_fold (h : HoleROM) (c : HoleCode) :
    ∀ (zs : List (Option SupportPin × Nat)) (acc r : List Nat),
      zs.foldlM (chStep digestOf look rv self h c) acc = .ok r →
      r = acc ++ deadPositions digestOf look rv self zs ∧
      ∀ pi ∈ zs, ∀ p, pi.1 = some p → supportLive digestOf look rv self p = false →
        Term.usesVar pi.2 c.body = false
  | [], acc, r, hf => by
    simp only [List.foldlM, pure, Except.pure, Except.ok.injEq] at hf
    subst hf; simp [deadPositions]
  | (o, x) :: zs, acc, r, hf => by
    rw [List.foldlM_cons] at hf
    cases o with
    | none =>
      obtain ⟨h1, h2⟩ := changed_fold h c zs acc r hf
      refine ⟨by simp [h1, deadPositions], ?_⟩
      intro pi hpi p hp hl
      rcases List.mem_cons.mp hpi with rfl | hpi
      · cases hp
      · exact h2 pi hpi p hp hl
    | some pin =>
      cases hpin : supportPinned digestOf look rv self pin with
      | error e =>
        have : chStep digestOf look rv self h c acc (some pin, x) = .error e := by
          simp [chStep, hpin, bind, Except.bind]
        rw [this] at hf; cases hf
      | ok u =>
        cases hlive : supportLive digestOf look rv self pin with
        | true =>
          have : chStep digestOf look rv self h c acc (some pin, x) = .ok acc := by
            simp [chStep, hpin, hlive, bind, Except.bind]
          rw [this] at hf
          obtain ⟨h1, h2⟩ := changed_fold h c zs acc r hf
          refine ⟨by simp [h1, deadPositions, hlive], ?_⟩
          intro pi hpi p hp hl
          rcases List.mem_cons.mp hpi with rfl | hpi
          · cases hp; rw [hlive] at hl; cases hl
          · exact h2 pi hpi p hp hl
        | false =>
          cases huse : Term.usesVar x c.body with
          | true =>
            have : chStep digestOf look rv self h c acc (some pin, x) = .error (.supportMoved h.name x) := by
              simp [chStep, hpin, hlive, huse, bind, Except.bind]
            rw [this] at hf; cases hf
          | false =>
            have : chStep digestOf look rv self h c acc (some pin, x) = .ok (acc ++ [x]) := by
              simp [chStep, hpin, hlive, huse, bind, Except.bind]
            rw [this] at hf
            obtain ⟨h1, h2⟩ := changed_fold h c zs (acc ++ [x]) r hf
            refine ⟨by simp [h1, deadPositions, hlive], ?_⟩
            intro pi hpi p hp hl
            rcases List.mem_cons.mp hpi with rfl | hpi
            · exact huse
            · exact h2 pi hpi p hp hl

private theorem changed_fold_ok (h : HoleROM) (c : HoleCode) :
    ∀ (zs : List (Option SupportPin × Nat)) (acc : List Nat),
      (∀ pi ∈ zs, ∀ p, pi.1 = some p → supportPinned digestOf look rv self p = .ok () ∧
        (Term.usesVar pi.2 c.body = true → supportLive digestOf look rv self p = true)) →
      zs.foldlM (chStep digestOf look rv self h c) acc = .ok (acc ++ deadPositions digestOf look rv self zs)
  | [], acc, _ => by simp [List.foldlM, deadPositions, pure, Except.pure]
  | (o, x) :: zs, acc, hz => by
    have hz' : ∀ pi ∈ zs, _ := fun pi hpi => hz pi (List.mem_cons_of_mem _ hpi)
    rw [List.foldlM_cons]
    cases o with
    | none =>
      exact (changed_fold_ok h c zs acc hz').trans (by simp [deadPositions])
    | some pin =>
      obtain ⟨hpin, huse⟩ := hz (some pin, x) List.mem_cons_self pin rfl
      cases hlive : supportLive digestOf look rv self pin with
      | true =>
        have : chStep digestOf look rv self h c acc (some pin, x) = .ok acc := by
          simp [chStep, hpin, hlive, bind, Except.bind]
        rw [this]
        exact (changed_fold_ok h c zs acc hz').trans (by simp [deadPositions, hlive])
      | false =>
        cases hu : Term.usesVar x c.body with
        | true => have := huse hu; rw [hlive] at this; cases this
        | false =>
          have : chStep digestOf look rv self h c acc (some pin, x) = .ok (acc ++ [x]) := by
            simp [chStep, hpin, hlive, hu, bind, Except.bind]
          rw [this]
          exact (changed_fold_ok h c zs (acc ++ [x]) hz').trans (by simp [deadPositions, hlive])

private theorem selectHole_inv {h : HoleROM} {s : HoleSelection}
    (hs : selectHole digestOf look rv self h = .ok s) :
    ∃ c, h.code[s.index]? = some c ∧ s.original = c.body ∧
      changedHypotheses digestOf look rv self h c = .ok s.strengthened := by
  unfold selectHole at hs
  simp only [bind, Except.bind, pure, Except.pure] at hs
  repeat' split at hs
  all_goals first | (simp at hs; done) | skip
  simp only [Except.ok.injEq] at hs
  subst s
  exact ⟨_, ‹h.code[_]? = some _›, rfl, ‹changedHypotheses digestOf look rv self h _ = .ok _›⟩

theorem selectHole_hypotheses {h : HoleROM} {s : HoleSelection}
    (hs : selectHole digestOf look rv self h = .ok s) :
    ∃ c, h.code[s.index]? = some c ∧ s.original = c.body ∧
      ∀ x p, h.hypotheses[x]? = some (some p) →
        (x ∈ s.strengthened ↔ supportLive digestOf look rv self p = false) ∧
        (supportLive digestOf look rv self p = false → Term.usesVar x c.body = false) := by
  obtain ⟨c, hc, ho, hch⟩ := selectHole_inv hs
  refine ⟨c, hc, ho, fun x p hx => ?_⟩
  rw [changedHypotheses_eq] at hch
  obtain ⟨hr, hu⟩ := changed_fold h c _ [] _ hch
  have hmem : (some p, x) ∈ h.hypotheses.zipIdx := List.mem_zipIdx_iff_getElem?.mpr hx
  refine ⟨?_, fun hl => hu _ hmem p rfl hl⟩
  rw [hr, List.nil_append]
  simp only [deadPositions, List.mem_filterMap]
  constructor
  · rintro ⟨⟨o, y⟩, hy, he⟩
    have hy' := List.mem_zipIdx_iff_getElem?.mp hy
    cases o with
    | none => cases he
    | some q =>
      simp only at he
      split at he
      · cases he
      · cases he
        rw [hx] at hy'
        cases hy'
        simpa using ‹¬supportLive digestOf look rv self p = true›
  · intro hl
    exact ⟨(some p, x), hmem, by simp [hl]⟩

theorem selectHole_live_selects {h : HoleROM} {amount ver i used : Nat} {bytes : ByteArray} {c : HoleCode}
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
    ∃ s, selectHole digestOf look rv self h = .ok s ∧ s.index = i ∧ s.version = ver := by
  have hch : changedHypotheses digestOf look rv self h c =
      .ok (deadPositions digestOf look rv self h.hypotheses.zipIdx) := by
    rw [changedHypotheses_eq]
    simpa using changed_fold_ok h c h.hypotheses.zipIdx [] (fun pi hpi p hp => by
      obtain ⟨o, x⟩ := pi
      simp only at hp
      subst hp
      exact hhyp x p (List.mem_zipIdx_iff_getElem?.mp hpi))
  have hg : runHoleGuard digestOf look rv self h = .ok used := by
    unfold runHoleGuard
    cases hgp' : h.guardPin with
    | none =>
      simp only [hgp', Option.all_none] at hguard
      simp [bind, Except.bind, pure, Except.pure, hguard]
    | some p =>
      simp only [hgp', Option.all_some] at hguard
      simp [bind, Except.bind, pure, Except.pure, hgp p hgp', hguard]
  have h1 : c.supports.all (supportObserved digestOf look) = true :=
    List.all_eq_true.mpr fun p hp => (hsup p hp).1
  have h3 : c.supports.all (supportLive digestOf look rv self) = true :=
    List.all_eq_true.mpr fun p hp => (hsup p hp).2
  have h2 : c.supports.all (rowSupportHolds digestOf look rv self) = true :=
    List.all_eq_true.mpr fun p hp => by
      cases p <;> simp only [rowSupportHolds] <;> first | rfl | exact (hsup _ hp).2
  unfold selectHole
  simp only [hrow, hdec, hc, h1, h2, h3, hch, hg, bind, Except.bind, pure, Except.pure]
  exact ⟨_, rfl, rfl, rfl⟩

end Nanodregg.Lang
