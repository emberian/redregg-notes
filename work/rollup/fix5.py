p="Kernel/SeatStore.lean"
s=open(p).read()
s=s.replace("  | cellUndecodable (cell : Nat)\n","  | cellUndecodable (cell : Nat)\n  /-- A post of an ending turn would sit on, or be, a kernel-activity cell. -/\n  | activityCellInSeatSpace (cell : Nat)\n",1)
old="""  posts : List Post
  postsExact : posts = statePosts domain snapshot loaded none next
  guards : List ReadGuard
  guardsExact : guards = (loadedCells domain loaded).map (guardAt snapshot)
"""
new="""  posts : List Post
  postsExact : posts = statePosts domain snapshot loaded none next
  /-- No post of the closing sits on a cell holding a kernel-activity cell or is one:
  the check is the kernel\\'s (the closing refuses otherwise), so the checkpoint
  invariant needs no coordinate-disjointness assumption between seat and activity
  cells. -/
  inert : ∀ post ∈ posts, ObjectiveActivity.payloadOf (snapshot.canonicalBytes post.cell) = none ∧
    ObjectiveActivity.payloadOf post.bytes = none
  guards : List ReadGuard
  guardsExact : guards = (loadedCells domain loaded).map (guardAt snapshot)
"""
new=new.replace("\\\\'","'")
assert old in s
s=s.replace(old,new,1)
old2="""  | .ok (next, batch) => pure ⟨loaded, next, batch, ended, _, rfl, _, rfl⟩
"""
new2="""  | .ok (next, batch) =>
    if inert : (statePosts domain snapshot loaded none next).all (fun post =>
        (ObjectiveActivity.payloadOf (snapshot.canonicalBytes post.cell)).isNone &&
          (ObjectiveActivity.payloadOf post.bytes).isNone) = true then
      pure ⟨loaded, next, batch, ended, _, rfl, fun post member => by
        have both := List.all_eq_true.mp inert post member
        simp only [Bool.and_eq_true, Option.isNone_iff_eq_none] at both
        exact both, _, rfl⟩
    else throw (.activityCellInSeatSpace (accounts.headD 0))
"""
assert old2 in s
s=s.replace(old2,new2,1)
open(p,"w").write(s)
