# IMPACT-E5 — receipts between Worlds: the head object, the receipt column, foreign_receipt_sound (CX-P5, 2026-10-23)

Base: nano `origin/main` = `1fc905f` (worktree `hbox:/tank/dregg-build/nanodregg/wt/p5`, clean, detached). Nothing
is built yet. Tags: MEASURED (a command or build ran), READ (file:line read this session at 1fc905f), INFERRED (my
reasoning, unchecked by a build), ASSUMED-BY-ME (a design choice the reader should challenge). Card: plan §2(a), §3 P5,
§1 B10; grant R-0051 (Protocol/**, Host/**, Kernel/Proofs/**, client/tests/**, rows/**; NOT Lang/**).

## 0. Answer first (six corrections to the card as written, each measured or read)

1. **"Same height, different roots" is not a fork in nano. The fork key is `steps`.** [READ `Kernel/World.lean:279–284`]
   A recorded refusal does not advance `height` but does advance `steps` and changes the refusals root. So two honest
   heads of A at one height can have different roots: before and after a recorded refusal. A `forkedHead` keyed on height
   would refuse a legitimate head advance. The deployed head line is already `head STEPS HEIGHT ROOTS`
   (`Protocol/Command/Machine.lean` `receiptText`, READ). The head is keyed by `steps`. X3 reads "second head of A at the
   same STEPS, different roots".
2. **The receipt column cannot be computed Protocol-side or Host-side. It is Lang's runtime applying Protocol's check,
   handed in as a parameter.** [READ] Protocol imports Lang (`Protocol/Rows.lean`, `Protocol/Command/*` import Lang;
   `git grep "^import Protocol" Lang` is empty, MEASURED). So Lang cannot call `Protocol.Receipt.check`. The decision must
   also run inside admission, because a follower re-derives every Turn (law 1, PROTOCOL-4). A check run by the Host before
   it submits is not re-run by any follower. There are two other ways to place it, and both are worse:
   - A Host-side wrapper around `Lang.program`'s `run` in `Host/Deployed.lean` would be deterministic, but it is a
     second semantics. No Lang theorem would cover it, and it would be keyed on an argument-field naming convention. That
     is the shape READ-E1 §1 refused ("a convention until something refuses").
   - Moving `Receipt.check` below Lang (into Kernel or Codec) changes `Lang.program`'s signature anyway, because it needs
     `Env` for the hash. It also makes Lang depend on receipt internals.

   So: `Lang.program` gains ONE parameter `receipts : ReceiptCheck`, an abstract `Cell → ByteArray → Except String Seen`
   (Lang half). `Host/Deployed.lean:23` passes `Protocol.Foreign.check`: decode the head object, `Receipt.ofBytes`,
   `Receipt.check` (mine). That is the `Program` pattern one level down: KERNEL declares `Program`, LANG instantiates it;
   LANG declares `ReceiptCheck`, PROTOCOL instantiates it. Followers run the same `Host.Deployed.X`.
3. **The column is E1's mechanism exactly, not a second relation and not a new primitive.** [READ `Lang/Rel.lean:160–175`]
   E1 adds a `live` field to each pinned point of a cell-keyed read, computed from `look` of the key's cell. E5 adds a
   `receipt` field to each pinned point of a cell-keyed read declared `(receipt ARG)`. It is computed from `look` of the
   key's cell (the HEAD OBJECT, any pinned cell, the same `look`) and the method's argument field `ARG` (bytes). The
   relation is the acceptor's own `heads` relation, keyed by head-object id: the TRUST ANCHORS its owner inserted. No
   foreign ROW read is needed, so **E5 does not wait on PROT-6** (plan §4 says it does; it does not: the peer read is a
   row under another object, and E5 reads a CELL through `look`, which E1 already threads).
4. **The head is an object of a generated package `Std.head`, not a data cell.** [READ `Protocol/Command/Verb.lean:344–345`]
   A data object's `write OBJ KEY VALUE` sets one slot to VALUE's UTF-8 bytes. A head is (steps, height, roots), and a
   law over raw text bytes cannot parse it (Lang's primitives are arithmetic, `beq`, `cat`, `lenLe`, `deq`:
   `Lang/Term.lean:17–26`). A package object takes `nd invoke HEAD 0 {steps=…,height=…,roots=…}`, read at the method's
   argument type by Lang's reader (`Lang/Program.lean` `argsOf`). Its law then judges the whole head in one step. The
   brief's "data cell with a Std.head-shaped law" is the right IDEA (the law is the safety, the method is convenience).
   The object form is what lets it be written in one Turn.
5. **The refusals-trie soundness half of cv 01a14dfa-200a is already LANDED.** [READ]
   `refusal_inclusion_sound` / `refusal_exclusion_sound` (`Kernel/Proofs/RefusalsHead.lean:167, :177`) and their `_sep`
   teeth (`:314, :324`) are consumed by `check_refused_sound` / `check_absent_unrefused`
   (`Protocol/Proofs/Receipt.lean:131, :160`). The module docstring (`:7–9`) and PROTOCOL-45's critique ("KERNEL states
   no refusals-trie inclusion soundness") are STALE. E5 corrects both texts and closes that half by name.
   The other half, "the World's last head link", is a `World` FIELD (`Kernel/World.lean:268–292` has `chain` and no link).
   That is Kernel source, outside R-0051. E5 also has no consumer for it: the head object holds ROOTS, which the poster's
   own fold computes in O(1). The field stays open, with its trigger: a party that holds only a chain digest (the phone,
   cv 01a14d95-36b0).
6. **cv 01a14dfa-1ffb (the Host's lookup reply carries a receipt) is NOT on E5's path. Its consumer was closed by
   PROTOCOL-46.** [READ `decisions/protocol.md:1314–1360`, `Protocol/Attempt.lean:1–45`] The Host hints and follow
   settles: the attempt store ends a call only on its own follow's `receipt CALL`. A Host that lies "not admitted" is
   already harmless, and the `settle` row's `lieLookup` fault plants exactly that lie (`Protocol/Rows.lean:161–163,
   :1323–1332`). PROTOCOL-46 §7 declined the Host half and named its trigger: "a member that holds a head but no World,
   the phone". E5's poster FOLLOWS A, and its receipts come from that follow's `receipt CALL`. A receipt the Host builds
   at its own tip would not even check against B's held head (roots differ, `headMismatch`). So no reply layout changes.
   Building the lookup receipt now would be a no-op feature (CLAUDE.md: "never keep a no-op"). Default: close
   01a14dfa-1ffb as superseded by PROTOCOL-46 §7, with the phone as its trigger (§9 Q3).

Also [READ]: `Receipt.answerOf`'s committed arm never reads the head's height (`Protocol/Receipt.lean`, the
`| .committed h td` arm checks `h < 2^64` and the journal inclusion only). So PROTOCOL-45's open item "a relayed head
must bind its height to its roots" does not touch a committed answer, which is the only answer E5 acts on (§1(c)).

## 1. The design

### (a) `Std.head`: the head object (Lang half: `Lang/StdHead.lean`, new; patch in `promo/E5/lang-half.patch`)

- **State type** (one field, one slot, so a post is one judged step):
  `{ world : digest, head : < at : {height : nat, roots : digest, steps : nat>,
                              forked : {held : digest, other : digest, steps : nat} > }`.
  `world` is A's origin, set at birth from the seed and never changed after. It is the poster's claim of which World it
  follows, read by acceptors' laws.
- **Methods `post (arg : {height, roots, steps})` and `fork (arg : {other : digest, steps : nat})`** write the state
  and DECIDE NOTHING. `post` sets `head := at arg`. `fork` sets `head := forked {held := <the held roots>, other, steps}`.
  The one decision is the law (law 1: one place decides). Every refusal below is the law's, whatever method wrote the
  state, so each has a deployed tooth through these two methods.
- **Law `head`** (judges every change, so it holds whatever method or future author writes the state). This is what
  the theorems are about:
  - `world` changed: `otherWorld`;
  - `at s` → `at s'` with `s' < s`: `staleHead`;
  - `s' = s` and (height, roots) differ: **`forkedHead`**. The only way to record a disagreement is the `forked` arm,
    and the arm must name the held roots;
  - `s' > s` with `height' < height`: `badHead` (an honest fold never lowers height);
  - `at` → `forked {held, other, steps}` admits only with `held = roots`, `steps = s` and `other ≠ roots`;
  - `forked` → anything else: `forkedHead` (frozen).
- **Authority**: the owner, plus every member the owner grants `invoke:N` on `post`. Several B members that each follow A
  can post. That is what makes `forkedHead` mean something: one poster following one log never sees two heads at one
  steps, and two posters fed different logs by an equivocating A do (§9 Q1).
- **`headView : Cell → Option HeadView`** (Lang): the cell's package slot is `Std.head`'s, and its state decodes at the
  state type. The hook uses it (§1(c)).

**DEFAULT ASSUMED-BY-ME: refuse AND record (the `forked` arm).**
- The plan's refusal stands literally. A post at the held steps with different roots is `at`→`at`, refused
  `forkedHead` (X3).
- The poster, holding the conflicting head, then records it with `fork` (admitted: `at`→`forked`, naming the held
  roots, L5). From then on the object is frozen (L3), and every receipt against it refuses `forkedHead` (P4, X3b).
- Plain refusal alone would leave the object trusting its first head. B would go on accepting receipts from a World one
  of its own posters saw equivocate, and the evidence would survive only as a refused tx id in B's refusals trie.
- The price of recording: one sum arm, one method, one hook check. The alternative is refusal only (§9 Q1).

### (b) The receipt column (Lang half: `Lang/Package.lean`, `Lang/Rel.lean`, `Lang/Program.lean`, `Lang/Read.lean`, `Lang/Print.lean`)

- `RelRead` gains `receipt : Option Label`. `(receipt ARG)` on a read of a cell-keyed relation names a `bytes` field
  `ARG` of the method's argument type, both checked at install. A `(receipt ARG)` read of a relation that is not
  `cellKeyed`, or with ARG not a bytes field, is refused at install by a wire name (READ-E1 condition 1's rule). I
  propose `badReceiptRead`; the Lang worker names it.
- `pointRecTy d live receipt` gains `receipt : {height : nat, turn : digest, tx : digest}` when `receipt = some _`.
- `readsData` / `relReads` / `pointData` gain the decoded args (already decoded at `Lang/Program.lean:401–403`, before
  `readsData` at `:404`) and the `ReceiptCheck`. For each pinned point of a `(receipt ARG)` read, with key cell `g`:
  - `look g = .error e`: the kernel's refusal `e` as is (`unpinned`), as E1;
  - `look g = .ok none` (a retired head object, which is how B's owner REVOKES a trust anchor): `.program "headDead"`;
  - `look g = .ok (some c)`: `receipts c args.ARG`. `.ok s` puts the record `s` in the point's `receipt` field.
    `.error name` refuses the run `.program name`. The first token is the name: law 7's convention for `program`
    (`Lang/Program.lean`, the resident readers' comment).
- `Lang.program (bytesOf) (digestOf) (receipts : ReceiptCheck)`. `Lang.noReceipts := fun _ _ => .error "noReceipts"` is
  for the Lang journey's own fixtures. The Lang journey gets a toy `ReceiptCheck` row (RC1–RC3: column present; a
  refusal name passes through; `headDead`), because the Lang journey cannot import Protocol.
- Wire: **NO package-wire byte moves, and no version bump.** (MEASURED while writing the patch; this corrects the
  first draft.) A method's reads are spelled by its rows argument's TYPE: `relReadShape` (`Lang/Package.lean:337–352`)
  reads a `RelRead` back from a record type. So a `receipt` field in a point record is already representable on the
  wire. It changes only what install ACCEPTS: today such a method type is refused `badMethod`, and it becomes a read.
  No stored package is reinterpreted, because none could have been installed.
  - It is still a semantic flag day. A log that recorded such an install as refused would re-fold to an admission.
    Every Store re-geneses (cheap), and the landing is `lang!` for that reason, not for a byte.
  - No surface syntax: the author writes the field in the method's rows type.
  - The argument label is FIXED: the method's argument record must have `receipt : bytes`. That is checked at install
    (`receiptRead`), together with the cell-keyed rule. The patch carries `RelRead.receipt : Bool`.

### (c) The deployed check (mine: `Protocol/Foreign.lean`, new; `Host/Deployed.lean:23`)

```
def Foreign.check (E : Env D) (dc : Stream D) (headPkg : D) : Lang.ReceiptCheck := fun cell rb => do
  let some hv := Lang.headView headPkg cell | .error "notHead"
  match hv.head with
  | .forked .. => .error "forkedHead"
  | .at height roots steps =>
    let some r := Receipt.ofBytes E dc rb | .error "badReceipt"
    match Receipt.check E height (← digest roots) r.txId 0 r with
    | .ok (.committed h td) => .ok ⟨h, dc.bytes td, dc.bytes r.txId⟩
    | .ok _ => .error "notCommitted"
    | .error e => .error e.name          -- headMismatch | pathMismatch | forgotten (otherTx is unreachable: txId := r.txId)
```

- Committed only. A `refused` answer is the World's recorded refusal (`check_refused_sound`), but it is FINAL only
  under the call's window (`settle_final_never_admits` needs `validUntil`), and the receipt does not carry
  `validUntil`. `absent` needs the call's `notBefore`. Acting on either needs an argument the column does not have. They
  refuse `notCommitted`. A refund leg (B pays back when A's leg is refused) is a later card, and its premise is the
  call's window.
- `headPkg` is the deployed `Std.head` package id. It is computed once from the generated bytes (the way the journey
  pins escrow's), and `Host.Deployed.X` closes over it.
- `Host/Deployed.lean:23`: `Codec.Deployed.ctx (Lang.program Digest.bytes Digest.ofBytes? (Foreign.check env dc headPkg))`.
  `Codec.Deployed.ctx` builds `env` from the digest codec. INFERRED: env is available without X (it is built from the
  digest codec). Settled at build.

### (d) The acceptor, for the rows (mine: `client/tests/fixtures/foreign/Accept.ob`, a hand-written package)

- State `{}`.
- `heads : {cell : digest} → {}` (cellKeyed; inserted by the owner: `trust (cell)`).
- `accepted : {tx : digest} → {height : nat}`.
- `accept (arg : {receipt : bytes})` reads `heads` with one point and `(live) (receipt receipt)`, then inserts
  `accepted[column.tx] := {height := column.height}`.

This is LPCFS's certificate monitor in one Turn [READ REOR A.9/B.9]:
- revocation is the head object being live (`headDead` once the owner retires it);
- the certificate is the verified receipt;
- use-once is the `accepted` insert (a second insert of the same key refuses).

All three are under one `receive`, by construction (C9's reading, LANG-75.2). This is a fixture, not a generator: the
Std package that would carry it waits for a consumer beyond the rows.

### (e) The two Worlds in the rows (X1–X3, mine: `client/tests/foreign.rs`, from `client/tests/join.rs:112`'s harness)

- **World A**: `host genesis` (nonce a), served; founder alice.
- **World B**: `host genesis` (nonce b), served; founder bob.
- Bob joins A from alice's invitation (join.rs's honest join) and follows A. Carol is enrolled in B and also follows A.
- In B, bob installs `Std.head` (`world/head/Head`, the printed generator text, Lang half) and `Accept`, creates
  `H := Std.head {world := A's origin, head := at <bob's A-follow head>}`, grants carol `invoke:4` on H, creates `ACC`,
  and runs `trust H`.

Rows:
- **X1** alice in A: `write @offer 1 terms` (her call c, txId t). Bob gives alice's frozen bytes to his A-follow:
  `receipt CALL` prints `receipt R`, `head S HT ROOTS`. Bob in B: `invoke H 0 {steps=S,height=HT,roots=ROOTS}`, then
  `invoke ACC 1 {receipt=R}`: **admitted**, and `read ACC accepted 1` shows `t`.
- **X1b** the same `accept` again: refused (the `accepted` row exists; the name is the kernel's row-insert refusal,
  MEASURED at build).
- **X2** R with one byte of its journal path changed: **refused `program` pathMismatch** (hint line).
  - X2h: a receipt for t built at a LATER head of A while H still holds S: `headMismatch`. The client re-fetches at
    H's head.
  - X2c: a receipt for a call that never reached A: `notCommitted`.
- **X3** carol posts `{steps=S, height=HT, roots=<different>}` through her grant: **refused `lawDenied`
  (`head: forkedHead`)**. H is unchanged (`read H` shows bob's head).
- **X3b** carol records it: `invoke H 1 {steps=S, other=<different>}`: admitted (`forked`). Then:
  - bob's `accept` with the X1-valid receipt: **refused `program` forkedHead**;
  - bob's `post` at S+1: **refused `lawDenied` (`head: forkedHead`)** (frozen).
- **X4** (plan §7's control): alice's A-call bytes submitted to B's host: **refused wrongWorld**.
- **X5** (revocation): bob retires H, then `accept` with a fresh valid receipt: **refused `program` headDead**.

The Worlds changed per Turn (the plan §2 refuter): X1 changes A (alice's write), then B (post), then B (accept). Every
row is one World per Turn. No row needs two Worlds atomically, so the refuter does not fire and P6 does not move ahead
of P5. [INFERRED from the row list; each row is one `nd` call against one host.sock]

## 2. Every touched name across the layers [MEASURED `git grep -c` at 1fc905f, `.lean`]

`Lang.program` / `program bytesOf` instantiations gain the `receipts` argument. Each is a BINDER or an instance, never a
hypothesis:

| layer | files (occurrences) | owner |
|---|---|---|
| Lang | Call 1, Journey/Contextual 1, Journey 5, Proofs/Call 3, Proofs/LiveClosed 1, Proofs/Provenance 5, Proofs/Rel 4, Proofs/StdActivityMonitor 3 | Lang worker (patch) |
| Ledger | Proofs/EscrowAdmitted 4, EscrowInvokes 2, EscrowRun 11, EscrowWitness 8, GrantCapTooth 1, Sim/Journey 2 | **ASK: cross-layer LEDGER grant** (binder only) |
| Hosting | Proofs/Deployed 2, Sim/Allowance 1, Sim/Journey 2 | **ASK: cross-layer HOSTING grant** (binder only) |
| Kernel/Proofs | InvokeTreeWitness 6, InvokeWitness 7, Logic/History 4, Logic/HistoryWitness 5 | mine (R-0051) |
| Host | Deployed 1 | mine |
| Protocol | Rows/Params 1 | mine |

`relReads` / `readsData` / `pointData` / `pointRecTy` / `relReadTy` / `RelRead`: the Lang worker greps these (Lang only;
E1's table `E1-grep-base.tsv` is the precedent). `Receipt.*`: no definition changes. `Protocol/Proofs/Receipt.lean`
gains theorems, and its docstring changes (§0.5).

The deployed-ctx theorems that name `Codec.Deployed.ctx (Lang.program Codec.Digest.bytes Codec.Digest.ofBytes?)`
literally are `Lang/Proofs/Provenance.lean:1244`, `Ledger/Proofs/EscrowInvokes.lean:104` and
`Ledger/Proofs/EscrowRun.lean:315`. Lang and Ledger cannot import Protocol, so they QUANTIFY over `receipts` (a
binder). `Host.Deployed.X` instantiates it. Each stays a theorem about the deployed ctx at every `receipts`, which
includes the deployed one. No theorem becomes silently about a non-deployed ctx: there is no default argument, by
design (minted: gating defaults to silence).

## 3. The theorems AS STATEMENTS, each with its nano object and the deployed mutation that falsifies it

### 3.1 Lang half (in the patch; `Lang/Proofs/StdHead.lean`, `Lang/Proofs/Rel.lean`)

- **L1 `receipt_column_authenticated`** (sibling of `cited_authenticated`, `Lang/Proofs/Rel.lean:340`). Object:
  `Lang.relReads`.
  `relReads digestOf rc look rv self i ℓ d x args = .ok v → x.receipt = some a → ∃ ps rest, v = .record (slotsD "p"
  x.points ps ++ rest) ∧ ∃ hlen, ∀ j hj, ∃ k b g c s, keyOf … = .ok k ∧ keyCell k = some b ∧ digestOf b = some g ∧
  look g = .ok (some c) ∧ args.field a = some (.bytes rb) ∧ rc c rb = .ok s ∧ (ps[j]).field "receipt" = some (seenData s)`.
  Mutation: `pointData` fills `receipt` from the receipt's own STATED answer without calling `rc` (a relay's
  `trustReceipt`). False at any receipt `rc` refuses.
- **L2 `forked_head_refused`**. Object: the generated law `Std.head.head` run by `runLaw` (`Lang/Law.lean:27`).
  `o.head = at ⟨h, R, s⟩ → n.head = at ⟨h', R', s⟩ → (h, R) ≠ (h', R') → runLaw lib headLaw o n r = .ok (.error
  "forkedHead")`.
  Mutation: the law compares `steps` only (admits any roots at equal steps). False at X3's pair.
- **L3 `forked_head_frozen`**. `o.head = forked .. → n ≠ o → runLaw … = .ok (.error "forkedHead")`.
  Mutation: the forked arm admits a return to `at`.
- **L4 `head_advances`**. `runLaw … = .ok (.ok ()) → o.head = at ⟨h,R,s⟩ → n.head = at ⟨h',R',s'⟩ → s ≤ s' ∧ (s = s'
  → (h,R) = (h',R')) ∧ h ≤ h'`.
  Mutation: drop the `staleHead` clause. False at `s' < s`.
- **L5 `head_fork_names_held`**. Admitted `at ⟨h,R,s⟩ → forked ⟨held, other, s'⟩` implies `held = R ∧ s' = s ∧ other ≠ R`.
  Mutation: the arm admits any `held`, so a poster can "record" a fork against roots the cell never held.
- **L6 `world_fixed`**. Admitted change implies `n.world = o.world`.
  Mutation: drop `otherWorld`.

### 3.2 Mine (Protocol/Proofs, Kernel/Proofs)

- **P1 `fold_journal_turn`** (`Kernel/Proofs/Journal.lean`, new). Object: `World.fold`'s journal. Stated against the
  WORLD, never a relayed claim:
  `World.fold E w l = .ok w' → w.JournalCanon E → w'.journalAt E k = some e → w.journalAt E k = some e ∨ ∃ l₁ t l₂ v
  v', l = l₁ ++ .turn t :: l₂ ∧ World.fold E w l₁ = .ok v ∧ World.admit E v t = .ok v' ∧ t.txId = k ∧ e = (v.height + 1,
  turnDigest E t)`.
  From `genesisWorld` (empty journal, `genesisWorld_journalOk`) the left disjunct is impossible. The corollary
  `reached_journal_turn` drops it.
  Mutation: `commit` writes the entry at the height BEFORE the turn (`w.height`). False at the first admission.
  (`commit_journal_mem`, `Journal.lean:110`, is the per-step lemma it folds.)
- **P2 `foreign_receipt_sound`** (`Protocol/Proofs/Foreign.lean`, new). Object: `Foreign.check` (the deployed column).
  `Lawful E n → 0 < n → World.fold X.env (genesisWorld X name nonce a fs) l = .ok wA →`
  `Lang.headView headPkg cell = some ⟨world, .at ⟨h₀, rootsB, s₀⟩⟩ → digestOf rootsB = some (wA.roots X.env) →`
  `Foreign.check X.env dc headPkg cell rb = .ok ⟨h, tdB, txB⟩ →`
  `(∃ l₁ t l₂ v v', l = l₁ ++ .turn t :: l₂ ∧ … ∧ X.env.bytes t.txId = txB ∧ h = v.height + 1 ∧ X.env.bytes (turnDigest X.env t) = tdB)`
  `∨ CollidesAmong X.env.hash ([rootsPre …, wA.rootsPre …] ++ inclPres (journalSpec …) … r.jpath wA.journal)`.
  - The collision list is EXPLICIT: `check_committed`'s, the census-safe `CollidesAmong hash S` form (minted 10-20:
    a disjunct provable from the premises is vacuous; this one names its list).
  - **The premise is named, not hidden: head freshness/honesty.** "The held head is the head of a fold of A from A's
    genesis" (`digestOf rootsB = some (wA.roots …)` with `wA` folded from `genesisWorld`). Nothing in B can prove it,
    because A's operator can fork A and B holds A head, not THE head. It is the thin-member trust of PROTOCOL-42's
    critique. `forkedHead` narrows it only to "no two posters to this object disagreed at one steps".
  - Mutation: drop the `rootsDigest … ≠ roots` comparison in `Receipt.check` (plan B10's tooth). A receipt with
    fabricated roots and a self-consistent fabricated journal path then checks, and the statement is false (the forged
    entry is in no fold of A).
- **P2′ `foreign_run_sound`** (the composed statement over B's admission). It composes L1 and P2: a deployed run
  (`Host.Deployed.X.program.run … = .ok _`) of a method with a `(receipt ARG)` read on point `g` ⇒ P2's conclusion for
  `look g`'s cell and `args.ARG`. Mutation: L1's or P2's.
- **P3 `forged_receipt_refused`**. Object: `Foreign.check` / `Receipt.check`.
  `… wA as P2 … → Receipt.ofBytes E dc rb = some r → r.txId = tx → rootsDigest E r.root r.jroot r.rroot r.rowsroot =
  wA.roots E → r.answer = .committed h td → wA.journalAt E tx ≠ some (h, td) → Foreign.check … cell rb = .error
  "pathMismatch" ∨ CollidesAmong E.hash (explicit list)`.
  "A relay cannot change the entry." Mutation: `answerOf`'s committed arm skips `verifyInclusion`. False: X2 admits.
  (Distinct from P2's mutation: with P3's mutation the roots are still compared.)
- **P4 `forked_head_column_refused`**. `Lang.headView headPkg cell = some ⟨_, .forked ..⟩ → Foreign.check … cell rb =
  .error "forkedHead"`. Mutation: the hook ignores the forked arm.
- **P5 `receipt_ofBytes_bytes`** (cv 01a14ef0-ffe7). Object: `Protocol.Receipt.bytes` / `ofBytes`.
  `LawfulOn PD dc → ReceiptFits PD r → bytes E dc r = some b → ofBytes E dc b = some r`, where `ReceiptFits` is every
  digest in `PD` and both paths `ProofFits` (`Codec/Proofs/TrieProof.lean:46`).
  `build_fits`: a receipt `build` makes from a JournalCanon, RefusalsCanon World fits (via `prove_fits`), so
  `ofBytes (bytes (build …)) = some (build …)`.
  `receipt_bytes_canonical`: `ofBytes E dc b = some r → bytes E dc r = some b`, from the frame's and the proof codec's
  `decode_eq_ok_iff`, PROVIDED the frame codec is lawful on its domain (INFERRED; settled at build).
  Tooth `receipt_member_dropped`: a closed instance. The deployed bytes of a `refused` receipt with the member field's
  last byte dropped do not decode (`ofBytes = none`), by `native_decide` + `#assert_compiled` (the compiler is the
  only reach for the deployed digest codec; CLAUDE.md's Lean rule, a named theorem, not a `#guard`).
  Mutation: `ofBytes` reads the refused arm's member as the turn field's default. The round-trip is false.

### 3.3 Landed, consumed, texts corrected (no statement change)

`refusal_inclusion_sound`, `refusal_exclusion_sound` (`Kernel/Proofs/RefusalsHead.lean:167, :177`), `check_committed`
(`Protocol/Proofs/Receipt.lean:43`), `check_refused_sound` (`:131`), `check_build_reached` (`:342`). Docstring fixes:
`Protocol/Proofs/Receipt.lean:7–9` (the refused arm IS sound through `RefusalsHead`), and `decisions/protocol.md`
PROTOCOL-45 critique (an `Amended by PROTOCOL-<n>` line, no rewrite of the old entry).

## 4. The rename map

None. New: L1–L6, P1, P2, P2′, P3, P4, P5 (+ `build_fits`, `receipt_bytes_canonical`, `receipt_member_dropped`,
`reached_journal_turn`). RESTATES-MEANING: none expected. The binder ripple (§2) is `RESTATES:` lines whose statement
gains one universally quantified `receipts` binder. GATES-20t (R-0034) treats a gained binder as a changed statement,
so each is a `RESTATES:` line, listed at build from the census diff. DELETES: none.

## 5. The premise price

- **Landed theorems gaining a HYPOTHESIS: 0** (INFERRED; MEASURED by `gates/decls.py` at build). The ripple is one binder.
- The new theorems' own premises: P2's head honesty (named above) and `Lawful`/`0 < n` (as `check_committed`).
- Kernel: 0 lines of `Kernel/*.lean` source.

## 6. Wire and flag day (say what breaks)

- **Package wire: unchanged** (see §1(b), MEASURED). The landing is still `lang!`: install accepts a type it refused
  before, so an old log can re-fold differently. Every Store re-geneses; no `world/*` byte moves.
- **Call codec: unchanged.** The receipt is an argument (bytes inside `invoke`'s args). No `Receive.Body` constructor;
  call kinds stay 13.
- **Host/Protocol reply layouts: unchanged.** No lookup change (§0.6). `receipt CALL`'s output is already
  `receipt HEX / head STEPS HEIGHT ROOTS / settle V`.
- `Host.Deployed.X` changes (the program gains the deployed check). Its consensus behaviour changes only for packages
  that declare `(receipt …)`, and none exist before this landing. With the version bump every Store re-geneses anyway.
- Landing kind: `lang!` for the Lang half (the Lang worker). Then mine: `protocol:` (new modules, `Host/Deployed.lean`,
  tests), on top of it. INFERRED: no `host!`, because no Host byte moves.

## 7. Plants (each run on the WHOLE tree; each must red only its own theorem/row by name; whole outputs to `promo/E5/`)

| plant | edit | must red |
|---|---|---|
| PL1 | `Receipt.check`: delete the `rootsDigest … ≠ roots` comparison | P2 (proof breaks); a forged-roots receipt row X2r admits → RED |
| PL2 | `answerOf` committed arm: drop `verifyInclusion` | P3; X2 admits → RED |
| PL3 | (Lang) `headLaw` compares `steps` only | L2; Lang journey head row; X3-law row |
| PL4 | `Foreign.check` ignores `forked` | P4; X3b admits → RED |
| PL5 | `pointData` reads the stated answer, never calls `rc` | L1; X2 admits |
| PL6 | `ofBytes` refused arm drops the member (reads `turn` as empty) | P5 |
| PL7 | the column ignores `look g = .ok none` (retired H) | X5 admits → RED |
| PL8 | `commit` journals `w.height` | P1 |

## 8. ASK (my grant is R-0051; these are outside it)

1. **The Lang half to the Lang worker**: `promo/E5/lang-half.patch`. It is written after this file, compile-checked in
   a SCRATCH worktree `wt/p5-lang` that I never land from (MEASURED when I report it).
   - `Lang/StdHead.lean`, `Lang/Proofs/StdHead.lean` (L2–L6), and `Lang/Print.lean` (print `world/head/Head`).
   - `RelRead.receipt`, `pointRecTy`, `relReads`/`pointData`/`readsData` args + `rc`, `Lang.program`'s parameter, and
     `Lang.noReceipts`.
   - The reader/printer syntax `(receipt ARG)`, the install check `badReceiptRead`, L1, the binder ripple in the 8 Lang
     files, `packageWireVersion` 6, and the codec vectors.
   - Journey rows RC1–RC3 and HD1–HD4 (the head law's four refusals over `runLaw`).
   - `world/head/Head`: the generated text, byte-for-byte as `world/escrow/Escrow` is.
2. **Cross-layer binder grants**: LEDGER (`Ledger/Proofs/{EscrowAdmitted,EscrowInvokes,EscrowRun,EscrowWitness,GrantCapTooth}.lean`,
   `Ledger/Sim/Journey.lean`) and HOSTING (`Hosting/Proofs/Deployed.lean`, `Hosting/Sim/{Allowance,Journey}.lean`): add
   one argument per instantiation, no statement otherwise changed. Either to the Lang worker as part of its `lang!`
   (one landing, the tree stays green: the signature change and its ripple must land TOGETHER), or to me after it. I
   ask that it go to the Lang worker: a signature change that lands without its ripple is a red umbrella.
3. **decisions/protocol.md** text: `PROTOCOL-<next>` (E5) with critique and meta-critique, and the PROTOCOL-45
   amendment line. `decisions/**` is not in R-0051.
4. **cv dispositions** (ROOT's to record):
   - 01a14dfa-200a: refusals half closed (landed); last-link half stays, with the phone trigger.
   - 01a14dfa-1ffb: superseded by PROTOCOL-46 §7, with the phone trigger.
   - 01a14ef0-ffe7: closed by P5.
   - 01a14de7-224a: its protocol half is closed by PROTOCOL-61 (carried invitations sign the origin; READ
     `decisions/protocol.md:1928–1995`). The residue is CLIENT's: `nd --join` has no `IN` argument, so a carried A cannot
     be joined by `nd`. E5's rows use a genesis A and do not depend on it.

## 9. Reader questions (defaults first)

- **Q1 refuse-and-record (default) vs refusal only, for a second head.** Default: X3 is refused `forkedHead`, and
  `fork` records the disagreement and freezes the object (X3b). Alternative: refusal only (the plan's text, one method
  fewer). Then B keeps accepting receipts after an equivocation one of its posters saw.
- **Q2 committed-only column (default) vs the full answer.** Default: committed only, because the other answers need
  the call's `validUntil`/`notBefore`, which the receipt does not carry. The alternative carries
  `(receipt ARG NOTBEFORE VALIDUNTIL)` and presents `refused`/`absent` with their settlement (`Settle.ofReceipt`). The
  trigger is the first refund leg.
- **Q3 close 01a14dfa-1ffb as superseded (default) vs build the lookup receipt.** §0.6.
- **Q4 trust anchors as the acceptor's `heads` rows (default) vs a fixed head id in the acceptor's state.** Rows let an
  owner trust several posters' head objects, and retire one by retiring the object. State is one anchor and smaller.
- **Q5 the hook as a `Lang.program` parameter (default) vs moving `Receipt` below Lang (Kernel/Codec).** §0.2. Both
  change `Lang.program`'s signature, so the ripple is the same. The parameter keeps the receipt's owner PROTOCOL.

## 10. Size (INFERRED)

Lang half: ~+450 (StdHead 150, proofs 200, Rel/Package/Program/Read/Print 60, journey 40) plus the binder ripple of
~±60 lines. Mine: Foreign 60, Proofs/Foreign 180, Proofs/Receipt +150 (round trip), Kernel/Proofs/Journal +80 (P1),
client/tests/foreign.rs ~350, Accept.ob 30. Theorems: +6 (Lang) +9 (mine) = 15. The plan's 25 assumed a separate
refusals-trie theorem set that already exists. Host closure: +1 module (`Protocol/Foreign`) if `Host.Deployed` imports
it: 89 → 90.

## 11. Gate after RELEASE

Mine, after the Lang half lands:
- `lake build` of my modules (`SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build`).
- `codec-vectors --check`.
- `cargo nextest run -p nanodregg-client --test foreign` (FILTERED to the new test) plus `--test join` (the harness's
  own test) as the control.
- The plants PL1, PL2, PL4, PL6, PL7, PL8 (whole outputs).
- `gates/check.py`, then `scripts/commit` (detached, `logs/p5-land1.pid`, foreground-wait, whole log read) as
  `protocol:` with `RESTATES:` lines for the Kernel/Proofs binder ripple, if any remain mine.

Bar: plan §7 runs `scripts/bar.sh` after P5. That is ROOT's run, after both landings.

## BUILT (2026-10-23, after R-0059; scratch `hbox:/tank/dregg-build/nanodregg/wt/p5-lang` at 1fc905f; nothing landed)

The patch set is `promo/E5/full.patch`: 51 files, +1610/−339. It applies clean on main `b4a7f38`, and no file new on
main since 1fc905f names a rippled function (MEASURED: `git apply --check`, plus a grep of the 19 changed files).
Every item below is MEASURED unless tagged.

- **Whole tree GREEN**: `lake build`, 733 jobs (`logs/p5-lang-whole2.log`).
- **`lang-journey` GREEN and byte-identical** to `promo/PROT2/journey.txt` (799 lines; `promo/E5/journey.txt`).
- **`codec-vectors` ok**: no wire byte moved. That corrects §1(b)'s first draft and the read's §4 version bump.
- **gates/check.py**: closure, refusals, size_limit, paths, runs, rebase, tcb, vectors, waste and targets are ok. `size` is
  red only for the commit-message SIZE lines; scripts/commit regenerates SIZE.md.
- **Theorems (0 sorry)**: L1 `receipt_column_authenticated`, plus the range-row arm (`receiptRow_conforms`,
  `receiptRows_conforms`, `receiptRows_digests`, `receiptSeen_ok`); L2+L4 `head_at_at`, L3 `head_forked_frozen`,
  L5 `head_at_fork`, L6 `head_world_fixed`; P1 `fold_journal_turn`; P2 `foreign_receipt_sound`;
  P3 `forged_receipt_refused`; P4 `forked_head_column_refused`; P5 `ofBytes_bytes`.
  - Not built: `build_fits`, `receipt_bytes_canonical` and the `receipt_member_dropped` tooth. The cv 01a14ef0-ffe7
    round trip is `ofBytes_bytes`; the tooth is owed.
- **The statement diff** (`promo/E5/statement-diff.txt`, my census-style digest of wt/p5 against wt/p5-lang):
  - 101 changed theorems. Of these, 89 are user declarations, listed as `RESTATES-MEANING` in `promo/E5/restates.txt`.
  - 2 vanished, both generated `match_on_same_ctor` of `CheckError`. CheckError gained `receiptRead`.
  - 39 new.
  - Meaning changes beyond the binder: `cited_authenticated` (C0), `relReads_points` (pinD's receipt arm) and
    `pointData_ok` (a third disjunct).
  - The witness theorems now name `Lang.noReceipts`. The deployed-ctx witnesses (`escrow_runs_witness`,
    `escrow_second_release_refused`, `escrow_link_bites`, `deployed_program_own_codec`) hold for EVERY `receipts`.
  - INFERRED: no landed theorem gained a hypothesis. The added items are binders, plus an `args`/`ad` argument
    inside hypotheses that already existed. The landing's `gates/decls.py judge` is the measurement.
- **Rows**: `client/tests/foreign.rs` passes (X1, X1b, X2, X2h, X3, X3b, X5) over two geneses and two writers (`logs/p5-x2.log`).
- **Plants**, whole logs in `logs/p5plants/`. Each reds its own row, and the control is GREEN after restore:

  | plant | edit | result |
  |---|---|---|
  | PL1 | roots comparison dropped | X2h passes the check (refused only by the use-once row, `keyTaken`) |
  | PL2 | journal inclusion dropped | X2 admitted |
  | PL3 | head law compares steps only (`world/head/Head` re-emitted under the plant) | X3 admitted |
  | PL4 | the check ignores `forked` | X3b names `notHead` |
  | PL5 | the column filled without calling the check | X2 admitted |

  One more measured fact: a head object of another package is `notHead`. When world/head/Head was not re-emitted,
  the plant's changed package id refused every receipt.

**Corrections to this file, measured during the build:**
1. **No wire bump.** Reads are spelled by the rows TYPE (§1(b), §6 corrected above).
2. **`nd` cannot pin a POINT read.** `Machine.derivePins` pins only the cells a derivation asks for and the rows the
   kernel names `rowUnpinned`, and `nd invoke` has `--range` only. So E1's `live` points and a point receipt read are
   reachable from the Sims and not from `nd`. Consequences:
   - the receipt column also covers RANGE rows (`receiptRows`, `rangeRowTy`);
   - the fixture reads `(heads (range 1 1) (receipt))` signed with `--range heads 1 (record (cell #H))`;
   - a `--pin` for point reads is a separate card (Machine.lean), with the trigger "the first deployed point read".
3. **The X rows that `nd` cannot drive**: X4 `wrongWorld` is the existing `Protocol.Rows.wrongWorld` row. `headDead`
   (retire an object) and `notCommitted` (a call never sent) have no `nd` verb, and their teeth are definitional.
   X5 is the anchor withdrawn (`untrusted`).
4. **`seenOk` became `seenFits : Seen → Bool`**, so the def module exports no Prop (closure C3). `headSt`, `atRec`
   and `forkRec` moved to `Lang/StdHead.lean`.
5. **Lang journey rows HD/RC are not built.** The law's four refusals are evaluated in `logs/p5scratch/HeadEval.lean`
   and covered by L2–L6 plus X3/X3b. A journey row would add closed-instance teeth for `headDead` and `notCommitted`.
   Owed: the Lang worker decides at the landing.
