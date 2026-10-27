# HOLISTIC-KERNEL — a judgment of nanodregg's `Kernel/` against the field (2026-10-24)

The reader who wrote READ-KERNEL.md wrote this, from the same whole-file context: World.lean, every
Receive/* file, and the statements of the named theorems. There were no edits and no builds. Tags: **READ** (path), **INFERRED** (my
judgment), **MEASURED** (a command run yesterday or today). Yesterday's defects are named here only
where a defect IS the architectural point.

---

## 1. What this layer is, in the field's terms

### 1.1 The one-sentence identification

`Kernel/` is a **deterministic, single-writer replicated state machine whose transition function is
also its specification**. It stores its state in **authenticated maps**: one path-compressed binary
Merkle trie type, instantiated four times, for cells, journal, refusals and rows. Its log is
**hash-chained** and commits each step's state roots. In front of the transition sits an **object-capability
authorisation layer**, the receivers, in which every authority is a grant chain stored *in* the state.
The audit model is **accountability by deterministic re-execution**, not agreement. READ:
`Kernel/World.lean` header (lines 1-20), `World.step`/`World.fold` (1765-1778),
`Receive/Audit.lean` header.

In the classical taxonomy it is Schneider's state-machine approach (1990) with one replica that
writes and many that check. Its nearest relatives sit in three distinct literatures.

### 1.2 Nearest relatives

**(a) Accountable / fork-consistent single servers.** The closest systems ancestor is not a blockchain.
It is SUNDR (Li, Krohn, Mazières, Shasha, 2004) and PeerReview (Haeberlen, Kouznetsov, Druschel,
2007): one untrusted (here: trusted-but-checkable) server, a tamper-evident log, and clients that
detect misbehaviour by re-execution or hash-chain comparison.
- `chain_binds` / `fold_reaches_host` (READ: Kernel/Proofs/Fold.lean:213, :460) are exactly the lemma
  fork consistency needs: one `(steps, chain)` is one log and one World, up to an explicit collision.
- Certificate Transparency (Laurie, Langley, Kasper, RFC 6962, 2013) supplies the receipt half: an
  inclusion or exclusion proof against a signed head. `head_refusal_read`, `head_refused_not_absent`
  and the cell/journal/rows head reads are CT's audit-path lemmas, mechanised.
- **Matches the state of the art.**

**(b) Object-versioned ledgers with optimistic concurrency.** A Turn names every cell it reads with a
pin. Since KERNEL-54 a pin carries a per-cell monotone version, and admission refuses a mismatched
read set by one name (`stale`).
- This is Kung–Robinson optimistic concurrency control (1981), in the specific form of object-versioned
  ledgers: Sui's owned objects (version + digest as the input reference), and Hyperledger Fabric's
  execute–order–validate MVCC (Androulaki et al., 2018).
- `stale_behind_forever` (READ: Proofs/Versions.lean:240) is the monotonicity theorem those systems
  assume and do not mechanise: a version observed on the fold and stale now is stale forever.
- **At the state of the art, and mechanised where the field is not.**
- One deviation is behind the art, and it is the architectural point of yesterday's D1 (§3.2).

**(c) Capabilities stored in the heap.**
- Grants are cells: target, grantee, issuer, an optional parent, and rights at slot keys (READ:
  Receive/Call.lean:379-404).
- `walk` follows a chain to its root issuer and requires the root to be the owner (READ:
  Receive/Authority.lean:33-61).
- Child grants may only narrow; counted rights are carved from the parent's ledger.
- The genealogy is KeyKOS/EROS-style capabilities-as-objects, delegation chains as in SPKI/SDSI (Ellison
  et al., RFC 2693, 1999), and attenuation as in macaroons (Birgisson et al., 2014) and the Biscuit token
  line of work.
- The difference from macaroons/biscuits: the chain is *state*, not a bearer token. Revocation is
  therefore immediate and global (retire one link), at the price that every use pins every link.
- Objects act as themselves (`At.actor`, KERNEL-28 (b), READ: Receive/Derive.lean:198-231). That is the
  ocap answer to the confused deputy: no ambient authority, in Miller–Yee–Shapiro's sense ("Capability
  Myths Demolished", 2003).
- **Sound and conventional.** "Counted rights" (`transfer cap`, `credit cap`, `enroll n` as an
  append-only ledger inside the grant) are a reasonable, unnamed variant of affine or linear
  capabilities: a capability with a fuel that only falls. The literature has the idea; it has no single
  standard construction for it.

### 1.3 Further relatives

**(d) Value as a kernel invariant, with floors.**
- `checkValue` (READ: World.lean:1044-1053) conserves each denomination's balance sum and floor sum
  outside the denomination's birth turn.
- `admit_value` holds for *every* Turn the kernel admits, forged ones included (READ:
  Proofs/Value.lean:402).
- This is the UTXO "value preservation" rule as a pure validation predicate (Cardano's multi-asset
  ledger; Chakravarty et al.'s EUTXO, 2020), transposed to an account model.
- The floor-as-issuance-cap and credit lines (`credit`: a floor transfer, READ: Receive/Ledger.lean:126-139)
  are Ripple/XRPL trust lines with a credit limit, conserved by construction.
- Move (Blackshear et al., 2019) gets conservation from linear types in the *language*. nano gets it from
  a sum check in the *kernel*, which is independent of any receiver or language. For a TCB-minimising
  design I think that is the better place.

**(e) Mechanised cryptographic escapes.** Every hash-dependent theorem concludes `P ∨ CollidesAmong
hash S` over an explicit list S of the inputs the theorem itself compared (READ: Proofs/Fold.lean:30).
- This is Rogaway's "Formalizing Human Ignorance" (2006) done in a proof assistant. You cannot assume an
  unkeyed hash is collision-free, but you can prove that every failure of the claim *exhibits* a
  collision among named inputs.
- The project rediscovered why the naive form fails: `∃ a b, a ≠ b ∧ H a = H b` is a pigeonhole theorem
  at a finite digest, so every escape it guarded was vacuous (KERNEL-56).
- Game-based frameworks (EasyCrypt; CryptHOL by Lochbihler and others) state reductions with
  probabilities and explicit adversaries. nano's symbolic "witness extraction" form is weaker: no
  advantage bound. It is also far cheaper, and it is *correct*.
- **Few production verification efforts do this at all.** This is one of the layer's real
  contributions.

**(f) Failed transactions as first-class, final log entries.**
- `Step.refusal` is a recorded, chain-bound, budget-charged, final refusal (READ: World.lean:229-249,
  1718-1762).
- Ethereum has the same idea: a reverted transaction is included, its nonce consumed, its gas charged.
- nano differs in charging a per-window *count* instead of a fee, and in *proving* finality
  (`submit_refused_never`).
- The per-member and per-World window caps with a count cache validated against its records
  (`refusalsCounted`, READ: World.lean:1701-1716) have no standard name. I judge this idiosyncratic,
  not novel: it is a rate limiter written as a ledger invariant, because there is no fee.

### 1.4 What is closest in the verification literature, and how it compares

It is NOT seL4/CertiKOS-style refinement. There is no abstract spec that the kernel is proved to
implement: `World.admit` is the spec, and compiled Lean runs it (`@[csimp]`
`World.admit_eq_admitImpl`, READ: World.lean:1586). The nearest analogue is the "executable
specification" school:
- the Cardano ledger specifications;
- Verdi (Wilcox et al., 2015), where the system *is* the verified functional program extracted to OCaml;
- IronFleet (Hawblitzel et al., 2015), but without its upper refinement layer.

The proof engineering is Mathlib-flavoured: small lemmas, `simp`-driven, `omega`, no tactic DSL
except one (`stale_only`, READ: Kernel/Tactics/StaleOnly.lean). It has no program logic. The
"Triple"/"Frame" modules (READ: Proofs/Logic/Triple.lean header) define a Hoare triple *over the two
functions*. They explicitly do not build an assertion language. Next to Iris (Jung et al., 2015 onward),
or to separation logic over a heap, this is a deliberately thin logic. It is adequate for a
single-threaded transition, and it will not scale to concurrent residents.

---

## 2. The architecture judged

### 2.1 The twelve laws as a design

**Load-bearing and correct:**

- **Law 1's core ("one transition"):** `World.step` is the only thing that changes a World; follower,
  reopening Host and audit all fold it. This is the single most valuable decision in the kernel. It is why
  `fold_reaches_host` and `audit_ok` can exist at all. (READ: World.lean:1765-1778.)
- **Law 2 (Lean decides, Rust moves bytes):** at the kernel it holds. Every accept/refuse is a Lean `def`,
  and Rust appears nowhere in my layer. This is the right TCB discipline, the "verified core, untrusted
  shell" shape of CertiKOS and IronFleet.
- **Law 3 (bytes end to end, canonical codecs):** the kernel's digest inputs are length-framed or
  fixed-width byte strings. Every injectivity premise is gathered into ONE structure, `Env.Lawful`
  (READ: Proofs/Lawful.lean:41-46). That is textbook-good: the cryptographic and codec assumptions are
  one premise, named, refutable, and discharged at the deployed codec.
- **Law 6 (named theorems, one axiom census, vacuity reads):** correct. In this project it found real
  vacuity (KERNEL-56's pigeonhole), which most verification projects never look for.
- **Law 7 (refusals by name):** correct in intent, and mostly realised (`Reject`, `Refusal`, `Verdict`).

**Aspirational (stated, not what the code does):**

- **Law 1's long tail.** "One of everything" is violated in small ways throughout:
  - three duplicate detectors;
  - twin journal/refused-final checks in `submit` and `checkJournal`;
  - bounds re-checked in `rowsRun`;
  - two refusal namespaces sharing wire names.

  (READ-KERNEL B5-B9.) None is dangerous. Together they show the law is enforced by review, not by
  construction. A law that cannot be checked mechanically will be broken at the rate the swarm writes
  code.
- **Law 7's injectivity:** `Verdict.name` is not injective. Some refusals carry the wrong name:
  `rangeUnpinned` for a missing relation, and `lawDenied` for what is really a stale read (D1).
- **Law 8 (def/proof split):** `World.lean`, the most-imported module, holds theorems (READ:
  World.lean:1570-1595).
- **Law 10 (decisions examined):** as practised, the decision file is a 3,218-line append-only narrative
  whose `Status:` lines lie (KERNEL-17 "open, not pruned"; KERNEL-23 "proposed") (READ:
  decisions/kernel.md). Critique and meta-critique of each decision is a good habit. An append-only file
  in which nothing is ever marked superseded is a bad *artifact*: the reader cannot find the current
  truth without reading the history.

**Wrong-headed, or at least mis-aimed:**

- **Law 10's form.** It produces prose, where what would compound is a *machine-checked* design record:
  a decision entry that names the theorem embodying it, with a gate that fails when that theorem moves.
  ADRs (Nygard's architecture decision records) are the industry's form; the verification community's
  is "the spec is the decision". nano has neither: its decisions are prose beside the spec.
- **Law 12 (size is a ratchet):** fine as hygiene. As a *design* law it rewards deleting lines over
  deleting concepts. The kernel's real complexity is conceptual (four tries, three pin kinds, two refusal
  budgets, counted ledgers in slot ranges), and the ratchet does not see it.

### 2.2 The layer cuts, as seen from the kernel

**The Kernel/Receive cut is right in principle and leaks in one place.**
- Admission (`World.admit`) is generic, defends against forged Turns, and enforces structure: pins,
  bounds, value, rows.
- The receivers decide authority, and derive.
- That is the validation/execution split of EUTXO and Fabric, and it is why conservation holds even for
  a forged log.
- The leak: the read set (pins) belongs to admission, but derivation consumes the Host's current state
  *before* admission validates the read set. The seam is ordered backwards (§3.2). It is the only place
  where the cut costs the design something it promised.

**Ledger inside Kernel (a KERNEL deliverable):** correct. Conservation is a kernel invariant, and
putting it in a separate layer would have made it a receiver promise.

**Lang behind `Program` (READ: Receive/Call.lean:332-346):** a record of four functions that see only
`Pinned` and `RowView`. That is a clean parametricity boundary, and it is what makes `receive_congr`
cheap. Right cut.

**A cut that is missing: storage economics.**
- The kernel has one World allowance, credit on retirement, and no receiver that retires anything but
  a grant. Objects, accounts and members are immortal (READ: Receive/Derive.lean:329 is the only
  `.retire`; Proofs/ObjectHead.lean `audit_object_head`).
- The field's answers are state rent, storage deposits refunded on deletion (NEAR's storage staking,
  Sui's storage fund) and per-principal quotas.
- nano has a budget and no *owner* of the budget. That is a missing concept, not a missing check.

**A cut that should not be there: four instances where one would do.**
- KERNEL-41's amendment made the journal a second trie instance rather than a slot kind. The refusals and
  rows followed as a third and a fourth.
- The price (READ: World.lean:436-580, and the Proofs families `JournalHead`, `RefusalsHead`,
  `RowsHeadRead`, each with `_sep` twins) is four parallel theorem families tied together by
  `HeadSound` (KERNEL-52).
- The abstraction is present, but each instance still re-proves its leaf injectivity and its head read.
- The 10-17 memory on pricing premises explains why one trie was rejected. I think a typed leaf sum
  under one trie would have been one family plus a `Canon` premise, against today's four families. That
  is a judgment call, and it is not clear the project chose wrong.

### 2.3 Single writer + receipts + no agreement

**For the chartered system** (a vat, an operator who sees every byte, members who consent by
re-execution), this is right, and it is not a deferral.
- It is E's vat model (Miller's "Robust Composition", 2006) with a persistent, authenticated log.
- What members need from a single trusted-but-checked writer is fork consistency (SUNDR) and
  accountability (PeerReview), not consensus. The kernel delivers the lemmas for both.

**Two caveats:**

1. Fork *detection* needs heads to flow between members, by gossip or by a witness. The kernel's
   `chain_binds` makes a fork a *proof* once two heads are compared. Whether Protocol compares them is
   outside my layer (INFERRED: I did not read it). Without that, "receipts between Worlds" binds the
   Host to a statement that only one party ever sees.
2. Liveness rests entirely on one Host. The charter says so and prices replication as a later phase.
   That is honest, and the kernel's design (one decided log per World) is exactly what a later
   Raft/Tendermint-style replication would decide over. Nothing in the kernel would have to change. Good.

### 2.4 Plants, judges, census: the verification method

I count about 1,600 `theorem` declarations in `Kernel/` alone (MEASURED: `grep -rn "theorem " Kernel |
wc -l` → 1618; lines, an approximation).

**Sound parts:**
- *Vacuity discipline.* Every statement read for empty premises; teeth (`_needs_*`,
  `*_floor`, `separates_lawful_floor`) proving a premise satisfiable and refutable.
- *Mutation plants.* A deliberate code mutation must turn a named proof or a sim arm red.

  This is mutation testing applied to proofs. It catches exactly the class seL4-scale projects fear
  least and suffer most: a theorem that is true for the wrong reason. Isabelle users do the premise half
  with Nitpick/Quickcheck. nano does it by hand, at a rate I have not seen elsewhere.

**Hollow part:** there is no top-level statement. 1,600 theorems, and none of the form "for every log
the follower accepts, every member-visible fact is X". The project has the pieces:
- `audit_ok` (an audited log is a fold of honest steps);
- `chain_binds` (heads bind logs);
- the head reads (receipts bind state);
- `transfer_authorized` / `effect_at_object` / `effect_at_grant` (who can change what);
- `admit_value` (conservation);
- `submit_refused_never` (finality).

They are not composed. A mechanised-metatheory practitioner would say plainly:
- the kernel needs no refinement theorem, because the transition *is* the spec;
- what it needs is a *security* theorem, in the shape of seL4's integrity and authority confinement
  (Sewell, Winwood, Gammie, Murray, Andronick, Klein, 2011): a cell's content changes along an audited
  log only by a step whose signed call was issued by a principal holding authority over it, through a
  live grant chain, with the change bounded by the right's caps.

Each of the six pieces above is a lemma of that theorem. Today they are 1,600 lemmas of nothing.

**Plants as the trust argument versus CompCert/seL4.** Those projects establish trust by one
end-to-end statement plus a small, audited TCB: the spec, the prover, the compiler for seL4's binary
proof. nano's analogue would be:
- the end-to-end statement (missing);
- `Env.Lawful` and the Lean compiler (present: law 6's census and `@[csimp]`);
- the plants, which are evidence that the statements are not vacuous. Necessary, but no substitute for
  the statement.

"Every theorem has a plant that reds it" is a sound discipline *for the statements it covers*. It cannot
reveal a property nobody stated. Yesterday's D1 is exactly that: no theorem said "a recorded refusal
was not caused by a stale read", so no plant could red it.

---

## 3. The details judged

### 3.1 Three choices I would defend at a top venue

**1. Monotone pins with finality relative to the fold (KERNEL-54, `stale_behind_forever`).**
- Recording every stale refusal (to close A→B→A) cost budget under honest contention.
- The team replaced it with a per-cell write counter in the *entry*, not the cell. Content addressing
  (`romIdOf`, `cellBytes`) stays untouched (READ: World.lean:39-49, 344-347).
- Absent, tombstone and live became three pin domains (READ: World.lean:311-317).
- Finality is stated in the "W0" form: observed on the fold, stale now ⇒ stale forever, with an explicit
  two-input collision escape.
- They split BEHIND (final) from AHEAD (not final) and declined to claim the false general statement.
- Version-based OCC finality is folklore in Sui and Fabric. A mechanised theorem with the AHEAD/BEHIND
  distinction made precise is, as far as I know, not in the literature. This is a workshop paper on its
  own, and a good section of a conference paper.

**2. `CollidesAmong` over explicit input lists, and the pigeonhole discovery (KERNEL-56).**
- The vacuity was discovered: `Collision := ∃ a b …` is provable at any finite digest.
- The repair was principled: every escape names its inputs, and a `Separates` premise gives the clean
  `_sep` form (READ: Proofs/Fold.lean:19-63).
- `separates_lawful_floor` proves that the lawful-`Env` premises neither force nor forbid separation.
- This is the human-ignorance methodology (Rogaway 2006) made routine in a proof assistant, with a
  vacuity theorem about its own premises. Formal-methods venues do not see this often enough, and the
  vacuity lesson generalises to every mechanisation that treats a hash as an injective function.

**3. Kernel-level conservation, independent of the receivers.**
- `admit_value` and `admit_floors` hold of *any* Turn `World.admit` takes (READ: Proofs/Value.lean
  header: "a receiver derived, a package posted, or a forged log carries").
- The receivers can then be wrong about authority without being able to mint.
- Combined with the floor-sum-at-birth rule (`FloorsBorn`, `admit_birth`), the issuance cap is a kernel
  theorem, not a receiver promise.
- This is the right decomposition: integrity of *quantity* in the TCB core, integrity of *authority* in
  the receiver layer. It is cleaner than Move's (linear types require trusting the bytecode verifier),
  and cleaner than Ethereum's (conservation per token contract, never at all).

### 3.2 Three choices I would be embarrassed to present

**1. Derivation runs on the Host's current state before the read set is validated (D1's root).**
- The Turn carries the caller's read set (pins), yet `receive` reads `w.live` (READ:
  Receive/Call.lean:422-423, Submit.lean:32-44). Any refusal it produces is trusted and recorded before
  `touchCheck` compares the pins.
- In OCC terms: the transaction's *abort decision* is made on a snapshot it never read, and then
  committed (recorded, charged, final).
- Every OCC design, Kung–Robinson onward, validates the read set before trusting anything the execution
  concluded. Fabric endorses against a snapshot and validates read versions at commit, and a failed
  validation is "MVCC conflict", never the chaincode's error.
- What makes it embarrassing is not the bug. The project built monotone versions *precisely* so that
  staleness would be cheap and unrecorded, then placed derivation in front of them.
- **What a strong student would build:** make pin validation phase 0 of `submit`. Every pin, row pin and
  range pin is compared before `receive`. Or derive against the *observed* view: the receivers already see
  only `Pinned`, so a view that refuses `stale` on a pin mismatch makes every receive verdict a function
  of the call alone.
- Then `receive_congr` (READ: Proofs/Receive.lean:38) strengthens from "same current cells ⇒ same
  verdict" to "same call ⇒ same verdict, or stale". That is the theorem the consent model actually wants.
- **A week**, most of it moving proofs that currently read `submit`'s order.

**2. Rights and ledgers as magic slot numbers in an untyped cell.**
- A grant is a generic `Cell` whose rights live at slot keys 16, 17, 1024.., 2048.., 2560.. and 4096+m.
  Each counted right is an append-only *series* of slots whose next index is its length (READ:
  Receive/Call.lean:379-404, Authority.lean:67-84).
- Correctness of "the cap falls" then needs a separately proved global invariant, `LedgerContiguous`
  (KERNEL-61), because the encoding admits gapped ledgers that never fall (`gap_never_falls`).
- That is typed data stored in an untyped store, with the type recovered by invariant.
- In capability-system terms the right is not first-class: an authorization logic (Appel–Felten PCA,
  1999; Garg–Pfenning's PCFS line; Biscuit's Datalog) or even a plain algebraic leaf would make
  "attenuation only narrows" and "a count only falls" *structural*.
- **What a strong student would build:** a `Grant` leaf kind with a `Right` multiset and one `Nat`
  remaining per counted kind, updated by one kernel act (`spend`) whose monotonicity is a two-line
  lemma. The contiguity invariant, the slot ranges and their disjointness argument all disappear.
- **A week to a fortnight:** a codec change, one new leaf, a re-genesis. That is the project's own unit
  of "free".

**3. Storage with no owner, and cells that can never die.**
- One World allowance that only falls, retirement credit that reaches only grants, `account` openable
  for any id by anyone, objects with no retire receiver (READ: Receive/Ledger.lean:86-91,
  Receive/Derive.lean:123-136, :329).
- The consequence: a single member can exhaust the World permanently, and the rows parent-retirement
  machinery (`dropHeads`, `checkRowsRemain`, KERNEL-63, the tombstone disjunct of the row stale
  theorems) is unreachable on every audited log.
- In the field, deletion and storage accounting are first-class: state rent proposals, storage deposits
  refunded on delete, per-principal quotas, Sui's storage rebates. A kernel with proved storage
  *conservation* (`fold_potential`, KERNEL-55) and no storage *ownership* has proved a bound nobody can
  act on.
- **What a strong student would build:** a deposit carried *by each cell* and refunded to the retirer,
  and a retire receiver for objects and accounts gated by owner authority (rows already require empty
  relations: `rowsRemain`).
- The kernel half exists. The receiver half and the deposit field are **about two weeks**. The
  *economics*, meaning who funds the World and how, is a design fork for Ember, not a lane.

---

## 4. What to do

### 4.1 The ONE structural change: validate the read set first

**Validate the read set before derivation.** Move the comparison of every pin (cell, row, range)
against the World to the front of `submit` and `judge`, so `receive` runs only on a view equal to the
signer's observation.

What it would make true, for about a week (INFERRED):
- Every recorded refusal is a function of the signed call and the observation it names, never of a race.
- Honest contention never spends the refusal budget (KERNEL-54's stated goal, met for every receiver,
  not only for admission).
- An AHEAD pin is never final (Submit.lean:147's claim becomes true).
- A call with garbage pins costs one pass over its pins instead of a full program run.
- `receive_congr` becomes the consent theorem the design narrates (Call.lean:7-11): a member's own
  follow derives the Host's verdict from the call alone.
- It also gives the missing top-level theorem (§2.4) its cleanest premise. Authority confinement can be
  stated over "the World the signer observed", which is exactly what a signature can attest to.

No other change in the layer moves this many stated properties from narrated to true.

### 4.2 The ONE thing to stop doing

**Stop growing kernel acts, theorem families and sim arms ahead of any receiver that produces them.**
- The kernel is generic over writers, which is right for *invariants*: conservation should hold of a
  forged log.
- It is wrong for *features*. Rows parent retirement, its floor reset, its tooth and its share of the
  overlay seal were all built for a transition no receiver emits. Every one of them is maintenance,
  premise spread and reading cost with no user.
- The same reflex built four trie theorem families with `_sep` twins where one generic family exists
  (`HeadSound`).
- The rule I would adopt: **every kernel act and every kernel refusal must have a receiver path in the
  same commit, or be deleted.** Forged-turn probes stay as *teeth*. They are not a reason for a feature.

### 4.3 Grade

**B+ against the bleeding edge.** The ingredients are each at or ahead of the state of the art:
- mechanised version-based OCC finality;
- symbolic collision-extraction escapes with a vacuity theorem about their own premises;
- kernel-level conservation independent of authority;
- CT-style authenticated reads proved down to the trie.

The composition is behind it in two ways. Its 1,600 theorems have no top-level security statement of the
seL4-integrity kind. And at the one seam the design worked hardest on (observation versus current
state), derivation was ordered in front of validation, so the system records the very race its version
discipline was built to make free.
