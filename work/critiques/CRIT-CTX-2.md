CRIT-CTX-2 — 2026-10-27

The resident now inhabits the open syntax and its runtime interpreter.
It does not inhabit the contextual typing judgment.
The new theorem characterizes support checking.
It does not establish the common repair semantics requested by the first review.

This review fixes repository claims at `2efa6a5719bf4898921cf24a1850dc5c204e20dc`.
That was `origin/main` after the review's fetch on hbox.
I read CRIT-CTX before inspecting the revision.
I read DESIGN-CTX in full, including §1.4, §11 and BUILT-7/8.
I read CHARTER and the LANG-101 and HOSTING-59 entries with their critiques.
I inspected Slot, the resident definitions, ResidentSlots, the interpreter proof, the owed-rings model and H4.
I checked the relevant typing rules, kernel authority and law paths, ROM resolver, document changes and offer statements.
Repository inspection used hbox.
I ran no build or test.
The reported H4 pass remains the lane's measurement.
The counterexamples below are deductions from the inspected definitions.

ANSWERED: the Empty-hole embedding no longer stands in for integration.
`Hosting.Resident.Prog` is an abbreviation of `Prot` with the inhabited hole type `Hosting.Resident.Hole`.
`readP` constructs a `serve` hole after receiving the pending rings.
`refusedP` and `probesP` construct a `use` hole after observing the refusal path.
`tick` executes these terms through `Slot.interp`.
NanoBridge and ContextualNano are deleted.
The `Empty` in `Prog.interpN` is the refusal-reason type, not the hole type.

PARAPHRASED: the calculus has earned a deployed syntactic instance, but not the claimed typed instance.
The resident supplies no `Iface`, `HasProt`, `Fills` or `SubstOK` derivation.
Its signature has the trivial index `Unit`.
The interpreter preserves the Lean types of operations and responses by construction.
That fact does not establish the interface's facts, affine resources, postcondition or obligations.
The existing contextual-substitution result remains a result about typed substitution.
World-dependent repair remains a different obligation from the contextual substitution principle in [CMTT, Theorem 4.3](https://software.imdea.org/~aleks/papers/cmtt/cmtt.pdf).

OWED: correction of the slogan that a World alone determines a closed justified program.
ROM resolution still depends on the caller's authenticated partial view.
It still embeds a typed refusal for an unresolved hole.
Demanding that hole fails during execution.
The new resident semantics does not replace this separate ROM semantics.
The existing strengthening result still re-embeds to the committed candidate body.

PARAPHRASED: the common SLOT now exists as executable code.
Its entire descriptor is `supports : Cand → List Fact` and `judge : Cand → Bool`.
The selection is an argument of `read`.
The candidate order is an argument of `resolve`.
The descriptor contains no chooser authority, transition lifecycle or history.
The resident uses its eligibility filter for two decisions.
Neither ROM filling nor `Receive.law` instantiates this descriptor.
The first review required those two different paths to derive their guarantees from one semantics.
That requirement is OWED.

PARAPHRASED: stored choice and current eligibility are distinguished by `Reading`.
`Reading` also makes refusal an outcome instead of another slot.
The deployed resident does not expose `Slot.read` as a member-facing evidence read.
Its control flow uses `Slot.alternatives`.
DESIGN-CTX's older classification of refusal as a SLOT instance remains incorrect.

PARAPHRASED: `slot_repair` replaces the requested transition theorem with a theorem about reads.
Fresh-versus-incremental agreement is OWED.
Preservation of an eligible selection across a repair transition is OWED.
Authorization of a replacement is OWED.
Preservation of accepted history by that replacement is OWED.
A common locality theorem for the deployed instances is OWED.
`Open.Replan` and fragment repair remain separate from the new theorem.

OWED: contextual integrity and repair over an audited log.
`Spec/Proofs/Claims.lean` still has neither `Integrity.contextual` nor `Integrity.repair`.
`Integrity.law` still carries the `NoRef` restriction.
The proposal in DESIGN-CTX §2.4 still contains undefined proposed relations and an ellipsis.
The generic read theorem cannot discharge those statements.
The proposed floors against stale eligibility and refusal of every alternative remain unconnected to such a top statement.

PARAPHRASED: permanent withdrawal now has an explicit premise.
`Permanent holdsAt later f` distinguishes predicates for which persistence can be proved from predicates for which it cannot.
It does not classify kernel facts by itself.
The resident does not derive this premise from the kernel's tombstone theorem.
Law membership can still become true after becoming false.
The original unconditional claim about every withdrawn justification remains OWED a correction.

OWED: the distinction between unavailable observation and false evidence in the common semantics.
`holdsAt` returns only a Boolean.
`Reading.rejected` separates judge failure from failed supports.
It does not distinguish guard exhaustion, missing observations and false World facts.
The ROM resolver already has several separate refusal constructors for these cases.
The proposed §2.4 formula still incorrectly requires every hole refusal to name a false support.

PARAPHRASED: exact diagnostics now hold for the declared support list of a generic `Slot.read`.
They do not hold for every failure of an invocation.
The ROM resolver still stops at the first failing stage.
Its docstring still claims that one refusal reveals the whole missing read set.
Later hypothesis and guard failures remain concealed by earlier failures.
H4 also demonstrates a deployed refusal whose text contains no coordinate.
Why-not completeness and minimal authorized repairs remain OWED.

OWED: the ATMS identification.
`Slot.alternatives` filters candidates at one supplied valuation.
It does not maintain minimal consistent assumption environments.
Those environments are central to [de Kleer's ATMS](https://dekleer.org/Publications/An%20Assumption-Based%20TMS.pdf).
The new record supplies a bounded support checker.
It supplies no recursively maintained belief network.

OWED: the identification with defeasible argumentation.
The new code has no attack relation or defense computation.
The proposed identification with Dung's grounded extension still has no translation theorem.
External Boolean conditions alone do not establish equivalence with [Dung's argumentation framework](https://cse-robotics.engr.tamu.edu/dshell/cs631/papers/dung95acceptability.pdf).

OWED: the Hazelnut comparison as a dynamic-semantics claim.
`Out.withdrawn` terminates the run at the unresolved hole.
It retains no hole closure for later completion.
It proves no fill-and-resume commutation property.
Those are substantive parts of [Hazelnut Live](https://arxiv.org/html/1805.00155v4).
The proposed partial document read remains an application feature.

OWED: the document consumer required by the first review.
The document test still explicitly invokes `rejudge` before inspecting suspension.
Its selection remains distinct from a live rendering of currently justified text.
Its support fields remain optional.
Its policy still does not require the contributor's own grant as the dependency.
Revoking that grant therefore does not establish withdrawal of every candidate the contributor can post.
The multi-section rendering, independent contributor's existing alternative and evidence-bearing read remain absent from this change.
H4 adds a resident-to-section path.
It does not turn the submitted bytes into a newly supplied program.

OWED: the claimed behavioral meaning of contract pins.
`cellLaw` checks the object's extra-law slots.
It does not establish the behavior of the selected code.
It does not bind that code's eventual call to the supported object.
It does not include package laws merely because they belong to the package.
Current membership does not establish governance of earlier history.
The contract journey still uses an approving law and candidate bodies that return `.var 1`.
The independent component replacement under an explicit behavioral obligation remains absent.

OWED: identification of cell liveness with authority.
`Authority.walk` checks the parent chain as well as the immediate grant.
The resident probes only the immediate `via` cell and the target.
Retiring an ancestor can invalidate this ring's invocation while both probed cells remain present.
`useChoice` then selects `stop` if the ring still waits.
The assertion that every refusal with both cited cells present affects every ring alike is false.

ANSWERED: the missing caller field and the root-`take` admission defect have changed since the first review.
`Req.caller` is present.
`take_notFuser` excludes a caller other than the named peer.
PARAPHRASED: the stronger claim that every session row proves execution of the peer's judged fuse.
The inspected take theorem establishes `CalledByPeer`.
Caller identity does not identify the caller's method or its behavioral specification.
The common repair theorem adds no composition result for that claim.
The session-type claim is still OWED.
`BellConform` explicitly supplies no global type or endpoint-projection theorem of the kind used in [multiparty session types](https://www.doc.ic.ac.uk/~yoshida/multiparty/multiparty.pdf).

ANSWERED: retirement no longer needs the proposed relink-to-empty fiction.
The kernel now has `Body.retire` and a judged retirement path that produces a tombstone.
OWED: package replacement with preservation of state, schema, method meanings and outstanding obligations.
There is still no `Body.relink`.
`Receive.law` still rejects programmed objects through `hasMethods`.
Judged law replacement for data objects still distinguishes outgoing approval from incoming adoption.
It still has no instance of the new SLOT semantics.
The negotiated replacement protocol remains OWED.

OWED: a demonstrated novelty claim beyond an ACL-protected store with a selected identifier.
The baseline paragraph now exists.
Its claimed separation is examined below.

`slot_repair` quantifies over arbitrary fact and candidate types.
It takes an arbitrary view type `V`.
It takes an arbitrary function `holdsAt : V → Fact → Bool`.
It takes an arbitrary relation `later : V → V → Prop`.
It fixes a slot, a view and a candidate.
It imposes no requirement that these views are authenticated or reachable Worlds.
It imposes no requirement that `later` describes execution.

Its first conjunct says that reading `some c` is usable exactly when the judge passes and all declared supports hold.
Its second conjunct says that a blocked read returns a nonempty list containing exactly the declared supports that are false.
Its third conjunct says that a false support remains in later blocked reads if its falsity is permanent along `later`.
That conjunct additionally requires the candidate to pass the judge.
Its fourth conjunct says that reading an already usable candidate as the supplied selection returns that candidate with its evidence.

The `Permanent` premise supplies the temporal content of the third conjunct.
It already assumes that the fact remains false at every related later view.
The theorem transports that assumption through list filtering.
The `usable = true` premise supplies the eligibility needed by the fourth conjunct.
That conjunct does not find a candidate.
It does not perform a selection update.
It does not establish permission to perform one.
There is no state transition in the theorem from which “nothing else changes” could follow.
There is no history parameter to preserve.
There is no cache to compare with fresh resolution.
The theorem is not the one requested by the first review.

Setting `holdsAt := fun _ _ => true` still satisfies the theorem.
That instantiation can ignore every revoked World support.
A server that refuses every selection update also leaves the theorem true.
The update operation is outside its statement.
The theorem therefore cannot refute either of the two broken systems named in the first review.

The seven named resident results are not seven instances of this theorem.
`resident_repair` is a direct specialization of conjuncts one, two and four.
It sets `V := Unit` and discards conjunct three.
Its additional result about `serveChoice` comes from membership in the filtered candidate list.
The always-eligible `idle` candidate makes total availability of some usable action uninformative about service.

`use_withdraw_names` derives membership in the aim's cell list and the supplied `gone` list.
It does not derive cell death from a kernel event.
`use_withdraws` is a separate path theorem about logging, successful noting and forgetting.
Its continuation premise excludes paths that stop because the volume operation failed.
`withdrawn_blocked` unfolds the resident's definitions to compute the blocked read.
`withdrawn_not_served` uses the equivalence with `decideTick` on the filtered queue.
`serve_keeps_withdrawn` is a separate memory-preservation proof over paths.
`serve_repairs` proves queue selection from premises that no kept answer is live and the live list has head `q`.
Its evidence-read conjunct uses `resident_repair`.
These are implementation-specific lemmas with two uses of the generic read facts.
They are not a derivation of all resident repair guarantees from one theorem.

Run-time filling has more than an implementation detail behind it.
`RunsR` gives an inductive, fuel-indexed trace semantics with return, call, fill, withdrawal and bound cases.
It is a big-step path relation, not a small-step reduction relation over machine states.
`runsR_withdrawn` proves that refusal at a hole performs no calls after that hole.
No generic theorem connects `Slot.interp` to `RunsR`.
The resident instead has its own `Runs` relation.
`ResidentRun.interp_runs` connects the deployed interpreter definition to that relation at a recording handler.
It quantifies over the oracle's possible responses.
`tickP_fits` supplies the two-hole depth bound.
The proof does not model the member socket as an authenticated World transition.
The resident's resolver always returns `.ok (fill h)`.
It does not call `Slot.resolve`.
Its withdrawal is a selected action inside `useP`.
The generic `Out.withdrawn` outcome has no deployed resident path.

The resolver passed to `Slot.interp` is pure.
It receives a hole name, not the monad's current state.
The resident captures observations in the hole name.
That construction permits decisions based on responses already received.
It does not provide §11's proposed moving authenticated view by itself.
It also does not provide the proposed `Spec.names` interpretation of responses.
The old syntax already allowed response-indexed hole names.
The runtime extension makes their resolution part of execution.
It does not establish a new causal-information theorem about them.

The existing typing rules retain their existing meaning.
The new interpreter does not consult them.
It can resolve a hole without checking the chooser or the interface acceptance predicate.
It can resolve to a body that spends an abstract token twice.
`Slot.resolve` permits that body whenever the independently supplied Boolean judge accepts its candidate.
No premise connects that judge to `Fills`.
Importing the affine guarantees requires a sound resolver theorem over the resource context at each reach.
It also requires preservation of those resources through resolved calls.
Calling the running resident “typed by the open calculus” before those results would change the meaning of typing by assertion.

The two resident holes are contextual decisions in the operational sense of depending on observations.
They remain guarded dispatch in the stronger comparison asked by this review.
`serveChoice_eq` proves that `serve` is `decideTick` over pending rings whose withdrawal flag is clear.
`use` dispatches among closed, withdraw and stop using the reread and probe flags.
Both slot judges are constantly true.
Both candidate-body families are fixed in the resident binary.
The system accepts new ring data.
It does not accept independently supplied fillings with declared contextual interfaces at these holes.

The support of an `answer r t` candidate is pending membership plus absence from the withdrawal list.
It does not check the answer's text.
It does not check the authority chain.
It does not check the target's application contract.
An initial `serve` selection can therefore be usable while the target grant is already dead.
H4 exercises precisely that sequence.
The resident asks before the failed invoke reveals the problem.
The kernel still refuses the invalid effect.
The design's proposed statement that invocation occurs only with all answer supports live is stronger than this implementation.

`text r` would become a substantive hole when answer candidates carry the context under which they may be used.
That context must bind the ring's identity and capture to the answer.
The acceptance judgment must state what makes an answer eligible.
The choice must respect the already spent ask obligation.
A supplied alternative must be replaceable before commitment without replaying a spent ask.
The lost-reply case must retain the resulting obligation across recovery.
Wrapping `answerText` in a new hole constructor would establish none of these properties.

`pins r` would become a substantive hole when alternative observation plans are checked against the obligations of the eventual invocation.
A plan must identify the exact target and evidence coordinates it supports.
Its success must mean sufficient authenticated observations for that invocation.
Its failure must distinguish unobserved evidence from evidence known false.
The present `forwardPin` is a fixed function of the aim.
Renaming that function a resolver would not supply the missing contract.

BUILT-7 honestly records that `text r` and `pins r` are not implemented holes.
HOSTING-59 honestly says the model's answer remains a value.
The preceding §11 sentence declaring it already a candidate contradicts those admissions.
The document needs one current claim instead of a future sketch written in the present tense.

H4 exposes the missing abstraction boundary in the earlier proofs.
A proof over a supplied refusal interpretation remains true when the deployed refusal cannot supply that interpretation.
The original text parser could pass its unit reasoning while failing on `refused missingCell`.
The replacement probes recover a coordinate from commands whose target the resident already knows.
`probeGone` interprets a refused `read c ?` named `missingCell` as evidence that `c` is gone.
The resulting `gone` list drives the new withdrawal branch.

The retired immediate-grant queue defect is closed in the inspected control flow.
H4 checks that the blocked ring remains pending.
It checks that the following plain ring is answered.
It checks that the withdrawal log names either the aim's grant or its target.
It checks that the queue does not end in `answerRefused`.
It checks a bounded interval without another ask about the withdrawn ring.
It does not check arbitrary authority-chain failures or application refusals.

The theorem-to-World gap remains named rather than closed.
`use_withdraw_names` concludes membership in `gone`.
It does not conclude a tombstone in an audited World.
The path model permits arbitrary command responses.
The probes occur after the refused invocation.
They need not describe the view at which that invocation was refused.
A tombstone observed later can still justify abandoning future attempts.
That justification needs an explicit connection to the kernel's irreversible fact.

`probeGone` also treats a never-created cell as gone.
The source comment explicitly includes that case.
The code does not distinguish permanent retirement from current absence.
The permanence theorem for retired identifiers therefore cannot justify every withdrawal this branch records.
The immediate-grant and target probe list also omits ancestor grants.
The earlier authority counterexample leaves the queue-stopping case intact.

The next ring is not served in the withdrawal tick.
`useP` returns `Tick.next` after recording the withdrawal and forgetting the answer.
The outer loop sleeps before starting the next tick.
`serve_repairs` describes selection when a subsequent `serve` sees a suitable queue.
It does not compose the refused tick with that subsequent tick.
The repeated “same tick” claim in §11 and LANG-101's meta-critique is false.

Commit `2efa6a57` persists withdrawals before forgetting the kept answer.
Startup reads and re-establishes the withdrawal file before initializing memory.
Those are actual recovery changes.
`ResidentSlots` still contains the obsolete comment that withdrawals are memory-only.
`BellConform` explicitly limits its theorem to one process life.
H4 reads the withdrawal file without restarting the resident.
Its substring assertion does not verify recovery composition.
BUILT-8's claim that the permanence premise now holds across restart exceeds the stated proofs.
The remaining theorem must compose durable noting, startup seeding, pruning and future ticks.

The owed-rings change preserves a useful boundary.
Withdrawal does not count as freeing an ask obligation.
`Frees` remains an acknowledged answer or a read that no longer lists the ring.
`bell_resident_conforms` rules out another spent ask before such an event within one process life.
This is a trace invariant over the resident's program.
It is not a session-type derivation.
It is not an instance of `slot_repair`.

DESIGN-CTX §1.4 overstates the difference from its baseline.
Its first item is true of the pure `Slot.read` function.
The resident does not deploy that function as the advertised evidence-bearing read.
Its `serve` evidence consists of a queue-membership test and a local withdrawal flag.
The document's corresponding read is explicitly owed.
An ACL row store can also retain a selected identifier while computing a separate eligibility result.
LANG-101's claim that the store cannot express this distinction is false.

The second item assumes a baseline behavior that the baseline definition never supplied.
Revoking a writer's ACL permission does not itself retract previously stored data.
Re-granting that permission therefore need not revive any previously withdrawn selection.
Binding a candidate to an immutable grant identifier supplies a useful revocation policy.
That policy can also be implemented with ordinary rows and non-reused identifiers.
The new theorem states its consequence only under the permanence premise.
The resident specializes withdrawal persistence to rings retained in its withdrawal list.

The third item is true of the resident's ability to continue without reinstalling or restarting.
It is not a separation from a store whose selected identifier can be changed.
The generic theorem's fourth conjunct is not a frame theorem for that update.
H4 demonstrates continuation to another ring rather than replacement of the failed answer for the same ring.

The fourth item belongs to authenticated deterministic replay.
Kernel followers can rederive the submitted effects from the event and checked view.
`slot_repair` proves nothing about followers.
The resident's queue decisions also depend on its local memory and volume.
No theorem here makes each member rederive those decisions.
Replay is a system guarantee to compose with a slot theorem, not a consequence of this slot record.
The paragraph's final statement that `use` extracts a cell identifier from refusal text is stale.
The landed code probes the World instead.

Before calling this a contribution, I require a transition semantics that relates observation, eligibility, authorized selection, execution and repair.
Its theorem must connect revalidation to fresh resolution.
It must preserve already accepted effects.
It must state sufficient observation and resource premises for repair availability.
It must distinguish reversible failure from irreversible revocation.
It must state the dependency footprint outside which changes leave the judgment unchanged.

I require a sound runtime resolver for the contextual typing judgment.
Its proof must connect selected bodies to their interfaces at the point of execution.
I require ROM or independently supplied typed component filling and judged law replacement to instantiate the same repair theorem.
The law instance must retain both outgoing approval and incoming adoption.
An example must reject a same-typed replacement that violates its behavioral obligation.
An example must accept an independently supplied replacement without reinstalling the consumer.

I require the deployed diagnostic and recovery paths to refine that semantics.
The checks must include ancestor-grant retirement, reversible policy failure, missing observations and restart after withdrawal.
The existing next-ring test is insufficient for these cases.
The document must render current eligibility and evidence while retaining blocked sections.
Its contributor-withdrawal policy must survive omitted or substituted supports.
The novelty statement must name the compositional guarantee obtained beyond a row store implementing the same checks.

The work is closer to a contribution because the resident now executes nonempty contextual syntax, but the contribution remains owed until one typed, history-preserving repair theorem covers both that execution and a genuinely different governance instance.
