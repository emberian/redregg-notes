CRIT-CTX — 2026-10-27

Nanodregg has a mechanized theory of typed contextual filling.
It does not have the unified contextual theory claimed by DESIGN-CTX.
Its deployed selection mechanism is guarded dispatch against an authenticated view.
Its proposed contribution is a compositional account of repair across changes of authority and governance.
That account is not in the tree.

This review fixes repository claims at origin/main `5c0c20550e1f9a64f922ee30f1656f66df1f2ccf`.
A second fetch returned the same revision.
Repository inspection used hbox.
I read DESIGN-CTX in full, including its BUILT entries.
I read both HOLISTIC reviews in full.
I read CHARTER and the relevant LANG-66, LANG-75.*, LANG-83 and LANG-84 decision material.
LANG-85 is absent from this revision's decision file.
The definition of `Req` has no `caller` field.
The design's reports of unlanded caller and fuse work are not evidence of those features on main.
I inspected the named runtime definitions, their relevant proof statements, both journeys and the complete document client test.
I inspected the generated Section texts structurally.
The four texts contain no contextual hole declarations or hole terms.
I did not rebuild the tree or rerun the reported tests.
The counterexamples below are deductions from the inspected definitions.

The dispute between the readers has a definite answer.
HOLISTIC-LANG is right about the runtime mechanism.
HOLISTIC-LANGPROOFS is right that the implementation contains real contextual substitution mathematics.
HOLISTIC-LANG overstates its case by calling that mathematics decoration.
HOLISTIC-LANGPROOFS overstates its case by treating an unfamiliar combination as demonstrated novelty.
A missing literature name proves nothing about originality.
The design does not settle this dispute by moving the novelty claim from the mechanism to an unproved system property.

`Lang/Proofs/Fill.lean:fillHoles_typed` is a genuine theorem.
It says that a filling typed at its declared context preserves the type of a term containing that hole under explicit substitution.
It also accounts for declarations left unfilled.
This is the contextual-substitution principle represented by Theorem 4.3 of Nanevski–Pfenning–Pientka.
It does not say that a World supplies an appropriate filling.
It does not say that a filling respects a behavioral contract.
It does not say that changing the World repairs an execution.
The correspondence is to a substitution fragment, not the whole modal calculus with its introduction and elimination forms. [Contextual Modal Type Theory](https://software.imdea.org/~aleks/papers/cmtt/cmtt.pdf)

`Lang/Proofs/LiveHoles.lean:selectHole_origin` identifies the ROM candidate named by the selection row.
`selectHole_cell_support` relates its cell supports to live cells in the supplied pinned view.
`selectHole_contract_support` relates its contract supports to the corresponding law and package slots.
`selectHole_hypotheses` identifies the dead hypotheses removed from a successful selection.
`selectHole_factor` proves that the strengthened filling remains typed.
The same theorem proves that re-embedding produces exactly the original candidate body.
That equality explains why the running mechanism remains dispatch among committed bodies.
`instantiateHoles_typed` proves that successful preparation produces a closed body at the package interface.
Its proof obtains typing from the runtime's final type check.
`instantiateHoles_sources` bounds the instantiated body's digest literals by the template and selected ROM bodies.
None of these statements is a history-level repair theorem.

The operational semantics is more precise than the slogan `⟦P⟧(W)`.
Preparation depends on the caller's pinned cell view.
It also depends on the caller's pinned row view.
Execution additionally depends on the method, arguments, state, request and budget.
Two requests at one World can produce different answers because one omitted a required pin.
The appropriate semantic object is resolution relative to an authenticated partial view, followed by execution.
Resolution can produce a typed refusal in place of a hole.
An undemanded blocked hole need not abort the method.
A demanded blocked hole faults through `blocked_step`.
The design's description of every deferred decision being filled by a justified candidate therefore misdescribes its own semantics.
Dependence on mutable World state alone distinguishes this system from no ordinary stateful interpreter.

The ATMS identification is also too strong.
De Kleer's ATMS maintains labels containing minimal consistent assumption environments.
Its defining obligations include soundness, completeness and minimality across alternative environments.
`selectHole` checks only the candidate named by one row.
It computes neither the alternative environments nor an ATMS label.
Its own docstring explicitly says that the live label is not computed.
LANG-75.3 records the removal of the abstract provenance and repair theory.
The defensible description is a bounded justification checker inspired by truth maintenance. [An Assumption-Based TMS](https://dekleer.org/Publications/An%20Assumption-Based%20TMS.pdf)

The posted-value machine is closer to Doyle's support-list discipline.
Its two optional positive supports and optional blocker determine a candidate's current verdict.
It still has no recursively maintained network of beliefs.
It implements no general defeasible-rule priority or conflict-resolution semantics. [Doyle's account of reason maintenance](https://www.csc2.ncsu.edu/faculty/jdoyle2/publications/fi94-intro.pdf)

Calling this Dung's grounded semantics requires an explicit translation.
Dung's framework consists of arguments and attacks between arguments.
Nanodregg's blocker is an observed external fact.
Nanodregg does not compute defense against attacks.
A translation could introduce arguments representing external facts.
The translation would then owe an equivalence theorem between the grounded extension and the deployed verdict.
No such translation is supplied by the assertion that the case is degenerate. [Dung, On the Acceptability of Arguments](https://cse-robotics.engr.tamu.edu/dshell/cs631/papers/dung95acceptability.pdf)

A failed coordinate is a diagnostic, not a provenance polynomial.
Grädel–Tannen's repair construction requires a formula and a defined set of permitted updates.
It relates those updates to satisfaction of that formula.
`selectHole` stops at the first failing stage.
Its filtered list covers failures in that stage only.
A failure in support observation can conceal a later guard failure.
The result contains neither alternative successful derivations nor minimal authorized repairs.
The docstring claiming that one refusal reveals the whole missing read set is false for the entire invocation.
The implementation supports coordinate-bearing diagnostics.
It does not establish why-not completeness in the cited sense. [Provenance Analysis and Semiring Semantics for First-Order Logic, §7](https://arxiv.org/html/2412.07986v1#S7)

Hazelnut Live gives incomplete programs dynamic meaning through indeterminate results and hole closures.
Its fill-and-resume account concerns computation retained around an unfinished expression.
Nanodregg substitutes a refusal into a blocked ROM hole.
It does not retain a suspended evaluation for later completion.
The document's proposed partial rendering is an application read operation.
It is not Hazelnut Live's dynamic semantics. [Live Functional Programming with Typed Holes](https://arxiv.org/html/1805.00155v4)

The SLOT is presently several objects with a shared name.
`HoleROM` contains a context, candidate terms, supports and a selection-row coordinate.
`Std.hole` emits a package managing posted first-order values and their statuses.
`Std.activity` emits a row protocol with captured data and a response.
`Std.offer` emits offer selection and an atomic nested-call protocol.
The law list is a kernel-managed sequence of package identifiers.
A refusal is an outcome of a check.
A refusal is not another deferred decision.
Putting it in the same list is a category error.

There is real reuse among the generators.
The posted hole uses the activity generator for accepted values.
The offer uses the activity log for sessions.
Neither fact establishes the claimed identity with ROM holes or law replacement.
The `Slot` in `Kernel/World.lean` is an unrelated storage-coordinate type.
The design's proposed descriptor is not implemented.
No shared definition is instantiated by both `HoleROM` and `Receive.law`.
No shared repair theorem covers both.

A single object requires a common transition semantics, not a record containing every available field.
Define a slot by its candidate interface, authorized chooser, evidence predicates, acceptance relation and lifecycle.
Keep the current selection separate from the set of eligible candidates.
Keep historical commitment separate from present eligibility.
Make refusal an output of the slot judgment.
Instantiate that definition for ROM filling and for law-list replacement.
Prove that the deployed paths simulate those instances.
For law replacement, the transition must distinguish approval by the outgoing regime from adoption by newly added laws.
The current kernel already makes that distinction.
A single `accept : Term` field does not explain it.

The common repair theorem should say that revalidation after a World change agrees with fresh resolution under the new authenticated view.
It should preserve the selection when that selection remains eligible.
It should expose eligible alternatives when the selection loses support.
It should require the authorized chooser's action before committing an alternative.
It should preserve the already executed history.
It should invalidate only future reliance on evidence that no longer holds.
A locality clause should state the support footprint outside which changes cannot alter the judgment.
These conclusions must hold for both the hole instance and the law-list instance.
Two independent proofs followed by a shared noun do not establish the abstraction.

For a member, contextual integrity must mean that every accepted effect used the candidate the member authorized at the checked view.
Every declared support needed for that use must hold at that view.
Every used contextual hypothesis must be justified there.
The candidate must meet the interface and acceptance contract.
The member's follower must rederive the same result from the same event and view.
No stale cached verdict may authorize a new effect.
This guarantee concerns the pre-Turn view.
It does not promise that the Turn leaves all of its supports live afterward.

For a member, repair must mean that losing a dependency does not require reinstalling the whole application.
The member must be told whether the obstacle is missing observation, failed evidence, policy rejection or resource exhaustion.
An authorized alternative must be selectable without rewriting the committed past.
The availability statement must name its prerequisites.
Those prerequisites include chooser authority, complete observations, a compatible candidate, adequate bounds and the required selection update.
Eventual action by a person or scheduler is a separate liveness claim.

The landed statements do not establish this combined promise.
`Spec/Proofs/Claims.lean` contains `Integrity.law` with its `NoRef` restriction.
It contains neither `Integrity.contextual` nor `Integrity.repair`.
The named `repair_available` and `selectHole_refusal_names` are absent.
The design's Lean block contains undefined proposed vocabulary.
Its repair definition is an ellipsis.
LANG-83 explicitly defers the top statement to S5.
A client test cannot inhabit a formal proposition that has not been defined.

The proposed statement also needs substantive correction before proof work begins.
An unpinned support is unobserved, not established false in the World.
A guard can return false while every support holds.
A guard can exhaust its budget.
A selection can name an absent or out-of-range candidate.
These refusals cannot all witness a false support coordinate.
The claim needs separate semantic cases for these outcomes.
The raw negative literal interpretation collapses knowledge, policy and execution failure.

The proposed repair guarantee is too strong in a different way.
`selectHole_live_selects` assumes that the selection row already names the successful candidate.
It assumes that the guard run returns true.
It proves success of that local selection operation.
It does not produce an authorized Turn changing the row.
The document uses separate `select` and contribution operations.
The contract journey uses a separate `choose_code` before `execute`.
An eligible alternative is not automatically used in the next Turn.

Permanent withdrawal also needs a typed distinction between assumptions.
A retired grant's tombstone supports permanent revocation of that cell.
An old exact row version remains obsolete under the kernel's version discipline.
A law-membership predicate has different behavior.
A data object can drop a permissive law and later adopt it again.
The same `cellLaw g L` predicate then becomes true again.
Package-membership predicates would have the same issue after relink.
Permanent withdrawal applies to particular irreversible evidence, not to every false predicate.

The document demonstrates continued dependence of an existing post on a cited cell.
Ordinary revocation of permission to post only stops later posting operations.
The section additionally rechecks a dependency when an editor selects or accepts a stored candidate.
That is the precise gain over a plain revocable posting grant.
The client test exercises it through real member commands and follower setup.
It demonstrates that the generic posted-value package can carry bytes as text.
It does not demonstrate a new contextual-substitution capability.

The demonstration is one section.
It has one editor and one contributor.
After revocation, the same contributor receives a fresh grant and posts the replacement.
The test does not select a preexisting alternative from another contributor.
It does not assemble a document from several sections.
It does not show a live provenance label.
It does not evaluate around a blocked section.
It does not run a newly supplied program.

The distinction between status and live meaning is visible in `Std.holePackage`.
`rejudgeBody` writes a candidate's status while returning the old object state.
The selected candidate ID therefore remains after the rejudge.
The test explicitly invokes `rejudge` before reading the suspended status.
An ordinary read before that invocation still sees the stored status.
The test proves no invariant that every displayed section has current support.
The phrase “revocation withdraws the text” is stronger than the demonstrated behavior.
The proved mechanism rechecks use.
The demonstrated reader displays stored rows.

The document also fails to require the advertised dependency.
`s0` and `s1` are optional.
The document's clause checks text length.
It does not require the cited cell to be the poster's contribution grant.
A contributor can propose with both supports absent.
A contributor can cite another live cell.
Revoking the contribution grant does not invalidate those candidates through the support check.
LANG-83 acknowledges the arbitrary-cell case.
Adding ROM `cellLaw` pins does not repair this document policy.
The Section generator does not use those pins.
The claimed contributor-withdrawal contract must be imposed by the package or its trusted posting path.

Contract pins add a condition about the target of a choice.
The authority chain answers whether an actor can perform a named operation on that target.
`cellLaw` asks whether the target's extra-law slots contain a particular package ID.
`cellPackage` asks whether its package slot contains a particular package ID.
These are independent questions.
An authorized call can fail the contract condition.
A contract condition can hold for a caller with no invocation authority.
Both checks belong in the same admitted use.

Even plain cell support is weaker than a checked authority chain.
`cellLive` establishes that one cell exists.
`Authority.walk` additionally checks its kind, target, holder, right and parent chain.
Revoking an ancestor grant invalidates authority without requiring the descendant cell itself to disappear.
The phrase “a live grant is authority” therefore loses a necessary distinction.

`selectHole_contract_support` proves the slot predicates it names.
It does not prove that the selected code invokes the supported object.
It does not prove a provider's behavioral specification.
`cellLaw` also omits laws supplied by the object's own package unless that package appears separately in the extra-law slots.
Current membership does not establish that the law governed the object's earlier history.
The kernel judges the outgoing laws on replacement.
It judges newly added laws on adoption.
That provides a transition discipline from the adoption point onward.
It does not rewrite the earlier history.

The contract journey tests nominal dependence only.
Its `openLaw` approves every act.
Its three candidate bodies are all `.var 1`.
The selected body returns the supplied natural.
It does not call either supported object.
Dropping the law makes that return refuse.
This establishes law-list-sensitive dispatch.
It does not establish composition with another member's program under a behavioral contract.

The strongest instantiation would make independently supplied components substitutable under explicit obligations.
A consumer would declare the behavior it requires.
Other members would supply implementations after the consumer's installation.
Resolution would expose which implementations currently meet the obligations.
An authorized choice would commit one implementation.
A subsequent governance change would invalidate exactly the affected future uses.
The repair operation would retain the consumer's identity and committed history.
The theorem would relate those operations to one semantics.

Other members' programs are only partially present.
The kernel already invokes separately installed objects through authority-checked nested calls.
LANG-77 provides typed construction of nested-call arguments.
ROM candidates are still fixed at installation.
The Section candidates are first-order data.
The new contract journey invokes no provider.
An open component registry needs candidate records containing a target, an interface and an evidence obligation.
The runtime must bind the evidence to the target actually called.
The existing kernel can support a restricted implementation through its ordinary invoke path.
That implementation still needs the Lang-level resolver and its composition theorem.
General foreign row access also needs an interface discipline beyond `methodReads`' current same-package peer check.
A synchronous returned value is a further requirement because the current nested-call mechanism returns effects, not a provider result to the suspended caller.

The package as a slot is a sketch.
Main has no `Body.relink`.
`Receive.law` still refuses programmed objects with `hasMethods`.
`Integrity.law` still promises that an object's package remains fixed.
Package replacement therefore changes an existing guarantee.
It requires a kernel operation with outgoing approval and incoming adoption.
It requires preservation or checked migration of state and relation schemas.
It requires stable meanings for method indices already named by grants.
It requires an account of pending activity captures and escrow obligations.
An unchanged argument type does not preserve any of those behavioral commitments by itself.
The new package must refine the obligation that consumers rely on, not merely fit an ABI.

The proposed retirement shortcut is inconsistent with the proposed replacement rule.
A package with no methods does not preserve an old callable interface.
A live object linked to an empty package is not a tombstone.
Existing grant and support checks would still encounter a live cell.
Retirement therefore needs explicit semantics or an explicitly different refinement policy.
It is not free relink-to-nothing.

Judged law replacement is already real for data objects.
The old laws judge the proposed list.
Newly added laws judge adoption over the current state.
The quorum generator supplies a policy for that replacement.
This is a transition protocol, not a negotiation semantics for discovering mutually acceptable replacements.
Programmed-object negotiation remains blocked by the package and law immutability rules.
Any new chooser still needs authority accepted by the kernel before its laws run.
A law cannot grant authority merely by approving a proposal.
An implementation needs an authorized proposal-and-approval protocol whose accepted decision drives the replacement operation.
Its theorem must connect the votes to the exact package or law list installed.

The fuse is an atomic agreement on one deal.
It is not a behavioral session contract.
Its current implementation permits an owner to invoke `take` at the root.
The source header explicitly says that one session row is not a fuse.
The caller and `notFuser` work described in BUILT-4 and BUILT-6 is not landed at the reviewed revision.
Even after a caller field lands, caller identity alone will not prove that the caller executed its judged fuse method.
That conclusion requires composition with the calling package's run theorem and the kernel's dispatch tree.
The separate `HasProt` calculus currently supplies no such judgment over the offer generator.

I require three things before calling this a contextual-theory contribution.

First, state and prove one deployed contextual integrity-and-repair theorem.
Give it an independent resolution semantics.
Distinguish observation failure from false evidence.
Distinguish irreversible revocation from reversible predicate failure.
State repair availability with authorization and resource premises.
Connect the theorem to admitted and refused events on an audited log.
Refute it with an implementation that retains stale eligibility.
Refute its repair clause with an implementation that refuses every alternative.
These tests must attack the member's guarantee rather than the spelling of a helper function.

Second, make the common slot semantics earn its abstraction through two substantially different instances.
Use typed component filling as one instance.
Use judged law or package replacement as the other.
Derive their guarantees from the same repair theorem.
Demonstrate a replacement supplied after consumer installation.
Demonstrate a same-typed replacement rejected for violating a behavioral obligation.
Demonstrate that accepted past effects remain fixed.
That would separate a theory of contextual repair from a collection of revocation checks.

Third, provide a member-facing consumer whose contract depends on that theorem.
A document must render its currently justified sections with their evidence.
It must distinguish a stored selection from a currently usable one.
It must expose blocked sections without hiding the rest.
Its withdrawal policy must survive a contributor omitting or substituting the advertised support.
Its repair must use another member's independent alternative without reinstalling the document.
The comparison baseline is an ACL-protected row store with a nullable selected ID.
State precisely which guarantee the common semantics supplies beyond that baseline.
Novelty belongs in that difference.

I would delete the hole-free protocol embedding in `Hosting/Contextual/NanoBridge.lean` and its equivalence-only proof layer.
`ofProg` translates an existing effect program into `Prot` with `Empty` as the hole type.
It therefore cannot exercise contextual filling or repair.
Its presence invites the false inference that the resident inhabits the open contextual theory.
The host's actual retry and lost-reply facts should remain with their deployed subjects.
The research calculus should earn its connection through a nonempty slot instance.

Completed 2026-10-27.
No repository was edited.
No build was run.
