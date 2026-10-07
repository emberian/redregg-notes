# LAWS-RECEIVER brief: the Receiver judges every written cell's law (QUEST-LAWS-RECEIVER, D-2)

Author: SCHOLAR-LAWS (consultant to the implementing successor; resume me by SendMessage for questions).
Sources: my review `work/REVIEW-SCHOLAR-LAWS-20261005.md` §4 D-2; ROOT decision 10-05 (Receiver takes the
deployment compiler profile as an environment parameter; resolves laws through
`PhysicalLawResolution.config`; `CanonicalCellRegistry` holds the only exemption list with a writer
theorem; `SubjectKeyRotation` first). Code facts below were READ at main `36fca3ac` (my clone) unless
marked; main has since moved (batches c1–c3: activity-native added a protected activity kind at ids
≥ 2^256, object-record added `Kernel/ObjectRecord`, seats/schema-v2/elaborator landed). **Re-read every
signature below at current main before editing; treat my line numbers as hints.**

## 1. Why (one paragraph)

`Kernel.Receiving.Family` lets each family decide whether a law judges its writes: `postLaw :
Prepared → Bool` ("family checks on the post images beyond the standard shape", `Kernel/Receiving.lean`
~141) and `shape = distinct cells ∧ current roots ∧ postLaw` (~169). Nothing makes every written cell's
committed law judge its step. Robust safety (a check on every write, whoever proposed it) is
therefore a per-family discipline across ~33 families, and `receive_committed` (`Theory/Receiving`
~461) says nothing about laws. LAWS-PIN (`6c5fb101`) made the package pin a law; that law is only as
strong as the guarantee that every route judges it.

## 2. Census: who judges laws where (read at 36fca3ac; grep of law machinery per receiver file)

| family | law machinery referenced | what that means |
|---|---|---|
| DeclaredResourceController (op 2; Group B rides it: ApplicationLifecycleBegin*, Claim*, Completion*, dispatch, session enrollment, failed-start recovery, NativePlanHeight) | `authorizeLeg` → `policyConfigFromStep` → `config.resolve?` → `law.admit` (+ `inputsInRange`, `castInjOn`) per target leg and the authority leg | judges every target's committed law on the projected step |
| ClockTick, Certify, PayAssignment, PayBook, PayClaim, PayEnrol (v1), PayEnrolV2, PayObservation, JobMoney, PurseRefill, RealmWell | `PhysicalLawResolution.config` + `ComposedPolicyAdmission.admit` inside `prepare` | judge the laws of the cells they choose, in their own code |
| SubjectKeyRotation (on `Family`), SubjectKeyCommitmentAdoption, ParticipantKeyEnrollment, ParticipantFactoryProvisioning, FleetTurn, CapabilityDelegation, CapabilityRevocation, CapabilityRenounce | `PhysicalPostLaw` only | physical well-formedness of the post image; **no committed `Pred` law** |
| PolicyInstall | `PhysicalLawResolution.addresses/loadGuards` + `PhysicalPostLaw` | validates the candidate law graph; the installed law is deliberately not evaluated against its own install |
| ResourceBirth, GrainResourceBirth, ApplicationShareIssue, ApplicationShareIssueGrain, FnSelectiveRelease, FnSelectiveReleaseSource | none directly (some use DRC types/markers) | births are judged by export laws of the factory/room (see trap T3); Fn and share issue: verify per family |

Successor's first task: turn this table into a measured one at current main (for each family: which
cells it writes, by kind; whether any of them can carry a committed law; where, if anywhere, that law
is judged). That table is the registry's input.

## 3. The design (adopted by ROOT)

### 3.1 Registry (in `Compiler/CanonicalCellRegistry.lean`)

`CanonicalCellRegistry.Kind` at 36fca3ac: `content | eventHistory | authority | declaredObject |
resourceBook | accountMetadata | declaredProgram | policySource | pay | stream | streamEntry |
nockProgram | clock | system | worldKind | worldInstance` (plus, at current main, the activity kind).

```lean
/-- How a cell kind is judged on write. -/
inductive LawClass where
  | lawBearing                       -- its committed law (PhysicalLawResolution) judges every write
  | kernelOnly (writers : List FamilyId)  -- no user law; only the named kernel families may write it
  deriving DecidableEq, Repr

def Kind.lawClass : Kind → LawClass       -- total, one row per kind, reviewed DATA
```

`FamilyId` is a closed enumeration of receiving families (one constructor per `Family` value; the
receiver-collapse `HostOp` table is its natural source). Every kind must be classified; no default arm.
Expected (to be confirmed by the census): `declaredObject`, `content`, `stream`/`streamEntry`,
`worldInstance`, `worldKind`, `resourceBook`/`accountMetadata`, `declaredProgram`, `nockProgram` are
`lawBearing`; `authority`, `clock`, `system`, `pay`, `policySource`, `eventHistory` and the activity
kind are `kernelOnly` with their writer families (`clock` → `[clockTick]`, `system` → `[certify]`,
authority → the key/capability families, …). If a kind is both (some writers kernel, some user),
that is a design bug to surface, not a third class.

### 3.2 `Kernel.Receiving.Family` changes

- New field, replacing the law role of `postLaw`:
  ```lean
  /-- The projected step of one write, for its cell's law: the target resource id the law is keyed
  by, and the old/new predicate states. Families project; the Receiver judges. -/
  lawStep : {env : Env} → {durable : Durable} → {command : Command} →
    (prepared : Prepared env durable command) → (write : DataWrite) → write ∈ writes prepared →
    Option LawStep
  structure LawStep where target : Nat; step : PolicyStepContext   -- PolicyStepContext has a
                                                                     -- private mk: build it with an
                                                                     -- existing constructor
  ```
  `none` means "this write is to a kernel-only cell" and is accepted only if the registry says so for
  this family (below).
- New field `id : FamilyId`.
- Keep `postLaw`, renamed `physicalPostLaw` (physical well-formedness only), so no family can hide a
  law check in it.
- The Receiver environment gains the deployment's `PolicyCompilerProfile F` and the snapshot/directory
  it needs for `PhysicalLawResolution.config`: `config profile snapshot directory base step target
  additional : ComposedPolicyAdmission.Config F` (read at `Compiler/PhysicalLawResolution.lean` ~62).
- `shape` becomes: distinct cells ∧ current roots ∧ `physicalPostLaw` ∧ `lawful`, where
  ```lean
  def lawful (prepared) : Bool :=
    (F.writes prepared).attach.all fun ⟨w, mem⟩ =>
      match kindOf w.cellId, F.lawStep prepared w mem with
      | k, some s => k.lawClass = .lawBearing &&
          match (PhysicalLawResolution.config profile … s.step s.target …).resolve? with
          | some law => inputsInRange … && castInjOn … && Pred.eval law.predicate s.step.oldState s.step.newState
          | none => false               -- a law-bearing cell whose law cannot be resolved REFUSES
      | k, none => decide (k.lawClass = .kernelOnly ws ∧ F.id ∈ ws)
  ```
  (The DRC already does exactly the `resolve?` / range / cast / eval sequence in `authorizeLeg`
  ~586–606; reuse its pieces, do not write a second evaluator. Note `law.admit` additionally binds the
  request and capability evidence: that is AUTHORIZATION and stays in the family; the Receiver's
  `lawful` is the law-judges-the-step half, and `PreparedLaw.verifies_iff_eval` (`ComposedPolicyAdmission`
  ~203) is the bridge if you want the compiled verdict instead of `Pred.eval`.)
- Refusal: a new `Refusal` arm in `Theory.Receiving` (`lawDenied (cell) (leaf : LawLeaf)` via
  `LawLeaf.of`, or `lawUnavailable cell`, `kernelOnlyForeignWriter cell family`), so the explanation
  names the clause exactly as the DRC's `lawLeaf` does.

### 3.3 Theorems (pin each with `#assert_axioms`)

1. `shape_lawful` (Kernel/Receiving): `shape prepared = true →` for every `write ∈ F.writes prepared`,
   either (a) `kindOf write.cellId` is `lawBearing`, `F.lawStep prepared write _ = some s`, the
   resolved law `law` exists and `Pred.eval law.predicate s.step.oldState s.step.newState = true`; or
   (b) it is `kernelOnly ws` with `F.id ∈ ws`.
2. `receive_committed_lawful`: the `committed` outcome of `receiveLoaded`/`receive` implies 1 for the
   admission's prepared value. Premises: exactly `receive_committed`'s (`R.receive verify append env
   state bytes = pure (.committed ingress admission witness)`), at `Id` with the pure verifier; it
   follows from `receive_committed` + `admit_ok_iff` (shape holds of `admission.accepted.prepared`) +
   `shape_lawful`. State it over `Family`, once.
3. `kernelOnly_writers_sound`: for every family `F` and every committed admission of `F`, every
   written cell of a `kernelOnly ws` kind has `F.id ∈ ws`. (This is the "only the families it names may
   write a kernel-only cell" theorem; it is a corollary of 1(b) but state it separately: it is what the
   registry review cites.)
4. Non-vacuity (premise inhabitants, not `#guard`): a fixture family over a two-cell journal whose
   committed admission exists (lawful write), and one whose `receive` returns the law refusal.

### 3.4 Migration order

1. Registry + `Family` fields + `lawful` + theorems, with `SubjectKeyRotation` migrated (it writes
   only the authority cell: `lawStep = none`, `authority` is `kernelOnly [subjectKeyRotation, …]`).
   Intents must stay byte-identical (control: compare the rotation intent bytes before/after).
2. Every later family that moves onto `Family` (receiver-collapse steps 1–8) supplies `lawStep`; the
   families that today judge laws in `prepare` (pay/clock/certify/…; DRC at step 3) delete their
   in-`prepare` law evaluation once `lawStep` carries the same step: one judge, not two.

## 4. Acceptance checks

- **The bypass tooth (required).** A fixture family `Bypass` that writes a `lawBearing` cell
  (e.g. a `declaredObject` whose committed law is `Pred.objectivePin [a]` from LAWS-PIN, or a
  `monotone` field) and whose `prepare` never judges any law. With the Receiver check, `receive`
  returns the law refusal naming the clause (`LawLeaf ⟨[0], …⟩`); with `lawful` removed from `shape`,
  the same ingress commits. Assert the mutation happened (the commit) before reading the verdict.
- `Bypass` with `lawStep = none` on a `lawBearing` cell is refused (`lawUnavailable`/registry
  mismatch), not admitted.
- A family not named in a `kernelOnly` row writing that kind (e.g. a fixture writing `clock`) is
  refused with `kernelOnlyForeignWriter`.
- `SubjectKeyRotation`: existing rotation journeys (JROTL) unchanged; rotation intent bytes identical.
- Gates: `lake build Minidregg +Host.Main:leanArts ObjectiveProofs`; host-closure (re-pin if
  Receiving's closure grows); import-boundary; proof-hygiene; build-surfaces (regenerate);
  objective-proofs unchanged; tracked-clean. Filtered Rust tests only if a Rust caller changes.

## 5. Traps

- **T1. Authorization is not law.** `ComposedPolicyAdmission.admit`/`Config.verifies` bind the
  request (policyId, revision, semantics, domain) and capability evidence. Do not move that into the
  Receiver; the Receiver judges `Pred.eval` of the resolved law on the step. Do not let a family
  satisfy `lawful` by passing a request that happens to verify.
- **T2. The step must be the real one.** `PolicyStepContext` has a private constructor
  (`Compiler/CanonicalPolicyAdmission` ~105); `old/newState` come from the family's projection of the
  real pre and post stores. A family that projects a different post than it writes defeats the check:
  `lawStep` must be stated against the same `write` (`exactPost`/`canonicalPostBytes` decode to the
  projected post). Make that a field obligation (`lawStep_post : … decode w.canonicalPostBytes = post`),
  or derive both from the typed patch the collapse design §3 plans (`writes := patch.map toWrite`).
- **T3. Births.** A newborn cell has no committed law at its pre-state; `LawComposition` says the
  newborn's law "is installed, validated as a graph, and deliberately not evaluated against its own
  birth", and births are judged by export laws of the factory/room. The registry/`lawful` must handle
  `expectedPre = empty root` as "judge the parent's export law", not "resolve the newborn's law"
  (which fails → spurious refusal) and not "skip" (which is the bypass).
- **T4. Law installation.** `PolicyInstall` writes `policySource` cells and changes what a target's law
  IS; the installed law is not judged against its own install. Classify `policySource` as
  `kernelOnly [policyInstall]` and keep the "old law judges the candidate" rule PolicyInstall already
  has; do not double-judge.
- **T5. One snapshot.** Resolve every law at the same snapshot the family prepared against
  (`LawComposition`: "all guards same snapshot"); the law's source cells become read guards (the
  `PhysicalLawResolution.readGuards` addresses must join `observed`), or a concurrent law change
  races the admission.
- **T6. Field parameter.** `Config F` needs `[Field F] [DecidableEq F]`; the Receiver gains `F` and
  the profile in `Env`. Do not pick a field in `Kernel/Receiving`; take it from the deployment.
- **T7. Double judging during migration.** While a family still judges laws in `prepare`, the
  Receiver judges again; that is fine for soundness but name it, and delete the family copy when it
  migrates (one judge).
- **T8. The pin slot.** LAWS-PIN projects `objective/artifact` first in DRC states only
  (`projectCommonSlots`). A family's `lawStep` that builds its own projection must also lead with it
  (`objectiveSlots command`, `-1` for non-Objective ingress), or `objectivePin` laws silently refuse
  every non-DRC family's writes. Better: one shared projection prefix used by every `lawStep`.
- **T9. Builds.** Burst boxes: take a slot (`flock -n /srv/build-slot-1 … || flock /srv/build-slot-2 …`);
  `SWARM_MEM_MAX=16G` OOM-killed a full umbrella on burst-gate for me (lake has no `-j`); 32G with a
  slot held worked. Run long builds inside `tmux` (an ssh-held nohup was killed with exit 143).
