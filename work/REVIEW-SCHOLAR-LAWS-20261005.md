# REVIEW-SCHOLAR-LAWS (2026-10-05)

Reviewer: SCHOLAR-LAWS (my report: `work/SCHOLAR-LAWS-CONTRACTS-20261004.md`, cited LAWS). Domain: design
§E, seats, Daml authority, necessity/protection, history slots, protocol objects, publish-time
certificates, OPEN question 2. Code read at `emberian/minidregg` main `36fca3ac` (fresh blobless clone,
read-only). Tags: **read** = I read the code at the path; **inferred** = my conclusion.

## 1. Verdict

The design's §E is the right shape, and the kernel already holds more of it than §E says. But the
first native Objective path judges laws in a state that does not know which code ran. The receiver
collapse makes law judgement a per-family option rather than part of the single Receiver. And the
activity kernel writes object state with no law at all. Until those three are fixed, "code proposes,
law disposes" holds for ordinary resource commands, not for objects.

## 2. What the design and the code got right

- **Laws judge the exact writes, before execution, and acceptance binds both** (read:
  `Kernel/DeclaredResourceController.lean` `admitObjective` 1655–1684). `admitAuthority` runs every
  target leg's committed law (`verifyAndAuthorizeLeg`, `lawLeaf`, 1087, 615) on the signed command's
  writes. Only then does `ObjectiveBendNativeAdmission.admit` re-execute the method and require its Plan
  to equal those writes (`Output.exact` → `BendWorldPlan.matchesCommand`). Finally `AcceptedInvocation`
  requires `execution.isSome` for the Objective family. So a refused law costs no execution, which is
  the design's "method guard" property. This is the Scilla/ConCert/EUTXO split (LAWS C4, C5, C11).
- **No solver on the admission path.** Admission evaluates `Pred.eval` on concrete projected states.
  The range and cast checks (`inputsInRange`, `castInjOn`) refuse rather than reinterpret (read, 600–606).
- **Refusals already name a leaf under a disclosure policy.** `lawRefusal fieldsOf` returns
  `ComposedLawDiagnostics.publicRefusal` filtered by the requester's grant, and `lawRefusal_isSome`
  proves disclosure never changes the verdict (read, 740–760). The design lists the redaction policy as
  new; it exists.
- **The activity kernel's resume contract is real.** `birth_checkpoint_typed` and
  `delivery_checkpoint_typed` (read: `Kernel/ObjectiveResumeContract.lean`) give typing from the actual
  preservation theorems. Consume-once is a compare-and-swap on the record cell, and fees are
  measurement-free (read: `Kernel/ObjectiveActivity.lean` header). Every await has a mandatory deadline
  height, which is idea 4's Marlowe rule (LAWS C12).
- **Root resolutions E1, C1 and D2 are correct against the literature.** E1 (finite transition table
  plus payload atoms) is the only way a difference-logic judge can host a session type. D2 (frames writing
  the same slot abort unless the law declares a commutative delta) is what CISE's conflict relation needs
  (LAWS F3).

## 3. What native admission checks today, against my eight ideas (all read at `36fca3ac`)

| idea (LAWS Part II) | on main |
|---|---|
| 1 two-state + request atoms | Request slots exist: `request/subject` (invoker), `/height`, `/verb`, `/target`, `/nonce`, `/cost`, `/policyEpoch` (`Compiler/CanonicalRuntimeProfileCore.requestSlots`). Clock, compute, `run/` and money slots are added by `projectCommonSlots`. Two-state atoms: `monotone`, `writeOnce` only. **Missing:** `leOld`, `request/method`, `request/package`, `request/cap/<i>`. **Defect D-1:** on the Objective path `run = none` (`compute_objective_matches_exact`, `Kernel/ResourceTransaction.lean` ~1305), so `runSlots` is empty and no slot names the method or package that ran. |
| 2 caller-side terms | None. The signed claim's `capacity` envelope is the only caller-side bound, and it covers cost only. |
| 3 Daml call-tree authority | No call tree yet. Every target leg carries its own signed envelope, which is the strictest Daml case (every touched party signs). |
| 4 history slots | Clock slots plus `monotone`/`writeOnce`; nothing else. |
| 5 protocol objects | None. |
| 6 coordination grade | `Pred/CoordinationDial` exists; nothing at publish or admission consults it. |
| 7 upgrade as law refinement | None. `Pred.Sat` certificates exist (`certificate_unsat`). |
| 8 decide at publish, evaluate at admission | Evaluate at admission: yes. Decide at publish: Objective publication (`BendSourcePublication`, `ObjectiveBendPublishedPackage`) runs no law analysis. |
| action scope (design §E) | Already built for joint commands: every participant's slots are projected under `joint/target/{id}/…` and `joint/index/{i}/…` into each target's law state (`projectWithCommon`, 270–297). Book balances enter through `moneyPolicySlots`. |

## 4. Defects and misses, each with replacement text

### D-1. The Objective path cannot pin an object to its package (Defect in landed code; design §A, §E)

**Evidence.**
- The law state for an Objective invocation has no method or package slot, because `prepared.run = none`
  and nothing replaces it (read; see the §3 table).
- The ordinary route (`admitOrdinary`) can write the same cells with any payload the cell's law accepts.
- The Nock route had `ran program`, "this step's writes ARE the product of program" (`Pred/Core.lean`).
  The Objective route has no analogue.
- So an object's package pin is enforced by nothing. Any signer whose envelope passes the cell's law can
  bypass the object's methods entirely, which defeats §A's "law + package pin" object and makes method
  guards impossible to express.

The fix is sound without reordering. The slot can be projected from the signed claim's `sourceAtom`
(the method artifact identity, which commits package and declaration) before execution, because
`AcceptedInvocation` exists only after `admit` has proved the executed artifact is the claimed one
(`resultExact`, `Authenticated.sound`). The law is therefore judged on a claim that acceptance makes
true.

**Replacement text (append to §E "Mechanism: three points"):**

> Every Objective invocation projects into each target's law state the slots
> `objective/artifact/<sourceAtom>` = 1 and `objective/method/<methodSemanticId>` = 1. They are named the
> way `ranSlot` is, so a 256-bit identity never enters an integer range. The slot is derived from the
> signed claim before execution; it is sound because `AcceptedInvocation` is constructed only after the
> executed artifact is shown to be the claimed one. Ordinary commands project neither slot, and reads
> fail closed. When an object is created, the kernel installs a kernel clause on its state cells,
> `any [eq (artifactSlot m) 1 | m ∈ pin.methods]`, which no package clause can remove. This makes the
> package pin a law, makes method-indexed clauses expressible (`eq (methodSlot m) 1 → …`), and refuses
> ordinary-route writes to object state. An upgrade (§C) rewrites this clause in the same turn as the
> pin. `request/cap/<i>` is projected the same way from the capabilities named in the claim's
> `inputRefs`.

### D-2. The single Receiver makes law judgement optional (design missed; receiver collapse)

**Evidence.**
- `Kernel.Receiving.Family` has `postLaw : Prepared → Bool`, documented as "family checks on the post
  images beyond the standard shape" (read: `Kernel/Receiving.lean` 141).
- `shape` = distinct cells ∧ current roots ∧ `postLaw` (169–180).
- The first migrated family, `SubjectKeyRotation`, sets `postLaw` to `PhysicalPostLaw` (physical
  well-formedness), not a committed `Pred` (read: `Kernel/Receivers/SubjectKeyRotation.lean` 239).

Nothing in `Theory.Receiving.Receiver` or `Family` requires that every written cell's committed law
judged its step. Robust safety, a check on every write whoever proposed it (LAWS B17, Part II opening),
is therefore a discipline 33 families must each remember, and the collapse's single proof
(`receive_committed`) says nothing about laws. Its migration step 3 moves `DeclaredResourceController`
onto `Family`, where today the law check lives inside `prepare`. The collapse is the moment to make law
judgement structural; after step 8 it would be a retrofit across every family.

**Replacement text (new §E paragraph "Where laws are judged"):**

> Laws are judged by the Receiver, not by families.
> - `Kernel.Receiving.Family` gains
>   `step : (p : Prepared env durable command) → (w : DataWrite) → w ∈ writes p → LawStep`,
>   where `LawStep` is the projected old and new `Pred.State` plus request slots.
> - `shape` resolves each written cell's committed law at the snapshot (`LawComposition`, one
>   snapshot) and requires `Pred.eval` to accept its `LawStep`.
> - A cell is exempt only if its kind is in a registered `KernelCellClass` (activity records, answer
>   slots, journals, fee accounts), and the registry carries a proof that only kernel families write
>   that class.
> - `postLaw` remains for physical well-formedness only.
> - Theorem `receive_committed_lawful`: every write of a committed ingress either has a committed law
>   that accepts its step or lies in a kernel class. It is proved once, over `Family`.
> - Tooth: a family whose `step` omits a write fails to construct. A fixture family whose write
>   violates its cell's law commits when the check is removed and is refused with it.

### D-3. The activity kernel writes object state with no law, and its "owner" is the fee payer (landed demo; blocks the running native-route lane)

**Evidence (read: `Kernel/ObjectiveActivity.lean`).**
- `commitYield` posts `plan.state` straight to the object cell (`statePost := postAt snapshot object
  stateBytes`, ~520). No law is judged, and the state is not checked against a declared state type.
- `writeState` lets `request.subject = record.escrow.payer` overwrite the object (934–941). The account
  that funded an activity's await fees becomes the owner of the object's state.
- The scratch world says honestly that it has no signature layer (read: `Host/ObjectiveActivityWorld.lean`
  header). The lane bringing activities onto the native route is running now; it should not inherit
  these two shapes.

**Replacement text (§B, add to Mechanism):**

> A yielded Plan's declared-state write is an ordinary write of the object's state cell. It is judged by
> that cell's committed law (D-2), with the activity's method and package slots (D-1) and the resuming
> invocation's request slots. Its value must type-check against `ObjectRecord.stateType`. There is no
> owner-write turn: state changes only through a method of the pinned package, or through an upgrade.
> Fee payer, invoker and object authority are three separate fields, and none implies another.

### D-4. "Law" and "requires" already mean something else in Objective Bend (design §E, §5 Q2; also BREAD §3.2)

**Evidence (read).**
- In the surface language, `law name(args): expr` is a universally quantified property of *methods*
  (`law positive(n: Nat): self.v(n) < n`; `native/bend-source/objective-elaborate-tv.ts` 49). It
  elaborates to a closure in spec metadata (`Compiler/ObjectiveBendElaborate.lean` 690–697), and
  "nothing discharges them" (`docs/OBJECTIVE-BEND.md` 222).
- `requires` declares a method the specification needs from final self (`requires odd(n: Nat) -> Bool`;
  `objective-parser.ts` 178 pushes a *signature*). It is not a precondition.
- The design's method guards and the Bread scholar's "generate clauses from `.obend` (`requires`,
  invariants)" would collide with both meanings.

**Replacement text (§E, new "Surface" paragraph):**

> In the surface language, admission rules are declared with four clause kinds: `invariant` (a state
> law), `guard` (a method guard over arguments and request slots), `permit`, and `forbid`. Each clause
> must elaborate to `Pred`, and anything outside the fragment is an elaboration error. A spec's `law`
> remains a property of methods. It is package evidence: discharged by the certifying checker where it
> can be, otherwise reported as unproved. It never reaches admission. `requires` keeps its meaning (a
> required member of final self).

### D-5. Seats: an empty `want` gives the contract everything (design §E seats, T3)

`offerSafe` is `any [all (want ≥), all (give ≥)]`. With `want = []`, the first disjunct is `all []`,
which is true. So every reallocation is offer-safe, and the contract may take the whole of `give`. Zoe
has the same semantics (inferred from `isOfferSafe`'s disjunction; LAWS B23); it is a donation, and it
should be explicit.

**Replacement text (§E seats):**

> An `offer` with empty `want` is refused unless the proposal says `donate`. T3 gains the tooth "an empty
> `want` without `donate` is refused at `offer`".

### D-6. Daml's "signatories" have no Mini referent (design §D, §E)

§D says a callee's fragment runs under "the callee's own signatories plus those controllers", but
`ObjectRecord` (§A) has no signatories. In Daml, signatories are the parties whose consent created the
contract, and that consent is what pre-authorizes its choices' consequences (LAWS C13; read:
`bernauer-daml-2023.txt` §3.6).

**Replacement text (§A record, and §D):**

> - `ObjectRecord` gains `creators : List SubjectId`: the signers of the birth turn, fixed for life.
> - A callee frame's authority context is the callee object's own held capabilities (its c-list) plus
>   the method's controllers present in the caller's context plus matching scoped grants.
> - `creators` are pre-authorizing parties: a frame may write cells whose law requires a creator's
>   consent only if the method's package was pinned when those creators signed (D-1's artifact clause).
>   That is exactly Daml's "a signatory has pre-authorized the consequences of the choices when the
>   contract instance was created".
> - The caller's ambient signers never enter the callee's context.

### D-7. Floors outside the fragment should be refused when installed (design §C cost paragraph)

§C says a floor containing `witnessed`, `hashEq` or `ran`, or past `dnfCap`, makes "every upgrade of that
object refuse". That silently turns a governed object into a frozen one.

**Replacement text (§C):**

> A floor is admitted into `UpgradePolicy.floors` only if `Pred.difference?` accepts it and `Pred.Sat`
> decides it satisfiable, with a witness. Otherwise the turn that adds it is refused by name. So an
> object whose floors are accepted can always be upgraded by a law that entails them.

### D-8. History slots must stay propositional (design §E history)

DejaVu's first-order past-time logic quantifies over unbounded observed values and needs BDDs (LAWS E6,
read §1). `Pred` has no such quantifier.

**Replacement text (§E history):**

> `Pred/History` compiles propositional past-time formulas only (`since`, `once`, `previously`) and
> bounded counts over a declared height window, over a fixed finite set of keys named at publish.
> Window storage is a ring of declared size, charged to the object's payer (§G). The kernel computes
> the new history from (old history, request, new state) before the law is evaluated on (old history
> and old state, new history and new state). First-order temporal quantification is out of the
> fragment.

## 5. OPEN questions

**Q2 (generate laws from `.obend` now, or unify into a decidable Objective Bend fragment).** As posed,
the question conflates two species (D-4): admission rules over state transitions, and properties of
methods. My answer:
- **Unify the syntax now; keep `Pred` as the semantics.** One `.obend` surface declares
  `invariant`/`guard`/`permit`/`forbid`. The Lean elaborator, now the implementation, elaborates them to
  `Pred` and refuses anything outside, with a theorem that the elaborated `Pred`'s `eval` is the
  clause's meaning. That is one language with one denotation, so no twin exists to drift.
- **Do not make Core4 evaluation the judge.** Everything admission relies on is indexed by `Pred`
  syntax, and a Core4 fragment would have to re-earn each of these (read on main):
  - satisfiability with certificates (`decide_unsat_iff`, `certificate_unsat`);
  - leaf explanations and disclosure (`firstFailingLeaf`, `publicRefusal`);
  - the coordination dial;
  - the constraint compiler with cast and range refusals (`Compiler/PredCompile*`, `castInjOn`).
- **External evidence for this split:** Cedar keeps a deliberately limited, separate language because
  analysability is the product (LAWS D1, D3: sound and complete Lean-proved symbolic compilation).
  Paxos Made EPR shows the language grows by keeping decision problems in a decidable class (LAWS E1),
  and refinement types show the surface-to-decidable-logic generation (LAWS E7).
- **Method properties** (spec `law`) stay package evidence (LAWS B3: Trillium-style refinement proved
  once, never at admission).

**Q1 (synchronous cross-principal `call`).** Yes, conditionally. Synchronous calls are where robust
safety is tested (LAWS B15, B16), so `call` should land only after D-1 and D-2. Without the method slot,
no law can tell a callee's write from a direct write. Without the Receiver judging every write, a new
`call` family could skip the callee's laws.

**Q3 (REPLAY).** Agree with the root's provisional drop. My domain adds nothing for keeping it.

**Q4 (order).** Insert D-1 and D-2 before L1's native route lands, and certainly before L5 (`call`). D-3
must be in the activity native-route lane's acceptance check: a yielded state write that violates its
cell's law is refused.

## 6. Commits

None. D-1 changes the law state of every Objective invocation, so it is a semantics-edition bump of
`DeclaredResourceController`'s projection, plus the Host closure and surface re-pins. D-2 is the
Receiver's core record. Neither is a small, well-scoped edit for a review lane. Separately, the local
data volume (`/System/Volumes/Data`) is at 99% (113 GiB free of 7.3 TiB, measured with `df` at review
time). Under the lane protocol's under-10% rule, I wrote nothing beyond this file and a 124 MB read-only
clone in my scratchpad.

## 7. Quests I would take next

**QUEST-LAWS-PIN (D-1).**
- Scope: Objective artifact and method slots in `projectCommonSlots` from `command.objectiveClaim`.
- Scope: `Pred` helpers `artifactSlot` and `methodSlot` beside `ranSlot`.
- Scope: a `semanticsId` bump and receiving-contract string.
- Scope: a kernel pin clause at object birth (with L3).
- Acceptance: an ordinary command writing an Objective object's state cell is refused, naming the pin
  clause.
- Acceptance: the same write through the pinned method is accepted.
- Acceptance: theorem `objective_artifact_slot_sound`: in an `AcceptedInvocation`, the projected
  artifact slot equals the executed artifact's identity; `#assert_axioms`-pinned.
- Build: `swarm-build env LEAN_NUM_THREADS=4 lake build Minidregg Host.Main:leanArts ObjectiveProofs`
  on hbox.

**QUEST-LAWS-RECEIVER (D-2).**
- Scope: `Family.step`, `KernelCellClass` with its writer-proof registry, and `receive_committed_lawful`.
- Scope: `SubjectKeyRotation` migrated as the first instance.
- Acceptance: the theorem is pinned.
- Acceptance: the fixture family's law violation is refused with the check and committed without it.
- Acceptance: rotation intents are byte-identical.
- Coordinate with the RECEIVER-COLLAPSE lane before its step 3.

**QUEST-LAWS-L4a.**
- Scope: `leOld` through `Pred.Sat` (extending `decide_never_unknown` and `certificate_unsat`).
- Scope: `Pred/Entailment` (equivalence, subsumption, dead and vacuous clauses, with certificates).
- Scope: D-7's install-time floor check.
- Acceptance: the necessity law "balance decreases only if `request/cap/owner` is presented" refuses a
  forged withdrawal.
- Acceptance: an always-false clause is reported at publish.
