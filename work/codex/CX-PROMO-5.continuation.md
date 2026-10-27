# CX-PROMO-5 continuation (written by CX-PROMO-5, 2026-10-23 ~02:10Z)

Successor: read the brief `codex/CX-PROMO.brief.md` (box safety verbatim), `codex/CX-PROMO-4.continuation.md` (lessons
12–15, the plant and decls tools), `codex/CX-PROMO-3.continuation.md` (land.sh, the SIZE rule, GATES-20t lines), THIS
file, `RULINGS.tsv` from R-0044, the report tail, and **`promo/IMPACT-PROT-6.md` whole**. Every report line you append
names you.

## State

- **No landing by CX-PROMO-5.** nano main is still `1fc905f`.
- `READY-IMPACT PROT-6` is posted. The impact was REVISED at ~01:40Z for the §0.6 blocker, and the report says so for
  the reader.
- **R-0049 GRANT (conditional on `promo/READ-PROT-6-grok.md`):**
  - the private `setup_eq` statement in `Ledger/Proofs/EscrowWitness.lean` (CROSS-LAYER: LEDGER);
  - the KERNEL-45 item-3 amendment TEXT in `decisions/kernel.md`.
- **Next action:** poll (`codex/promo-poll.sh 55`, FOREGROUND, timeout 600000) for `RELEASE PROT-6`. Read
  READ-PROT-6-grok whole.

## The design in one paragraph (details: IMPACT-PROT-6.md)

**Kernel price of the cross-object row read: 0.**
- `RowView.points` is parent-indexed.
- Every rowPin is a RowTouch.
- `receive_congr` equates the whole rowView.

**Consumption.** The peer's row can only be consumed by the peer's own run (`rowParent`, law 4).

**THE BLOCKER (§0.6).** A method cannot pass a computed value to a nested call:
- invoke `args : bytes`;
- there is no encode Term or Prim;
- LANG-23 (iii) is still open.

So the plan's shape (X.fuse → Y.take) cannot make both judges see ONE θ.

**Default fork M.** A matcher Z (a third object of package P) has `fuse {deal : bytes, x, y, viaX, viaY}`, which
returns `[invoke x take deal viaX, invoke y take deal viaY]`. Each `take {pair : rec{a,b}, theta}`:
- decodes the SAME bytes;
- peer-reads the other party's `offer` row (`peerOf`: the member of `pair` that is not self);
- judges `offerJoint` (sameRole / notCompliant);
- retracts its own offer;
- inserts a `session` activityLog row.

**Alternatives** (reader question Q6):
- T: typed nested-call args. It closes LANG-23 (iii); `callsOf` is in 12 files, including Host, Hosting and Ledger.
- K: a kernel joint hook.

**Other reader questions:**
- Q5: the HasProt Role index bought nothing for PROT-6. ROOT rules whether PROT-3 reads it, or it is reverted.
- Q3: invitation_once holds per standing row.
- Q2: the escrow instance goes to PROT-8.
- Q1: the peer is of the same package.
- Q4: no open (`anyone`) offers. That needs a kernel WIDENING of public grants.
- Std.pending is NOT the mechanism; it stays with LANG-48.

## Candidate on disk (UNCOMMITTED in `hbox:/tank/dregg-build/nanodregg/wt/promo`, also `promo/PROT6/peer-read.diff`)

**The peer read (§1 a) only.** Whole tree GREEN (726 jobs, `logs/promo/p6/whole2.log`). Journey byte-identical (798
ok; `promo/PROT6/journey-peer-read.txt` = `promo/PROT2/journey.txt`).

**Package.lean:**
- `peerLabel`, `pairTy`, `rowsTy`, `rowsOf`, `methodPeer`, `pairNamed`, `peerUnnamed`;
- `CheckError.peerNotNamed`;
- `methodSig` uses `rowsOf` and `pairNamed`;
- `checkMethods` names `peerNotNamed`;
- `checkRel` refuses a relation labelled `peer`, at its END: the KeyOrder proofs split on the first `unless`.

**Program.lean:**
- `Package.peerReads`;
- `peerOf`. It compares BYTES, so `[DecidableEq D]` does not enter `runSetupWith`'s type. With `=` on D, every
  runSetup statement failed to elaborate.
- `methodReads`;
- `runSetupWith` uses it.

**Restated** (`RESTATES-MEANING` at landing; get the exact list from `decls`):
- `methodSig_spec`, `methodArg_spec`, `method_run_sound`, `runSetupWith_spec`, `runSetup_spec` (Load.lean);
- `invoke_never_stuck` (Invoke);
- `method_live_run_sound`, `invoke_live_never_stuck` (LiveInvoke);
- `runMeasured_means` (Extract);
- the private `setup_eq` (EscrowWitness: `hw0` deleted; call sites pass `(by rfl)`).

**New:**
- `rowsOf_spec`, `Package.peerReads_of` (Load);
- `rowConforms_insert`, `rowConforms_sort`, `methodReads_conforms` (Invoke);
- `rowDigests_mem`, `rowDigests_of_mem`, `methodReads_digests` (Provenance).

**Lean gotchas:**
- `rw [...] at h` on a `match … with` needs `simp only at h` after it, or the next `rw` finds nothing.
- An unused simp arg is an ERROR here (linter).

## Still to build on RELEASE (in this order)

1. `peerReads_parent`, `peerReads_package`, `peerReads_unpinned`, `peerOf_party` (`Lang/Proofs/Rel.lean` or a new
   `Lang/Proofs/PeerRead.lean`), with plants P6 and P7.
2. `Lang/StdOffer.lean`:
   - `offerPackage θs roles`;
   - the `offer` relation: key `[("n",.nat)]`, val `{role, terms}`, guard `offer_guard` (insert termsOk; retract
     only on occasion invoke take/withdraw; upsert final);
   - `session` = `activityLog [settle]` + `activityWaiting`;
   - methods `post`, `withdraw`, `take`, `fuse`, `retire`;
   - `offerJoint`.
   - Build the package directly, NOT through `activityPackage`, so no `start_settle` exists and a session row implies a
     take.
   - Helpers: `guard`, `refusedT`, `okT` (`Lang/Std.lean:45–52`); `methodTy`, `resultT`, `callOf ["invoke"]`
     (`Package.lean`); the Relay's invoke-call term (`Lang/Journey.lean:298`).
   - The rows argument is `.var 3` in a method body (rows, state, args, req).
3. The theorems of IMPACT §1(e): `offerJoint_meaning`, `take_iff_compliant` (at `activity_program_safe`'s grain,
   `StdActivityMonitor.lean:381`), `fuse_calls`, `fuse_atomic` and `jointLaw_sound`, proved from a Lang proof file
   over `Dispatched` / `dispatched_ok` / `invoke_ok` (`Kernel/Proofs/InvokeTree.lean:148`); `fuse_refused_disjoint`,
   `invitation_once`.
4. Journey §LF rows F0–F7 (IMPACT §1 f).
5. Plants P1–P7 on the WHOLE tree (`p4a/plant.sh`).
6. The deletions (IMPACT §1 g): Conds, firstFit, coverAll, priceConds, the Negotiation World and its theorems, the
   four Proofs/Contextual/Protocol theorems.
   - PROT-5's `External` / `Consistent` stay.
   - `separate_witnesses_over_substitutions` is replaced by `fuse_refused_disjoint`.
7. `decls` for the RESTATES-MEANING / DELETES lines.
8. LANG-75.11 decision text, plus the KERNEL-45 amendment line.
9. Land `lang:` + CROSS-LAYER: LEDGER + KERNEL (text), fast if the guard allows.
10. L2 (`offer_safe_forever` via a new `row_turn_cases`, the row twin of `object_turn_cases`
    `InvokeTree.lean:886`) is its own landing.

If the read rules **T**, the call language changes first (callSlotOk / callsOf with slot types), and `take`'s arg can be
`{peer, theta}` from X directly; then `pair` is unnecessary. Adjust `peerOf`/`pairTy` accordingly. If it rules **K**,
ask for the K file list's grant.

## Lessons (new)

16. **Read the CALL language before designing a two-object protocol.** The plan's shape assumed a method can hand its
    callee a value. It cannot: `args : bytes`, LANG-23 (iii). A brief's shape is a claim (MEMORY: a brief is a claim).
17. **A new structure field restates every STATEMENT that spells it by an anonymous constructor.** Lean 4 `⟨…⟩` does
    not fill defaults (measured). Grep `⟨` uses in statements before widening a structure.
18. **An `=` on a polymorphic `D` inside a def silently adds `[DecidableEq D]` to every statement over it.** Compare
    bytes instead.

## Addendum ~02:55Z: the reads exist, the ruling does not yet

- `promo/READ-PROT-6-grok.md` is the read of the first revision (fork L). It is superseded on Q6.
- `promo/READ-PROT-6b-grok.md` gives **VERDICT: M-THEN-T RULE**. M lands, with nine conditions. Read its head whole
  before building. In short:
  1. "one θ" is the matcher's property, not the takes';
  2. the owner can root-invoke `take`, so `fuse_atomic` covers the fuse call only, and L2's second conjunct as written
     is false;
  3. no `fuse_iff_compliant`; `take_iff_compliant` on each side;
  4. the `fuse_atomic` membership is over (slot, act), and its mutation is P3;
  5. the peer-box witness is a θ in one box and outside the other, not F2 at θ = 11;
  6. F6's refusal name follows `via` (`grantRight` / `noGrant` / `unpinned`);
  7. the KERNEL-45 line does not say "joint law": it is two runs of one term, coupled by one forwarded byte string and
     one seal;
  8. T's trigger is rewritten ("the first method whose nested invoke argument is not a byte string it already holds");
     LANG-23 (iii) stays open;
  9. the deletions are the first read's list, including `Conds.space` and `Assigns`.
- No RULINGS row for PROT-6 after R-0049 yet. Poll for `RELEASE PROT-6`.
