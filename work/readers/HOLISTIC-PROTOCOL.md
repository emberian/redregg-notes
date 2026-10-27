# HOLISTIC-PROTOCOL — a judgment of nanodregg's PROTOCOL layer against the field (2026-10-24)

Reader: the same subopus that wrote READ-PROTOCOL.md yesterday. Repo: `/Users/ember/dev/nanodregg` at
`f9657bd`. No edits, no builds.

Tags: READ (path) for what I read, INFERRED for what I reason to. One count was taken by command, and it is
marked MEASURED.

Scope of "the layer": `Protocol/` (50 files, ~15,900 lines):
- the follower's command machine (`Command/Machine.lean`);
- receipts and settlement (`Receipt.lean`, `Settle.lean`, `Attempt.lean`);
- thin consent and invitations (`Thin.lean`, `Invite.lean`, `Envelope.lean`);
- receipts between Worlds (`Foreign.lean`);
- the conformance rows and their in-process harness (`Rows.lean`, `Rows/*`), about a third of the lines.

---

## 1. What this layer is, in the field's terms

### 1.1 The design it instantiates

The closest named design is a **single untrusted server with client-side re-execution and tamper-evident
history**. That is the line of work from SUNDR (Li, Krohn, Mazières, Shasha, OSDI 2004) through SPORC (Feldman et
al., OSDI 2010) and Depot (Mahajan et al., OSDI 2010), crossed with **accountability by replay**: PeerReview
(Haeberlen, Kuznetsov, Druschel, SOSP 2007), where a node's log is hash-chained and auditors re-execute it
against a reference state machine.

Nano's follower is exactly a PeerReview auditor of one node:
- every logged step is re-derived by the same decision functions the writer used (`absorbStep`, READ
  `Command/Machine.lean`);
- the fold must reach the writer's stated `(steps, chain)` (`absorbPage`, READ);
- a divergence is named at its log position (`eventMismatch`, `chainMismatch`, `cancelForged`).

What nano adds to that lineage is **consent at signing time**. The follower plans the member's call on its own
caught-up World. It hands custody a message to sign only if its own `World.admit` accepts the derived Turn. Then
it re-plans and byte-compares before submitting (`plan`, `planMoved`, `step_submit_planned`; READ
`Proofs/Command.lean`). PeerReview audits after the fact. Nano audits before the signature, so a member never
authorizes an effect its own replica refuses. In SUNDR's terms, the member's own fork view gates its writes. I
know no published system that states this as a theorem about the signing path. It is a real, small contribution.

### 1.2 The pieces, mapped one by one

**The command machine is a defunctionalized continuation held by the client** (READ `Machine.lean`, `State`,
`Reply`).
- `start` and `step` turn a multiparty protocol into a resumable server-side state machine whose state `k` the
  client carries. The four parties are follow, custody, writer and the attempt store.
- The family: Reynolds' defunctionalization (1972), and the web-continuation server line of Queinnec and of
  Krishnamurthi et al.'s PLT web server work.
- That line's first lesson is that a client-held continuation must be authenticated (MAC'd) or it is an input.
  Stateless SYN cookies (Bernstein) and TLS session tickets (RFC 5077) are the systems-world versions of the same
  lesson.
- Nano's `k` is unauthenticated by design (PROTOCOL-64's critique says so).
- Its "k cannot steer what is signed" property is bought by re-deriving everything at every step. That is a
  legitimate alternative to MAC'ing, but it leaves exactly the gap a MAC would close: step 4 settles the call
  bytes `k` names, not the call the argv planned.

**The protocol itself is a session in the session-types sense** (Honda 1993; Honda, Yoshida, Carbone, POPL 2008,
for multiparty).
- One command has a fixed global choreography: sign → log* → plan → sign → submit → settle, with branches for
  expiry, incoming key, cancel and adopt.
- Nano encodes it as a `phase : UInt8` and a list-shaped `acc`, matched by hand (READ `Machine.lean:1184-1379`).
- There is no global type and no projection, and the per-phase shape of `acc` is a convention, not a type.
  This is one of the places nano is furthest behind the art (§3).

**Receipts are Merkle inclusion and exclusion proofs against a held root** (READ `Receipt.lean`).
- That is the Certificate Transparency and verifiable-log-backed-map family: RFC 6962 (Laurie, Langley, Kasper,
  2013), CONIKS (Melara et al., USENIX Security 2015), the Trillian maps.
- The roots digest over four tries (cells, journal, refusals, rows) is an Ethereum-style multi-root header.
- `Receipt.check` is a light-client query.
- The soundness theorems (`check_committed`, `check_refused_sound`, `check_absent_unrefused`; READ
  `Proofs/Receipt.lean`) are the right shape: inclusion or exclusion is true of the World, or the hash collides
  among an EXPLICIT list of inputs. That list form is the correct mechanised statement of a computational
  reduction without a probability monad. It is stronger than what most deployed ledgers ever state, and it
  avoids the pigeonhole vacuity the project has been burned by (MEMORY: "a disjunct provable from the premises").

**Settlement is idempotent at-most-once RPC with a dedup window** (READ `Settle.lean`, `Attempt.lean`).
- The family: Birrell and Nelson's RPC semantics (1984), and the "idempotency key" practice of payment APIs.
- The transaction id is the key, and the journal is the dedup table, bounded by the window (KERNEL-33).
- `Attempt.next` is the client's retry policy as a total decision table exported as data.
- The `open` / `expired` / `forgotten` verdicts are honest about the three states an at-most-once client really
  has. Most RPC systems collapse them.

**`staleBehind` finality is optimistic concurrency control with version pins** (Kung and Robinson, 1981).
- A call carries the versions of what it read (pins). A pin observed on the fold and stale now is stale forever
  (`staleBehind_final`; READ `Proofs/Behind.lean`).
- That is the OCC validation argument turned into a finality rule a CLIENT can apply to its own call without
  asking the server. I have not seen that last step stated elsewhere. It is a nice result.

**Thin consent is a weak-subjectivity checkpoint, with the social trust made explicit** (READ `Thin.lean`,
`Invite.lean`).
- The family: Buterin's 2014 weak-subjectivity post, and trusted checkpoints in light clients generally.
- A sponsor signs a pin, a `(steps, digest)` of World bytes its OWN follow verified (`pinOf`, PROTOCOL-47), and
  the joiner adopts only bytes hashing to it.
- That is precisely the state of the art for bootstrapping without replay, with one improvement over common
  practice: the sponsor pins its own digest, never the server's claim.

**Receipts between Worlds are an IBC-style cross-chain client without signed headers** (READ `Foreign.lean`,
`Lang/StdHead.lean`).
- The head object plays the IBC light-client role (the Cosmos IBC specification line of work), except:
  - its heads are posted by grantees, not signed by A's writer;
  - there is no header chain or consistency proof between two posted heads;
  - fork detection fires only when two posters disagree at the SAME step count.
- `foreign_receipt_sound` states head freshness as a named, undischarged premise (`hr`). That is honest, and
  everything rests on it.

**The rows are scenario-based conformance testing with mutation analysis.**
- The plant discipline is mutation testing (DeMillo, Lipton, Sayward, 1978) applied to the test suite's
  sensitivity. In model checking the analogous concern is vacuity detection (Beer, Ben-David, Eisner, Rodeh,
  1997; Kupferman and Vardi on vacuity).
- `judge_members_pass_iff` makes the judge itself a proved function (READ `Proofs/Judge.lean`). That is more
  rigour than any test framework I know applies to its own oracle.

### 1.3 Where nano matches, trails, or is merely different

Matches the state of the art:
- explicit-list collision disjuncts;
- the sponsor-pinned checkpoint;
- re-execution consent;
- decision tables exported to the unverified shell as data. This is EverParse's posture (Ramananandro et al.,
  USENIX Security 2019) and Narcissus's (Delaware et al., ICFP 2019): verified core, generated readers.

Trails the state of the art:
- no protocol type (session types, or a TLA+ or Ivy spec);
- no trace-level statement over an adversarial environment (Interaction Trees, Xia et al., POPL 2020, are the
  natural Lean-adjacent vehicle);
- no signed heads or consistency proofs for cross-World freshness (RFC 6962's signed tree heads plus consistency
  proofs; CONIKS' gossip);
- no budget typing of frames: layouts bound fields, never totals (READ `Codec/Layout.lean` header; yesterday's
  D1).

Novel or idiosyncratic:
- "settlement is the member's word" (PROTOCOL-46) and the client-side BEHIND finality are novel in statement, if
  not in idea;
- refusals as first-class recorded steps, with an audit name shared by follower and auditor (`cancelForged` =
  `Receive.forgedName`) is a neat idiosyncrasy. The literature would call it a typed abort record in the log,
  and it has no standard name;
- the line-number plant (`.caught m line got`) is idiosyncratic. It is mutation testing whose kill condition is
  pinned to a source position in a scenario. It is fragile in a way the field avoids, by asserting a property
  rather than a position (§3).

---

## 2. The architecture judged

### 2.1 The twelve laws as a design

**Load-bearing and correct.**
- **Law 2 (Lean decides, Rust moves bytes)**:
  - This is the EverParse and Project Everest posture, and it is the right one.
  - In Protocol it is mostly true: the attempt policy is `Attempt.table`, codes and layouts are generated, and
    every refusal name is Lean's (READ).
  - PROTOCOL-64's own finding (step 4's `ok` was Rust's reading of the attempt) shows how the law decays.
    Decisions migrate into the shell through RELAY, not through code: when Rust chooses which bytes to hand back,
    it decides.
- **Law 7 (refusals by name)**:
  - Correct, and well enforced.
  - In this layer it is what made the rows possible at all: every expectation is a name.
- **Law 10 (decisions with critique and meta-critique)**:
  - Rare in practice and valuable.
  - The meta-critiques in PROTOCOL-64, -67 and -69 contain the best self-diagnosis in the layer ("trusting the
    docstring over the function").
- **Law 1 (one of everything)**:
  - Correct as an aspiration and mostly met for shapes.
  - Where it fails in Protocol it fails as STATE duplication inside the continuation rather than as twin
    definitions. Phase 4 carries the call twice, and phase 9 carries `cb` beside the argv (READ `Machine.lean`).

**Aspirational: stated but not what the code does.**
- **Law 4 (a static bound on everything)**:
  - Every field is bounded. No frame, continuation-plus-result, or step reply is bounded as a whole.
  - The law's own words, "a static bound on everything", are violated at the one place the transport refuses:
    the frame total.
  - This is a typing failure as much as a code failure. `Layout` cannot express a total.
- **Law 2 again**:
  - `stepsPerCommandMax` is documented as follow's, but enforced by `client/src/run.rs` (READ).
  - The attempt loop that chooses step 4's `result` is Rust.
  - PROTOCOL-64 argues the loop is "not on the ok path any more". That is true for the RESULT, and false for
    the CONTINUATION: Rust relays `k`, and `k` names the call follow settles.
- **Law 6's "every theorem statement read by a second agent"**:
  - This is a human vacuity check. The census automates part of it.
  - The defects I found were all where a DOCSTRING stated a property and no theorem existed: `cancelAnswer`'s
    `ok`, `atGenesis`'s name, the step bound.
  - The law guards theorems. The failure mode lives in prose that is not a theorem.

**Wrong-headed in light of the field.**
- **Law 11's carve-out, "the conformance ROWS restate the minidregg journeys step for step, because the journeys
  ARE the spec"**:
  - Scenarios are not a specification. They are a finite sample of one.
  - Elevating 45 hand-written scenarios to "the spec" means the project has no object to state refinement
    AGAINST.
  - That explains the absence of a top-level theorem better than any cost argument does (§2.4).
- **Law 8 (proofs in separate files)**:
  - A sound engineering workaround for Lean 4.30's rebuild behaviour.
  - Not wrong-headed, but it is a build-system fact dressed as a design law. Being a law means nobody will
    revisit it when the build system changes.

### 2.2 The layer cuts

Protocol is three things under one name, and only one of them is a layer.
1. **The follower's machine** (`Command/*`, `Envelope`, `Thin`, `Invite`, `Attempt`, `Settle`, `Receipt`) is a
   genuine layer. It sits above Kernel (it calls `submit`, `judge`, `cancel` and `World.admit`) and below Host
   (`Host.Follow.answer` calls `Command.step`; READ `Host/Follow.lean`). The cut is right.
2. **`Foreign`** is a Lang plugin (`Lang.ReceiptCheck`) that Protocol supplies and Host wires in (READ). That is a
   correct dependency inversion. The check belongs to the receipt's owner, not the language.
3. **The rows** (`Rows.lean`, `Rows/*`: ~3,600 lines, a quarter of the directory) import `Host.Serve`,
   `Host.Loop`, `Host.Open`, `Host.Carry`, `Host.Follow` and `Host.Sim.*` (READ `Rows/Writer.lean`,
   `Rows/Loopback.lean` imports).
   - This is a cross-layer integration harness living in a lower layer's directory.
   - It is not an import cycle in Lean (Host does not import Rows), but it is a conceptual cycle: the layer's
     "spec" depends on the layer above it.
   - The rows should be their own top-level component (`Conformance/`), with the declared status of a test
     suite, not of Protocol's spec.

**A cut that is missing: the transport's frame budget.**
- The budget is split three ways:
  - `Protocol.Bounds.frameBytesMax` (Protocol);
  - `Host.Page.budget = frameBytesMax − 1024` (Host);
  - `Host.Wire.bodyMax` and `client/src/frame.rs` (Host and Rust).
- No layer owns "what fits in one frame, and in which direction".
- That is why D1 exists. The Host subtracted 1024 for ITS reply and never knew that Protocol echoes that reply
  inside a frame that also carries a continuation.
- A Frames component with a total-budget type would own it.

**A cut nano pays for and should not have made: `k`.** Making follow stateless per command, with all state in
the client's continuation, buys restart-transparency. Its costs:
- (a) unauthenticated state, answered by re-derivation everywhere;
- (b) the continuation echoing the argv into every frame (D1);
- (c) duplicated state (law 1).

Follow already holds per-member memory (`Follow.download`, `Follow.verified`; READ `Machine.lean:198-208`) that
dies on restart, and commands already restart-class on failure. So statelessness is buying little. See §4.

### 2.3 Single writer, receipts between Worlds, no agreement: the right call?

For this system, yes, and it is a choice, not a deferral, with one exception.

SUNDR and SPORC established that a single untrusted server, plus client-side verification, plus fork detection,
is a coherent and useful point in the design space. CHARTER ("Scope", ruled 2026-10-21) puts nano there
deliberately. And:
- the operator is trusted for confidentiality;
- integrity is checked by every member's re-execution;
- availability is the operator's.

That is a clean threat model, and the layer implements its integrity half thoroughly.

The exception is **fork detection**:
- SUNDR's guarantee is fork CONSISTENCY: a server can show two members different histories, but then can never
  re-join them undetected, and members who compare notes out of band detect it.
- Nano's members never compare heads. Inside one World the Host can fork two members' views indefinitely. Each
  member's follow is internally consistent, so nothing fires.
- The only place heads are compared is the cross-World head object, and only at equal step counts.
- This is not an agreement engine. It is twenty lines of gossip, CONIKS-style: members post or compare
  `(steps, roots)` pairs.
- It is the cheapest missing guarantee in the threat model the charter chose. Without it "members who consent by
  re-execution" consent to A history, not THE history: the same caveat `foreign_receipt_sound` states for B
  holding A's head, true inside a single World too, and unstated there.

### 2.4 The verification method: plants, census, judge, and no top-level theorem

What the method is:
- **Plants** are mutation testing of theorems and rows: a mutation must turn something red.
- **The census** is axiom and statement-shape hygiene.
- **The judge** is a proved test oracle.

MEASURED: `grep -c '^theorem'` over the tree's `.lean` files totals 5,389; Protocol's proofs hold 393.

READ: `Census/Refines.lean` is a CODEC refinement census (each codec refinement carries a lawfulness theorem).
It is not a system refinement.

INFERRED from my greps: there is no theorem anywhere that states "the system refines a spec".

How CompCert and seL4 establish trust:
- CompCert (Leroy, 2006 onward) and seL4 (Klein et al., SOSP 2009) each state ONE top-level theorem against an
  independently written specification: semantic preservation, and functional correctness as refinement.
- Every other lemma exists to discharge it. Trust comes from the TOP statement being small and readable, and
  from the proof being checked.
- IronFleet (Hawblitzel et al., SOSP 2015) and Verdi (Wilcox et al., PLDI 2015) do the same for distributed
  systems:
  - a high-level spec (a linearizable key-value store, or a state machine);
  - a protocol layer proved to refine it;
  - an implementation proved to refine the protocol;
  - with the environment, the network and the adversary, modelled explicitly.

Nano's method inverts this. Thousands of local theorems, each with a plant showing it is not vacuous, and no
statement they jointly discharge. A mechanised-metatheory practitioner would say three things.

1. **Plants establish non-vacuity, not coverage.**
   - A plant proves that a tooth bites. Nothing proves that the set of teeth covers the property the system
     needs.
   - My D2 (cancel's `ok` on the Host's word) is the proof by example. Every theorem around it is true and
     non-vacuous: `sendCancel_host`, `step_host_cancel`, `cancel_never_admits`. The hole is the property nobody
     stated.
   - In CompCert's method that hole cannot survive, because the top statement ("every `ok` the member sees is
     true of the decided log") would fail to discharge.
2. **The theorems are per-step invariants, IronFleet's "inductive invariant" style, missing the trace closure and
   the environment.**
   - `step_keeps`, `step_submit_planned`, `step_settled_ok` and `step_persists_admitted` are the right lemmas.
   - What is missing is the statement over all interleavings of an adversarial environment. That environment is
     a relay that holds `k`, a Host that answers anything, and a custody that signs.
   - D3 (the swapped continuation) is invisible to every step lemma and obvious in a trace statement.
3. **A spec should exist, and for Protocol it is short.** A member-level specification, in prose:

   > For every trace of `start`/`step` against any environment, (i) every message offered for signature is
   > `callMessage u` for a `u` the member's argv plans on a World of its own fold that admits it; (ii) every
   > `done ok` of a writing command implies the member's own World journals the call the argv planned; (iii)
   > every `refused`/`expired` settlement is final against every extension of the writer's log; (iv) the
   > member's World is a fold of the writer's log from the genesis (or the pinned base) it was invited to.

   (i) is mostly `step_submit_planned`. (iii) is `settle_final_never_admits` and `staleBehind_final`. (iv) is
   `step_persists_admitted` with `step_keeps`. (ii) is FALSE today, by D2 and D3.

   Writing this one theorem is the single most informative act available to the layer. It would have found both
   defects, and it would make the 393 Protocol theorems legible as the discharge of something.

The plants are not hollow. They are excellent vacuity hygiene, and better than what most verified-systems
projects do, since those projects rarely mutation-test their specs. But as a SUBSTITUTE for a top-level statement
they are hollow in the precise sense that they cannot detect an unstated property.

---

## 3. The details judged

### 3.1 Three choices I would defend at a top venue

**(D-1) Consent by re-execution, with plan-then-recompare, as a theorem about the signing path.**
- READ `Machine.lean` (`plan`, phase 3's `planMoved`); `Proofs/Command.lean` (`plan_admits`,
  `step_submit_planned`).
- The member's replica must admit the derived Turn before custody is asked to sign. At submit, the call is
  re-planned from the replica's CURRENT World and byte-compared with what was signed.
- So no continuation, relay or stale plan can make the member sign or submit an effect its own replica refuses.
- Positioned against PeerReview (audit after) and SUNDR (fork consistency, no semantic check), this is
  pre-signature semantic consent with a mechanised statement.
- At a venue I would present it as "accountable single-server systems where clients never authorize what they
  have not re-executed", with `step_submit_planned` as the headline lemma.

**(D-2) Client-side finality: settlement from the member's own fold, with BEHIND staleness and explicit-list
reductions.**
- READ `Settle.lean`, `Proofs/Settle.lean` (`settle_final_never_admits`, `settle_refused_absorbed`,
  `WindowedIn`), `Proofs/Behind.lean` (`staleBehind_final`).
- An at-most-once client usually needs the server to tell it a request is dead. Nano's member decides it alone:
  - recorded refusals are final within a window it can bound;
  - the window's passing is final by height;
  - a call whose pinned read-versions its own fold has superseded is final by OCC monotonicity.
- Each finality claim carries its reduction as `CollidesAmong` over an explicit list, or as "S holds a distinct
  call with the same id": a second preimage, said as such.
- This is the strongest part of the layer: a novel combination (OCC validation run by the client as a finality
  oracle), stated precisely.

**(D-3) The retry policy and every wire shape as total, exported decision data, and the test oracle as a proved
function.**
- READ `Attempt.lean` (`next`, `table`, `inputs`), `Frames.lean`, `Proofs/Judge.lean`
  (`judge_members_pass_iff`), `Rows/Run.lean`'s `--harness-control`.
- The client's attempt loop cannot hold a second copy of the rule, because the rule is a table the Lean side
  emits. The rows' verdict function is proved to mean "every line got its declared outcome and the observed ops
  equal the declared ops". And the runner has a known-red control that proves the plant reader is live.
- That is the EverParse discipline (generate the shell from the verified core) extended to policy and to the
  test oracle. It is defensible as engineering methodology, and the known-red control in particular is better
  practice than most CI anywhere.

### 3.2 Three choices I would be embarrassed to present

**(E-1) The protocol has no type: phases are bytes, the continuation is an untyped list, and its authenticity
is argued by re-derivation.**

READ `Machine.lean:220-251, 1184-1379`.
- `phase : UInt8` and `acc : List ByteArray` are matched by position (`| _, 2, [startB, signedB, pagesB, upToB,
  triedB]`); a wrong shape is the catch-all `badState`.
- The continuation is unauthenticated, and its total size is unbounded by any type.
- The defects that follow from this:
  - D3 (step 4 settles whichever call `k` names);
  - D1 (`k` echoes the argv into every frame);
  - law-1 duplication (phase 4 holds the call twice).
- In the field's terms this is a multiparty session implemented as an untyped, unauthenticated, client-held
  defunctionalized continuation. A reviewer from the session-types community (Honda–Yoshida–Carbone 2008;
  Scalas and Yoshida's "Less is more", POPL 2019, on multiparty session type checking) or from the web-continuation community would
  flag all three in the first paragraph.

What a strong PhD student would build:
- a `Phase` inductive indexed by the command kind, each constructor carrying its typed fields (an indexed state
  type, not a list);
- the continuation sealed by a MAC under a key follow holds, or kept in follow's memory and named by a nonce;
- a size index on the frame type, so that "fits a frame" is a type-level fact with one theorem per transition.

The typed phases plus the MAC are about a week of work in Lean for this machine (its ~12 phases are small).
The size-indexed frames are a few more weeks, because `Layout` and the emitter would grow a total-budget notion.

**(E-2) The specification is 45 scenarios with line-numbered plants, and the harness differs from the deployed
transport.**

READ `Rows.lean`, `Rows/Loopback.lean`, `Rows/Params.lean`, `Rows/Run.lean`.
- The "spec" is a list of scripted journeys. Each plant is pinned to a line index, and about a third of the
  plants are harness-side flags that rewrite the deployed machine's output after it runs. `Sys` carries 30
  boolean plant fields (READ `Rows/Loopback.lean:48-110`).
- The harness bounds fields where the deployed transport bounds frames, and pages at a budget a quarter of the
  deployed one.
- So the rows are a thorough sample, at a configuration the deployment does not run, and they cannot fail for a
  property no scenario exercises.
- In the field's terms this is example-based conformance testing promoted to specification. Concretely:
  - A model checker would explore the machine against an adversarial environment. TLA+ or Apalache over a
    transliterated model, or better, bounded exhaustive or random exploration of the LEAN machine itself, since
    it is executable.
  - The QuickCheck line (Claessen and Hughes, ICFP 2000) and its stateful variant, the Erlang QuickCheck state
    machine models of the Arts and Hughes line of work, are the standard tool for exactly this shape of
    protocol: a client state machine against a model server with fault injection.
  - Lean's own property-testing tool (Plausible) could drive `Command.step` with generated results and
    continuations directly.

What a strong PhD student would build:
- a stateful random-testing environment over `Command.step` and `Host.handle`;
- fault injection (drops, reorders, lies, swapped continuations, oversize frames) generated, not scripted;
- properties checked at every step, the trace properties of §2.4 (i)–(iv), rather than per-line expectations;
- the rows kept as regression cases.

A month for the generator and properties. Every one of my D1–D3 would have fallen out of it within the first
week of fuzzing.

**(E-3) Cross-World receipts rest on unsigned heads posted by grantees, with fork detection only at equal step
counts.**

READ `Foreign.lean`, `Proofs/Foreign.lean`, `Lang/StdHead.lean`.
- A receipt is checked against roots that some grantee of B's head object posted.
- The writer of A signs nothing, and no proof links two posted heads.
- `foreign_receipt_sound`'s premise `hr` ("the held head is a fold of A") carries the whole guarantee, and
  nothing in either World discharges it.
- Next to Certificate Transparency (signed tree heads, consistency proofs between any two heads, gossip) and the
  IBC client model (signed headers, verified header-to-header transitions), this is the design before the field
  learned its lesson.
- Nano already has the ingredients:
  - every World has a hash chain, so a step-indexed chain link is a consistency proof;
  - the writer has a key;
  - `Receipt.check` already verifies multi-root paths.

What a strong PhD student would build:
- A's writer signs `(origin, steps, height, roots, chain)` heads;
- the head law requires each new post to carry a chain-consistency proof from the held head, so forks are
  detected at ANY step count, not only at equal ones;
- `hr` is discharged down to "A's writer key signs at most one head per step count", which is accountability,
  not trust.

A few weeks for heads plus consistency checking. The theorem rework is perhaps a month, because
`foreign_receipt_sound`'s conclusion would strengthen to "or A's writer equivocated, with the two signed heads as
the witness".

(Runner-up for embarrassment: refusal names are strings re-parsed inside Lean. `settledName` splits
`Verdict.text` to recover a code, and a Host name and a Lean name share one namespace. READ `Machine.lean:975-979,
1062`. It is small, but a reviewer reads it as "stringly typed core".)

---

## 4. What to do

### 4.1 The one structural change with the best ratio

**Move the command's state into follow, behind an unforgeable, small handle, and give it a type.**
- Follow keeps each live command's state in memory: an indexed `Phase` value (E-1), keyed by a fresh nonce.
- The continuation `k` becomes that nonce, plus a MAC if the handle must survive follow restarts. Today a
  restart loses the base download anyway (READ `Machine.lean:192-197`), and every command already ends
  restart-class.

What it would make true, at once:
- **The frame-budget problem on the continuation side vanishes.** `k` is constant-size, so a resume is page plus
  ~40 bytes, and `Page.budget`'s 1024 slack is real. The step reply that carried the call three times carries it
  once. (D1's continuation half; the per-field typing remains a Frames issue, but now with slack.)
- **Step 4 settles the call the argv planned.** The state holding `cb` is follow's, not the relay's (D3). The
  §2.4 statement (ii) becomes provable for writes: `settled_ok` composed with "the state at phase 4 is what
  phase 3 stored".
- **The law-1 duplications inside `k` disappear**, and so does every "k cannot steer" argument scattered through
  docstrings. They collapse into one lemma: the state is follow's.
- **Phase matching becomes typed.** `badState` stops being a catch-all for shapes and becomes the one refusal
  "unknown or expired handle".

The cost is about a week of Lean: `Follow` gains a bounded map; `step` matches on a typed phase; the theorems
that quantify over `kb` re-quantify over the stored state, and most become simpler. Plus a bound
(`commandsInFlightMax`) and the restart rule. The ratio is the best in the layer: one change closes two DEFECT
classes and makes the layer's headline property statable.

(Cheaper alternatives:
- Fix `cancelAnswer` to settle on follow's World. A day; it closes D2 only.
- MAC the existing `k`. Two days; it closes D3 only, and leaves D1 and the duplication.)

### 4.2 The one thing to stop doing

**Stop answering each finding with a new scripted row and a new harness flag.**
- Each PROTOCOL-NN in the 40s–60s adds a row and a `Sys` boolean that mutates the harness. There are 30 now.
- The rows grow linearly with past bugs and say nothing about the next one. D1–D3 all sit in that blind spot:
  - the harness is not the transport;
  - no scenario swaps a continuation;
  - no scenario has a Host lie about a cancel.
- Freeze the rows as regression cases and put the next finding's effort into a property: a trace statement
  (§2.4) or a generated adversarial environment (E-2's fix).

A smaller, related habit to stop: writing a property in a docstring ("ends `ok` only…", "before follow ends it",
"a World a genesis builds") with no theorem behind it. Every defect I found yesterday lived under such a
sentence. PROTOCOL-64's meta-critique names the bias ("trusting the docstring over the function"), and the
practice continued after it.

### 4.3 Grade

On a scale where A is "publishable as a verified-systems artifact at SOSP/OSDI/PLDI against IronFleet and Verdi"
and C is "a well-tested prototype with proofs of pieces", **PROTOCOL is a B−**.

The local mathematics is at or above the field's bar:
- explicit-list reductions;
- client-side finality via OCC monotonicity;
- consent before signature;
- a proved oracle with a known-red control.

But the layer has no specification it refines, no model of the adversarial environment that holds its
continuation, and no type for the protocol it implements. Its strongest guarantees are true one step at a time,
and its two real defects live exactly where a trace-level statement would have looked.
