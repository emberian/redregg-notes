p="Kernel/ObjectiveActivityReceiver.lean"
s=open(p).read()
a=s.index("/-- A cell an activity intent writes is an activity cell or the Book. -/")
b=s.index("def PhysicalShape")
new='''/-- A cell an activity intent writes is an activity cell at its own coordinate, the
Book, or a cell the kernel retires: the registry's retired image at a protected
coordinate (an ended record or a settled slot). -/
def ActivityOrBook (deployment : Deployment) (write : DataWrite) : Prop :=
  write.cellId = ⟨deployment.resourceBookId⟩ ∨
    (∃ payload, ObjectiveActivity.payloadOf write.canonicalPostBytes = some payload ∧
      write.cellId.value = ObjectiveActivityCell.coordinate deployment.domain payload.role payload.key) ∨
    (write.canonicalPostBytes = ObjectiveActivity.retiredImage ∧ ObjectiveActivityGate.Protected write.cellId)

instance (deployment : Deployment) (write : DataWrite) : Decidable (ActivityOrBook deployment write) :=
  if book : write.cellId = ⟨deployment.resourceBookId⟩ then isTrue (Or.inl book)
  else if retired : write.canonicalPostBytes = ObjectiveActivity.retiredImage ∧
      ObjectiveActivityGate.Protected write.cellId then isTrue (Or.inr (Or.inr retired))
  else match found : ObjectiveActivity.payloadOf write.canonicalPostBytes with
    | none => isFalse (by
        rintro (h | ⟨payload, hp, _⟩ | h)
        · exact book h
        · rw [found] at hp; cases hp
        · exact retired h)
    | some payload =>
      if at_ : write.cellId.value = ObjectiveActivityCell.coordinate deployment.domain payload.role payload.key then
        isTrue (Or.inr (Or.inl ⟨payload, found, at_⟩))
      else isFalse (by
        rintro (h | ⟨other, hp, hat⟩ | h)
        · exact book h
        · rw [found] at hp; cases hp; exact at_ hat
        · exact retired h)

'''
s=s[:a]+new+s[b:]
s=s.replace("""/-- **Protected coordinates.** Every cell an accepted activity turn writes is
an activity cell at its own coordinate, or the deployment's Book. -/""","""/-- **Protected coordinates.** Every cell an accepted activity turn writes is
an activity cell at its own coordinate, the deployment's Book, or a retirement
(the registry's retired image) at a protected coordinate. -/""")
open(p,"w").write(s)
