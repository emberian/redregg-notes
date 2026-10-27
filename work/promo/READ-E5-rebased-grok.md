VERDICT: RULE E5-LANDING

One condition, still. The tooth is real; the sentence that names it is not. Strike `X2h admitted` from `promo/E5/commit-msg-draft.txt` (the PLANT line, which also cites `logs/p5plants/PL1-roots.log`) and from the plants bullet in `promo/E5/decision-protocol.md`. The mutant admits **X2r**. The log that shows it is `logs/p5plants2/PL1-roots.log`. The log the draft cites is the old run: `X2h: refused keyTaken`. Everything below holds.

Read against `promo/E5/full-2.patch`, byte-identical on hbox to `git diff 28e2d88` of `wt/p5-r2` [MEASURED `diff -q`: 55 files, +1705/−392]. The ready line's +1688 is a miscount of that diff. No build.

## 1. The condition

PL1 is a tooth. [READ `client/tests/foreign.rs`] X2r is a second call of A, never passed to accept. Its cells-root byte is flipped (`ROOT_HEX + 1`). The assert demands `headMismatch`. [MEASURED `p5plants2/PL1-roots.log`] under the mutant the test dies at line 235, `X2r: tx 498d6dee…`, and the output has no `refused`. That is the success line. X2's `pathMismatch` assert is above it and did not fire, so the height forge still refuses. [MEASURED `p5plants2/control.log`] the same test, unmutated, is green, so the `headMismatch` assert holds without the mutant.

The unmutated name is `headMismatch`, not `pathMismatch`. [READ `Protocol/Receipt.lean` `check` on `wt/p5-r2`] `rootsDigest ≠ roots` is `.error .headMismatch`, and it sits in front of `answerOf`, whose failure is `pathMismatch`. Forging `r.root` moves the digest and leaves `r.jroot` and the journal path alone, so dropping the comparison falls through to an inclusion that still verifies. [INFERRED] that is the mutation: the log says `PL1-roots apply ok`, and the assert that goes red is the one the comment says a skipped roots check would admit. `pathMismatch` stays X2, the height forge (PL2).

X2h is a different row. [READ the test] it is a receipt built at a later head, asserted `headMismatch`, and the decision's rows list says so. The plants bullet and the commit draft still say the roots mutant admitted it. It did not, last time or this time.

## 2. The rebase

The fuse's Lang survives next to the receipt. [READ `Lang/Package.lean`] `RelRead` is still `points`, `range`, `live`, plus `receipt : Bool := false`. There is no peer field on `RelRead`; the fuse's peer read is the second list. [READ `Lang/Program.lean`] `methodReads` still takes `rs` and `ps`, still calls `peerOf`, still checks the package slot, still appends `peerLabel`, and now passes `rc` and `args` into both `readsData`s. `program` is `(bytesOf) (digestOf) (rc : ReceiptCheck)`. [READ `methodSig` / `CheckError`] `pairNamed` stays, and `(rs ++ ps).any (·.2.receipt)` requires `receipt : bytes`; `peerNotNamed` stays, and `receiptRead` is added beside it.

No fuse theorem weakened. Five, each a binder and no new premise [READ the hunks]:

1. `fuse_atomic` — `{rc}`; `hX` is `Lang.program … rc`; `hc` and the invoke premises stay.
2. `jointLaw_sound` — same binder; the conclusion is still the two peer `offer` records, `methodReads` gaining `rc`.
3. `invitation_once` — same; `ha` and `hcan` stay; the peer records stay.
4. `peerReads_package` — `h` and `hps : ps ≠ []` stay; the conclusion is still the package slot.
5. `take_run_sound` — `hR`, `hid`, `hp` stay; the run hypothesis and the `methodReads` conjunct gain `rc`; the two row acts stay.

`methodReads_no_peer` is the same shape: an equality, both sides gain `rc`, no premise. The 2 vanished names in `statement-diff-2.txt` are generated `CheckError.match_on_same_ctor`, not theorems.

108 is 89 − 1 + 20. The one that left is `EscrowWitness.hw0`: it is not on `28e2d88` and not in this tree [MEASURED `git grep`]. The 20 that entered are the fuse statements the parameter reaches: `fuse_atomic`, `fuse_calls`, `invitation_once`, `jointLaw_sound`, `take_run_sound`, `methodReads_{conforms,digests,no_peer}`, `peerReads_{package,parent,unpinned}`, and the private helpers in `PeerRead`, `StdOffer`, `StdOfferFuse` (`readsData_record`, `point_cases`, `rows_cases`, `runMeasured_inv`, `take_rowsTy`, `fuse_tree`, `methodReads_offer`, `party`, `readsData_offer`). Net +19. I opened the five above and `readsData_record` (conclusion still `∃ fs, d = .record fs`; `args` is a binder). I did not open `point_cases`, `rows_cases`, `take_rowsTy`.

## 3. Beyond the rebase and the plant

`Params` gains `receipts : ReceiptCheck`, and `Loopback.measureInvoke` takes it off the writer. That is the fuse's measure path running the program the writer runs, not a second check. [READ `ReceiptWire`] `receipt_member_dropped` and `receipt_tooth_reads` inline the bytes in the statement and close `by decide +kernel`. No `set_option` in that hunk. The ready line calls the inlining the refusals-gate fix. I did not re-diff it against `full.patch`.

## 4. lang!

No wire bump. [MEASURED] `Lang/Bounds.lean` and `gates/codec-vectors` are not in the diff; `packageWireVersion` on the tree is `5`. `lang!` is the install-acceptance flag day, as before.

CROSS-LAYER lines are in the commit draft: LEDGER, HOSTING, KERNEL (Proofs only), PROTOCOL, HOST. CLIENT tests is there too.

[MEASURED `git show 28e2d88:decisions/protocol.md`] the last heading is PROTOCOL-64. `decision-protocol.md` is PROTOCOL-65, written to append after it, fuse paragraph at the end. It does not contain PROTOCOL-64.
