p="Kernel/ActivitySeatEnd.lean"
s=open(p).read()
add = '''
/-! ## An ending turn's final posts

The activity kernel's admitted turn (`ObjectiveActivity.AdmittedTurn`) and the
turn the receiver commits differ only when the turn ENDS an activity that holds
seats: then the committed posts are the joint ones (`Joined.rewrite`) and the
intent carries the seat cells' guards as well. These are stated here, on the
kernel's turn, so the checkpoint invariant and the receiver share one
definition. -/

open Minidregg.Kernel.ObjectiveActivity (AdmittedTurn)

/-- The activity a turn ENDS, with its loaded Book and its postings: a birth or a
delivery whose record is no longer awaiting (done or faulted), and every
abandonment. Other turns end nothing. -/
def AdmittedTurn.ending {rootBytes : Bytes → Digest} {config : Config} {snapshot : Snapshot rootBytes}
    {height : Nat} :
    AdmittedTurn config snapshot height → Option (Nat × Σ pre : BookCell, Postings pre)
  | .birth _ born => match born.record.phase with
    | .awaiting _ => none
    | _ => some (born.cell.value, ⟨born.book, born.posted⟩)
  | .deliver request delivery => match delivery.next.phase with
    | .awaiting _ => none
    | _ => some (request.record.value, ⟨delivery.book, delivery.posted⟩)
  | .abandon request abandoned => some (request.record.value, ⟨abandoned.book, abandoned.posted⟩)
  | _ => none

/-- The turn\\'s final posts and extra guards: the kernel\\'s own, or, when the turn
ends an activity that holds seats, the joint turn (`Joined.rewrite`). -/
def finalize {rootBytes : Bytes → Digest} (config : Config) (snapshot : Snapshot rootBytes)
    (height : Nat) (turn : AdmittedTurn config snapshot height) :
    Except SeatStore.Refusal (List Post × List ReadGuard) :=
  match turn.ending with
  | none => .ok (turn.posts, [])
  | some (record, ⟨_, posted⟩) =>
    match join config snapshot height record posted with
    | .error reason => .error reason
    | .ok none => .ok (turn.posts, [])
    | .ok (some joined) => .ok (joined.rewrite turn.posts, joined.held.guards)

/-- The intent of an admitted turn over final posts and extra guards (an ending
turn\\'s own transaction, guards and claims). -/
def AdmittedTurn.finalIntent {rootBytes : Bytes → Digest} {config : Config} {snapshot : Snapshot rootBytes}
    {height : Nat} (sealing : Seal) (posts : List Post) (extra : List ReadGuard) :
    AdmittedTurn config snapshot height → DataIntent rootBytes
  | .birth request born =>
      ObjectiveActivity.intentOf rootBytes (ObjectiveActivity.birthTransaction request) posts
        (born.guards ++ extra) [] sealing
  | .deliver _ delivery =>
      ObjectiveActivity.intentOf rootBytes (ObjectiveActivity.deliveryTransaction delivery.await.id) posts
        (delivery.guards ++ extra) delivery.claims sealing
  | .abandon _ abandoned =>
      ObjectiveActivity.intentOf rootBytes (ObjectiveActivity.abandonTransaction abandoned.await.id) posts extra
        abandoned.claims sealing
  | turn => turn.intent sealing

'''
add=add.replace("\\'","'")
anchor="#assert_axioms joint_admission"
assert anchor in s
s=s.replace(anchor, add+anchor,1)
open(p,"w").write(s)
p="Kernel/ObjectiveActivityReceiver.lean"
s=open(p).read()
s=s.replace("finalExact : finalize config","finalExact : ActivitySeatEnd.finalize config")
s=s.replace("match finalExact : finalize config","match finalExact : ActivitySeatEnd.finalize config")
s=s.replace("unfold finalize at final","unfold ActivitySeatEnd.finalize at final")
s=s.replace("match finalize config durable.snapshot","match ActivitySeatEnd.finalize config durable.snapshot")
s=s.replace("accepted.prepared.decided.ending =","ActivitySeatEnd.AdmittedTurn.ending accepted.prepared.decided =")
open(p,"w").write(s)
