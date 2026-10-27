CRIT-TRUST — 2026-10-27

Nanodregg currently gives a member an audited local history with a cryptographic commitment to its retained prefix.
It gives explicit comparisons against selected positions in other histories.
It does not establish SUNDR fork consistency for ordinary client operations.
Its certificate verifier establishes endorsement under a supplied authority.
It does not establish the validity of the endorsed state.

This review distinguishes the design from the fetched implementation.
I read DESIGN-TRUST.md in full, including BUILT-2 through BUILT-6 and the custody and pinless-adoption addenda.
I read CRIT-SPEC.md, including its receipt and authority objections.
The fetched GitHub main was 5c0c20550e1f9a64f922ee30f1656f66df1f2ccf.
Repeated fetches returned that same commit.
Host/Certify.lean, Hosting/Certify.lean, and Hosting/Proofs/Certify.lean do not exist at that commit.
PROTOCOL-78 is referenced as future work but has no decision entry there.
The brief's claim that these files have landed is unsupported by this source snapshot.
I therefore review the broker's proposed behavior as a design.
I do not report granted_one_head as an inspected theorem.
The code findings below come from source inspection.
I ran no builds or attack tests.
I changed no repository files.

A full member can reject a page whose events do not re-execute under the deployed receiver.
It can reject a page whose claimed terminal chain differs from the chain it computes.
These checks establish execution according to the deployed semantics from the member's accepted start.
They do not establish that those semantics implement every intended authority or language rule.
A member that started from a sponsor-pinned checkpoint inherits the checkpoint's validity from that sponsor.
The checkpoint's earlier history has not thereby been re-executed by the joining member.

The history-binding theorem has a precise conclusion.
Kernel.Proofs.Fold.fold_head_binds assumes two successful folds from the same start.
Equal step counts and equal chains imply equal logs, apart from the stated collision alternative.
Protocol.Head.anchor_binds applies that result to a prefix reached during a comparison.
Neither theorem quantifies over invocations and responses of a distributed client protocol.
Neither theorem says that a client operation occurring in two views has the same preceding history.

That missing statement is SUNDR's essential no-join condition.
Li–Mazières define no-join using a common honest client's operation in accepted result lists.
Their fork* relaxation allows at most one such joining operation from a correct client.
Distinct terminal hash values do not establish either condition.
A forked server can retain distinct hash values while copying later operations between its branches.
The literature's condition concerns shared operations, not convergence of digest values. [Li–Mazières, “Beyond One-third Faulty Replicas in Byzantine Fault Tolerant Systems,” §§3–4](https://usenix.org/legacy/events/nsdi07/tech/full_papers/li/li_html/index.html).

The deployed call format exposes this gap.
Kernel.Receive.Unsigned contains the World origin, the member key, a height window, selected cell and row pins, ranges, a price ceiling, and the body.
It contains no commitment to the member's entire observed prefix.
Command.planUnchecked discovers the pins needed by the operation's derivation.
It does not add the current chain.

Consider two lawful branches at the same height.
Let them differ only in an object outside Alice's next operation's read and write sets.
Let Alice observe the first branch.
Let Bob retain the second branch.
Alice signs a write to an unrelated object whose pinned state agrees on both branches.
The writer delivers that signed call on both branches.
Both branches can admit it.
Their chain values remain different.
Alice's next write can also be delivered on both branches when its pinned dependencies agree there.
This gives two shared Alice operations after unequal prefixes.
It violates the fork* join-at-most-once condition.
It therefore also violates the stronger fork no-join condition.
This is a source-derived counterexample construction, not a claim that an executable attack row was run.

The supported description is retained audited views with explicit prefix comparison.
Calling that fork-linearizability would additionally require a trace statement about operation results and real-time order.
Calling it fork-sequential consistency would still require no-join.
Calling it fork-join-causal consistency would require a causal model and rules for observing and reconciling divergent updates.
None of those follows from Head.
Depot's fork-join-causal model explicitly defines ordering across observed updates. [Depot](https://www.cs.utexas.edu/depot/).
SPORC attaches history information to every operation and combines fork* consistency with operational transformation.
Periodic optional head posts do not implement that protocol. [SPORC, §§2.5 and 5](https://www.usenix.org/event/osdi10/tech/full_papers/Feldman.pdf).

Even the narrower retained-view guarantee has operational premises.
The members must authenticate the same starting World.
Each member must preserve its accepted prefix across restart.
An adversary must not be able to reset the member to an older checkpoint.
The hash functions must resist the collisions named by the proofs.
The signatures require unforgeability under uncompromised keys.
The member's execution and storage boundary must be trusted.
A writer-controlled rollback of the member's own state defeats the retained-prefix argument without breaking a hash.

Comparison establishes agreement only up to the compared position.
An old shared prefix says nothing about a later split.
A writer can withhold the steps needed to reach a supplied anchor.
The result is unreached rather than a fork proof.
The command refuses ahead even when the supplied step equals the member's current step.
Comparing older positions requires retained history through the Store path.
A thin member cannot make that comparison below its adopted base.

Eventual detection requires a comparison path across the split.
An authenticated channel outside the writer's control can supply that path.
A writer-mediated post supplies it only if the writer delivers the relevant post across branches.
A malicious writer can censor those posts indefinitely.
Silence supplies no cryptographic proof distinguishing censorship from disconnection.
CONIKS explicitly requires a means of communication outside the equivocating provider's control.
Certificate Transparency likewise separates signed heads from gossip needed to expose inconsistent views. [CONIKS, §2](https://eprint.iacr.org/2014/1004.pdf). [RFC 9162, §11.3](https://www.rfc-editor.org/rfc/rfc9162.html#section-11.3).

The deployed automatic comparison is weaker than “every post is checked.”
Head.selfPosts iterates over the cells touched by each page step.
Head.selfPost reads every one of those cells from w', the final World after the whole page.
It does not read the state immediately after that particular step.
A conflicting post followed by a higher-step replacement in the same page is inspected as the replacement twice.
Std.head permits a higher-step replacement without proving ancestry.
A granted poster can first submit a conflicting historical chain and then replace it with an arbitrary future position.
The page-local checker calls the future position unreached.
The behind-position checker ignores it because it is ahead.
The earlier conflicting claim has escaped both comparisons.
A replacement with a valid later head can also erase the earlier mismatch from this scan.

The same implementation can misattribute a detected claim.
selfPost combines the final object's head with the member decoded from each earlier touching step.
The printed member can therefore be an earlier toucher who never signed that final head.
Theorems quantified over selfPosts preserve this construction.
They do not prove that its tuple corresponds to the actual post in that step.
This is a defect in the observation being specified.

The Store comparison has a separate coverage gap.
Host.Follow.behindOr converts read errors into none.
Head.forkedBehindPost treats none as no comparison.
This is appropriate as an inability to determine the historical chain.
It is inappropriate as evidence that all absorbed posts agreed.
A post ahead of the current page also has no pending comparison state in the inspected implementation.
The contract needs a named unchecked outcome for these cases.
An absence of forkedPost is not a completed consistency audit.

Attestations give third parties less than the design claims.
A verified attestation proves that the listed key signed those head bytes.
Head.signer checks that the key is current in the verifier's present World.
It does not prove that the signer ran the honest follower.
attestTip_sign constrains one implementation's signing request.
It cannot constrain a malicious member that directly signs fabricated bytes.
Two members' conflicting attestations therefore prove conflicting member claims.
They implicate the writer only with additional assumptions about both members' honesty and starting states.

The current-key rule also makes evidence handling branch-dependent.
A member enrolled only on one fork need not be recognized on the other.
A key rotated on one fork need not be current on the other.
An honestly signed older attestation can fail staleKey.
That failure does not erase its historical evidentiary value.
Archival evidence verification needs authenticated key history.
It must be separate from permission to act with a key now.

Two heads at different step counts are not a compact proof of a fork.
Different chains are expected at different positions on one honest history.
A checker needs a link from the longer history to the shorter position.
The current hash-chain route supplies that link by walking retained history.
Two terminal signatures alone do not supply it.
A transferable witness must carry enough authenticated history or a consistency proof to establish the contradiction.
PeerReview obtains accountability through signed communication records and checks against reference behavior.
A local refusal string plus two member assertions is not that evidence system. [PeerReview](https://www.mpi-sws.org/tr/2007-003.pdf).

A thin joiner currently trusts a sponsor's pin over the downloaded World bytes.
Command.step invokes Head.certifiesWorld only after Thin.accept has checked that pinned download.
The authority is then read from those pinned bytes.
This avoids allowing an unauthenticated candidate state to appoint its own verifier.
It does not remove the sponsor's validity assumption.
Under Authority.none, certifiesWorld deliberately requires no certificate.
Under a positive threshold, it requires endorsement of the downloaded World's head.

The pin must remain until the state commitment is complete.
Head.headOf omits allowance.
World.roots commits the four tries but also omits allowance.
A candidate World can keep the same Head while changing that execution-relevant field.
The design's T3c addendum identifies this defect correctly.
The current sponsor pin binds the omitted bytes.
Replacing that pin with a certificate now would reopen the defect.
A complete commitment would bind state bytes.
It would still not prove that the bound state arose by lawful execution.

Head plus Authority is a common evidence format.
The one-key and threshold-key cases genuinely share a signature-counting verifier.
They also share a quorum-intersection lemma.
That is the extent of the unification currently proved.
Authority.none is excluded by certified.
Its threshold cannot satisfy the intersection premise.
A new World created after a fork is a recovery operation.
It is not an authority instance or a consequence of quorum intersection.
The design itself changes from “three instances” to “a fourth row, not a fourth authority.”
That correction describes the actual boundary more accurately.

The precise committee theorem is weaker than the design's first table.
certified_intersect produces one common signing index when n < 2t.
certified_equivocation adds differing certified bytes for different chains at equal step counts.
Neither theorem proves that the common signer is honest.
For 2f+1 signers out of 3f+1, the required intersection bound is at least f+1.
That stronger cardinality statement is not the conclusion of the inspected theorem.
Distinct indices must also denote distinct keys.
Genesis checks that requirement through Authority.Fits.
A third-party verifier supplied a raw Authority must preserve that validation boundary.
Distinct keys do not establish independent operators or fault domains.

A committee becomes a safety mechanism only with a bound on faulty certifiers.
Honest certifiers must validate the state they endorse.
They must sign a consistent chain of decisions.
Their safety state must survive crashes.
Sign-once at each step count is insufficient across step counts.
A signer can endorse one branch at step ten and another at step eleven without signing twice at either count.
The protocol must check extension of earlier decisions.
If an engine uses rounds, its voting rule must also distinguish tentative votes from final decisions.
HotStuff's locking and commit rules do that work.
A quorum certificate for a proposal is not automatically a finality certificate. [HotStuff, §§4–5](https://arxiv.org/pdf/1803.05069).

The committee deployment also needs available log data.
A certified digest does not let another host reconstruct the state after the writer disappears.
The deployment needs authenticated peer identities and protected independent keys.
It needs state transfer anchored in trusted decisions.
It needs a reconfiguration rule.
It needs recovery from incomplete decisions.
Liveness requires an explicit communication and scheduling model.
Measured failover on one box does not establish availability across independent host failures.

An IBC-style verifier is also more than a stateless signature counter.
The Tendermint client retains trusted consensus state.
It applies trust-period checks to updates.
It validates validator transitions.
It freezes on specified misbehaviour.
Nanodregg's immutable authority avoids an in-place validator transition today.
Its proposed carry moves that problem into authenticating the successor World.
The statement that a verifier never runs the consensus engine is true.
The implication that it therefore needs only genesis and a signature is false. [IBC ICS-007](https://github.com/cosmos/ibc/blob/main/spec/client/ics-007-tendermint-client/README.md).

The design is explicit that no committee engine is deployed.
Its BUILT-3 discussion accurately calls the quorum result a theorem over the object.
Its “MET” table nevertheless assigns operational guarantees to future certificate and committee work.
Those assignments do not follow from the landed theorem.
A committee can be motivated by distrust of a live writer.
Host death is not the only legitimate trigger.
Conversely, trusted failover can address some host failures without Byzantine agreement.
The fault model determines which machinery is required.

A writer certificate is evidence of the authority key's endorsement.
Conflicting certified chains at one step count give checkable key-level equivocation evidence.
The evidence must be checked against an independently authenticated origin-to-authority binding.
The signature does not identify the human who caused it.
After key theft it implicates the compromised key rather than proving operator intent.
A single fabricated signed head need not produce any equivocation witness.
Two incompatible signed checkpoints at different heights need ancestry evidence before the inconsistency is established.
Two signatures also say nothing about which branch a relying party should choose.

The proposed broker improves the boundary only if its protected state survives the writer adversary.
Its own-fold check can restrict a compromised writer process to positions accepted by the broker.
A statement about two grants against one fixed fold does not prove safety across broker restart or replacement.
The required invariant ranges over all signatures ever released under that key.
The anti-rollback record must become durable before the signature is released.
Every later signing request must extend the recorded head.
The broker must reject a conflicting higher-step history as well as an equal-step conflict.
Recovery from a newer base must authenticate that extension.
A cloned broker and copied signing state must not create two independent signers for the same key.
A 0600 file supplies none of these temporal properties by itself.

The design's final custody addendum distinguishes an admitted Store fold from re-execution of signed calls.
That distinction is necessary.
Host.Tail opens a Store and applies its configured record step.
An on-fold signing rule does not turn that reader into a validity auditor.
A broker that follows writer-controlled persisted state needs an authenticated starting checkpoint.
A writer's MAC does not authenticate that checkpoint against the writer itself.
The exact compromise boundary must include permissions on the seed, the anti-rollback record, the decider, and the Store.
Same-uid file permissions alone do not isolate the seed from a compromised process.

The domain theorems prove that the signed message formats are disjoint.
They prevent a permitted signing request from being confused with a different permitted format under the cryptographic assumptions.
They do not constrain a thief who possesses the raw seed.
That thief can sign the call domain as readily as the certificate domain.
Keeping the writer key separate from member authority therefore remains necessary.

The proposed pre-rotation story contains a direct contradiction.
Section 4.4b places certify and certify.next in the same broker key file.
The same section says a thief of that file does not hold the next key.
A thief of the whole file holds both.
Precommitting a successor key protects recovery only against an adversary that lacks the successor secret.
The next secret needs a distinct compromise boundary for that threat model.

Before an authenticated rotation protocol exists, the old writer key remains authoritative for the old origin.
Creating a new World does not revoke signatures for the old World.
A returning third party needs an authenticated rule selecting the successor.
It also needs a rule rejecting stale authority information.
An ordinary carry supplies a new identity.
It does not establish universally recognized succession.
After key compromise, certificate-only consumers can be given arbitrary endorsed roots.
Members retaining audited prefixes still reject unlawful extensions and conflicting replacements.
They remain vulnerable to censorship.
Externally retained evidence can expose conflicting signatures.
Recovery cannot retroactively make already accepted forged receipts valid.

An unsigned foreign head is a grantee's assertion recorded in the receiving World.
The posting call authenticates that local assertion.
It does not authenticate the source World's writer.
Protocol.Foreign.check verifies a receipt against the asserted roots.
It does not call certified.
It ignores the head's chain during receipt verification.
The source name must be supplied by the receiving application's trusted head-object policy.

A dishonest grantee can construct a journal containing an invented transaction entry.
The grantee can compute its root and an inclusion path.
The grantee can post the corresponding head.
No hash collision is needed for the receipt to verify against that invented root.
The result is inclusion in the asserted commitment.
It is not evidence that the source World executed the transaction.
foreign_receipt_sound supplies that connection through its fold and root-equality premises.
Its fold premise is not the stronger Honest audit premise.

A signed-head receipt adds the source authority's endorsement of that commitment.
A lawful-source conclusion still needs replay, a checkpoint trusted for validity, or honest certifiers whose validation rule establishes validity.
“Signs one head per step” is not such a rule.
The corrected custody addendum acknowledges this.
The earlier M7 row and proposed replacement of hr still state the false implication.
The document needs one operative contract rather than contradictory versions separated by appendices.

Adding chain to Std.head does not prove that successive foreign heads extend one another.
headAtAt compares chain only at equal step counts.
A larger step count can carry an unrelated chain.
The receiving World does not possess the foreign log used by the self-head checker.
Two foreign branches can therefore be posted at increasing steps without triggering this law.
The claim that T2 detects foreign forks “at any step” is false of this implementation.

A receipt proves a fact at its named commitment.
It does not prove freshness.
It does not prove availability of the source history.
It does not prove global uniqueness of that history.
It does not provide atomic commitment across Worlds.
Destination-side use-once prevents duplicate consumption only within the destination history that retains it.
Two forked destination histories can each consume the same receipt.
A monotone step count is not a freshness deadline.
Cross-World payments need an explicit policy for source validity, source finality, replay scope, expiry, and recovery after equivocation.

Many Worlds on many hosts are compatible with this evidence format.
Replication of one World's writer is not implemented by that compatibility.
Head does not specify discovery, witness connectivity, data replication, takeover fencing, or recovery authority.
The single-host broker is another availability dependency.
The charter's trusted-operator confidentiality boundary also remains unchanged by signatures.
A malicious operator can disclose bytes it already holds.

“A fork is a new World” is a coherent identity rule.
It avoids pretending that conflicting ordered histories are one sequence.
It is not a merge algorithm.
Exporting their common prefix discards both suffixes from the new live state.
A witness explaining that discard does not preserve the suffixes' effects.
The suffixes can include acknowledgments already acted upon outside the system.
Escrow settlement on one branch can conflict with a refund on another.
Renaming the resulting state does not reconcile those obligations.

Recovery needs a rule for choosing the carried state.
It needs authorization for that choice.
It needs provenance links to the discarded histories.
It needs handling of receipts and external effects from both branches.
Offline editing additionally needs semantics for combining compatible changes.
Disjoint-turn commutativity at one starting World is insufficient for that purpose.
Noncommuting resource decisions require coordination or an explicit conflict outcome.
Nano's charter can exclude those problems.
A design offered as the route to mini's offline and merge ambitions must own them.
Using the new-World sentence as that route is an abdication.

The first change I would require is an operation-level member consistency contract enforced by the actual protocol.
Every relevant signed operation must carry an authenticated history dependency.
The protocol must state whether its execution model targets fork or fork* consistency.
The theorem must range over client views and shared operations.
The implementation must check each actual post at its step.
It must retain unresolved comparisons and durable evidence.
The validation must use two lawful divergent histories.
It must include relaying two later calls from the same member across those histories.
It must include two head updates in one page.
It must include the historical-index failure and restart cases.
A literal impossible digest is not a substitute for these executions.

The second change I would require is a consumer contract separating assertion, endorsement, audited validity, and decided finality.
Each thin or foreign consumer must authenticate the authority independently.
Each acceptance must name its source of state validity.
Pinless adoption must wait for a complete state commitment.
Foreign-head advancement must validate ancestry when prefix continuity is required.
Unavailable historical comparison must remain visibly unchecked.
Transferable fork evidence must preserve the signed statements and their authenticated history links.
The corresponding receipt theorem must retain the validity premise that the deployed consumer actually discharges.

The third change I would require is a recoverable signing authority before anyone relies on writer certificates.
The guarantee must cover the entire broker lifecycle.
Durable signing state must constrain every subsequent signature.
The restart path must establish extension of the last certified prefix.
The rotation rule must authenticate succession for returning consumers.
The successor secret must survive the stated current-key compromise.
The recovery procedure must state the disposition of old-origin receipts.
Until those conditions hold, certificates should be treated as endorsements whose key can fail permanently.

The one thing I would delete is the claim that the existing hash chain already provides SUNDR's no-rejoin property “for free.”
Keep fold_head_binds.
Delete the inference from immutable chain digests to no-join for client operations.
That inference is the false foundation on which the design prices most of the remaining work as comparison plumbing.

Source scope: I read CHARTER.md and the specified PROTOCOL-74 through PROTOCOL-77.1 and KERNEL-69 entries at the fetched commit.
I inspected Protocol/Head.lean, Protocol/Proofs/Head.lean, Protocol/Proofs/Domains.lean, and the relevant Command.Machine paths.
I inspected Kernel/Proofs/AuthorityOf.lean, Kernel.Receive.Unsigned, and the planning and fold definitions used above.
I inspected Lang/StdHead.lean, Protocol/Foreign.lean, Protocol/Proofs/Foreign.lean, Host/Follow.lean, and Host/Tail.lean.
The broker and rotation discussion reviews DESIGN-TRUST's proposal because the named Certify modules were absent from fetched main.

DONE 2026-10-27. No commits landed. The review finds that hash-chain binding is not operation-level fork consistency, the page scanner can miss and misattribute posts, and certificates require explicit validity and recovery assumptions.
