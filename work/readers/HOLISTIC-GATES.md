# HOLISTIC — GATES + CENSUS + LEDGER: the verification method, judged (2026-10-24)

Reader: the LEDGER/CENSUS/GATES whole-file reader (READ-LEDGER-CENSUS-GATES.md, yesterday's defect memo).
No edits, no builds. Code claims are tagged READ (path) or INFERRED. Citations name a year only where I am
confident of it; otherwise I say "the X line of work".

The one-sentence version: nano has built an instrument panel for its proofs that is careful, often clever,
and better at proving each gate can fail than most verified-systems projects bother to be. But it points the
instruments at the wrong object. The trust base of a mechanised system should be a small set of statements a
human can read. nano's trust base is all 6,305 theorem statements (SIZE.md: `theorems 6305`, READ) plus every
definition they name. So the gates spend their whole effort guarding a perimeter that was never drawn.

---

## Part 1 — What this layer is, in the field's terms

The layer is three things wearing one name.

### 1a. The judge, plants and controls: mutation analysis applied to the oracle

A "plant" is a mutant that must be killed. A "known-red control" (GATES-15, READ `gates/runs.py:594-604`) is
a mutant of the oracle itself, which the oracle must reject through its own comparator. This is the
mutation-testing tradition, from DeMillo, Lipton and Sayward's "hints on test data selection" (1978)
onward, turned one level up: it asks whether the TEST can fail, not whether the code passes.

Two parts of it are close to the state of the art:
- **Mutations are checked before verdicts are read.** `certificate_plants.py`'s `site moved` and P2's probe,
  and the plants' asserted mutations in `decls_plants.py` (READ), check that a mutation happened before its
  verdict counts. Most CI never does this.
- **The verdict is the last line plus the exit code.** A runner's verdict is never the exit code of a wrapper
  (`runs.py:314-324` requires `rc == 0` AND the exact last line).

For a test infrastructure, that is very good practice.

What has no standard name: running "can this gate fail?" as a STANDING row (`gates/runs.tsv:56-59`) beside
the gate. Mutation-adequacy is usually a one-off study. Here it re-runs at every convergence. I would call
that idiosyncratic-good rather than novel: the idea is folklore, and the discipline of keeping it is rare.

### 1b. The census and the certificate: vacuity detection and statement pinning

- **The axiom census** (`Census/Axioms.lean`, READ) is Lean's `#print axioms` taken over the whole
  environment. That is what Mathlib-scale practice converges on. The independent-checker step
  (lean4checker; the nanoda line of external kernels) is named as the lift in tcb.tsv's lean4 row and is not
  taken.
- **The statement census** (`Census/Statements.lean`, READ) is VACUITY DETECTION in the model-checking
  sense: Beer, Ben-David, Eisner and Rodeh's work on vacuity in temporal model checking (late 1990s), and
  Kupferman and Vardi's semantic definition (1999). A property is vacuous when a subformula can be replaced
  by `true`/`false` without changing the verdict. The field's definition is SEMANTIC. nano's census is a
  hand-written SYNTACTIC recognizer for one vacuous shape, an unbounded pigeonhole equation, and it misses
  neighbours of that shape (yesterday's D3, MEASURED). Here nano is behind the state of the art, and
  knowingly: GATES-20s's critique says "syntax census".
- **The certificate** (`gates/certificate.py`, `Census/Certificate.lean`, READ) pins a theorem's statement,
  axioms, direct supports and one level of vocabulary. Its closest relative is not a paper. It is the
  practice in seL4 and CompCert of freezing the TOP-LEVEL statements and the specification files and
  reviewing every diff to them by hand. nano pins one theorem (`grant_moves_le_cap`) by SHA-256 of a
  `reprStr` DAG encoding. That is the embryo of a trusted-statement file, built as a hash gate instead of as
  a type-checked file.

### 1c. The declaration diff: change-impact analysis for proofs

`gates/decls.py` (READ) diffs the elaborated environments of parent and candidate and demands a message
line per deleted or restated declaration. The literature is proof engineering:
- Ringer, Palmskog, Sergey, Gligoric and Tatlock's survey "QED at Large" (2019);
- the REPLica study of how Coq proofs change;
- the proof-repair line (PUMPKIN PATCH; repair across type equivalences).

Those works treat change as something to REPAIR automatically or to STUDY. nano treats it as something to
DECLARE. Declaring is cheaper and weaker: it records intent and checks nothing about direction, whether a
change strengthens or weakens a statement. And it is blind to definitions (yesterday's D1, MEASURED).

### 1d. The ledger: counted capabilities and a linear payout

- **Grants.** Attenuable capabilities with a counted right (`Right.transfer cap`, carved from the parent:
  READ `Kernel/Receive/Derive.lean:288-302`). They sit in the object-capability and macaroons line (Birgisson
  et al., NDSS 2014), and closer to Biscuit (attenuation with a Datalog of caveats). The count is a
  quantitative caveat, which neither macaroons nor Biscuit have natively. Spend limits of that kind usually
  live in payment-channel and allowance designs (ERC-20 `approve`/`allowance` is the folk version).
- **`grant_moves_le_cap`** (READ `Ledger/Proofs/GrantCap.lean`) is a potential-function argument over an
  audited history (`Std.chain_sum`, with potential `2^64 − left`). That is textbook amortised reasoning, done
  cleanly.
- **The escrow's at-most-one payout.** It is a once-nullifier (Zerocash-style double-spend prevention) plus a
  law under which `settled` is absorbing. The field's modern statement of the same fact is a LINEAR RESOURCE:
  Move (Blackshear et al., 2019) makes "the escrowed coin is consumed exactly once" a TYPE property, and the
  Move Prover line checks the rest. Scilla and Obsidian (typestate) are the other neighbours. nano proves
  linearity extensionally, by chain counting over runs (`escrow_runs_one_payout`, READ
  `Ledger/Proofs/EscrowRun.lean`), where Move gets it from the type system. That is behind the language state
  of the art but entirely respectable as a verified-system statement.
- **Proving a hosted package's property by kernel evaluation** of its actual runs (`decide +kernel` in
  EscrowWitness, LEDGER-14) has no common name. It is closest to translation validation of one program
  (Pnueli, Siegel and Singerman's translation validation, 1998; Necula's variant, 2000), done for a specific
  contract. It is idiosyncratic and useful.

---

## Part 2 — The architecture judged

### 2a. The laws, from where this layer sits

**Load-bearing and correct:**
- **Law 6 (named theorems, one axiom census).** The census over the whole environment is exactly right, and
  the ban on `#guard` follows breadstuffs' measured lesson.
- **Law 7 (refusals by name).** The gates themselves obey it: every red names its object. That is why the
  defects I found yesterday were findable at all.
- **Law 10 (decisions with critique and meta-critique).** Unusual, and valuable. The GATES-20s
  meta-critique ("I wrote the plants first and then a rule that fired on them") is the most honest sentence
  in the layer, and it predicts D3 exactly.

**Aspirational (stated, not what the code does):**
- **Law 6's "every theorem statement is read by a second agent before it lands".** No gate checks it. A
  `RESTATES-MEANING:` line is accepted on its own (READ `gates/decls.py:461-464`).
- **Law 9's "every commit builds".** Under GATES-22 fast mode, a landing builds the reached targets
  (READ `gates/fast.py`). The census, the rows and the plants judge it up to three hours later (READ
  `scripts/pre-push:319-370`). That was a reasonable call by Ember. It turns the gates from preventive to
  detective, and three decision entries still describe them as preventive.
- **Law 2's "Lean decides, Rust moves bytes".** In this layer, `tcb.tsv`'s stdio-leg row trusts Rust for an
  ordering claim (READ `gates/tcb.tsv:54`).

**Wrong-headed, or at least mis-aimed, in light of the field:**
- **Law 12 (size ratchet).** It measures lines and counts. Verified-systems experience (seL4's
  proof-to-code ratio of roughly 20:1 is the famous datum) says proof SIZE is not the cost driver. Proof
  FRAGILITY under change is. A ratchet on theorem count punishes exactly the lemma-splitting that makes proofs
  robust. I would keep the module-dependency ceiling, which measures rebuild cost, and drop the theorem and
  line counts as gates.
- **Law 1 inside this layer.** Three expression serializers (yesterday's B1) shows the law is checked
  nowhere structurally. "One of everything" is a reviewer's law, and this layer has no reviewer gate.

### 2b. The cuts

The CENSUS and GATES layer is cut correctly AWAY from the kernel: Census modules are excluded from the census
(READ `gates/census.py:22`), and nothing outside Census may import them (closure).

It is cut wrongly in one place. The census's Lean (Census/*.lean) is a module, so a change to it is a FAST
landing, while a change to gates/*.py is FULL (READ `gates/fast.py:42-52`). The judge's code is split across
two languages, and only one half is protected by the self-judge rule. The cut should be "anything the judge
executes", not "*.py under gates/".

The LEDGER cut (Ledger/ for the escrow package and its proofs, Kernel/ for the receivers) is right. The grant
cap lives in Ledger/Proofs but is purely about kernel receivers. It belongs beside `spend_reads_back` in
Kernel/Proofs, or in the spec layer proposed in Part 4.

### 2c. Single writer, receipts, no agreement: from where I sit

From this layer's vantage, the single writer is what makes the whole verification method POSSIBLE. Every
theorem is over a deterministic `audit` of one decided log (READ `Kernel/Receive/Audit.lean:68`). That is
Calvin's insight (Thomson et al., SIGMOD 2012: decide the order first, then execute deterministically) taken
to its limit. With an agreement engine, every ledger theorem would need a refinement through a consensus
protocol (the Verdi/IronFleet burden). So it is the right call for a system whose product is checkable
statements, and the charter honestly prices replication as a later phase. It is a deferral only in the sense
that every theorem silently assumes the log is the log: `host_reopen_folds` does not carry `Honest` across a
crash (READ `Host/Proofs/Refine.lean:24-30`).

### 2d. The method: is "every theorem has a plant" sound?

This is the question I was asked above all, and the answer is that the discipline is sound for what it
measures and measures the wrong thing.

**How CompCert, seL4 and IronFleet establish trust.**
- **CompCert** (Leroy, POPL 2006; CACM 2009): ONE top-level theorem, semantic preservation from Clight to
  assembly. The TRUSTED reading is the source semantics, the target semantics and that statement, a few
  thousand lines that experts review. The other several hundred lemmas are untrusted scaffolding. The kernel
  checks them, and nobody needs to read them, plant them or pin them. Csmith (Yang et al., PLDI 2011) found
  bugs in CompCert only in its unverified parts. That is the empirical proof the method works: trust
  concentrated in a small statement survives adversarial testing.
- **seL4** (Klein et al., SOSP 2009): refinement from C to an executable spec to an abstract spec. Then
  security theorems ON THE ABSTRACT SPEC: integrity (Sewell et al., 2011) and noninterference (Murray et
  al., S&P 2013), proved once over a small spec and transported down by refinement. The validation of the
  spec is done by proving properties of it. Those properties are seL4's "plants": they show the spec is not
  vacuous by deriving facts a user cares about. And they are proved against ONE spec, not 6,000 statements.
- **IronFleet** (Hawblitzel et al., SOSP 2015): implementation ⊑ distributed protocol ⊑ a short centralized
  spec, with the spec's size kept deliberately tiny and reviewed. Verdi (Wilcox et al., PLDI 2015) and
  CertiKOS's certified abstraction layers (Gu et al., POPL 2015; OSDI 2016) have the same shape: the trust
  argument is one chain of refinements ending at a statement a human can read in an afternoon.

**What nano does instead.** It has no designated top. It has property theorems, each its own little spec:
- conservation (LEDGER-2);
- `grant_moves_le_cap`;
- `escrow_invokes_one_payout`;
- `chain_binds`;
- the inclusion/exclusion soundness family (READ `Kernel/Proofs/Cells.lean:324-353`);
- and so on, 6,305 of them.

Because none is designated as THE claim, every one is part of the trust base. And a trust base of 6,305
statements must be policed statement by statement. That is precisely what the gates do:
- the statement census looks for vacuous disjuncts in every theorem;
- the declaration diff makes every restatement of any of them a message line;
- the certificate pins the one theorem someone thought mattered most;
- the plants show, per gate, that the policing can fail.

**Is "every theorem has a plant that reds it" sound?** It is sound as a NON-VACUITY discipline: a tooth like
`grant_cap_needs_contiguous` (READ `Ledger/Proofs/GrantCapTooth.lean:141-157`) shows a premise is load-bearing,
which is exactly what a vacuity check should establish. It is hollow as a TRUST discipline, for three reasons:
1. **Non-vacuity of each statement says nothing about adequacy of the set.** Every theorem can be non-vacuous
   while no theorem says the system does what the BAR or the charter says it does. A plant proves "this
   statement is not trivially true"; it does not prove "this statement is the one we needed". CompCert's one
   theorem is trusted because it is the RIGHT statement, not because it has a mutant.
2. **The plants police statements, and meaning lives in definitions.** Yesterday's D1 is the architectural
   point, not a bug: a `def` change moves the meaning of every theorem over it, and no statement-level gate
   can see it. Refinement-based methods do not have this problem, because the definitions under the spec ARE
   the spec, and changing them is a spec change by construction.
3. **The cost grows with the corpus, not with the claim.** Every landing that restates lemmas pays map lines:
   E1 66 lines, P7 111 (READ GATES-20t). That is effort spent on internal lemmas whose statements nobody
   needs to trust.

**What a mechanised-metatheory practitioner would say about 6,000 theorems with no top-level refinement.**
Someone who has maintained a CompCert pass, an seL4 refinement layer or an Iris development would ask, before
reading a single gate: "Which of these statements would you put on a slide as the theorem?" Today there are
candidates but no answer.

Does a top-level statement exist? Partly. `Host/Proofs/Refine.lean` (READ) is titled "`Host ⊑ Kernel`", and
`host_run_audits` (line 246) proves the follower's audit accepts exactly what the Host staged and reaches the
Host's World. That is a genuine refinement theorem, and the right kind. But:
- it ends at the KERNEL, and the kernel is its own specification;
- `receive` and `World.admit` are the implementation, and no abstract machine states what admission should
  permit;
- the crash edge is a fold, not an audited one.

So the chain is implementation ⊑ implementation. The property theorems hang off the bottom of it instead of
off an abstract top.

Should one exist? Yes, and it is smaller than the gates that compensate for its absence. An abstract vat would
have:
- objects as state machines with typed state;
- per-denomination balances;
- grants as counted capabilities in a delegation tree;
- receipts as an append-only log;
- one relation `Allowed(actor, request, s, s')`.

Its theorems would be:
- `audit X w l = .ok w' → AbstractRun (α w) (α w')`;
- conservation, the grant cap over the delegation tree (yesterday's L1), and the one payout, proved ONCE on
  the abstract machine, where they are short;
- plus the Host ⊑ Kernel theorem that already exists, extended across the crash edge.

The trusted reading becomes the abstract machine, the abstraction function and the refinement statement:
perhaps 1–2k lines. Everything else becomes internal. Its statements may change freely, with no map lines,
no census rows and no plants, because the kernel checks that the refinement still holds.

---

## Part 3 — The details judged

### Three choices I would defend at a top venue

1. **Known-red controls through the oracle's own comparator, with the mutation asserted before the verdict is
   read (GATES-15; READ `runs.py:594-604`, `certificate_plants.py:84-96`, `statement_plants.py:224-237`).**
   As an experience paper at ICSE or FSE, or as the methodology section of an SOSP verified-systems paper,
   this is a crisp, generalisable rule. "A gate that cannot go red is not a gate" is folklore. Here it has a
   mechanism, a record of the failures it caught (decision entries 20k, 20s, 20u) and a measured false
   negative it closed: the statement census at f8d04ac read `ok` on three planted vacuous theorems.
2. **The axiom census as one environment-wide pass, plus `native_decide` tied to a TCB row at the toolchain
   pin (READ `Census/Axioms.lean`, `gates/tcb.py:131-139`).** This is the right granularity: one checker,
   every declaration, and an allow list that goes red when stale. It is what a Lean FRO reviewer would
   recommend, and the per-row trusted-for sentence beats anything Mathlib has.
3. **The grant cap as `Std.chain_sum` over the deployed `audit`, with a kernel-evaluated tooth showing the
   contiguity premise is necessary (READ `GrantCap.lean:222-268`, `GrantCapTooth.lean`).** The statement is
   about the real follower path (`audit` in Kernel/Receive, not a proof twin). It uses one generic chain
   scheme rather than a bespoke induction, and the tooth refutes the bound exactly where the premise fails.
   That is how a capability-accounting theorem should look. A CCS or CSF reviewer would want the delegation
   tree (L1) and an abstract spec to state it against. The core is sound.

### Three choices I would be embarrassed to present

1. **The statement census as syntactic vacuity detection for a cryptographic escape.**
   - Why it embarrasses: a reviewer from the vacuity literature would say vacuity is semantic. A reviewer
     from the crypto-verification literature (EasyCrypt; CryptHOL; SSProve; the computational-soundness
     line) would say the deeper problem is that "`P ∨ Collision`" is the wrong statement form: a collision
     disjunct over an unbounded domain is always provable, so the right form is a REDUCTION. You state
     "an adversary that breaks P yields a collision among these explicit, polynomially many queries", or
     you take collision-freeness on a named finite set as an explicit premise. Breadstuffs' lesson
     (`CollidesAmong` over an explicit list) is the right half. The census then tries to police the
     remaining half by pattern-matching Expr, and it misses `¬ Function.Injective` (MEASURED yesterday).
   - What a strong PhD student would build: drop the census rule. Make every hash-binding theorem take
     `CollisionFreeOn hash S` with `S` a term of the theorem's own objects, or conclude
     `CollidesAmong hash S` for an `S` that is a definitional function of the premises. Then add ONE census
     check: no `Collision`-like disjunct at all, which is trivially syntactic and complete. **A week.**
2. **Pinning one theorem by SHA-256 of `reprStr` encodings, one level deep, in a JSON file that is plain data
   (READ `CertificateData.lean:24-58`, `gates/certificate-grant.json`; yesterday's D6).**
   - Why it embarrasses: the field's way to pin a statement is to TYPE-CHECK it against a frozen copy. A
     `Spec/GrantCap.lean` holds the statement and the definitions it uses, written once and reviewed, and an
     implementation module proves `theorem pin : Spec.grantCap := Ledger.Proofs.grant_moves_le_cap` (or
     proves the implementation definitions refine the spec ones). The kernel then checks the whole meaning
     cone, at every depth, for free: `GrantContiguous := … ∧ False` breaks the build instead of passing the
     pin. Hashing encodings re-implements, badly, what the kernel's definitional-equality check does exactly.
   - What a strong PhD student would build: the Spec module and the `pin` theorems for the 5–10 statements
     that matter. **A week to a month,** depending on how much of the kernel's vocabulary must be restated
     abstractly.
3. **A declaration-change protocol over the entire corpus (RESTATES-MEANING lines; GATES-20t), while the
   preventive gates run only post-landing (GATES-22).**
   - Why it embarrasses: it is process standing in for structure. A reviewer from the proof-engineering
     community would note that the protocol checks the DECLARATION of change, never its DIRECTION. It costs
     each restatement-heavy landing 20–111 lines of ceremony, and it guards 6,305 statements of which
     perhaps ten are claims.
   - What a strong PhD student would build: the trusted/internal split of Part 4. Internal lemmas change
     freely; Spec changes are flag days, judged in FULL with a named human reader. If the direction matters
     within the spec, have the gate demand a proof `New → Old` (the new statement implies the old, i.e. it
     is a strengthening) or else an explicit `WEAKENS:` line routed to Ember. That is a small Lean elaboration
     task for the spec file only. **Weeks.**

---

## Part 4 — What to do

### The one structural change: a trusted Spec layer, pinned by the kernel instead of by hashes

Create `Spec/`, a library holding:
- (a) the abstract vat machine sketched in 2d: objects, balances, counted grants in a delegation tree,
  receipts;
- (b) the 5–10 statements the project actually claims:
  - conservation;
  - grant cap over the delegation tree;
  - escrow one-payout over the object's whole life;
  - Host ⊑ Kernel including the crash edge;
  - `audit` ⊑ the abstract machine;
  - the trie inclusion/exclusion soundness at its root.

Then add one module `Spec/Pins.lean` of `theorem pin_X : Spec.X := …`, proved from the implementation.

What it would make true:
- every meaning change under a claimed statement, at any depth, becomes a BUILD error (closes yesterday's
  D1, D2, D6 at the root, rather than one gate at a time);
- the trusted reading becomes a file a stranger can audit in a day;
- the statement census, the certificate and the declaration diff can shrink to "Spec/ changed → FULL judge,
  named reader, and a `New → Old` proof or an Ember-routed `WEAKENS:` line";
- the 6,000 internal lemmas leave the trust base.

Cost: the abstract machine and the refinement from `audit` are the real work. That is a month or two for one
strong agent, because the kernel already has the per-step lemmas (`spend_reads_back_dispatched`,
`object_history_of_audit`, `host_run_audits`, READ) that a refinement proof composes. The pins for the
existing property theorems are days. This has the best ratio in the layer by a wide margin.

### The one thing to stop doing

Stop treating every theorem as part of the trust base. Concretely: stop requiring declaration-map lines
(RESTATES-MEANING / RESTATES / DELETES) for theorems that no claimed statement depends on, and stop writing
per-gate plant machinery to police properties of the whole corpus (the statement census's pattern rules).
Keep the axiom census, which is cheap, environment-wide and correct, and the known-red-control rule for the
gates that remain. Move the plants' effort to theorems ABOUT the spec (seL4's validation method): a
property you can derive from the abstract machine is a far stronger "tooth" against an inadequate spec than a
mutant of one lemma.

### Grade

Against the bleeding edge, split, because the layer is two things:
- **Falsifiability engineering of the gates: A−.** I know of no verified-systems project that holds its own
  oracles to known-red controls as standing rows, with mutations asserted before verdicts. This is genuinely
  ahead of common practice. The minus is for the post-landing gap and the claims that outran it.
- **Verification architecture (what the gates ultimately protect): C.** No top-level abstract specification.
  The one refinement theorem ends at the implementation. The trust base is the whole corpus, so the gates
  defend a perimeter the field would never have drawn.
- **Ledger proofs: B+.** The statements are correct, about the deployed path, with teeth. They are stated
  against the kernel rather than against an abstract ledger, and the cap stops at one grant rather than its
  delegation tree.

Overall: **B−.** The sentence that justifies it: nano has built the most honest instrument panel I have seen
for a proof corpus, and pointed it at 6,305 statements because it never wrote down the ten that it actually
claims. CompCert, seL4 and IronFleet are trusted for the opposite choice.
