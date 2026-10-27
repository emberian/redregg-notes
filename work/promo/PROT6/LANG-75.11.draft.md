
### LANG-75.11 E3 + PROT-6 · the declared peer row read, Std.offer, and the fuse as a matcher: two runs of one judge term, one forwarded byte string, one seal (2026-10-23; CX-PROMO-5 design, CX-PROMO-6 build; IMPACT `redregg/work/promo/IMPACT-PROT-6.md`; cross-family reads `redregg/work/promo/READ-PROT-6-grok.md`, `READ-PROT-6b-grok.md`; RELEASE R-0050 as fork M; grants R-0049)

**Decision.**
- **The peer read.** A method's rows record may carry one reserved field, `peer`. It holds reads of the package's OWN relations under the other member of the argument's `pair : rec {a, b : digest}` (`Lang.peerOf`; `rowsTy`, `rowsOf`, `methodPeer`).
  - A peer-reading method without a `pair` is refused at install, `peerNotNamed`.
  - A relation labelled `peer` is refused, `badRel peer`.
  - `methodReads` is the only path from the RowView to a method. It reads the peer with the SAME `readsData`, at `parent := peer`, after the kernel's `readKind` (an unpinned peer cell is the kernel's own refusal) and a same-package-id check (`peer: another package`).
  - The kernel price is 0: `RowView.points` is parent-indexed, and every row pin is a RowTouch.
  - `Sig` gains no field.
- **Std.offer** (`Lang/StdOffer.lean`). An offer is a row `{role, terms}`: a chooser role and an acceptance box over θ (closed nat intervals).
  - `offer_guard`: an insert's box must be well formed (`badTerms`); a retract only on `invoke take|withdraw` (`notConsumer`); an upsert never (`final`).
  - The session row is an `activityLog` row guarded by `activityWaiting`. No method of this package answers or retires it; settlement moves value, which is PROT-8.
  - Methods: `post`, `withdraw`, `take`, `fuse`.
- **Fork M.** The matcher's `fuse` returns `[invoke x take deal, invoke y take deal]`, the same bytes to both. Each `take` runs as its own object. It decodes the bytes, reads its own offer and its peer's, evaluates `offerJoint` (`sameRole` / `notCompliant`), and only on `ok` retracts its OWN offer (law 4) and inserts its session row capturing `{pair, θ}`.
  - The two retracts sit in one Draft, sealed once.
  - This is not a joint law and not one judge. Nothing observes both rows together. The one θ is the MATCHER's guarantee (`fuse_calls`), not the takes'. An owner may root-invoke its own `take`, so one session row is not a fuse.
  - KERNEL-45 item 3 fired at its stated price; the amendment is in `decisions/kernel.md`.

**Theorems** (`Lang/Proofs/PeerRead.lean`, `StdOffer.lean`, `DispatchRows.lean`, `StdOfferFuse.lean`):
- The peer read: `peerOf_party`, `peerReads_parent`, `peerReads_package`, `peerReads_unpinned`, `methodReads_no_peer`.
- The term: `offerJoint_meaning` and `offerJoint_total` (the generated term's three verdicts).
- Each side's honesty: `take_iff_compliant` at the method-term grain. The matcher is not a premise. Six take refusals are named; `peerRowUnpinned` is its own name (an unpinned peer ROW), distinct from the kernel's `unpinned` (an unpinned peer CELL).
- The deployed run: `take_run_sound` (`Lang.program`'s run ⇒ `JointOk`, no calls, exactly the own retract and own session insert) and `fuse_calls`.
- `fuse_refused_disjoint` over the two real rows. It replaces the arithmetic half of the deleted `separate_witnesses_over_substitutions`.
- Kernel-side, proved from outside: `dispatched_invoke_rows` / `dispatched_ok_rows` (a dispatched invoke's returned row acts are touches of the sealed Turn) and `admit_retract_absent`.
- The fuse call (premises on the matcher z and the two parties only; `X.program = Lang.program`): `fuse_atomic` (both offer retracts are touches of the sealed Turn, slot AND act), `jointLaw_sound` (one pair and θ decoded from the one forwarded deal; each take found `JointOk` on what it read; each one's peer is the other, so both read the same two pinned rows; the two session inserts carry the same bytes), `invitation_once` (after `World.admit` both offer rows are absent: once per standing row; the grant is not spent).

**Not proved, said out loud.** The run-grain CONVERSE of `take_run_sound` (compliant ⇒ the run returns). Two lemmas are missing from the tree: machine completeness at `Bounds.stackMax` (`bigStep_run` names no stack bound; `StdRun.lean:203` records the same gap), and `extract` completeness. TAKE estimated roughly 400 lines. Journey row LF1 is its instance; `take_iff_compliant` is the iff at the term grain. `offer_safe_forever` is NOT this landing. It needs a new `row_turn_cases` (the row twin of `object_turn_cases`), and READ-PROT-6b condition 2 makes its second conjunct as written false (owner-root take). The escrow instance is DEFERRED to PROT-8, because a value-moving offer needs `Val`.

**Rows.** Journey §LF has 12 rows. LF1 is admitted: both offer rows gone, two session rows, equal `captured`. LF2 is refused `notCompliant` and both rows stand. LF2r is `sameRole`. LF3 is the peer cell `unpinned`. LF3r is `peerRowUnpinned`. LF4 is `peer: another package`. LF5 is `noOffer`, with the grants still live. The controls LF6a/b/c (`noGrant` / `grantRight` / `unpinned`, following `via`) and LF7 (`revisited`) are KERNEL-25's and the walk's, not teeth.

**Plants** (whole tree): P1 `offerJoint := ok` reds the judge's evaluation lemmas (`offerJoint_meaning`'s route) and journey LF2/LF2r admit; P2 `take` skips the judge reds `take_iff_compliant`'s route and LF2/LF2r admit (B7's tooth: no judge remains in `fuse`); P3 `fuse` drops the second call reds `fuse_calls` and LF1; P4 a second deal for y reds `fuse_calls` and every LF row (a changed argument type, so the journey deal no longer decodes); P5 retract → upsert is refused `final` by `offer_guard`, so LF1 refuses: its tooth is the row, not a theorem; P6 the peer read under `self` reds `peerReads_parent` and LF1/LF2 (`sameRole`); P7 no package check reds `peerReads_package` and LF4. Each red is read from the whole tree; under P1–P5 Lake leaves `StdOfferFuse` unbuilt below the red `Proofs.StdOffer`, so `fuse_atomic`/`jointLaw_sound` are reasoned (P3: Y's retract is absent from an admitted Turn; P4: the one-θ conjunct), not observed red. Several reds sit in private helper lemmas of the target theorem's proof; the journey rows are the outcome-level evidence (`redregg/work/promo/PROT6/plants/`).

**Deletes.**
- From `Lang/Contextual/Protocol.lean`: `Conds`, `firstFit`, `coverAll`, `priceConds`, and the Negotiation `World` with its helpers (`Tok'` included).
- From `ProtocolTyping.lean`: `Conds.space` and `Assigns`.
- From `Proofs/Contextual/Protocol.lean`: four scalar illustrations.
- From `Negotiation.lean`: twelve World theorems plus `BuyerGuard`.
- Each was a kernel fact restated over a private model. PROT-5's `Consistent` / `External` / `Internal` family stays.
- `separate_witnesses_bounded` (a scalar illustration not on the ruled list) stays, and is a candidate for PROT-5's sweep.

**The roles claim (R-0048).** Not earned here, and not reverted here. The offer's role is data on a row, judged `sameRole`. No `HasProt sp r1` / `HasProt sp r2` judgment exists, and no bridge was built (it would be a twin). PROT-3's `proj` is still the index's named reader.

**Price.** 9 RESTATES-MEANING (the rows step `readsData → methodReads`, and `methodSig_spec`'s `readsTy → rowsTy`: a peer-free method reads exactly as before, `methodReads_no_peer`), the private `setup_eq` in Ledger (CROSS-LAYER: LEDGER, R-0049), 0 hypotheses gained, 39 DELETES; no byte moves (codec vectors identical, `lang:`), no re-genesis, Std.activity's layout unchanged; journey +12 LF rows, every other row byte-identical.

**Finding (JR).** `take` consumes whichever own offer row the CALL pinned. The deal names no offer key. So a party with several standing offers does not bind which one a fuse consumes, unless θ or the box excludes the others. Every consumed offer still passes `offerJoint`. If a row owner wants that binding, the deal gains the two keys (the takes check them against their pinned points); it is a later card.

**LANG-23 (iii) stays open.** Its trigger is rewritten: the first method whose nested invoke argument is not a byte string it already holds. This fuse is not that method: it forwards bytes. T (typed nested-call arguments) is its own card.

**Critique.** `take_iff_compliant` is an iff at the term grain and only a soundness at the run grain. The honesty the plan wants, "a party never retracts without judging", is the run-grain direction, and it is the one proved. The converse is liveness, and its absence is a real gap in Lang's metatheory (no completeness at the deployed stack bound), not this card's.

**Meta-critique.** The plan's shape (X.fuse → Y.take) was written before anyone read the call language, and the blocker was found by measurement only after the IMPACT's first revision. The BIAS: designing a two-party protocol from the session-type literature's picture, where a participant hands its peer a value, and not from the ABI the methods actually have, which forwards bytes.
