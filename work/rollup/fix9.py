import re
p="Kernel/ObjectiveActivityReceiver.lean"
s=open(p).read()
a=s.index("<<<<<<< HEAD\n/-- A cell an activity intent writes")
b=s.index(">>>>>>> 5c79cbf6", s.index(">>>>>>> 5c79cbf6")+10)
b=s.index("\n",b)+1
new='''/-- A cell an activity intent writes is an activity cell or a seat cell (the seats
an ending activity held), each at its own protected coordinate; the Book; or a
cell the kernel retires: the registry's retired image at a protected coordinate
(an ended record or a settled slot). -/
def ActivityOrBook (deployment : Deployment) (write : DataWrite) : Prop :=
  write.cellId = ⟨deployment.resourceBookId⟩ ∨
    (∃ payload, ObjectiveActivity.payloadOf write.canonicalPostBytes = some payload ∧
      write.cellId.value = ObjectiveActivityCell.coordinate deployment.domain payload.role payload.key) ∨
    (∃ payload, SeatStore.payloadOf write.canonicalPostBytes = some payload ∧
      write.cellId.value = SeatCell.coordinate deployment.domain payload.role payload.key) ∨
    (write.canonicalPostBytes = ObjectiveActivity.retiredImage ∧ ObjectiveActivityCell.reservedBase ≤ write.cellId.value)

def activityCellAt (deployment : Deployment) (write : DataWrite) : Bool :=
  match ObjectiveActivity.payloadOf write.canonicalPostBytes with
  | some payload => decide (write.cellId.value = ObjectiveActivityCell.coordinate deployment.domain payload.role payload.key)
  | none => false

def seatCellAt (deployment : Deployment) (write : DataWrite) : Bool :=
  match SeatStore.payloadOf write.canonicalPostBytes with
  | some payload => decide (write.cellId.value = SeatCell.coordinate deployment.domain payload.role payload.key)
  | none => false

def retiredAt (write : DataWrite) : Bool :=
  decide (write.canonicalPostBytes = ObjectiveActivity.retiredImage ∧
    ObjectiveActivityCell.reservedBase ≤ write.cellId.value)

theorem activityOrBook_iff (deployment : Deployment) (write : DataWrite) :
    ActivityOrBook deployment write ↔
      (write.cellId = ⟨deployment.resourceBookId⟩ ∨ activityCellAt deployment write = true ∨
        seatCellAt deployment write = true ∨ retiredAt write = true) := by
  unfold ActivityOrBook activityCellAt seatCellAt retiredAt
  constructor
  · rintro (h | ⟨payload, hp, hat⟩ | ⟨payload, hp, hat⟩ | h)
    · exact Or.inl h
    · exact Or.inr (Or.inl (by rw [hp]; simpa using hat))
    · exact Or.inr (Or.inr (Or.inl (by rw [hp]; simpa using hat)))
    · exact Or.inr (Or.inr (Or.inr (by simpa using h)))
  · rintro (h | h | h | h)
    · exact Or.inl h
    · split at h
      · rename_i payload hp; exact Or.inr (Or.inl ⟨payload, hp, by simpa using h⟩)
      · cases h
    · split at h
      · rename_i payload hp; exact Or.inr (Or.inr (Or.inl ⟨payload, hp, by simpa using h⟩))
      · cases h
    · exact Or.inr (Or.inr (Or.inr (by simpa using h)))

instance (deployment : Deployment) (write : DataWrite) : Decidable (ActivityOrBook deployment write) :=
  decidable_of_iff _ (activityOrBook_iff deployment write).symm
'''
s=s[:a]+new+s[b:]
assert "<<<<<<<" not in s
open(p,"w").write(s)
