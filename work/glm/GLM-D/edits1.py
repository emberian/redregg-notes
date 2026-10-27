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

# A1: Call.lean — notWell docstring widened, assetNotWell constructor added after it
edit("Kernel/Receive/Call.lean",
"""  /-- a credit line out of an account that is not a well (its denomination is not its own id) -/
  | notWell (cell : D)
""",
"""  /-- a `.well` reference or a credit line naming an account that is not a well (its
  denomination is not its own id) -/
  | notWell (cell : D)
  /-- an account opened of an asset that is not a well (its denomination is not its own id): a
  denomination is a well's id, so an account names one -/
  | assetNotWell (asset : D)
""")

# A2: Call.lean — Refusal.name
edit("Kernel/Receive/Call.lean",
"""  | .notWell _ => "notWell"
""",
"""  | .notWell _ => "notWell"
  | .assetNotWell _ => "assetNotWell"
""")

# B: Submit.lean — refusalNames, in constructor order
edit("Kernel/Receive/Submit.lean",
"""   "duplicateEffect", "sameAccount", "zeroAmount", "assetMismatch", "overflow", "notWell",
""",
"""   "duplicateEffect", "sameAccount", "zeroAmount", "assetMismatch", "overflow", "notWell",
   "assetNotWell",
""")

# C1: Derive.lean — checkParent: a root grant is its owner's act
edit("Kernel/Receive/Derive.lean",
"""rights are never rooted here (`unrooted`): only genesis roots them. -/
def checkParent (X : Ctx D) (look : Pinned D) (actor : D) (target : D) (rights : List Right) :
    Option D → Except (Refusal D) (Option (D × Act))
  | none => do
      req (!(target = worldId X || rights.any isEnroll)) (.unrooted target)
      pure none
""",
"""rights are never rooted here (`unrooted`): only genesis roots them. A root grant on any other
target is its owner's act: the target is read (`missingCell` where it is not live), bears an
owner slot (`malformedCell`), and the actor IS that owner (`notOwner`) — a root grant whose
issuer is not the owner confers nothing, so it is refused at admission, never admitted useless. -/
def checkParent (X : Ctx D) (look : Pinned D) (actor : D) (target : D) (rights : List Right) :
    Option D → Except (Refusal D) (Option (D × Act))
  | none => do
      req (!(target = worldId X || rights.any isEnroll)) (.unrooted target)
      let cell ← match look target with
        | .error e => .error e
        | .ok none => .error (.missingCell target)
        | .ok (some cell) => .ok cell
      let owner ← slotDigest X target cell slotOwner
      req (owner = actor) (.notOwner target)
      pure none
""")

# C2: Derive.lean — dispatch reads the asset through the pinned view
edit("Kernel/Receive/Derive.lean",
"""  | .account asset owner => stepped wk (account X asset owner)
""",
"""  | .account asset owner => stepped wk (account X look asset owner)
""")

# D: Ledger.lean — account reads the asset well
edit("Kernel/Receive/Ledger.lean",
"""/-- `account asset owner`: the empty account of the asset's denomination owned by `owner`, at its
keyed id. Anyone may open anyone's (it is empty, floor 0, and only its owner can debit it); a
second open of the pair is `World.admit`'s `idTaken`. It does not read the well, so opening an
account never pins the hot cell. -/
def account (X : Ctx D) (asset owner : D) : Except (Refusal D) (Draft D) :=
  pure ⟨[(accountId X owner asset, accountCell X owner (X.env.bytes asset) 0)], [], [], []⟩
""",
"""/-- `account asset owner`: the empty account of the asset's denomination owned by `owner`, at its
keyed id. Anyone may open anyone's (it is empty, floor 0, and only its owner can debit it); a
second open of the pair is `World.admit`'s `idTaken`. The asset must be a live pinned well
(`assetNotWell` otherwise): a denomination is a well's id, so an account never opens of an asset
nobody issued — the price is that opening one now pins the well. -/
def account (X : Ctx D) (look : Pinned D) (asset owner : D) : Except (Refusal D) (Draft D) := do
  let (_, wv) ← readAccount look asset
  req (decide (wv.denom = X.env.bytes asset)) (.assetNotWell asset)
  pure ⟨[(accountId X owner asset, accountCell X owner (X.env.bytes asset) 0)], [], [], []⟩
""")
