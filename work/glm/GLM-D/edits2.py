import sys, pathlib
root = pathlib.Path.home() / "nd-land/glm-d"

def edit(rel, old, new, count=1):
    p = root / rel
    t = p.read_text()
    n = t.count(old)
    if n != count:
        print(f"ANCHOR-MISS {rel}: found {n} wanted {count}"); sys.exit(1)
    p.write_text(t.replace(old, new))
    print(f"ok {rel}")

# E: Authority.lean — grant_root_owner after grant_rooted
edit("Kernel/Proofs/Authority.lean",
"""      rw [req_ok] at hr
      rcases hw with hw | hw <;> simp_all
""",
"""      rw [req_ok] at hr
      rcases hw with hw | hw <;> simp_all

omit [Ord D] in
/-- **A root grant's issuer owns its target** (cv 01a17d72-9475). A derived parentless grant names
a live pinned cell at its target whose owner slot reads back as the actor — the check
`checkParent`'s root arm makes (`notOwner`, `missingCell` or `malformedCell` otherwise) — so a
root grant confers its issuer's ownership and none is admitted useless. -/
theorem grant_root_owner {X : Ctx D} {look : Pinned D} {c : Call D} {a : At D} {target grantee : D}
    {rights : List Right} {d : Draft D}
    (h : grant X look c a target grantee rights none = .ok d) :
    ∃ cell, look target = .ok (some cell) ∧ slotDigest X target cell slotOwner = .ok a.actor := by
  unfold grant at h
  simp only [except_bind_ok] at h
  obtain ⟨_, _, ⟨⟩, _, _, hp, _⟩ := h
  simp only [checkParent, except_bind_ok] at hp
  obtain ⟨⟨⟩, hlook, hown, hreq, _⟩ := hp
  rw [req_ok] at hreq
  refine ⟨_, hlook, ?_⟩
  rw [hown, hreq]
""")

# F1: Ledger.lean — account_creates over the reading receiver
edit("Kernel/Proofs/Ledger.lean",
"""theorem account_creates {X : Ctx D} {asset owner : D} {d : Draft D}
    (h : account X asset owner = .ok d) :
    d.creates = [(accountId X owner asset, accountCell X owner (X.env.bytes asset) 0)] ∧
      d.effects = [] ∧ d.nullifiers = [] := by
  simp only [account, pure, Except.pure, Except.ok.injEq] at h
  subst h
  exact ⟨rfl, rfl, rfl⟩
""",
"""theorem account_creates {X : Ctx D} {look : Pinned D} {asset owner : D} {d : Draft D}
    (h : account X look asset owner = .ok d) :
    d.creates = [(accountId X owner asset, accountCell X owner (X.env.bytes asset) 0)] ∧
      d.effects = [] ∧ d.nullifiers = [] := by
  unfold account at h
  simp only [except_bind_ok] at h
  obtain ⟨(_, _), _, _, h⟩ := h
  simp only [pure, Except.pure, Except.ok.injEq] at h
  subst h
  exact ⟨rfl, rfl, rfl⟩
""")

# F2: Ledger.lean — account_asset_well
edit("Kernel/Proofs/Ledger.lean",
"""omit [Ord D] [DecidableEq D] in
/-- What a use of a counted right through `via` spends (KERNEL-60): nothing for the owner's own
authority, else the pinned live grant's `spendAt`. -/
""",
"""omit [Ord D] [DecidableEq D] in
/-- **An account's asset is a well** (LEDGER-3; cv 01a17d72-9475): an admitted open pins a live
account at the asset whose denomination is the asset's own id, so an account never opens of an
asset nobody issued. -/
theorem account_asset_well {X : Ctx D} {look : Pinned D} {asset owner : D} {d : Draft D}
    (h : account X look asset owner = .ok d) :
    ∃ cell v, readAccount look asset = .ok (cell, v) ∧ v.denom = X.env.bytes asset := by
  unfold account at h
  simp only [except_bind_ok] at h
  obtain ⟨(cell, v), hra, hw, _⟩ := h
  rw [req_ok, decide_eq_true_eq] at hw
  exact ⟨cell, v, hra, hw⟩

omit [Ord D] [DecidableEq D] in
/-- What a use of a counted right through `via` spends (KERNEL-60): nothing for the owner's own
authority, else the pinned live grant's `spendAt`. -/
""")

# G1: Sim Gen.lean — capArms: the root transfer/mutate grants pin the target account
edit("Kernel/Sim/Gen.lean",
"""      let c := signed P st o o.key (S.pinsFor P.env st.host [o.id, g.id]) (.grant src.1 g.id [.transfer 1] none)
""",
"""      let c := signed P st o o.key (S.pinsFor P.env st.host [o.id, g.id, src.1]) (.grant src.1 g.id [.transfer 1] none)
""")
edit("Kernel/Sim/Gen.lean",
"""        let c := signed P st o o.key (S.pinsFor P.env st.host [o.id, g.id]) (.grant src.1 g.id [.mutate] none)
""",
"""        let c := signed P st o o.key (S.pinsFor P.env st.host [o.id, g.id, src.1]) (.grant src.1 g.id [.mutate] none)
""")
edit("Kernel/Sim/Gen.lean",
"""              let c := signed P st iss iss.key (S.pinsFor P.env st.host [iss.id, cg.id]) (.grant wl.1 cg.id [.credit 1] none)
""",
"""              let c := signed P st iss iss.key (S.pinsFor P.env st.host [iss.id, cg.id, wl.1]) (.grant wl.1 cg.id [.credit 1] none)
""")

# G2: Sim Gen.lean — ledgerAct k=1: pin the well, and probe a non-well asset
edit("Kernel/Sim/Gen.lean",
"""          let taken := st.accounts.any fun a => a.1 = id
          let what := if taken then "account-twice" else if o.id = m.id then "account" else "account-for-other"
          let c := signed P st m m.key (S.pinsFor P.env w [m.id]) (.account well.1 o.id)
          let (st, t) := submit P st c (if taken then .rejected "idTaken" else .ok) what
          match t with
          | some t =>
              if (createdIds t).headD P.zero = id then { st with accounts := st.accounts ++ [(id, o.id, well.1)] }
              else { st with failures := "account: born at an id that is not accountId owner asset" :: st.failures }
          | none => st
""",
"""          let taken := st.accounts.any fun a => a.1 = id
          let what := if taken then "account-twice" else if o.id = m.id then "account" else "account-for-other"
          let c := signed P st m m.key (S.pinsFor P.env w [m.id, well.1]) (.account well.1 o.id)
          let (st, t) := submit P st c (if taken then .rejected "idTaken" else .ok) what
          let st := match t with
          | some t =>
              if (createdIds t).headD P.zero = id then { st with accounts := st.accounts ++ [(id, o.id, well.1)] }
              else { st with failures := "account: born at an id that is not accountId owner asset" :: st.failures }
          | none => st
          -- an account of an asset that is not a well (a holder account): `assetNotWell`
          match st.accounts.find? fun a => a.1 ≠ a.2.2 with
          | none => st
          | some h =>
              let c := signed P st m m.key (S.pinsFor P.env st.host [m.id, h.1]) (.account h.1 m.id)
              (submit P st c (.refused "assetNotWell") "account-not-well").1
""")

# G3: Sim Gen.lean — arm 9: pin the target, and probe a root grant by a non-owner
edit("Kernel/Sim/Gen.lean",
"""          let c := signed P st owner owner.key (S.pinsFor P.env w [owner.id, ge.id]) (.grant obj.1 ge.id [.mutate] none)
          let (st, t) := submit P st c .ok "grant"
          match t with
          | some t => { st with grants := st.grants ++ [((createdIds t).headD P.zero, obj.1, ge.id, owner.id)] }
          | none => st
""",
"""          let c := signed P st owner owner.key (S.pinsFor P.env w [owner.id, ge.id, obj.1])
            (.grant obj.1 ge.id [.mutate] none)
          let (st, t) := submit P st c .ok "grant"
          let st := match t with
          | some t => { st with grants := st.grants ++ [((createdIds t).headD P.zero, obj.1, ge.id, owner.id)] }
          | none => st
          -- a root grant by another than the target's owner: `notOwner`
          match st.members.find? fun m => m.id ≠ owner.id with
          | none => st
          | some other =>
              let c := signed P st other other.key (S.pinsFor P.env w [other.id, ge.id, obj.1])
                (.grant obj.1 ge.id [.mutate] none)
              (submit P st c (.refused "notOwner") "grant-not-owner").1
""")

# H1: Rows — journey: a root grant by a non-owner is refused by name
edit("Protocol/Rows.lean",
"""    no "newcomer" ["write", "@shared", "2", "3"] "noGrant",
""",
"""    no "newcomer" ["write", "@shared", "2", "3"] "noGrant",
    no "newcomer" ["grant", "@shared", "@sponsor", "observe"] "notOwner",
""")

# H2: Rows — well: an account of an asset that is not a well is refused by name
edit("Protocol/Rows.lean",
"""    no "operator" ["account", "@w"] "idTaken",
    ok "sponsor" ["account", "@w"],
""",
"""    no "operator" ["account", "@w"] "idTaken",
    okBind "sponsor" ["account", "@w"] "sw",
    no "sponsor" ["account", "@sw"] "assetNotWell",
""")
