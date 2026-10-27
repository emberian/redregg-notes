# TOPLEVEL-SPEC — the statements that say what nanodregg is FOR (real 2026-10-24)

Author: a Fable, from the nine HOLISTIC-*.md judgments, VERDICT-20261024.md, COLLATION-20261024.md,
CHARTER.md, the decisions' entry titles, and the code at `origin/main 7655145` (past the readers'
`f9657bd` by seven landings; see §0.2). No edits to either repository; nothing elaborated. Every
Lean block below is a STATEMENT against the real definitions, written to be the first draft of a
`Spec/` module, with `-- exists` on what the tree already proves and `-- NEW` on what it does not.
Where I name a function or theorem it is one I read (path given); where a definition does not exist
I say so and name the model.

Ember's two asks, verbatim, are the two rules of this document:

> "hopefully we can figure out some *toplevel* theorem statements that we can phrase that will be
> enforcing of *wholesystem correctness*."

> "we only need the TOPLEVELMOST theorem to be nonvacuous. That nonvacuity cascades downward. We
> were enforcing it bottom-up."

So: a small number of statements about the WHOLE (§2–§9), each with the trivial system it excludes
(its FLOOR: the model that must fail it, and the deployed run that must reach it), and nothing else
in the tree owes a vacuity argument. The 6,305 theorems become lemmas of these or become internal.

---

## 0. Orientation

### 0.1 What the system is, in one paragraph (the readers' consensus, which I accept)

One writer per World orders and admits signed calls through one transition, `World.step`
(`Kernel/World.lean:1765`); members hold a follower that re-derives every logged step by the same
kernel functions before taking it (`Protocol/Command/Machine.lean` `absorbStep`, :437) and never
signs a call its own copy does not admit; objects are cells with laws authored in Lang, judged on
every act; value is conserved per denomination with floors; authority is a grant chain stored in the
state, rooted at an owner, with counted rights that only fall; a member settles its own call from
its own fold, never from the writer's word; receipts are trie paths against a head; a hosted
resident answers a Bell through its own member socket with a model it reaches through a
key-holding broker. The operator is a trusted vat (sees every byte); members consent by
re-execution; liveness is measured, never proved (CHARTER §Scope).

The observers, each of whom is owed one sentence: a MEMBER (signs calls, holds a follower); an
OBJECT'S AUTHOR (installed a package with laws); a VALUE HOLDER (a well, an account); the WRITER
(what it can and cannot do); the OPERATOR after a CRASH; TWO MEMBERS (what they can be shown);
the RESIDENT and its RINGER (the Bell); a HOLDER OF A FOREIGN HEAD (receipts between Worlds).

### 0.2 What moved since the readers read (origin/main f9657bd → 7655145)

Seven landings, five of them collation defects the statements below depend on:

| landing | collation | effect on this spec |
|---|---|---|
| f1839ed KERNEL-66 pins compared before receivers (`Submit.lean` step 4, `stale_declined_before_receive`) | A1 | §3's consent premise is now true: a receiver's verdict is a function of the call and its observation |
| 7332f9c HOSTING-47 `journal_committed`/`answered_row_committed` over `ReachOn S` with `CollidesAmong` over the frames' calls | A5 | §6's row clause is now sound in form |
| a7bccd8 CLIENT-37 the next run of the same argv IS its open attempt | A6 | §4(vi) is implemented (in Rust); still no theorem |
| 37772b9 HOSTING-48 `no_refusal_repeats_forever` over `Ticks`; `Lifetime` deleted | A13 | §6 has one chain inductive |
| e82f74d / a77f3d8 / a1575fd LANG-78/79/81 | A10, A11, A15 | §3's law clause loses three false sentences |
| 7655145 charter: a plant is a vacuity check run when cheap, not a per-theorem rule | — | §1.3 is now the charter's own position |

Still open from the collation and load-bearing here: A7 (`nd cancel` exits ok on the Host's word),
A9 (two re-derivers: `Kernel.Receive.audit` vs `Command.absorbStep`), A3 (frames bounded per field),
A17/A20 (hand-written Rust layouts; the `stdio-leg` row bundles four trusts).

### 0.3 How to read a statement here

Each of §2–§9 has: the sentence; the Lean (real names, `-- exists` / `-- NEW`); its lemmas in the
tree; TODAY (true / partly / false / unstatable, with the file that says so); the FLOOR (the trivial
system it refutes, the deployed run that inhabits it); and WHAT IT NEEDS where the system as built
cannot carry it. §10 says which are load-bearing and which are consequences; §11 says what the
system must become, as one list; §12 is the `Spec/` layout and the order of work.

---

## 1. The shape of the spec

### 1.1 Not a second machine: predicates over the deployed system

GATES proposed an abstract vat (objects, balances, grants as a delegation tree, receipts) that the
kernel refines. KERNEL replied that the transition IS the spec and what is missing is a SECURITY
theorem in seL4's integrity shape. I side with KERNEL, for a reason the tree already paid for: a
second machine beside `World.admit` is a twin (law 1), and its own non-vacuity would need the same
floor argument as the statements below, so it buys a reviewable text at the price of a reviewable
text plus a refinement. The abstraction the readers wanted already exists as the kernel's and the
protocol's own vocabulary, each a definition that other theorems consume: `Honest` (an audited log,
`Kernel/Proofs/Audit.lean`), `ObjectHistory`/`ObjectStep` (what the World does around one object,
`Kernel/Proofs/Logic/History.lean`), `Chain` (a grant chain to a principal, `Kernel/Proofs/Authority.lean`),
`Dispatched` (an invoke tree, `Kernel/Proofs/InvokeTree.lean`), `Std.Chain`/`Std.Step` (a law's
history, `Lang/Proofs/Chain.lean`), `RootedFold` (`Kernel/Proofs/RootedFold.lean`), `ReachOn`/`Moves`
(follow's World after its own frames, `Hosting/Proofs/Socket.lean`), `Ticks`/`Runs` (the resident's
process, `Hosting/Proofs/ResidentRun.lean`), `WriterLife` (`Host/Proofs/Trusted.lean`), `Kept`
(`Host/Proofs/Deployed.lean:374`). The top statements are written in that vocabulary, about the
deployed entry points: `Host.Serve.machine`, `Host.Follow.answer`, `Command.start`/`Command.step`,
`Receive.submit`/`judge`/`cancel`/`audit`, `World.step`/`fold`, `Lang.program`, `Resident.tickP`,
`Broker.decide`, `Envelope.check`, `Receipt.check`.

What must be MODELLED, because it is not in Lean, is the outside: the relay that carries follow's
continuations (Rust), the disk under the Store (POSIX), the volume under the resident (POSIX), the
provider behind the broker. Those models are `Spec/Env.lean` (§1.4): they are the IronFleet network
semantics, not a second kernel, and the project's own doctrine ("iterate inside the substrate")
allows exactly them.

### 1.2 Each claim is a predicate on a `System`, so a trivial system can be plugged in

The Host refinement already does this: `host_step_folds_tooth_unmoved/_wrong_op/_unjudged/_censor`
(`Host/Proofs/Refine.lean`) each take a machine equal to the writer's except at one arm and show the
statement refuses it. Generalised: every top claim is `Claim : System → Prop` over a record of the
components it ranges over, the top theorem is `Claim deployed`, and the floor is `¬ Claim trivialₖ`.

```lean
-- Spec/System.lean (NEW; every field names a deployed definition)
structure System (D : Type) [Ord D] [DecidableEq D] where
  X        : Receive.Ctx D                                  -- Host.Deployed.X at D := Digest
  dc       : Codec.Stream D
  B        : Protocol.Thin.Base (World D)
  admit    : World D → Step D → Except (Reject D) (World D) -- World.step X.env
  absorb   : World D → ByteArray → Except (Command.Refusal D) (Step D × World D)  -- Command.absorbStep X
  start    : Command.Self D → Command.Follow D → List ByteArray → Command.Reply   -- Command.start X
  step     : Command.Self D → Command.Follow D → ByteArray → ByteArray →
               Command.Follow D × Command.Persist D × Command.Reply             -- Command.step X dc B
  writer   : Host.Machine (World D) (Step D) Host.Frame D                        -- Host.Serve.machine X
  tick     : Resident.Where → Resident.Mem → Resident.Prog Resident.Tick         -- Resident.tickP
  broker   : Broker → Nat → ByteArray → Broker.Ask → Except Broker.Refusal (Broker × Broker.Grant) -- Broker.decide
  envelope : World D → Protocol.Envelope D → Except Protocol.ReadRefusal Unit     -- Envelope.check X

def deployed : System Digest := { X := Host.Deployed.X, admit := World.step Host.Deployed.X.env, … }
```

### 1.3 The one vacuity rule, and why it cascades

Ember: "we only need the TOPLEVELMOST theorem to be nonvacuous. That nonvacuity cascades downward."
Made precise, with the project's own memory ("Prove the floor FALSE": a floor must be satisfiable
and refutable but not provable):

* **REFUTED.** For each top claim there is a trivial system (one component replaced by the thing a
  lazy implementation would do: a follower that trusts the Host, a kernel that admits everything, a
  writer that replies before `fsync`, a Bell without its guard) and a theorem `¬ Claim trivialₖ`.
* **INHABITED.** For each top claim there is a deployed run (a journey row, the Bell rows, the
  standing reopen) that reaches the claim's non-trivial case, as a theorem `∃ run, Claim.case run`
  (by `decide`/`native_decide` over the simulation, as `Lang.Journey` and `Protocol.Rows` already run
  in process). This is what excludes "an empty World": a safety statement over a system that never
  admits anything is true and worthless.

Why it cascades: `Claim deployed` is proved from lemmas. If some lemma were vacuous (`P → P`, an
empty premise, a free disjunct), the proof of `Claim deployed` would either not go through or would
go through on a claim that `¬ Claim trivialₖ` shows is not trivial. A vacuous lemma can still be
USED, but it cannot be LOAD-BEARING: whatever meaning `Claim deployed` has, the lemmas it rests on
carry it between them. So the per-theorem plant, the statement census and the second-reader rule
(law 6's second half) become optional hygiene, which is where the charter put them this morning
(7655145). The floors are the whole vacuity obligation of the tree, and there are about a dozen.

> CORRECTION (2026-10-27, SPEC-4, CRIT-SPEC-2): false. A floor refutes ONE lazy system; it does not
> make a claim adequate. Adequacy is measured against the apex contracts, now stated as `Prop`s in
> nanodregg `Spec/Proofs/Apex.lean` (SPEC-22).

The two existing floor patterns to generalise, so nothing here is a new discipline: `Separates`
teeth (`Kernel/Proofs/Fold.lean:19-63`, with `separates_lawful_floor` proving the premise is neither
forced nor excluded) and the four `host_step_folds_tooth_*` machines.

### 1.4 The environment models (`Spec/Env.lean`, NEW)

* **Relay** — what carries follow's continuation and results. `faithful`: every `resume` carries a
  continuation follow handed out, byte for byte (today's `FollowRun`, `Hosting/Proofs/Socket.lean`,
  whose `hk : r.cont = some k` IS this assumption, and the `stdio-leg` TCB row). `arbitrary`: any
  bytes. The statements are proved under `faithful` today and must hold under `arbitrary` once the
  command's state lives in follow (§11.2).
* **Host replies** — already arbitrary: `Moves` quantifies over every `res`, and `Runs` over every
  socket reply. No model needed; the adversary is free.
* **Crash** — the Store with crashes: `MemStore.crashImage` (`Host/Sim/MemStore.lean:30-32`,
  `synced ++ prefix pending`) promoted from a test harness to THE semantics the proofs and the
  simulator share (HOST's missing cut). The resident's volume already has one: `Resident.Volume`
  (`Hosting/Proofs/ResidentVolume.lean`).
* **Provider** — a token is at least one byte (HOSTING-12's platform fact); the broker's statement
  is relative to it.

---

## 2. ONE LAWFUL HISTORY — the apex (load-bearing)

**Sentence.** Every member's World is the audited fold, from a start it consented to, of a log whose
every step is the kernel's own decision of a signed event; two members of one World hold one
history; and "the kernel's own decision" is lawful: a cell moves only under authority over it,
value is conserved, an object moves only as its laws admit (§3). The apex is `§2 ∧ §3`, because
neither half excludes the other's trivial system (§2.FLOOR).

### 2.1 A1 — the member's World is an audited fold from a start

```lean
-- Spec/Claims.lean
/-- A start of a follower (NEW): a genesis this binary built from the signed inputs, a carried
import under a sponsor-signed origin (PROTOCOL-61), or a base whose bytes hash to the pin a sponsor
the member trusts signed (thin consent: the history BEFORE the pin is trusted, PROTOCOL-14). -/
inductive Start (S : System D) : World D → Prop
  | genesis {name nonce a fs} : Start S (Receive.genesisWorld S.X name nonce a fs)       -- Kernel/Receive/Follow.lean:103
  | carried {o w} : Carry.importWorld … = .ok w → CheckpointTrusted o w → Start S w        -- Host/Proofs/Trusted.lean:76
  | pinned {pin : Thin.Pin} {bytes w} :
      S.B.digest bytes = pin.digest → S.B.world.decode bytes = .ok w → S.B.stepsOf w = pin.steps →
      Start S w                                                                           -- Protocol/Proofs/Thin.lean accept_done

/-- A1. Whatever frames a follower is fed (any results, any continuations the relay returns, any
interleaving with its other commands: `Reach`), its World is `audit`-accepted from a start. -/
def OneHistoryMember (S : System D) : Prop :=
  ∀ (me : Command.Self D) (w₀ w : World D), Start S w₀ → Reach S.X S.dc S.B me w₀ w →
    ∃ w₁ l, Start S w₁ ∧ Receive.audit S.X w₁ l = .ok w
    -- i.e. World.fold S.X.env w₁ l = .ok w ∧ Honest S.X w₁ l   (audit_ok, Kernel/Proofs/Audit.lean:275)
```

(The `∃ w₁` is the adopt edge: `Persist.adopt` replaces a World by a decoded base, which is a new
start, never a step; `Moves` already ranges over it. HOSTING-43 made adopt refuse a populated World.)

**Lemmas (exist):** `absorbStep_step`, `absorb_admits`, `absorbPage_ok`, `step_persists_admitted`
(every `Persist.steps` is a `RootedFold`), `step_keeps` (a predicate preserved by `absorbStep` is
preserved by `step`), `ReachOn.step`; `submit_ok` and `receive_derived` (a `submit`-accepted Turn is
`receive`'s), `recordedBy_of_judge`/`recordedBy_of_cancel` (a `judge`-/`cancel`-recorded refusal is
`Honest`'s refusal clause, used this way in `host_step_folds`); `accept_done` (Thin), `accept_ok`
(Invite), `genesis_trusted`, `import_trusted_pinned`.
**NEW:** `absorbStep_honest : absorbStep X w e = .ok (s, w') → Honest X w [s] ∧ World.step X.env w s = .ok w'`
(a case split on `absorbStep`'s four arms, each already proved in the Turn/refusal/cancel form for
the WRITER in `Refine.lean:160-210`), and the induction over `ReachOn`.

**TODAY: true, not composed.** Every lemma exists; the induction is not written. Nothing in the
collation falsifies it. The follower split (HOST/PROTOCOL/KERNEL) does not block THIS direction:
A1 is soundness ("what follow took is honest") and `absorbStep` calls `submit`/`judge`/`cancel`
directly. It blocks A1′.

### 2.2 A1′ — an honest writer's pages absorb (completeness; the writer–follower agreement)

```lean
/-- A1′ (HOST §4.1's theorem). What the writer stages for a batch, served as a page over its durable
records, is absorbed by the deployed follower to the writer's World. -/
def WriterFollowerAgree (S : System D) : Prop :=
  ∀ (w : World D) (qs : List (Host.Request Host.Frame)), Kept w →
    let (w', out) := S.writer.admitBatch w qs
    let P := Host.Page.build … (out.staged …)               -- Host/Page.lean, over the durable records
    Command.absorbPage S.X w P.events P.steps P.chain _ = .ok (w', _, _)
```

**Lemmas (exist):** `host_run_audits` (`Host/Proofs/Refine.lean:246`), but over `Kernel.Receive.audit`;
`absorbStep_cancelEvent`; `eq_callBytes_of_decodeCall` (Codec); `Page` coherence (`Host/Proofs/Coherence.lean`).
**TODAY: false as a theorem about the deployed follower** (collation A9): `host_run_audits` is about
a re-deriver nobody runs; the deployed `absorbStep` differs from `auditStep` in the refusal compare
and in `staleRecorded`. The evidence for A1′ today is the rows' end-to-end follow (a sample).
**NEEDS:** one re-deriver (§11.2): `absorbStep X w e := auditStep X w ∘ (decode e)`, or `audit`
deleted and `host_run_audits` restated over `absorbStep`. Weeks (HOST's price); FIX-HOST is on it.
A1′ is what makes A1's floor INHABITED non-trivially (a page with a Turn is absorbed), and it is
what §7 (the writer cannot be falsely accused) rests on.

### 2.3 A2 — two members hold one history

```lean
/-- A2. Two followers of one World that compare heads hold one World, up to a collision among the
two folds' link inputs. Verbatim `fold_reaches_host` (Kernel/Proofs/Fold.lean:456); what is NEW is
the deployed ACT that produces `hs ∧ hc` between two MEMBERS. -/
def OneHistoryPair (S : System D) : Prop :=
  ∀ {n} (hE : S.X.env.Lawful n) {g wf wg : World D} {lf lg : List (Step D)},
    Start S g → World.fold S.X.env g lf = .ok wf → World.fold S.X.env g lg = .ok wg →
    wf.steps = wg.steps → wf.chain = wg.chain →
    wf = wg ∨ CollidesAmong S.X.env.hash (foldPres S.X.env g lf ++ foldPres S.X.env g lg)

/-- A2′ (the fork-consistency half: SUNDR 2004). A member behind another that catches up TO THE
OTHER'S HEAD either reaches that World or refuses `chainMismatch` by name; so a writer that forks
two members can never show either a page that joins the forks. NEW act: `nd sync --to STEPS:CHAIN`
= `absorbPage` with the stated `(steps, chain)` taken from the OTHER member, not from the writer. -/
def ForkConsistent (S : System D) : Prop :=
  ∀ me wf wg lg S', Start S g → ReachOn S.X S.dc S.B me g S' wf → Receive.audit S.X g lg = .ok wg →
    wf.steps ≤ wg.steps →
    ∀ evs, Command.absorbPage S.X wf evs wg.steps (S.X.env.bytes wg.chain) _ = .ok (wf', _, _) →
      wf' = wg ∨ CollidesAmong S.X.env.hash (…)
```

**Lemmas (exist):** `fold_reaches_host`, `chain_binds`, `headLink_inj`, `absorbPage_ok` (the
absorbed fold reaches the STATED `(steps, chain)` or refuses), `chainMismatch` in `Command.Refusal`.
**TODAY: A2 true (it is a kernel theorem); A2′ true of the function, UNSTATABLE of the system**:
nothing deployed ever puts another member's `(steps, chain)` into `absorbPage`. Members never
compare heads (HOST §1.3, PROTOCOL §2.3, VERDICT §6). `host check --anchor STEPS:CHAIN`
(`Host/Check.lean`) is this exact check, available to the OPERATOR only. The cross-World
`Std.head` object compares heads only at equal step counts and only for posters' claims.
**NEEDS (§11.1):** (a) the member verb `nd sync --to STEPS:CHAIN` (days: it is `absorbPage` with
two arguments taken from argv); (b) a channel for heads: the cheapest honest one is a
`Std.head`-shaped object IN THE SAME WORLD to which members post their own `(steps, chain)` by signed
calls (gossip through the writer: a forking writer must then keep each fork consistent with every
post it serves, which is SUNDR's fork consistency exactly; detection still needs one out-of-band
comparison, which (a) performs); (c) writer-SIGNED heads `(origin, steps, height, roots, chain)`,
which turn a detected fork into a PROOF (two signed heads at one step count) and which §9 needs for
the same reason. (a)+(b) is a week; (c) is weeks and one re-genesis (the writer key enters genesis).

### 2.FLOOR

* **Refuted by** `trustingAbsorb`: `absorb := fun w e => (decode e) >>= World.step` (no re-derive).
  On a log holding a Turn whose event `receive` refuses (a write by a non-owner: the row plant
  "receiver skips the grant check on write" is its event), `Reach` moves follow's World to a World
  that `audit` refuses `eventMismatch` at that index: `¬ OneHistoryMember trusting`. This floor is
  REAL only because `receive` refuses something — which is §3's claim. That is why the apex is the
  conjunction: a kernel that admits everything makes `Honest` trivially true, so
  `OneHistoryMember admitEverything` HOLDS; it is `Integrity admitEverything` (§3.FLOOR) that fails.
* **Refuted by** `trustingAdopt`: `Start.pinned` without `S.B.digest bytes = pin.digest`: a served
  base with one forged byte becomes a start. (`Protocol/Rows` `untrustedAdopt` is this row.)
* **A2 refuted by** an `Env` whose link ignores its inputs (`stepLink := fun c _ _ => c`): two
  different logs reach one chain and the collision disjunct is empty of them (`headLink_inj`'s tooth).
* **Inhabited by** any journey row in which follow absorbs a page holding at least one Turn
  (`∃ S w, ReachOn deployed … S genesis w ∧ 0 < w.steps`): J0–J8 as nanodregg rows (`Protocol/Rows`).

---

## 3. INTEGRITY — what "lawful" means (load-bearing; the apex's other half)

Three statements over an audited log, each a promise to a different observer. They hold of ANY
`audit`-accepted log, so by A1 of every member's World.

### 3.1 B1 — authority confinement (seL4 integrity, Sewell et al. 2011, in the kernel's terms)

**Sentence (what a cell's owner is promised).** Along an audited log, a cell changes only by a Turn
derived from a signed call whose signer exercised authority over that cell: an object by its owner's
`write`/`law`, directly or through a live grant chain rooted at the owner carrying the right, or by
an `invoke` its laws judged (itself authorized by a chain carrying `invoke m`, `Derive.lean:188`
`ownerAuthority … (.invoke method) via`); a grant only by its retirement or by a spend of its own
counted right; a value account only by a `transfer`/`credit` the owner or the well's issuer authorized;
a member only by its own `rotate` to the key it precommitted; a package never (ROM).

```lean
/-- What the signed call `c` was entitled to do to cell `id` at the World it was derived against
(NEW, one arm per kind; each arm is an existing theorem's conclusion). -/
inductive Authorized (X : Ctx D) (w : World D) (c : Call D) (id : D) (cell : Cell) : Prop
  | object_write {edits via owner} : cell.kind = kindObject →
      c.unsigned.body = .write id edits via → slotDigest X id cell slotOwner = .ok owner →
      (via = none ∧ c.unsigned.member = owner ∨
       ∃ g, via = some g ∧ Chain X (pinned X.env w c.unsigned.pins) id .mutate true g c.unsigned.member owner) →
      Authorized X w c id cell
  | object_law   … (the same with `.law` and `.mutate`)
  | object_invoke {n wk a method args budget via} : cell.kind = kindObject →
      Dispatched X w c n wk a (.invoke id method args budget via) → Authorized X w c id cell   -- its own chain is inside invokeRun
  | grant {e} : cell.kind = kindGrant → (e.2 = .retire ∨ LedgerSpend id cell e.2) → Authorized X w c id cell
  | account … : transfer_authorized's conclusion (Kernel/Proofs/Ledger.lean:379) or credit's
  | member : cell.kind = kindMember → c.unsigned.member = id → (∃ k n, c.unsigned.body = .rotate k n) → Authorized X w c id cell

def Integrity.authority (S : System D) : Prop :=
  ∀ {w w' l} (hcan : CellsCanon S.X.env w), Receive.audit S.X w l = .ok w' →
    ∀ id {cell cell'}, w.live S.X.env id = some cell → w'.live S.X.env id = some cell' → cell' ≠ cell →
      ∃ v v' t c, (v, Step.turn t, v') ∈ foldSteps l ∧                                   -- NEW: the step triples of a fold
        Receive.receive S.X v c = .ok t ∧ World.admit S.X.env v t = .ok v' ∧ Authorized S.X v c id cell
```

**Lemmas (exist):** `object_history_of_audit` (`Logic/History.lean:235`: every change of an object
live at the start is a judged `ObjectStep`), `object_turn_cases` (`InvokeTree.lean:916`: no receiver
but write, law and invoke writes an object), `effect_at_object`/`effect_at_grant` (`InvokeTree.lean:825/873`),
`transfer_authorized`, the `write`/`law` authority theorems of `Kernel/Proofs/Authority.lean`
(`walk_chain`), `receiveWith_key` (every call but `rotate` is signed by the current key; `rotate` by
the precommitted one), `fold_rom` (`Frame.lean:82`), `audit_package_fixed`, `Honest` (the step IS
`receive`'s, so `Derived.signed` holds: the call verifies under the member's key).
**NEW:** the `Authorized` inductive and the composition over every cell kind. Objects born inside
the log need the split at birth `History.lean` already describes. Weeks; every lemma exists.
**TODAY: true, not composed.** KERNEL-66 (f1839ed) removed the one thing that made the consent
narrative around it false (a receiver judging the World as it is now, not as observed).

### 3.2 B2 — value (what a holder of value is promised)

```lean
def Integrity.value (S : System D) : Prop :=
  ∀ {w w' l}, Kept w → Receive.audit S.X w l = .ok w' → ∀ d,
    (d ∉ (Step.turns l).flatMap createdIds |>.map S.X.env.bytes) →
      w'.valueSum d = w.valueSum d ∧ w'.floorSum d = w.floorSum d        -- admit_value, admit_floors (Kernel/Proofs/Value.lean:402/410)
def Integrity.grantCap  (S : System D) : Prop := grant_moves_le_cap's statement     -- Ledger/Proofs/GrantCap.lean:256, exists
def Integrity.escrow    (S : System D) : Prop := escrow_invokes_one_payout's statement -- Ledger/Proofs/EscrowInvokes.lean:70, exists
```

**TODAY: true.** `admit_value` holds of EVERY admitted Turn, forged logs included (Value.lean's
header), which is stronger than B1 needs and is why conservation does not depend on authority.
`grant_moves_le_cap` carries `LedgerContiguous` (KERNEL-61), discharged by `Kept`'s canon at the
deployed `Env`; its tooth `grant_cap_needs_contiguous` is a floor theorem already. What is NOT
promised and the names suggest: that the escrow pays what a party was owed. `escrow_invokes_one_payout`
says AT MOST ONE payout; the joint judge ignoring the legs (collation A4, open) is a defect of the
escrow's OWN spec, which is the tier below (§10.3), not of B2.

### 3.3 B3 — law (what an object's author is promised)

**Sentence.** An installed package never changes under its object (ROM; `audit_package_fixed`); every
state the object's cell ever holds along an audited log was reached by a step every law in force
admitted on the view the signer pinned, and a replacement of its laws was admitted by the old laws
and the incoming ones over the unchanged state (KERNEL-57, `law_judged`); each judged step's new
state, calls and edits are the reference meaning of the method (`BigStep`) on that view, independent
of fuel; and every edit of a relation under the object passed the relation's guard (the receiver is
the monitor).

```lean
def Integrity.law (S : System D) {rc} (hprog : S.X.program = Lang.program S.X.env.bytes S.X.digestOf rc) : Prop :=
  ∀ {obj w w' l}, CellsCanon S.X.env w → Receive.audit S.X w l = .ok w' →
    ∀ {cell}, w.live S.X.env obj = some cell → cell.kind = kindObject →
      ∃ tr, ObjectHistory S.X obj w w' tr ∧                                           -- object_history_of_audit
        (∃ cell', w'.live S.X.env obj = some cell' ∧ packageOf S.X obj cell' = packageOf S.X obj cell) ∧   -- audit_package_fixed
        (∀ e ∈ tr, Judged e) ∧                                                         -- object_step_some: laws in force passed old → new
        (∀ law t, InForce law t tr → Lang.NoRef t →                                     -- object_history_chain (History.lean:357)
            Std.Chain (Std.Step [] t) (stateAt w) (tr.map projectStep)) ∧
        (∀ e ∈ tr, RunMeans e)                                                         -- object_history_runs + run_bigStep + runMeasured_means + run_agree
```

**Lemmas (exist):** all named; plus `activity_monitor_safe` (`StdActivityMonitor.lean:367`) for the
relation-guard clause, instantiated for the Bell as `bell_monitored` (`Lang/Proofs/Bell.lean:61`).
**TODAY: true with two honest restrictions.** (i) The chain lift is for `NoRef` laws only
(`Lang/Proofs/Receiver.lean:129`); contextual (hole-bearing) laws have a separate relational
meaning (`Lang/Proofs/LawMeaning.lean`) and no chain lift. The Bell is `NoRef` (its root has no
imports and no holes). Either the lift is extended or the claim says "NoRef laws", and contextual
packages are outside the author's promise until then. (ii) The promise is "your laws were consulted,
on the pinned view, and admitted every step": it is NOT "the stdlib law your package used means
what its name says". That second promise is per generator (`Std.offer`'s compliance,
`Std.offerEscrow`'s legs, `Std.activity`'s machine) and belongs to LANGPROOFS' `MethodSpec` tier
(§10.3), where collation A4 lives.

### 3.FLOOR

* **Refuted by** `openKernel`: the receivers with `ownerAuthority := fun _ _ actor _ _ _ _ => .ok actor`
  (the row plant "receiver skips the grant check on write"). A non-owner's `write` derives and
  admits; `Integrity.authority` demands `Authorized`, whose `object_write` arm needs a `Chain` to the
  owner; none exists: `¬ Integrity.authority openKernel`.
* **Refuted by** `mintingKernel`: `admitImpl` with `checkValue` removed. A Turn whose posts raise a
  denomination's sum admits: `¬ Integrity.value minting`. (`admit_value`'s own plant.)
* **Refuted by** `unjudgedKernel`: `Lang.program` with `judge := fun … => .ok ()`. A write a law
  refuses is admitted; the `Judged` clause of `Integrity.law` fails.
* **Refuted by** `freeKernel`: a kernel in which `admit` does not check the pins against the
  World (`touchCheck` with the pin compare dropped). Then "on the view the signer pinned" is false:
  the admitted Turn's touches need not be the signer's observation (`Derived.pinned` is of the call,
  but admission would accept a Turn over moved cells). This is the floor of KERNEL-54/66 together.
* **Inhabited by** the Bell journey (an `invoke` moves an object's state through a law), the `pay`
  and `well` rows (a transfer moves value under a `transfer (cap)` grant; `grant_moves_le_cap`'s
  tooth row moves 10 under a cap of 10), LB13 (a layer cannot override a law), the escrow `bounty`
  row (one payout).

---

## 4. CONSENT AND SETTLEMENT — what a member is promised of its own follower (load-bearing)

PROTOCOL's four clauses, with two more the readers named (RUST's at-most-once; the signing domains),
stated over a trace against the environment of §1.4.

```lean
/-- One command's run (NEW, from `FollowRun` in Hosting/Proofs/Socket.lean with the relay a parameter):
from `start`, each `step` fed the result the environment chose and the continuation the RELAY chose
(`faithful`: the one the previous reply carried; `arbitrary`: any bytes), with any other frames of
the member between (`Reach`), ending `fin = (exit, stdout, stderr)`. -/
inductive Run (S : System D) (relay : Relay) (me : Command.Self D) :
    Command.Follow D → Command.Reply → Command.Follow D → UInt8 × ByteArray × ByteArray → Prop
  | done … : Run S relay me f (.done e o r) f (e, o, r)
  | step  … (hk : relay.allows r k) (hg : Reach S.X S.dc S.B me f.world g.world)
            (hs : S.step me g k res = (f', p, r')) (rest : Run S relay me f' r' fe fin) : Run S relay me f r fe fin
```

**C(i) — signing.** Every message follow offers custody for a CALL signature is `callMessage u` for a
`u` planned from the member's argv on a World of follow's own fold that admits the Turn it derives;
and the submitted bytes are that signed call, re-planned and byte-compared at submit (`planMoved`).

```lean
def Consent.signsOnlyAdmitted (S : System D) (relay : Relay) : Prop :=
  ∀ me f argv fe fin, Run S relay me f (S.start me f argv) fe fin →
    ∀ msg k, (.sign msg k) ∈ asked (Run …) →                                           -- NEW: the replies a run handed out
      ∃ u sg rs b w, Reach S.X S.dc S.B me f.world w ∧ msg = S.X.callMessage u ∧ u.member = me.member ∧
        body S.X me w sg argv = .ok b ∧ signedReads S.X w argv = .ok rs ∧ plan S.X me w sg.key rs b = .ok u ∧
        ∃ t w', deriveTurn S.X (pinned S.X.env w u.pins) (rowView S.X.env w u) ⟨u, _⟩ = .ok t ∧ World.admit S.X.env w t = .ok w'
```
Lemmas (exist): `plan_admits` (`Protocol/Proofs/Command.lean:171`), `step_submit_planned` (:399),
`planMoved`'s arm, the `signNext`/`precommit` arms (CLIENT-13), `Protocol/Proofs/Domains.lean`
(`call_envelope_disjoint`, `call_possession_disjoint`, …: a call signature is never an envelope,
invitation, possession or cancel). TODAY: **true under `faithful`**, lemma by lemma; the run-level
composition is new. **False under `arbitrary`**: `State.ofBytes` decodes any bytes, so a fabricated
`k` carries an argv the member never issued and follow plans from it (PROTOCOL E-1, collation A3's
cousin). What it still guarantees under `arbitrary` is the second half: whatever is signed, follow's
own World admitted it (`plan_admits`), so the relay can make the member sign only calls the member's
own copy accepts — which is the ocap "confused deputy is the member's own decider" point RUST §1.3
makes. NEEDS §11.2.

**C(ii) — ok means committed.** Every `done ok` of a writing command means the member's OWN World
journals the call the argv planned (`submit`-class commands), or holds the cancel record of the call
named (`cancel`).

```lean
def Consent.okIsCommitted (S : System D) (relay : Relay) : Prop :=
  ∀ me f argv fe o e, Run S relay me f (S.start me f argv) fe (CommandExit.ok.code.toUInt8, o, e) →
    Verb.writes argv →
      (∃ cb c hh td, plannedFrom argv cb ∧ S.X.decodeCall cb = some c ∧
          fe.world.journalAt S.X.env (txIdOf S.X c) = some (hh, td)) ∨
      (∃ c, Verb.isCancel argv c ∧ fe.world.refusalAt S.X.env (.tx (txIdOf S.X c)) = some (.refused _ cancelledCode _))
```
Lemmas (exist): `step_settled_ok` (`Command.lean:295`: `done ok` at phase 4 ⇒ `settleOf X me f.world c = .committed`
for the `cb` the continuation carries, PROTOCOL-64), `step_submit_planned` (that `cb` is the planned
call at phase 3), `settle_committed`. TODAY: **true for submit-class under `faithful`** (two lemmas
and the continuation chaining); **FALSE for `cancel`** (collation A7, open): `cancelAnswer`
(`Machine.lean:1136`) exits `ok` on the Host's `refused cancelled` without settling on follow's
World. This arm is the deployed instance of the trivial model in 4.FLOOR. NEEDS: `cancel` settles
like step 4 (a day; PROTOCOL's cheaper alternative), then §11.2 for `arbitrary`.

**C(iii) — final is final.** Every `refused`/`expired` settlement follow prints is final against
every extension of the log.

```lean
def Consent.finalIsFinal (S : System D) : Prop :=
  ∀ me w c l w', Kept w →
    (settleOf S.X me w c = .expired ∨ ∃ code, settleOf S.X me w c = .refused code) →
    World.fold S.X.env w l = .ok w' → ∀ out, Receive.submit S.X w' c ≠ .ok out
    -- the `refused staleCode` case additionally needs `staleBehind_final`'s premises (the call is the member's own,
    -- planned on a World of follow's fold) and ends `∨ CollidesAmong (behindPres …)`
```
Lemmas (exist): `settle_final_never_admits` (`Protocol/Proofs/Settle.lean:201`), `staleBehind_final`
(`Behind.lean:249`), `submit_refused_never`, `absent_final`. TODAY: **true**. This is the clause the
readers rate highest (client-side OCC finality) and it needs nothing.

**C(iv) — the member's World.** A1 (§2.1), shared.

**C(v) — at most once per intent.** For each argv the member issues, across any interleaving of
crashes, timeouts and re-runs of nd, at most one call commits.

TODAY: **implemented, no theorem.** CLIENT-37 (a7bccd8) makes the next run of the same argv reload
its open attempt; the attempt loop, fuel, payload and files are Rust (`client/src/attempt.rs`,
`run.rs`), so this is a test of Rust against Rust's reading of Lean (RUST §3.2(3)). It becomes
a Lean theorem (`∀ runs of argv, committed ≤ 1`) when the attempt is follow's state (§11.3).

**C(vi) — the retry policy is the table.** `Attempt.next` is total and emitted; nd keeps no second
copy. Exists (`Protocol/Proofs/Attempt.lean`, `next_final`: only follow's word is final).

### 4.FLOOR

* **Refuted by** `hostWord`: `step` whose phase-4 arm reads `result[0] = committed` as `done ok`
  (the pre-PROTOCOL-64 machine; today's `cancelAnswer` is this model live). With a Host that answers
  `ok` for an unsubmitted call, the run ends `ok` and `fe.world.journalAt … = none`:
  `¬ Consent.okIsCommitted hostWord`.
* **Refuted by** `relaySigner`: a `step` whose sign arm offers `result` itself to custody
  (`.sign result k`). `Consent.signsOnlyAdmitted` fails on any result that is not a planned
  `callMessage`.
* **Refuted by** `neverFinal`: `settleOf := fun … => .open`. `finalIsFinal` is vacuously true of it
  — which is why C(iii)'s INHABITED half is required: a run that ends `refused` or `expired`.
* **Inhabited by** a journey row ending `done ok` on a `write`, one ending `refused NAME` (recorded),
  one ending `expired`, and the `stale` row THE BAR re-runs (PERF-13).

---

## 5. DURABILITY — what survives a crash (load-bearing)

**Sentence (durable linearizability, Izraelevitz–Mendes–Scott 2016, in Host's terms).** Every reply
the writer acknowledges as decided (`ok`, or `refused` with a record) names a step in the durable
log; after any crash the writer reopens to the audited fold of exactly the records on disk, which
hold every acknowledged step and nothing the writer did not stage; a follower's Store holds only
steps its own `World.step` took and reopens the same way; the resident's kept answer is intact or
absent, never torn.

```lean
-- Spec/Env.lean: the Store with crashes (NEW: MemStore.crashImage promoted to THE semantics)
structure Crash where synced pending : ByteArray  -- an image keeps `synced ++ prefix pending`

/-- D1. The writer. -/
def Durable.writer (S : System D) : Prop :=
  ∀ keys file file' o (life : WriterLife keys file file') (img : Crash) (acks : List Ack),
    Image life img → AcknowledgedIn life acks →                                   -- NEW: the loop as an interpreter over Store/Port
    ∃ b l, Base.read keys c world file' = .ok (b, _, _) ∧ CheckpointTrusted o b.world ∧
      Receive.audit S.X b.world l = .ok (reopened img) ∧                           -- audited, not only folded
      ∀ a ∈ acks, a.decided → a.step ∈ l
/-- D2. The follower. -/
def Durable.follower (S : System D) : Prop :=
  ∀ me fs f fs' p st pl, Host.Follow.answer S.X S.dc S.B me fs f = (fs', p, st, pl) →
    (p = .steps ts → World.RootedFold S.X.env fs.world ts fs'.world ∧ appended-before-sent ts) ∧
    (p = .adopt w' → Start S w' ∧ sealed-before-sent w')
/-- D3. The resident's volume. -/
def Durable.resident : Prop := keep_atomic ∧ keep_durable ∧ resume_durable          -- Hosting/Proofs/ResidentVolume.lean, exist
```

**Lemmas (exist):** `open_sound` (`Host/Proofs/Open.lean:57`: for ANY bytes, the opened World is the
fold of records whose encoding is literally the prefix before `validLen`), `host_reopen_folds`
(`Refine.lean:510`), `writer_life_trusted`/`link_trusted` (`Trusted.lean`), `host_run_kept`
(`Refine.lean:451`), `machine_commits`, `step_submit`, `openWith_backup`, `sealed_opens`,
`step_persists_admitted`, `accept_done`, the `ResidentVolume` family.
**TODAY: the reopen half true; the reply half read off; `Honest` not carried across the crash.**
Precisely (Refine.lean's own header): the crash edge is a FOLD, not an audited one; no theorem ties
the segment's bytes to what `admitBatch` staged (the write side: a record appended is
`Record.codec` of the staged batch); the loop's append → `fsync` → reply order (`Host/Loop.lean:4-15`)
and "the loop holds only open/`admitBatch` Worlds" are HOST-69/71's read-off premises. `Durable.follower`'s
"appended before sent" is likewise the loop's text (`Follow.lean:98-118`), not a theorem.
**NEEDS (§11.4):** `serve` as an interpreter over the `Store`/`Port` effect records it already takes
(`Loop.lean:37-55, 105-125`), `Crash` as the one semantics (the simulator's `MemStore` already
implements it), and the three clauses proved over it. A month for the interpreter and the write
side; a quarter for the reply clause with the async seal Task (HOST's price). A full POSIX model is
the right not-yet: HOST-71's named OS assumptions stay as `Spec/Env` premises.

### 5.FLOOR

* **Refuted by** `eagerWriter`: `serve` with `port.send` before `fsync`. There is a crash image
  (`pending` cut before the record) in which an acknowledged `ok` has no step: `¬ Durable.writer eager`.
* **Refuted by** `amnesiacOpen`: `openLog` that returns `w₀` whatever the segment holds. `open_sound`'s
  `o.records = rs.length` fails on a one-record segment.
* **Refuted by** `inPlaceKeep`: the resident writing the kept name in place (`in_place_loses_both`
  is this tooth, already in the tree).
* **Inhabited by** the standing fuel-restart reopen (`Loop.lean:370-397`: every 4096 batches the
  writer reopens itself and refuses `reopenDiverged` if the result differs — the floor run as a
  standing check, which HOST called the one idea others should copy) and the crash-restart plant
  row; the follower's crash row; `resident_bell`'s restart row.

---

## 6. THE BELL — the one running multi-party instance (load-bearing instance)

HOSTING's five lines, which I adopt as the composite, with the Lang half (the ringer's promise)
made explicit.

**Sentence.** For every ring, from the moment it is pending: it is answered at most once, by the
resident, with the ring's own text echoed (the `rings` guard, LANG-59); its answer text is decided by
at most one charged ask, or is `(unanswered restart)`; the answered row's text is the kept text; no
ask is charged past the allowance's cap, and no window is refunded across a restart; across any
schedule of ticks, socket replies, crashes and restarts; and no refusal is retried forever.

```lean
-- Spec/RingLife.lean (NEW): one ring's life, the abstract process the resident refines
inductive RingState | pending | asked (intent : ByteArray) | kept (text : ByteArray) | answered (text : ByteArray) | retired
inductive RingLife : RingState → RingState → Prop   -- pending→asked (one charge) →kept →answered; pending→retired; crash edges resume from the volume

def Bell (S : System D) : Prop :=
  ∀ w m (life : Life S w m)                                -- NEW: Ticks interleaved with Crash edges on Resident.Volume
    (hs : StdioLeg S.X S.dc S.B me w.conf (events life))     -- the relay premise (Hosting/Proofs/Socket.lean:450); shrinks under §11.2
    (k : RingKey),
    charged life k ≤ 1 ∧                                                                     -- (2)
    (∀ t wf, Reach … wf → answeredRow wf k = some t → t = keptText life k ∨ t = intentText) ∧ -- (3)
    (∀ obj wf tr, ObjectHistory S.X obj … tr → answersFor k tr ≤ 1) ∧                        -- (1) the ringer's promise, from bell_monitored
    (∀ ask ∈ asks life, Capped (brokerAfter ask) ∧ Fresh (brokerAfter ask)) ∧                -- (4)
    (∀ chain ⊆ life, allUnsettled chain → chain.length ≤ retriesMax)                          -- (5)
```

**Lemmas (exist):** per tick `tick_counts` (`ResidentRun.lean:410`: at most one ask, right after
the intent is kept; at most one invoke, of the kept answer) and the nine `order_refuses_*` teeth;
per process `bell_resident_conforms` (`BellConform.lean:356`: two asks for one ring have a `Frees`
between) and `no_refusal_repeats_forever` (:989); per crash `keep_atomic`, `resume_durable`,
`seed_after_keep`; the row `delivered_answer_committed_strong` (`SocketStrong.lean:640`: an `ok`
invoke is the resident's datum committed on the member's World) and `answered_row_committed`
(`BellRow.lean:214`, now over `ReachOn S`), `answered_row_is_kept_answer` (:149); the guard
`bell_monitored` (`Lang/Proofs/Bell.lean:61`, the Bell instance of `activity_monitor_safe`: every
admitted edit of `rings` is a `WaitingStep`, so an answered row never changes again) plus
`Std.chain_count` for "at most one answer per key"; the broker `capped_decide` (`Broker.lean:207`),
`start_window_refused` (:267), `capped_follow`; `answer_commits` (`BellCommit.lean:96`).
**TODAY: every slice true; the composite unstated** (HOSTING §2, E2: "the absence of the composite
is not a missing theorem, it is the missing verification"). The seams where a defect could sit —
a crash between keep and ask, a lost reply, the World that holds the row, the journal's provenance
— are exactly the "Not claimed" lists of HOSTING-42..46; two of them closed this week (A5 →
`ReachOn`, A13 → `retriesMax`), one (A14: undecodable stdout reads as "nothing pending") is open
and is a counter-example to (2) under a lying relay.
**NEEDS (§11.5):** `RingLife` and `Life` (Ticks with crash edges resuming through `resumeOps`), the
resident as its refinement, and the one theorem. One to two months (HOSTING's price). Plus: the
`StdioLeg` premise shrinks to "bytes moved" once follow holds the command state (§11.2), which is
what makes (2)–(3) statable against an `arbitrary` relay.

### 6.FLOOR

* **Refuted by** `askFirst`: `tickP` with the ask before the keep (`order_refuses_ask_before_keep`
  is this tooth): a crash between the ask and the keep, then a restart, asks again: `charged k = 2`.
* **Refuted by** `unguardedBell`: `world/resident/Bell.ob` without `(guards queued rung)`: two
  `answer` invokes for one key both admit: the ringer's clause fails.
* **Refuted by** `refundingBroker`: `Broker.follow` keeping a meter's `spent` across a changed
  allowance: `start_window_refused` fails.
* **Refuted by** `blindResident`: `Ring.readAll` with non-UTF-8 stdout read as `[]` — this is the
  DEPLOYED code today (collation A14): the resident forgets its kept answer and asks again. The
  floor theorem would be red against `deployed` until A14 lands; that is the floor doing its job.
* **Inhabited by** `resident_bell` Q1–Q7 (a ring is answered; a retired ring is skipped; a restart
  answers with the kept text).

---

## 7. WHAT THE WRITER CAN AND CANNOT DO (consequence of §2–§4)

Not a new theorem: a reading of the apex from the adversary's chair, one clause per lemma, so the
operator's power is written down once.

The writer CAN: choose the order of calls within a batch and across batches; delay or withhold
any call, page or reply (liveness is measured, never proved: CHARTER); decline (not record) a valid
call forever, which a member sees as `open` (`declined_open`); refuse within the budget, charged to
the member (`KERNEL-44`); read every byte (CHARTER §Scope 2: the vat is trusted for confidentiality).

The writer CANNOT, without being refused by name by every follower that sees the page:
* (CORRECTION 10-27, SPEC-19: the list below is about the HONEST HANDLER's code; G2 constrains only the
  `defer` arm — a `reply` or `lookup` leak satisfies it — and the charter trusts the operator for
  confidentiality; nothing here prohibits an adversarial operator releasing bytes it holds.)
* invent a Turn or alter an admitted one (`eventMismatch` at the position: A1; `chain_binds`);
* record a refusal `judge` would not record, or censor a call it would admit under a refusal
  (`host_step_folds_tooth_censor`; the audit's `forgedName`);
* record a stale (`staleRecorded`); re-judge a journaled call (`replayed`);
* make a member see `ok` for a call its own World does not journal (C(ii); after PROTOCOL-64,
  `T0`: no Rust path yields `ok`);
* make a member sign anything its own World does not admit (C(i), `plan_admits`);
* turn a committed call into `absent` or `refused` in a receipt, or move its entry (`check_committed`,
  `check_refused_sound`, `check_absent_unrefused`: `Protocol/Proofs/Receipt.lean`);
* mint, or move value past a grant's cap (B2: `admit_value` holds of forged logs too);
* serve the log to a holder of no live follow grant (§8);
* JOIN two forks it has shown two members — ONLY once A2′ is an act (§2.3). Today it can fork
  undetected; that is the one adversary capability the design's own threat model (integrity not
  trusted) leaves open, and §11.1 closes it.

What the writer CANNOT be accused of falsely: an honest page absorbs (A1′) — today evidenced by
rows, not a theorem about `absorbStep` (§2.2).

---

## 8. WHAT TWO MEMBERS CAN AND CANNOT BE SHOWN (half consequence, half primitive)

**G1 — can be shown the same history:** A2/A2′ (§2.3).

**G2 — a non-member is shown nothing of the log.** The writer answers a `log`/`read` frame with a
page only past `Envelope.check` (`Protocol/Envelope.lean:94`): the envelope names this World, its
window is at most `windowMax`, the member is live and the key its current one, the signature
verifies, the follow grant's chain is live to a founder's root (`mayFollow`, `Kernel/Receive/Follow.lean`:
revoking any link revokes everything through it), and the height is inside the window. The one
thing an unauthenticated party learns is nothing; the one thing an authenticated-but-expired member
learns is the writer's height (PROTOCOL-19).

> CORRECTION (2026-10-27, SPEC-4, CRIT-SPEC-2): "learns nothing" is not proved. G2 (`top_shown`) is a
> handler lemma about the `defer` arm only (SPEC-19); a `reply` or a `lookup` (no envelope guards it)
> is not covered, and the operator who holds the bytes is trusted. No confidentiality theorem exists.

```lean
def Shown.onlyFollowers (S : System D) : Prop :=
  ∀ w f d, Host.Serve.handle S.X w f = .defer d →
    ∃ e, Protocol.Envelope.ofBytes S.X f.payload = some e ∧ S.envelope w e = .ok () ∧
      mayFollow S.X w e.member e.grant = true ∧ currentKey S.X.env w e.member = some e.key
```
Lemmas (exist): the envelope theorems of `Protocol/Proofs/Envelope.lean` (the `check_ok` family;
PROTOCOL-27's one-window replay bound), `handle`'s two `defer` arms (`Host/Serve.lean`, read:
both sit under `Envelope.check … = .ok ()`). TODAY: **true**, a one-page proof.

**G3 — inside a World, nothing is hidden between members.** Every follower pages the whole log; a
member's calls, refusals, balances and rows are visible to every other member and to the operator.
Membership (holding a live follow grant) is the confidentiality boundary, by charter. This is a
statement the spec must MAKE, not prove: a reader of §8 must not infer a privacy property the design
excludes.

### 8.FLOOR
* **Refuted by** `openHost`: `handle` deferring `log` without `Envelope.check`.
* **Inhabited by** the row where a stranger's envelope is refused `noFollowGrant`, and the
  revocation row (a retired link refuses the next page).

---

## 9. RECEIPTS BETWEEN WORLDS (consequence, with one undischarged premise)

```lean
def Foreign (S : System D) : Prop := foreign_receipt_sound's statement   -- Protocol/Proofs/Foreign.lean:74, exists
```
**Sentence.** A committed receipt checked against a head this World holds means the call was admitted
in the fold that head is the head of — PROVIDED the held head IS the head of a fold of A from A's
genesis (`hr`), or the hash collides among the receipt's path inputs.

**CORRECTION (real 2026-10-27, SPEC-3 from CRIT-SPEC; decisions/spec.md SPEC-19).** The discharge proposed
below is WRONG: a writer can sign exactly one fabricated head per step count, satisfying "at most one
head per step", and that head need belong to no lawful fold; a signature is attributable endorsement,
not the endorsed proposition. The foreign-head contract must choose its validity source explicitly —
re-execution, an authenticated checkpoint trusted for validity, or an authority ASSUMED to certify only
valid extensions — and the authority must be authenticated independently of the object checked (never
read from the head object; `Head.certifiesWorld`'s reliance on prior trust in the pinned bytes is the
right shape). Today `Protocol.Foreign.check` reads roots from the head object and calls no certificate
verifier. Signed heads give ACCOUNTABILITY (checkable equivocation evidence), not validity.

**TODAY: true, and `hr` is undischargeable** (PROTOCOL E-3): heads are posted by grantees, unsigned by
A's writer, with no consistency proof between two posts; `Std.head`'s law can only order posts and
freeze on a disagreement at one step count. **NEEDS** the same change as A2′(c): A's writer signs
step-indexed heads; the head law demands a chain link from the held head to the new one; `hr`
reduces to "A's writer signs at most one head per step count", which is accountability, and the
theorem's conclusion gains "or A's writer equivocated, with the two signed heads as witness".
Weeks; one re-genesis for the writer key.

> CORRECTION (2026-10-27, SPEC-4): the `NEEDS` above repeats the discharge §9's own correction refutes
> (a signed fabricated head satisfies "one head per step"). The selected shape is nanodregg
> `Apex.ForeignValid` under `Apex.AuthorityValid` (an authority the recipient names, assumed to certify
> only heads of audited folds); `Foreign` itself no longer needs a fold from genesis (SPEC-23).

---

## 10. Load-bearing versus consequence

### 10.1 The load-bearing five

| claim | one line | trivial system it alone excludes |
|---|---|---|
| §2 ONE HISTORY | a member's World is an audited fold from its start; two members hold one | the follower that trusts the Host; the chain that ignores its inputs |
| §3 INTEGRITY | audited = lawful: authority, conservation, law | the kernel that admits everything; the kernel that mints; the kernel that skips `judge`; the kernel that ignores pins |
| §4 CONSENT | the follower signs only what its own World admits and says `ok` only of what it journals; final is final; one commit per intent | the follower that reports the Host's word; the signer of relay bytes |
| §5 DURABILITY | acknowledged ⇒ durable; reopen = audited fold of the durable records | the writer that replies before `fsync`; the open that forgets |
| §6 THE BELL | one charged ask, one answer, the kept text, across crashes | the resident that asks before it keeps; the Bell without its guard; the broker that refunds |

The APEX is §2 ∧ §3, because each half's floor is the other's trivial system (§2.FLOOR). §4 is the
member machine on §2's World; §5 is what the two Stores keep of it; §6 is the system's only
multi-party instance, and the one place all five meet (a resident is a member; the Bell is an
object; an ask is value-like under a cap; the volume is a crash).

### 10.2 The consequences

§7 (writer confinement: a reading of §2–§4 per lemma), §8 G1 (from A2), §9 (from `check_committed`
under a premise). §8 G2 is a primitive, small and true.

### 10.3 What is NOT top-level, and must not be mistaken for it

* **Generator meaning** (what `Std.offer`, `Std.offerEscrow`, `Std.activity`, `Std.head`, the Bell
  MEAN): the tier below §3.3, one `MethodSpec` per generator with LANGPROOFS' generic
  run-refines-spec theorem and one kernel lift. Collation A4 (the escrow judge ignores the legs)
  lives here, and §3.3 cannot see it — correctly: the author's promise is "your law was run", the
  stdlib's promise is "this law means X", and only the second is false today.
* **Codec canonicity** (`decode_eq_ok_iff`, `Lawful`): a premise of every claim above (`hX :
  decodeCall b = some c → callBytes c = b`, discharged by `eq_callBytes_of_decodeCall`), not a claim.
  CODEC's own top is right and exists; what it lacks is the compiled/emitted gap (§11.7), which is
  a TCB question, not a statement.
* **THE BAR, waste, size**: measured, never claimed (charter).
* **Liveness**: measured, never proved (charter). §7 says so in the writer's voice.

---

## 11. Where the system as built cannot carry a statement, and what it must become

One list; the readers' three structural moves are items 1–4 seen from the statements' side.

1. **Fork consistency (A2′, §9).** Members never compare heads. Needed: `nd sync --to STEPS:CHAIN`
   (days); a head channel — a self-head object in the World, posted by signed calls (a week); and
   writer-signed step-indexed heads with a consistency link in the head law (weeks, one re-genesis),
   which also discharges §9's `hr`. Until then §2 holds for each member alone, §7's last clause is
   open, and "members who consent by re-execution" consent to A history, not THE history
   (PROTOCOL §2.3).
2. **The follower as one object (A1′, C(i)/(ii) under `arbitrary`, E's premise).** Today: the
   decision split across `Kernel.Receive.audit` (proved about), `Command.absorbStep` (run),
   `Host.Follow.loop` (persists), with the command's state in an unauthenticated client-held `k`.
   Needed: `absorbStep := auditStep ∘ decode` or `audit` deleted (weeks; FIX-HOST); the command's
   state inside follow as a typed `Phase` behind a nonce handle (a week of Lean: PROTOCOL §4.1),
   after which `Run arbitrary` collapses to `Run faithful`, the `stdio-leg` row shrinks to "bytes
   moved" (its four trusts: one follower serves the resident; follow's World moves only by its
   frames — already `Moves`; a restarted follow reopens what it persisted — §5 D2; which
   continuation nd returns — gone), and collation A3 (the argv echoed into every frame) disappears
   with the continuation.
3. **The attempt machine in follow (C(v)).** `Attempt.next` is Lean; the loop, fuel, arming and
   files are Rust. Needed: the frozen call and its state in a durable record beside follow's Store
   (NOT a trie kind: the 10-17 premise-spread lesson), every command beginning with "resolve open
   attempts". One to two months (RUST §4.1). Then "at most one commit per intent across re-runs"
   is a theorem over follow's state, and `client/src/attempt.rs` is deleted.
4. **A crash semantics the proofs and the simulator share (§5).** `MemStore.crashImage` as
   `Spec/Env.Crash`; `Loop.serve` as an interpreter over its `Store`/`Port` records; the write side
   (record = `Record.codec` of the staged batch) and the reply-after-sync clause proved over it;
   `Honest` carried across the crash edge (an audited reopen). A month plus a quarter (HOST §3.2(2)).
5. **One ring life (§6).** `RingLife`, `Life` = `Ticks` with crash edges through `resumeOps`, the
   resident as a refinement, the composite theorem. One to two months (HOSTING E2). Close A14 first
   (refuse by name on undecodable output): it is a live counter-example.
6. **`NoRef` (B3).** Extend `object_history_chain` to contextual law bodies through `LawMeaning`,
   or state B3 for `NoRef` laws and keep contextual packages outside the author's promise. The
   deployed Bell, escrow, offer, activity and head are `NoRef`; the eight-of-nine readers' verdict on
   the contextual calculus (delete or connect) is Ember's call (R-0021 kept it) and this spec does
   not depend on it either way.
7. **The compiled and emitted artefact (a TCB row, not a statement).** Every claim above is about
   Lean definitions; the deployed bytes come from the Lean compiler and from `Emit/Rust.lean`'s
   templates, which no instrument examines (CODEC §4.1: three evaluators per vector row; RUST §4.2:
   no hand-written byte layouts). This does not change any statement; it changes what `Spec/` is
   trusted to be ABOUT. The `stdio-leg` row and the `lean4` row should say so in one sentence each.
8. **`cancel` settles on follow's World (C(ii)).** A day (collation A7). Do it before writing
   `Consent.okIsCommitted`, or the pin is red on the first build — which is also fine.

What this list does NOT contain, on purpose: an abstract vat machine; a plant per theorem; a
statement census; a declaration-diff protocol over 6,305 statements. Under §1.2 a meaning change
under any claim is a build error in `Spec/Deployed.lean`, at any depth, which is what the
certificate, the decls gate and the census were approximating by hash and pattern (GATES §3.2(2)).

> CORRECTION (2026-10-27, SPEC-4, CRIT-SPEC-2): false. Weakening a definition below a claim can keep
> its proof green; a meaning change is a build error only where a proof breaks. And §1.1's "a second
> machine is a twin" is wrong for a RELATION: the independent boundary is a transition relation the
> kernel is proved to implement (nanodregg decisions/spec.md SPEC-19, SPEC-24).

---

## 12. `Spec/` — the layout and the order of work

```
Spec/
  System.lean    the record of deployed entry points; `deployed`            (~80 lines)
  Env.lean       Relay (faithful | arbitrary), Crash, Provider              (~120)
  RingLife.lean  one ring's life                                            (~80)
  Claims.lean    OneHistoryMember, WriterFollowerAgree, OneHistoryPair, ForkConsistent,
                 Integrity.{authority,value,grantCap,escrow,law}, Consent.{signsOnlyAdmitted,
                 okIsCommitted,finalIsFinal,atMostOnce}, Durable.{writer,follower,resident},
                 Bell, Shown.onlyFollowers, Foreign                          (~400)
  Floor.lean     ¬ Claim trivialₖ for each row of §2–§8.FLOOR; `inhabited_*` by `decide`
                 over the rows                                              (~300)
  Deployed.lean  theorem top_* : Claim deployed, from the lemmas            (the proofs; untrusted)
```

The trusted reading is `System` + `Env` + `RingLife` + `Claims` + `Floor`: under a thousand lines,
an afternoon, against 6,305 statements today. Law 8 is amended once: spec / def / proof, with
`Spec/` importing definitions only (it names `Honest`, `ObjectHistory`, `Chain`, `ReachOn`, which
live in `Proofs/` modules today — those four definitions move to def modules or `Spec/` re-states
them; LANGPROOFS §2's point that law 8 left specification Props nowhere to live is this).

**Order.** (1) Write `Claims.lean` and `Floor.lean` FIRST, with today's honest premises (`faithful`,
`NoRef`, the crash edge folded not audited, `StdioLeg` as is): days. The floors go red where the
collation says they must (`cancelAnswer`, A14) — leave them red; they are the work list with teeth.
(2) Prove `top_oneHistoryMember`, `top_integrity_value`, `top_integrity_law` (as restricted),
`top_consent_final`, `top_consent_ok` (submit-class), `top_durable_reopen`, `top_shown`: each a
composition of lemmas that exist, one to two weeks in all. That is the apex with named premises,
and from that day the tree has a top. (3) Then the premises, in the order of §11: 8 and 1(a) (days),
2 (weeks), 3–5 (months, one lane each), 6–7 as Ember rules. Each item, when it lands, deletes a
premise from a claim in `Claims.lean` — a strengthening the kernel checks (`New → Old`), which is
the only direction a spec change should ever go without a named reader.

**What the plants become.** The nine `order_refuses_*`, the four `host_step_folds_tooth_*`,
`grant_cap_needs_contiguous`, `in_place_loses_both`, `separates_lawful_floor`, `kept_refutable`,
`not_trusted_of_potential`: these are floor theorems already, and move to `Floor.lean` under the
claim they refute. Every other plant is hygiene, run when cheap (7655145).

---

## 13. The statements, one paragraph each (for the report)

**ONE HISTORY (apex, with INTEGRITY).** A member's World is `audit`-accepted from a start it
consented to — a genesis it built from signed inputs, a carried import under a signed origin, or a
base whose bytes hash to a sponsor's pin — whatever the writer, the relay or its own other commands
did (`∃ w₁ l, Start w₁ ∧ audit X w₁ l = .ok w` for every `Reach`); and two members whose heads agree
at a step count hold one World up to a named collision. True today lemma by lemma, not composed;
the pair half is a kernel theorem (`fold_reaches_host`) with no deployed act behind it — members
never compare heads — and the fork-consistency form needs `nd sync --to` plus a head channel and,
for proof, writer-signed heads. Excludes the follower that trusts the Host and the chain that
ignores its inputs; cannot alone exclude a kernel that admits everything, which is why INTEGRITY is
the same statement.

**INTEGRITY.** An audited log is lawful: a cell changes only by a Turn whose signed call held
authority over it (owner or a live grant chain to the owner carrying the right; an invoke judged by
the laws; a grant only by retire or a spend of its own count; an account only by an authorized
transfer or credit; a member only by its own rotate; a package never); every denomination's balance
and floor sums are conserved and a grant moves at most its cap; and every state an object ever
holds was admitted by every law in force on the pinned view, with the package fixed and each run the
`BigStep` meaning, fuel-independent. Authority: true, composition new (weeks). Value: true. Law:
true for `NoRef` laws; it promises the author that its law was run, not that a stdlib law means its
name (that is the generator-spec tier, where the escrow's missing "receives" lives). Excludes the
open kernel, the minting kernel, the unjudged kernel and the kernel that ignores pins.

**CONSENT AND SETTLEMENT.** Against any Host and, today, a faithful relay: every message follow
offers custody for a call signature is `callMessage u` for a `u` planned from the member's argv on a
World of its own fold that admits it; every `done ok` of a write means the member's own World
journals the planned call (true for submit-class since PROTOCOL-64; FALSE for `cancel`, collation
A7); every `refused`/`expired` settlement is final against every extension (true, needs nothing);
and at most one call commits per intent across re-runs (implemented in Rust by CLIENT-37, no
theorem until the attempt is follow's). Under an arbitrary relay the signing clause is false today
(a fabricated continuation carries an argv the member never issued) and becomes true when the
command's state lives in follow behind a handle. Excludes the follower that reports the Host's word
— the deployed `cancelAnswer` IS that model — and the signer of relay bytes.

**DURABILITY.** Every acknowledged decision names a step in the durable log; after any crash the
writer reopens to the audited fold of exactly the records on disk, holding every acknowledged step
and nothing it did not stage; a follower's Store holds only steps its own `World.step` took and
reopens the same way; the resident's kept answer is intact or absent, never torn. The reopen half is
proved over arbitrary bytes (`open_sound`, `host_reopen_folds`); the write side and the
append-then-sync-then-reply order are read off the loop; `Honest` is not carried across the crash.
Needs the loop as an interpreter over its Store/Port records with `MemStore.crashImage` as the one
crash semantics. Excludes the writer that replies before `fsync` and the open that forgets; inhabited
every 4096 batches by the writer's own `reopenDiverged` check.

**THE BELL.** For every ring, across any schedule of ticks, replies, crashes and restarts: answered
at most once, by the resident, with its own text echoed (the `rings` guard); its answer decided by at
most one charged ask or named `(unanswered restart)`; the answered row's text the kept one; no charge
past the cap and no refund across a restart; no refusal retried forever. Every slice is a theorem
(`tick_counts`, `bell_resident_conforms`, `keep_atomic`/`resume_durable`,
`delivered_answer_committed_strong`, `answered_row_committed` over `ReachOn`, `bell_monitored`,
`capped_decide`, `start_window_refused`, `no_refusal_repeats_forever`); the composite across crashes
is not written and needs one `RingLife` process the resident refines. Collation A14 (undecodable
stdout reads as "nothing pending") is a live counter-example to the one-ask clause under a lying
relay. Excludes the resident that asks before it keeps, the Bell without its guard, and the broker
that refunds.

**WHAT THE WRITER CAN AND CANNOT DO** (consequence). It can order, delay, withhold, decline forever
(seen as `open`), refuse within budget, and read everything. It cannot invent or alter a Turn, record
a refusal `judge` would not, censor under a refusal, record a stale, re-judge a journaled call, make a
member see `ok` for an unjournaled call or sign an unadmitted one, falsify a receipt, mint, exceed a
cap, or serve the log to a non-follower — each by a named lemma. It CAN fork two members undetected
today; that is the one open adversary capability and the fork-consistency act closes it.

**WHAT TWO MEMBERS CAN AND CANNOT BE SHOWN.** They can be shown one history (A2, once they compare
heads). A holder of no live follow grant is shown nothing of the log (`Envelope.check` before every
`defer`; true, one page). Inside a World nothing is hidden between members or from the operator —
membership is the confidentiality boundary, by charter, and the spec says so rather than letting a
reader infer otherwise.

**RECEIPTS BETWEEN WORLDS** (consequence). A committed receipt against a held head means the call
was admitted in that head's fold — provided the held head is the head of a fold of A, a premise
nothing discharges today (heads posted by grantees, unsigned). Writer-signed step-indexed heads with
a consistency link, the same change fork consistency wants, reduce it to "A's writer signs one head
per step count" and turn a lie into an equivocation proof.
