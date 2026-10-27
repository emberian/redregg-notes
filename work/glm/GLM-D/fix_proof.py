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

edit("Kernel/Proofs/Authority.lean",
"""  match hl : look target with
  | .error e => simp only [checkParent, hl] at hp; exact Except.noConfusion hp
  | .ok none => simp only [checkParent, hl] at hp; exact Except.noConfusion hp
  | .ok (some cell) =>
      simp only [checkParent, hl, except_bind_ok, pure, Except.pure, Except.ok.injEq] at hp
      obtain ⟨⟩ := hp
""",
"""  match hl : look target with
  | .error e =>
      simp only [checkParent, hl] at hp
      have hf : Except.error e = Except.ok _ := hp
      exact Except.noConfusion hf
  | .ok none =>
      simp only [checkParent, hl] at hp
      have hf : Except.error (Refusal.missingCell target) = Except.ok _ := hp
      exact Except.noConfusion hf
  | .ok (some cell) =>
      simp only [checkParent, hl, except_bind_ok, pure, Except.pure, Except.ok.injEq] at hp
      obtain ⟨⟨⟩, -, -, hcell, -, hown, ⟨⟩, hreq, -⟩ := hp
      rw [req_ok, decide_eq_true_eq] at hreq
      subst hcell
      exact ⟨cell, rfl, by rw [hown, hreq]⟩
""")
