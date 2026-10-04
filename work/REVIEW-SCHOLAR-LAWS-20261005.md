# REVIEW-SCHOLAR-LAWS (2026-10-05)

Reviewer: SCHOLAR-LAWS (report `work/SCHOLAR-LAWS-CONTRACTS-20261004.md`, cited LAWS). Code read at `emberian/minidregg` main `36fca3ac` (fresh blobless clone,
read-only). Tags: **read** = I read the code at the path; **inferred** = my conclusion.

## 1. Verdict

The design's §E is the right shape, and the kernel already holds more of it than §E says. But the
first native Objective path judges laws in a state that does not know which code ran. The receiver
collapse makes law judgement a per-family option rather than part of the single Receiver. And the
activity kernel writes object state with no law at all. Until those three are fixed, "code proposes,
law disposes" holds for ordinary resource commands, not for objects.

## 2. What the design and the code got right

- **Laws judge the exact writes before execution, and acceptance binds both** (read:
  `Kernel/DeclaredResourceController.lean` `admitObjective` 1655–1684): every target leg's committed law
  runs on the signed writes (`verifyAndAuthorizeLeg`, `lawLeaf`); then the method is re-executed and its
  Plan must equal those writes (`Output.exact`); `AcceptedInvocation` needs both. A refused law costs no
  execution (the design's method-guard property), and admission never calls a solver.
- **Refusals already name a leaf under a disclosure policy** (`lawRefusal fieldsOf` →
  `publicRefusal`; `lawRefusal_isSome` proves disclosure never changes the verdict; read 740–760). The
  design lists redaction as new; it exists.
- **The resume contract is real** (`birth_checkpoint_typed`, `delivery_checkpoint_typed` from the actual
  preservation theorems; consume-once CAS; measurement-free fees; a mandatory deadline on every await,
  idea 4's Marlowe rule, LAWS C12).
- **Root resolutions E1 and D2 are right**: a finite transition table plus payload atoms is the only way
  a difference-logic judge hosts a session type; D2's commutative-delta exception is CISE's conflict
  relation (LAWS F3).

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

**Evidence (read).** The Objective law state has no method or package slot (`run = none`, §3), while
`admitOrdinary` can write the same cells with any payload the law accepts; the Nock route's `ran program`
has no Objective analogue. So the package pin is enforced by nothing: a signer can bypass the object's
methods, and method guards cannot be expressed.

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

**Evidence (read).** `Family.postLaw : Prepared → Bool` is "family checks on the post images beyond the
standard shape" (`Kernel/Receiving.lean` 141), and `shape` = distinct cells ∧ current roots ∧ `postLaw`
(169–180); the first migrated family sets it to `PhysicalPostLaw`, not a committed `Pred`
(`Receivers/SubjectKeyRotation.lean` 239). Nothing makes every written cell's law judge its step, so
robust safety (LAWS B17) is a discipline 33 families must each remember, and `receive_committed` says
nothing about laws. Step 3 moves `DeclaredResourceController`, whose law check lives inside `prepare`,
onto `Family`: now is the moment to make it structural, not after step 8.

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

**Evidence (read: `Kernel/ObjectiveActivity.lean`).** `commitYield` posts `plan.state` straight to the
object cell (`statePost`, ~520) with no law and no declared-type check; `writeState` lets
`request.subject = record.escrow.payer` overwrite the object (934–941), so the fee payer is the owner.
The scratch world is honest that it has no signature layer; the running native-route lane must not
inherit either shape.

**Replacement text (§B, add to Mechanism):**

> A yielded Plan's declared-state write is an ordinary write of the object's state cell. It is judged by
> that cell's committed law (D-2), with the activity's method and package slots (D-1) and the resuming
> invocation's request slots. Its value must type-check against `ObjectRecord.stateType`. There is no
> owner-write turn: state changes only through a method of the pinned package, or through an upgrade.
> Fee payer, invoker and object authority are three separate fields, and none implies another.

### D-4. "Law" and "requires" already mean something else in Objective Bend (design §E, §5 Q2; also BREAD §3.2)

**Evidence (read).** Surface `law name(args): expr` is a ∀-property of *methods*
(`law positive(n: Nat): self.v(n) < n`, `objective-elaborate-tv.ts` 49), elaborated to a closure in spec
metadata (`ObjectiveBendElaborate.lean` 690–697) that "nothing discharges" (`docs/OBJECTIVE-BEND.md`
222). `requires` declares a member needed from final self (`objective-parser.ts` 178 pushes a
*signature*), not a precondition. The design's guards and BREAD's "generate clauses from `requires`"
collide with both.

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

**Q3 (REPLAY).** Agree with the provisional drop.

**Q4 (order).** Insert D-1 and D-2 before L1's native route lands, and certainly before L5 (`call`). D-3
must be in the activity native-route lane's acceptance check: a yielded state write that violates its
cell's law is refused.

## 6. Commits

None: D-1 is a semantics-edition bump with Host-closure re-pins and D-2 is the Receiver's core record;
neither is a small review-lane edit. The local data volume is at 99% (113 GiB free of 7.3 TiB, `df`), so
under the protocol's 10% rule I wrote only this file and a 124 MB read-only clone in my scratchpad.

## 7. Quests I would take next

**QUEST-LAWS-PIN (D-1).** Artifact/method slots in `projectCommonSlots` from `command.objectiveClaim`;
`artifactSlot`/`methodSlot` beside `ranSlot`; `semanticsId` bump; the kernel pin clause at birth (with
L3). Acceptance: an ordinary write to an Objective object's state cell is refused naming the pin clause,
the pinned method's write accepts, and `objective_artifact_slot_sound` (the projected slot equals the
executed artifact in every `AcceptedInvocation`) is `#assert_axioms`-pinned. Gate: `swarm-build env
LEAN_NUM_THREADS=4 lake build Minidregg Host.Main:leanArts ObjectiveProofs` on hbox.

**QUEST-LAWS-RECEIVER (D-2).** `Family.step`, `KernelCellClass` with its writer proof,
`receive_committed_lawful`; `SubjectKeyRotation` first. Acceptance: theorem pinned; the fixture
violation refused with the check and committed without it; rotation intents byte-identical. Before the
collapse's step 3.

**QUEST-LAWS-L4a.** `leOld` through `Pred.Sat` (`decide_never_unknown`, `certificate_unsat` extended),
`Pred/Entailment` with certificates, D-7's install-time floor check. Acceptance: the necessity law
"balance decreases only if `request/cap/owner` is presented" refuses a forged withdrawal; an always-false
clause is reported at publish.
