# DESIGN-P6 — replicated agreement for a World's writer: the object, its price, and whether to build it

Design memo, real 2026-10-23, by FABLE-P6. Read against nano `origin/main` = **231af0e** (GitHub is the
truth; the local mirror's `main` at 360e1ed is 106 files behind, so every nano path below was read with
`git show origin/main:PATH`), and against mini `hbox:/tank/dregg-build/pipeline/warm-base/src` at
**334316df** (read-only). Tags: **READ** (path:line, at those two tips) · **MEASURED** (a command I ran) ·
**INFERRED** (attack these first). Nothing was built; neither repository was edited.

## 0. The verdict, before the design (honesty over completeness)

**The strongest refuter is §7.3: do not start the engine now.** Three measured facts carry it.

1. **Nothing deployed needs a World to survive its host.** MEASURED: `git grep -n "killed\|kill(" origin/main
   -- 'client/tests/*.rs' 'launcher/tests/*.rs' 'Protocol/Rows*.lean'` finds one kill, the writer PROCESS in
   `client/tests/join.rs` (`drop(writer)` → `seal_stopped` → `supervise … serve` again, a 20 s liveness
   deadline, READ join.rs:38-52 and the tail at :284-290). No row, test or journey names a dead HOST. The
   availability nano already measures is process-loss: cold reopen **63–110 ms** on hbox
   (READ `gates/bar.tsv` run rows `reopen-ms` 63.128 / 105.249 / 110.074 at de718bf, b9cd50f), under THE
   BAR's limit of 60,000 ms. P6 buys a different fault class (node loss), and no consumer asks for it.
2. **The price §2(b) of PROGRAM-20261022 put on landed theorems is not there.** The program said the hypothesis
   "the folded log is a prefix of the decided log" lands on every follower and settlement path and restates
   `WriterLife`/`writer_life_trusted`. READ, every one of those theorems quantifies over a free log `l`
   (`World.fold X.env w l = .ok w'`) or over follow's OWN frames (`Reach`), and none names the writer (§2
   below, statement by statement). The hypothesis cost on landed theorems is **zero**. What P6 restates is
   the writer's MACHINE refinement (`Host/Proofs/Serve.lean` 19 theorems + `Refine.lean` 11, MEASURED
   `grep -c '^theorem'`), because `Serve.handle` judges and commits in ONE `Answer.commit` (READ
   `Host/Serve.lean:126-146`, `Host/Batch.lean:42-56`) and a committee must judge → propose → decide →
   commit. That is a smaller and differently-shaped price than the program's "6–9k Lean, 2–3 lane-weeks";
   it is also why §7.1/§7.2 come out as "smaller than planned", not as "wrong".
3. **The engine is the cost, and liveness is never its theorem.** Mini's Generic Simplex closure is 33 files,
   7,282 lines (MEASURED `wc -l Kernel/GenericSimplex*.lean | tail -1; ls … | wc -l` on hbox), its safety is
   stated over an executable `step` (READ `Kernel/GenericSimplexEngineSafety.lean:62-94`), and its own doc
   says twice "Liveness is NOT a theorem here" (READ `docs/GENERIC-SIMPLEX-NATIVE.md` §fix C and §quiescent
   leader). The view-change machinery (leader rotation, deadlines, CANDIDATE(⊥), safe parent, disable) is
   ~80 % of those lines and exists to buy availability, which is the part nobody has a row for.

**So:** the right first move is NOT card 1 of a build. It is to record this memo's measurement in
`decisions/host.md` (a `HOST-74 · P6 priced, not started` entry) and leave the trigger named: **the first
row whose World must outlive its host.** If Ember wants P6 regardless (the charter already calls it "a
planned, priced phase", READ `CHARTER.md` scope item 3), §8's card 1 is the smallest true thing, it needs
ONE decision from Ember first (a Store SIGNING key: custody, pause item 1), and cards 2–3 split safety from
liveness so that safety is complete before a single view ever changes.

The rest of this memo is the design, so that the decision is made against the real object and not against
the program's inferred one.

---

## 1. THE OBJECT — what a "decided log" IS in nano's terms

**What nano has today (READ).** A World's log is `List (Step D)` with `Step = turn t | refusal r`
(`Kernel/World.lean:246-249`). `World.fold E w l` folds it (`:1770-1779`); each step links the chain,
`stepLink E c s rs` over the roots digest after it (`:1781-1783`); `chainOf` replays the links from
`(Step × roots)` pairs without admitting (`:1788-1790`). A Store record is `List (Step D × D)`: each step
with the roots digest after it, run by `runRooted` at open, `rootMismatch` by name when the stated root is not
reached (`Host/Record.lean:1-16, 72-80`). A World's position is `Record.mark E w = (w.steps, E.bytes w.chain)`
(`Host/Record.lean:63`). **Follower soundness is landed:** `fold_head_binds` — two folds from one start to
one `(steps, chain)` are one log, or two explicit `foldPres` inputs collide (`Kernel/Proofs/Fold.lean:428-434`,
over `chain_binds :213`).

**The decided log, in those terms (INFERRED design).** A *decision* is a signed statement that a
`(steps, chain)` position is the World's: no new step kind, no new fold. Precisely:

- `Committee D := { keys : List ByteArray, f : Nat }` with `keys.length = 3*f + 1`, `f ≥ 0`, keys distinct.
  It is a GENESIS INPUT: `GenesisInput` today is `name × nonce × allowance × founders`
  (READ `Kernel/Receive/Follow.lean:36-41`), and the origin hashes exactly that
  (`originOf`, `:68-73`, domain `nanodregg/kernel/origin/v2`). The committee joins the input, so the World's
  identity commits to who may decide it, and `wrongWorld` (the FIRST check, KERNEL-24) refuses every call
  signed for a World with another committee.
- `Decision D := { steps : Nat, chain : D, epoch : Nat, sigs : List (Nat × ByteArray) }`: signer index into
  `committee.keys` and an Ed25519 signature over `domDecision ‖ origin ‖ u64 steps ‖ chain ‖ u64 epoch`.
  `Decided X cmt w d : Bool` = `d.steps = w.steps ∧ d.chain = w.chain ∧ sigs distinct ∧ sigs.length ≥ 2f+1 ∧
  every sig verifies under its key` (`Codec.Ed25519.verify`, READ `Codec/Ed25519.lean:220`; Lean also SIGNS,
  `sign :264`, with `sign_verifies` READ `Codec/Proofs/Ed25519/Sign.lean:150`, so no Rust signer is needed).
- **The decision is a Store record kind**, a second frame beside the batch record in the segment's framed log
  (frames are `u32 ‖ record ‖ tag`, READ `decisions/host.md` HOST-20 critique), so `World.fold` stays over
  `Step` and KERNEL's 224 `World.fold` lines (MEASURED, §2) see nothing. A decision frame at logical offset o
  certifies the position of the records before it. `Base.shapeStamp` covers the batch codec (READ
  `Host/Base.lean:124`, HOST-20): a new frame kind moves the stamp, so an old Store refuses `shapeMismatch`
  by name (§4).
- **The decided log of a World** = the unique log (by `fold_head_binds`) that reaches the newest `Decided`
  position from genesis. A replica's local World that has run past its newest decision is a PROPOSAL, not the
  World: it answers reads of the decided prefix and `undecided` for anything past it.
- **The committee of n = 3f+1 Store processes** are n followers (each re-derives every step, PROTOCOL-4,
  READ `decisions/protocol.md:93-110`) of which one, the leader, also derives. A replica SIGNS a position
  only after its own `Receive.judge` reproduced every step up to it (the vote is an audit, `audit_ok` as the
  vote rule). The decided log is therefore "what 2f+1 re-derivations agreed on", which is law 1's sentence
  "followers re-derive every Turn" with a count on it.
- **f = 0 is the lock writer.** A committee of one (n = 1, quorum 1): the writer certifies its own sealed
  positions with one signature. This is how law 1 is kept (one shape of a Store, one shape of "the World's
  position"), and how THE BAR's deployment (two friends + hosted Hermes, one `host serve` per World, READ
  `deploy/RUNBOOK.md:54-58`) stays a one-process deployment. The engine at n = 1 is the identity.

**The one-host plant, said precisely.** Lean can refuse (a) a committee whose size is not `3f+1`
(`committeeShape`), (b) a decision with fewer than `2f+1` distinct valid signatures (`quorumShort`), (c) a
signer twice (`signerRepeated`) or outside the committee (`signerUnknown`), (d) a page or base past the
newest decision (`undecided`). Lean CANNOT see which host holds which key: a host holding 3 of 4 seeds decides
alone and nothing in Lean refuses it. So "one host alone must refuse to decide" splits into a THEOREM
(`decided_quorum`: two decisions at one `steps` under ≤ f faulty share an honest signer; a mutation to `f+1`
votes reds it, §3) and a CUSTODY PREMISE (seeds of one committee on distinct hosts: a `gates/tcb.tsv` row
under HOST, kind `platform-fact`/`trusted-unverified`, and a RUNBOOK line). The row that drives it: four
Stores, three killed, a write to the survivor ends `open`/`uncertain` and never `ok` (§5). Pause item 1
applies: this introduces a Store signing seed; today `Keys` holds integrity-at-rest MAC keys only (HOST-16,
READ `Host/Proofs/Trusted.lean` module doc) and KERNEL-44 explicitly chose "NO host key" (READ
`decisions/kernel.md:1769+` "The receipt").

---

## 2. THE PREMISE PLACEMENT — measured, not guessed

Rule applied (READ `memory/minted-price-premises-not-only-cost.md`): a design's price is every premise it
adds to LANDED theorems; a binder is not a hypothesis; enumerate (1) statements that change, (2) hypotheses
gained and where discharged, (3) deletions.

### 2.1 The four named theorems keep their statements — read, with why

| theorem | statement's log variable | why P6 leaves it | READ |
|---|---|---|---|
| `stale_behind_forever` | `h₁ : World.fold E w₀ l₁ = .ok w`, `h₂ : World.fold E w l₂ = .ok w'`, `l₁ l₂` free | about pins along ANY fold; a decided log is one log | `Kernel/Proofs/Versions.lean:240-245` |
| `settle_final_never_admits` | `hf : World.fold X.env w l = .ok w'`, `l` free; `w` = the member's own World | about `submit` on any World reached from a settled one | `Protocol/Proofs/Settle.lean:201-207` |
| `staleBehind_final` | `h₁ h₂` folds from `w₀` (the W0 premise), `l₁ l₂` free | the follower's own fold; no writer named | `Protocol/Proofs/Behind.lean:249-256` |
| `audit_ok` | `audit X w l = .ok w' ↔ World.fold X.env w l = .ok w' ∧ Honest X w l` | a log is honest or not; which log is decided is a different question | `Kernel/Proofs/Audit.lean:275-277`, `Honest :195-200` |

Also unchanged, same reason: `submit_refused_final` / `submit_refused_never`
(`Kernel/Proofs/Refusals.lean:478-483, :495-500`: `World.refuse` then any fold), `settle_refused_final` /
`settle_refused_absorbed` (`Settle.lean:458-466, :489-497`: over `WindowedIn`/`Absorbed`, follow's own steps),
`check_committed` (`Protocol/Proofs/Receipt.lean:46-52`: a receipt against a World's roots), and PROTOCOL-64's
T0 `settled`/`step_settled_ok` (`Protocol/Command/Machine.lean:1047-1062`, `Protocol/Proofs/Command.lean:271,
:295`: follow settles on its OWN World). **KERNEL-44 finality** is `submit_refused_final` over the World that
RECORDED the refusal; under P6 the writer may only ANSWER `refused NAME` once the refusal step is decided, which
is a change in `Serve.handle`'s reply timing (§2.3), not in the theorem.

MEASURED, the whole spread: `git grep -c "World.fold" origin/main -- '*.lean'` = 59 files, 329 lines; by
proof layer Kernel 28 files/224 lines, Host 7/44, Protocol 6/18, Hosting 4/15, Lang 1/3, Ledger 0; theorem
statements with a `World.fold … = .ok` hypothesis: 114 (`grep -c` over `*/Proofs/*.lean`). Every one of
them takes `l` as a free binder. **Hypotheses gained by landed theorems: 0.**

### 2.2 `WriterLife` / `writer_life_trusted` are NOT restated

READ `Host/Proofs/Trusted.lean:239-253`: `WriterLife keys file₀ fileN` is an inductive over a base FILE:
`link` = one `openWith` of the file, an admitted fold `World.fold X.env o.opened.world l = .ok w'`, a seal
`Base.file … w' … = .ok file'`. It names no writer, no lock, no log position's authority; HOST-69 says so:
"Stated over opens and seals only" (READ `decisions/host.md:3117-3124`). Each committee replica is a Store
with its own files, opens, folds and seals, so `writer_life_trusted` holds per replica AS STATED
(`CheckpointTrusted` at the replica's origin, discharged by `genesis_life_trusted` for the founding replicas
and `import_life_trusted` for a joined one). HOST-71 already recorded the same reading for adoption
("HOST-69's WriterLife … unchanged; received-base adoption still does not … become a WriterLife link", READ
`decisions/host.md:3244-3255`). The program's §2(b) "restated over the decided log's writer" was INFERRED and
is refuted by reading: there is no "writer" variable to restate. What P6 ADDS beside it is the new theorem
`replica_prefix_decided` (§2.4), stated over the SAME `WriterLife` plus the decision frames in the file.

**Law 4's text.** "The writer lock IS the append fd" (READ `CHARTER.md` law 4; `Host/Store.lean:19-20,
342-353, 379-380`: `Writer.lock` is the key file's flock'd read handle held by `Writer.hold`) stays a
PER-STORE fact: exactly one process appends to one Store's files. It stops being THE safety argument for
"one log per World" only at f ≥ 1, where that argument becomes `decided_quorum` + `fold_head_binds`. The
charter sentence to change is the parenthetical in law 4, not the lock.

### 2.3 What DOES restate (the real price), measured

**(a) The writer's machine refinement — restated, no hypothesis.** READ `Host/Serve.lean:126-146`:
`handle` on `.submit` runs `judge X w c` and returns `.commit (.turn t) w' ok receipt` or
`.commit (.refusal r) w' st p` in ONE answer; `Machine.step` stages the step with its roots note and pushes
the reply (READ `Host/Batch.lean:67-84`). `Host.Proofs.Serve.step_submit` states the machine's step IS
`judge`'s (`Host/Proofs/Serve.lean:98-102`) and `Refine.host_step_folds/host_run_folds/host_run_audits/
host_run_kept/host_reopen_folds` + four teeth lift it to an admitted fold (`Host/Proofs/Refine.lean:177,
223, 246, 261, 293, 324, 383, 451, 467, 510`). Under P6 the leader's `submit` answer becomes
`.propose (step) w' …`: the step is staged in a PROPOSAL buffer, the reply is deferred (the existing
`Answer.defer` shape, `Host/Batch.lean:52-55`) until the position is `Decided`, then committed and answered
with `ok`/`refused NAME` exactly as today. MEASURED: 19 + 11 = **30 theorems restate** (binder: the proposal
buffer; `step_submit`'s conclusion changes meaning: "the machine's step is judge's" → "the machine's step is
judge's into the proposal, and the commit is the decided prefix of the proposal"). At f = 0 the proposal
commits in the same batch, and every restated theorem specialises to today's statement (a corollary each,
kept as teeth).

**(b) The follower's page gate — one new refusal, no restatement.** READ `Protocol/Command/Machine.lean:
508-516`: `absorbPage` re-derives the page and requires `w'.steps = steps ∧ chain = stated`, else
`chainMismatch`; the stated `(steps, chain)` is the WRITER's word (`chainMismatch` catches a lying page only
because follow re-derived). Under P6 the `log` reply carries the newest `Decision` and `Command.step`'s log arm
refuses a page whose end is past it with `undecided` BEFORE `absorbPage`. So `absorbPage`, `Absorbed`,
`WindowedIn` and the 28 + 14 + 7 + 3 absorb theorems (MEASURED `grep -c 'absorbPage\|Absorbed\|absorb '`
over Command/Settle/FollowHead/Allowance Proofs) are untouched. INFERRED ≤ 10 theorems in
`Protocol/Proofs/Command.lean` that unfold the log arm (`step_cont`-family, `absorbPage_base`'s caller) gain a
binder; the IMPACT file measures it by statement-digest diff (`Census/Statements.lean`, `gates/census.py`).

**(c) `Thin.accept` and PROTOCOL-47's pin — a certificate beside the sponsor's pin.** READ
`Protocol/Thin.lean:1-20, 142`: a thin member adopts bytes that hash to a pin a sponsor signed. P6 adds: the
pinned position must be `Decided` (the served base carries its decision frame). `accept_done`/`accept_moved`
(`Protocol/Proofs/Thin.lean`, 4 theorems) gain a binder. The sponsor's pin stays the trust root (PROTOCOL-61);
the certificate is what makes `CheckpointTrusted` for a RECEIVED base dischargeable in principle (HOST-64's
named gap) — NOT claimed here; it would be its own theorem with the custody premise.

**(d) PROTOCOL-41's "a reply is FINAL only when the refusal is recorded"** (READ `decisions/protocol.md:1020`)
becomes "…recorded in the decided log": a text change in the decision and in `Settle.verdictReply`'s
docstring; no theorem.

### 2.4 The hypothesis, stated ONCE, and where it is discharged

```lean
/-- A replica's World is the fold of a prefix of the decided log: its newest Decided position
    `(s, c)` is on its own fold. -/
def PrefixDecided (X : Ctx D) (cmt : Committee D) (w : World D) (d : Decision D) : Prop :=
  Decided X cmt d = true ∧ ∃ g l₁ l₂ w₁, World.fold X.env g l₁ = .ok w₁ ∧ w₁.steps = d.steps ∧
    w₁.chain = d.chain ∧ World.fold X.env w₁ l₂ = .ok w
```

It is a hypothesis of NEW theorems only: `replica_prefix_decided` (a replica that signs only positions on its
own fold — `signOnce`, §3 — and absorbs only `Decided` pages keeps `PrefixDecided` along its `WriterLife`;
discharged by induction over `WriterLife` exactly as `writer_life_trusted` is, with `absorbPage`'s
re-derivation as the per-page fact) and `decided_unique` (§3). Nothing landed takes it. Where the program
expected it to "land on every settlement path", the settlement paths already settle on follow's OWN World
(T0), and that World is `PrefixDecided` by construction once the page gate exists.

### 2.5 Deletions

`Writer.lock`'s docstring claim that the lock is THE safety argument (`Host/Store.lean:19`); charter law 4's
parenthetical; KERNEL-45 item 4's "DEFERRED behind a second writer for one World" (READ
`decisions/kernel.md:1888-1913`) is NOT fired by P6 (one decided log is still one World), say so there.

---

## 3. THE SAFETY THEOREM — Generic Simplex restated over nano's executable step

**Mini's statement (READ).** `CommittedAt tr faulty v b := (v = 0 ∧ b = []) ∨ ∃ time party, party ∉ faulty
∧ tr time = .commit party view block` (`Kernel/GeneralSimplexReachability.lean:13-14`);
`committed_prefix_consistency : LocalFaithful tr roster faulty f → roster.card = 3f+1 → faulty.card ≤ f →
CommittedAt v b → CommittedAt w c → b.IsPrefix c ∨ c.IsPrefix b` (`:109-113`); over the executable engine:
`actual_committed_prefix_consistency (reachable : Reachable c faulty checked time net) (size) (faultBound)
… : a.IsPrefix b ∨ b.IsPrefix a` and the certificate form `actual_certificates_prefix_consistent` over
`AttributedCommitSends` = "∃ signers ⊆ roster, 2f+1 ≤ card, every HONEST signer sent COMMIT for the block"
(`GenericSimplexEngineSafety.lean:62-80`; `GenericSimplexCertificateSafety.lean:14-17`). A mini `Block` is
the FULL history (`List Bytes`; "the full block (exact ancestry)", READ `GENERIC-SIMPLEX-NATIVE.md` §quiescent
leader), so "prefix" is list prefix.

**Nano's restatement (INFERRED, the statement; every ingredient landed).** Nano's "full block" is the
chain: `chainOf` commits the whole log, and `fold_head_binds` turns equal `(steps, chain)` into equal logs.
So prefix consistency is about positions:

```lean
/-- Two decisions of one World, under at most f faulty signers, name positions on ONE log:
    the later chain is reached from the earlier by the steps between them, or two explicit
    chain inputs collide. -/
theorem decided_unique {X : Ctx D} {n : Nat} (hE : X.env.Lawful n) {cmt : Committee D}
    {faulty : Finset Nat} (hf : faulty.card ≤ cmt.f)
    {g w₁ w₂ : World D} {l₁ l₂ : List (Step D)} {d₁ d₂ : Decision D}
    (hhonest : ∀ i ∉ faulty, SignsOnce X cmt i)           -- the vote rule, §3.1
    (h₁ : World.fold X.env g l₁ = .ok w₁) (hd₁ : Decided X cmt d₁ = true) (hp₁ : d₁.steps = w₁.steps ∧ d₁.chain = w₁.chain)
    (h₂ : World.fold X.env g l₂ = .ok w₂) (hd₂ : Decided X cmt d₂ = true) (hp₂ : d₂.steps = w₂.steps ∧ d₂.chain = w₂.chain)
    (hs : d₁.steps ≤ d₂.steps) :
    (∃ l, l₂ = l₁ ++ l) ∨ CollidesAmong X.env.hash (foldPres X.env g l₁ ++ foldPres X.env g l₂)
```

**What it quantifies over.** Every fold from a common start `g` (genesis or a carried World), every pair of
decisions that verify (`Decided` is executable: signature checks and counting), every faulty set of size ≤ f,
and every HONEST signer's behaviour under the vote rule. The adversary is free: a faulty signer may sign
anything (mini: "Byzantine signers have no protocol-behavior premise", READ CertificateSafety:11-13). The
collision disjunct is over the EXPLICIT `foldPres` lists (the census's `CollidesAmong hash S` form, READ
memory `minted-a-disjunct-provable-from-the-premises-is-vacuous`), inherited from `fold_head_binds`.

### 3.1 The vote rule, in two strengths (this is where the engine's size comes from)

- **Sign-once (cards 1–2).** `SignsOnce X cmt i := ∀ s c c', signed i s c → signed i s c' → c = c'`, enforced
  locally: a replica journals its own signature per `steps` in its Store (a frame, like a recorded refusal:
  the same "remember what you did" that KERNEL-44 gave refusals) and refuses to sign a second chain at a
  position it signed (`alreadySigned`). Then `decided_unique` is quorum intersection: `2f+1 + 2f+1 > 3f+1` ⇒
  an honest signer in both certificates ⇒ equal chains at the smaller `steps` ⇒ `fold_head_binds` ⇒ equal
  prefixes. ~200 lines INFERRED, no `LocalFaithful`. The cost is LIVENESS: a position whose signatures split
  (2 for chain A, 2 for chain B after a leader crash mid-proposal) can never reach 2f+1 — the World HALTS at
  that position. Recovery is the charter's fork rule: a new World by re-genesis from the decided export
  (`host export` at the newest decision; law 1 "a fork is a new World"). Honest: safety complete, availability
  worse than one writer in that case. Liveness is not a theorem (it is false here by construction).
- **Simplex's rule (card 3).** A signature is per (view, position); a replica may sign a different chain for
  the same position in a LATER view only after 2f+1 CANDIDATE(⊥) disabled the earlier view (mini's
  `committed_not_disabled`, `honest_vote_has_safe_origin`, READ CertificateSafety:40-55 via
  `GeneralSimplexReachability`). `SignsOnce` is replaced by `LocalFaithful`-shaped rules over nano's
  replica step, and `decided_unique`'s `hhonest` premise is DISCHARGED by the replica's executable step
  (mini's `actual_local_faithful`: "derived from actual executable reachability", READ EngineSafety:52-60),
  so the final theorem's premises are `Reachable` + `faultBound` only. Mini's proof of this is the 7,282
  lines; nano's would restate it over `Committee`/`Decision`/`World.step` (law 11: from the theorem, smaller;
  INFERRED 3–4k lines because nano's block is a digest, not a list, and the ancestry lemmas become
  `fold_head_binds`).

**The deployed mutation that falsifies it (the tooth).** `Decided`'s count `2*f+1` → `f+1`. Mini's own
witness is exactly this: `hostile_run_conflicting_commits` — with `excessFaulty = {2,3}` (f+1 = 2 of 4)
honest parties 0 and 1 commit `thirdBlock` and `otherBlock` in one view (READ
`GenericSimplexWitnesses.lean:82-107`), and the engine stays `LocalFaithful` throughout
(`overfault_execution_faithful`, EngineSafety:105-107: "Fidelity does not hide the fault bound"). Nano's
plant, as a ROW over four real Stores (§5): partition {0,1} | {2,3}, two leaders, mutated quorum f+1 → two
`Decided` frames at one `steps` with different chains, found by `host check --committee` reading all four
Stores → RED by name `decidedDisagree steps`; unmutated, the row reaches `undecided` on both sides and no
second certificate exists. Assert the mutation happened before reading the verdict (memory
`minted-a-falsifier-that-stopped-falsifying`): the plant prints the mutated constant.

---

## 4. THE WIRE AND THE FLAG DAY

**What the record format gains (INFERRED, each item its law-1 reading).**
1. `GenesisInput` gains `committee : List ByteArray × Nat`; `domOrigin` v2 → v3, `domGenesis` v1 → v2
   (READ `Kernel/World.lean:311`, `Kernel/Receive/Follow.lean:46-48`). Every old call is `wrongWorld` in the
   new World (KERNEL-24), which is what OPS-1 already relies on for a carry (READ `decisions/ops.md:45-48`).
   `Carried` (READ `Kernel/World.lean:286-300`) gains the committee for the new World (a carry may change it:
   that IS reconfiguration, done as re-genesis, which is mini's own conclusion: "Reconfiguration must preserve
   existing liabilities; a fresh file or epoch number is not proof that old certificates cannot complete" —
   READ `GENERIC-SIMPLEX-NATIVE.md` §Durable decisions. Nano's answer: old certificates are over the OLD
   origin and verify for nothing in the new World; no liability crosses, by KERNEL-24).
2. `Keys` gains a signing seed (Lean signs with `Codec.Ed25519.sign`); the committee's public keys are in the
   World (genesis), not in `Keys`.
3. A second segment frame kind, `decision`, codec `Decision`; `Base.shapeStamp` moves ⇒ every old Store opens to
   `shapeMismatch` 43 by NAME, never reinterpreted (READ HOST-20 `decisions/host.md:455-503`, `Host/Base.lean:
   13-14, 474, 516`). A base file carries the newest decision at or before its position (the thin member's
   adopt reads it with the base, PROTOCOL-47's pin unchanged).
4. The `log` reply layout gains the newest `Decision` (one field; `Host/Page.lean`'s `build`); the `read`
   (base page) layout gains it. Call codec UNCHANGED (no new `Receive.Body`: call kinds stay 13/13, READ
   `SIZE.md`). Protocol ops: `propose`/`vote` as two ops would raise the ceiling 7 → 9 (SIZE line required);
   the alternative that raises nothing is ONE op `agree` whose payload tags propose|vote|decision, which
   law 7 permits as long as each tag refuses by name. I prefer the one op (fewer shapes).

**The Rust transport for votes (law 2: Lean decides the vote, Rust moves it).** The exact boundary:
- Lean `Serve.handle` receives `agree` frames on `host.sock` like every op and DECIDES: a `propose` frame is
  re-derived (`judge` per step, the audit) and answered with a `vote` frame or a refusal by name
  (`eventMismatch`-class names reused: a replica votes for nothing it did not re-derive); a `vote` frame is
  verified (`Ed25519.verify`) and counted; at 2f+1 Lean WRITES the decision frame, commits the proposal
  prefix and releases the deferred `ok`/`refused` replies. Lean also SIGNS (no Rust key use). The replica's
  outgoing frames are REPLIES on the connection that carried the peer's frame, so Lean never dials.
- Rust `nd-peer` (a sibling of `nd-members`, READ `launcher/src/bin/nd-members.rs:1-30`; built from `mux`'s
  pieces, READ `client/src/mux.rs:1-14` "parses no payload and decides nothing"): holds one connection from
  each replica's `host.sock` to each other replica's, relays `agree` frames both ways, retries with the
  journal's obligations (a replica re-sends its newest proposal/vote on reconnect; Lean emits them, Rust moves
  them), and names every close (`CloseReason`). It parses frame headers only. Fault model carried in a
  `gates/tcb.tsv` row: "authenticated reliable delivery" is NOT assumed from Rust — authentication is Lean's
  signature check, reliability is Lean's re-send-on-ask; what Rust is trusted for is "a frame it forwards
  is a frame it received" (byte relay, the same sentence shape as the E2 `stdio-leg` row, READ
  `gates/tcb.tsv` last row).
- Could Lean dial directly? `Host.Sock` is THE Lean client end of a Unix socket (READ `Host/Sock.lean:1-18`:
  "a future Host serve extends sock.c rather than adding a second socket C file"); cross-HOST votes need TCP,
  which that C does not have (`nd_unix_connect`). Adding TCP to `sock.c` raises C lines 315/315 (a ceiling).
  So Rust relays; the C ceiling is the reason, stated.

**Every Store re-geneses.** What re-emits: every World's genesis (`host genesis … --committee K…`), the
Std.hole/offer/Bell packages re-install into the new Worlds (package ids are content, unchanged; their
INSTALLS are new Turns), `deploy/units/STORE.md` (generated from `Host.Store.layout`), the RUNBOOK's genesis
section, `gates/codec-vectors.tsv` rows for the new frame and genesis input, `gates/waste.tsv` gains
`agree hashes-per-decision` and `log bytes-per-decision` with ceilings. Named as the flag day in the landing
commit: shape changed = genesis input, segment frame kinds, log/read reply layouts; refuses to load =
`shapeMismatch` for every pre-P6 Store, `wrongWorld` for every pre-P6 call. Never priced as a reason: a
rebuild is the answer to "what does it cost" (CLAUDE.md).

---

## 5. THE AVAILABILITY ROW

**What exists (READ).** `client/tests/join.rs:112-190`: one `host genesis`, a writer under `nd-supervise`
(`supervise_host`, READ `devtools/src/lib.rs:178-216`), followers per member, `drop(writer)` → the child exits
on stdin's end → `seal_stopped` retries `host seal` while `locked`, 20 s deadline (`neverUnlocked`) →
`supervise … serve` again (join.rs:284-290). `client/tests/real.rs` runs writer + follower on two Stores from
one genesis (`:1-7`). THE BAR records `reopen-ms` and `follow-reopen-ms` as `run` rows and judges `limit` rows
(`gates/bar.tsv` header). Kill discipline: the Supervisor's Drop sends SIGTERM to its one child by PID
(CLIENT-30; never by pattern).

**What it becomes (INFERRED).** `client/tests/committee.rs`: `host genesis … --committee` with four keys →
four Stores B0..B3 each `supervise(… "serve" STORE "--replica" i)`; `nd-peer` wiring the four `host.sock`s;
member `a` writes `1=hello` via B0 (the leader of epoch 0): expect `ok` and `host check --committee` shows
one `Decided` at `steps = s`; `drop(leader)`; start a timer; `a.write 2=next` via B1: expect `ok` within
`failoverMax`; record `failover-ms`. Then the plants in the same file: (i) three killed, a write via the
survivor ends `open` (attempt left open) and `lookup` answers `absent`/`uncertain`, never `ok`, within the
same bound (the one-host plant's row); (ii) the quorum mutation of §3 under a partition → `decidedDisagree`
RED. The row's control: the counts `steps/cmd` and `seg-bytes/cmd` the BAR already pins (bar.tsv columns)
must not move for n = 1 (byte-identical records at f = 0: the decision frame is the only addition and is
counted separately).

**The bound, named.** Mini's view timer: `viewTimeout = timeout · 2^min(views since last commit, backoffCap)`,
fixture `backoffCap = 3`, 100 s → 800 s (READ `GENERIC-SIMPLEX-NATIVE.md` §fix C; theorems `viewTimeout_bounds`
EngineSafety:117-122). For nano: `Bounds.agreeTimeoutMs` and `agreeBackoffCap` as `Bounds` (law 4), with
`failoverMax = agreeTimeoutMs · 2^agreeBackoffCap` a DERIVED `limit` row in `gates/bar.tsv`
(`limit failover-ms …`), and `run` rows per measured failover. A number I would propose and expect to be
argued: 2,000 ms · 2^3 = 16 s on a quiet box. The row judges a `run` against the `limit` in full mode only,
like `write-p99-ms`. The claim the row makes is a MEASUREMENT on one box; it is not liveness and the
decision entry says so in those words.

**Cards 1–2 have a weaker row:** at sign-once (no view change) a killed leader is a HALT, so the row there is
(i) the one-host plant and (ii) "a killed FOLLOWER replica does not stop writes" (3 of 4 serve). The
failover row needs card 3.

---

## 6. WHAT IT DOES NOT BUY, plainly

- **Liveness is never a theorem.** Not in mini (said twice in its doc), not here. Cards 1–2 do not even
  have it empirically (a split position halts the World). Card 3 has it empirically on one box under a
  configured bound, and the paper's argument needs `timeout ≥ 7Δ` after GST, which nobody measures.
- **Merge stays refused (§2(c) of the program).** A decided log is ONE log; two decisions that disagree are a
  SAFETY failure (`decidedDisagree`), not two histories to reconcile. `fold_head_binds` is the reason: the
  object every fold-extension theorem is stated over is one list. A halted World (sign-once split) is
  recovered by re-genesis from the decided prefix's export, which is "a fork is a new World" applied to
  the honest prefix, and no theorem over `World.fold` loses its object.
- **Cross-World atomic commitment stays out.** E6 (multi-signer Turns, KERNEL-45 item 2) and KERNEL-45
  item 4 are untouched: a decision certifies one World's position. Nothing here lets two Worlds decide together.
- **How a decided log composes with E5's heads (landed at 1f09446, PROTOCOL-65).** READ
  `Protocol/Proofs/Foreign.lean:72-86`: `foreign_receipt_sound` takes `hr : the head cell's rootsB decodes to
  wA.roots` — "the held head is a head of A" — as its named premise (head freshness, thin-member trust). A
  head cell of A held in B is `Std.head … .at w h₀ rootsB s₀` (a position with roots). P6 lets the head
  carry A's `Decision` for `s₀`; `Decided` of A's committee replaces "B's member followed A" as the reason
  to believe `hr`. The premise does not vanish — it becomes "A's committee has ≤ f faulty" plus the custody
  row — but a forged head now needs 2f+1 of A's keys instead of one follower's word. `forkedHead`
  (`head_forked_frozen`, PROTOCOL-65) at the same `steps` with different roots becomes evidence of A's
  SAFETY failure, recordable as such. One lane-day, card 4.
- **It does not make nano a model of its Rust.** The relay row is one byte-relay sentence; every decision
  (re-derive, verify, count, sign, commit, refuse) is in `Serve.handle`.
- **It does not give a RECEIVED base `CheckpointTrusted`.** Possible later with the custody premise; not here.

---

## 7. THE REFUTERS — three ways this design is wrong, each with its measurement

### 7.1 "The prefix hypothesis cannot be stated without a Canon-like premise on cell theorems" — REFUTED

Measurement, done: the hypothesis `PrefixDecided` (§2.4) is over `World.fold` and `(steps, chain)`; the
theorems it feeds (`decided_unique`, `replica_prefix_decided`) use `fold_head_binds`, whose premises are
`E.Lawful n` and two folds (READ `Fold.lean:428-431`): no `Canon`, no `RowsCanon`, no `JournalCanon`. The
cell theorems never see it: MEASURED, `World.fold` appears in 224 Kernel proof lines and NONE of them
would take `Decision` or `Committee` (the decision is a Host frame, not a `Step`). If a builder finds
themselves adding `hd : Decided …` to a Kernel theorem, the design has leaked and the card stops. The
KERNEL-41 lesson is kept by construction: the decision lives beside the fold, as the journal lives beside
the cells.

### 7.2 "HOSTING-43's `Reach` premise already IS the decided-log prefix; the design is smaller than planned" — HALF TRUE, and the half that is true is why §2 came out at zero

READ `Hosting/Proofs/Socket.lean:277-310`: `Moves`/`Reach` move follow's World only by `Command.step` on
follow's own frames; `FollowRun` quantifies over every result a frame is handed. It is NOT a prefix relation
to any writer's log; it is "nobody but follow moves follow's World". The prefix relation to the writer's log
lives in `absorbPage`'s `chainMismatch` check against the writer's STATED `(steps, chain)`
(`Machine.lean:508-516`), and T0 made every settlement read follow's own World (PROTOCOL-64). So: the
follower side of P6 is exactly ONE change — the authority of the stated position moves from "the writer
said" to "2f+1 said" (the `undecided` page gate) — and the rest of the follower is already shaped for it.
That is smaller than §2(b) planned (it planned a hypothesis on every path). What is NOT smaller is the
writer: 30 machine-refinement theorems restate (§2.3a). Measurement to confirm before building: write
`decided_unique` and `replica_prefix_decided` as STATEMENTS at 231af0e (2 h, no proofs), run the statement
census, and count (a) landed theorems whose digest changes — expected 0 in Kernel/Protocol/Hosting, 30 in
Host/Proofs/{Serve,Refine}, ≤ 10 in Protocol/Proofs/Command, 4 in Thin; (b) hypotheses (not binders) added to
any landed theorem — expected 0. If (a) in Kernel > 0 or (b) > 0, §7.1 has fired and the card stops.

### 7.3 "Single-writer-per-World with E5 receipts already gives the availability a row needs; P6 should not be built" — THE STRONGEST, as §0 says

Measurement, done: (i) zero rows/tests/journeys name a dead host (grep in §0); (ii) process-loss recovery
is measured at 63–110 ms reopen (bar.tsv) with a 20 s harness deadline (join.rs) — i.e. the availability
every existing row needs is already a PASS row; (iii) E5 moves knowledge between Worlds asynchronously
(`foreign_receipt_sound`), which is what Ember's "cross-host: we do need to think about this" asked for, and
it landed without agreement. What P6 adds is a World that outlives its host, for which no consumer exists.
Against it: the charter calls P6 "planned, priced" and Ember opened it; the program's §2(b) priced it at
6–9k Lean and 2–3 lane-weeks on an INFERRED premise spread that this memo measured at zero hypotheses and
~45 restatements. **What flips 7.3:** a row whose World must survive its host. The only candidate I can
see in the deployed system is the hosted Hermes resident's World when the hosting box dies — and today the
resident dies WITH its box (nd-members runs on the writer's host, READ `nd-members.rs:1-30`; RUNBOOK §
"Writer's node"), so even that row would first need the resident's host and the World's host to be different
machines, which is an OPS decision nobody has made. Measure: ask Ember for the row; if none, record and stop.

A fourth, smaller way it is wrong, named because it is the one that would bite a builder: **a Store signing
seed is a custody object** (pause item 1). KERNEL-44 refused a host key for refusal receipts because the chain
proves them (READ `decisions/kernel.md` KERNEL-44 "The receipt"). P6 cannot avoid it: a decision is a
signature by construction. The seed's home (`Keys`, same file as the MAC keys, 0600, read by `host` alone)
and the rule "one committee's seeds on distinct hosts" are Ember's to rule BEFORE card 1.

---

## 8. THE CARDS — in order, with consumers and plants, sized in lane-days

Format: lands · consumer · deletes · premise price (hypotheses on LANDED theorems) · gate · plant · refuter.
Method per R-0069 (READ `RULINGS.tsv` R-0069): land when the builder's build + plants are green; fast judge
at most; convergence per batch; Grok only on a NAMED fork (there is one: card 2's sign-once vs. card 3 first,
§3.1); no RELEASE rows; GitHub is the truth. The STALL-WATCH tail shows the batch rule catching in 19 min
what eight fast landings missed (00ed907: `atGenesis` refused every honest adopt): card 1 touches genesis,
so its batch convergence must include `cargo:client:join` and `rows --deployed`.

**P6-0 · The measurement (0.5 day, before any build).** `promo/IMPACT-P6.md`: the §7.2 statement census at
231af0e (two statements written, no proofs; the digest diff); the §0 grep as a table; the per-row Worlds list
(NVM E.1's refuter, still owed by the program). Consumer: Ember's decision on the signing seed and on 7.3.
Price 0. Gate: none (a file). Refuter: if the census shows a Kernel statement moving, stop.

**P6-1 · The committee and the certificate, no engine (1.5 days). The smallest true thing.** Lands:
`Committee` in `GenesisInput` (`committeeShape` refuses `n ≠ 3f+1`, repeated or malformed keys; `f = 0` is
allowed and IS the lock writer); `Keys.signing`; `Decision` codec + `Decided`; the `decision` segment frame
written at every seal (f = 0: one signature by the writer itself) and read by `openWith` (a base whose
position has no decision frame at or before it is `undecided`; a decision that does not verify is
`decisionCorrupt`); the `log`/`read` reply field; `Thin.accept` requires `Decided` of the pinned position;
`Command.step`'s log arm refuses a page past the newest decision `undecided`. Theorems: `decided_quorum`
(two certificates at one `steps` under ≤ f faulty share an honest signer: counting, ~40 lines),
`decision_bytes_roundtrip`, `thin_accept_decided`, `genesis_committee_origin` (two geneses with one origin
have one committee, from `genesis_inj`). Consumer: `host check` prints the newest decision; the thin adopt
in `join.rs` (member `c`) now checks it; the invite's pin (PROTOCOL-47) unchanged. Deletes: nothing yet
(law 4's parenthetical in card 5). Price: 0 hypotheses; restated by binder: `accept_done`, `accept_moved`
(+2), `openWith_*` consumers gain the frame (INFERRED ≤ 6). Gate: `host!` + `protocol!` (flag day, §4).
Plants: `committeeShape` with a 3-key committee → RED by name; a decision frame with `f+1` signatures →
`quorumShort`; a flipped signature byte → `decisionCorrupt`; the pre-P6 Store from `plant-old-shape` →
`shapeMismatch`. Refuter: if the f = 0 self-certificate adds a WASTE row that does not stay ≤ one
signature per seal, the shape is wrong (a decision per RECORD would be O(appended records) signing).
**Blocked on Ember: the signing seed.**

**P6-2 · Sign-once replication, fixed leader (2 days).** Lands: `Serve.handle` `.submit` → `.propose`
(deferred reply), the proposal buffer in `Loop`, the `agree` op (propose | vote | decision tags), a replica's
vote = re-derive (`judge` per step) then sign, `SignsOnce` journaled per `steps` (`alreadySigned` refusal),
commit + release at 2f+1; `nd-peer` (Rust, relay only, PID file, named closes); `decided_unique` under
`SignsOnce` (§3, quorum intersection + `fold_head_binds`); `replica_prefix_decided` over `WriterLife`;
the 30 Host machine theorems restated with the f = 0 corollaries kept as teeth. Consumer: `committee.rs`
(four Stores; a write decided; a killed FOLLOWER replica does not stop writes; three killed → the survivor
never says `ok` = the one-host row). Deletes: the docstring claim that the lock is the safety argument.
Price: 0 hypotheses; 30 + ≤ 10 restatements (measured in P6-0). Gate: `host!`. Plants: quorum `f+1` under a
{0,1}|{2,3} partition → `decidedDisagree` RED (assert the mutation printed); `nd-peer` forwarding a frame it
did not receive → `badSignature` at the replica (the relay row's tooth); a replica voting without
re-deriving → `eventMismatch` plant from PROTOCOL-4's audit row. Refuter: if `decided_unique` needs any
premise beyond `hE`, `hf`, `SignsOnce` and the two folds, §7.1 fired. **Named fork for the one Grok read:**
sign-once first (this card) vs. Simplex rules first (card 3 without card 2). My default: sign-once first,
because it lands the safety theorem in ~200 lines and the halt-on-split is honest and recoverable by the
charter's own fork rule.

**P6-3 · Simplex views: the engine (5–8 days).** Lands: views, leader `(view − 1) % n`, `enterView` with
`Bounds.agreeTimeoutMs · 2^min(…, agreeBackoffCap)`, CANDIDATE(⊥), the safe-parent and disable rules, the
quiescent leader (`hasWork`, READ mini doc), the journal of inputs with checkpoints (mini's log format 4:
a base frame may carry the engine state) — restated over `Committee`/`Decision`/`World.step` by law 11
(statement first, mini's code never copied). `SignsOnce` → per-(view, position) with disable; `decided_unique`
re-proved with its `hhonest` DISCHARGED from the replica's executable step (mini's `actual_local_faithful`
shape). Consumer: the failover row (`failover-ms` limit + runs in `gates/bar.tsv`). Price: 0 hypotheses;
card 2's `decided_unique` statement unchanged, proof replaced. Gate: `host!` (the engine state in the base).
Plants: mini's two, restated: the recorded-stall replay (two COMMITs in views 1–2, then commit in view 3
under backoff; fixed timer commits nothing → RED without backoff) and `always-work` (idle views grow
without bound → the row's step count rises → RED). Refuter: mini's own warning — "A Δ above
timeout·2^backoffCap/7 is still not survived" — makes the failover row a measurement on one box, nothing
more; if the row cannot be made to fail by a mutation (not by load), it is not a row.

**P6-4 · The decided head for E5 (1 day).** `Std.head`'s `.at` carries the decision; `foreign_receipt_sound`'s
`hr` discharged from `Decided` + the custody row; `forkedHead` at equal `steps` recorded as A's safety
failure. Price: `foreign_receipt_sound` RESTATES (its premise `hr` is replaced, meaning changes: say so);
`head_at_at`/`head_forked_frozen` gain a binder. Gate: `protocol!`.

**P6-5 · The text (0.5 day, plain commits under R-0069 (3)).** `CHARTER.md` law 4's parenthetical; scope item
3 "planned, priced" → "landed at f ≥ 1 for …" or "priced, not started" (whichever §0 decided); `decisions/
host.md` HOST-74 with CRITIQUE (a committee of one Store is a lock writer with a signature: did we add a
shape?) and META-CRITIQUE (the program priced an INFERRED premise spread; this memo measured it; the bias was
"a distributed object must cost every theorem"); `gates/tcb.tsv` rows: `nd-peer` byte relay, committee seeds
on distinct hosts; RUNBOOK §genesis `--committee`.

**Sizes.** P6-0 0.5 · P6-1 1.5 · P6-2 2 · P6-3 5–8 · P6-4 1 · P6-5 0.5 = **10.5–13.5 lane-days**, of which
the engine is half. Lines INFERRED: P6-1 ≈ +600 Lean; P6-2 ≈ +1,200 Lean, +700 Rust; P6-3 ≈ +3–4k Lean;
theorems ≈ +35 (not the program's +60: `decided_unique` is one theorem, proved twice).

**What I would do tomorrow if Ember says "build":** P6-0 as one 2-hour lane (statements + census), hand its
IMPACT file and this memo's §1 to the SAME lane for P6-1 (send the veteran back), with the signing-seed ruling
in its brief as a DECISION already made, not a question.

---

## Appendix — commands behind MEASURED tags

- Tips: `cd ~/dev/nanodregg && git fetch origin && git log --oneline origin/main -1` → 231af0e; `git rev-parse
  --short HEAD` → 360e1ed; `git diff --stat origin/main HEAD | tail -1` → 106 files. hbox: `git rev-parse
  --short HEAD` in `/tank/dregg-build/pipeline/warm-base/src` → 334316df.
- Spread: `git grep -c "World.fold" origin/main -- '*.lean' | awk -F: '{n++; s+=$NF} END{print n, s}'` → 59, 329;
  per layer the same over `'Kernel/Proofs/*.lean'` etc.; statements: `git grep -n "World.fold X.env\|World.fold
  E " origin/main -- '*/Proofs/*.lean' | grep -c "theorem\|(h[a-z₀-₉']* : World.fold"` → 114.
- Identifier counts: `git grep -l`/`-c` over `'*.lean' '*.rs'` for `WriterLife` (1 file, 12), `writer_life_trusted`
  (1, 6), `CheckpointTrusted` (4, 33), `Follow.loop` (4, 5), `Honest` (5, 56), `Reach ` (9, 67), `staleBehind`
  (7, 30), `stale_behind_forever` (9, 30), `audit_ok` (5, 18), `settle_final_never_admits` (2, 6); `writerLock`,
  `appendFd`, `storeVersion|formatVersion|schemaEpoch`: 0 (the lock is `Writer.lock`, the shape is a stamp).
- Restated set: `git show origin/main:FILE | grep -c '^theorem'` for Host/Proofs/Serve 19, Refine 11, Trusted
  23, Protocol/Proofs/Thin 4, Command 99, Settle 27, Behind 11, FollowHead 9, Hosting/Proofs/Socket 29,
  Allowance 21; absorb mentions `grep -c 'absorbPage\|Absorbed\|absorb '` Command 28, Settle 14, FollowHead 7,
  Allowance 3.
- Decisions: `git show origin/main:decisions/kernel.md | grep -ci` record 173 · genesis 152 · "flag day" 37 ·
  re-genes 51; host.md record 366 · genesis 183 · "flag day" 48 · re-genes 26 · "writer lock" 3 · lock 25.
- Mini: `wc -l Kernel/GenericSimplex*.lean | tail -1` → 7282; `ls Kernel/GenericSimplex*.lean | wc -l` → 33;
  `Config` fields `parties faults timeout pumpBudget backoffCap` (Kernel/GenericSimplex.lean:25-32), `quorum :=
  parties − faults` (:35), `leader view := (view − 1) % parties` (:36).
- Harness: `git ls-tree -r --name-only origin/main client/tests launcher/tests` (17 + 10 files);
  `gates/bar.tsv` run rows (reopen-ms 63.128, 105.249, 110.074; follow-reopen-ms 106.689–113.911).
- SIZE at 231af0e (READ `SIZE.md`): Host closure 93/150, theorems 6,253, protocol operations 7/7, call kinds
  13/13, C lines 315/315, Rust 21,347.
