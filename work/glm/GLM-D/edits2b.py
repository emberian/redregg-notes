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

# InvokeTree.lean — checkParent_at's none arm now reads the target first
edit("Kernel/Proofs/InvokeTree.lean",
"""  | none =>
      simp only [checkParent, except_bind_ok, pure, Except.pure, Except.ok.injEq] at h
      obtain ⟨⟨⟩, -, rfl⟩ := h
      simp
""",
"""  | none =>
      simp only [checkParent, except_bind_ok, pure, Except.pure, Except.ok.injEq] at h
      obtain ⟨⟨⟩, -, -, ⟨⟩, rfl⟩ := h
      simp
""")

# InvokeTree.lean — the account arm of the effects theorem, over the reading receiver
edit("Kernel/Proofs/InvokeTree.lean",
"""  | account asset owner =>
      have hd := stepped_draft h
      simp only [account, pure, Except.pure, Except.ok.injEq] at hd
      intro e he; rw [← hd] at he; simp at he
""",
"""  | account asset owner =>
      have hd := stepped_draft h
      unfold account at hd
      simp only [except_bind_ok, pure, Except.pure, Except.ok.injEq] at hd
      intro e he; rw [← hd] at he; simp at he
""")

# Rooted.lean — the account arm, over the reading receiver
edit("Kernel/Proofs/Rooted.lean",
"""    | account asset owner =>
        have hd := stepped_draft h
        simp only [account, pure, Except.pure, Except.ok.injEq] at hd
        rw [← hd]
""",
"""    | account asset owner =>
        have hd := stepped_draft h
        unfold account at hd
        simp only [except_bind_ok, pure, Except.pure, Except.ok.injEq] at hd
        rw [← hd]
""")
