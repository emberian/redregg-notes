## PROTOCOL-65 · receipts between Worlds: another World's committed call, checked by Lean against a head this World holds (E5, PROGRAM-20261022 §2(a) / P5; R-0051, R-0059; cv 01a14ef0-ffe7, 01a14dfa-200a, 01a14dfa-1ffb, 01a14de7-224a)

**Decision.**
1. **The head is an object of the generated package `Std.headPackage`** (`Lang/StdHead.lean`, text `world/head/Head`).
   - State: `{world : digest, head : at {height, roots, steps} | forked {held, other, steps}}`.
   - Methods `post` and `fork` write the state and decide nothing. The law `head` is the one decision:
     - `world` fixed (`otherWorld`);
     - from `at` to `at`: the step count never falls (`staleHead`), an equal step count keeps height and roots (`forkedHead`), and the height never falls (`badHead`);
     - from `at` to `forked`: the fork names the held roots at the held step count, with other roots (`badFork`);
     - `forked` is frozen (`forkedHead`).
   - The key is STEPS, not height. A recorded refusal advances `steps` and the refusals root at one height (`Kernel/World.lean`, `World.steps`).
   - Posters are the owner plus whoever the owner grants `invoke` on `post`/`fork`. Several followers of A can post, and two of them fed different logs make the fork visible. Cost: a grantee can freeze the object. Recovery is a new head object, not an unfreeze.
2. **The receipt column.** A cell-keyed read declared `(receipt)` gives each point, and each row of its signed range, a `receipt` field `{height, turn, tx}`:
   - the run checks the method's own `receipt : bytes` argument against the head object that row's key names (`Lang.receiptSeen`), through the caller's pinned view;
   - an unpinned head object is `unpinned`; a retired one is `headDead`;
   - the check's refusal is the run's, by name: `notHead`, `forkedHead`, `badReceipt`, `headMismatch`, `pathMismatch`, `forgotten`, `notCommitted`;
   - what the check shows enters only as the language's data (`seenFits`, LANG-38).

   Install refuses a receipt read of a relation that is not cell-keyed, or one without `receipt : bytes`, as `receiptRead`. The read is spelled by the method's rows TYPE, as E1's `live` is, so **no package byte moves**: `codec-vectors` is byte-identical.
3. **The check is PROTOCOL's and the runtime is LANG's.** `Lang.program` gains one parameter, `receipts : ReceiptCheck` (`Cell → ByteArray → Except String Seen`). `Host.Deployed.X` passes `Protocol.Foreign.check`:
   - `Lang.headView` at the deployed `Std.headPackage` id;
   - then `Receipt.ofBytes`;
   - then `Receipt.check` against the held head's height and roots;
   - committed only. `refused` and `absent` need the call's window, which a receipt does not carry; the trigger for adding them is the first refund leg.

   Followers run the same `X`. There is no default argument. Every theorem over `Lang.program` quantifies over `receipts` (a binder), and the toy contexts pass `Lang.noReceipts`.
4. **Trust anchors are rows.** The fixture acceptor (`client/tests/fixtures/foreign/Accept.ob`):
   - keeps `heads : {cell} → {}`, which the owner inserts and retracts (revocation);
   - keeps `accepted : {tx} → {height}`, with one acceptance per transaction id (use-once).

   It accepts on `(heads (range 1 1) (receipt))`. Revocation, the certificate and use-once are three checks under one `receive`, the LPCFS monitor shape (REOR A.9).
5. **No atomic cross-World commitment.** Every row changes one World per Turn (the §2 refuter does not fire).

**Measured on the way, and acted on.**
- `nd` cannot pin a POINT read. `Machine.derivePins` pins the cells the derivation asks for and the rows the kernel names `rowUnpinned`, and `nd invoke` takes `--range` only. So a point `(live)` read (E1) is reachable from the Sims and not from `nd`, and E5's column also covers range rows. A `--pin REL KEY` for `nd invoke` is a separate card (Machine.lean); the trigger is the first deployed point read.
- Refusals-trie soundness had already landed (`Kernel/Proofs/RefusalsHead.lean`: `refusal_inclusion_sound`, `refusal_exclusion_sound`). The `Protocol/Proofs/Receipt.lean` header said it had not, and is corrected. **Amends PROTOCOL-45's critique**: "KERNEL states no refusals-trie inclusion soundness" is no longer true. `check_refused_sound` and `check_absent_unrefused` consume it.

**Theorems.**
- `Protocol/Proofs/Foreign`:
  - `foreign_receipt_sound` (P2): a committed column means the transaction was ADMITTED in a fold of A from A's genesis, at `v.height + 1` with that turn digest, or `CollidesAmong` the listed inputs (`check_committed`'s). The premise is named: the held head's roots are that fold's. This is head freshness and the poster's honesty, the thin-member trust of PROTOCOL-42. B holds A head, not THE head.
  - `forged_receipt_refused` (P3).
  - `forked_head_column_refused` (P4).
- `Lang/Proofs/StdHead` (over BigStep): `head_at_at` (L2 + L4), `head_forked_frozen` (L3), `head_at_fork` (L5), `head_world_fixed` (L6).
- `Lang/Proofs/Rel`: `receipt_column_authenticated` (L1). `cited_authenticated` is restated (RESTATES-MEANING: the live record may carry the receipt field, `[]` when `receipt = false`; no hypothesis added).
- `Kernel/Proofs/Journal`: `fold_journal_turn` (P1).
- `Protocol/Proofs/ReceiptWire`: `ofBytes_bytes` (P5, cv 01a14ef0-ffe7).

**Rows.** `client/tests/foreign.rs` runs over TWO geneses and two writers through the real `host`:
- X1: offer in A, accept in B: admitted;
- X1b: a second acceptance: refused;
- X2: the stated height forged: `pathMismatch`;
- X2r: another call's receipt with its cells root forged: `headMismatch`;
- X2h: a receipt at a later head: `headMismatch`;
- X3: a second poster's same-steps head: `lawDenied forkedHead`;
- X3b: the fork recorded, then accept and post: `forkedHead`;
- X5: anchor withdrawn: `untrusted`.

The `wrongWorld` control is the `wrongWorld` row.

**Plants** (whole logs `logs/p5plants2/`). Each reds its own row and nothing else on the way:
- roots comparison dropped: X2r (a never-accepted call's receipt with a forged cells root) admitted;
- journal inclusion dropped: X2 admitted;
- the head law comparing steps only: X3 admitted;
- forked ignored by the check: X3b names `notHead`;
- the column filled without the check: X2 admitted.

Control GREEN after restore.

**Flag day.** Lang semantics change (install accepts a receipt read it refused), so `lang!`. Every Store re-geneses. No codec, call or reply byte moves. Host closure 89 → 93 (`Protocol.Foreign`, `Lang.StdHead` and what they import).

**cv.**
- 01a14ef0-ffe7: closed (P5).
- 01a14dfa-200a: refusals half closed (landed earlier); the last-head-link half stays, with trigger "a party holding only a chain digest (the phone, cv 01a14d95-36b0)".
- 01a14dfa-1ffb: closed as superseded by PROTOCOL-46 §7 (the Host hints, follow settles; `lieLookup` is the plant). Reopen on the phone.
- 01a14de7-224a: protocol half closed by PROTOCOL-61. The residue is CLIENT's (`nd --join` takes no `IN`).

**Critique.**
- The premise of `foreign_receipt_sound` is the whole trust. It is stated, not discharged, and forkedHead narrows it only at one object and one step count. A poster that follows a forked A posts a consistent lie.
- `notCommitted` and `headDead` have no `nd` row: `nd` cannot retire an object or sign a call it does not send. Their teeth are the check's and the column's definitions only.
- The receipt column needed a range-row arm because of the point-pin gap, which is the bigger finding. E1's live column has the same gap and was not fixed here.

**Meta-critique.**
- I first designed the column on points, the shape E1 had. The deployed client made that a Sim-only feature, and I found out only when writing the two-Store row. The BIAS: trusting a landed mechanism's reach because it has theorems. "E1 synthesizes the live column" was true of Lang and false of `nd`.
- I also first claimed a package-wire bump by analogy with E1. Measurement showed reads are types and no byte moves.

**On the fuse (rebased onto 28e2d88, PROT-6).** `methodReads` threads the same `receipts` and the method's arguments into
its peer part, so a `(receipt)` read is a column of the reader's own rows and its peer's alike. `methodSig` keeps the
fuse's `pairNamed` rule and adds the receipt-argument rule (`(rs ++ ps).any (·.2.receipt)` requires `receipt : bytes`).
`CheckError` holds both `peerNotNamed` and `receiptRead`. The fuse's theorems (`fuse_atomic`, `jointLaw_sound`,
`take_run_sound`, `invitation_once`, `peerReads_*`, `methodReads_*`) gain the binder, with no hypothesis added.
