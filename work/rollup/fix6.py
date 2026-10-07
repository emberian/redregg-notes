p="Kernel/ObjectiveCheckpointInvariant.lean"
s=open(p).read()
s=s.replace("import Kernel.ObjectiveActivityGate\n","import Kernel.ObjectiveActivityGate\nimport Kernel.ActivitySeatEnd\n",1)
# Step
old="""  | turn {snapshot : Snapshot rootBytes} {height : Nat} (turn : AdmittedTurn config snapshot height)
      (sealing : Seal) (schedule : DurableCommitProtocol.Schedule) :
      Step config snapshot ((execute schedule snapshot (turn.intent sealing)).storeAfter snapshot)
"""
new="""  | turn {snapshot : Snapshot rootBytes} {height : Nat} (turn : AdmittedTurn config snapshot height)
      (sealing : Seal) (posts : List Post) (extra : List ReadGuard)
      (final : ActivitySeatEnd.finalize config snapshot height turn = .ok (posts, extra))
      (schedule : DurableCommitProtocol.Schedule) :
      Step config snapshot ((execute schedule snapshot (turn.finalIntent sealing posts extra)).storeAfter snapshot)
"""
assert old in s
s=s.replace(old,new,1)
old="""  | turn turn sealing schedule =>
    exact execute_preserves typed (AdmittedTurn.intent_writes sealing turn) (AdmittedTurn.safe typed turn) schedule
"""
new="""  | turn turn sealing posts extra final schedule =>
    exact execute_preserves typed (finalIntent_writes sealing final) (finalize_safe typed turn final) schedule
"""
assert old in s
s=s.replace(old,new,1)
anchor="/-! ## Reachable worlds -/"
lem='''/-! ## An ending turn's final posts are safe

A turn that ends an activity holding seats commits the joint posts: its own with
the Book post replaced by the joint batch's, then the seat cells the closing
changed (`ActivitySeatEnd.Joined.rewrite`). The replaced Book post sits on the
cell its original sat on and holds the Book; a closing post sits on a cell that
holds no kernel-activity cell and is none (`HeldEnd.inert`, the closing's own
check). -/

/-- The writes of an admitted turn's final intent are exactly its final posts. -/
theorem finalIntent_writes {rootBytes : Bytes → Digest} {config : Config} {snapshot : Snapshot rootBytes}
    {height : Nat} (sealing : Seal) {turn : AdmittedTurn config snapshot height} {posts : List Post}
    {extra : List ReadGuard} (final : ActivitySeatEnd.finalize config snapshot height turn = .ok (posts, extra)) :
    (turn.finalIntent sealing posts extra).writes = posts.map (Post.write rootBytes) := by
  cases turn with
  | birth _ _ => rfl
  | deliver _ _ => rfl
  | abandon _ _ => rfl
  | publish _ _ => simp [ActivitySeatEnd.finalize, ActivitySeatEnd.AdmittedTurn.ending] at final; rw [← final.1]; rfl
  | create _ _ => simp [ActivitySeatEnd.finalize, ActivitySeatEnd.AdmittedTurn.ending] at final; rw [← final.1]; rfl
  | resolve _ _ => simp [ActivitySeatEnd.finalize, ActivitySeatEnd.AdmittedTurn.ending] at final; rw [← final.1]; rfl
  | topUp _ _ => simp [ActivitySeatEnd.finalize, ActivitySeatEnd.AdmittedTurn.ending] at final; rw [← final.1]; rfl
  | writeState _ _ => simp [ActivitySeatEnd.finalize, ActivitySeatEnd.AdmittedTurn.ending] at final; rw [← final.1]; rfl
  | exhaust _ _ => simp [ActivitySeatEnd.finalize, ActivitySeatEnd.AdmittedTurn.ending] at final; rw [← final.1]; rfl

/-- **An ending turn's final posts are safe.** -/
theorem finalize_safe {rootBytes : Bytes → Digest} {config : Config} {snapshot : Snapshot rootBytes}
    {height : Nat} (typed : RecordCellsTyped config snapshot) (turn : AdmittedTurn config snapshot height)
    {posts : List Post} {extra : List ReadGuard}
    (final : ActivitySeatEnd.finalize config snapshot height turn = .ok (posts, extra)) :
    ∀ post ∈ posts, PostSafe config snapshot post := by
  have safe := AdmittedTurn.safe typed turn
  unfold ActivitySeatEnd.finalize at final
  cases ending : ActivitySeatEnd.AdmittedTurn.ending turn with
  | none =>
    rw [ending] at final
    simp only [Except.ok.injEq, Prod.mk.injEq] at final
    rw [← final.1]; exact safe
  | some found =>
    obtain ⟨record, pre, posted⟩ := found
    rw [ending] at final
    cases joined : ActivitySeatEnd.join config snapshot height record posted with
    | error reason => simp [joined] at final
    | ok optional =>
      cases optional with
      | none =>
        simp only [joined, Except.ok.injEq, Prod.mk.injEq] at final
        rw [← final.1]; exact safe
      | some made =>
        simp only [joined, Except.ok.injEq, Prod.mk.injEq] at final
        rw [← final.1]
        intro post member
        unfold ActivitySeatEnd.Joined.rewrite at member
        rcases List.mem_append.mp member with mapped | closing
        · obtain ⟨original, inOriginal, replaced⟩ := List.mem_map.mp mapped
          by_cases isBook : original.cell = config.bookCell
          · rw [if_pos isBook] at replaced
            subst replaced
            have base := safe original inOriginal
            refine ⟨?_, fun found read _ => ?_⟩
            · simpa [ActivitySeatEnd.Joined.bookPost, postAt, isBook] using base.1
            · simp [recordIn, ActivitySeatEnd.Joined.bookPost, postAt, bodyOf, payloadOf_book] at read
          · rw [if_neg isBook] at replaced
            subst replaced
            exact safe original inOriginal
        · have inert := made.held.inert post closing
          exact postSafe_inert (bodyOf_of_payload_none inert.1)
            (by simp [recordIn, bodyOf_of_payload_none inert.2])

'''
assert anchor in s
s=s.replace(anchor,lem+anchor,1)
s=s.replace("#assert_axioms AdmittedTurn.safe\n","#assert_axioms AdmittedTurn.safe\n#assert_axioms finalIntent_writes\n#assert_axioms finalize_safe\n",1)
open(p,"w").write(s)
p="Kernel/ObjectiveActivityGateRoute.lean"
s=open(p).read()
old="""        (sealing : ObjectiveActivityWire.Seal), derived.intent = turn.intent sealing) ∨"""
new="""        (sealing : ObjectiveActivityWire.Seal) (posts : List DurableDataIntent.Post)
        (extra : List DurableDataIntent.ReadGuard),
        ActivitySeatEnd.finalize kernel opened.durable.snapshot height turn = .ok (posts, extra) ∧
          derived.intent = turn.finalIntent sealing posts extra) ∨"""
assert old in s
s=s.replace(old,new,1)
old="""    exact ⟨_, _, accepted.prepared.decided,
      ObjectiveActivityReceiver.admissionSeal accepted.prepared ingress, exact⟩"""
new="""    exact ⟨_, _, accepted.prepared.decided,
      ObjectiveActivityReceiver.admissionSeal accepted.prepared ingress, accepted.prepared.final.1,
      accepted.prepared.final.2, accepted.prepared.finalExact, exact⟩"""
assert old in s
s=s.replace(old,new,1)
open(p,"w").write(s)
