
/-! ## C7 scratch: a support pin precedes what its Turn writes -/

private theorem touchCheck_acts {E : Env D} {w : World D} {x : Touch D} {r : Option (Post D)}
    (h : touchCheck E w x = .ok r) (hact : x.act ≠ .keep) :
    ∃ cell v p, w.entry E x.cell = some (.live cell v) ∧ r = some p := by
  unfold touchCheck at h
  simp only [except_bind_ok] at h
  obtain ⟨⟨⟩, -, h⟩ := h
  revert h
  generalize w.entry E x.cell = cur
  intro h
  cases hx : x.act with
  | keep => exact absurd hx hact
  | write ops =>
      rw [hx] at h
      rcases cur with _ | (⟨cell, ver⟩ | _)
      · cases h
      · simp only [except_bind_ok] at h
        obtain ⟨⟨⟩, -, post, -, hp⟩ := h
        simp only [pure, Except.pure, Except.ok.injEq] at hp
        exact ⟨cell, ver, _, rfl, hp.symm⟩
      · cases h
  | retire =>
      rw [hx] at h
      rcases cur with _ | (⟨cell, ver⟩ | _)
      · cases h
      · simp only [except_bind_ok] at h
        obtain ⟨⟨⟩, -, hp⟩ := h
        simp only [pure, Except.pure, Except.ok.injEq] at hp
        exact ⟨cell, ver, _, rfl, hp.symm⟩
      · cases h

/-- A touch that writes or retires leaves its cell strictly past the entry its pin was checked on. -/
private theorem admit_touch_adv {E : Env D} {w w' : World D} {t : Turn D}
    (h : World.admit E w t = .ok w') {x : Touch D} (hx : x ∈ t.touches) (hact : x.act ≠ .keep) :
    EAdv (w.entry E x.cell) (w'.entry E x.cell) := by
  obtain ⟨posts, hk, rfl⟩ := admit_ok h
  have hk' := hk
  obtain ⟨raw, hm, hposts⟩ := hk.touches
  obtain ⟨r, hrm, hr⟩ := mapEx_fwd hm x hx
  obtain ⟨cell0, v0, p, hlive, rfl⟩ := touchCheck_acts hr hact
  have hent : (commit E w t posts).entry E x.cell =
      match (insertAll E (insertAll E w.trie (posts.map Post.pair)) (bornEntries t)).get (trieSpec E)
        (.cell x.cell) with
      | some (.entry e) => some e
      | _ => none := by
    show (match (commitTrie E w t posts).get (trieSpec E) (.cell x.cell) with
      | some (.entry e) => some e
      | _ => none) = _
    rw [commitTrie_cell]
  have hb : x.cell ∉ (bornEntries t).map Prod.fst := by
    intro hb
    obtain ⟨⟨c', e'⟩, hm', hce⟩ := List.mem_map.mp hb
    simp only at hce
    subst hce
    unfold bornEntries at hm'
    obtain ⟨⟨c'', cell⟩, hm'', hce'⟩ := List.mem_map.mp hm'
    simp only [Prod.mk.injEq] at hce'
    obtain ⟨rfl, -⟩ := hce'
    have hnot : w.taken E x.cell = false := by
      have := hk'.creates
      unfold checkCreates at this
      simp only [except_bind_ok] at this
      obtain ⟨⟨⟩, -, ⟨⟩, -, ⟨⟩, -, hf⟩ := this
      have := req_ok.mp (forEx_ok.mp hf x.cell (List.mem_map.mpr ⟨(x.cell, cell), hm'', rfl⟩))
      simpa using this
    unfold World.taken at hnot
    rw [hlive] at hnot
    cases hnot
  have hpm : x.cell ∈ (posts.map Post.pair).map Prod.fst := by
    have hp' : p ∈ posts := by
      rw [hposts]
      simpa [List.reduceOption, List.mem_filterMap] using hrm
    exact List.mem_map.mpr ⟨p.pair, List.mem_map.mpr ⟨p, hp', rfl⟩, (touchCheck_adv hr).1⟩
  rw [hent, insertAll_get_of_not_mem hb]
  obtain ⟨e, he, hg⟩ := insertAll_get_mem (m := w.trie) hpm
  rw [hg]
  obtain ⟨q, hqm, hqe⟩ := List.mem_map.mp he
  simp only [Post.pair, Prod.mk.injEq] at hqe
  obtain ⟨hqc, rfl⟩ := hqe
  rw [hposts] at hqm
  have hq' : some q ∈ raw := by simpa [List.reduceOption, List.mem_filterMap] using hqm
  obtain ⟨y, -, hy⟩ := mapEx_mem hm (some q) hq'
  obtain ⟨hc, hadv⟩ := touchCheck_adv hy
  rw [← hqc, hc]
  exact hadv

/-- **A support pin precedes every entry its Turn writes, and every entry after** (C7 scratch). -/
theorem support_precedes {E : Env D} {w w' w'' : World D} {t : Turn D} {l : List (Step D)}
    (hf : w.CellsFit Cell.Fits E) (h : World.admit E w t = .ok w') (hl : World.fold E w' l = .ok w'')
    {x : Touch D} (hx : x ∈ t.touches) (hact : x.act ≠ .keep) :
    x.seen = pinOf E (w.entry E x.cell) ∧
      (x.seen ≠ pinOf E (w''.entry E x.cell) ∨
        CollidesAmong E.hash [pinPre E (w.entry E x.cell), pinPre E (w''.entry E x.cell)]) := by
  obtain ⟨posts, hk, -⟩ := admit_ok h
  obtain ⟨r, hr⟩ := hk.touch x hx
  have hpin := (touchCheck_pin hr).symm
  refine ⟨hpin, ?_⟩
  have hadv : EAdv (w.entry E x.cell) (w''.entry E x.cell) := by
    rcases fold_entryStep x.cell hl with heq | hadv'
    · rw [← heq]; exact admit_touch_adv h hx hact
    · exact eAdv_trans (admit_touch_adv h hx hact) hadv'
  have hf'' : w''.CellsFit Cell.Fits E := fold_cellsFit (admit_cellsFit hf h) hl
  have hpre : pinPre E (w''.entry E x.cell) ≠ pinPre E (w.entry E x.cell) :=
    pinPre_adv_ne (cellsFit_verFit hf _) (cellsFit_verFit hf'' _) hadv
  rw [hpin]
  by_cases hp : pinOf E (w.entry E x.cell) = pinOf E (w''.entry E x.cell)
  · exact .inr ⟨_, List.mem_cons_self, _, List.mem_cons_of_mem _ List.mem_cons_self,
      fun h => hpre h.symm, (pinOf_eq_pre E _).symm.trans (hp.trans (pinOf_eq_pre E _))⟩
  · exact .inl hp
