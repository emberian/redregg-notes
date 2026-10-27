# RETIRE-LANG report (Lang half of KERNEL-70 `retire`), 2026-10-26

Key: MEASURED = I ran it. READ = I read it. INFERRED = I reasoned it and did not run it.

## Artifacts
- My delta only: `/private/tmp/claude-501/-Users-ember-dev-breadstuffs/01a179c1-8fda-7533-bba2-b7eab03493e4/scratchpad/retire-lang.diff` (41 files, +543/-224). It was made against 5a0a7e4 with the base for lang staged. MEASURED: it applies cleanly with `git apply --3way` on top of the newest kernel patch, /Users/ember/dev/redregg/work/codex/retire/retire-full.diff.
- One base fix kept separate: `/private/tmp/claude-501/-Users-ember-dev-breadstuffs/01a179c1-8fda-7533-bba2-b7eab03493e4/scratchpad/retire-lang-basefix.diff`. Kernel/Sim/Gen.lean probeRetire wrote `some .tomb`; it must be `some Entry.tomb`, because it does not elaborate (the same bug is at line 1888 of retire-full.diff). Without this fix, nothing that imports Kernel.Sim.Gen builds, lang-journey included.
- The hbox build tree is /tank/dregg-build/nanodregg/wt/retire-lang (base + delta + basefix). Logs are in /tmp/retire-lang/ on hbox.

## Files by column
- TYPES, Lang/Package.lean: `occasionTy` gains `("retire", .record [])` between relaw and write, and the docstring now covers retire.
- CTX, Lang/Program.lean: `occasionData` gains `.retire => .inj "retire" (.record [])`, and `occasionOk` treats `.retire` like birth/write.
- TRUST: Lang/StdHead.lean `headLaw` retire = `refusedT "retire"` (the docstring says so); Lang/Proofs/StdHead.lean adds `head_retire_refused`.
- LANG: Lang/Std.lean, Lang/Surface.lean (`occasions` gains retire; the doc says "all six"), Lang/StdOffer.lean (the offer guard's occasion case gains `retire => refused notConsumer`), Lang/Journey.lean, Lang/Journey/{Claims,ContextualLaw,Main,Retire(new)}.lean, Lang/Proofs/{Std,Chain,StdChain,Receiver,StdFits,StdGen,StdHead,StdTeeth,Claim,Invoke}.lean.
- LEDGER: Ledger/Escrow.lean (`lawOf6 … frozenC frozenC frozenC …`; retire is refused `frozen`), Ledger/Proofs/Escrow.lean, Ledger/Proofs/EscrowRun.lean, world/escrow/Escrow.ob.
- HOSTING: Hosting/Proofs/Package.lean (`phase_frozen` gains a retire conjunct).
- PROTOCOL: Protocol/Rows.lean (`sealedLaw` gains `(retire x {no})`).
- CLIENT: client/tests/fixtures/foreign/Timelock.ob (`(on (relaw retire write) (refuse "frozen"))`) and client/tests/fixtures/pin/Live (edited by hand, see below).
- KERNEL/TRUST: Kernel/Proofs/Logic/History.lean (see "Restated"). It is UNBUILT because it imports the broken InvokeTree.

## Law decisions (each stated in its docstring)
- ownerSigns, allowlistLaw, allowlistWith: retire = c, the same clause as the other acts.
- boundedWith, windowedLaw: retire = okT.
- quorumLaw: retire = `refusedT "quorum"`.
- machineLaw: retire = the `frozen` clause.
- headLaw: retire = `refusedT "retire"`.
- Escrow (Lean law and .ob) and Timelock.ob: retire = `frozen`.
- Protocol `sealed`: retire refused `sealed`.
- StdOffer guard: retire refused `notConsumer`.
- Journey laws tallyFresh, frozen (it freezes the LAWS, not the object), birthOnly, onlyTo, decider and openLaw: retire = ok.
- Claims `leaky`: retire = test.
- Surface laws with `else` (Bell `(else ok)`, Rows `always`, the decider) fall to their else, which is ok.
- One departure from the brief: `Std.keeps` retire = c (`guard (inv new)`), not okT. With okT the law leaves the certifying shape: `Term.guardedBy` excepts only the relaw arm, so `keeps_guarded` would fail. Because old = new, c admits every retirement of a state the law reached. Lang/Claim.lean is unchanged.

## Restated theorems (old → new)
- `Std.lawCase5_arm` (5 clauses, a 5-row find?) → `Std.lawCase6_arm`: 6 clauses (b ad rl rt wr iv); the row list gains `("retire", rt ⟨1⟩)` after relaw.
- `Std.lawCase_arm` {b ad rl c} → {b ad rl rt c}; the list gains `("retire", rt ⟨1⟩)`. `lawCase_change/birth/relaw/adopt` gain the implicit rt (they are stated over `lawCase b ad rl rt c`). New: `lawCase_retire`.
- `Std.LawKeeps` (a def under every `Step`): `(ℓ = "relaw" ∨ ℓ = "adopt") → n = o` becomes `(ℓ = "relaw" ∨ ℓ = "adopt" ∨ ℓ = "retire") → n = o`. This is the true kernel fact: `retireCheck` judges old = new. bounded_reached and windowed_count_reached rely on it, because their laws admit retire with okT.
- `Std.lawOf5_occasion` ("one of the five") → `Std.lawOf6_occasion`: six labels, retire included.
- `Std.windowed_epochs_every`: `ℓ ≠ "relaw" →` becomes `ℓ ≠ "relaw" → ℓ ≠ "retire" →`. This narrows the claim; the reason is the same as the relaw exception: windowed admits a state-keeping retirement in any window. The landing message must declare it.
- `NoRefStd.lawOf_` gains an hrt premise. `lawOf5_` → `lawOf6_`. `isLaw_lawOf` is over 5 clauses; `isLaw_lawOf5` → `isLaw_lawOf6`.
- `Std.lawOf5_prints` → `Std.lawOf6_prints` (adds hrt); `lawOf_prints` adds hrt. MEASURED: the bound is unchanged, `max (M+2) (max 9 (N+5))`; one more arm adds no depth, and it builds green.
- Ledger `escrow_frozen`: `ℓ = "write" ∨ ℓ = "relaw"` becomes `… ∨ ℓ = "retire"` (stronger). `escrow_occasion`: six labels. `escrow_verdicts`: the frozen list adds "retire".
- Hosting `phase_frozen`: adds `verdictIs false (… retireD …)` (stronger).
- Kernel `object_step_some`: a new conjunct after the relaw/adopt one, `(r.occasion = .retire → new = old)`. The private `occasion_relaw` now takes `ℓ = relaw ∨ adopt ∨ retire` and returns `(∃ ls, relaw ∨ adopt) ∨ r.occasion = .retire`. INFERRED, unbuilt (InvokeTree).
- New theorems: `machine_retire_refused`, `quorum_retire_refused`, `head_retire_refused`, `judgeOne_quorum_retire_refused` (receiver level), and the teeth (decide +kernel) `quorum_retire_refused_quorate`, `ownerSigns_retires`, `ownerSigns_retire_delegate`, `allowlist_retires`, `allowlist_retire_refuses`, `bounded_retires`.
- No sorry, native_decide, #guard or budgets were added.

## Re-emitted files
Every package text changes, because reqTy prints the occasion sum.
- world/doc/Section, Section.lib0, .lib1, .lib2: `lang-journey --write world/doc`.
- world/escrow/Escrow: `ledger-sim --write-text`.
- world/grain/Lifecycle and world/hosting/Allowance: `hosting-sim --write-text`.
- world/resident/Bell, client/tests/fixtures/foreign/Accept and Timelock: lowered from their .ob by `Surface.readPackage` + `Print.package`. Script: /private/tmp/claude-501/-Users-ember-dev-breadstuffs/01a179c1-8fda-7533-bba2-b7eab03493e4/scratchpad/emit-cores.lean, run with `lake env lean --run` from the tree root.
- world/head/Head: `Print.package Std.headPackage`, same script.
- client/tests/fixtures/pin/Live has no generator, so I edited it by hand: `(retire (rec))` added to the 8 occasion sums, and a `retire` arm added to its open law. MEASURED with the rebuilt `ob "(check …)"`: the new text is `ok 4047 bytes id 230b7453…`, and the old text is refused `badMethod post`.

## Builds and runs (hbox, 6G, 2 threads)
- MEASURED green: Lang.Proofs.{Std,Chain,StdChain,Receiver,StdFits,StdGen,StdHead,StdTeeth,Claim,Invoke}, Ledger.Proofs.{Escrow,EscrowRun}, Hosting.Proofs.Package, Protocol.Rows, Ledger.Escrow, Kernel.Sim.Gen (with basefix), lang-journey, ledger-sim, hosting-sim, ob.
- MEASURED full `lake build`: the only failures are Kernel.Proofs.InvokeTree and Kernel.Proofs.Carry, both base kernel issues. Kernel.Proofs.Logic.History, and whatever imports InvokeTree, could not be built.
- MEASURED lang-journey: GREEN (1251 lines). `--harness-control`: RED (1), as the control should be. Before the re-emit it was RED (6): LB0, LBw, and DC0 ×4.
- MEASURED: ledger-sim 1 and hosting-sim 1 are ALL PASS.
- No cargo was run.
- MEASURED `codec-vectors --check`: RED (20). Only kernel/body (13), kernel/call (2) and kernel/unsigned (2) have stale tags, from the base's Body change. No lang site moved. KERNEL must run `codec-vectors --write gates/codec-vectors.tsv`.

## Journey rows (MEASURED, from the default run)
ok   RT0 A installs ownerSigns, quorum {A, B} k 2 and the board (methods [drop, put], relations [notes]): [admitted, admitted, admitted]
ok   RT1 B retires A's data object under ownerSigns (expected notOwner): refused notOwner Nanodregg.Kernel.Receive.Refusal.notOwner 1263587183056711438
ok   RT2 A retires it (expected admitted): admitted; a tombstone true; allowance 99971487 → 99971108, charge 444, weight back 65
ok   RT3 A, its owner, retires the quorum object (expected lawDenied quorum): refused lawDenied Nanodregg.Kernel.Receive.Refusal.lawDenied 2566878014620656176 "shared: quorum"
ok   RT4 A creates the board and puts note 1 (expected admitted): [admitted, admitted]; the row stands true; head count (some 1)
ok   RT5 A retires the board while note 1 stands (expected rowsRemain): rejected rowsRemain
ok   RT6 A drops note 1 (expected admitted): admitted; the row stands false; head count (some 0)
ok   RT7 A retires the empty board (expected admitted): admitted; a tombstone true; its head true → false; allowance 99968601 → 99968306, charge 444, back 65 (the cell) + 84 (its heads)
ok   RT8 a put pinned at the board's last live entry (expected stale): rejected stale
ok   RT9 a row insert under the retired board, the board pinned at its tombstone (expected orphanRow): orphanRow
ok   RT10 a range read of the retired board's relation (expected noRelation): noRelation

RT9 and RT10 hand World.admit a Turn no receiver derives (the board pinned at its tombstone). Through Receive, a call on the retired board stops earlier, at `stale` (RT8).

## Base (kernel side) defects found
1. Kernel/Sim/Gen.lean probeRetire: `some .tomb` does not elaborate (line 1885 in 5a0a7e4+base; 1888 in retire-full.diff). Fix: basefix diff. MEASURED.
2. Kernel/Proofs/InvokeTree.lean: still `revoke` (lines 623/680/999). MEASURED. Note for the lane: `effect_at_object` now has to admit a retire effect at an object.
3. Kernel/Proofs/Carry.lean:309 `dispatch_world`: `rfl` fails on enroll, because enroll reads `c.unsigned.world` (MEASURED on the 5a0a7e4 base). The newest patch moves the World check into receive/signedBy, so this may be fixed there (INFERRED).
4. Kernel/Proofs/Logic/History.lean `occasion_relaw`: the case over Occasion lacked `retire` once Occasion.retire was added. I added it, inside my delta.
5. History has no ObjectStep for a retirement. A retire of obj is none of keep/other/frame, so an honest history around obj cannot contain its end, and `object_history_of_honest` needs a retire case or an end-of-history rule. My History change keeps the lift correct once such a step (old = new, occasion retire) exists. INFERRED (READ).
6. codec-vectors not re-drawn (MEASURED; see above).
