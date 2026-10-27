# DESIGN-TRUST — the trust model nano needs to scale toward mini's ambitions: agreement as an object, head comparison as its first instance

Design memo, real 2026-10-26, by FABLE-TRUST. Read against nano `origin/main` = **ad90a47** (every nano
path below read with `git show origin/main:PATH`; the local mirror is 25 behind) and mini
`hbox:/tank/dregg-build/pipeline/warm-base/src` at **334316df** (read-only: `README.md`, `PROJECT.md`,
`docs/GENERIC-SIMPLEX-NATIVE.md`, `docs/agreement/CUTOVER.md`, `docs/DISTRIBUTED-DESIGN.md`,
`Kernel/GenericSimplexEngineSafety.lean`). Inputs: `DESIGN-P6.md` whole, `VERDICT-20261024.md`,
`HOLISTIC-HOST.md`, `HOLISTIC-PROTOCOL.md`, `TOPLEVEL-SPEC.md`, `PROGRAM-20261022.md` §2, nano
`CHARTER.md`. Tags: **READ** (path, at those tips) · **MEASURED** (a command I ran) · **INFERRED** (attack
these first). Nothing in either repository is edited by this memo; §5's first move is built after it, in
its own worktree, and this file records what it measured.

## 0. The answer in one page

**The question Ember has not asked.** What does a member get from nano that it would not get from one
trusted server with a signed log? Today (READ, the readers' §6; TOPLEVEL-SPEC §2.3, §7): the lawfulness
of every step, checked by its own re-execution (`absorbStep`), and finality of its own calls from its own
fold (`settle_final_never_admits`). In the TRUST model, nothing: the single thing a trusted server also
cannot give, **the assurance that two members are looking at one history**, nano does not give either.
Members never compare heads. A writer can serve two members two histories forever, each internally
honest, and no refusal fires.

**What "metamodelling agreement" should mean here (§1).** Not an engine. The object the kernel's theory
is missing is a **HEAD with an AUTHORITY**: a head is `(origin, steps, height, roots, chain)`; an
authority is a rule, fixed at genesis, for which signatures make a head *the World's* (none / the
writer's one key / 2f+1 of 3f+1); and beside it, under every authority, a member's **ATTESTATION** of its
own head, signed with the key it already holds, meaning "my follow's fold sits here". The theorems are
about heads and signatures, quantified over the authority; the engine (Simplex) is what *produces*
certificates under the committee authority and is never consulted by a verifier. That is the lesson of
Certificate Transparency (RFC 6962: signed tree heads + consistency proofs, verified by monitors that
never run the log), of IBC light clients (verify headers, never run Tendermint), and of SUNDR (Li,
Krohn, Mazières, Shasha, OSDI 2004: one untrusted server, fork consistency from signed version
structures). One-writer, committee and "a fork is a new World" are the three instances: the rule with no
certifier, the rule with threshold 1 of 1 or 2f+1 of 3f+1, and the recovery act when two heads under
one rule are not on one fold (export the common prefix, re-genesis, carry the witness).

**Head comparison first (§2): yes, and it is the first instance, not a side road.** CORRECTED (CRIT-TRUST,
real 2026-10-27; PROTOCOL-82). This paragraph used to say nano already had the *no-rejoin* half of SUNDR's fork
consistency "for free" because the chain is a hash chain over the whole log. That inference is false and is
deleted. What `fold_head_binds` (READ `Kernel/Proofs/Fold.lean:428-434`) proves: two successful folds from one
start with equal step counts and equal chains have one log, up to a collision among listed inputs. It is a
statement about two folds. It says nothing about client operations: a signed call carries no commitment to the
prefix its signer saw, so a writer can admit one member's signed call on two branches whose chains differ, and
SUNDR's no-join (and fork*'s join-at-most-once) fails. What nano gives is **prefix agreement on comparison**: a
member that compares another member's stated head `(s, c)` with its own fold at step `s` learns that their logs
agree up to `s` (up to the collision), or gets a named refusal and a witness. A member that never compares has
only its own audited chain. Detection needs a comparison path across the split: a channel outside the writer's
control, or posts the writer delivers, which it can withhold indefinitely. T1 adds the compare act (nothing
deployed put another member's position into `absorbPage`) and the witness object (a signed statement "I am at
(s, c)"); together they make this true: *a member can establish, against any other member whose stated head
reaches it, that they share one history up to a step, or obtain a signed witness that they do not.* Operation-level
fork consistency needs every signed call to carry its signer's head, compared on absorption (SPORC's route to
fork*); it is not built (PROTOCOL-82 names it).

**What mini's ambitions require (§3).** Of nine member-facing guarantees mini's README and PROJECT.md
promise, the single writer with receipts meets four, head comparison (T1–T2) meets two more on comparison, certified
heads (T3, which needs Ember's signing-seed ruling) meets two, and ONE — "work on offline branches and
merge without erasing provenance" — this model does not meet and should not pretend to: it is a
different step-logic (mini's own `DISTRIBUTED-DESIGN.md` §0: independence, I-confluence), and the
charter's "a fork is a new World" is the honest answer until a demoland row demands otherwise.

**The price (§4), measured where this lane could measure.** Of TOPLEVEL-SPEC's five claims, ONE HISTORY
gains its act (A2′ becomes statable of the deployed system) and CONSENT gains a seventh clause; INTEGRITY,
DURABILITY and THE BELL do not change statement. Kernel theorems gaining a premise: **0** (nothing
touches `World.fold`; DESIGN-P6's §2 measurement carries over because the head lives beside the fold
exactly as P6's decision did). Protocol: `absorbPage` gains one binder (an optional anchor), restating
its direct consumers by binder, not hypothesis. Re-genesis: none for T1; T2 (`Std.head` gains `chain`)
is a `lang!` flag day; T3 (the writer's certificate in the `log` reply and in genesis) is `host!` +
`protocol!` and every Store re-geneses. The Store signing seed is needed FIRST at T3 and not before; the
question for Ember is stated in §4.4 in system terms.

**The verdict.** Build head comparison now as the first instance of the head-with-authority model;
hold the committee and the engine behind the trigger DESIGN-P6 named (a row whose World must outlive
its host), which no consumer has pulled; and let the Store signing seed be decided on T3's concrete
shape, where it buys a non-repudiable writer head for third parties and thin joiners rather than
anything a member needs to detect a fork.

---

## 1. WHAT "METAMODELLING AGREEMENT" MEANS HERE

### 1.1 The gap, said in the kernel's own vocabulary

Every landed theorem about history is stated over a FREE log: `World.fold E g l = .ok w` with `l` a
binder (MEASURED by DESIGN-P6: 114 statements, 0 that name a writer). The kernel knows *this log is
honest* (`audit_ok`, `Honest`, READ `Kernel/Proofs/Audit.lean:275`) and *one (steps, chain) is one log*
(`fold_head_binds`). It has no object for *this log is the World's*. That object lives nowhere: the
follower takes it from the writer's stated `(steps, chain)` on each page (`absorbPage`, READ
`Protocol/Command/Machine.lean:495-507`, `chainMismatch` when its own fold does not reach the statement),
the thin joiner takes it from a sponsor's pin (`Thin.accept`, PROTOCOL-47), the foreign World takes it
from a grantee's post (`Std.head`, PROTOCOL-65). Three places, three unsigned-or-differently-signed
authorities, no theorem across them. That is what "agreement is not an object of the theory" means
concretely.

### 1.2 The object: Head, Attestation, Authority

```lean
-- Protocol/Head.lean (NEW, T1 lands the first two; T3 the third)
/-- A position of one World, as every party states it: the World, its step count (the chain's index,
    KERNEL-47), its height, its roots digest (what receipts check against) and its chain (what
    `fold_head_binds` binds). The roots and the chain are both carried because they answer different
    questions: a receipt is a path against the roots; one history is equality of the chain. -/
structure Head (D : Type) where
  origin : D
  steps  : Nat
  height : Nat
  roots  : D
  chain  : D

/-- A member's statement that its OWN follow's fold sits at `head`: signed by the member's current key
    under `domHead` (the seventh signing domain, pairwise disjoint from the six of
    `Protocol/Proofs/Domains.lean`). Not an authority: it says what one member holds, never what the
    World is. -/
structure Attestation (D : Type) where
  head : Head D
  member : D
  key : ByteArray
  signature : ByteArray

/-- Who may CERTIFY a position as the World's, fixed at genesis (T3+). `certifiers = []` is today:
    nobody certifies, the writer's page is its bare word and members audit. One key with threshold 1
    is the lock writer with a signature (DESIGN-P6 §1 "f = 0"). `3f+1` keys with threshold `2f+1` is
    the committee. -/
structure Authority where
  certifiers : List ByteArray
  threshold : Nat

/-- A certified head: `threshold` distinct valid signatures by certifiers under `domCertify`. -/
structure Certificate (D : Type) where
  head : Head D
  sigs : List (Nat × ByteArray)
```

**What a Turn becomes.** Nothing. A `Step` is a Turn or a recorded refusal (READ
`Kernel/World.lean:246-249`); heads, attestations and certificates are NOT steps. DESIGN-P6 §1 put the
decision frame beside the fold so that KERNEL's 224 `World.fold` lines see nothing, and §7.1 made
"a Kernel theorem gains `hd : Decided …`" the stop condition. This memo keeps both: if a builder finds
themselves adding a `Head` premise to a Kernel theorem, the design has leaked.

**What a receipt becomes.** Its shape is unchanged (`Protocol/Receipt.lean`: txId, four roots, answer,
two paths). What changes is what it can be *paired with*: today "the head is the member's own folded
World" (READ Receipt.lean header: "a relayed head would need its height bound to the roots"). A receipt
plus an attested or certified head of the same `(steps, roots)` is a **transferable proof**: a party
that holds no World (the phone, cv 01a14d95-36b0; a foreign World under E5) checks the signature, then
`Receipt.check` against the head's roots. The receipt theorems (`check_committed`, `check_refused_sound`,
`check_absent_unrefused`) are untouched; the head's provenance is the premise they always had, now a
signed object instead of a docstring.

**What a head becomes.** `World` has `steps`, `height`, `chain` and `roots X.env` (READ
`Kernel/World.lean:268-292`); the `log` reply states `(steps, chain)` and the base's `(steps, digest)`
(`logPage`, Machine.lean:470-488); `receipt CALL` prints `head STEPS HEIGHT ROOTS` (Machine.lean:957);
`Std.head` holds `{height, roots, steps}` keyed by steps (READ `Lang/StdHead.lean:1-20`). Four partial
spellings of one thing. `Head` is the one spelling; T2 moves `Std.head` to it (adding `chain`), T3 the
`log` reply.

**What a member's signature becomes.** A member key signs six shapes today, each under its own domain
with pairwise-disjoint theorems (READ `Protocol/Proofs/Domains.lean:1-13`: call, possession, envelope,
whoami, invitation, cancel). It gains a seventh, `domHead = "nanodregg/protocol/head/v1"`, six more
disjointness pairs, and ONE consent theorem in the shape of C(i): follow offers custody a head message
only for follow's OWN World's head after a catch-up (`attest_own_head`). An observer custody that signs
envelopes only (HOSTING-17 §7, CLIENT-22) never signs a head (`head_not_envelope`), so a timer-driven
`sync` stays an observer and `sync --attest` needs a member's custody.

**What a writer's or replica's signature becomes.** `domCertify`, over the same `Head` bytes. It does
not exist until T3 and the seed ruling (§4.4). Law 2 keeps it in Lean (`Codec.Ed25519.sign` exists,
READ `Codec/Ed25519.lean:264`, `sign_verifies` proved).

### 1.3 The theorem the object is for, quantified over the authority

```lean
/-- Two heads of one World that are each ON A FOLD from the same start are prefix-related, or the two
    folds collide among their listed inputs. This is `fold_head_binds` lifted from "equal (steps,chain)"
    to "the smaller step count's chain is on the longer fold" — the shape every instance needs. -/
theorem heads_prefix {X : Ctx D} {n} (hE : X.env.Lawful n) {g w₁ w₂ : World D} {l₁ l₂ : List (Step D)}
    (h₁ : World.fold X.env g l₁ = .ok w₁) (h₂ : World.fold X.env g l₂ = .ok w₂)
    (hs : w₁.steps ≤ w₂.steps) (hc : chainAt X.env g l₂ w₁.steps = some w₁.chain) :
    (∃ l, l₂ = l₁ ++ l) ∨ CollidesAmong X.env.hash (foldPres X.env g l₁ ++ foldPres X.env g l₂)
```

Under each authority the SAME statement reads differently, and that is the point:

| authority | "on a fold" is discharged by | a violation is | who is named |
|---|---|---|---|
| none (today + T1) | each member's own audit (A1: `OneHistoryMember`) | two attestations whose chains are not prefix-related | the only party that orders: the writer (or a sponsor whose pin is off the chain) |
| writer, 1 of 1 (T3) | the writer's signature + the member's audit | two certificates at one `steps` with different chains | the writer, non-repudiably, to anyone with its key |
| committee, 2f+1 of 3f+1 (T4) | 2f+1 signatures, each a re-derivation (DESIGN-P6 §3: the vote is an audit) | two certificates at one `steps` with different chains | f+1 named signers (quorum intersection) |

"A fork is a new World" is the fourth row of the table, not a fourth authority: it is what happens to
the World when the right column fires. The common prefix of the two folds is well defined (both folds
agree up to the step before the fork, by `fold_head_binds` at that step), `host export` of the World at
that step is the honest state, and a carry (`Carried`, READ `Kernel/World.lean:286-300`) re-geneses
under a new origin. The only addition the fork act wants is that the carry's origin input may carry the
witness (two signed heads), so the new World's genesis says why it exists. That is one field in
`CarryInput` (`Kernel/Receive/Follow.lean:46-57`), a `domOrigin` bump, and it is T2b, not T1.

### 1.4 The alternatives, judged

- **An engine bolted on (Simplex, Raft, Tendermint).** No, and DESIGN-P6 already measured why: mini's
  Generic Simplex is 7,282 lines of which ~80% is view-change (READ P6 §0.3), liveness is "NOT a
  theorem here" twice in its own doc, and the one consumer that would need it (a World outliving its
  host) does not exist in any row. The engine is the liveness machinery of the committee authority.
  Verifiers, members, thin joiners and foreign Worlds need only certificates. Build the object first;
  the engine, if ever, produces instances of it.
- **Fork consistency with one server (SUNDR; fork-linearizability, Cachin–Shelat–Shraer 2007).** CORRECTED
  (CRIT-TRUST). Not an instance today. SUNDR's version structures are per-user signed vectors attached to EVERY
  operation. Nano's chain commits the whole log, so a signed `(steps, chain)` names a position as SUNDR's
  structure does, but nano's calls do not carry one, so SUNDR's no-join does NOT hold: the writer can deliver one
  signed call on two branches. What carries over is detection when stated heads are compared (T1, T2). The
  operation-level form attaches the signer's head to every call and compares it on absorption (SPORC, fork*);
  PROTOCOL-82 names it as the next protocol change.
- **A DAG of Worlds with receipts (E5, landed).** Orthogonal and already half-built. E5 moves
  KNOWLEDGE between Worlds; it never says which history a World has. Its one undischarged premise
  (`hr` in `foreign_receipt_sound`, READ `Protocol/Proofs/Foreign.lean:72-86`: "the held head is a head
  of a fold of A") is exactly a head's provenance. T2 gives `Std.head` the chain so forks are seen at
  any step count; T3 lets a certified head discharge `hr`. The DAG consumes this model; it is not a
  substitute for it.
- **CRDT-style convergence for the commuting fragment (`admit_comm`).** `admit_comm` exists (READ
  `Kernel/Proofs/RowsComm.lean:791`, with `_trie` and `_rows` forms) and says two Turns that retire
  nothing, touch disjoint cells and leave heads unpinned commute AT ONE WORLD. It gives no merge of two
  logs, and the charter's refusal of merge stands for the reason PROGRAM §2(c) listed: every theorem
  over fold extensions loses its object. Mini's `DISTRIBUTED-DESIGN.md` §0 is the right diagnosis: this
  is a second step-logic (independence: I-confluence, join-semilattice merges) beside ordering, with its
  own classifier (which guards are monotone, which force consensus). It is a research line, not a trust
  model, and the trust model here must not be shaped to leave room for it: a World is one log.
- **A hierarchy of Worlds with agreement only at the root.** This is the head CHANNEL, not a trust
  model. A parent World holding its children's heads (as `Std.head` objects) is exactly where members
  of a child would compare, and the writer of the parent is the same question one level up. Useful as
  deployment shape (one "registry" World per host, T2 posts child heads into it); it adds no authority.

**So the abstraction is right, with one honesty clause.** `Head` + `Authority` is the right object
because every party that today trusts a position (follower, thin joiner, foreign World, phone) can be
rewritten to trust a *signed head under the rule*, and the rule is a genesis parameter so a World says
what it means by "its history". The honesty clause: with `certifiers = []` the model's assurance is
prefix agreement for members whose stated heads are compared, which is LESS than SUNDR's (no operation-level
no-join, PROTOCOL-82) — detection on comparison, not prevention. Prevention of forks needs a
threshold that no single host meets, which is the committee row, which is the engine, which no row
asks for.

---

## 2. HEAD COMPARISON FIRST, OR NOT

### 2.1 What nano has, measured against SUNDR's definition

SUNDR's fork consistency: the server may show two clients different histories, but then can never show
either a history that includes the other's later operations without one of them detecting it. Two
halves: **no rejoin** and **detection**.

- *No rejoin* — nano does NOT have it for operations. CORRECTED (CRIT-TRUST; this bullet used to infer it from
  `fold_head_binds`). What `fold_head_binds` gives: two members whose folds diverged at step k hold different
  chains at every later step, so no single page with a stated `(steps, chain)` is absorbed by both. That binds
  pages and heads, not operations. A signed call names no prefix (`Kernel.Receive.Unsigned`: origin, member, a
  height window, pins, ranges, a price ceiling, the body), so the writer can admit Alice's next call on both
  branches when its pins agree on both, and a page on each branch carries it, each with its own chain. Two shared
  operations after unequal prefixes is a join, which SUNDR's fork consistency forbids and fork* allows at most
  once. A writer that forks M1 and M2 keeps two logs and may copy calls between them.
- *Detection* — nano LACKS it. `host check --anchor STEPS:CHAIN` (READ `Host/Check.lean`) is this
  exact comparison, for the OPERATOR against a Store. `Std.head` detects a disagreement between two
  POSTERS of a foreign head, at equal step counts only, by law (`forkedHead`). Inside one World no
  member act takes another member's position.

So T1 builds the act and the witness. Operation-level fork consistency is a separate protocol change, not
built (PROTOCOL-82).

### 2.2 The first move, exactly (T1; built in this lane)

One verb, `sync`, gains three forms (the verb count stays 20/20; `sync` already means "relate my fold to
the writer's tip"):

- `nd sync --to STEPS:CHAIN` — catch up as today; **while absorbing, when follow's fold reaches step
  STEPS, its chain must be CHAIN**, else the step refuses `forkedWorld STEPS` by name, nothing past it
  absorbed (what was absorbed before it is kept, as every page refusal keeps). A position follow is
  already past when the command begins is refused `ahead STEPS` before anything is sent: the ahead
  party cannot compare purely (its World holds only the current chain) — the other member runs the
  check, or the member runs `host check FOLLOWSTORE --anchor` on its own Store, which exists. Passing it
  prints `shared STEPS` beside the usual height/chain/roots; a writer whose tip is below it prints
  `unreached STEPS`.
- `nd sync --attest` — catch up, then ask custody to sign `headMessage` of follow's World as it stands
  (the shape of `invite`: catch-up, then one `.sign`, Machine.lean:1296-1320 `.invite` arm), and print
  `attest HEX`: the `Attestation` bytes.
- `nd sync --check ATTESTHEX` — decode; the signer must be a live member of follow's World and the key
  its CURRENT one (`currentKey`, as `Envelope.check` requires), the signature must verify under
  `domHead`, the head's origin must be this World; then it is `sync --to head.steps:head.chain`.

The comparison is a walk over the page's steps AFTER `absorbPage` (`Head.anchorCheck`), not a
parameter of it: `absorbPage` already returns every step it took with the roots digest after it
(`Persist.steps`, the record's shape), and `chainOf` over those pairs IS the chain `World.fold`
stamps (`RootedFold.chain`, READ `Kernel/Proofs/RootedFold.lean`). So the chain at every past step
of the page exists purely, follow's `absorbPage` keeps its signature and every consumer its statement,
and the check is one function with its own theorems. No Store access, no new state in `Follow`, no
kernel change. The protocol is "the member behind checks": between two members, the one with the
smaller step count passes through the other's position. If both are past each other's attestation
(an old one), either asks for a fresh attestation, or `host check --anchor`. (BUILT in this lane as
PROTOCOL-74; the first draft put the check inside `absorbPage` and would have restated ~12 statements
by binder for nothing: the memo's §4.1 counts are from the landing.)

**Refusals by name (law 7).** `Command.Refusal` gains `forkedWorld (steps : Nat)` (its own exit class,
restart-class is wrong: a fork is final for this follow against this writer) and `Attestation`'s own:
`badAttestation`, `notMember`, `staleKey` (signed by a key that is not the member's current one),
`badHeadSignature`, `otherWorld` (reused name shape of `Invite.Refusal.otherWorld`).

**The theorems (Protocol/Proofs/Head.lean, NEW).**

1. `absorbPage_anchor_ok`: `absorbPage X w evs steps chain base (some a) = .ok (w', ts, _)` and
   `w.steps ≤ a.steps ≤ w'.steps` ⇒ the fold of `evs` from `w` passes a World `v` with `v.steps = a.steps
   ∧ X.env.bytes v.chain = a.chain`. (The anchor is ON follow's fold.)
2. `absorbPage_anchor_forked`: the refusal `forkedWorld s` is returned only when the fold reached a
   World at step `s` whose chain is not the anchor's. (The refusal is never free.)
3. `anchor_binds` (the member-facing statement; `heads_prefix` of §1.3 at this act): follow started
   from `g`, reached `w'` by its own audited fold (A1, `OneHistoryMember`), and passed the anchor `(s,
   c)`; the OTHER member's World `wg` is an audited fold from `g` with `wg.steps = s ∧ wg.chain = c`.
   Then follow's fold up to step `s` IS the other member's log, or the two folds collide among their
   `foldPres`. Proof: `fold_head_binds` at the prefix.
4. `attest_own_head` (consent, C(vii)): every `.sign msg k` a `sync --attest` run hands out with `msg`
   beginning `domHead` has `msg = headMessage X (headOf w')` for the `w'` follow's own fold reached in
   that run. Same shape and proof route as `step_submit_planned`.
5. `check_attestation_ok`: `Attestation.check X w a = .ok ()` ⇒ `a.member` is live in `w` with current
   key `a.key`, `a.head.origin = w.origin`, and `Ed25519.verify a.key (headMessage a.head) a.signature`.
6. Domains: `head_not_call`, `head_not_envelope`, `head_not_possession`, `head_not_whoami`,
   `head_not_invite`, `head_not_cancel` (six `append_ne_of_byte` instances).

**What the witness is.** Two attestations `a₁, a₂` of one World, both `check`-ok against a third
member's World (so both signers are members and both signatures verify), with `a₁.steps ≤ a₂.steps`,
such that `sync --to a₁.steps:a₁.chain` by the holder of `a₂`'s fold refuses `forkedWorld`. By (3),
(5) and A1, the two signers' folds are not prefix-related from the common genesis; by `attest_own_head`
each signed only what its own audit reached; so two honest audits of pages one writer served diverge —
the writer served two histories (or a sponsor's pin started one member off the chain, which the pin's
signature attributes). CRIT-TRUST: this implicates the writer only if both members ran the honest follower from
one authenticated start; a member can sign fabricated bytes, so two conflicting attestations prove two
conflicting MEMBER claims. And two heads at different step counts need a link from the longer history to the
shorter position before they show a fork. The witness is checkable by anyone holding the genesis and the two members'
keys. That is more than SUNDR gives (SUNDR's detection is a client's local observation; here the
evidence is two signatures), and less than a writer certificate gives (the writer is implicated by
exclusion, not by its own signature): §4.4.

**The rows and plants.** A Protocol row `fork`: two followers of one writer; the harness's writer serves
member B a forged event at step k (the `lieLog`-class plant already in `Rows/Loopback.lean`'s `Sys`
fields); A attests at step k+1; B `sync --check`s A's attestation → `forkedWorld k+1`; control: without
the fault, `shared k+1`. A second row `attest`: a stranger's attestation (a key that is no member) →
`notMember`; a rotated-away key → `staleKey`; a flipped byte → `badHeadSignature`. The plant that reds
`absorbPage_anchor_forked`: drop the anchor conjunct → the row's `forkedWorld` line is `shared` → RED
by the judge. The client test: `client/tests/join.rs`'s members gain one `sync --attest`/`--check`
round trip over the real sockets (filtered: `-E 'test(join)'`).

### 2.3 What it costs, in the spec's terms

- TOPLEVEL-SPEC §2.3 `ForkConsistent` becomes TRUE OF THE SYSTEM (CRIT-TRUST: what became true is the
  comparison of stated heads, `anchor_binds`; the claim was renamed `HeadsCompared`, PROTOCOL-83): its "NEW act" line is `sync --to`;
  its statement is `anchor_binds` with the deployed `absorbPage`. §2's "members never compare heads"
  clause is deleted. A2 (`OneHistoryPair`) is unchanged.
- §4 CONSENT gains C(vii) `Consent.attestsOwnHead` (statement 4 above) with the floor `relayAttester`
  (a `step` whose attest arm signs `result` rather than `headMessage (headOf w')`).
- §7 "the writer CANNOT … JOIN two forks it has shown two members — ONLY once A2′ is an act" does NOT close
  (CRIT-TRUST): the writer can still copy signed calls between forks; only stated heads are compared;
  "It CAN fork two members undetected today" becomes "it can fork two members until either compares;
  a comparison yields a signed witness".
- §9 Foreign: unchanged at T1; T2 strengthens `Std.head` (chain), T3 discharges `hr`.
- §3, §5, §6: no change of statement.
- Hypotheses on landed theorems: 0 (INFERRED before the build; MEASURED in §4.1 after it).
- Restated by binder: none. `absorbPage`'s signature is unchanged (the walk runs over the steps it
  returns), so `absorbPage_ok/_admits/_steps/_base`, `absorbPage_keeps`, `absorbPage_windowedIn`,
  `Absorbed` and Host's `honest_page_absorbed` keep their statements by name. `hintNames_complete`
  gains one arm (the attest refusals are in `hintNames`).
- Size: verbs 20/20 unchanged; refusal constructors +6 (no ceiling); `Protocol/Head.lean` +
  `Protocol/Proofs/Head.lean` two modules; Host closure 94 → 95 (`Protocol.Head`, imported by
  `Command.Machine`); no Rust (`nd` parses nothing; the custody `.sign` path is the existing one).
- Flag day: none. No byte of any Store, call, reply or package moves. A pre-T1 `nd` prints
  `badArgument` on the new flags, which is the only difference an old client sees.

### 2.4 Why first, and not after the Spec/ layer or the follower unification

Because it is the one item on the readers' list that lands a guarantee rather than a statement about an
existing one, it touches nothing the three structural programs (Spec/, one follower, emitted Rust
boundary) are moving, and its theorem (`anchor_binds`) is a lemma those programs will want
(`OneHistoryPair` with an act behind it). The one ordering constraint is FIX-HOST's re-deriver
unification (A9): `absorbPage` is the deployed re-deriver and stays; if `absorbStep` becomes
`auditStep ∘ decode`, the anchor conjunct sits above it unchanged.

---

## 3. WHAT MINI'S AMBITIONS REQUIRE OF THE TRUST MODEL

Mini's charter is its README and PROJECT.md (READ, 334316df): "a programmable shared world for people
and agents"; documents, rooms, chat, hosted apps as grains, Hermes residents, a public node with
enrolled friends, payments, "the agreement mesh … so that a world can be replicated across replicas
that agree on its history"; and PROJECT.md's user questions: "Is a conflict explicit, or was one writer
silently lost?", "Can I hand a compact proof of this history to another device or agent?", "work on
offline branches and merge without erasing provenance". As member-facing guarantees, with what meets
each:

| # | guarantee (member's words) | single writer + receipts (today) | head comparison (T1–T2) | certified heads (T3) | agreement (T4–T5) |
|---|---|---|---|---|---|
| M1 | what I signed is what was admitted, lawfully, or I am refused by name | **MET**: INTEGRITY + CONSENT (`plan_admits`, `settle_final_never_admits`) | — | — | — |
| M2 | my own calls settle from my own copy; nobody can tell me `ok` for what did not commit | **MET** for submit-class (PROTOCOL-64, T0); `cancel` open (A7) | — | — | — |
| M3 | the room I am in is the room you are in: we see one history | NOT MET (members never compare) | **met on comparison only** (T1; T2 when the writer delivers posts and the member's fold covers the posted step); operation-level no-join NOT met (CRIT-TRUST, PROTOCOL-82) | met with the writer's name on it | met by prevention (2f+1) |
| M4 | I can hand you a compact proof of what happened here | half: a receipt is a proof against MY head; you must follow this World to trust the head | **MET between members**: receipt + my attestation (you check my key in your copy) | **MET for strangers**: receipt + the writer's certified head (you need only the World's genesis) | the same, with 2f+1 signatures |
| M5 | this World keeps going if its host dies | NOT MET; measured not asked for (P6 §0.1: process-loss reopen 63–110 ms, no row names a dead host) | — | — | **the only thing that meets it**; the trigger is still unpulled |
| M6 | agents and people are the same kind of member, under the same consent | **MET** (the resident is a member; the Bell; `bell_resident_conforms`) | — | — | — |
| M7 | across Worlds and hosts, an outcome in A is usable in B | half: E5 receipts under an undischarged freshness premise (`hr`); forks seen at equal steps only | T2: forks of A seen at any step by B's head object (chain in `Std.head`) | **MET**: `hr` discharged to "A's writer signs one head per step", equivocation becomes a witness | the same, with a quorum |
| M8 | a stranger on the public node learns nothing it was not granted | **MET** (`Envelope.check` before every `defer`, §8 G2) | — | — | — |
| M9 | I can work offline on a branch and merge later without losing provenance | **NOT MET, by charter**: a fork is a new World; `admit_comm` commutes two Turns at one World, no merge | not this model | not this model | not this model: a committee decides ONE log |

Reading the table: four met now, two by head comparison (on comparison), two by certified heads, one by agreement
with no consumer, one by nothing here. The last row is the honest cost of this design. Mini's
`DISTRIBUTED-DESIGN.md` names the missing logic (independence: I-confluent invariants merge by join;
a bounded resource forces ordering) and lands the categorical shape with teeth (the PN-counter overdraft
that is linear but not I-confluent). If a demoland row ever needs M9, the right move is a CHILD WORLD
per branch with receipts into the parent (M7 + the hierarchy of §1.4) — which this model supports —
and not a merge of two logs of one World, which it refuses. Say so in the charter when the row comes.

Ambitions that are NOT trust-model questions, listed so they are not mistaken for ones: Objective Bend
and the language (LANG); hosted grains and the broker (HOSTING); private execution (ruled out of nano,
charter §Scope 1–2); payments (a ledger row under M1/M4); performance (THE BAR).

---

## 4. THE PRICE, IN NANO'S OWN TERMS

### 4.1 T1, measured on the landing worktree (filled by this lane when it builds; INFERRED until then)

| item | expected | measured (hbox, worktree `wt/fable-trust` on ad90a47, PROTOCOL-74) |
|---|---|---|
| Kernel statements whose digest changes (`Census/Statements`) | 0 | 0: no file under `Kernel/` or `Host/` touched |
| hypotheses added to any landed theorem | 0 | 0 |
| Protocol statements restated by binder (`absorbPage` consumers) | ≤ 12 | 0 (`absorbSync` wraps; proofs gain try-lines, statements unchanged) |
| new theorems | ~14 | 35 (`SIZE.md` theorems 6462 → 6497: 12 domain pairs, 10 head/anchor, 13 machine lemmas) |
| Host closure modules | 94 → 95 | 95 |
| verbs / call kinds / protocol ops | 20 / 13 / 7, unchanged | unchanged |
| conformance rows | +1 | 49 → 50 (`fork`; PASS toy + deployed, plant caught at line 10) |
| Lean lines | — | Protocol +726, Hosting +2, deployed +308; Rust +23 (the join test) |
| re-genesis | none | none; no wire or disk byte moves |

### 4.2 T2 (self-heads through the writer; `Std.head` gains `chain`)

- `Lang/StdHead.lean`: `headAtTy` gains `("chain", .digest)`; the law's `at → at` arm compares chain
  with roots at equal steps (`forkedHead`); `Lang.headView` returns the chain; `Protocol.Foreign.check`
  ignores it (a receipt checks against roots). `world/head/Head` re-emits; `headPackageId` changes; so
  every Store that installed it re-geneses: **`lang!` flag day**, coordinate with FABLE-CTX (Lang is
  theirs this week; the change is 20 lines and one vectors row).
- A self-head is a `Std.head` object whose `world` is THIS World's origin, posted by members by
  `invoke … post`. Follow, absorbing a Turn, reads every touched head object whose `world = X.origin`
  (`Lang.headView`, already a Protocol function) and runs the anchor check of T1 on `(steps, chain)` as
  it passes (or records `ahead`). Members who post periodically are compared by every other member
  automatically, through the writer, with no out-of-band step (CRIT-TRUST: only stated heads are compared; the
  writer may copy ordinary calls between forks, and may withhold posts indefinitely): a writer that forks M1 | M2 must either
  censor M1's posts from M2's fork forever (M1's post stays `open` on M2's fork: visible as a liveness
  signal, and a writer's standing right) or serve them and be refused `forkedWorld` by M2's follow.
  This is NOT SUNDR's "the server carries every user's version structure": SUNDR's structure rides on every
  operation, a post is periodic and optional (CRIT-TRUST; SPORC attaches history to every operation).
- Price: 0 kernel; Lang `headLaw` theorems restate by field (the four `StdHead` proofs); Protocol gains
  the absorbed-post hook (one function, one theorem: a post follow absorbed whose head is on its fold
  passes, one that is not refuses). One lane-week with the rows.

### 4.3 T3 (certified heads: the writer's signature; DESIGN-P6's P6-1 reshaped on `Head`)

- `GenesisInput` gains `Authority` (`certifiers`, `threshold`): `domOrigin` v2 → v3; `wrongWorld`
  refuses every old call (KERNEL-24); `Carried` gains it for the new World. Every Store re-geneses:
  **`host!` + `protocol!` flag day** (as P6 §4 priced).
- `Keys` gains a signing seed (§4.4). The writer signs `Certificate` over `Head` at every seal and at
  every `log` reply's end; the reply layout gains one field; `Thin.accept` requires a certificate of the
  pinned position (the sponsor's pin stays the trust root, PROTOCOL-61; the certificate is what makes a
  RECEIVED base's `CheckpointTrusted` dischargeable in principle, HOST-64's gap); `Std.head`'s post
  carries the certificate and the head law requires it when the foreign World's authority has
  certifiers (`uncertified` by name); `foreign_receipt_sound` RESTATES: `hr` is replaced by "A's
  certificate verifies under A's authority", and the conclusion gains "or A's certifiers equivocated,
  with the two certificates as witness".
- Price: 0 kernel hypotheses (the certificate lives beside the fold; P6 §7.1's measurement carries);
  `accept_done`/`accept_moved` + the `openWith_*` consumers gain a binder (P6 §8 card 1: ≤ 8);
  `foreign_receipt_sound` changes meaning (say so); 30 Host machine theorems do NOT restate at
  threshold 1 (the certificate is written at seal, the commit is unchanged; P6-2's proposal buffer is
  what restates them, and that is T4).

### 4.4 The Store signing seed: the question for Ember, in system terms

KERNEL-44 refused a host key for refusal receipts because the chain proves them (READ
`decisions/kernel.md` "The receipt": "a host-SIGNED receipt … buys nothing for (U), which the client
recomputes, and nothing for (A), which the chain proves"). That reasoning holds for T1 and T2: a member
proves a fork with its own key and the chain. It stops holding at T3, where the thing to be proved is
about a party that today HAS no key: the writer.

What the system does today: the writer's word on a position is unsigned; a member believes it only by
re-deriving; a thin joiner believes a sponsor's signed pin; a foreign World believes a grantee's post;
a stranger believes nothing.

After T3 with the seed: the writer signs every head it serves; a stranger with the genesis checks one
signature; a thin joiner's base carries the writer's certificate beside the sponsor's pin; a fork is
attributed to the writer by its own signature; E5's `hr` is discharged.

After T3 without the seed (member-attested heads only, k-of-members): a stranger needs k members' keys
from the genesis's founder list or an enrolment it trusts; a thin joiner's base carries k attestations;
a fork is attributed by exclusion. This works and needs no custody decision; it is weaker for strangers
and for a World whose members are few.

The price of the seed: one more secret in `Keys` (same file as the MAC keys, 0600, read by `host`
alone), one rotation story (the authority is in genesis, so rotating the writer key is a carry), and
the rule that ONE Store's seed lives on one host (a `gates/tcb.tsv` row). The default I would defend:
**take the seed at T3, as a `certify` key distinct from the MAC keys**, because every row of §3's T3
column (M4 for strangers, M7's `hr`) is a third party believing a head, and third parties are exactly
whom a member's key cannot speak for. Nothing in T1 or T2 waits on it.

### 4.5 What re-geneses, when, and what refuses to load (the flag-day ledger, law 1)

| move | shape changed | re-emits | refuses by name |
|---|---|---|---|
| T1 | nothing on any wire or disk | nothing | an old `nd` on the new flags: `badArgument` |
| T2 | `world/head/Head` package text (chain field) | the Std.head package id; `codec-vectors` row; every World that installed it (re-genesis) | `install` of the old text: a different package id, not a refusal; the X rows pin the new id |
| T3 | `GenesisInput` (+authority), `log`/`read` reply (+certificate), `Keys` (+seed), base file (+certificate frame) | every Store (re-genesis), `deploy/units/STORE.md`, RUNBOOK §genesis, `codec-vectors` | `shapeMismatch` for every pre-T3 Store; `wrongWorld` for every pre-T3 call |
| T2b (fork act) | `CarryInput` (+witness), `domOrigin` | carried Worlds' origins | a carry without the field: `badCarry` |

---

## 5. THE SEQUENCE — each move a new guarantee, not a refactor

**T1 · fork detection on comparison (this lane, one lane-day). LANDED: nano main `5fa281d`,
PROTOCOL-74.** Lands §2.2. New guarantee: M3 on
comparison, M4 between members. Consumer: the `fork` and `attest` rows; `join.rs`. Lets the system do
what it cannot now: two friends on THE BAR's deployment can prove to each other, and to a third friend,
that they are in one room.

**T2 · self-heads through the writer; `Std.head` carries the chain (one lane-week, Lang coordination).**
New guarantee: M3 on comparison, through the writer — every member's periodic post that the writer delivers
is checked by every other member's follow whose fold covers the posted step (CRIT-TRUST: censorship is silent,
and calls between posts are not compared); M7 strengthened
(forks of a foreign World seen at any step). Lets a room of strangers (mini's public node) detect a
fork without anyone arranging a comparison. Also T2b, the fork ACT: `host export --at STEPS` of the
common prefix and a carry whose origin input holds the two attestations, so "a fork is a new World" is
a command with a reason in its genesis, not a sentence in the charter.

**T3 · certified heads (DESIGN-P6's P6-1 on `Head`; 1.5 lane-days + Ember's ruling).** New guarantee:
M4 for strangers, M7's `hr` discharged, a thin joiner's base certified by the writer beside the
sponsor's pin, a fork attributed to the writer by its own signature. Lets a phone, or a World on another
host, act on a receipt from this World with one signature check and the genesis. **Blocked on the seed
(§4.4); every piece that does not sign — `Authority` in genesis, `Certificate` codec, `Certified`, the
reply field, `Thin.accept`'s check, the head law's `uncertified` — builds now with an empty certifier
list.**

**T4 · the committee authority, sign-once (P6-2; 2 lane-days).** New guarantee: M3 by PREVENTION (a
position needs 2f+1 re-derivations before anyone is told `ok`) and the one-host plant (a host holding
one key cannot decide). Lets a World be served by several Stores on several hosts with safety as a
theorem (`decided_unique`, P6 §3) and liveness honestly absent (a split halts; recovery is T2b). Trigger,
unchanged from P6: a row whose World must outlive its host. Costs the 30 Host machine restatements P6
measured, the proposal buffer, `nd-peer`.

**T5 · the engine (P6-3; 5–8 lane-days).** New guarantee: M5, measured on one box under a configured
bound, never a theorem. Same trigger as T4.

The order is forced by what each needs: T2 needs T1's anchor check; T3 needs `Head` (T1) and benefits
from T2's channel; T4 needs T3's `Authority` and seed; T5 needs T4. Nothing in T1–T3 restates a Kernel
theorem; the first Kernel-visible change is T2b's `CarryInput` field.

---

## 6. THE ONE WAY THIS DESIGN IS WRONG, AND WHAT WOULD SHOW IT

**The assumption is that one decided log per World, with members comparing heads, is the unit mini's
ambitions need — and that availability (a World outliving its host) is the only thing that would ever
force a committee.** If the demoland's first real multi-party row needs two members to WRITE while they
cannot reach one writer (two phones on a train editing one document; a room whose host is one friend's
laptop, closed), then the object this memo builds is the wrong half: the room needs the independence
logic (which cells merge by join, which force ordering) and the trust model needs to say what a member
is promised about a MERGE, which §3's M9 row refuses. What would show it: a row in which `a fork is a
new World` is the answer and the row's owner rejects it — the detector KERNEL-45 asked for ("the row
author choosing escrow should say whether it would have preferred one turn") applied to Worlds: every
row that re-geneses a World after a partition should say whether it would have preferred a merge. Two
such rows and this memo's §1.4 CRDT paragraph is the design, not a footnote.

The smaller way it is wrong is the one SUNDR had: a guarantee conditional on an act. If nobody ever
runs `sync --check`, T1 detects nothing, and a public node of strangers will not arrange comparisons.
What would show it: THE BAR's deployment running for a month with zero `forkedWorld` AND zero `shared`
lines in any journal. The answer is already in the sequence (T2 makes the comparison automatic), so
this is a reason to land T2 within the week of T1, not a reason to doubt the object.

---

## 7. Literature, by name, as used

- SUNDR: Li, Krohn, Mazières, Shasha, "Secure Untrusted Data Repository", OSDI 2004 (fork consistency,
  signed version structures, detection by comparison).
- Fork-linearizability: Cachin, Shelat, Shraer, "Efficient fork-linearizable access to untrusted shared
  memory", PODC 2007; SPORC (Feldman, Zeller, Freedman, Felten, OSDI 2010) and Depot (Mahajan et al.,
  OSDI 2010) for fork-join-causal and recovery from forks.
- Accountability by replay: PeerReview, Haeberlen, Kouznetsov, Druschel, SOSP 2007.
- Signed tree heads and consistency proofs: Certificate Transparency, RFC 6962 (Laurie, Langley,
  Kasper, 2013); CONIKS (Melara et al., USENIX Security 2015) for gossip of heads.
- Light clients that verify certificates, never run the protocol: the IBC client model (Cosmos IBC
  specification); Tendermint's commit certificates.
- Quorum intersection and certificates: Castro and Liskov, PBFT (OSDI 1999); Simplex (Chan and Pass,
  2023) as mini's Generic Simplex instantiates it.
- Fencing tokens for a single writer: Burrows, "The Chubby lock service", OSDI 2006 (HOLISTIC-HOST
  §3.2's point about the lock; not a trust-model item, listed because T3's certificate is a fencing
  token's honest cousin).
- Durable linearizability as the writer's top claim: Izraelevitz, Mendes, Scott, DISC 2016
  (TOPLEVEL-SPEC §5; unchanged by this memo).
- I-confluence / coordination-free invariants, for M9's refusal: Bailis et al., "Coordination avoidance
  in database systems", VLDB 2015, as mini's `DISTRIBUTED-DESIGN.md` carries it into Lean.
- Verified distributed systems the method is measured against: IronFleet (Hawblitzel et al., SOSP
  2015), Verdi (Wilcox et al., PLDI 2015).

---

## Appendix A — what was read, by path, for the claims above

- nano `Kernel/World.lean:246-320, 1760-1800` (Step, World, Carried, refuse, step); `Kernel/Proofs/Fold.lean:420-470`
  (`fold_head_binds`, `fold_reaches_host`); `Kernel/Receive/Follow.lean:30-110` (GenesisInput, origin,
  CarryInput); `Kernel/Receive/Call.lean:1-80`; `Kernel/Proofs/RowsComm.lean:791-846` (`admit_comm`).
- nano `Protocol/Command/Machine.lean:180-300, 470-560, 1085-1400` (Follow, Memory, Persist, State,
  absorbPage, start, step: the sync and invite arms); `Protocol/Command/Verb.lean:1-120, 391, 405`;
  `Protocol/Proofs/Domains.lean:1-60`; `Protocol/Invite.lean:1-90`; `Protocol/Receipt.lean:1-60`;
  `Protocol/Envelope.lean:1-50`; `Protocol/Foreign.lean`; `Protocol/Proofs/Foreign.lean:55-100`;
  `Protocol/Rows.lean` (sync at :649, invite rows :972+).
- nano `Lang/StdHead.lean:1-140`; `Host/Check.lean:1-60` (`--anchor`); `Host/Follow.lean:1-120`;
  `Host/Page.lean:1-60`; `SIZE.md` (verbs 20/20, call kinds 13/13, ops 7/7, Host closure 94/150).
- nano `decisions/kernel.md` KERNEL-44 ("The receipt": no host key), KERNEL-45 (deferrals and triggers);
  `decisions/protocol.md` PROTOCOL-65 (E5 as landed; its critique: "the premise of `foreign_receipt_sound`
  is the whole trust"); `CHARTER.md` §Scope 3 and laws 1, 2, 4, 7, 12.
- mini `README.md` (the ambitions table, "Honest state"), `PROJECT.md` (the user questions),
  `docs/GENERIC-SIMPLEX-NATIVE.md` (liveness "NOT a theorem here" ×2; certificates; re-genesis on
  reconfiguration), `docs/agreement/CUTOVER.md` (00f711 abandoned; four replicas one host),
  `docs/DISTRIBUTED-DESIGN.md` §0–2 (the three step-logics; I-confluence with teeth),
  `Kernel/GenericSimplexEngineSafety.lean:1-60`.
- redregg `promo/DESIGN-P6.md` whole; `readers/VERDICT-20261024.md`; `readers/HOLISTIC-HOST.md`;
  `readers/HOLISTIC-PROTOCOL.md`; `promo/TOPLEVEL-SPEC.md` whole; `promo/IMPACT-E5.md` §0;
  `PROGRAM-20261022.md` §2.

---

## BUILT-2 — T2 as landed by FABLE-TRUST-2/3/4 (real 2026-10-26; PROTOCOL-75 + LANG-95; origin/main `9ccb6b6e`, landed by FABLE-TRUST-4 after the judge rebased it over c4800fb7)

**What was built (MEASURED on `wt/fable-trust` against 1e8a2a0).** `Std.head` carries the chain (`headAtTy` =
`{chain, height, roots, steps}`; `head_at_at` gains `c = c'`; `world/head/Head` re-emitted, 3 lines; journey HD3b).
`nd sync --post OBJ` (`Cmd.post` → `invoke OBJ post` of `Head.headText` of follow's OWN World at the tip; consent
`body_post`). `Head.forkedSelfPost` after `absorbSync`: every `Std.head` of THIS World a step of the page touched
is read (`selfPosts`) and the page walked against its `(steps, chain)` as `sync --to` walks; a position reached
with another chain is `refused forkedPost STEPS` (poster named) with the page KEPT. Theorems
`forkedSelfPost_forked`, `forkedSelfPost_none`. Row `selfHead` PASS on toy and deployed parameters (line 8 post
ok; line 9 cold sync ok; line 12 `refused forkedPost`; line 13 ok); plant MEASURED: with `forkedSelfPost := none`
line 12 ends `ok` (row FAIL), reverted, rebuilt green. `cargo test --test foreign` ok (the X rows post the chain
they read off `receipt`). `receipt CALL` prints `head STEPS HEIGHT ROOTS CHAIN`. Hypotheses added to landed
theorems: 0; Kernel/** and Host/** untouched; restated by binder: `Proofs.Foreign`'s four statements (`c₀`),
`head_at_at`. `forkedSelfPost` is `@[irreducible]`, and the verdict is applied by `postOr` (irreducible, a
top-level function the page arm's `moved` wraps every reply in), never a match in `step`'s body: `step_world`'s
blanket split pays per match of `step`, and one more there put it past the default budget; the reply-shape proofs
read `postOr` by `postOr_cases` and its elims. Every proof stays at 200 000 heartbeats (FABLE-TRUST-3: the first
build had raised the budget; the source gate refuses that, rightly).

**Two corrections to §4.2, found by building.**
1. *Refusing the page is wrong here.* §4.2 said "refuse `forkedWorld` as T1 does". A forked self-head post is
   evidence about the POSTER or the writer, never about the lawfulness of the page on follow's fold; refusing
   the page would let any member with post rights freeze every other member's follow forever (`forkedWorld`
   was right for `sync --to` only because the position came from the member running the command). So:
   page kept, command ended by name, the next command proceeds, the poster's signed call is the witness.
2. *"or records `ahead`" is the common case, not an edge.* The pure walk compares a post only against positions
   INSIDE the page that carries it. A live member is past every post it absorbs; it compares nothing purely.
   Its chain at that step is in its own Store's index (`host check --anchor`: `Page.kept` at budget 0). The
   automatic guarantee "M3 continuously" therefore holds, after this landing, for members BEHIND the post
   (cold joiners; members catching up after a pause), and for always-on members only after **T2b'** — the
   follow loop (`Host.Follow.loop`, with a `PageFiles` from `Host/Cli.lean`) resolving behind-positions through
   `pageKept`, HOST-prefixed, TRUST-owned: cv task `01a176ab-14f5`. The `selfHead` row says this with
   `fault := .cold`. §3's M3 row should read "MET continuously for members behind a post (T2); for all members
   at T2b'". (CRIT-TRUST: "continuously" overclaimed: a post is compared only where follow's fold covers its
   step, only if the writer delivers it, and only the stated head, never the calls between posts; PROTOCOL-82.)

**Price, measured.** 0 kernel premises (§4's count holds); `lang!` flag day as priced (the package id moves);
Protocol +~140 lines, Lang +~30, Rust +~10; one refusal constructor; one conformance row; three theorems; Host
closure: `Protocol.Head` now imports `Protocol.Foreign` (already in the closure). The Store signing seed:
untouched (cv `01a1769d-2f64` open; T3 waits on it; its unsigned pieces are the next lane's first move after T2b').

## BUILT-3 — T3's unsigned half as built by FABLE-TRUST-3 and landed by FABLE-TRUST-4 (real 2026-10-26; PROTOCOL-76; origin/main `f70a5f9e`, on T2's `9ccb6b6e`)

**T2's landing shape (MEASURED).** The self-head verdict is `postOr` (irreducible) wrapping every reply of the page
arm, never a match in `step`; the reply-shape proofs over `step` read it through `Protocol/Proofs/PostOr.lean`
(`postOr_cases` and one elim per reply constructor; C3 refused theorems in the def module). The `.done` arms are
closed right after the strip: left to the `_ne_submit`/`_ne_host` cascades they alone pass 200 000 heartbeats
(bisected). Every proof in the tree is at the default budget. Rebased onto c82f171 (the generator landing): GN2
and X6 post heads with the chain; `headPackageBytes` is symbolic, so GN1 tracks the package id.

**T3 built without the seed (MEASURED on `wt/fable-trust`: `Protocol.Proofs.Head`, `Protocol.Proofs.Domains`
green).** §1.2's `Authority` and `Certificate` exist as written there, with two corrections found by building:
(1) a certificate's signers are INDICES into the authority's list, not keys — a certificate is bound to the
authority it was made under, and a carried World's new authority invalidates every old certificate by
construction; (2) the verification walk is strict (a bad signature at any listed index refuses by that index;
nothing is discounted and counted), so a verifier never accepts a certificate it cannot tell from a
forged-then-padded one. §1.3's table is now one theorem with a bound: `certified_intersect` names a shared
listed certifier whenever `n < 2t`; `0 < 0` (today) names nobody, `1 < 2` the writer, `3f+1 < 2(2f+1)` a
committee member; `certified_equivocation` adds the witness (two certified strings at one step count, different
chains, one signer of both). `anchor_binds` (T1) stays the fold half under every row; `heads_prefix` as one
statement is the conjunction of the two and is not stated separately (nothing consumes it).

**What is still not deployed, by name.** No producer (the seed: cv `01a1769d-2f64`, Ember's) and no consumer
(the authority is not in the genesis input: T3b, cv `01a176f6-ac3f`, `host!` + `protocol!`). §4.3's price
stands: 0 kernel premises for the object; the wiring is where `accept_done`/`accept_moved` and the `openWith_*`
consumers gain a binder (≤ 8) and `foreign_receipt_sound` changes meaning. §4.5's T3 row re-emits nothing yet.

**Price, measured.** Protocol +~150 lines of definitions, +~190 of proofs, +~50 of domain pairs; one new
refusal type (`CertRefusal`, six constructors); `Protocol/Proofs/Head.lean` imports `Kernel.Proofs.Journal`;
Kernel/** and Host/** untouched; hypotheses added to landed theorems: 0; restated by binder: 0.

## BUILT-4 — T3b's first landing as built by FABLE-TRUST-4 and carried by RELAND-TRUST (real 2026-10-26; KERNEL-69 + PROTOCOL-77 — renumbered from 68, which OBS's meter took on d280d23; `kernel!`; LANDED origin/main `8f1e3329`)

**What was built (MEASURED on `wt/fable-trust` over f70a5f9e).** The authority is a fact of the World: `Authority
{certifiers, threshold}` is a genesis input (the keys as a raw list and the threshold `nat64` after the founders;
`domOrigin` v3), so the origin commits to it — `genesis_inj` now concludes `auth = auth'` — and one ROM cell in the
World carries it (`authorityCell`: kind `kindAuthority`, the threshold, the count, the keys; `authorityId` =
`romIdOf` of it; `genesisEntries` = the founders' entries then the authority; `authorityOf w` reads the one live
`kindAuthority` cell, two or none refused). The signed start carries it (`Start.genesis … auth`; the invitation's
`input` bytes). `host genesis --certifier HEX … --threshold N`; absent, `Authority.none`. `GenesisRefusal` gains
four names (`tooManyCertifiers`, `certifierTooLong i`, `repeatedCertifier i`, `badThreshold`); `Authority.Fits`
is the quorum somebody can meet (`0 < t ≤ n`, or none). `Protocol.Head.Authority` of PROTOCOL-76 is deleted: the
certificate theorems are over the kernel's object unchanged in meaning.

**Three corrections to §4.3 / the T3b task, found by building.**
1. *`Carried` gains nothing.* The carried trie carries the cell, and the carry origin commits to the trie root; a
   committee that rotates is a new World by `carry` of a trie with another cell — not designed here, named.
2. *Not a cell under an origin-derived id.* The founders' pattern (`founderId X o i`) would put a ROM cell at a
   non-content id and contradict `RomContent` (KERNEL-3: a ROM cell sits at `romIdOf` of itself; `admit` refuses
   `notContentId`); a RAM cell would be immutable only by no receiver naming its kind — a belief. At its content id
   the cell satisfies `RomContent` by construction and `fold_rom` keeps it: immutability is a landed theorem.
   The reader finds it by kind (one scan at adopt/genesis, where `atGenesis` already scans).
3. *`genesisLeaf` widens, `atGenesis` is not the authentication.* A step-0 World holds members, grants and the
   authority; what authenticates an adopt was always the invitation's pin (the bytes must hash to it).

**Still not deployed, by name.** `authorityOf_genesis` (`authorityOf (genesisWorld … auth) = some auth` under
`GenesisFits`): the next theorem; the `log`/`read` reply field, `Thin.accept`'s requirement, the head law's
`uncertified`, `foreign_receipt_sound` restated (T3b's second landing, `protocol!`, each a consumer of
`authorityOf`); the producer (the seed, Ember's). Under `Authority.none` every row, Store and client behaves as
before up to the origin.

**Price, measured.** Kernel: +~120 lines of definitions, +~90 of proofs; the binder `auth` on every statement
over a genesis World (~40 files, counted in the report); hypotheses added to landed theorems: 0; one restated
invariant: none (`RomContent` untouched; `genesis_romContent`'s reading changes from "no ROM cell" to "one, the
authority, at its content id"). Flag day: every origin moves, every Store re-geneses, every invitation re-issues;
the World codec is unchanged; no schema epoch moves.

**RELAND-TRUST (carried onto d280d23, the meter).** Nothing in the design moved. The meter's window trie and the
authority cell compose without a premise: `reach_refusals_bounded` keeps the meter's two conjuncts and gains the
binder. Waste measured on the composed tree: admit trie-hashes-per-turn 14.297 (the meter's 14.219 + the authority
leaf), worstcut-writes 19.641 (18.661 before: a 591 B base, so one leaf lengthens most paths); births, retires and
rows stay under their pins. **`authorityOf_genesis` BUILT** (cv 01a177f3-2293), in the new
`Kernel/Proofs/AuthorityOf.lean`: `authorityOf_genesisWorld` (premise: the two counts fit a `u64`; no hash
premise, because the authority is written last, so a founder id that equals its content id is overwritten by it,
not the reverse), `authorityOf_genesis` under `GenesisFits`, and the weak fold form `fold_genesis_authority` (every
reached World still holds the cell, by `fold_rom`). The strong form, `authorityOf w' = some auth` on every reached
World, needs "no turn births a `kindAuthority` cell" as a theorem; no receiver names the kind today, so it is a
statement to prove, not a design change.


## BUILT-5 — T2b' as landed by RELAND-TRUST (real 2026-10-26; HOST-79; `host:`; origin/main `202f8f46`)

A live member compares every self-head post it absorbs. PROTOCOL-75's walk reaches only the step counts a page
itself walks from follow's position; `Head.behindPosts` is exactly the complement (`steps ≤ w.steps`) and
`Head.forkedBehindPost` decides it against an oracle (`forkedBehindPost_forked`: a refusal names a carried post
where follow's history holds another chain; `_none`: otherwise every behind post agrees wherever the history is
kept). The deployed oracle is the member's own Store: `Host.Deployed.chainKept` (`Page.kept` at budget 0, now
also `host check --anchor`'s), read in `Host.Follow.loop` before the append; a mismatch is `refused forkedPost`,
the page kept. **Correction found by building:** a self-head SEED is a claim at its step (step 0: the genesis
chain) and is compared like a post; exempting creates would exempt the forgery (a forger may seed at any step).
**Still not covered:** a thin joiner below its adopted base (not compared: the Store cannot say; the certificate
consumer landing is the answer); no Lean row drives the loop half (rows drive `Follow.answer`); the client test
`client/tests/join.rs` does, plant measured.

## BUILT-6 — T3b's second landing: certificates READ and CHECKED (real 2026-10-26; TRUST-SEED; PROTOCOL-77.1; `protocol!`)

**What was built (MEASURED on `wt/fable-trust` over 5a0a7e4a).** The `read` reply's last field is the writer's
certificate of the base's head (`readReplyLayout` + `certificate`; the Store holds it as `STORE/base.cert`, served as
read, self-authenticating, no MAC; absent: empty; `Host.Page.basePage` pays for it from the page budget). A thin
member's `adopt` asks `Head.certifiesWorld` on the World the pinned bytes decode to: nothing under an authority that
names nobody (every Store today, `certifiesWorld_none`); otherwise the certificate verifies under THAT World's authority
and certifies exactly `headOf w` (`certifiesWorld_ok`), refused by `CertRefusal`'s name. The rows' Worlds name the
writer's certify key as their one certifier, so every thin row adopts a certified base; row `certified` with plant
`forgeCertificate` (a flipped signature byte: refused `badCertifySignature`), PASS toy and deployed (Ed25519).

**Two corrections to the plan, found by building.** (1) The check is a property of the decoded WORLD (its authority is
a cell of it), so it lives in `adopt`'s `.done` arm, not in the byte-level `Thin.accept`. (2) `certified` under
`Authority.none` ACCEPTED a certificate with no signature (threshold 0 ≤ 0 signers): the one verification path every
third party will run said "certified" for every World that exists. It now refuses `noAuthority` at threshold 0
(`certified_none`), at the path, not at each caller.

**Still not covered, by name (cv).** Adoption with no sponsor pin, the authority from the genesis inputs (T3c,
01a17a55-5e88); certificates on `log` pages, so members compare the writer's certified head as they follow (T3d,
01a17a55-5ea9); the stranger's check `host certified INPUTS CERT` (T3e, 01a17a55-5ebc); THE PRODUCER (below).

## BUILT-7 — THE SEED as landed (real 2026-10-27; TRUST-SEED-2 built it, TRUST-SEED-3 landed it; HOSTING-56 + HOST-80 + PROTOCOL-78; `hosting!`; origin/main `272fd767`)

§4.4b items 1–6 and 8 are built as designed, with the restart guard of the "Resolved" note: keybroker holds `certify`
and `certify.next`, binds `SOCKDIR/.writer/certify.sock` only when the slot is present, persists the head to
`KEYS.certified` before signing, and signs `domCertify ++ granted bytes` only; `Hosting.Certify.decide` grants only a
head its own `Host.Tail` fold reaches at a record end, never below or beside the last certified head, anchored at a
restart by `chainOf` over the kept records (`decide_ok`, `certify_on_fold`, `granted_one_head`, `anchoredBy_chain`).
`host serve/seal --certify` produce `base.cert` per seal, self-checked by `certifiesWorld`; `host certified INPUT_HEX
CERT` is the stranger's check (`stranger_ok`). Measured: `launcher/tests/certify.rs` (certified seal, thin joiner
adopts and refuses a flipped byte, stranger takes and refuses forged/otherWorld, decider refuses notYet/notOnFold/
regressed across a restart), broker 13/13, fence 3/3. NOT in it: item 7 (pre-rotation, the next free KERNEL number,
cv 01a17a5c-fa4c), the deployed units' wiring (OPS, cv 01a17b00-67a4), T3c (§T3c below: owes a `kernel!` committing
`allowance`, then trusts the writer for lawfulness by name), T3d (certificates on log pages, cv 01a17a55-5ea9).
**What it proves (CRIT-SPEC):** the key holder's commitment to a head and evidence if it equivocates; lawfulness rests
on the decider's fold from an honest base, i.e. on the operator, not on the signature.

## BUILT-8 — T3d: the writer's certified head on every log page (real 2026-10-27; TRUST-SEED-3; PROTOCOL-81; `protocol!`; origin/main `eb674e79`)

`logReplyLayout` + `certificate` (`base.cert`, capped at 1424 bytes / 16 signatures). Follow verifies it under the
authority of its OWN World (never the page's) and compares the certified chain with its re-executed fold: on the page
(`Head.forkedCertified` in `postOr`) and behind it against its Store (`Head.behindCertified`, `Follow.behindOr`, on
empty pages too). Mismatch: `refused forkedCertified`, page kept, `forkedCertified_forked`. Row `certifiedPage`, plant
`forkCertificate` (a genuine signature on a head with another chain). What it buys: ATTRIBUTION, a transferable witness
of the writer's fork signed by the writer, where a self-head post is a member's word. Open: (1) a relay that STRIPS the
certificate is undetectable (empty is the honest shape without a producer): under a certifying authority a page
without a certificate could be refused, which costs every Store a live producer; a design call. (2) The behind path is
unmeasured with a forked certificate (no row drives `Follow.loop`).

## §4.4b — THE SEED, as it will be built (TRUST-SEED; Ember's YES, cv 01a1769d-2f64, real 2026-10-26; PROTOCOL-78 + HOST-80)

**The custody, in one paragraph a member can read.** The writer's signing seed is not in the writer. It sits in
keybroker's key file, beside the provider keys, read once under the same custody checks (0600, the operator's), and
keybroker signs with it only what Lean's decider approves: a head of THIS World that the decider's own re-derivation of
the Store has at exactly that step count. The writer can ask, never read: a thief of the writer process can obtain
certificates only of heads on the one history the decider re-derived, so it cannot get two certificates for one step
(`certified_equivocation` needs two). A thief of the key file can sign any head, which is why the genesis lists the
key (a stranger trusts the World's authority, never the host) and why the NEXT key is committed in advance, KERI-style:
the successor World that rotates the key out must be authorised by the pre-committed next key, which the thief does
not hold. [CORRECTED, §4.4c: item 1 below put the next seed in the same file, so a thief of the file holds
it; the next seed needs its own custody.] The seed signs heads ONLY: keybroker prepends `domCertify` itself and has no path that signs raw bytes with it,
so even a confused decider cannot make it sign a call, an envelope or an attestation (the domains are pairwise
disjoint, `Protocol.Proofs.Domains`). Refusal receipts stay unsigned (KERNEL-44 stands: the chain proves them).

**The shape (law 1: one more principal under the existing broker, no new custody object).**
1. *Key slot.* KEYS gains the slot `certify` (an Ed25519 seed) and `certify.next` (the pre-committed next seed, fresh
   OS randomness, never derived), the `SameRecord` custody shape of `client/src/custody.rs` (a hosted principal has no
   offline). `keybroker --certify-pub KEYS` prints the current public key and the next key's digest for `host genesis
   --certifier HEX --threshold 1`.
2. *Socket.* keybroker binds ONE extra socket, `SOCKDIR/.writer/certify.sock` (a leading dot: no grain name can take
   it, `grain_name_ok`), peer = the writer's uid; identity is the socket, as for residents.
3. *Request.* `certify` (a new `requestCases` tag): the certified bytes (`Head.certifiedLayout`). keybroker never
   decodes them; it puts `certifyAsk atMs` in front and hands both to the decider (HOSTING's pattern, BrokerWire).
4. *Decision (Lean, `Hosting.Broker.certify`).* The bytes decode (`Head.certifiedSaid`) to a head of the World the
   decider follows (it already follows STORE for allowances), at a step count its own fold holds, with exactly its own
   chain, height and roots there (`Host.Deployed.chainKept` behind the tip, the World at the tip); else refused by name
   (`otherWorld`, `notOnFold`, `notYet` when the decider has not reached the step: the writer retries). Theorem: a
   granted certify names a head on the decider's fold (`certify_on_fold`), so two grants at one step name one chain.
5. *Verdict.* `sign` (slot `certify`): keybroker signs `domCertify ++ bytes` with the slot's seed and answers the
   signature; nothing else uses that slot.
6. *Producer (HOST-80).* `host serve --certify SOCK`: after each seal installs a base, the writer asks custody for the
   base World's head (`Head.certifiedBytes (headOf base)`), builds the certificate (`certificateBytes`, signer index
   from the World's authority) and replaces `base.cert` atomically (`certTmpPath` → rename → sync dir). At each SEAL,
   not on request: one signature per seal cadence, of exactly the object a thin member adopts, and no signing oracle
   on the network path (an on-request signer would let any reader drive the broker once per page). A refusal or an
   absent socket leaves the old certificate (stale: `otherHead` until the next seal) and is named on stderr; it never
   blocks a commit.
7. *Rotation (KERNEL-70, its own `kernel!`).* `Authority` gains each certifier's next-key digest (the authority cell,
   `domOrigin` v4); `carry` refuses a successor World whose authority does not list keys matching the predecessor's
   committed digests (`notPreRotated`). Until then a writer key rotates by an ordinary carry (DESIGN-TRUST §4.4).
8. *Tests.* `launcher/tests`: keybroker + decider certify a head on the fold, refuse a forged one `notOnFold`;
   `client/tests/join.rs`: a Store whose authority is keybroker's certify key, `host serve --certify`, a thin joiner
   adopts certified, a forged `base.cert` refused `badCertifySignature`; rows `--deployed` flip `Writer.authority` to
   the deployed producer once host signs.

**Ownership.** keybroker, `launcher/` and `Hosting/Broker*` are AGENT's column (FABLE-OWNERSHIP): every hunk there is a
report line in FABLE-TRUST.report.md first, and a HOSTING number claimed by line (TRUST claims HOSTING-56).

**Claims in §4.4b marked by source.** READ: keybroker's shape (KEYS under custody checks, one socket per principal,
identity = socket, every verdict the Lean decider's, the decider given STORE to follow: `launcher/src/bin/keybroker.rs`
header, `Hosting/BrokerWire.lean`), the member custody shapes (`client/src/custody.rs` header), `domCertify` disjoint
(PROTOCOL-76). ASSUMED BY ME, the first thing the builder reads: that the decider's view of STORE is a re-derived fold
(the property item 4's theorem needs) and not the Store's own word; if it reads the base and tail without re-deriving,
item 4 must run `Host.openWith` + `absorb` (an audited follower), and its cost is the decider's cold open.
**Resolved (READ by TRUST-SEED, `Hosting/BrokerCli.lean` header, `Host/Tail.lean`):** the decider follows STORE as a
`Host.Tail` — THE open (base + tail), then every appended record folded by the same per-record step a reopen runs
(`Host.Proofs.Tail.absorb_encodeAll`), forward only, a rewritten byte `corrupt`. So it holds ONE fold of the Store's
bytes (admitted, chain-asserted), not a re-derivation: enough for item 4's non-equivocation (it never holds two chains
at one step while it runs), not for "a certified head is lawful" (members audit that by re-execution, as today). A
decider restarted against REWRITTEN files could certify a second history: item 4 also keeps the last certified
`(steps, chain)` in a 0600 file beside KEYS and refuses below or beside it (`regressed`), so a restart does not reset
the guarantee.

## §T3c — pinless adoption: what a certified head binds (TRUST-SEED-3, real 2026-10-26; READ, not built)

A certificate signs `headOf w = (origin, steps, height, roots, chain)`. Eight of the World's nine fields are bound by
it up to an explicit collision, by composing landed theorems: `rootsDigest_inj` (roots → four trie roots),
`HeadSound.root_binds` × 4 (each root → its canonical trie, premises met by `world_decode_canon`/`_cellsFit`/…), and
the head's own five fields. The ninth, **`allowance`, is committed by nothing in the head**: it is neither a head field
nor under `roots`, and only a FOLD binds it (`fold_reaches_host`). A pinless joiner adopting certified-head bytes can
therefore be handed any allowance, and `checkCharge` reads it, so its admissions diverge from the host's. OWED, in
order: (1) `kernel!`: `allowance` becomes an input of `rootsDigest` (or the head link), re-emit, re-genesis;
(2) `World.head_binds`: equal heads ⇒ equal Worlds ∨ `CollidesAmong` over the rootsPre pair and the four tries'
`bindingPres`; (3) T3c's adoption on that lemma (cv 01a17a55-5e88). Until (1), pinless adoption is unsound and the pin
(hash of every byte) stays the only way in.
**Amended (CRIT-SPEC, real 2026-10-27).** Even with `allowance` committed, a certified head binds CONTENTS, not
LAWFULNESS: a key holder can sign one fabricated head per step count and never equivocate, so a certificate is
attributable endorsement plus equivocation evidence, never a proof the head is a lawful fold. T3c is therefore
recorded as: "pinless adoption trusts the writer for lawfulness; sound only with an audited prefix or a member's
attestation", and the authority it checks against must come from the genesis input the joiner already trusts, never
from the bytes being adopted. Owed in this order: commit `allowance` (kernel!), `World.head_binds`, then T3c with the
trust it carries named in the joiner's output.

## §4.4c — RECOVERY: a signing authority that survives its broker (TRUST-4, real 2026-10-27; CRIT-TRUST's third change)

**Correction first.** §4.4b's custody paragraph said "the NEXT key is committed in advance, KERI-style: the successor
World that rotates the key out must be authorised by the pre-committed next key, which the thief does not hold", and
item 1 put `certify.next` in keybroker's KEYS file beside `certify`. A thief of that file holds both. Pre-commitment
protects recovery only from an adversary that lacks the successor secret, so the successor secret needs a compromise
boundary of its own. Until the five properties below hold, a certificate is an endorsement whose key can fail
permanently (docs/TRUST.md says so).

**What recovery must give (CRIT-TRUST), and where each stands.**

1. *Durable signing state constrains every later signature.* keybroker writes the head it is about to sign to
   `KEYS.certified` (`fsx::replace`: tmp, sync, rename, sync the directory) before it signs, and the decider reads it
   at every start. BUILT-7 proved one head per step count (`granted_one_head`). That is not enough: a key can endorse
   one branch at step 10 and another at step 11 without signing twice at either. **TRUST-4 builds the cross-step
   property:** the decider checks every record's link itself (`Certify.linked`: the kernel's `chainOf` from the
   window's tip over the record's step pairs reaches the new head; an unlinked head unanchors it for the life), so its
   window is one line of heads with the last certified head on it (`Proofs.Certify.Line`, kept by `opened_line`,
   `absorb_line`, `decide_line`), and **`granted_extends`**: over any run of grants, across any number of decider
   lives, every granted head extends every head granted before it and the persisted start (`Extends`: one World,
   and step pairs whose chain link runs from the earlier chain to the later). Premise named: each life's certifier
   is built by `opened`, `absorb` and `decide` (the IO loop in `Hosting/BrokerCli.lean` does nothing else to it).
2. *The restart path establishes extension of the last certified prefix.* **`restart_extends`**: a decider that comes
   up anchored with the persisted head `l` holds a World whose head extends `l` (the opened World is `l`'s head, or
   the Store's kept step pairs run the chain link from `l` to it). A Store rewritten to another history cannot anchor:
   it would need a chain-link collision.
3. *A rotation rule that authenticates succession* — designed here, not built:
   - `Authority` gains `next : List D`, one digest per certifier, `H(domCertifyNext ‖ next public key)`; the genesis
     input and the authority cell carry it (`domOrigin` v4: every Store re-geneses). `checkGenesis` refuses a list of
     another length (`badNext`).
   - `CarryInput` gains the predecessor's head at export (`fromSteps`, `fromChain`: where the successor continues,
     so a consumer can place old certificates against it) and the successor authority. A carry either KEEPS the
     authority cell (an ordinary carry: the old keys go on certifying the new origin) or ROTATES: `carryWorld`
     replaces the cell, and `checkCarry` refuses `notPreRotated` unless every successor certifier's key hashes to the
     predecessor's committed `next` at its index, and the successor commits fresh `next` digests.
   - The stranger's check gains `Certified.succeeds G S`: S names G's origin, S's keys open G's `next` digests, and a
     certificate under S's authority verifies. Then the consumer believes S's heads.
4. *The successor secret survives compromise of the current key.* `certify.next` leaves KEYS: keybroker refuses a
   KEYS file that carries it (the old shape refuses to load), and a separate command (`keybroker --certify-keygen
   OUT`) writes a fresh seed to a file the operator keeps elsewhere (offline media, another account), printing only its
   public key's digest for `host genesis --certifier-next`. At rotation the operator brings the next seed in as
   `certify` and makes a new next. A thief of KEYS then holds one seed, which cannot open the committed digest.
5. *The disposition of old-origin receipts and certificates.* A consumer that has accepted successor S of G: (a) takes
   an old-origin certificate at a step count past `S.fromSteps` as `superseded` (the old key may be stolen; anything it
   signs past the rotation point is not the World's); (b) at exactly `S.fromSteps`, an old certificate whose chain is
   not `S.fromChain` is equivocation evidence against the old key; (c) an old-origin RECEIPT is honoured by checking
   it again against S: the carry carries the journal, so a call the old World committed is in S's journal under S's
   certified roots. A consumer that has not learned of S can still be fed old-origin heads signed by a thief: there is
   no revocation channel, under the same communication assumption as PROTOCOL-82. Recovery does not make receipts a
   consumer already accepted from forged heads valid; it gives the evidence that they were forged.

**Assumptions that stay named.** One keybroker per certify seed: a cloned broker with copied `KEYS.certified` is two
signers of one key, and nothing in the protocol detects that before they equivocate. The seed and `KEYS.certified`
are backed up and restored together; restoring an older `KEYS.certified` resets the guard to an older head. The
decider's view is the Store's admitted fold, not a re-execution of signed calls, so a certificate's lawfulness rests
on the operator (BUILT-7's paragraph stands).

## BUILT-10 — PRE-ROTATION of the writer's certify key, as landed (real 2026-10-27; TRUST-5; KERNEL-79 + PROTOCOL-86 + HOSTING-61; `kernel!`; origin/main `276ba794`)

§4.4c items 3, 4 and 5, built, with one design change: the rotation is a kernel act inside the World, not a carry
to a successor World.

- **Item 3, the rotation rule.** `Authority.next` (one digest per certifier, `H(domCertifyNext ‖ key)`), carried
  in the genesis input (`domOrigin` v4, `badNext`) and the authority cell, now RAM at one fixed `authorityId`.
  `Body.rotateCertifier i key next`: member = the authority cell, signed by `key`, `key` opens the commitment at
  `i` and is no listed key; else `notPreRotated i` (declined, not recorded). Totality `effect_at_authority`;
  `authorityOf_honest_fold` now says the genesis authority or a run of pre-rotated rotations of it;
  `rotate_retires`, `rotateCertifier_authorityOf`: after a rotation only the new key is listed at its index.
  Spec B1 gains `Authorized.certifier`.
  *Why not the carry.* A carry gives the successor a new origin, so every consumer needs a succession rule
  (§4.4c's `Certified.succeeds`) and old receipts must be re-checked against a carried journal. Inside the
  World, a follower meets the rotation as one more step it re-executes; the origin, the log and the receipts stay.
- **Item 4, the successor secret.** `keybroker --certify-keygen OUT` writes a fresh seed to an operator-held
  file keybroker never reads (decided over a second broker: a second running process under the same account
  falls with the first; the successor is used once and needs no uptime). `host rotate-certifier STORE OUT
  NEXT` on a stopped writer; KEYS then takes OUT's line; `serve --certify` certifies the rotated base at start,
  now inline before the first frame (the queued start certification raced the first page: measured).
- **Item 5, consumers.** Certificates carry each signer's key; a signer holds its slot by its current key or by
  the key that opens the slot's committed digest (`Head.holds`; `otherKey` otherwise). A follower behind the
  rotation takes the successor's certificate; past it, it refuses the retired key's. Old certificates stay
  valid for their heads under those heads' own authority; receipts keep origin and journal. docs/TRUST.md says
  this in its "what happens to old certificates and receipts" paragraph.
- **Rows.** `rotateRefused` (plant `nextIgnoresKey`, caught line 7), `certifierRotation` (plant
  `retiredCertifier`, caught line 10; MEASURED red at lines 11–12 with the successor branch of `holds`
  removed). `launcher/tests/certify.rs` rotates a real Store.
- **Not built, by name.** A stranger with only the genesis input follows one rotation, not two; a follower two
  rotations behind refuses the second successor's page until it folds the first (cv 01a17e0d-0ea6).
  Reconfiguration (a new threshold, a certifier added or removed) has no act. No revocation channel: a consumer
  that has not reached the rotation still takes the retired key's signature.
