
/-- PROT-1 scratch: **a run's rows are the edits its guards admitted.** -/
theorem runMeasuredWith_rows_guarded {D : Type} {bytesOf : D → ByteArray} {digestOf : ByteArray → Option D}
    {setup : Kernel.Receive.Pinned D → Kernel.Receive.RowView D → D → Kernel.Slots → Nat → ByteArray → Kernel.Receive.Req D → Except (Kernel.Receive.Refusal D) RunSetup}
    {look : Kernel.Receive.Pinned D} {rv : Kernel.Receive.RowView D} {pkg : D} {state : Kernel.Slots}
    {method : Nat} {args : ByteArray} {r : Kernel.Receive.Req D} {budget : Nat} {s : Kernel.Slots}
    {calls : List (Kernel.Receive.Body D)} {rows : List (Kernel.RowSlot D × Kernel.RowAct)} {t n : Nat}
    (h : runMeasuredWith bytesOf digestOf setup look rv pkg state method args r budget = .ok (s, calls, rows, t, n)) :
    ∃ S e es, setup look rv pkg state method args r = .ok S ∧ editsOf S.rels r.self e = .ok es ∧
      guardEdits bytesOf digestOf S rv pkg r es = .ok () ∧ rows = es.map (fun x => (x.slot, x.act)) := by
  unfold runMeasuredWith at h
  simp only [bind, Except.bind, pure, Except.pure] at h
  split at h
  · cases h
  rename_i S hS
  repeat' split at h
  all_goals first | (simp at h; done) | skip
  simp only [Except.ok.injEq, Prod.mk.injEq] at h
  obtain ⟨-, -, rfl, -, -⟩ := h
  exact ⟨S, _, _, hS, ‹editsOf _ _ _ = .ok _›, ‹guardEdits _ _ _ _ _ _ _ = .ok _›, rfl⟩
