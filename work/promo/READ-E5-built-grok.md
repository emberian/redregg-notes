VERDICT: RULE E5-PATCHSET

Condition, before this lands. PL1 is not the tooth the ready line names. `logs/p5plants/PL1-roots.log` panics at `client/tests/foreign.rs:226` with `X2h: refused keyTaken`. The forged-height assert (line 214) had already passed, so dropping the roots comparison does not admit X2. X2h is refused, not admitted: the same transaction was already accepted at X1, and the insert dies `keyTaken`. The commit draft and `decision-protocol.md` both say X2h was admitted. It was not. Re-plant a forged-roots receipt whose transaction is not already in `accepted` (the design's X2r) so the row admits, and strike "X2h admitted". Everything else below holds.

Read against `promo/E5/full.patch` (3695 lines) and the tree the plants ran on, `hbox:/tank/dregg-build/nanodregg/wt/p5-lang` at `1fc905f` plus that diff. No build. The worktree numstat is 51 files, +1644/−339 [MEASURED `git diff --numstat`]. The ready line's +1610 is a miscount of this diff; the new-file lengths in the patch match the worktree (StdHead proofs 194, Foreign proofs 153, `foreign.rs` 257).

## 1. C0

Holds, and the parenthetical is not the statement that landed.

[READ hunk `Lang/Proofs/Rel.lean`, `cited_authenticated`] The old conclusion was the exact three-field record `("key", k), ("live", cellLive), ("val", val)` from `x.live = true` alone. The new statement keeps that hypothesis and no other. It concludes

`ps[j] = .record ([("key", k), ("live", cellLive look g)] ++ col ++ [("val", val)]) ∧ (x.receipt = false → col = [])`.

When `receipt = false`, `col = []`, so a live-only read is still the three-field record. It is not a fourth field `receipt = none`. When `receipt = true`, this theorem does not pin `col`; the proof builds `[("receipt", seenData sn)]` and the sibling `receipt_column_authenticated` states it, for point slots. Declared: `restates.txt` line 13, `Nanodregg.Lang.cited_authenticated`. That is the design's restatement, not a hypothesis.

Sample of ten, each a real statement change the parameter reaches, none a new hypothesis [READ the hunks]:

1. `cited_authenticated` — conclusion restated as above; binder `rc` and `args`; `x.live = true` stays the only hypothesis.
2. `deployed_program_own_codec` — `∀ rc`, equality includes `rc`, proof `rfl`.
3. `activity_monitor_safe` — `∀ rc` on `runMeasured` / `runSetup`; conclusion unchanged.
4. `object_history_chain` — `hprog` is `Lang.program … rc`; binder, not a premise.
5. `invoke_lift_witnessed` — the exhibited program is `Lang.program … Lang.noReceipts`. An instance, not a hypothesis.
6. `escrow_invokes_deployed` — `ObjectHistory` over `Lang.program … rc`, quantified.
7. `pointData_ok` — third disjunct for `receipt = true`; the old two records remain under `receipt = false`.
8. `run_calls` — `∀ rc` on `(program bytesOf digestOf rc).run`.
9. `contextual_law_demanded_hole` — `judge` is named at `noReceipts`. The constructor changed; no premise was added.
10. `requiredOf_total` — `∀ rc`; still `∃ N, requiredOf … = .ok N ∧ N < ticks`.

The other 79 names in `restates.txt` are the same ripple (binders, `noReceipts` instances, or the `readsData … ad` argument). I did not open every one of them. I did not find a landed theorem given `x.receipt = false` as a premise [MEASURED: the only `receipt = false` lines added in the diff are conclusions of `pointData_ok` and `cited_authenticated`, plus `hx : x.receipt = true` on the new `receipt_column_authenticated`].

## 2. C1

One diff, and it carries the instantiations. Nothing is left on the two-argument form [MEASURED: `rg` of `Lang.program` in the worktree finds no call that is not `noReceipts`, a `ReceiptCheck` binder, or `Protocol.Foreign.check`].

Present [READ the diff headers]: Lang (the program, `Rel`, `Package`, `Surface`, the proof files the census named, including `LiveTeeth`, `Load`, `Need`, `NeedComplete`, `Provenance`), Ledger (`EscrowAdmitted`, `EscrowInvokes`, `EscrowRun`, `EscrowWitness`, `GrantCapTooth`, and `Ledger/Sim/Journey`), `Hosting/Proofs/Deployed.lean`, `Hosting/Sim/Journey.lean`, `Kernel/Proofs/{InvokeTreeWitness,InvokeWitness,Logic/History,Logic/HistoryWitness}`, `Host/Deployed.lean`, `Protocol/Rows/Params.lean`, plus `Protocol/Rows/{Deployed,Loopback}` which the signature also reaches.

"Hosting/Proofs 3" is not three proof files. The proofs file is `Deployed.lean` only. `Hosting/Sim/Allowance.lean` mentions `Lang.program` in a comment and calls `langProgram`, which Journey now builds with `noReceipts` [READ]. "Ledger/Proofs 6" is five proof files plus `Ledger/Sim/Journey`. All of those are in this diff.

## 3. The objects

**Std.head, refuse and record.** [READ `Lang/StdHead.lean`] `headPackage`: methods `fork` and `post` write state and decide nothing. The law `headAtAt` at equal steps demands `eqData` of the whole `at` record, refused `forkedHead`; a lower step count is `staleHead`; a lower height at a higher step count is `badHead`. `headAtFork` records a fork only when it names the held roots, at the held step count, with other roots (`badFork`). The `forked` arm is `eqData` of the head, refused `forkedHead`: frozen. [READ `decision-protocol.md`] The cost is named: a grantee of `invoke` on `post` can freeze the object; recovery is a new head object, not an unfreeze. Q1 holds.

**Heads rows.** [READ `Accept.ob`] `heads` is `(key (cell digest))`, `trust` inserts, `distrust` retracts. The accept reads `(heads (range 1 1) (receipt))` and refuses `untrusted` when the range lists nothing. Retire of the anchor is that retract. X5 is that row [READ `foreign.rs`]. Q4 holds. `headDead` (a retired head *object*, `look` returns `none`) is a different refusal and has no `nd` row; the decision says so.

**The parameter, Lang below Protocol.** [READ `Lang/Rel.lean`] `ReceiptCheck := Cell → ByteArray → Except String Seen`, `noReceipts` refuses every receipt. [READ `Lang/Program.lean`] `program` takes it and passes it to `readsData`. [READ `Host/Deployed.lean`] `X` passes `Protocol.Foreign.check`. [MEASURED] `rg "^import Protocol" Lang` in the worktree is empty. The only new `import Protocol` in the patch is `Host/Deployed.lean`. Q5 holds.

**Argument, not a call kind. Committed only.** [MEASURED on the worktree base, file not in the diff] `Body` has 13 constructors (`enroll`, `rotate`, `install`, `create`, `write`, `law`, `invoke`, `grant`, `revoke`, `issue`, `account`, `transfer`, `credit`). [READ `Protocol/Foreign.lean`] `check` returns `.ok` only on `Receipt.check … = .ok (.committed h td)`; `.ok _` is `notCommitted`; `notBefore` is passed as `0`. The committed arm of `answerOf` does not read `notBefore` [READ `Protocol/Receipt.lean:78–83` on the base]. Q2 holds.

## 4. The theorems

**`foreign_receipt_sound`** [READ `Protocol/Proofs/Foreign.lean`].

- Object: `Foreign.check`, then `check_committed` on the World `hr` names.
- Weaker without it: an `.ok` from the column is not an admission in a fold of A.
- Disjunct: `CollidesAmong` of `check_committed`'s list, not a bare `Collision`. [READ base `Protocol/Proofs/Receipt.lean:47–49`] that list is `[rootsPre …, w.rootsPre …] ++ inclPres (journalSpec …) …]`. The new theorem `rcases`es `check_committed` and returns that disjunct. The height in the conclusion is `v.height + 1`, from `fold_journal_turn`, not "at step s₀".
- Mutation: drop `rootsDigest ≠ roots` in `Receipt.check`. The freshness premise `hr` (`decode rootsB = some (wA.roots)`) is on this theorem only. `check_committed` does not have it. [MEASURED PL1] that mutation does **not** admit a row. See the condition. The theorem's shape is the one the design asked for; the tooth was not.

**`forged_receipt_refused`.**

- Object: the committed arm of `answerOf` (`verifyInclusion`), with the roots comparison still in force (`hroots` makes the `headMismatch` split absurd).
- Weaker without it: a relay who keeps the roots can swap the entry.
- Disjunct: `.error "pathMismatch" ∨ CollidesAmong` on that same inclusion list.
- Mutation: drop `verifyInclusion`. [MEASURED `PL2-inclusion.log`] the forged-height accept succeeds: panic at line 214, `X2: tx e07b90a9…`, with no `refused`. Distinct from PL1, and it is the one that admits X2.

**`forked_head`.** Two theorems, both in the patch.

- `head_at_at` (L2+L4) [READ `Lang/Proofs/StdHead.lean`]: an *admitted* `at → at` change has `s ≤ s'`, `s = s' → h = h' ∧ r = r'`, and `h ≤ h'`. Not an equality to `.error "forkedHead"`. No hash disjunct. A law that compared steps only and admitted X3's pair makes it false. [MEASURED `PL3-headlaw.log`] `refused` on `invoke … 1` (post) panics `admitted: tx 944609b9…`. That is the second head. Named, and distinct from PL1 and PL2.
- `forked_head_column_refused` (P4): `headView = some (.forked _) → check = .error "forkedHead"`. No disjunct. [MEASURED `PL4-forked.log`] X3b's accept is `hint program: notHead`, still refused. The builder said `notHead`, and the log agrees. The design's mutation ("ignore `.forked`" so the receipt is *accepted*) did not happen: the row still refuses, under another name. The equality to `forkedHead` would fail to prove, which is why the test is red, but the freeze still refuses. Weaker tooth than P3's, and already disclosed. Not the condition.

Also present, and they are the record half of Q1: `head_at_fork` (L5), `head_forked_frozen` (L3), `head_world_fixed` (L6). `fold_journal_turn` (P1) is what makes the genesis disjunct of P2 impossible. `ofBytes_bytes` (P5) is in the patch; [MEASURED `PL6-member.log`] dropping the refused member reds that proof (`unsolved goals` on the `refused` arm), not a row.

## 5. The range extension

A widening of where E1 put a column, and one check.

E1's `live` is a field of `pointRecTy` only. E5's `receipt` is on points (`pointRecTy`) and on range rows (`rangeRowTy`) [READ `Lang/Package.lean`]. Both are filled by `receiptSeen` [READ `Lang/Rel.lean`: `pointData` and `receiptRow` each call it; `receiptRows` maps `receiptRow` when `receipt` is true]. One definition.

The fixture exercises the range arm, not the point arm: `accept` declares `(heads (range 1 1) (receipt))` and `foreign.rs` passes `--range heads 1`. A point read would call the same `receiptSeen`. `receipt_column_authenticated` states the point slots only; there is no theorem whose conclusion is the range row's `receipt` field. The range assembly is the three-line `receiptRow`. That is a gap in the statement, not a second check.

The pin gap is real and not patched here. [READ `Verb.lean` on the worktree, not in the diff] `invoke` takes `--range` only. [READ `Machine.derivePins`] pins are the cells the derivation asks for and `rowUnpinned` rows. No `Machine.lean` hunk. [READ `decision-protocol.md`] a `--pin` for `nd invoke` is filed as its own card, trigger "the first deployed point read". E1's live column has the same gap and was left alone. Right place to leave it.

## 6. Wire

There is no 5 → 6. That is the right price, and it is not this condition.

[MEASURED] `Lang/Bounds.lean` is not in the diff; `packageWireVersion : UInt8 := 5` on the worktree. `gates/codec-vectors.tsv` is not in the diff, so nothing was regenerated: the vectors are the version-5 vectors, byte-identical because no wire definition moved. An old package does **not** refuse by version. A first byte other than 5 still refuses `lang/package-version/5`, by the theorem that was already there (`packageWireVersion` is unchanged).

Why no bump is sound [READ `Lang/Package.lean` `relReadShape`]: `RelRead` is recovered by type equality against `relReadTy`. The receipt field is extra record fields in a method that declares `(receipt)`. Those shapes are tried after the old `(live, receipt) = (false, false)` and `(true, false)` shapes, so a package that installed before cannot decode as a receipt read. A receipt-shaped type was `badMethod` and is now accepted, which is why the landing is still `lang!` (an old log that *attempted* that install can re-fold). That is a flag day of meaning, not of byte 0. The design's §4 bump listed a byte that does not move. The builder's disagreement, on the record before the build, matches the diff.

Call codec: unchanged, 13 kinds, as above. Reply layout: `receiptText` is not in the diff [MEASURED]. No `host!` from a reply field.

## 7. sorry, admit, native_decide, weakenings

[MEASURED] `rg` of `sorry|native_decide` over `Lang/StdHead.lean`, `Lang/Proofs/StdHead.lean`, `Lang/Rel.lean`, `Protocol/Foreign.lean`, `Protocol/Proofs/Foreign.lean`, `Protocol/Proofs/ReceiptWire.lean`, `Kernel/Proofs/Journal.lean` is empty. The receipt tooth is `decide +kernel`, which is the kernel decider, not `native_decide`.

No landed statement was given a new hypothesis. `cited_authenticated` is the declared restatement in §1. `head_at_at` is weaker than the design's "equals `.error forkedHead`" and stronger than a name: it constrains every admitted change. The name is the term, and PL3 is what shows the name's row. I do not count that as a hidden weakening.

Q3: the lookup receipt is not built. `Foreign.check` has no host-hint arm. [READ `decision-protocol.md`] 01a14dfa-1ffb is recorded closed as superseded by PROTOCOL-46 §7. That close is the decision text, not a cv write I saw.
