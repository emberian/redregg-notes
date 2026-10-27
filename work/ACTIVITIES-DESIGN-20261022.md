# Activities and continuations in nano: the map, the design, the theorems, the price (2026-10-22)

SCHOLAR-ACTIVITIES, read-only. Sources, each at the commit I read: nano hbox main `81e0507` (N:,
`/tank/dregg-build/nanodregg/main`); mini `334316df` (M:, `~/dev/minidregg`); breadstuffs `22fad151e` (B:,
`~/dev/breadstuffs/metatheory`); the proposal `redregg/work/ACTIVITIES-PROPOSAL-20261022.md` (P:, the three GPT
documents, also pasted whole by Ember). Labels: **MEASURED** = a number or a statement I read off the tree at a
file:line; **READ** = a definition, theorem or decision I opened; **ASSUMED** = my judgement, nobody measured it.
No build was run; no file but this one was written.

Ember's ruling: "I want activities and continuations ... promote those things into nano, because we would finally
have a firm theoretical, metaprogrammatic and proof-engineering basis to rest them upon." The charter excludes
proof systems, host-hiding and multi-node agreement, nothing else (N:CHARTER.md "Scope", READ). A re-genesis is a
judge, never a cost; a design's price is the premises it adds to landed theorems.

---

## 0. The verdict in twelve lines

1. Nano already holds **every load-bearing half** of the proposal, under its own names, PROVED: the dependency
   tracking (versioned pins, `Pinned D`, `receive_congr`, `stale` BEHIND/AHEAD), the continuation structure
   (`Prog`/`interp_runs`/`kept_follows`/`resume_durable`), the accepted history (`ObjectHistory`,
   `object_history_chain`), locality (`CallFoot`/`submit_frame`/`admit_comm`), conditional soundness
   (`law_judged`/`write_judged`/`invoke_next_judged`/`object_step_some`), and a worked TMS (the GATES judge).
2. What nano lacks is **the object**: a persistent place where a decision is made, that remembers its candidates
   and the reason each was set aside, and a method that SUSPENDS into it. LANG-48 (`Std.pending`) was approved on
   10-18 and never built; it is one third of the object.
3. The Bell (LANG-58/59 + the resident) **is already activity v0**: `ring` suspends, `pending` is the suspension
   relation, `answer` resumes under a guard over the response, `rung: answered` is resume-consumes-once. It lacks
   only the name, the declared machine, and candidates.
4. The right nano shape is **rows, not a cell kind**: a continuation is a ROW under the activity's object; a hole is
   a row plus a `candidates` relation; fill/select/rejudge are package METHODS whose edits a LANG-59 guard judges.
   Kernel premises added: **zero** (MEASURED from LANG-48's price and LANG-44 (c)'s enumeration). A cell kind would
   touch the three totalities (`effect_at_object`, `object_turn_cases`, `effect_at_grant`) and every `readKind` site.
5. "Withdraw a support" is a **pin going stale**, detected by the kernel, not by a guard: a candidate records the
   pins it depends on; a `select` must re-cite them; a moved one is refused `stale`. Derivability (the row's
   recorded status) and current admission (the select's pins at the World) are two different judges, exactly P:'s
   distinction, and nano already keeps them apart in `receive` versus `World.admit`.
6. The response-dependent continuation (mini's `IndexedProgram.call op k`) maps onto nano's `Std.machine`: the
   typestate is the machine field, an operation is a method, `next(op, r)` is the `case` on the response inside
   the method, and the landed `machine_reached` + `object_history_chain` are **`interp_runs` for any activity**.
7. The strong hole (undetermined shape or amount) stays inexpressible, as breadstuffs and LANG-48 ruled.
8. Experiment 4 (a cycle losing its grounding) **refutes a one-level support record**: the design must forbid a
   hole supporting a hole, or close supports transitively to a bounded depth. Decision card F.
9. Experiment 6 (replace a filling preserving its contract) exposes that nano's locality is **by bytes, not by
   contract**: a consumer that pinned the hole's row is stale after any replacement. The honest answer is a separate
   exported `value` row the consumer pins, and an ASSUMED fact about row versions to measure first.
10. Nothing re-geneses for the rows design. It is a `lang!` (new Std generators; the Bell re-ids and re-emits) plus
    PROTOCOL journey rows. No wire moves. No vector moves unless the package wire gains a node (it need not).
11. Mini's deliberate divergences stay reversed: call-by-value and `let`-eager stay (a continuation is data, never
    a heap checkpoint); `perform` stays out of the term language (LANG-6 holds); reflection stays out; the activity
    is a package shape, not a type `Activity<P,R,A>`.
12. One redesign day: two LANG lanes (activity generator; hole generator), one PROTOCOL lane (rows LH0-LH9), the
    Bell re-cut as the instance, zero KERNEL code, one KERNEL proof lemma (support pins as a `CallFoot` corollary).

---

## 1. THE MAP: proposal concept -> nano HAS IT / BUILD IT / MINI-ONLY

Columns: the proposal's object; where nano has it (file:line, its nano name); what remains to build; what cannot
transfer under the charter and why. Every HAS row is READ at the cited line unless marked otherwise.

### 1.1 The open artifact and its parts: (P, Omega, sigma, D, support, Phi, t)

| proposal part | nano HAS | BUILD | MINI-ONLY / out of charter |
|---|---|---|---|
| P, the retained template separate from its environment | A package is ROM, immutable, content-addressed (`Lang/Package.lean:35` `structure Package`; `romIdOf`, LANG-9); an object is `{pkg, laws, state}` (`Kernel/Receive/Derive.lean:113` `objectCell`). The template never specialises: every run re-reads the package (`Program.run` at `Kernel/Receive/Call.lean:~340`). | nothing | mini's `check_instantiate` template instantiation is TYPE-level polymorphism (M:`Theory/ObjectiveBendTemplates.lean:1033`); nano has no polymorphism (LANG-1 critique, LANG-23) and does not need it for this: the "environment" is state + rows, not a type substitution. |
| Omega, the open interface (which components are unspecified) | The declared RELATIONS of a package (`Package.rels`, `RelDecl` at `Lang/Package.lean:21`): a relation is a PLACE, never a value, with a declared key, value type, limit, guard. A hole's interface = a relation's declared row type. | a `Std.hole` generator declaring the two relations (`holes`, `candidates`) with their types (section 3.3) | nothing |
| sigma, the current partial substitution | `pending` in LANG-48's sum `open {closes, filler} \| filled {by, value}` (APPROVED 10-18, NOT BUILT: `decisions/lang.md:1609`, MEASURED: no `Std.pending` in `Lang/Std.lean`, grep `pending` = 0 hits in that file). As hand-written patterns: CappedTally (LANG-45), Escrow `held -> released \| refunded` (LEDGER), the Bell's `rings[k].answer : optTy bytes` (LANG-59). | `Std.pending` as approved, extended: the filled arm names the CANDIDATE key, not only a value | nothing |
| D, the available derivation | nano has NO derivation objects in state (charter: no proof system; "admission is checked by re-execution", CHARTER.md Scope item 1). The derivation of a turn is `receive X w c` itself, re-run by every auditor (`Kernel/Receive/Audit.lean`). | nothing: D is the re-execution. A candidate's "derivation" is its recorded status + its supports. | P:'s `[Psi |- A]` as a stored proof term: MINI-ONLY in spirit (mini stores typed checkpoints, `stored_checkpoints_typed`); nano stores data and re-judges. Correct under the charter. |
| support, the dependencies | **versioned pins**: `Unsigned.pins : List (D x D)` (`Kernel/Receive/Call.lean:96-110`), `rowPins`, `ranges`; the receiver sees only `Pinned D` (`Call.lean:422` `pinned`: `unpinned` for any other id); `receive_congr` (`Kernel/Proofs/Receive.lean`): two Worlds agreeing on the pinned cells derive the same Turn; `stale_refused`/`admit_pins` (`Kernel/Proofs/Admit.lean`); KERNEL-54 as built: a per-entry write counter, `stale_behind_forever` (`Kernel/Proofs/Versions.lean`), BEHIND final / AHEAD open (`Protocol/Command/Machine.lean:876` `staleBehind`). | record a candidate's supports IN ITS ROW (the pins it was verified under), so a later `select` must re-cite them (section 3.3) | mini's `PlanBinding.Footprint` (M:`Theory/PlanBinding.lean:68`) is the same object; nano's is stronger (versions make BEHIND final). |
| Phi, the residual obligations | Refusals by name (law 7; `Refusal`/`Reject` constructors, `Submit.lean:16` `Verdict`); the attempt store's statuses `committed \| refused \| declined \| unknown \| absent \| lost \| open` (`Protocol/Attempt.lean:~60` `Seen`); `uncertain` is a real outcome (`Machine.lean:969-1001`). For a hole: LANG-48's `open` arm. | the candidate status sum `verified \| suspended obligation \| conflict reason \| pruned reason \| uncovered ticks` (section 3.3) | nothing |
| t, the accepted interaction history | `ObjectHistory X obj w w' tr` (`Kernel/Proofs/Logic/History.lean:116`), every step of the World around one object; `object_history_of_audit` (`:234`): an audited log IS one; `object_history_chain` (`:356`): it projects to `Std.Chain (Std.Step [] t)` for every `NoRef` law in force. The journal is the receipt (KERNEL-17). | nothing | mini's `History.reference` / interaction tree (M:`docs/OBJECTIVE-BEND.md:491-499`): the same shape at the activity level; nano's is at the object level, which is where the kernel judges. |

### 1.2 The three kinds of openness (P: doc 2 section 1)

| openness | nano HAS | BUILD | MINI-ONLY |
|---|---|---|---|
| an unspecified component, resolved by typed substitution | a row `upsert`/`insert` at a declared value type, judged by the relation's guard `S -> Req -> {edit, old} -> Verdict` (`Lang/Package.lean:381-384` `guardInTy`/`guardTy`, LANG-59); Lang's install check types the edit (`methodSig`, `:325`) | the "Discharges-style" check IS: install typing (static) + guard (dynamic). Nothing more. | Cave-Pientka first-class substitutions: nano has no substitution objects and no binders at the data level; a filling is a VALUE at a declared type. Enough for every experiment in P:; the contextual-type machinery (metavariables with local contexts) would only be needed for holes INSIDE terms, which LANG-6 keeps out. |
| an interaction with an environment (a peer may accept, refuse, respond, stay silent) | the host side: `Prog` (`Hosting/Resident/Run.lean:281`) `cmd c k \| keep r t k \| forget k \| ask r q k \| say s k`, a continuation per RESULT (`k : Except String Reply -> Prog`, `k : AskEnd -> Prog`); `Runs` (`Hosting/Proofs/ResidentRun.lean:51`) = every path for every reply; `interp_runs` (`:700`); `tick_order`/`tick_counts`. The kernel side: `Std.machine` edges `(state, method, state')` (`Lang/Std.lean:305-321` `machineLaw`/`stepLaw`), `machine_reached` (`Lang/Proofs/StdChain.lean:100`). | the activity as a package shape: machine + a `waits` relation + one resume method per plan kind whose argument is the response sum (section 3.2) | mini's `Activity<P,R,A>` as a TYPE with `perform`/`done` in the term language (M:`docs/OBJECTIVE-BEND.md:74,334-392`): not transferred; LANG-6 (`DECISIONS.md:525`) cut `perform` for measured reasons (delvetalk's checkpoint cost, mini's ~25 files of checkpoint/settle/collect). The data shape loses nothing observable (LANG-45 measured: "the port lost nothing observable but the activity's return value"). |
| an unfinished execution (dispatched, outcome unresolved) | the attempt store (`Protocol/Attempt.lean`): a FROZEN call driven by `submit/lookup/confirm/probe`, never re-signed; `uncertain` stays frozen on disk; follow settles (`Settle.ofReceipt`, PROTOCOL-46); the resident's `Mem.kept` + the volume (`Run.lean:127-135`, `keep_durable`, `resume_durable`, HOSTING-37/39): "a spent ask is never repeated". | the same discipline for a suspended activity's outstanding CALL: the continuation row records `dispatched : bool`; a replacement of the plan after dispatch is refused by the guard until the outcome row exists (section 3.3, experiment "lose the reply after dispatch") | mini's portable continuation (M:`docs/PORTABLE-CONTINUATION.md:58-60`: "Uncertain external calls carry exact original custody and remain uncertain until the ... receiver resolves them") is the same rule stated for a multi-host move; the move itself is out of charter (host-hiding, agreement). |

### 1.3 Repair hints, ATMS justifications, pruning reasons (P: doc 1 sections 2, 4, 7, 8)

| concept | nano HAS | BUILD | MINI-ONLY |
|---|---|---|---|
| a justification that is inspectable (which assumptions support this judgment) | the call's pins + the Turn's touches (`Kernel/Turn.lean:37` `Touch {cell, seen, act}`), one per observed cell, in the journal; the refusal record (KERNEL-44) names the code; GATES-20: every verdict row carries its TRACED READ-SET (`decisions/gates.md:514-580`, `t:<key>` records with the read-set in the payload) | the candidate row's `supports` field | nothing |
| why an alternative was set aside | the kernel records REFUSALS by name and keeps them final (KERNEL-44; `refusedFinal`, `Submit.lean:32`); a member's CANCEL record (KERNEL-60 (3): `recordOf`, `cancelled`, the member's signature in the record). The GATES judge records why a run re-ran: `reuse U: re-run (key changed)` versus `reused (key ...)` (GATES-19 (3)). | the candidate status arms `pruned reason` / `conflict reason` / `suspended obligation`, each payload a refusal NAME (law 7), written by the method that set it aside, so the reason is data a later `rejudge` reads | nothing |
| a pruning reason that can itself be withdrawn | KERNEL-57 `law_judged` (`Kernel/Proofs/Authority.lean:193`): a `relaw` is judged by the laws in force AND every added law judges the state it is adopted over (`adopt`): a law is a pruning reason with a base case; relaw removes it. GATES-20e: a changed judge TABLE selects the row that measured it (a changed ceiling re-judges). | `rejudge` re-reads a `pruned` candidate under the CURRENT laws/guard parameters (experiment 3) | nothing |
| repair correctness: repair agrees with from-scratch | GATES-19 (3) + GATES-20: a verdict is carried only under a BYTE-IDENTICAL input key, re-keyed on the candidate by the judge's code before the verdict (`rebase.py verify`, "stale verdict" refusal); and `receive_congr`: the derivation is a function of the pinned view, so a cached derivation equals a fresh one whenever the pins agree. The follower's `audit` IS from-scratch (Audit.lean re-derives every Turn). | `rejudge_agrees` (section 4.2) | Demanded Abstract Interpretation's incremental-vs-batch theorem: the nano form is `receive_congr` plus determinism of `Lang.judge`; no fixpoint iteration exists to be incremental about. |
| locality: repair need not inspect the rest | `CallFoot X c w` (`Kernel/Proofs/Logic/Triple.lean:45`): what a call may write = pinned cells, untaken ids, unspent nullifiers; `callFoot_of_turn` (`:68`); `call_frame` (`:91`); `submit_frame` (`:98`): the frame rule; `not_callFoot_live`/`indep_live` (`:105-119`); `admit_comm` (LANG-44 (11), built LANG-49: "two answers / two proposals over one view both land, in both orders"). | nothing for cells; for a hole: `select_frame` is `submit_frame` at the hole's rows (section 4.3) | mini `no_toctou` (M:`Theory/PlanBinding.lean:375`) and `independent_commute` (`:438`): the same two facts; nano's are over the deployed receivers, mini's over a toy `Store L`. |
| ATMS: multiple environments kept apart (p :- not q. q :- not p.) | not representable: nano has no derived facts, no negation-as-failure, one total order. The nearest object: two CANDIDATES of one hole, each `verified` under its own supports, neither selected: their union is never asserted because `selected` names one. | the `selected : optTy candidateKey` field (one world chosen; the others retained) | de Kleer's label propagation over a Datalog program: out of scope, not out of charter; nano's ATMS is the judge's read-set attribution (GATES-22 (3)), which intersects read-sets with changed paths. |
| a cycle must lose support when its grounding disappears | not representable by one-level pins (experiment 4 REFUTES: a hole whose candidate pins another hole's selected row stays `verified` when that hole's own support moves, because the pin commits to the row's BYTES, not to the currency of the row's recorded supports) | decision card F: forbid hole-supports-hole, or close supports to depth `callDepthMax` = 4 (the same bound the invoke tree uses, `Kernel/Receive/Derive.lean:356` `tree`) | nothing |
| provenance semiring (ab + c): retracting a keeps J through c | two candidates c1 (supports a, b) and c2 (supports c): withdraw a => c1 stale, c2 selectable (experiment 1). Sums = candidates; products = a candidate's support list. | nothing beyond the hole generator | the semiring as an algebra over derivations: not needed; the kernel's pins are the product and the candidates relation is the sum. |

### 1.4 Guarded holes (P: doc 1 section 4-5, doc 2 section 3, doc 3 LPCFS)

| concept | nano HAS | BUILD | MINI-ONLY |
|---|---|---|---|
| the weak hole: eager shape, lazy witness | breadstuffs B:`Dregg2/Exec/GuardedHole.lean:37-70` (`GuardedHole {field, actor, target, guard}`, `holeFill_binds_in_circuit`, `holeFill_rejects_guard_violation`; READ); nano LANG-48 proposed `pending_fill_binds` as its twin (`decisions/lang.md:1609-1676`); as package patterns: CappedTally, Escrow, the Bell's `rings[k].answer` with guard `rung` (LANG-59: `insert: answer none ("answered")`, `upsert: ... old.answer none ("answered"); new text = old.text ("text")`) | `Std.pending`, built as approved | mini's `HoleSpec` (M:`Theory/GuardedAdvice.lean:44`: eleven eager fields incl. `continuation`, `nullifierDomain`) is Theory only, "never reached Mini's Host" (MINI-CONCEPTS section 6 (2), READ). Nano does not want a kernel HoleSpec (LANG-48 alternative (a): a second shape of "a law over pending state", law 1). |
| the guard over the response | LANG-59 guard type `S -> Req -> {edit, old : optTy V} -> Verdict`: sees the state before, the request, the edit and THE ROW IT REPLACES; `guardEdits` finds every old row before running any guard (`guardEdits_unpinned`, `guardOld_pinned_row`); refusal `lawDenied pkg "GUARD: reason"` | nothing: the hole's guard IS a relation guard | nothing |
| fill = typed substitution checked against the guard | install: `methodSig` rebuilds the reads/edits types and compares EXACTLY (LANG-49); at run: the guard; the value's codec round trip is Lang data's (`Means`, `Lang/Proofs/Extract.lean:79`; `runMeasured_means` `:363`: what extraction forces is the meaning, LANG-61/62) | nothing | `Advice.codec_roundtrip` (M:`GuardedAdvice.lean:~70`): the same fact for mini's `LawfulCodec` |
| use-once + revocation in one transaction (LPCFS) | nullifiers (`Body.transfer ... once`, `onceNullifier`; `checkNullifiers` in `World.admit`; `CallFoot.spent`); `revoke`; `rotate_stales_outstanding` (`Kernel/Proofs/RotateStale.lean`, KERNEL-60): a rotation ends every in-flight call that pinned the member; and all of it inside ONE `World.admit` (law 1: one admission path). "Using a resource once inside one proof does not prevent replaying the whole proof in another request": nano's answer is that the proof IS the request (re-execution) and the journal makes a duplicate commit impossible (`replayed`, `Submit.lean:32`). | nothing | nothing |
| polarity / ownership of a hole (who chooses, who must accept) | LANG-48 `fillerTy = sum {anyone, member digest}`; the Bell's guard `rung`: `insert: ringer = agent ("notYours")`, `upsert: agent = resident ("notResident")` (LANG-59): two polarities on one relation, by edit arm; `Req.agent`/`Req.principal` (`Call.lean:317`); grants (`Right.invoke method`) for who may call which method | `chooser`/`acceptor` fields in the hole row, enforced by the guard's arms (card E) | interface automata's alternating simulation as a THEOREM about refinement: not needed for the experiments; nano states polarity as a refusal by name. |
| partiality visible in the result type (witnessed / open / refuted / outside) | attempt `Seen` + `Settle`: `committed` / `refused` (recorded, or window passed, or BEHIND stale: final) / `open` (AHEAD, absent, window live) / `forgotten` / `uncertain` (`Protocol/Attempt.lean`, `Protocol/Settle.lean`); the rows judge's `Verdict.hang` ("not a pass and not a fail", `Protocol/Rows/Judge.lean:~30`); `Pred.eval`'s missing-field-is-false (B:`PredAlgebra.lean:185-224`, READ via P:) has NO nano twin: a Lang `case` on a sum has no default arm (`lawCase5`, `Lang/Std.lean:112`: "the checker requires one arm per label"), so an `open` arm must be written and cannot be read as `false`. | the candidate status sum: `verified` = witnessed; `suspended obligation` = open; `conflict reason` = refuted (a CHECKED refusal, named); `uncovered ticks` = outside this procedure (the budget) | nothing |
| derivability separate from current admission | `receive X w c` derives on the PINNED view only (`Pinned D`); `World.admit` checks the pins against the current World (`touchCheck`, `stale`); `Triple X P c Q` (`Triple.lean:52`) is defined over the two functions. A derived Turn is "a construction valid relative to its context"; admission is "the context is current". | a candidate's recorded status (relative to recorded supports) versus a `select`'s pins (current): the same two judges (section 3.3) | mini `Capability.Admissible.at_policy_revision` (M:`Theory/TypedAuthorization.lean:1210-1245`, READ via P:): the transport theorem; nano's twin is `receive_congr` + `admit_pins`. |
| executed-prefix obligations (mini's six cuts) | Reserve/Install/Retire = escrow phases `open \| held \| released \| refunded` (LEDGER-6/10), nullifiers, grant ledgers (KERNEL-60/61: `grant_turn_ledger`: a cap only falls); Observe/Invoke = `Right.observe`/`Right.invoke`; Release = `read` with a follow grant (PROTOCOL-3: membership is the confidentiality boundary). "Yesterday's acceptance can stay true while today's role change prevents installation": `rotate_stales_outstanding` + `revoke` + KERNEL-57 adoption. | the continuation row's `dispatched` flag and the "no re-plan after dispatch until the outcome row exists" guard arm | mini's `Cuts.lean` as six distinct TYPES (M:`Kernel/Contracts/Cuts.lean:338-372`): nano has them as receivers and laws, not as a typed vocabulary; a vocabulary without a consumer is a twin. |
| stability class: under which substitutions is a guard's verdict stable | `Relib` (`Lang/Proofs/Extract.lean:638`), `means_relib` (`:616`), `bigStep_relib` (`:476`): a `NoRef` term's meaning is stable under any library change; `receive_congr`: a derivation is stable under any World change outside the pins; `judgeOne_admits_relib` (used at `History.lean:384`). These ARE the "class of substitutions this result is stable under": every change outside the pinned view and outside the term's refs. | state it once for holes: `candidate_status_stable` (section 4.2) | Hu-Pientka-Schopp's presheaf naturality: the nano instance is the two theorems above; nothing categorical is needed. |

### 1.5 Response-dependent continuations and the interpretation theorem

| concept | nano HAS | BUILD | MINI-ONLY |
|---|---|---|---|
| `Program.call op k`, `k : (r : Resp op) -> Program (next op r)` | `Prog.cmd c k`, `k : Except String Reply -> Prog alpha` etc. (`Run.lean:281-292`): a free program over five effects with `Ix` trivial; `Handler M` (`:295`) = mini's `Handler`; `Prog.interp` (`:304`) = mini's `interpret`; `Runs` = the path relation; `interp_runs` (`ResidentRun.lean:700`): the interpreter performs exactly a path, for EVERY oracle = "fold correctness at the recording handler"; tooth `interpTwice_no_path` (`:736`). Kernel side: `Std.machine` (`Lang/Std.lean:298-321`): `stateTy states`, `machineLaw`, `stepLaw`, `stepTarget`: the typestate and its edges; `Reach` (`StdChain.lean:93`), `machine_reached` (`:100`). | the activity generator composes `Std.machine` + a `waits` relation + per-plan resume methods: the method's `case` on the response IS `k r`; the edge the method takes IS `next op r` (section 3.2) | `fold_fusion`/`fold_rel` (M:`Theory/IndexedProgram.lean:103,136`): nano has no second carrier to fuse into (one machine, one judge; law 1), and `interp_runs` at the recording handler is the one instance it needs. |
| the continuation cell (captured context, durable) | the resident's `Mem.kept : Option (Ring x ByteArray)` + the volume (`keep`/`forget`/`resume`, `Run.lean:192-245`); `kept_follows` (`ResidentRun.lean:571`): the memory never holds a text the volume did not report kept; `seed_after_keep`/`resume_durable`/`keep_resumed` (HOSTING-37/39). THIS IS A PROVED CONTINUATION CELL ON THE HOST SIDE. | the kernel side: a `waits` row under the activity object, keyed by the suspension's key, valued by the captured context at a declared type (section 3.2) | mini's typed checkpoint of a demand-machine heap (`stored_checkpoints_typed`, `runSegment_stored_converse`): a heap checkpoint is what LANG-6 refused to pay for; nano's captured context is DATA the author names. |
| resume consumes once | the Bell: `rung: answered` on the `rings` upsert (LB8, LB8b, LB13e; LANG-59); the resident: "a spent ask is never repeated", the intent keep before the ask (`tick_order`, `order_refuses_ask_before_keep`) | nothing: a resume is an upsert on the `waits` row guarded by `old.answered = none` | mini `resume_consumes_once` (nullifier bound to the checkpoint digest): nano gets the same from the row's version + the guard; a nullifier would be a second lock (LANG-59 deleted exactly that: "one guard for exactly-once instead of two locks"). |
| the interpretation of substitution (interpreting an instantiated protocol agrees with interpreting its template) | `object_history_chain` (`History.lean:356`): an object's history under a law in force IS a `Std.Chain` of that law's steps, "step for step", under every lib; `runMeasured_means` (LANG-61/62): what a run's extraction forces is its meaning | nothing: for an activity the "template" is the package and the "instantiation" is the rows + state; the chain theorem already quantifies over both | nothing |

### 1.6 What is MINI-ONLY by charter (not by omission), listed once

- Multi-party agreement over a hole (the two-cell negotiation with two WRITERS, Generic Simplex, tiers): out
  (charter item 3). The first integration experiment (P: doc 3) "two cells negotiate a one-use capability" runs
  on nano with ONE writer and two MEMBERS: both members sign calls against one World; that is enough for every one
  of its four changes (section 5, LH9).
- A proof object stored in the hole (`[Psi |- A]` as a term, Pumpkin Pi transport, OpenTheory certificates): out
  (charter item 1). Nano's D is re-execution; "transport a surviving proof" becomes "re-judge under current laws
  with the recorded supports current".
- Hiding a candidate from the Host (a sealed bid as a hole filling the operator cannot read): out (charter item 2).
  A sealed market on nano is commit-then-reveal in two rows, both readable by the operator.
- Mini's upgrade/drain/migrate of a running activity (M:`docs/OBJECTIVE-BEND.md:421-436`): not charter-excluded,
  but nano has no package upgrade (a package is ROM; an object cannot change package). A new package is a new
  object; the old activity's rows are its executed prefix and stay where they are. Experiment 5 (dependent-context
  change) is therefore `relaw`/`adopt` on the SAME package, which KERNEL-57 already judges (section 5).

---

## 2. THE FOUNDATIONS, stated so the design can rest on them

**F1. The resident's `Prog` is a free program over effects whose interpreter is proved to perform exactly a
path** (HOSTING-36/37, READ). `Prog alpha` (`Run.lean:281`) has one constructor per effect, each with a
continuation on the effect's RESULT; `Runs p es a` (`ResidentRun.lean:51`) is the path relation; `interp_runs o p n
es` (`:700`) says that at the recording handler, whatever results the oracle gives, `interp` appends exactly one
event per node in tree order and ends with the path's end. `tick_order` (`:273`) and `tick_counts` (`:410`) then
read the effect order off `Runs`. The trust boundary is named: `ioHandler`'s five fields are the five calls;
IO's bind sequencing is the runtime's. This is P:'s "response-dependent continuation" with `Ix` trivial and the
interpretation theorem (`fold_fusion`'s job) done at the one handler that matters.

**F2. The continuation cell is durable over a crash RELATION, and the restart's seed is what the volume holds**
(HOSTING-37/39, READ). `keep_durable`/`keep_atomic`/`forget_durable` over every crash outcome of a POSIX model
(`Resident/Volume.lean`, `Crash` a relation); `kept_follows` (`:571`) ties the next tick's memory to the successful
keeps and forgets; `resume_durable`/`resume_atomic`/`keep_resumed` (HOSTING-39) make a start re-run a whole keep of
what it holds before its first tick. P:'s "an unfinished execution: a transition that preserves history and
outstanding obligations" is this, proved, for the one activity nano runs.

**F3. The kernel's accepted history around one object is a chain of judged steps, for every law in force**
(KERNEL-59, READ). `ObjectStep` (`History.lean:62`, eight constructors: refusal, other, keep, frame, write, law,
invoke, nested), `ObjectHistory` (`:116`), `object_step_none` (a non-judged step keeps the object), `object_step_some`
(`:156`: the old state is live, the laws judged `old -> new`, a relaw/adopt keeps the state, an invoke's package
RAN `old -> new`, the next live state reads `new` at every key), `object_history_of_audit` (`:234`: the totality at
the log), `object_history_chain` (`:356`: THE LIFT). Premises: `X.Lawful` (as 116 landed theorems), `X.program =
Lang.program ...` (as `escrow_*`), the law in force at every judged step, a live start. No typing premise.

**F4. Locality is the receivers' TYPE** (KERNEL-58, READ). A receiver sees `Pinned D` and refuses `unpinned`
for anything else; `CallFoot` is read off the call and the World; `submit_frame` is the frame rule; at a live
object the footprint is exactly the pins (`not_callFoot_live`). Rows: `admit_comm` (LANG-44 (11), built LANG-49).

**F5. The dependency record is the signer's, versioned, and its staleness is final when BEHIND** (KERNEL-11, 54,
READ). Every touch is a pin the signer saw; `stale_refused`; the entry version makes a pin observed earlier on
the same fold stale forever (`stale_behind_forever`); `judge` DECLINES stale (never recorded); the attempt side
settles BEHIND -> refused, AHEAD -> open from the member's own fold.

**F6. The judge is a worked TMS** (GATES-19/20/20b/20d/22, READ). Every run is traced; its read-set keys the
verdict; a verdict is carried only under a byte-identical key and re-keyed on the candidate by main's code
before use; a changed table selects the row that measured it; a red at the convergence is ATTRIBUTED to the commits
whose changes a full judge would have selected it for (intersecting read-sets with changed paths); a tracer failure
is UNREAD, never a verdict; an escaped name invalidates the whole trace (fail-closed). The vocabulary P: wants for
holes (support, justification, carried-under-identical-support, attribution of a withdrawal) is this vocabulary.

**What the foundations do NOT give (the honest gaps).** (g1) No persistent hole object with candidates. (g2) No
kernel-side continuation row: the Bell's `pending` is one by accident of design, unnamed. (g3) No `Std.machine`
on the Bell (its state is `open bool`; MEASURED LANG-58 state line), so `machine_reached` does not yet apply to
the one activity. (g4) A guard sees (state, req, edit, old row): never another object (LANG-48 critique (1),
LANG-49 critique (3)); a candidate's support on ANOTHER cell is therefore checked by the kernel's pins, not by the
guard. (g5) One-level pins (experiment 4).

---

## 3. THE DESIGN, as nano objects

### 3.1 Vocabulary (each word is one nano object)

| word | nano object |
|---|---|
| ACTIVITY | a package whose state carries a `Std.machine` field and which declares a `waits` relation and, per plan kind, one `resume_<plan>` method |
| SUSPENSION | a method run that INSERTS a `waits` row `{plan, captured, dispatched := false, answered := none}` and steps the machine to a `waiting_<plan>` state |
| CONTINUATION CELL | that row: key `(notBefore nat)(agent digest)` or `(nonce digest)`; value `rec {plan : planTy, captured : K, dispatched : bool, answered : optTy R}` |
| RESPONSE TURN | a signed `invoke obj resume_<plan> {key, response : R}` whose signer pinned the row (`derivePins` does it, PROTOCOL-17) |
| RESUMPTION | the `resume_<plan>` run: `case response` chooses the edge; upserts the row's `answered`; steps the machine; emits calls/edits; returns the new state |
| HOLE | a `waits` row whose resumption is a SELECTION among retained candidates: relation `candidates` keyed `(hole key, cand digest)`, value `rec {value : V, status : statusTy, supports : supportsTy, by : digest}`; the hole row carries `selected : optTy digest`, `chooser`, `acceptor`, `closes` |
| GUARD | the relation guards (`waits`, `candidates`), LANG-59 shape; plus the laws on the object |
| SUPPORT | a list of `(cell digest, pin digest)` recorded in the candidate (fixed arity, `supportsMax = 8`, like `callsMax`) |
| WITHDRAWAL | a recorded support's cell moving (its entry version bumps): detected by the kernel as `stale` on the next call that re-cites the pin |
| REPAIR | `select` another candidate whose supports are current, or `rejudge` writing `suspended obligation` |

### 3.2 The ACTIVITY: a package method that may SUSPEND

**Shape (Lang, a generator `Std.activity` beside `quorum`/`windowed`/`machine`, LANG-20's library).** Given
`S` (the state record), `states`, `initial`, `edges`, and a list of plans `(label, planTy, respTy, K)`:

1. The state gains the machine field `phase : stateTy (states ++ waiting_<plan> ...)` (`Lang/Std.lean:299`).
2. A relation `waits : (notBefore nat)(agent digest) -> rec {plan : sum plans, captured : K, dispatched : bool,
   answered : optTy (sum resps)}`, `limit` declared, `retract true`, guard `waiting` (below).
3. For each plan `p`: a method `resume_p {notBefore, agent, response : respTy p}` that reads NO row (LANG-58 ROOT
   Q2: "no row read in any method"; the signer pins the row, the guard sees it as `old`), upserts
   `waits[k].answered := some (inj p response)`, retracts nothing, and `case response` of ... each arm computing
   the new state and the machine edge; the author writes the arms. The generated machine law refuses an edge not
   declared (`Std.stepTo`, LANG-43/53).
4. The suspending method `start_p {args}` inserts `waits[k]` with `k = (req.notBefore, req.agent)` (LANG-58's
   key: commutes, orders by admission within `windowMax`) and steps to `waiting_p`.
5. Guard `waiting`: `insert: agent = ringer-of-key ("notYours"), answered none ("answered"), dispatched false`;
   `upsert: old present ("unstarted"), old.answered none ("answered"), new.plan = old.plan ("plan"), new.captured =
   old.captured ("captured") ("a resumption never rewrites what was captured"), answered some ("unanswered")`;
   `retract: old.answered some ("unanswered")` (retire only an answered suspension). This is LANG-59's `rung`
   verbatim with two more equalities. **Exactly-once is one guard on one relation, layer-proof** (LANG-59 as built).

**Who may resume.** The `acceptor` of the plan: for the Bell, the resident (`agent = resident`); for a hole, the
`chooser` (card E). The guard arm reads the field from the object's STATE (`S`) or from the row (`old`), both of
which it sees.

**Required steps and ticks (LANG-64's model, LANG-34's ratio).** A suspension is an ordinary run: its row insert
is growth (`Turn.growth`, charged and conserved, KERNEL-12/15/19; LANG-44 (10)); `captured : K` is bounded by
`valueBytesMax`; the reference derivation counts the run and its extraction (`Derives`, `Need.need`). A resumption
reads one pinned row (the `R` binder, `methodTy S A ks R E es`, `Lang/Package.lean:195`) and the response: its
required steps are the run's; the row read costs the signer one row pin, the kernel one path hash (MEASURED for the
Bell: ring 79/120, answer 96/143 required steps/ticks at LANG-59; `admit hashes-per-row-insert` pinned). **A
suspended activity costs nothing while suspended**: no tick runs, no law runs; its storage is the row's bytes, credited
back on retract (LANG-44 (10)). No new tick kind. Nothing in `Lang/Eval.lean` moves. THE BAR's ratio does not move
(the machine is unchanged; only packages change). ASSUMED: the generated `resume_p` with a `case` of `n` arms costs
about what CoAuthor's `vote` costs (115/166 at LANG-49), not measured.

**The Bell as the first instance (MEASURED against LANG-58/59).** `ring` = `start_ask {text}`; `pending` =
`waits` restricted to `answered = none` (LANG-58 ROOT Q4: the cursor is a relation because a range prefix is exact
match); `rings` = `waits` whole; `answer` = `resume_ask {notBefore, ringText, ringer, text}`; guard `rung` = guard
`waiting`; the resident's `Mem.kept` + volume = the host-side continuation cell (F2). What the Bell LACKS to be
an instance: a `phase` machine field (today `open bool`, LANG-58 state line) and the `plan`/`captured` fields
(today `text` alone is both). The re-cut is a `lang!`: the Bell re-ids, LB0 re-pins ("the Bell became an
activity"), LB rows re-cut, the resident's `Shape.read` reads the new rel line (`Hosting/Resident/Bell.lean:84`
`Shape`; it already reads the description, not a hard-coded layout: "No index, bound or relation layout is written
into the program").

**The IndexedProgram correspondence, exactly.** `Sig.Op i` = the methods enabled at phase `i` (the edges leaving
`i`); `Sig.Resp op` = `respTy p`; `Sig.next op r` = the edge the `case` arm takes; `Program.call op k` = the `waits`
row (the yield) + `resume_p` (the `k`); `Handler.handle` = the signer who answers + the kernel's judge;
`interpret` = the object's `ObjectHistory`; `fold_fusion` = nothing (one carrier); the "program is data, the kernel
judges each resumption" is literal: each resumption is an `invoke` judged by `invoke_next_judged`.

### 3.3 The GUARDED HOLE: a continuation whose resumption is gated, with candidates and reasons retained

**Shape (a generator `Std.hole` composed over `Std.activity`).** Given `V` (the filling's type), the guard clause
over `(old, value, req)` (LANG-48 (2)), `chooser`, `acceptor`, `closes`:

1. The hole is a `waits` row with plan `fill` and `captured = rec {chooser : fillerTy, acceptor : fillerTy,
   closes : nat, selected : optTy digest, accepted : bool}`.
2. A relation `candidates : (hole_nb nat)(hole_agent digest)(cand digest) -> rec {value : V, status : statusTy,
   supports : supportsTy, by : digest, dispatched : bool}` with
   `statusTy = sum {verified : rec {}, suspended : bytes, conflict : bytes, pruned : bytes, uncovered : nat}` (the
   payloads are refusal NAMES or the tick count; law 7) and `supportsTy = rec {s0..s7 : optTy (rec {cell : digest,
   pin : digest})}` (fixed arity, like `callsTy`).
3. Methods: `propose {hole, value, supports}` (inserts a candidate, status `verified` iff the guard clause admits
   the value against the state and `suspended "<why>"` otherwise: the GUARD decides, not the method);
   `prune {hole, cand, reason}` (upsert status `pruned reason`; chooser only); `select {hole, cand, supports}`
   (upsert `waits[hole].captured.selected := some cand`, with `edit.supports = old.supports` enforced by the guard
   AND the call's pins carrying those supports: see below); `accept {hole}` (acceptor only; upsert
   `accepted := true`; this is the resumption of the `fill` plan); `rejudge {hole, cand}` (anyone; re-runs the
   guard clause on the current state and writes the status); `retire`.
4. Guards. `candidates` guard: `insert: by = agent ("notYours"); status is what the clause says ("guard")`;
   `upsert: old present ("unknown"); new.value = old.value ("value") (a candidate's value never changes; propose
   another); status transitions: verified -> pruned|suspended|conflict|uncovered by anyone's rejudge, pruned ->
   verified by rejudge only when the clause admits now ("still pruned")`. `waits` guard (`fill` plan arms): `upsert
   selected: agent = chooser ("notChooser"); the named candidate's status must be verified`: BUT a guard sees one
   edit and one old row of ONE relation (g4), so it cannot read the candidate row. Therefore: **`select` carries the
   candidate's value and supports in its argument, and the signer pins the candidate row; the `candidates` guard
   is not involved; the `waits` guard checks `edit.captured.selected = some cand`; and the KERNEL checks the
   pins.** The fact that makes this sound is `select_cites_supports` (section 4.1): the call's pins include every
   recorded support of the candidate at its recorded pin, so a moved support refuses the select `stale`.

**fill = a typed substitution checked against the guard, Discharges-style.** The install check types `value : V`
(static); `propose`'s guard runs the clause (dynamic); `holeFill_binds_in_circuit`'s twin `pending_fill_binds`
(LANG-48 (6)) says the law admits EXACTLY the fills the shape promised, both directions.

**withdraw = a pinned read going stale.** A candidate's `supports` are pins the proposer observed. The design
makes every later `select` re-cite them (the argument carries them; `derivePins` adds the pins; the kernel's
`touchCheck` refuses `stale` when any moved; BEHIND is final by `stale_behind_forever`). So a withdrawn support
turns a candidate from selectable to unselectable WITHOUT any daemon: nano has no turn without a signer (LANG-45
(2): "closed is a law refusal of late answers, not an event"); the row's `status` is updated by whoever runs
`rejudge`, which is the resident's tick (the Bell pattern: HOSTING-36's `decideTick`), and the status is
advisory: the kernel's pins are the truth. **Derivability = the row's status under its recorded supports;
admission = the select's pins at the current World. Two judges, as P: demands, and as `receive`/`World.admit`
already are.**

**repair = select a surviving candidate, or expose the obligation.** `select` of another `verified` candidate
whose supports are current; else `rejudge` writes `suspended "<the refusal name the kernel or guard gave>"` on the
hole's candidates and the hole stays `open` (LANG-48's `open` arm): no negation is acquired, the hole is not
`refuted` unless a `conflict` is CHECKED (a candidate whose value the guard clause refuses on the current state,
written by the guard itself, never by a method's opinion).

**Polarity.** `chooser` picks `selected`; `acceptor` sets `accepted`. A producer's candidate narrows ITS outputs
(one row); an acceptor's extra demand is a relaw adding a law over `captured` (KERNEL-57: judged over the current
state at adoption, so an adoption that the already-selected candidate violates is REFUSED `law_adopt_refused`:
renegotiation is visible at adoption, experiment 5). An `anyone` chooser is the co-receipt's open offer.

**The executed prefix.** The hole object's `ObjectHistory` is its history; `propose`/`prune`/`select` are judged
steps (`ObjectStep.invoke`); replacing `selected` is one more step; nothing earlier moves (`Chain` is a list).
After `accept`, `dispatched := true` on the hole's `waits` row, and the guard refuses a further `select` until an
`outcome` row exists (`candidates[cand].dispatched = true`, written by the acceptor's resume): the "lose the reply
after dispatch" case can only advance, never re-plan (P: doc 2 section 8's theorem target).

### 3.4 Continuation as a ROW versus a CELL KIND: the price of each (card A)

**Row (chosen).** Kernel statements changed: **0** (LANG-48 "Price. Kernel: zero (a law shape)"; LANG-44 (c)
measured that rows readers alone carry `RowsCanon`, no cell reader gains a premise). Lang: `Std` gains two
generators and their theorems (Std, StdTeeth, StdFits' print bounds); the 85 law theorems and the 24+69
method/package-shape statements are untouched because no type changes (the generators emit at the existing
`methodTy`, `guardTy`, `lawTy`). Flag day: `lang!` only (the Bell and any package using the generators re-id).

**Cell kind `kindContinuation` (refused).** A new `Cell.kind` enters `readKind` (every receiver's kind check),
the three totalities (`effect_at_object` `InvokeTree.lean:795`, `effect_at_grant` `:843`, `object_turn_cases`
`:886`: each gains a case or a premise "the cell is not a continuation"), `admit_kind` (`History.lean:219`),
`ObjectStep` (eight constructors become nine or the lift loses continuations), CODEC's cell tag and every World
vector, `Program.rels` (a continuation cell needs a parent link the trie does not give: LANG-44 (f) "rows as
ordinary cells at hashed ids ... scatter"). MEASURED count of statements naming `kindObject|kindGrant|kindMember`:
not run (read-only lane; LANG-44 (c)'s method applies). ASSUMED: tens of statements, several with a new
premise. Refused on price AND on law 1: rows already are "keyed, bounded things under an object".

**A state SLOT (a third option, refused).** One suspension per object (a `pendingTy` field, LANG-48 (1) as
written): zero kernel price, but one hole per object, every fill conflicts on the cell (LANG-58's finding: "a state
counter makes `ring` write the bell's cell, so two rings over one view collide"), and no candidates. It is the
`once` mode of LANG-48 and stays available for single-slot objects (the escrow's settlement); it is not the
activity.

---

## 4. THE THEOREMS, and what each adds in PREMISES to landed theorems

### 4.1 Conditional soundness: every resumed step is judged

- `resume_judged` (new, Kernel/Proofs/Logic or Lang/Proofs): a signed `invoke obj resume_p args` derived from `w`
  and admitted to `w'`: (i) `invoke_next_judged` (`InvokeNext.lean:529`) gives the laws in force judged
  `old -> new` with `lawsOf X obj cell = .ok laws`; (ii) `object_step_some` gives the run; (iii) LANG-59's
  `guardEdits_never_stuck` + `guard_run_ok` give that the `waits` upsert's guard ran over `(state, req, {edit, old
  row})` and returned `ok`. Statement: the row after the turn reads `answered = some r` AND the guard admitted
  `(old, r)` AND the machine law admitted the edge. **Premises: `X.Lawful`, `X.program = Lang.program ...`** (the
  two every `escrow_*` and the lift already take). **Landed theorems changed: none** (a new statement over landed
  ones).
- `select_cites_supports` (new, the one KERNEL proof lemma): for a `select` call `c` whose argument names
  candidate `cand` with recorded supports `ss`, if `receive X w c = .ok t` and `World.admit ... = .ok w'`, then
  every `(cell, pin) in ss` is in `c.unsigned.pins` (the generated method's argument is read back from the pins:
  `rows_of_pins`, LANG-49's `readsData`; the generator makes the argument's supports equal the pins by the guard's
  equality `edit.supports = old.supports` plus `derivePins`) and `pinOf X.env (w.entry X.env cell) = pin`
  (`admit_pins`). Corollary: **a select admitted at `w` has every support of its candidate current at `w`**.
  Premises: the run facts only. Landed: none.
- `fill_binds` = LANG-48 (6) `pending_fill_binds`, both directions, at `invoke accept`.
- Tooth: `select_without_pins` (the generator with the supports-equality arm removed admits a select whose
  support moved; experiment 1's plant).

### 4.2 Repair correctness: repair agrees with from-scratch

The model is the judge's carried-verdict rule (F6): a verdict is carried only under a byte-identical input key.
The kernel twin is `receive_congr`: the derivation is a function of the pinned view.

- `rejudge_agrees` (new, Lang/Proofs): `rejudge {hole, cand}` run at `w` writes status `verified` iff
  `propose {value, supports}` run at `w` would write `verified`, because both run the same guard clause on the same
  `(state, req, value)` (determinism of `Lang.judge`: it is a function; `judgeOne_ok`). With `receive_congr`: if the
  hole object's cell and the candidate row agree between `w0` (when the status was recorded) and `w` (now), the
  recorded status IS the from-scratch status. **Premises: none new** (`receive_congr`'s one honest premise since
  LANG-49: the two `RowView`s agree).
- `candidate_status_stable` (new): under any World change outside the hole object's cell and the candidate row,
  the recorded status is the from-scratch status (`Indep` of the hole's footprint; `submit_frame`). Premises: none.
- What repair-correctness does NOT say, stated: the status of a candidate whose SUPPORT moved is whatever
  `rejudge` writes; `select` is still refused `stale` whether or not anyone re-judged. The kernel never trusts
  the status. (This is why "a daemon re-judges" is not in the TCB.)

### 4.3 Locality: the boundary is `CallFoot`

- `select_frame` = `submit_frame` instantiated: a `select` pins the hole's cell (`keep`), the `waits` row, the
  candidate row and the supports (all `keep` but the `waits` row); its `CallFoot` is those; any assertion
  `Indep` of them survives. **Premises: none** (`submit_frame` takes only the run).
- `holes_commute` = `admit_comm` (LANG-44 (11), built): two `propose`s to different holes, or two `select`s of
  different holes under one object, land in either order to equal rows and cells roots (LANG-49 MEASURED: LT7c,
  LS10c for the Bell/CoAuthor instances). Two `select`s of ONE hole: the second is `stale` on the `waits` row
  (LS11's shape). Premises: `admit_comm`'s (disjoint footprints; the order laws for rows, KERNEL-54 as built).
- The boundary theorem P: asks for ("every reusable boundary declares the observations it preserves"): in nano
  the declaration is the PIN. A consumer that pins the hole's `waits` row preserves "the row's bytes"; one that
  pins only the hole's exported `value` row (card B) preserves "the selected value". Nothing weaker is
  expressible, and nothing weaker should be (a weakened pin is item 2 of the pause list).

### 4.4 `interp_runs` generalised from the resident to any activity

- Host side (already landed, F1): any `Prog` the resident builds is performed exactly as a path.
- Kernel side (already landed, F3 + StdChain): `object_history_chain` gives the hole object's history as a
  `Std.Chain (Step [] machineLaw)`; `machine_reached` (`StdChain.lean:100`) gives every reached phase
  `Reach edges initial`; `chain_count` (`Chain.lean:136`) gives at most one `accept` per hole (mark = the
  `accept` step; `Stop` = `accepted = true`, from which the guard admits no further select: `chain_stops`).
  **Statement to add:** `activity_history_is_path`: for a `Std.activity` object, the judged steps of its history
  are a path of its declared machine, with each resumption's edge the one its response arm names. Proof: the lift
  + `machine_reached` + the generated `stepLaw`'s meaning theorem (`Lang/Proofs/Std`'s `machine_*`, LANG-43/53).
  **Premises: the lift's** (`X.Lawful`, `Lang.program`, the machine law in force at every judged step, a live
  start). Landed: none.
- The two sides meet at the Bell: the resident's `invoke` nodes (`tick_counts`: at most one, of the kept answer)
  are the kernel's `resume_ask` steps. A theorem joining them ("every `answered` row was the text of some tick's
  kept answer") would need the member-socket model, which no proof has; it stays a journey row (LB4/LB7 +
  resident_bell), stated as such.

### 4.5 The premise spread, enumerated (PRICE-PREMISES)

| landed family | statements | premise added by the rows design | by the cell-kind design |
|---|---|---|---|
| Kernel cell readers (`admit_frame`, `rom_keep`, `admit_rom`, `admit_nullifiers`, `admit_live`, Value/Ledger sums, Rooted) | ~150 (LANG-44 (c), KERNEL-41's count) | **0** | 0 (a kind is a value field) but see totalities |
| the three totalities + `admit_kind` + `ObjectStep`/`ObjectHistory` consumers | `effect_at_object`, `effect_at_grant`, `object_turn_cases`, `admit_kind`, `object_history_of_audit`, `escrow_invokes_one_payout(_deployed)` | **0** | each gains a case; `escrow_*` restate (ROOT for LEDGER) |
| rows readers (`RowsCanon` family, `admit_comm_rows`, `rows_ext`, range theorems) | per KERNEL-54 as built: 73 changed statements that day | **0** (no row shape changes; new relations are data) | 0 |
| Lang law theorems (Std, StdTeeth, Receiver, LawRun, StdFits) | 85 | **0** (new generators add theorems; `lawTy` unchanged) | 0 |
| Lang method/package-shape statements | 24 + 69 (LANG-44 (c)) | **0** (`methodTy` unchanged since LANG-49) | 0 |
| Hosting resident proofs (`tick_order`, `tick_counts`, `kept_follows`, volume) | ~40 | **0** if the Bell's `answer` keeps its argument type `answerArgTy` (`Bell.lean:73`); if the resume argument gains `plan`, `Shape.read`/`answerArg` restate (Hosting's, ASSUMED ~6 statements) | same |
| Protocol (`Command`, `Settle`, `Attempt`) | | **0** (`derivePins` already pins rows; LANG-58 ROOT Q2) | 0 |
| Codec vectors | | **0** unless the package wire gains a node; the generators emit existing shapes | `kernel/cell` tag, every World vector |

Totals: rows design **0 premises on landed theorems, 0 statements restated** outside Hosting's ASSUMED ~6 if the
Bell's argument type changes (avoidable: keep `answerArgTy` and add `plan` to the ROW, not the argument). The cell
kind design: ASSUMED tens of statements and a kernel flag day. The measurement a lane makes before any code: `grep`
the statements naming `answerArgTy`/`Shape` in `Hosting/Proofs`, and the statements naming `kindObject` in
`Kernel/Proofs` (for the record of why the kind was refused).

---

## 5. WHAT RE-GENESES, WHAT REFUSES, WHAT MINI DIVERGENCE NANO REVERSES

**Flag day: `lang!`, no `kernel!`.** The Bell re-ids (new relations and methods; LB0's byte-identity row re-pins
with the reason "the Bell became an activity"); `world/resident/Bell(.ob)` re-emits; LB rows re-cut (LB0-LB13 +
new); `launcher/tests/resident_bell.rs` and `Hosting/Resident/Bell.lean`'s `Shape.read` cut over in the same commit
(HOSTING-11's pattern). The wire: nothing moves (`lang/package/2` unchanged; no new node). Vectors: none. Stores:
no re-genesis required; an old Bell object's state does not read at the new state type (as at LANG-58), and the
operator re-creates the Bell (OPS). Every Store re-geneses anyway at the next `kernel!`.

**What refuses now, by name.** A resume without its row pinned: `rowUnpinned` (before any guard; LANG-59). A second
resume: `waiting: answered`. A resume that rewrites the captured context: `waiting: captured`. A resume by the wrong
party: `waiting: notChooser` / `notAcceptor`. A select of a candidate whose support moved: `stale` (declined,
BEHIND final from the fold). A select after dispatch: `waiting: dispatched`. A candidate whose value the clause
refuses: inserted with `suspended "<reason>"` (never silently dropped; a reader sees why). A relaw that the
selected candidate violates: `lawDenied <law> <reason>` at adoption (KERNEL-57). A fill past `closes`:
`waiting: closed` (the guard reads `req.validUntil ≤ closes`, LANG-48 (4)). A 769th row: `relationFull`.

**Mini's deliberate divergences, and which nano keeps reversed.**
- Call-by-value / `let`-eager STAYS (LANG-45 measured `let`-shared continuations evaluate eagerly; the demand
  machine's budget theorems reach no thunk). A continuation is DATA the author names (`captured : K`), never a
  heap checkpoint. What this costs: the author must choose what to capture (mini captured the whole demand state);
  what it buys: `valueBytesMax` bounds it, extraction's meaning theorem covers it (`runMeasured_means`), nothing is
  typed by a `stored_checkpoints_typed` invariant because nothing is stored but typed data.
- `perform` STAYS OUT of the term language (LANG-6). A method is pure; suspension is a ROW EDIT. Mini's
  `perform_under_update_refused`/`sharedEffect` class of refusals has no nano twin because there is nothing to
  refuse.
- Reflection STAYS OUT (`metadata`/`reflect`, M:`docs/OBJECTIVE-BEND.md` "Specification metadata"): a nano package
  cannot inspect a term. P:'s "repair machinery can inspect derivations" lands on the RESIDENT (host side: it reads
  rows and descriptions, `read OBJ ?`), never on a method. That is the Contextual MetaML point (clients see a
  behavioural contract; the analyser sees the syntax) with the analyser outside the TCB.
- Mini's `Activity<P,R,A>` TYPE, the `await` Plan with `patience`, `AnswerSlot`, the checkpoint tariff, `abandon`,
  `exhaust` (M:`docs/OBJECTIVE-BEND.md:459-530`): not reproduced. `patience` = `closes`; `abandon` = `retire` past
  `closes` by anyone; `exhaust` = the kernel's `ticks` refusal (LANG-64: refused before it walks); `topUp` = nothing
  (no purse; the signer pays each turn).
- Mini's upgrade/drain/migrate: not reproduced (a package is ROM). The nano move is relaw/adopt on the same package
  (KERNEL-57), and a new package is a new object. Experiment 5 lives there.
- Mini's `Hyperedge` multi-signer turn: out (charter 3; MINI-CONCEPTS section 4). The two-cell negotiation is two
  members, one writer.

---

## 6. THE EIGHT EXPERIMENTS as nano rows (lang-journey LH0-LH9), with plants and the theorem each exercises

Fixture: a hole object `H` (package `Std.hole` over `V = nat`, clause `value ≤ old.cap`, chooser = member A,
acceptor = member B, `closes` = h + 500); two support objects `G1`, `G2` (data objects A writes); candidates
`c1` (value 5, supports `[G1@pin1, G2@pin2]`), `c2` (value 7, supports `[G2@pin2]`), `c3` (value 50, pruned:
`cap = 10`). Every row ends with the `read H ?` description line and a `rows --deployed` byte check where it applies.

| row | the experiment (P: doc 1 section 9) | nano steps | expected, by name | theorem exercised | plant (the row goes RED) |
|---|---|---|---|---|---|
| LH0 | byte identity of the fixture | install `Std.hole`'s core text; `read H ?` | the description line; package bytes pinned | `print_parse` round trip (LANG-29) | one byte of the core |
| LH1 | withdraw one of two supports | A writes `G1`; A `select c1` (pins `G1@pin1`): refused; A `select c2`: admitted | `declined stale` (BEHIND from A's fold: `refused` at settle); then `ok` | `select_cites_supports`, `stale_refused`, `stale_behind_forever` | remove the `edit.supports = old.supports` guard arm: `select c1` is `ok` on a moved support |
| LH2 | withdraw the last known support | A writes `G2`; `select c2` refused; anyone `rejudge H c1`, `rejudge H c2`: both `suspended "stale"`; `read H` shows `open`, no `conflict` | `declined stale`; statuses `suspended`; no negation | `rejudge_agrees`, LANG-48's `open` arm | a `rejudge` that writes `conflict` on a stale support: the guard refuses it `candidates: conflictNeedsCheck` (the conflict arm is writable only by the clause's own refusal) |
| LH3 | withdraw a pruning reason | `c3` was `pruned "cap"`; A `relaw` adds `bounded cap ≤ 100` and writes `cap := 60`; `rejudge H c3`: `verified`; `select c3`: `ok` | `pruned` -> `verified` -> selected | `law_judged` (the relaw judged; the adopted law judges the state), `rejudge_agrees` | the generator's `pruned -> verified` arm removed: `rejudge` refused `candidates: still pruned` |
| LH4 | a cycle losing its grounding | hole `H2` whose candidate `d1` supports `[H.waits@pinH]`; `H`'s `c1` supports `[H2.waits@pinH2, G1@pin1]`; A writes `G1`; A `select` on `H2` citing `d1`: **admitted** (its one support, H's row, did not move) | `ok` — the row documents the REFUTATION of one-level supports; under card F's ruling (forbid hole-supports-hole) the `propose d1` is refused `candidates: supportIsHole` and LH4 reads that refusal instead | `select_cites_supports` (shows exactly what it does NOT cover) | n/a: the row IS the plant until card F lands; after it, the plant is the generator admitting a hole-typed support |
| LH5 | a dependent-context change | B `relaw` adds `bounded value ≤ 6` while `selected = c2` (value 7): refused at adoption; with `selected = c1` (value 5): admitted; then `select c2`: `lawDenied bounded "value"` | `lawDenied` at adoption, naming the law; then the select refused by the new law | `law_adopt_refused` (KERNEL-57), `bounded_adopt` (StdTeeth) | KERNEL-57's own plant: adopt judged over an empty state |
| LH6 | replace a filling preserving its contract | consumer object `C` pins `H.value` (card B's exported row: `value : (hole key) -> rec {v : nat}`, upserted only when `selected`'s value changes); A `select c2'` (value 5, another provenance): `C`'s plan (pinning `H.value`) still admitted; A `select c2` (value 7): `C`'s plan `stale` | the consumer survives a same-value replacement and is refused on a value change | `admit_comm` / `submit_frame` at `C`'s pins; **ASSUMED** that an upsert with identical bytes leaves the row leaf's version unchanged (KERNEL-54 N bumps per WRITE; `postWrite` for cells skips when `diffOps` is empty, `writeOf` keeps; for rows: not read, MEASURE FIRST) | if the version bumps on an identical upsert, the row is RED by design: it then reads "a same-value replacement is a withdrawal", and card B's lean changes |
| LH7 | correctness kept, a cost bound lost | candidate `c4` whose clause run (the author's clause does a `cat` of two 64 KiB captured strings) exceeds `lawTicks`: `propose c4` inserted with status `uncovered 2048`; `rejudge` after a relaw that shortens the clause: `verified` | two statuses: the guard never says `refused`; the budget says `uncovered n` | `law_walks_le`, `cat64_price` (LANG-64), `fault_never_admits` (a faulting law has no step) | the `uncovered` arm removed: the propose is refused `ticks` outright and the candidate is LOST (no row), which is the defect the arm exists to prevent |
| LH8 | re-apply an earlier filling | after LH1 (`c2` selected), `G1` restored to its old bytes: `pinOf` of `G1` is NOT `pin1` again (the version moved: KERNEL-54 amendment 1, `pinOf_old_recurs` is the tooth for the old pin); A `propose c1'` (same value, supports `[G1@pin1', G2@pin2]`): `verified`; `select c1'`: `ok`; `read H candidates` lists `c1` (suspended), `c1'` (verified), `c2` (verified) | re-application is a NEW candidate under new pins; the old candidate row is retained, never retracted | `pinOf_old_recurs` (what makes the old support unusable), `chain_count` (one accept) | retract candidates on deselect: `c1`'s row gone, `read` cannot show why it was set aside |
| LH9 | the first integration experiment (P: doc 3): two members negotiate a one-use capability, alternative providers, a deadline, a cancellation path | `H` with `closes`; providers P1, P2 each `propose` (supports: their own grant cell `grantP1@pin`); the operator REVOKES P1's grant (unrelated state update first: `G1` written, `select P2` still `ok`); `select P1`: `stale`; B `accept` (dispatch: `dispatched := true`, the capability's nullifier spent via the emitted `transfer ... once`); a second `accept`: `waiting: answered`; past `closes`: `retire` by anyone | each of the four changes names its operation: unrelated write = frame; revocation = stale support; representation change = n/a on nano (no proof objects; state it); replay = `waiting: answered` + the nullifier | `submit_frame`, `select_cites_supports`, `rotate_stales_outstanding`'s shape for revoke (a `revoke_stales_supports` corollary: a revoked grant's cell is retired, its pin moves), `chain_count`, `checkNullifiers` | the `dispatched` guard arm removed: a second `select` after `accept` admitted, the capability promised twice |

Each row prints its required steps/ticks (LANG-34's row); the Bell's LB rows stay beside them as the activity
instance. The plants are by hand in a lane log (HOSTING-36's method: "the proof goes RED ... the row goes RED").

---

## 7. DECISION CARDS for Ember

### Card A. The continuation's representation: ROW under the object vs CELL KIND vs STATE SLOT
- OPTIONS: (1) a `waits` row (LANG-44/49 rows, LANG-48 (8)); (2) `kindContinuation` cell; (3) a `pendingTy` state field.
- PREMISES ADDED: (1) **0** kernel, 0 Lang statements restated; (2) the three totalities + `admit_kind` +
  `ObjectStep` gain a case, LEDGER's `escrow_invokes_*` restate, a `kernel!` flag day with every World vector;
  (3) 0, but one suspension per object and every fill conflicts on the cell (LANG-58's measured refutation).
- PRIOR ART: the Bell (LANG-58/59) IS (1) built; mini's `AnswerSlot`/awaiting record is (2) at kernel coordinates
  ≥ 2^256 (M:`docs/OBJECTIVE-BEND.md:419`); breadstuffs' `EventualRef` slot is (3).
- ROOT'S LEAN: (1).
- RULING: **a continuation is a row; (3) stays as `Std.pending once` for single-slot objects; (2) is refused.**

### Card B. The hole's representation: an object vs relation rows; and the exported `value` row
- OPTIONS: (1) one object per hole (a `Std.hole` package instance per hole); (2) holes as rows under one object
  (`waits` + `candidates`), many holes per object, commuting; (3) (2) plus a third relation `value` holding only
  the selected value, for consumers to pin.
- PREMISES ADDED: (1) 0 but every hole is a `create` (a cell, ~13.7 hashes, a package pin, no commutation between
  holes of one market); (2) 0; (3) 0, plus the ASSUMED row-version fact LH6 measures.
- PRIOR ART: LANG-48 (8) ("an `open` slot can be a ROW keyed by its requester ... fills of different slots commute");
  mini's `ObserverLens.dependencies` as a declared sufficient dependency set (M:`CanonicalReactiveView.lean:46`):
  the `value` row is the nano way to declare "I depend on the value, not the provenance".
- ROOT'S LEAN: (3), with LH6 measured before the `value` relation is kept (if an identical upsert bumps the
  version, (3) buys nothing and the generator omits it).
- RULING: **rows; one object may hold many holes; the `value` relation is kept iff LH6 reads green.**

### Card C. fill / withdraw / repair: kernel receivers vs Lang methods
- OPTIONS: (1) three new `Body` constructors (`fill`, `withdraw`, `repair`); (2) package methods generated by
  `Std.hole`, judged by relation guards and laws; withdrawal is the kernel's existing `stale`.
- PREMISES ADDED: (1) `Body` gains constructors: `dispatch`, `derive`, the receiver census (PROTOCOL's
  `every_op_has_a_row`), `effect_at_object`'s "every other receiver writes a cell it read as ..." gains three
  cases, codec tags, the op table (target ≤ 40 ops); a `kernel!`. (2) **0**: `invoke` is the receiver; the one new
  proof is `select_cites_supports`, a corollary over the generated method + `admit_pins`.
- PRIOR ART: KERNEL-60's cancel record is a receiver because it must be SIGNED BY THE MEMBER and judged by
  `World.refuse` (a system interaction); a fill is an object's business, judged by its laws, like every method.
  LANG-48 alternative (a) refused a kernel `HoleSpec` as a second shape.
- ROOT'S LEAN: (2).
- RULING: **methods; withdrawal is `stale`; no new receiver.**

### Card D. The tick model for a suspension and a resumption
- OPTIONS: (1) no new tick kind: a suspension and a resumption are runs priced by LANG-64 (ticks per word) and
  LANG-34 (required steps = the reference derivation), the row's bytes as growth; (2) a storage deposit per
  suspended row refunded at retract (mini's `storageDeposit`); (3) a "wake" fee paid by the resumer to the suspender.
- PREMISES ADDED: (1) 0; (2) 0 kernel (growth is already charged and credited back on retract, LANG-44 (10)), so
  (2) is (1) under another name; (3) a value move per resume: a `transfer` call in the generated method, LEDGER's
  theorems unchanged, but a purse per activity (mini's) is a second ledger shape (law 1).
- PRIOR ART: LANG-64 (`walked_le`, pay-before-walk); KERNEL-12 (`charge = weight`); mini's tariff
  (`refund_measurement_free`: no fee depends on measured work), which nano already obeys by charging the bound.
- ROOT'S LEAN: (1).
- RULING: **no new tick kind; a suspended activity costs its row's bytes and nothing else; the signer of each
  turn pays that turn.**

### Card E. Polarity's encoding: who chooses, who must accept
- OPTIONS: (1) `chooser`/`acceptor : fillerTy = sum {anyone, member digest}` in the hole row's `captured`,
  enforced by guard arms (`select: agent = chooser`, `accept: agent = acceptor`); (2) grants: `Right.invoke
  select`/`Right.invoke accept` carved to the parties (KERNEL-20/25); (3) both.
- PREMISES ADDED: (1) 0; (2) 0 (grants exist); (3) 0.
- PRIOR ART: the Bell's `notYours`/`notResident` arms (LANG-59); LANG-48's `fillerTy`; `Req.agent` vs
  `Req.principal` (object-as-grantee, LANG-21); interface automata's input/output variance (P: doc 2 section 5):
  the producer's candidate is an OUTPUT (its row), the acceptor's demand is an INPUT guard (a law).
- ROOT'S LEAN: (3): the row says WHO (data a reader sees in `read H ?`), the grant says MAY (authority the kernel
  walks); an `anyone` chooser is the open offer.
- RULING: **fields in the row, enforced by the guard; grants for delegation; a party's narrowing is a relaw
  judged at adoption (KERNEL-57), so renegotiation is visible.**

### Card F. Supports: one level, forbid hole-supports-hole, or close transitively (experiment 4)
- OPTIONS: (1) one level (a support is any cell at a pin); the cycle experiment refutes it; (2) a support may not
  be a `waits` row of a hole (the generator refuses `candidates: supportIsHole` at propose: a support is a DATA or
  value cell, or a grant); (3) a candidate's supports include the transitive closure through holes to depth
  `callDepthMax` = 4, computed by the client (`derivePins`-style) and checked by the guard's equality.
- PREMISES ADDED: (1) 0 and wrong; (2) 0; (3) 0 kernel, but `supportsMax` grows (8 -> 8 x 4 pins per candidate:
  `touchesMax` pressure; LANG-44 critique (2): the client must plan the closure).
- PRIOR ART: de Kleer 1986's unrecorded control decisions; the invoke tree's `callDepthMax` and `revisited`
  refusal (LANG-21: re-entry refused by name) are nano's bounded-closure precedent; GATES-22 (3)'s attribution over
  read-sets is one level too, and GATES-20d records that a warm cargo's read-set hides the probe paths: the same
  blind spot, named.
- ROOT'S LEAN: (2) now; (3) when a journey needs a hole to support a hole (a market whose offers cite other
  offers), as its own `lang!` with the closure measured.
- RULING: **(2): a support is never a hole's row; LH4 reads the refusal; (3) is a dated item with the trigger
  "a row that needs a hole to cite a hole".**

### The one-day build order (one kernel+Lang redesign day; lanes and dependencies)

| lane | prefix | does | depends on | gate |
|---|---|---|---|---|
| LANG-A | `lang!` | `Std.activity`: machine + `waits` + `resume_<plan>` generator; theorems `activity_*` in Std/StdTeeth/StdFits; `activity_history_is_path` over the lift; the Bell re-cut as the instance (`world/resident/Bell.ob` re-emit, LB rows re-cut, `Shape.read` + resident_bell cut over, HOSTING-11's pattern, ROOT for HOSTING) | nothing (rows landed LANG-49, guards LANG-59, machine LANG-43/53) | LB0-LB13 green; `tick_order`/`tick_counts` unchanged in statement (MEASURE the Hosting spread first: grep `answerArgTy`) |
| LANG-B | `lang!` | `Std.hole`: `candidates` + status sum + supports; `propose/prune/select/accept/rejudge/retire`; `pending_fill_binds` (LANG-48 (6)); `rejudge_agrees`, `candidate_status_stable`; card F (2) in the generator | LANG-A (the hole is an activity with plan `fill`) | LH0-LH3, LH5, LH7, LH8 green; plants logged |
| KERNEL-P | `kernel:` (proof-only) | `select_cites_supports` (over `admit_pins` + the generated argument read-back) and `revoke_stales_supports` (a revoked grant's cell retires, so a candidate citing it is `stale`: `rotate_stales_outstanding`'s shape); no deployed check changes | LANG-B's generated method shape (its argument/row equality) | second-agent statement read with the disjunct check (KERNEL-56's rule); 0 landed premises |
| PROTOCOL-R | `protocol:` | journey rows LH0-LH9 as `members` rows (`Protocol/Rows.lean`), the LH6 version measurement FIRST (a `kernel:` note to KERNEL on the row-version fact), LH9 with two members and a revoke | LANG-B | rows green; `every_op_has_a_row` unchanged (no new op) |
| LEDGER-E | `ledger:` | the escrow's settlement restated as `Std.pending once` (LANG-48 (7)); `escrow_absorbing`/`escrow_one_payout` as corollaries of `pending_fill_binds` | LANG-B | E rows green; `ledger-sim --write-text` re-emit |
| GATES | none | nothing: a `world/` text selects every row (GATES-19 (0)); the convergence runs them | | |

Order: LANG-A and KERNEL-P's statement drafting in parallel (KERNEL-P reads LANG-A's generated shape); LANG-B after
A; PROTOCOL-R and LEDGER-E after B. One landing per lane, fast-judged (GATES-22); the convergence judges the
system. What re-emits: Bell(.ob), Escrow; what re-ids: both plus any package using the generators. What refuses:
section 5's list. Nothing re-geneses by necessity; the operator re-creates the Bell object (OPS RUNBOOK line).

---

## 8. What I would not do, and why (the critique of this document)

- **Not a kernel `HoleSpec`, not an `Activity` type.** Both are second shapes of things nano has (a law over
  pending state; a package with a machine). Law 1.
- **Not automatic withdrawal propagation.** A daemon that re-judges every candidate when a cell moves is O(store)
  on the request path (law 5) and a second truth beside the pins. The kernel's `stale` is the truth; `rejudge` is
  advisory and pull-driven (the resident's tick).
- **Not transitive supports in v0** (card F): the closure is the client's to plan, and no row needs it yet.
- **Not Pumpkin-Pi transport.** There is nothing to transport: a candidate is data, re-judged.
- **The weakest claim here** is LH6's ASSUMED row-version behaviour; it is the first thing a lane measures.
- **The strongest claim** is the zero-premise price of the rows design; it rests on LANG-48's "Kernel: zero" and
  LANG-44 (c)'s enumeration (both READ), and on no type changing (`methodTy`, `guardTy`, `lawTy` unchanged), which
  a lane verifies by the statement diff before landing (KERNEL-54's method).
- **Meta-critique.** I was briefed with "IndexedProgram's shape as a kernel receiver"; the independent test was to
  ask what the kernel would gain by a receiver that `invoke` does not already give, and the answer was nothing but
  a `kernel!`. I was also pulled toward the GATES judge as THE ATMS because it is the richest TMS in the tree; the
  honest reading is that it is the model for repair-CORRECTNESS (carried verdicts), while the kernel's pins are
  the model for SUPPORT, and the two are different objects in P: too.

---

## 9. PROTOTYPE (lane, nothing landed): what was built, what it showed, what the adversarial read corrected

Lane worktree: `/tank/dregg-build/claude-lanes/activities` (hbox; nanodregg `744d00c`; a `git worktree add`, warm
`.lake` copied from the standing tree; no `scripts/commit`, no `wt/*` touched). Files (all MEASURED by running):

- `/tank/dregg-build/claude-lanes/activities/world/hole/Hole.ob` — the hole as a surface package (6,673 chars;
  34,865 package bytes): one hole per object; relations `candidates` (value, status sum `pruned bytes | suspended
  bytes | verified`, two optional supports `(cell, pin)`, by) and `facts` (assumption TOKENS: `(cell) -> (by, pin)`,
  posted / re-pinned / withdrawn only by their poster); methods `post repin unpost propose prune select accept`;
  guards `proposed` (the status is the clause's, not the author's; only the chooser prunes; value and author never
  change) and `posted`; law `shape` (cap, chooser, acceptor, closes never move on an invoke).
- `/tank/dregg-build/claude-lanes/activities/Lang/JourneyHole.lean` + a `lang-hole` exe entry in the lane's
  lakefile — rows LH0–LH12 through the REAL receivers (`Receive.submit`), the Sim's toy parameters, follower and
  auditor at the end. Output: `lane-logs/lang-hole.out`; plant: `lane-logs/plant-pin-equality.out`.

**Result: `lang-hole: GREEN`, 13 turns, follower and auditor reach the Host's World.** The row that is
experiment 1: B re-pins fact f1 (an assumption token MOVES: LH6, admitted); A selects c1, which recorded f1@p1:
`refused program "select: refused support0 moved"` (LH7); the same select signed over the view BEFORE the re-pin:
the same refusal (LH7b; the method reads the row as it is, LANG-59 critique (1), so the kernel's `stale` stands
behind the name and is not reached); on a scratch World where B WITHDRAWS f1 (retract): `select: refused support0
withdrawn` (LH7c); A selects c2, whose one support f2@p2 stands: admitted, 139 required steps / 179 ticks (LH8) —
the judgment survives through the other support. B accepts (LH9); a select after acceptance is `select: refused
accepted` (LH9b); B withdraws f2 after acceptance and the selection stands (LH10: the executed prefix does not
move); c3 (value 50 past the cap) was INSERTED with `suspended "cap"`, never dropped (LH5c); A prunes c1 naming
why and the three candidates read back with their reasons (LH11). PLANT (by hand): the two `(deq v.pin s.pin)`
equalities removed from `select` — LH7 flips to ADMITTED (155 / 197), and LH7b, the select signed over the
pre-withdrawal view, flips to **`rejected stale`: the KERNEL's row-pin check, reached exactly when the method's
check is absent**; `lang-hole` reads RED; restored, GREEN (`lane-logs/plant-pin-equality.out`). So a withdrawn
support is refused twice over: by the method's comparison of the recorded pin against the row as the World holds
it (by name, first), and behind it by the kernel's `stale` on the signer's row pin (final when BEHIND, KERNEL-54).
Derivability and admission are two judges, measured.

**Corrections from the adversarial read of this document (REVIEWER-ACTIVITIES, 14 findings, all READ at source),
each of which the prototype already obeys or which changes a section above:**

1. HIGH. A method NEVER sees its call's cell pins (`Lang/Program.lean:288-301`: env = [req, args, state, rows];
   `reqOf` carries no pins), and rows are read under `self` only (`Program.lean:299`, LANG-49). `rows_of_pins` does
   not exist as a theorem. So section 3.3's "a candidate's supports are pins on OTHER cells, re-cited by `select`"
   and section 4.1's `select_cites_supports` as stated are UNPROVABLE: nothing ties an argument to
   `c.unsigned.pins`. **Restated:** a support is a ROW UNDER THE HOLE OBJECT (an assumption token its owner posts,
   re-pins, withdraws), and `select` point-reads it; the kernel's row pin makes the read current and the method
   compares the recorded `(cell, pin)` to the row's value. That is what `Hole.ob` does, and LH7/7b/7c are its
   measurement. A support on another object's cell is checkable only through a nested invoke of a method of that
   object that refuses when its state differs (by value, one level down). Sections 3.3, 4.1, 6 (LH1, LH9) and
   card F read with this restatement.
2. HIGH. `relaw`/`adopt` on a PROGRAMMED object is refused `hasMethods` (`Derive.lean:145-175`); laws judge state
   slots, never rows. So experiments 3 and 5 as "a relaw narrows the guard" (sections 1.3, 3.3, 5, LH3, LH5, card E)
   are impossible as written. **Restated:** a pruning reason or a guard parameter is STATE the chooser changes by a
   method (`setCap`); adoption-time refusal (KERNEL-57) is available only on data objects.
3. HIGH. `admit_comm` (`Kernel/Proofs/RowsComm.lean:791`) requires `InsOnly` row touches and no ranges; a `select`
   upserts and point-reads (a `keep` row touch), so `holes_commute = admit_comm` (section 4.3) holds only for pure
   `propose`s. Commuting selects is new kernel proof work. LT7c/LS10c are measurements, not instances.
4. HIGH. A machine `phase` field in STATE (section 3.2 items 1, 3, 4) makes every suspension write the object's
   cell: LANG-58's own refutation, which card A cites against option (3). **Restated:** the phase lives in the
   `waits` row, or an activity is one suspension per object. The prototype has no phase field.
5. HIGH. `chain_count`/`object_history_chain` see state only, never rows; "at most one accept per hole" (section
   4.4) is the guard's fact (LANG-59's `rung` shape) plus row versions, not a chain theorem.
6. HIGH. A guard returns `ok | refused`; a refusal refuses the whole call, so "the GUARD decides the status" and an
   `uncovered n` status written on tick exhaustion (sections 3.3, 6 LH7) cannot be built: no term observes its own
   exhaustion (`fault_never_admits`). **As built:** the METHOD computes the status from the clause and the guard
   RE-CHECKS it (`proposed`'s arms; LH5c, LH5d). `uncovered` is dropped from the status sum.
7. HIGH (LH6's ASSUMED fact, now MEASURED by the reviewer at `Kernel/World.lean:~1251-1256`): a row upsert bumps
   the leaf version `u + 1` whatever the bytes (cells differ: `writeOf` emits `keep` on an empty `diffOps`). So
   card B (3)'s exported `value` row works only if the generator SKIPS the upsert when the value is unchanged (it
   can: `select` point-reads its own `value` row). A consumer's dependency is its own voluntary row pin, which also
   pins the hole's cell.
8. HIGH. Card F (2) "a support is never a hole's row" cannot be enforced by digest (a method cannot tell what a
   digest names); with supports restricted to self-rows (finding 1) the generator checks the RELATION INDEX. The
   cycle refutation (LH4) stands.
9. MEDIUM. `machine_reached` + the lift gives "every reached phase is reachable" with the premises of
   `object_history_chain` (`X.Lawful`, `Lang.program`, the law in force at every judged step, `NoRef` and `IsLaw`
   of `machineLaw`: both landed, `Receiver.lean:340,362`), NOT "each resumption took the edge its response arm
   names": `stepTarget` takes the FIRST edge and cannot depend on the response. Section 1.5's "interp_runs for any
   activity" is overstated to that extent; the response-dependent part is author code covered by no landed theorem.
10. MEDIUM. `CallFoot`/`Indep`/`submit_frame` cover the CELLS trie only (`Triple.lean:17-18`); `receive_congr`
    takes equal origins, agreeing pinned cells AND equal `rowView`s. "Premises: none" in 4.2/4.3 is wrong by those.
11. MEDIUM. The 0-premise table (4.5) omits LEDGER's `escrow_absorbing`/`escrow_one_payout` restatement (named by
    LANG-48 itself and by this document's LEDGER-E lane), the `Lang/Proofs/Rel` guard family, the `stepTo_*` family,
    and `RowsCanon` on new row-reading conclusions. The price stays zero only under finding 1's restatement; exposing
    pins to methods would be a `reqTy`/`methodTy` change restating the 24 + 69 (+85) statements.
12. MEDIUM. `select` can READ the candidate row (it is under `self`), so the candidate's status and supports need not
    travel in the argument; the prototype reads them (`rows.candidates.p0`).
13. MEDIUM (vacuity). `rejudge_agrees` as "rejudge writes verified iff propose would" is near `P ↔ P`: state it as
    "the status equals the clause's meaning on the current state". `select_without_pins` removes an arm the `waits`
    row does not have: a falsifier that cannot falsify; the real plant is the one run above (the `pin` equality).
    Every "support current since w₀" corollary carries `CollidesAmong hash S` over an explicit list (KERNEL-56).
14. LOW. Citation drift: `Std.machine` is at `Lang/Std.lean:355` (`stepTo` :366); `admit_kind` is private; the
    durability proofs are in `Hosting/Proofs/ResidentVolume.lean`; LANG-48 reads PROPOSED in `lang.md:1609` and its
    approval is in `docs/record/DREDGE-20261021.md:19`, as `once` only; g4's attribution should cite LANG-59 (it
    superseded LANG-49 critique (3)); section 3.2 item 3 ("reads NO row") contradicts its cost paragraph.

**What the prototype is, and is not (Ember's critique, 10-22).** It is the operational witness that nano's
receivers, rows and guards can carry a hole whose candidates are retained with their reasons and whose supports are
withdrawable assumption tokens. It is NOT the theory the proposal describes: contextual modal types `[Ψ ⊢ A]`,
metavariables with explicit and first-class substitutions, derivability versus availability as judgments, the
strengthening factorization `t ≡ t₀[π]`, the four typed repair outcomes, blocked inspection of an unresolved
metavariable, the stability class of a guard under substitution. None of that is in Lean anywhere in nano, mini or
breadstuffs beyond breadstuffs' prose study (`docs/GUARDED-HOLES-METATHEORY.md` §1c names CMTT and builds nothing of
it). Two Lean lanes were opened in the same worktree to build it: `Lang/Contextual/Core.lean` (+ `Lang/Proofs/
Contextual/Core.lean`): the simply-typed CMTT core, well-scoped, with `subst_lemma`, `msubst_lemma`, `subst_comp`,
`box_cannot_capture`, `mvar_blocked`, `strengthen`; and `Lang/Contextual/Closure.lean` (+ `Lang/Proofs/Contextual/
{Closure,Experiments}.lean`): the guarded contextual closure over an ABSTRACT calculus (so it does not wait on the
core), versioned assumption tokens, `Derivable`/`Available`, the four `Outcome`s, `fill`/`select`/`withdraw`/
`prune`/`rejudge`/`repair`/`fromScratch`, the theorems `fill_preserves_derivable`, `conditional_soundness`,
`withdraw_never_refutes`, `repair_agrees_from_scratch`, `locality`, `history_is_prefix`,
`executed_prefix_blocks_replan`, `stability_class` with its syntactic contrast, and the eight experiments as named
theorems over a concrete instance (the cycle experiment as least-fixpoint versus counting, both proved). Their
reports append below when they return. The `.ob` instance then becomes a MODEL of the closure theory (a `Calculus`
instance over Lang data + rows), which is the right relation between them.

### 9.1 The Lean-level theory, as returned by the lanes (MEASURED: every theorem elaborates clean; axioms propext / Classical.choice / Quot.sound only; no sorryAx)

**CMTT core** — `Lang/Contextual/Core.lean` (224 lines) + `Lang/Proofs/Contextual/Core.lean` (841 lines, 79 theorems).
Well-scoped simply-typed CMTT: `Ty := base | arr | box Ψ A`; `Tm := var | lam | app | box Ψ t | letbox | mvar u σ`
(σ an explicit simultaneous substitution); one `HasTy Δ Γ t A` inductive (the `mvar` rule carries `HasSubst` inline;
`HasTy.mvar'` is the textbook form); `box` is CLOSED to the ambient Γ (ordinary substitution does not enter it,
metavariable substitution does); one substitution operation over functions, lists as its prefix form, so
`subst_comp` needs no scoping premise. Theorems: `subst_comp`, `hasTy_weaken`/`_weaken_append`/`_rename`/`_mweaken`/
`_mren`, `hasSubst_id`/`_proj`/`_shiftSub`/`_nil`/`_cons`, `subst_lemma`, `hasTy_substFn`, `msubst_lemma` and
`hasTy_msubst_gen` (any depth), `hasTy_uses_lt`, `strengthen` (the proposal's factorization `t ≡ t₀[π]`: unused
hypothesis ⇒ a smaller-context construction and the projection recover `t`); teeth `box_cannot_capture` (∀ Δ Γ T,
`|Ψ| ≤ k → ¬ HasTy Δ Γ (box Ψ (var k)) T`) and its toy, `mvar_blocked`/`subst_keeps_blocked` (ordinary substitution
never unblocks an `mvar` head), `msubst_unblocks`/`msubst_other_blocked` (only a metavariable substitution for THAT
variable does: Layered MTT §5.2 made operational), `strengthen_needs_unused`. Reduction: weak-head `Step` (β;
`letbox (box Ψ t) s ↦ msubst t 0 s`; congruence only at app-function and letbox-scrutinee), `subject_reduction`
(its two redex cases ARE `hasTy_beta` and `msubst_lemma`), `step_deterministic`, `no_step_under_box`, `lam/var/mvar_no_step`,
`letbox_needs_box` (a letbox on an unresolved metavariable is stuck; its toy: an outer letbox fires, the scrutinee
becomes a box, the inner one steps), `bell_resume_computes` (rfl) and `bell_resume_toy`: the Bell-shaped
continuation `k = box [base] ((λy.y) r)` is typed at `[base ⊢ base]` under ANY ambient context (it captures nothing),
`let box u = k in u[x]` types at `base`, steps to `(λy.y) x` then `x`, each typed by `subject_reduction`. DEFERRED
(logged with two options, closures vs projections with a `Sub` type mutual with `Tm`): first-class substitutions
(Cave–Pientka). Lean v4.30.0 refuses `deriving DecidableEq` on the nested inductive, so toys are `rfl`.

**Guarded contextual closure** — `Lang/Contextual/Closure.lean` (583 lines) + `Lang/Proofs/Contextual/Closure.lean`
(1,236 lines, 75 theorems) + `Lang/Proofs/Contextual/Experiments.lean` (31 theorems). Over an abstract `Calculus`
(Ty, Ctx, Tm, decidable term equality, `HasTy` over a meta-context, `msubst` with the partial `msubst_lemma` "filled
holes leave Ω", `check`/`check_sound`, `uses`/`drop`/`strengthen`/`weaken` with `strengthen_lemma`/`strengthen_factor`;
no `box` field: the theory never boxes). Tokens `{id, ver}` immutable and versioned; `World {live, env}`; `Edit :=
withdraw | assert | setEnv`; `reissue`. `Iface` (a hole's interface: context, type, hypotheses backed by tokens,
its own guard over env and filling, budget, chooser, acceptor); `Candidate {filling, supports, blockers, cost, by,
status}`; `Status := verified | suspended (missing tokens) | pruned (live blockers) | conflict (illTyped | guardFails) |
uncovered (cost, budget)`; `Obligation := refill | support | settle | reconcile`; `Outcome := kept | replacement u j M |
strengthening u x t₀ | alternative u j | suspended u Φ`; `Template` (Γ, T, P, Ω, its typing proof, distinct hole
names); `Closure` (template, a slot per hole: candidates, selected, accepted; owed obligations; history) — σ, D,
support, Φ are DERIVED. `judge` is the one status function; `effSupports` = declared supports + the token of every
context hypothesis the filling USES; judgments `Derivable`, `Available`, `WellFilled`, `Settled`, `Coherent`;
`observe` = every retained candidate's recorded status, hole by hole (selection and history excluded). Operations
`propose select fill deselect accept prune rejudge repair withdraw fromScratch`, `Op.run`, `Session.run`;
`Consumer` reads a hole only through a projection; `ValueGuard`/`StableUnder`; `Rule`/`Derives`/`lfpIter` (least
fixpoint) versus `supportCount`/`countRun` (naive counting). Theorems: `reissue_never_reenables`; `judge_congr`,
`judge_frame`, `judge_verified_iff`, `judge_conflict_iff`, `judge_pruned`; `provenance_iff` (verified iff some
monomial of the provenance polynomial is all live); `withdraw_never_refutes`, `token_edit_conflict_iff`,
`withdraw_never_prunes`, `withdraw_never_refutes_closure`; `repairCands_eq`; `repair_agrees_from_scratch` (under
`Coherent`; `repair_coherent`, `fromScratch_coherent`); `alternative_sound`, `replacement_sound`,
`strengthening_sound`, `suspended_sound`; `repair_keeps_accepted`; `repair_carries_untouched`, `locality`;
`conditional_soundness`, `conditional_soundness_closure`; `derivable_of_wellFilled`, `op_preserves_wellFilled`,
`fill_preserves_derivable`, `op_preserves_coherent`; `select_requires_available`; `reissued_support_unverified`;
`history_is_prefix`; `executed_prefix_blocks_replan`; `consumer_boundary`, `valueGuard_iff`, `stability_class`,
`judge_stable`; `lfpIter_sound`, `no_facts_no_derivation`. The eight experiments (decide over concrete sessions;
the cycle by induction): `withdraw_one_of_two_supports(_available)`, `withdraw_last_support(_unavailable)`,
`withdraw_pruning_reason` + `prune_needs_chooser`, `cycle_grounded`/`cycle_loses_grounding`/`counting_keeps_cycle`/
`counting_disagrees_with_lfp`, `dependent_context_change`, `replace_filling_preserving_contract`,
`correct_but_cost_lost`, `reapply_earlier_filling` + `unversioned_reissue_reenables`; beyond them
`withdraw_hypothesis_strengthens`/`_obstructs`, `unchecked_select_underivable`, `value_guard_stable`/
`syntactic_guard_not_stable`, `unrelated_withdraw_is_frame`, `executed_prefix_instance`. Falsifiers (logged): four
definition mutations each break a named theorem (withdrawal producing a conflict breaks `withdraw_never_refutes`;
repair dropping the accepted check breaks `repair_keeps_accepted`; select trusting the recorded status breaks
`select_requires_available`; repair re-judging nothing breaks `repairCands_eq`); two of them also break proofs
structurally, which the log says.

**CORRECTIONS TO THE PROPOSAL, dated 2026-10-22, PROVED (read this, not sections 3–4, for the design that exists)** (CLOSURE's findings, READ; the obend-level corrections are the 14 numbered items above): (1) the guard belongs to the
HOLE, not the candidate — a candidate-supplied guard lets the proposer certify itself, against "a proposed
replacement acquires authority through checking"; per-candidate conditions are data the hole's judge reads. (2) The
four outcomes are not exhaustive and differ in who may apply them: a fifth, `kept`; `alternative` keeps σ (same
filling, another derivation) so repair applies it; `replacement` changes what the acceptor receives so repair only
OFFERS it to the chooser; after acceptance only `suspended (reconcile)`. (3) `observe (repair S) = observe
(fromScratch w′)` is false without a coherence premise and an explicit observable (the selection is history, not
observation); and since recompute-all satisfies it, locality is a separate theorem (`repair_carries_untouched`,
resting on sufficient dependency sets, `judge_frame`). Also: "withdrawing a leaves Δ = ∅" is checkable only when
supports are DERIVED from the filling's use of hypotheses (declared-only supports would leave such a filling
verified); REFUTED has no sound producer at the hole level (a conflict is evidence about one candidate); "live at its
recorded version" is redundant once the version is the token's identity. Limits (logged): the toy's strengthening is
the identity (the real `t ≡ t₀[π]` waits for the Core instance); supports are one level deep; an env edit marks
every candidate touched; the toy's hole occurrences carry no `u[θ]`.

**The instance** (in progress): `Lang/Proofs/Contextual/CoreInstance.lean`, `cmttCalculus : Calculus` with the real
CMTT, which requires in Core a type checker `infer` with `infer_sound`/`infer_complete`, a hand-written decidable
equality on the nested inductive, and the strengthening FUNCTION `unshiftAt` with `weaken_unshift`.

### 9.2 The second-agent vacuity read (READER-CONTEXTUAL, 187 theorems read, disjunct check per theorem; READ)

Law checks pass (def modules export no theorem; proof modules import def or proof modules only; no sorry/#guard/
partial/native_decide/axiom/unsafe). Verdict: **Closure + Experiments LAND-WITH-FIXES; Core HOLD** until the instance
lane stops (its new `infer`/`check`/`msubstP`/`unshiftAt`/`beq` have no theorems yet), then LAND-WITH-FIXES.
Findings, each now routed back to the lane that owns the file:
1. HIGH: the `Calculus` strengthening fields are satisfiable by `drop := id`, `strengthen = weaken = id`, so the
   abstract `strengthening_sound` had no content (the toy bit only because its `drop` filters). Fix: a non-degeneracy
   field `weaken_avoids : HasTy [] (drop Ψ x) M A → uses (weaken x M) x = false`.
2. MEDIUM: `Calculus.msubst_lemma` (named, simultaneous, partial, no renumbering) was FALSE under the obvious
   list-based instance (Ω = [⟨7,[base],base⟩], P = `mvar 0 [var 0]`); Core's `MEnv`/`msubstP` rewrite is the right
   shape; the instance is owed with `hasTy_msubstP` and `check_sound`.
3. MEDIUM: `provenance_iff` is `judge_verified_iff` repackaged (`provenance` copies judge's non-support clauses and
   evaluates guards and blockers at `w`): kept as THE BRIDGE, docstring to say so (ROOT's ruling).
4. MEDIUM: on every reachable closure recompute-all satisfies `repair_carries_untouched`/`locality` (by
   `judge_frame`), so no statement separated repair from recompute-all. Fix: `repair` returns the indices it
   re-judged; `repair_rejudged_eq_touched`.
5. MEDIUM: `msubst_unblocks` had an identity-carrier conjunct and an overclaiming name (false when the filling's head
   is itself an `mvar`); split into `msubst_mvar_self` and a real `headKnown`-becomes-true theorem with its side
   condition.
6. MEDIUM: `box_cannot_capture` covers a bare `var k` body; the general fact `box_ambient_free : HasTy Δ Γ (box Ψ t)
   T → HasTy Δ Γ' (box Ψ t) T` is added.
7. MEDIUM: experiment 4 is a separate rule model and its withdrawal world was the empty world; relabelled "not
   expressible in the one-level closure" and restated over a world with an unrelated live fact.
8. MEDIUM: Core's newest definitions land only with their theorems.
9–12. LOW: a named `Coherent` instance on an experiment state + `session_preserves_coherent`; `prune` ignored
   `accepted` (refused now, or stated); `mvar_blocked`/`subst_keeps_blocked` are definitional (docstrings say so);
   dangling references (`owed_grows`, experiment 1's header) fixed; `letbox_needs_box_toy` shows its terms typed.
Per-theorem notes (which side of each iff, which ∃ witness, which premise makes each experiment bite) are in the
reader's report; no experiment uses a world where every token is dead; `suspended_sound`'s two disjuncts are each
inhabited and mutually exclusive on `accepted`; `strengthen`'s ∃ t₀ is the renamed term, not derivable from the
premises; `step_deterministic` is genuine; the `*_no_step` facts hold by construction of `Step` (design facts).

### 9.3 LANDED (2026-10-22; MEASURED by the judge)

- `1e9418374c783d8ef3a823b19f3747e363ad2575` — `lang: contextual modal types and the guarded contextual closure
  (LANG-66)`: Lang/Contextual/{Core,Closure}.lean, Lang/Proofs/Contextual/{Typing,Core,Closure,Experiments}.lean
  (106 + 87 + 37 theorems), Lang/Journey.lean (holeText + LH0–LH11; lang-journey GREEN 704 rows), decisions/lang.md
  LANG-66. PRE-PUSH FAST GREEN; no wire moves, no re-id, no re-genesis, no landed premise or statement changed.
- `56c79a0` — `lang: the real-CMTT instance (LANG-66 (a))`: Lang/Contextual/CoreCalculus.lean (`cmttData`, `holeEnv`),
  Lang/Proofs/Contextual/CoreInstance.lean (`theorem cmttLaws`, every law discharged; `bell_template_toy`,
  `cmtt_strengthen_toy`). PRE-PUSH FAST GREEN.
- The gate's def/proof split (closure.py C3) shaped the final form: `Calculus` became `CalculusData` (def module)
  + `CalculusLaws D HasTy : Prop` (proof module) with `HasTy` a parameter and `Template.Typed` a predicate — nano's
  own `Env`/`Ctx.Lawful` pattern; the judgments `HasTy`/`HasSubst`/`Step` live in the proof module `Typing.lean`;
  fixtures are private. The first landing attempt was refused by C3 before any build because both lanes had
  checked with `lake env lean` (which does not apply the lakefile's `leanOptions`) and `lake build`, never
  `gates/check.py`; recorded here so the next lane runs the source gates first.
- Reader's final skim after the restructure: 0 conclusions changed beyond binders; `cmttLaws` genuine;
  LAND-WITH-FIXES → commit 3 (fix-forward): `Template.Typed` proved on the experiment templates and
  `s1_derivable`; the def module's four private theorems removed; `drop_removes`' docstring (its premise is false
  for CMTT, which shifts `var x`; it covers degenerate weakenings only).
- `6bf2585` — `lang: the derivability theorems applied to a concrete closure, a weakening fact that bites for CMTT,
  and a def module with no theorem (LANG-66)`: `tpl0_typed`, `tplH_typed`, `s1_derivable` (experiment 1's state is
  Derivable, with a FILLED hole), `session_preserves_tpl`, `weaken_never_var` (holds for CMTT: Ψ=[base,base], x=0,
  `shiftAt` sends `var 0` to `var 1`), `drop_removes` a corollary; Core.lean's `beq` + four private theorems replaced
  by mutual structural `Ty.decEq`/`Tm.decEq`. Reader's skim: LAND. PRE-PUSH FAST GREEN.
- `8c31ace` — `lang: open protocols as typed families of continuations (LANG-67)`: Lang/Contextual/{Protocol,NanoBridge}.lean,
  Lang/Proofs/Contextual/{ProtocolTyping,Protocol,Negotiation}.lean (101 theorems); READER-PROTOCOL LAND-WITH-FIXES →
  eight fixes → LAND; `nano_interp_runs` re-derives HOSTING-37's `interp_runs`. PRE-PUSH FAST GREEN.
- cv task `01a1587d-9a98`: first-class substitutions (Cave–Pientka), the two syntax options.
- All four landings of the ACTIVITIES lane are on main: 1e94183, 56c79a0, 6bf2585, 8c31ace.

### 9.4 Open protocols (PROTOCOL lane, returned; the reader and the C3 restructure in flight; the author's report READ)

`Lang/Contextual/Protocol.lean` (812 lines) + `Lang/Proofs/Contextual/Protocol.lean` (936) + `Negotiation.lean` (347):
`Sig {Op, Resp, next}`, `Prot := ret | call op k | hole h`, interfaces Ω with polarity/acceptor/context/tokens/result
condition/obligations/contract, `Spec` (consumes a linear token, requires facts, establishes obligations), the judgment
`HasProt sp Ω Γ Q Φ Δ P` (Δ a bag, spend removes one per continuation; Φ an UPPER BOUND), `Hist`/`Started`/
`Dispatched` (entered), `Open` with a guarded `resubst`, `admits` separate from typing. Proved: the four families
(`fill_preserves_hasProt`, `interpret_fill`, `interpret_record`, `locality`, `repair_agrees_from_scratch`,
`repair_residual`, `repair_reuses`, `hasProt_reach`, `linear_once`, `resubst_preserves_started`, `admits_local`,
`commit_once`); `no_foresight` versus `response_dependent_succeeds` (a hole is not an interaction: scope, not polarity,
separates them); `separate_witnesses_insufficient`, `greedy_vs_logical` (by decide); the negotiation's four changes
(`unrelated_update_keeps_plan`, `provider_revoked_unavailable` + `revocation_repair`,
`representation_change_transports`, `competing_commitments`/`replay_refused`), `internal_once_not_external_once`,
`exactly_once_needs_reply_and_dedupe`, `deadline_expires`, `cancel_path_refunds_obligation`,
`lost_reply_keeps_obligation`, `lost_reply_blocks_replan`, `replan_before_dispatch`; and the nano bridge:
`nano_runs_iff`, `nano_interp_agrees`, **`nano_interp_runs` — HOSTING-37's `interp_runs` re-derived from
`interpret_record`**, so the resident's proved continuation structure is an instance of the protocol theory (section
1.5's claim, now a theorem rather than a correspondence table). Corrections to the prose found by formalizing: Φ is an
upper bound and a call's obligation starts at dispatch; polarity does not capture causality, scope does; "unexecuted"
must be "not entered" (three states: not reached / reached / entered). Decision entry LANG-67 drafted; lands as its own
`lang:` after the reader's verdict and the C3 restructure (Props to the proof module; bridge defs to
`Lang/Contextual/NanoBridge.lean`).
READER-PROTOCOL (90 theorems, disjunct check per theorem): LAND-WITH-FIXES, nothing unsound. HIGH: the prose "a filling
cannot depend on a response" is FALSE in the calculus (response-indexed hole names give foresight: a counter-theorem
is added and the separation restated for response-independent naming — scope is a naming discipline, not a fact).
MEDIUM: `theirs_hole_untypable`/`fill_skips_theirs` are design rules, not findings; `Iface.acceptor` read by nothing
(deleted or given a reader + a non-trivial `accepts` tooth); the external-once theorems were facts of the module's own
delivery model, now linked to the history via `Internal.ofHist`; `representation_change_transports` was over a
one-element epoch with no stale-opening refusal (epoch : Nat, partial correspondence, `stale_opening_refused`);
`lost_reply_blocks_replan` restated over `replan`/`Replan` with the answered-half tooth; section 4's scalar
illustrations labelled or instantiated over the template. LOW: "linear" is affine (`at_most_once`); a dead docstring
reference; `residual` returns fragment names, not obligations. Confirmed real: the four families, `commit_once`,
`replay_refused`, `deadline_expires`, `cancel_path_refunds_obligation`, and the nano bridge (`nano_interp_runs` has
exactly HOSTING-37's statement, genuinely re-derived; `ofProg`/`toEv` cover all six `Prog` constructors).
