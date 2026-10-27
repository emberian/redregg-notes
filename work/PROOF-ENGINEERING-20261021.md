# PROOF ENGINEERING — what nanodregg's proofs are made of, and what they should be made of (SCHOLAR-PROOF-ENG, 2026-10-21)

Read-only; nothing built, nothing landed, nothing killed. For a reader who studied the program logics and
wants to decide, not be told. Ember's sentence (10-21): *"Regarding proof engineering we need to break out
that subtopic into a wider topic with more detail because I don't know how to make a call here yet."*

| Tree | Read at | Role |
|---|---|---|
| nanodregg | hbox `/tank/dregg-build/nanodregg/main` @ `cdd9d84` (10-21; `SIZE.md`: 4966 theorems, 202 proof-modules, 0 sorry, 12 native) | the subject |
| breadstuffs | `~/dev/breadstuffs/metatheory/Dregg2` @ `22fad151e` | the prior art for wp / temporal / refinement |
| minidregg | `~/dev/minidregg` @ `334316df` | the prior art for law meaning and the run-level lift |
| prior scholars | `PROOF-TECHNIQUE-20261019.md` (left Q1/Q2/Q3), `COMPARE-20261021.md` §4 (the wp polarity finding) | not re-derived; corrected where the tree moved |

Labels: **MEASURED** (I read the statement or ran the grep at the commit above), **READ** (prose: a
docstring, a decision, a header), **INFERRED** (my step from measured facts), **ASSUMED** (not checked; a
lane checks it first). Counts are `grep` over `^theorem|^lemma|^private theorem` and miss multi-line
headers; treat each as ±5%.

What moved since the 10-19 brief, so its numbers are stale (MEASURED): KERNEL-51 (`Logic/Frame.lean`, the
frame rule) and its locality half `check_local` LANDED; KERNEL-52 (`Logic/HeadRead.lean`, `HeadSound`)
LANDED; KERNEL-56 deleted `Collision`/`Trie.Coll`/`HashColl` and put `CollidesAmong hash S` over an
explicit list in every escape (61 theorems were vacuous); KERNEL-57 landed `law_judged`; `InvokeNext.lean`,
`InvokeTree.lean`, `Ledger/Proofs/EscrowRun.lean` + `EscrowInvokes.lean` built the run-level lift for ONE
package by hand. 3734 → 4966 theorems in two days.

---

## 0. The four-line verdict

1. Nano's receivers already have small-footprint semantics **by type**: `receive` never sees a `World`, it
   sees `Pinned D`, a partial heap answering only for pinned ids (`Kernel/Receive/Call.lean:1-15`, READ;
   `receive_congr` is 13 lines of `funext`, MEASURED). Separation logic's locality is enforced at the
   definition, so no logic is needed to prove it. **Q1: name the contract as a Prop-structure, add one
   call-level frame rule, no assertion language.**
2. Host ⊑ Kernel exists as five equalities nobody has composed (`step_submit`, `open_sound`, `audit_ok`,
   `fold_reaches_host`, `Kept`) and a sim plant that sees only seeded paths. **Q2: one theorem over every
   request kind; keep the plants for the IO.**
3. The run-level lift exists for one package as three inductives and two lift theorems
   (`Chain`/`Runs`/`Invokes`, `invokes_runs`). **Q3: generalise that, proved once; `Admits` stays
   existential (a fault never admits); the fold is wp-shaped, the law is sp-shaped.**
4. Of the logics nano lacks, **a temporal vocabulary is the only one worth 30 lines**; separation is
   already there in the trie's keys and the authority layer is a capability logic by hand; a kernel cost
   logic buys build-time instead of gate-time and nothing else.

---

## 1. THE INVENTORY — every proof shape nano uses today

### 1.1 Counts by layer (MEASURED, `^theorem|^lemma|^private theorem`)

| layer | theorems | note |
|---|---|---|
| Kernel/Proofs (+Logic) | 1380 + 15 | Logic = Frame.lean 255 lines, HeadRead.lean 172 lines |
| Lang/Proofs | 1256 | `Std.lean` 86 (the law theorems) |
| Codec/Proofs | 897 | codec algebra; not this document's subject |
| Hosting/Proofs | 429 | resident/broker/controller; the crash model lives here |
| Host/Proofs | 378 | open/seal/backup/size/loop |
| Protocol/Proofs | 314 | receipts, settle, command |
| Ledger/Proofs | 87 | escrow: the one package with a run-level theorem |

### 1.2 Shape census (MEASURED, grep over all proof dirs)

| shape | count | grep |
|---|---|---|
| `by decide` / `<;> decide` proofs | 1066 | the witness theorems; the sim's planted arms and the teeth |
| `:= rfl` proofs | 178 | definitional unfoldings (`tick_def`, `resolve0`, …) |
| `native_decide` | 3 | with allow rows (law 6) |
| teeth (`_tooth`, `_needs_`, `_bites`, `_tells`, `_refuses_`) | 131 | one refutation per predicate, the floor-false discipline |
| `… ∨ CollidesAmong …` statement lines | 45 | every hash escape, over an explicit list since KERNEL-56 |
| `*_sep` (escape-free twin under `Separates`) | 61 | one per escape: `hs.elim (main …)` |
| `fold_*` theorems | 59 | fold inductions; 21 go through `fold_keeps` |
| `admit_*` / `refuse_*` / `genesis_*` | 76 / 49 / 28 | the "preserved through each transition" family |
| `deployed_*` | 40 | generic theorem + `deployed_lawful`/`deployed_reach`, by hand each time |
| `↔` statements | 90 | canonicity, Bool↔Prop reflections, `audit_ok` |
| `_le`/`_lt`/`_bounded`/`_ge` | 104 | size, budget, cost bounds |
| `_inj`/`_injective`/`_injOn` | 69 | commitments and names |
| `_congr`/`_local` | 15 | locality |
| never/once/first/after/mono/antitone in the name | 47 | the hand-rolled trace properties |
| `inductive … : Prop` in proof modules | 51 | footprints, read sets, chains, meanings, derivations |
| `structure … : Prop` in proof modules | 19 | `Checked`, `Frame`, `Agree`, `Kept`, `HeadSound`, … |
| theorems taking `hE : E.Lawful n` / `hX : X.Lawful` | 116 | the one bundled parametricity premise |
| theorems taking a trie `*Canon` premise | ~150 | the premise that KERNEL-41/49 priced |
| theorems taking `hk : Kept` | 12 | Host's reach invariant |

### 1.3 The shapes, each with its best example and what it cannot say

**S1 · Equalities and invariants over the fold** (59 `fold_*`; the Kleene-star rule by hand).
Scheme: `fold_keeps {P} (ha : P w → admit = ok w' → P w') (hr : P w → refuse = ok w' → P w') : P w → fold = ok w' → P w'`
(`Kernel/Proofs/Refuse.lean:164-167`, MEASURED). Used 21 times. The other ~38 are relations to the START
state (`fold_conserves`, `fold_value`) or potentials, written out by induction each time (READ, 10-19 brief;
unchanged). Best example of the reach: `Host/Proofs/Size.lean:155` `reached_size_le (hb : budgetFault w = none)
(hk : Kept w) (h : fold X.env w l = .ok w') : (world codec).bytes w').size ≤ Cadence.deployed.worldBytesMax`,
closed by `omega` over six bounds (MEASURED). **Cannot say:** anything about a position IN the fold ("at
step i", "after the first X", "never after"); `fold` is a `List (Step D)` with no index vocabulary, so each
trace property is a fresh inductive (S5) or a `fold_append` argument.

**S2 · `P ∨ CollidesAmong hash S`** (45 statement lines + 61 `_sep` twins).
`CollidesAmong hash S := ∃ p ∈ S, ∃ q ∈ S, p ≠ q ∧ hash p.1 p.2 = hash q.1 q.2`; `Separates hash S := ∀ p q ∈ S,
hash p = hash q → p = q` (`Fold.lean:30, :43`, MEASURED). Best: `chain_binds (hE) … chainOf E c l₁ = chainOf E c l₂
→ l₁ = l₂ ∨ CollidesAmong E.hash (chainPres E c l₁ ++ chainPres E c l₂)` (`:199-202`); `inclusion_sound (hw : WF)
(hr : Routed) (hv : verifyInclusion … = true) : (∃ v, t.get S k = some v ∧ S.vdigest v = dig) ∨ CollAmong S
(readPres S k p t)` (`Trie.lean:968-970`). The escape names its inputs; the `_sep` form is the statement with
no escape. This is a *computational-soundness* idiom (ROM-free: no random oracle, an explicit colliding
pair), and KERNEL-56's finding — that `∃ a b, a ≠ b ∧ hash a = hash b` is provable by pigeonhole from
`E.Lawful` — is the reason the list must be explicit (memory `minted-a-disjunct-provable-from-the-premises-is-vacuous`).
**Cannot say:** a probability. Every bound is "or here is the pair"; there is no `ε` and no reduction, which
is right for a kernel whose hash is a parameter.

**S3 · Frame and read-set locality** (`Logic/Frame.lean`, `Local.lean`; 15 `_congr/_local`).
`inductive CellFoot (t) : Slot D → Prop` (touched non-keep / born / spent, `:32-35`); `structure Frame E w w' t : Prop`
with `cells` (no premise), `rows (w.RowsCanon E →)`, `journal (w.JournalCanon E →)`, `refusals (w.RefusalsCanon E →)`
(`:65-71`); `admit_Frame : admit = ok w' → Frame E w w' t` (`:76`); `not_cellFoot_iff` is the reader's evidence
that the footprint is not larger than the old inline hypotheses (`:48`). The read half: `CellRead`/`RowRead`/
`RowsAgree`/`Agree` (`:118-152`) and `check_local (h : Agree E w w' t) : check E w' t = check E w t`
(`Local.lean:440`); its teeth `check_local_outside`, `check_reads_kept(_sep)`, `check_unread_row` (`:489-552`),
and `cellFoot_read : CellFoot t s → CellRead t s` (`Frame.lean:162`: a turn reads what it writes). This is the
small-footprint semantics of Calcagno–O'Hearn–Yang, stated for one concrete transition over a map keyed by
`Slot D`. **Cannot say:** a frame for a CALL (the footprint is of the derived `Turn`, not of `c`); two-turn
disjointness as a rule (`admit_comm` in `RowsComm.lean` is the instance, still by hand, READ).

**S4 · The law × occasion meaning statements** (16 of `Std.lean`'s 86; COMPARE §4.2 census, READ, grep-confirmed 86).
`Admits lib t rq n o := ∃ cenv w, BigStep lib (rq.toVal :: n.toVal :: o.toVal :: cenv) (lawBody t) (.ok (.inj "ok" w))`
(`Std.lean:186-187`, MEASURED). Best: `windowed_counts (h : Admits lib (windowedLaw S T W limit g) rq n o)
(ho : rq.field "occasion" = some (.inj ℓ x)) (hl : ℓ = "write" ∨ ℓ = "invoke") : ∃ c inc, n.field "count" = some (.nat c)
∧ … ∧ c ≤ limit …` (`:751-757`), whose docstring confesses the gap: *"A per-STEP fact: 'at most `limit` changes
per epoch' is its induction over a history … no theorem here states that induction"* (`:746-750`, READ).
The bridge to the deployed judge: `judgeOne_admits (hid : digestOf (bytesOf law) = some law) (hp : readPackage look
law = .ok p) (hb : p.body = .record fs) (h : judgeOne … = .ok ()) : ∃ o n lib f, readState … old = .ok o ∧ readState … new
= .ok n ∧ ∀ ℓ ∈ p.laws, ∀ t, Row.find? ℓ fs = some t → IsLaw t → Std.Admits lib (t.relocate f) (reqData bytesOf r) n o`
(`Lang/Proofs/Receiver.lean:411-418`). **Cannot say:** anything across two steps; the state the law judges
is `(o, n)` and the theorem ends there.

**S5 · Chains over admitted histories** (the by-hand run-level lift; one package).
Three inductives, each a trace predicate for the escrow:
- `inductive Chain lib : Data → List (Data × Data) → Prop` — `cons : Admits lib law rq n o → Chain lib n rest → Chain lib o ((rq, n) :: rest)` (`Ledger/Proofs/Escrow.lean:201-204`). Pure Lang; `escrow_law_payout_once : Chain lib o steps → payouts steps ≤ 1` (`:229`).
- `inductive Runs prog pkg p : Slots → List (List (Body D)) → Prop` — `cons : readPackage look pkg = .ok p → prog.run look rv pkg state method args r budget = .ok (s, calls, rows, used) → prog.judge look (some pkg) laws state s r = .ok () → (∀ k, next.get k = s.get k) → Runs … next rest → Runs … state (calls :: rest)` (`EscrowRun.lean:307-318`). The receiver's runs, with the slot link `∀ k, next.get k = s.get k`.
- `inductive Invokes X obj pkg p : World D → List (List (Body D)) → Prop` — `invoke : receive X w c = .ok t → admit X.env w t = .ok w' → c.unsigned.body = .invoke obj … → invokeRun … = .ok (cell, pkg, r) → readPackage … = .ok p → X.program.run … (stateOf cell) … = .ok (s, calls, rows, used) → Invokes … w' rest → Invokes … w (calls :: rest)`; `other : admit X.env w t = .ok w' → (∀ x ∈ t.touches, x.cell ≠ obj) → obj ∉ createdIds t → Invokes … w' rest → Invokes … w rest` (`EscrowInvokes.lean:44-57`). The World's history around one object.
- The lifts: `invokes_runs : Invokes X obj pkg p w invs → invs = [] ∨ ∃ cell, w.live X.env obj = some cell ∧ Runs X.program pkg p (stateOf cell) invs` (`:64-66`), proved from `admit_frame`, `invokeRun_live`, `invoke_next_judged`, `invoke_next_slots` (MEASURED, the proof body `:67-86`); then `escrow_invokes_one_payout (hX : X.Lawful) (hprog : X.program = Lang.program …) : Invokes X obj pkg escrow w invs → payoutCalls invs ≤ 1` (`:90-92`) and `escrow_invokes_deployed` at `Host.Deployed.X` (`:102`).
- The kernel link it rests on: `invoke_next_slots (hc : receive X w c = .ok t) (ha : World.admit X.env w t = .ok w') (hb : c.unsigned.body = .invoke obj method args budget via) (hr : invokeRun X (pinned X.env w c.unsigned.pins) c c.unsigned.member obj method via = .ok (cell, p, r)) (hp : X.program.run (pinned …) (rowView …) p (stateOf cell) method args r (min budget (poolOf c.unsigned.body)) = .ok (s, calls, rows, used)) : ∃ cell', w'.live X.env obj = some cell' ∧ ∀ k, (stateOf cell').get k = s.get k` (`Kernel/Proofs/InvokeNext.lean:444-452`, MEASURED). No premise beyond the two transitions and the run (header `:19-22`, READ).
- The rely: `def Honest X : World D → List (Step D) → Prop | _, [] => True | w, .turn t :: rest => ∃ c, X.decodeCall t.event = some c ∧ receive X w c = .ok t ∧ ∀ w', admit X.env w t = .ok w' → Honest X w' rest | w, .refusal r :: rest => …` (`Kernel/Proofs/Audit.lean:156-161`); `audit_ok : audit X w l = .ok w' ↔ fold X.env w l = .ok w' ∧ Honest X w l` (`:235-237`).
**Cannot say:** the same for a second package without writing three more inductives; a step that touches
`obj` other than as a top-level invoke (the `EscrowInvokes` header says so, READ; HEAD `ececba1` added
`invoke_tree_slots` for nested invokes but `Invokes` does not yet use it, INFERRED from the header).

**S6 · Crash-relation durability** (`Hosting/Proofs/ResidentVolume.lean`, HOSTING-37).
`def Crash (v v' : Vol) : Prop := (∀ p, v'.live p ∈ v.hist p) ∧ (∀ p, v'.hist p = [v'.live p]) ∧ (∀ i, v.synced i = true →
v'.data i = v.data i) ∧ (∀ i, v'.synced i = true) ∧ v'.next = v.next ∧ v'.cur = none` (`:58-62`): a crash returns ANY
value an entry has held since the last directory sync, and unsynced file data is arbitrary. `keep_atomic (hs : Stable
v w.kept) (hf : Fresh v) (hl : Live v) (n) (hc : Crash (v.applyAll ((keepOps w s).take n)) v') : v'.read w.kept = v.read
w.kept ∨ v'.read w.kept = some (some s)` (`:184-186`). The teeth are the three classic bugs (no fsync, no dirsync,
in-place write), each "some crash outcome is wrong" (header `:9-14`, READ). The effect-tree half:
`inductive Runs : Prog α → List Ev → α → Prop` (`ResidentRun.lean:51-57`: one constructor per effect, ANY result) and
`interp_runs (o : Oracle) (p) (n) (es) : ∃ es', ((p.interp (recorder o)).run (n, es)).2.2 = es ++ es' ∧ Runs p es' …`
(`:700-702`): the deployed interpreter performs exactly a path. This is a free-monad/algebraic-effects
semantics with a nondeterministic crash relation — the shape of a verified-storage proof (FSCQ's crash
Hoare logic, Yggdrasil's crash refinement) done on one small volume. On the Host side the same idea is
`recover_torn` (`Host/Proofs/Log.lean:5-6`, READ): cut the next frame anywhere and the prefix reads back.
**Cannot say:** anything about a crash DURING the Host loop's seal/append (Host's loop is not a `Prog` tree;
its durability facts are per-file lemmas, INFERRED from the Host/Proofs listing: Log, Seal, Backup, Index).

**S7 · Size / budget / cost bounds** (104 `_le/_lt/_bounded`).
Kernel/Host: `reached_size_le` (S1), `store_turns_le` (`Size.lean:105`), `turns_logWeight_le` (`:81`: log bytes ≤
weight + allowance, from `fold_conserves`). Lang has a real cost calculus: `Derives lib env t r n` (`BigStep` carrying
the derivation size), `derives_unique` (`Need.lean:41`), `need_derives` (`:325`: the deployed counter returns that
size), `Forces lib T v n` (`:343`) tied by `forces_le` (`:531`) to `Machine.extract`, `required_lt_ticks` (`:746`: the
reference count is below the ticks charged); and LANG-64's `walked_le : walked lib cap fuel (State.init t env) ≤
Bounds.wordBytes * (run lib cap fuel 0 (State.init t env)).used` (`Cost.lean:161-163`) proved by a POTENTIAL
(`stackPaid : List Frame → Nat`, `:64`; `step_paid`, `:93`): the amortised-complexity argument of Tarjan, in 167
lines. **Cannot say (kernel):** hash counts; by KERNEL-36 they are instruments (WASTE rows), not theorems (READ, 10-19 brief).

**S8 · Witness theorems by `decide` + kernel** (1066 `by decide`, 178 `rfl`, 3 `native_decide`).
Closed instances evaluated in the kernel: `idApp_ticks : (run [] 8 16 0 (State.init idApp)).used = 7 := by decide`
(`Need.lean:769`); `worldBytesDerived_eq : worldBytesDerived = 91914346 := by decide` (`Size.lean:116`);
`runLaw_nat_stuck` (`LawRun.lean:193-196`); every `*_needs_*` tooth builds a concrete turn and runs `admit`. Law 6
(`CHARTER.md:56-62`, READ): named theorems, a tree-wide axiom census, `native_decide` only with an allow row.
**Cannot say:** anything general; a `decide` proves one instance and the reader must ask what general fact it
instantiates (the 10-19 brief's "a tooth per theorem is hygiene, not a calculus" stands).

**S9 · Machine ⟷ reference: the one place that is already a calculus** (Lang).
`BigStep` + `bigStep_deterministic`; `run_bigStep`/`bigStep_run` (machine ≡ reference); `Means lib T v d` (`Extract.lean:79`)
with `extract_means` (`:128`: whatever extraction returns at any budget is the meaning, no premise),
`means_deterministic` (`:217`), `means_get` (`:300`: a field is its projection's meaning under ANY derivation);
`runMeasured_means` (`:363`); `extract_progress` (`LawRun.lean:60`: typed extraction never ends `stuck`),
`runLaw_never_stuck` (`:150-158`). This is a denotational-vs-operational adequacy result plus a progress
theorem under typing; it is the textbook shape and needs nothing. **Cannot say:** anything about `World`.

**S10 · Teeth** (131). Not a logic; the floor-false discipline (memory `feedback-prove-the-floor-false`). Keep.

### 1.4 What the inventory as a whole cannot express (the gaps a decision is about)

| gap | where it bites today | evidence |
|---|---|---|
| G1 no run-level lift for laws | `windowed_counts`' docstring; escrow's three hand inductives | S4, S5 |
| G2 no named Host ⊑ Kernel | five equalities + a seeded plant; a Host path the generator misses is invisible | §3 Q2; KERNEL-57 meta-critique (`decisions/kernel.md:2874-2890`, READ) |
| G3 no temporal vocabulary | 47 never/once/after/mono theorems, each its own induction; `settle_final_never_admits` is `□¬` by hand | S1, §4.2 |
| G4 no call-level frame | `Invokes.other` spells "neither touches nor creates obj" inline; a frame for `submit c` does not exist | S3 |
| G5 no assertion language | not a gap: see §4.1 | — |
| G6 kernel cost outside the logic | by ruling (KERNEL-36) | S7 |

---

## 2. THE THREE QUESTIONS, widened into options worked on nano's own code

Two theorems are restated in every option. The landed texts (MEASURED):

```lean
-- Kernel/Proofs/Receive.lean:120-126
theorem receive_ok (h : receive X w c = .ok t) :
    X.verify c.unsigned.key (X.callMessage c.unsigned) c.signature = true ∧      -- 1 signed by the named key
      t.charge = t.weight ∧ t.charge ≤ c.unsigned.maxCharge ∧                      -- 2,3 pays its weight, within the ceiling
      t.touches.map (fun x => (x.cell, x.seen)) = c.unsigned.pins ∧                -- 4 touches = the signer's pins, in order
      t.event = X.callBytes c ∧ t.txId = txIdOf X c ∧                              -- 5,6 the event and id are the call's
      t.notBefore = c.unsigned.notBefore ∧ t.validUntil = c.unsigned.validUntil    -- 7,8 the window is the signed one

-- Kernel/Proofs/Receive.lean:38-41 (locality)
theorem receive_congr (ho : w₁.origin = w₂.origin)
    (agree : ∀ p ∈ c.unsigned.pins, w₁.live X.env p.1 = w₂.live X.env p.1)
    (rows : rowView X.env w₁ c.unsigned = rowView X.env w₂ c.unsigned) : receive X w₁ c = receive X w₂ c
```
and `invoke_next_slots` as quoted in S5 (five hypotheses `hc ha hb hr hp`, conclusion
`∃ cell', w'.live X.env obj = some cell' ∧ ∀ k, (stateOf cell').get k = s.get k`).

### 2.1 Q1 · Which logic should the receivers speak?

The fact that decides this (MEASURED): `receive X w c` is `receiveWith X (pinned X.env w c.unsigned.pins) (rowView X.env w
c.unsigned) c` after the origin check (`receive_ok_with`, `Receive.lean:25-28`), and `receiveWith` takes `look : Pinned D`
— a function that answers `unpinned` for any id not in the pins (`Call.lean:6-9`, READ). The receiver's heap is the
footprint. That is why `receive_congr` is a `funext` and 13 lines, and why the receivers have no `Canon`
premise anywhere (grep: `Receive.lean` takes none).

**Option A — the eight-conjunct contract, as landed.** Composition today: by `obtain ⟨h1, …, h8⟩` at every
consumer (`invoke_next_slots` opens `receive_ok_with` → `receiveWith_sealed` → `sealTurn_ok` → `derive_eq` → the
`dispatch` cases, `InvokeNext.lean:453-470`, MEASURED). Premises added: none. What does not compose: a
consumer that needs conjunct 4 and a kernel fact must thread both by hand; nothing names "the contract".

**Option B — a Hoare triple over `submit` with a frame rule.** Since `receive` and `admit` are functions, the
triple is a definition over them, not a new semantics:

```lean
/-- {P} submit c {Q}: every derived-and-admitted run of `c` from a `P`-World lands in `Q`. -/
def Triple (X : Ctx D) (P : World D → Prop) (c : Call D) (Q : World D → Turn D → World D → Prop) : Prop :=
  ∀ w t w', P w → receive X w c = .ok t → World.admit X.env w t = .ok w' → Q w t w'

/-- `receive_ok`, restated: the contract is the postcondition of the trivial precondition. -/
structure Derived (X : Ctx D) (c : Call D) (t : Turn D) : Prop where
  signed    : X.verify c.unsigned.key (X.callMessage c.unsigned) c.signature = true
  exact     : t.charge = t.weight
  priced    : t.charge ≤ c.unsigned.maxCharge
  pinned    : t.touches.map (fun x => (x.cell, x.seen)) = c.unsigned.pins
  event     : t.event = X.callBytes c
  txId      : t.txId = txIdOf X c
  window    : t.notBefore = c.unsigned.notBefore ∧ t.validUntil = c.unsigned.validUntil
theorem receive_derived (h : receive X w c = .ok t) : Derived X c t       -- = receive_ok, as a record
theorem submit_derived : Triple X (fun _ => True) c (fun _ t _ => Derived X c t)

/-- `invoke_next_slots`, restated: precondition = the run on the pinned view; post = the next state. -/
theorem invoke_next_triple (hb : c.unsigned.body = .invoke obj method args budget via) :
    Triple X
      (fun w => ∃ cell p r, invokeRun X (pinned X.env w c.unsigned.pins) c c.unsigned.member obj method via = .ok (cell, p, r)
         ∧ X.program.run (pinned …) (rowView …) p (stateOf cell) method args r (min budget (poolOf c.unsigned.body)) = .ok (s, calls, rows, used))
      c
      (fun _ _ w' => ∃ cell', w'.live X.env obj = some cell' ∧ ∀ k, (stateOf cell').get k = s.get k)
```
The rule that does not exist today and would (G4): a **call-level footprint** and its frame.
```lean
/-- What a call may write: its pins (every touch is a pin, `receive_ok`.4), the ids it bears
    (`bornAt X c base cr`: a function of `X`, `c` and a count, `Receive.lean:82-85`), its nullifiers. -/
inductive CallFoot (X : Ctx D) (c : Call D) : Slot D → Prop
  | pinned {p} (hp : p ∈ c.unsigned.pins) : CallFoot X c (.cell p.1)
  | born {i} (hi : i ∈ bornIds X c) : CallFoot X c (.cell i)          -- bornIds: a def-module helper (closure C3)
  | spent {n} (hn : n ∈ nullifiersOf X c) : CallFoot X c (.nullifier n)
theorem callFoot_of_turn (h : receive X w c = .ok t) : ∀ s, CellFoot t s → CallFoot X c s
/-- An assertion that reads only outside the call's footprint is kept by the call. -/
def Indep (X) (c) (R : World D → Prop) : Prop :=
  ∀ w w', (∀ s, ¬ CallFoot X c s → w'.trie.get (trieSpec E) s = w.trie.get (trieSpec E) s) → (R w ↔ R w')
theorem submit_frame (h : Triple X P c Q) (hR : Indep X c R) : Triple X (fun w => P w ∧ R w) c (fun w t w' => Q w t w' ∧ R w')
  -- proof: admit_Frame + callFoot_of_turn; cells only. A rows/journal frame takes RowsCanon/JournalCanon INSIDE the field, as Frame does.
```
`Invokes.other`'s inline `(∀ x ∈ t.touches, x.cell ≠ obj) → obj ∉ createdIds t` becomes `¬ CallFoot X c (.cell obj)`
(INFERRED: it is `not_cellFoot_iff` one level up). **What composes that does not today:** sequential
composition over a two-call fold, `{P} submit c₁ {Q} → (∀ t w', Q … → P' w') → {P'} submit c₂ {R} → {P} fold [c₁, c₂] {R}`,
which is what every chain in S5 does by hand; and `submit_frame`, which is what `invokes_runs`' `other` case
does by hand with `admit_frame`. **Premises added to landed theorems: 0** (every landed statement is an
instance by `intro`). **Cost:** one hub proof-module (`Kernel/Proofs/Logic/Triple.lean`), ~150 lines; the
per-assertion `Indep` proofs are the new labour — and note they are one `cases` each, because every assertion
nano writes is a `get` at a named slot.

**Option C — a separation-logic spec over the pinned view.** Assertions `c ↦ cell := w.live E c = some cell`,
`∗` as key-disjoint conjunction, the pins as `∗_{(c,d) ∈ pins} c ↦ₚ d` (the pin is a digest of the live cell,
`pinOf`, READ 10-19 brief). `receive_ok` becomes `{ ∗ pins } receive c { t. Derived ∧ CellFoot t ⊆ pins ∪ born ∪ spent }`
and `unpinned` is the frame's refusal. **What it buys over B:** nothing the type does not already give. Because
`receive` takes `Pinned D`, "a derivation depends only on what the signer saw" is not a theorem to be made a
rule; it is the function's domain. `∗` over a map keyed by `Slot D` is `∧` with distinct keys (the PCM is
disjoint union of a finite map; no fractional or counting permission except the row HEADS, which `RowFoot.head`
already puts inside the footprint, `Frame.lean:41-42`). **What it costs:** an assertion language is a second
World of statements (the 10-19 brief §4.4's warning, which I confirm): every theorem in S3 would need a
translation lemma to the `get`-equalities the consumers actually use. **Premises added: 0 to landed, but an
`Indep`-like side condition on every assertion forever.** Lean: no.

**Option D — a trace / temporal statement over the fold.** `receive_ok` as "along an `Honest` log every turn is
`Derived` of its own call": that is `Honest`'s definition (`Audit.lean:158`) composed with `receive_derived` —
`□ Derived`, with `Honest` the `□`. `invoke_next_slots` as `□(invoke obj at i → state at i+1 = s_i)`: that is
`Invokes.invoke` + the theorem. **What it buys:** a name for "every step", which `Honest` already is. **What it
costs:** a position index on the fold; today every chain avoids indices by being an inductive. Premises: `Honest`
on each new theorem. This is not a receiver logic; it is §4.2's vocabulary applied to receivers. Not Q1's answer.

**My read.** B, minus nothing. The receivers already speak small-footprint semantics by type; what they lack is
a NAME for the contract (`Derived`) and ONE rule at the call level (`submit_frame` over `CallFoot`). minidregg
does exactly the record-as-contract move (`structure FillAllowed … : Prop`, `structure Fill …` bundling every
precondition, `Kernel/CanonicalEscrowMarket.lean:122, :381`, MEASURED) and it reads well there. The
eight-conjunct `∧`-chain and the 23-component `obtain` patterns the 10-19 brief counted are the cost of not
naming it.

### 2.2 Q2 · `Host ⊑ Kernel` as a named refinement theorem, or a plant?

**What exists (MEASURED):**
- `step_submit (hop : Op.ofCode? q.body.op = some .submit) (hc : X.decodeCall q.body.payload = some c) : let g := (refusedAnswer X w c).isNone && journalForgets w.height c.unsigned.notBefore; ((machine X).step (w, out) q).1 = (if g then w else Settle.keptWorld w (judge X w c)) ∧ ((machine X).step (w, out) q).2.staged = (if g then out.staged else judgeStaged X out (judge X w c))` (`Host/Proofs/Serve.lean:91-95`): the Host's World after ONE request kind is the kernel's `judge`.
- `open_sound … (h : openLog s recordMax step w₀ initial log = .ok o) : ∃ rs, log.extract 0 o.validLen = encodeAll s initial rs ∧ rs.foldlM step w₀ = .ok o.world ∧ …` (`Host/Proofs/Open.lean:57-60`): an opened World is the fold of the bytes.
- `structure Kept (w : World D) : Prop` with `canon, slotted, cellsFit, journalOk, …` (`Host/Proofs/Deployed.lean:363-367`+): the reach invariant; 12 theorems take `hk : Kept w`.
- `audit_ok` (S5) and `fold_reaches_host (hE) (hh : fold E g lh = .ok host) (hf : fold E g lf = .ok follower) (hst : follower.steps = host.steps) (hc : follower.chain = host.chain) : follower = host ∨ CollidesAmong E.hash (foldPres E g lf ++ foldPres E g lh)` (`Fold.lean:442-446`): follower ⊑ writer.
- The plant: kernel-sim compares the four tries' listings and roots after every seed (`same`, `reopened`; READ, 10-19 brief §5 Q2; not re-read).
- The prose premise `CheckpointTrusted` the brief told me to read in `Host/Proofs/Trusted.lean` **does not exist in Lean**: the file is absent; the name occurs once, in a PROPOSED retention decision (`decisions/kernel.md:1867`: "a received base … is NOT discharged: that is the trust above, stated as a premise (`CheckpointTrusted`)"). MEASURED (grep over Host/Hosting/Protocol/Kernel/Ops/Client). The brief's pointer was to a design, not a theorem.

**What the refinement would state, exactly.** Concrete: the Host machine `(machine X).step : HostState → Request Frame → HostState` over the six protocol ops (SIZE: "protocol operations 6"). Abstract: `World.fold X.env` over `List (Step D)` under `Honest`. Relation: `R s w := s.1 = w ∧ Kept w` (the Host state's World component IS the abstract state; no abstraction function, a projection). The square, per step and per run:
```lean
/-- Every Host step is an honest fold of zero or one kernel step on its World. -/
theorem host_step_folds (hk : Kept s.1) (q : Request Frame) :
    ∃ l, l.length ≤ 1 ∧ World.fold X.env s.1 l = .ok ((machine X).step s q).1 ∧ Honest X s.1 l
theorem host_run_folds (hk : Kept s₀.1) (qs : List (Request Frame)) :
    ∃ l, World.fold X.env s₀.1 l = .ok (run (machine X) s₀ qs).1 ∧ Honest X s₀.1 l ∧ Kept (run …).1
```
`step_submit` is the `.submit` case; the other five ops are `l = []` cases or (for `log`/`carry`/`import`, ASSUMED which) a seal that leaves the World. The staged output's half (`judgeStaged`) is a second field. **Under crash:** `open_sound` + `recover_torn` give `host_reopen_folds : openWith … = .ok o → ∃ l ≤ the log, fold g l = .ok o.world`, i.e. every instant of a live Store refines some prefix (the backup theorems already say this per file, READ 10-19 brief §2.3).

**What it catches that the plants cannot.** A Host path that moves the World without `judge`. The plant runs seeded calls; a path with no seed row (a cadence seal, `makeRoom`, a carry import, `accept` of an invitation — `Host/Proofs/Cli.lean:64-65, :167, :185` shows `Protocol.Invite.accept … = .ok (i, w)` producing a World, MEASURED) is invisible to it, and KERNEL-57's meta-critique names the class: "a branch the generator cannot reach is a label that reads as coverage" (`decisions/kernel.md:2890`, READ). The theorem is over `step`'s match, so it is total over ops by construction: a seventh op without a case does not compile.

**What it does not catch.** IO: fsync order, socket replies, the loop's clock. For those the resident's pattern (`Prog` tree + `Runs` paths + `interp_runs`, S6) is the right instrument, and the Host loop is not a `Prog` tree today. Making it one is option C below.

**Options.** (A) plants only. (B) `host_step_folds`/`host_run_folds` as above, the five equalities as cases; ~1-2 lane-days; premises on landed 0; new theorem takes `Kept` (already discharged at genesis and kept by `kept_fold`, `Size.lean:159`) and `X.Lawful`. (C) the Host loop re-shaped as a `Prog` tree with `Runs` paths (HOSTING-36's move for the resident), the refinement a path property that also fixes IO order: a deployed-code change to the Host's biggest module; a flag day the charter prices at zero but a lane-week of work; premises 0.

**Prior art, honestly.** breadstuffs `Proof/Refine.lean` (361 lines, 17 theorems, 0 `#guard`) closes "Exec ⊑ Abstract … by citing the proven squares of the sibling LTS modules" (`:1-40`, READ) while `Spec/ExecRefinement.lean`'s header still says the operational thread is "`-- OPEN:`-marked" (`:25-30`, READ): a stale twin of its own status (ASSUMED unresolved; not this document's job). Both are over `recCexec`/`execFullForestA`, Lean models, never the executor a node runs (memory `project-lean-must-be-the-implementation`). Nano's would be over `machine X`, which the node runs (`Serve.lean`). That is the whole difference and the reason to write it.

**My read.** B now; C only if the Host loop gains a second path or a crash bug the per-file lemmas miss. Name the theorem; keep the plants as the IO's witness.

### 2.3 Q3 · The run-level lift

**What is landed (S5):** the lift for ONE package, as `Chain` (Lang) ← `Runs` (receiver) ← `Invokes` (World), with `invokes_runs` and (INFERRED from `escrow_program_one_payout`'s name and premises, `EscrowRun.lean:401`) a `Runs → Chain`-shaped step through `judgeOne_admits`. And KERNEL-57's `law_judged` for the `law` body: both judge verdicts `.ok ()` over `(stateOf cell, stateOf cell)` with the exact lists and occasions (`Authority.lean:193-203`).

**The generalisation, in three definitions and two theorems.**

```lean
-- Lang/Proofs/LawRun.lean (moved from Ledger/Proofs/Escrow.lean:201, generalised over the law)
inductive Chain (lib : List Term) (law : Term) : Data → List (Data × Data) → Prop
  | nil (o) : Chain lib law o []
  | cons : Admits lib law rq n o → Chain lib law n rest → Chain lib law o ((rq, n) :: rest)
def Chain.last : Chain lib law o steps → Data              -- o if steps = [], else the last n
theorem chain_invariant (inv : Data → Prop)
    (hpres : ∀ rq o n, Admits lib law rq n o → inv o → inv n) :
    Chain lib law o steps → inv o → inv (Chain.last …)
theorem chain_count (f : Data × Data → Nat) (bound : Nat)
    (hstep : ∀ rq o n, Admits lib law rq n o → f (rq, n) ≤ 1 ∧ (f (rq, n) = 1 → Settled n))    -- escrow's shape
    (hsettled : ∀ rq o n, Settled o → ¬ Admits lib law rq n o) :
    Chain lib law o steps → (steps.map f).sum ≤ 1

-- Kernel/Proofs/Logic/History.lean: the World's history around one object, EVERY body kind
inductive ObjectStep (X : Ctx D) (obj : D) : World D → World D → Option (Req D × Slots × Slots) → Prop
  | frame   : admit X.env w t = .ok w' → ¬ CallFoot X c (.cell obj) → … → ObjectStep X obj w w' none
  | write   : receive X w c = .ok t → admit … → c.unsigned.body = .write obj … → <write's judge facts> → ObjectStep X obj w w' (some (r, old, new))
  | create  : … → ObjectStep X obj w w' (some (r, ∅, seed))
  | law     : law_judged's eight facts → ObjectStep X obj w w' (some (r, s, s))       -- relaw then adopt, s = s
  | invoke  : invoke_next_judged's facts → ObjectStep X obj w w' (some (r, stateOf cell, s))
  | nested  : invoke_tree_run's facts (ececba1) → ObjectStep X obj w w' (some …)
inductive ObjectHistory (X) (obj) : World D → List (Option (Req D × Slots × Slots)) → Prop   -- the Kleene star
/-- THE lift: an honest, audited log projects, at `obj`, to a Chain of Admits for every law in force. -/
theorem object_history_chain (hX : X.Lawful) (ha : audit X w l = .ok w')
    (hlaw : ∀ i, law ∈ lawsAt obj (worldAt i)) :           -- the law is in obj's law slots at every step
    ∃ steps, Chain lib (law.relocate f) (stateData w obj) steps ∧ Chain.last … = stateData w' obj
```
`object_history_chain`'s proof is `audit_ok` (fold ∧ Honest) → per step `Honest` gives `receive X w c = .ok t` →
`derive_eq` cases on `c.unsigned.body` → the landed per-body fact (`law_judged`, `invoke_next_judged`,
`invoke_next_slots`, the write analogue — ASSUMED it exists by the name `write_judged`; `law_judged` and
`invoke_next_judged` are MEASURED) → `judgeOne_admits` → `Chain.cons`; the `frame` case is `admit_Frame.cells`
at `.cell obj`. **Premises on the new theorem:** `X.Lawful` (which carries `digestOf (bytesOf l) = some l`,
LANG-46, READ), `readPackage` installed (through `judgeOne_admits`'s `hp`), `Honest` (through `audit_ok`). No
typing premise: `judgeOne_admits` takes none (MEASURED `:411-414`). **Premises on landed theorems: 0.**

**How many of the 86 become instances.** Statements: **0** change (LANG-19/K27's "the law theorems keep their
statements", READ). Roles: the **16** law×occasion theorems become the `hpres` argument of 16 one-line
run-level corollaries (`bounded_always : Chain lib (bounded S f max) o steps → ∀ (rq, n) ∈ steps, ∃ m, n.f = nat m
∧ m ≤ max`; `windowed_per_epoch`, the induction its docstring promises; `ownerSigns_always`, …); the 23 combinator
inversions and 33 clause lemmas are untouched. Ledger: `escrow_law_payout_once` becomes `chain_count` applied
to `payout_settles` + `escrow_judge_settled` (both MEASURED names, `Escrow.lean`, `EscrowRun.lean:338`);
`Runs`/`Invokes` become `ObjectHistory` restricted to `.invoke`, two instances; `invokes_runs` becomes a
corollary of `object_history_chain`. Net: 3 inductives + 2 lift theorems → 2 inductives + 2 schemes + 1 lift,
reused by every package after the first.

**The wp polarity, settled.** Breadstuffs' `wp step t Q s := ∀ s', step s t = some s' → Q s'` (`Proof/WP.lean`,
MEASURED via COMPARE §4.1) is partial correctness: failure satisfies everything (`wp_of_none`). Two
transformers are in play and they have OPPOSITE polarity, and that is correct:
- **Over the fold, wp (demonic on refusal).** `fold_keeps`, every `admit_*`, `host_run_folds`, `chain_invariant`
  are all "if it committed then". A refused turn is a `.refusal` step that changes no cell; "nothing bad
  commits" is the kernel's safety and partial correctness is its right shape.
- **Over the law, sp/total (angelic on the verdict).** `Admits` is `∃ cenv w, BigStep … (.ok (.inj "ok" w))`: a
  derivation TO `ok`. A law that faults (`stuck`, ticks, stack: `runLaw_never_stuck` shows the fault arm is live,
  `LawRun.lean:150-158`) has no such derivation and therefore no `Chain.cons`; the judge returns `.error`, the
  receiver refuses by name, and the step is recorded as a refusal, not a turn. COMPARE §4.3's finding stands:
  `Admits := wp law (· = ok)` would make a faulting law admit vacuously. **Keep `Admits` existential.**
- The tooth that pins the polarity (not landed, one line from `judgeOne_ok`, INFERRED): `fault_never_admits :
  runLaw L.lib (.get (.ref g) ℓ) od nd r = .error f → judgeOne … ≠ .ok ()`. State it; it is the "never" the brief asked for.

**Prior art.** breadstuffs `vcg_run_sound` (one lift over `Execution.Run`, over a model, 404 lines, 4 `#guard`;
COMPARE §4.1). minidregg does the SAME three-part move nano needs, at scale: `inductive Reachable config genesis
: Snapshot → Prop` (`Kernel/ObjectiveCheckpointInvariant.lean:1711`), an invariant lift (`reachable_upgradable`),
and a per-operation corollary `migrate_cannot_fail (book) (clean) (reachable : Reachable config genesis snapshot)
… : ∃ migrated, migrate config snapshot height request = .ok migrated` (`ObjectiveUpgradeInvariant.lean:3385-3397`,
MEASURED) — with 2928 `#assert_axioms` lines in `Kernel/` where nano has one census (law 6). Its law meaning is
denotational (`compile_sound : eval (compile law) before after = law.denote facts old new`, `ObjectLaw.lean:507-509`;
`package_law_enforced : admitWrite … = .ok () → ∀ law ∈ record.packageLaws, law.2.denote … = true`, `:594-596`): a
`Bool`-valued denotation, so its polarity question never arises (no faults) and its laws cannot compute. Nano's
laws run on a machine; that is why `Admits` must be existential and why the lift is worth more here.

**My read.** Build the lift as above. It is the one item in this document that changes what a package author
can STATE: today "at most one payout over the World's history" cost three inductives; after, it is `chain_count`
applied to two per-step lemmas.

---

## 3. WHAT THE LOGICS NANO LACKS WOULD BUY — honestly

### 3.1 Separation logic (ownership of cells by objects)

**Does the trie's keyed ownership already give it?** The heap half, yes. `World.trie` is a map keyed by
`Slot D = .cell c | .nullifier n`; rows by `RowSlot D = .row key | .head parent rel` (MEASURED from the
footprint constructors, `Frame.lean:32-43`). A finite map's PCM is disjoint union; `∗` over distinct keys is `∧`;
the frame rule is `admit_Frame`; two-turn disjoint commutation is `admit_comm` (READ). The one non-trivial
resource is the row HEAD counter — shared, additive (`count + insN t₁ + insN t₂`, READ 10-19 brief §2.1), a
counting permission — and K51 put it INSIDE the footprint (`RowFoot.head`) rather than modelling it as a
fraction, which is the right call for a kernel with no concurrency inside a turn.

The ownership half is NOT in the heap and separation logic would not put it there. "Object `obj` owns cell
`c`" is authority: `objectCell X owner pkg laws state` (`Derive.lean:122`), `ownerAuthority X look actor obj cell
.mutate via = .ok principal` (quoted in `law_judged`), rights `observe | mutate | invoke m | enroll n`
(`Call.lean:21-34`), grants carved from grants (`checkParent`, `Derive.lean:261`). In Iris terms that is ghost
state and a `◯`-fragment; in nano it is cells with rights in them, judged by `Authority.lean` (13 theorems,
READ 10-19 brief). The calculus it is groping toward is **capability attenuation**: `Authorizes X look actor obj
right` with a chain lemma "a grant carved from a grant confers no more" (`enrollUnits` is already monotone by
construction, `Derive.lean:243-248`, INFERRED). **ASSUMED: no `attenuation_le` theorem exists**; a lane greps
`Authority.lean` first. That is the through-line's own word ("an attenuable proof-carrying token"), and it is
worth one scheme — but it is an authority logic, not separation.

**Verdict:** do not build an assertion language or import one (no Mathlib, GATES-1). Build `CallFoot` +
`submit_frame` (§2.1 B) and, separately, name the attenuation lemma. Premises added: 0.

### 3.2 A temporal logic over the fold

The hand-rolled trace properties (MEASURED): `settle_final_never_admits (hc : w.RefusalsCanon) (hjc : w.JournalCanon)
(hv : <the receipt reads expired or refused-final>) (hf : fold X.env w l = .ok w') : ∀ out, submit X w' c ≠ .ok out`
(`Protocol/Proofs/Settle.lean:201-207`) — that is `□¬(submit ok)` from `w` over every continuation;
`submit_replayed` (`Receive.lean:162-165`) — per state, but "forever within the window" needs `journalForgets`;
`escrow_runs_after_payout` (`EscrowRun.lean:362`) — "a payout is the last run": `□` over `Runs`;
`crashLooping_antitone` (`Hosting/Proofs/Loop.lean:523`) — monotone in the clock; 47 theorems with never/once/
after/mono/antitone in the name, most of them per-step monotonicities.

What the vocabulary would be, in full (every lemma a one-liner from `fold_append`/`fold_keeps`, INFERRED):
```lean
def Always (E) (P : World D → Prop) (w : World D) : Prop := ∀ l w', World.fold E w l = .ok w' → P w'
theorem always_of_keeps (ha) (hr) : P w → Always E P w          -- = fold_keeps: □-introduction
theorem always_now : Always E P w → P w                         -- fold [] = ok w
theorem always_mono / always_and / always_idem (fold_append)
def Within (E) (k : Nat) (P) (w) := ∀ l w', l.length ≤ k → fold E w l = .ok w' → P w'   -- the window-bounded □
```
`settle_final_never_admits` becomes `Always X.env (fun w' => ∀ out, submit X w' c ≠ .ok out) w` under the same
premises; `submit_replayed` becomes `Within … windowMax` (ASSUMED the exact bound; it is `journalForgets`'s).
No `◇`: nano's kernel has no scheduler and no fairness; the Host loop is deterministic; the only liveness
results are progress theorems of the machine (`runLaw_never_stuck`, `extract_progress`) and they are not trace
properties. breadstuffs' `Proof/Temporal.lean` (400 lines, 22 theorems, 8 `#guard`, over `trajA` of a model;
header `:1-45`, READ) is the precedent and it says itself its `◇` theorems are "the trivial ones".

**Verdict:** worth ~30 lines, the day the third trace theorem is written in the `Always` shape; port nothing
from breadstuffs. Premises added: 0 (an abbreviation). Not worth a module of its own until it has three users.

### 3.3 A cost logic

Lang has one and it is good (S7): sized derivations, a potential-function amortisation, "the counter is the
derivation size". The kernel's hash counts are instruments by ruling (KERNEL-36). A kernel cost calculus would
annotate `insAt`/`getAt` with a hash count and prove `hashes (insert k v t) ≤ depth + 2`, making the WASTE row
`hashes-per-touched-cell` a theorem's measurement. **What it buys:** the regression is caught at `lake build`
instead of at the WASTE gate — timing, not strength, since both are over the same deployed code. **What it
costs:** a second, annotated copy of the trie operations or a cost monad through `Kernel/Trie.lean` (deployed
code; a hub). **ASSUMED: no WASTE row has flapped.** If one has, that is the trigger.

**Verdict:** instruments stay. Premises added: 0 either way.

### 3.4 Refinement and rely–guarantee

Refinement: §2.2. Rely–guarantee: `Honest` IS the rely (every step is the receiver's own derivation of its
event); `chain_binds`/`fold_reaches_host` are the guarantee; PROTOCOL-46 makes the client's rely on the Host
empty (READ, 10-19 brief). The missing rule is `honest_keeps (P) : (∀ w c t w', receive X w c = .ok t → admit = ok
w' → P w → P w') → … → Honest X w l → fold = ok w' → P w → P w'` — `fold_keeps` under the rely — which the lift in
§2.3 contains as its first step. One scheme, ~6 hand proofs subsumed (10-19 brief's count, READ, not re-counted).

---

## 4. THE DECISION CARDS

### Q1 · The receivers' logic

| | |
|---|---|
| **OPTIONS** | (A) the eight-conjunct `∧`-chain + `receive_congr`, as landed · (B) `structure Derived X c t : Prop` (the same eight facts, named) + `Triple`/`CallFoot`/`Indep`/`submit_frame` in `Kernel/Proofs/Logic/Triple.lean` · (C) a separation-logic assertion language over `World` with `∗` and `↦` · (D) trace-only, via `Honest` |
| **PREMISES ADDED** | A 0 · B **0 on landed** (each landed theorem is an instance by `intro`); new theorems take what `receive_ok` takes: nothing · C 0 on landed but an `Indep`-style side condition on every future assertion, and a translation lemma per S3 theorem · D `Honest` per theorem |
| **PRIOR ART** | minidregg's Prop-structures as contracts (`FillAllowed`, `Fill`, `Deposit`: `CanonicalEscrowMarket.lean:122, :239, :381`) · breadstuffs `Triple`/`wp` over `recCexec` (a model) · Calcagno–O'Hearn–Yang small-footprint semantics, which nano has BY TYPE (`Pinned D`) |
| **ROOT'S LEAN** | B. The receivers already have locality at the definition; what is missing is a name and one call-level rule. C is a second World of statements for a locality the type already enforces. |
| **RULING (one line)** | A receiver's contract is `Derived`, a Prop-structure; its frame is `submit_frame` over `CallFoot`; no assertion language, `unpinned` stays the receiver's refusal by name. |

### Q2 · `Host ⊑ Kernel`

| | |
|---|---|
| **OPTIONS** | (A) plants only (sim `same`/`reopened`) · (B) `host_step_folds` + `host_run_folds` over `(machine X).step`, total over the 6 ops by `match`, with `step_submit`/`open_sound`/`Kept`/`audit_ok` as its cases; `host_reopen_folds` for the crash edge · (C) the Host loop as a `Prog` tree with `Runs` paths (HOSTING-36's move), the refinement a path property that also fixes IO order |
| **PREMISES ADDED** | A 0 · B **0 on landed**; the new theorem takes `Kept` and `X.Lawful`, both discharged at `Deployed` · C 0 on theorems; a deployed-code reshaping of `Host/Loop.lean` (a flag day: free by charter, a lane-week by size) |
| **PRIOR ART** | breadstuffs `Proof/Refine.lean` (361 lines; over a model; its `ExecRefinement.lean` header still says OPEN — a stale twin) · l4v `proof/refine` · nano's own `interp_runs` (the resident, S6) · FSCQ/Yggdrasil for the crash edge |
| **ROOT'S LEAN** | B now. The plant sees seeded paths only (KERNEL-57's "a branch the generator cannot reach is a label"); the theorem is total over ops by construction and would have to speak for `accept`, carry, seal, `makeRoom`. C when the Host loop grows a second path or a crash bug the per-file lemmas miss. |
| **RULING (one line)** | `Host ⊑ Kernel` is ONE theorem, `host_run_folds`, over every request kind; the plants stay as the IO's witness; `CheckpointTrusted` is prose and becomes a premise only when retention lands. |

### Q3 · The run-level lift

| | |
|---|---|
| **OPTIONS** | (A) per-package hand lifts (`Chain`/`Runs`/`Invokes` × every future package) · (B) `Chain lib law` + `chain_invariant`/`chain_count` in Lang; `ObjectStep`/`ObjectHistory` (six body kinds, `frame` by `CallFoot`) + `object_history_chain` from `audit_ok`, `law_judged`, `invoke_next_judged`/`_slots`, `invoke_tree_run`, `judgeOne_admits` in `Kernel/Proofs/Logic/History.lean`; the 16 law theorems as `hpres`; escrow's three inductives as instances · (C) a term-level `wp` for laws with `Admits := wp law (· = ok)` |
| **PREMISES ADDED** | A 0 (and three inductives per package) · B **0 on landed**; the lift takes `X.Lawful`, `readPackage`, `Honest` (via `audit_ok`); no typing premise (`judgeOne_admits` takes none) · C **negative**: a faulting law would admit vacuously (`wp_of_none`'s polarity); `runLaw_never_stuck` shows the fault arm is live |
| **PRIOR ART** | breadstuffs `vcg_run_sound` (one lift, over a model; its `wp` is the FOLD's polarity, right for the kernel, wrong for a law) · minidregg `Reachable` + `reachable_upgradable` → `migrate_cannot_fail` (the same move, 2928 `#assert_axioms` lines; `Bool` denotation, so no polarity question) · nano's own `invokes_runs` |
| **ROOT'S LEAN** | B. The polarity rule in one sentence: **wp over the fold, sp over the law** — "if it committed then" for the World, "a derivation to `ok`" for the judge; `fault_never_admits` is the tooth. Zero statements of the 86 change; 16 gain run-level corollaries; `escrow_*_one_payout` becomes `chain_count` of two per-step lemmas. |
| **RULING (one line)** | `Admits` stays existential; the lift is `object_history_chain`, proved once over every body kind, with `Chain`/`Runs`/`Invokes` as its instances and the 16 law theorems as its step lemmas. |

### The order, if all three are taken (one lane each; none blocks another except as marked)

1. Q3's Lang half (`Chain`, `chain_invariant`, `chain_count`; `escrow_law_payout_once` restated) — pure Lang, no kernel dependency, half a day.
2. Q1's `Derived` + `CallFoot` + `submit_frame` — needed by Q3's `frame` case; one day.
3. Q3's kernel half (`ObjectStep`, `object_history_chain`, `fault_never_admits`; `Invokes` as an instance) — after 1 and 2; two days.
4. Q2's `host_run_folds` — independent of 1-3; one to two days.
5. §3.2's `Always` — only when the third trace theorem arrives; not a lane.

---

## 5. Corrections to the briefs, and what I could not verify

- **`Host/Proofs/Trusted.lean` / `CheckpointTrusted` do not exist in Lean** (MEASURED, grep over every source dir). The name is in one PROPOSED retention decision (`decisions/kernel.md:1867`). The brief's pointer was to a design.
- **`Hosting/Resident/*` holds no proofs**; the resident's theorems are `Hosting/Proofs/Resident*.lean` (MEASURED listing). `interp_runs` is at `ResidentRun.lean:700`, the crash relation at `ResidentVolume.lean:58`.
- The 10-19 brief's counts are stale by ~1200 theorems; its `Collision` escape is gone (KERNEL-56); its "~22 frame instances" was corrected to 3 by KERNEL-51 AS BUILT (`kernel.md:2855-2862`, READ) and its "~45 → 8 + 4" head-read fall did not happen (`:2904`, READ: "the count can only rise"). The schemes were still worth landing; the ratchet predictions were not grepped. This document's counts are grepped.
- COMPARE §4.2's "16 law×occasion theorems" I confirm by its Appendix A; my `Admits lib`-hypothesis grep finds 14 lines because two headers wrap. 86 in `Std.lean` confirmed.
- **ASSUMED, for a lane to check first:** that a `write_judged` analogue of `law_judged` exists (I did not grep `Kernel/Proofs/Authority.lean` for it); that no `attenuation_le` exists; that no WASTE row has flapped; which of the six ops move the World in `(machine X).step`; the exact window bound for `submit_replayed`'s `Within`.
- **Nothing here needs a re-genesis, a re-emit, or a changed definition** except Q2's option C (not recommended now). Every recommended item is proof-side.

### Pointers used
nanodregg @ `cdd9d84`: `CHARTER.md:14-62`; `SIZE.md`; `decisions/kernel.md` 1855-1870, 2378-2501, 2637-2645, 2866-2890;
`Kernel/Proofs/{Receive,InvokeNext,Local,Fold,Refuse,Trie,Audit,Authority}.lean`, `Kernel/Proofs/Logic/{Frame,HeadRead}.lean`;
`Kernel/Receive/{Call,Derive}.lean` (headers, def index); `Lang/Proofs/{Std,LawRun,Need,Extract,Cost,Receiver}.lean`;
`Ledger/Proofs/{Escrow,EscrowRun,EscrowInvokes}.lean`; `Host/Proofs/{Size,Deployed,Open,Serve,Log,Cli}.lean`;
`Hosting/Proofs/{ResidentRun,ResidentVolume,Loop,Resident,Residents}.lean`; `Protocol/Proofs/Settle.lean`.
breadstuffs: `metatheory/Dregg2/Proof/{WP,WPCatalog,Temporal,Refine,LTS,CTL,MuCalculus,Noninterference}.lean` (headers, defs, counts), `Spec/ExecRefinement.lean` header.
minidregg: `Kernel/ObjectiveUpgradeInvariant.lean:3378-3411`, `Kernel/ObjectiveCheckpointInvariant.lean:1711`, `Kernel/ObjectLaw.lean:505-608`, `Kernel/CanonicalEscrowMarket.lean:122-381`.
Local: `redregg/work/PROOF-TECHNIQUE-20261019.md`, `COMPARE-20261021.md` §4; memories `minted-price-premises-not-only-cost`, `minted-a-disjunct-provable-from-the-premises-is-vacuous`, `feedback-greenfield-never-price-a-regenesis`, `project-lean-must-be-the-implementation`, `feedback-prove-the-floor-false`.
