# FABLE-OBS — self-measurement (axis 4) and time/oracles (axis 5): report and continuation

Worker: FABLE-OBS (Claude Fable 5.1), session cv 01a167c9-1142. Repo: `~/dev/nanodregg` (mirror; origin github
emberian/nanodregg). hbox worktree: `/tank/dregg-build/nanodregg/wt/fable-obs` (detached at 18cd38b; `.lake` a
real `cp -a` of `wt/fable-ctx`'s, 4815 files, verified by count). Local editing surface: this session's
scratchpad worktree `…/scratchpad/nano` (a git worktree of the mirror, detached at origin/main). Design:
`redregg/work/promo/DESIGN-OBS.md`. Coordination: DESIGN-TRUST.md read whole; the oracle is an instance of its
Head+Authority model (DESIGN-OBS §2.2, §2.4), nothing beside it.

## Dated lines

- 2026-10-27 00:0xZ READ: FRONTIER-AXES 4+5, VERDICT-20261024, HOLISTIC-GATES/KERNEL whole, TOPLEVEL-SPEC §0–2,
  §5, §7–§13, DESIGN-TRUST whole, waste.tsv/waste.py, converge, bar.sh+bar.tsv, PERF-2, KERNEL-44 whole, World.lean
  (refusals trie, `refusalsCounted`, `checkRefusal`, `commitRefusal`, prune), Turn.lean, Receive/{Call,Derive,Submit,
  Rederive}, Bounds, Protocol/Foreign + Proofs, StdHead, Rel.lean (receipt column), Journey/Head.lean, foreign.rs,
  Accept.ob, Escrow.ob, Surface grammar, Sim/Required, Codec.Kernel.turn.
- 00:4xZ MEASURED: Turn construction sites 26 in 18 files (`grep 'charge :='`), destructurings 14; the refusal-counter
  proof family touches 16 files; `.lake` warm copy verified (4815/4815 files); main moved ad90a47 → 18cd38b
  (fable-ctx's landing) while reading; worktree created at 18cd38b.
- 01:1xZ DESIGN written: DESIGN-OBS.md (§1 the meter leaf in the window trie; three kinds of number; the size
  ratchet; the health receipt; THE BAR; price; §2 three oracle designs priced, (i) World + (ii) inside it; the
  timelock prototype; the cell receipt as the next step).
- 01:3xZ BUILT locally (not yet compiled): `client/tests/fixtures/foreign/Timelock.ob`; journey rows TL0–TL3 in
  `Lang/Journey/Head.lean` (+ `timelockSourcePath`, `timelockStateTy`, `releasedOf`; `headRows`/`headSession`
  gain the text); `Lang/Journey/Main.lean` reads it; `client/tests/foreign.rs` gains X6 in the one test.

## State (fill as it moves)

- TL landing: (pending) — `lang:` fast judge from wt/fable-obs, CROSS-LAYER CLIENT (fixture + foreign.rs).
- Meter (kernel!): (not started) — DESIGN-OBS §1.3, §1.7, §3 item 2.

## Continuation (for a successor if this session parks)

1. If the TL landing log (`wt/fable-obs/logs/fable-obs-tl.log`) shows a refusal, read it whole and fix forward
   in the scratchpad worktree, re-sync (`rsync` the named files to hbox), re-run the same scripts/commit line.
2. The meter, in the order of DESIGN-OBS §3 item 2. Start at `Kernel/Turn.lean` (fields `member`, `ticks`;
   `logWeight` + 40), `Kernel/Receive/Call.lean` `sealTurn` (set them; `derive` must return the Walk's `pool`),
   `Kernel/World.lean` (`RefusalSlot.ticks`, `ticksUsed`, the check in `check` beside `checkWindow`, the
   insert in `commitWith`, `refusalFits`/`keptRefusal`/`refusalsCounted`/`RefusalLeaf.fits`/`refusalKeyBytes`),
   `Kernel/Bounds.lean` (`ticksPerWindow := 16 * treeTicksMax`), `Codec/Kernel.lean` `turn` (+`dc`, +`nat64`)
   and `Codec/Proofs/Kernel.lean` (`turn_size_logWeight`, `turnBytes_injective`, `turn_lawfulOn`), then the 26
   literal sites (`grep -rn 'charge :=' --include='*.lean'`), `Kernel/Sim/Required.lean` (the meter path on
   invoke turns), the kernel-sim probe, the journey row, `nd whoami --meter`. Land `kernel!:` with the WASTE
   line `WASTE: admit: the meter leaf` and the map lines the judge prints.
- 01:5xZ BUILT on hbox (wt/fable-obs, warm): `lake build lang-journey` green; `lang-journey` GREEN with TL0–TL3
  (TL3 first red `rowUnpinned`: a retract pins its row; fixed by pinning the heads row); `ob -f (core …)` lowered the
  fixture to `Timelock` (6013 bytes); `cargo test -p nanodregg-client --test foreign` ok (X1–X6, 10 s).
- 02:0xZ PLANT: `<=` → `<` in the fixture: TL0 and TL2 RED by name (`early`), lang-journey RED (2); restored, cmp-verified.
- 02:1xZ LANDING attempt 1 REFUSED: main moved 18cd38b → 62a36ee (a Doc journey added to Main.lean); conflict in
  Lang/Journey/Main.lean. Worktree moved to 62a36ee, Main.lean re-patched (both sessions kept), rebuilt, journey GREEN (939 lines).
- 02:2xZ LANDING attempt 2 launched detached (`wt/fable-obs/logs/fable-obs-tl.{pid,log}`), `lang:` fast judge.
ROOT (real 10-26 05:10Z): /Users/ember/dev/redregg/work/codex/FRONTIER-BOARD.md collects every axis's verdict, landed hash and shared need in one page; read it before a decision that touches another axis; ROOT keeps it current.
- 02:4xZ TL LANDING attempt 2 REFUSED by the size ratchet (three SIZE lines needed); attempt 3 REFUSED by `cargo fmt`
  (one long assert in X6); formatted; attempt 4 launched (pid 2387164) — queued behind four other landers (load 33).
- 02:5xZ METER BUILT (defs): Bounds (`Bound.ticks`, `ticksPerWindow`), Turn (`member`, `ticks`, +40 logWeight),
  World (`Reject.ticksBudget`, `RefusalSlot.ticks`, `ticksUsed`/`checkTicks`/`commitMeter`, fits/kept/counted),
  Call (`sealTurn`), Derive (`deriveWithTicks`), Submit (`rejectNames`), Codec.Kernel `turn`, Codec.World slot kind 3,
  26 literal sites; `lake build Kernel.World … Codec.World` green; whole-tree build running (logs/meter-build-all.log).
  Probe `probeTicks` (kernel-sim arm 19) and journey row M0 written locally, not yet synced (the build is reading the tree).
  KERNEL-68 written in decisions/kernel.md.
- 03:3xZ TL LANDED: **fab2875** (`lang:` fast judge GREEN; attempts 3–5 lost rebase races to 62a36ee/1e8a2a0 and one
  judge included the meter's M0 row by mistake — split out; pushed to origin). DESIGN-OBS §2.3's prototype is on main.
- 03:3xZ METER: whole-tree build iterations 1–8 fixed: Admit/Receive/Refuse/Frame/StaleOnly/Tree/Codec proofs, the
  21 `receiveWith_sealed` consumers through `derive_of_withTicks` (the theorem gained the ticks binder: RESTATES-MEANING),
  `Frame.refusals` excludes the turn's meter key (RESTATES-MEANING), `commit_refusals` over `commitMeter`
  (RESTATES-MEANING) + `commit_refusals_of_ticks_zero`; teeth charges +40 (Frame 170→210, 250→290; Local 145→185).
  Build 9 running.

## Closing state (2026-10-27 ~05:00Z; parked near the context ceiling)

- **Landed:** `fab2875` — DESIGN-OBS §2.3's oracle prototype (Timelock fixture, TL0–TL3, X6) on main, pushed.
- **Written:** `promo/DESIGN-OBS.md` (both axes, priced, each design's one way wrong); `decisions/kernel.md` KERNEL-68
  (in the WIP patch, not on main).
- **The meter (KERNEL-68), NOT landed: whole tree green but TWO proof modules.** Every edit is in
  `promo/METER-wip.patch` (git diff of the scratch worktree against `fab2875`; 1949+ lines, 40 files) and live
  in `hbox:/tank/dregg-build/nanodregg/wt/fable-obs` (worktree at fab2875 + the same edits, `.lake` warm, build log
  `logs/meter-build-17.log`). Definitions, codec, Required, kernel-sim probe (`probeTicks`), journey row M0,
  and 38 proof modules build. Red:
  1. `Kernel/Proofs/RefusalsCounted.lean:443` — the admission-preserves-`refusalsCounted` theorem's
     `hr : w'.refusals = pruneRefusals E (w.height+1) w.refusals` is now `… (commitMeter E w t)`. Plan: split
     `by_cases ht : t.ticks = 0`; the zero case is the old proof with `commit_refusals_of_ticks_zero`; the
     nonzero case needs a listing lemma for one insert (`Trie.toList` of `insert` = the old listing with one
     entry added or replaced at the `.ticks` key — look for `Trie.toList_insert`/`mem_toList` in
     `Kernel/Proofs/Trie*.lean`), then: `refusedOne`/`refusedIn`/`refusedWin` are 0 on a ticks entry (the arms
     already added at lines 92/133/241/270/458), so every sum is unchanged; the `l.all` clause for the new entry
     is `true` (World.lean `refusalsCounted`); the tally ignores it (`tallyStep` falls to `t`).
  2. `Kernel/Proofs/RowsComm.lean:730, 781` — `admit_comm` (two Turns commute at one World). Line 730: replace
     `pruneRefusals_get hrc _` by `by unfold World.refusalAt; rw [commit_refusals, pruneRefusals_get
     (commitMeter_canon hrc), commitMeter_get_ne (by simp)]`. Line 781: the `checkWith` tuple needs
     `(), hticks',` before `(), hst` where `hticks' : checkTicks E (commit E w t₁ posts₁) t₂ = .ok ()`. This is a
     NEW PREMISE of `admit_comm` (RESTATES-MEANING, say so): two Turns commute only if neither moves the
     other's meter; the honest premises are `w.RefusalsOk E` (in place of `RefusalsCanon`: a leaf of a future
     window must be excluded, `refusalFits` gives `win = refusalWindow w.height`) and `t₁.ticks = 0 ∧ t₂.ticks
     = 0` (THE BAR's writes and the two-rains tooth both have no ticks). Proof of `hticks'`: from `hk₂.ticks`
     (`Checked.ticks`, added) via `pruneRefusals_get (commitMeter_canon hrc.1)`, `commitMeter` at `ticks = 0`,
     and a window case split (`(w.height+2) % windowMax = 0` → the key's window is new → the leaf is absent by
     fits → `0 + 0 ≤ cap`; else the same leaf as `hk₂`'s). ~40 lines; no consumer of `admit_comm` in any proof
     (MEASURED: only World.lean's and Gen.lean's doc comments name it).
  3. After green: `lake exe kernel-sim --seeds 64` (the probe `ticks-window:ticksBudget` must be met),
     `lake exe lang-journey` (M0: `meter == log sum > 0`), `lake exe codec-vectors --check gates/codec-vectors.tsv`
     and `emit-rust --check client/src/generated.rs` will be RED (the Turn layout moved): regenerate both
     (`lake exe codec-vectors > gates/codec-vectors.tsv`? read `gates/generated.tsv`'s rule: `lake exe EXE
     --check PATH`, and the exe's own usage for the write form), `cargo test -p nanodregg-client --test
     vectors` (filtered), host-sim seeds 1–3, rows. Then land as `kernel!:` with
     `scratchpad/fable-obs-meter.msg` (draft; add the RESTATES-MEANING map lines the judge prints — expected:
     `receiveWith_sealed`, `receive_of`, `Frame` (refusals clause), `Agree` (meter field), `commit_refusals`,
     `admit_refusalAt` (new `hk`), `admit_comm`, `Checked` (ticks field), `Turn.Fits`, `turn_size_needs_digest32`;
     DELETES: none) and the three SIZE lines. Flag day: every Store re-geneses (`shapeMismatch`).
- Decls price as built: hypotheses on landed theorems: `admit_refusalAt` +1 (`k ≠` the meter key), `Agree` +1
  field, `Frame.refusals` +1 premise, `admit_comm` +2 (pending). The DESIGN-OBS §1.7 estimate of 0 was wrong
  by these four: the meter IS in the footprint and the read set, and the theorems that say "a Turn changes no
  refusal leaf" had to learn it. Say so in KERNEL-68's price when landing.
- Not done: `nd whoami --meter` (the member's own read: DESIGN-OBS §1.3 "Reading it"); the bytes meter; the
  `Receipt.check` ticks arm; the cell receipt (§2.5). All in DESIGN-OBS §3.

## FABLE-OBS-2 (successor; real 2026-10-26, cv 01a167c9-1142)

- 10-26 READ: this report whole; DESIGN-OBS whole; FRONTIER-BOARD; the price-premises and never-price-a-regenesis
  memories; METER-wip.patch's World/Turn/Admit/Frame/Refusals/kernel.md hunks; World.lean's refusal family
  (RefusalSlot…refusalsCounted, commitRefusals); RefusalsCounted's red theorem; RowsComm's `admit_comm` and its
  red lines; Local's `check_local`; Trie's `toList_insert_perm`; RefusalsHead's theorem list; Codec/World's slot codec.
- MEASURED: main moved fab2875 → c82f171 (META); the WIP rebases onto it CLEAN (no conflicting hunks). Direct
  trie-key sites (not through `refusalAt`): 186 lines in 20 files; `refusalAt` consumers: ~130 lines in 16 files
  (unchanged by the decision below). `admit_comm` has NO consumer in any proof (doc comments only).
- DECIDED (the brief's one question): YES, a shape excludes the meter key by DOMAIN. The window trie's key type is
  `WindowSlot D | refusal (k : RefusalSlot D) | meter (k : MeterSlot D)`; `RefusalSlot` keeps its three
  constructors; `MeterSlot | ticks member win`; `refusalAt : RefusalSlot → …` reads `.refusal k`, `meterAt :
  MeterSlot → Option Nat` reads `.meter k`. So `admit_refusalAt` and `Frame.refusals` keep their LANDED statements
  (the exclusion is `WindowSlot.refusal k ≠ WindowSlot.meter _`, by constructor: `commitMeter_get_refusal` has no
  hypothesis); the meter gets its own kind's theorems (`admit_meterAt` with the turn's own key excluded — its
  footprint, as its cells are — and `admit_meterAt_self`; `Frame.meter` a NEW clause). The wire is unchanged from
  the WIP (kind byte 3, the `count` leaf). What is NOT removable, and why: `Agree.meter` (+1 field) — `Agree` IS
  `check`'s read set and `check` now reads the meter; the only shape that keeps `Agree`'s statement is "do not check
  the meter", a no-op. `admit_comm`: `RefusalsCanon` → `RefusalsOk` (a window boundary needs fits to know a future
  window's leaf is absent) and `hmeter : same member → both spend ticks → used + t₁ + t₂ ≤ ticksPerWindow` — a
  THEOREM OF THE MODEL (two turns of one member that together pass the window do not commute: the second is refused
  `ticksBudget`), guarded so zero-ticks turns owe nothing; no consumer. `World.RefusalsOk` is RESTATED over the trie's
  keys (it must bound the meter leaf too; through `refusalAt` it no longer would).
- BUILT (defs + statements, local branch `fable-obs-meter` 41977c0 on c82f171, synced to hbox wt/fable-obs):
  World.lean typed (24 exact replacements, `scratchpad/typed-window.py`); Refuse/Refusals/Frame/RowsComm statements
  (`typed-window-2.py`). `lake build Kernel.World` GREEN on hbox (logs/typed-1.log).
- FORKED: the carry-through of `WindowSlot` across the 20 files, the two red proofs, the whole-tree build, kernel-sim,
  lang-journey, the regenerated codec vectors + generated.rs, host-sim 1–3, the plant; notes in
  `scratchpad/fork-typed-window.notes.md`. I land.

FABLE-TYPES-2 (real 10-26 ~09:0xZ): LANG-89 re-draws `gates/codec-vectors.tsv`'s `lang/package/6` and
`lang/package-version/6` sites (57 insertions, 56 deletions; one NEW row pins a nonempty effects child), no other site moves,
`--check` ok at 289 vectors of 59 sites. Found on the way: `--write` keeps a site's rows verbatim while its tag is unchanged,
so a vector added under an already-pinned tag never draws until the site's rows are pruned (CODEC-28 as designed; said here
so the next lane does not read a missing row as a bug). Lands with LANG-89 (CROSS-LAYER: GATES, by this line).
- FORK RETURNED (notes `scratchpad/fork-typed-window.notes.md`): branch `fable-obs-meter` 469a9b36 (24 wip commits on
  c82f171), whole tree GREEN (hbox `logs/typed-22.log`, `logs/final-1.log`: 774 jobs). Gates: kernel-sim `--seeds 64`
  `admitted=4639 refused-as-expected=61511 failing-seeds=0` (the probe `ticks-window:ticksBudget` seen; the
  harness-control red); lang-journey GREEN with `M0 … B's ticks this window reads 330; the log's sum … is 330; A's
  founder has no meter`; codec-vectors re-drawn (`289 vectors of 59 sites`, committed); `emit-rust --check` ok
  (generated.rs does NOT carry the Turn layout: no Rust re-emit); host-sim 1/2/3 ALL PASS (control red); `cargo fmt`
  ok; client `--test vectors` 4 passed, `--test foreign` 1 passed. PLANT: `checkTicks` `≤`→`<` reads `FAIL … probe
  ticks-window: full tree 16 of 16 in one window refused ticksBudget`, 4 seeds red; restored, diff clean. WASTE: one
  row moved, `admit trie-hashes-per-turn` 14.092 → 14.219 (65370 → 65961 hashes, same 4639 turns): the meter path.
- FORK'S TWO DECISIONS BEYOND THE BRIEF (accepted; in KERNEL-68's price table): (1) the meter's leaf COUNT needed a
  bound for `refusals_bounded` (its "every entry is one of three kinds" identity was false): a new `CountedOk`
  clause `Σ meterKeyOne ≤ height % windowMax + 1`, checked by `refusalsCounted`, preserved by admit/refuse;
  `refusals_length_le` → `4C + 1 + windowMax`; `worldBytesDerived` 91,914,346 → 91,965,546 (`baseRecordMax`
  91,965,674); RUNBOOK's bound line brought current, decisions/*.md and docs/record left as history. (2)
  `Host.Proofs.Deployed.admit_listing` gained `hf : w.RefusalsCanon` (the listing after an insert is known only on
  a routed trie); discharged by `Kept` in `fold_listing`. Also: `probeCarryBudget`'s plant retires a crafted 1 KiB
  cell (seed 41's heaviest cell no longer out-refunded a retire record 40 bytes heavier).
- LANDING: KERNEL-68 rewritten on the branch (c272f889); message `scratchpad/meter.msg` (111 map lines, SIZE, WASTE);
  fast-judge PROBE running on hbox (`logs/prepush-probe-1.log`) for the exact declaration names before the FULL judge.
- PROBES (hbox `logs/prepush-probe-1..7.log`): the owners gate wants ONE `CROSS-LAYER: LAYER:` line per owner (a
  combined line names none); SIZE.md must be written (`python3 gates/size.py . --write`, not `-I`); `--rev HEAD` diffs
  one commit, so the branch was SQUASHED to one commit on c82f171; the decls judge runs only in `--index` mode and
  printed 181 `add the line:` suggestions + 13 unused lines (the first summary showed 37 of 363 lines). Probe 7:
  FAST GREEN, `decls: ok — 406 modules exported, 17818 parent declarations in the reach, 280 map lines, 280 declared
  changes of meaning`; census ok; cbytes ok. Message `scratchpad/meter.msg` (280 map lines: the typed key restates
  every theorem quantified over the trie's keys — Codec's slot/order/size/wire families, Host's Deployed/Size, the
  receipt's path, every `refusal*` family in Kernel).
- LANDING launched: `logs/launch-meter.sh` → `scripts/commit -F logs/meter.msg <70 paths>` detached, PID in
  `logs/fable-obs-meter.pid`, log `logs/fable-obs-meter.log`; FULL judge, queued behind four landers on c82f171.
- FULL JUDGE attempt 1 REFUSED (log hbox `logs/fable-obs-meter.log`; gate log `main/.git/nanodregg-gate-2/6b4b5d766ddd.log`):
  main had moved (f70a5f9 TRUST certified heads; 9ccb6b6 `protocol!` self-heads; c4800fb `hosting!` inbox) → rebased
  clean (SIZE.md only), whole tree GREEN again (`logs/typed-rebased-1.log`, 777 jobs). The judge's reds, each read at
  source: (1) the 14 Rust "test failed" lines are the `nobin RED` CONTROLS (ND_LEAN_BIN empty must read red) — not
  reds; (2) host-file-sim 2/3 `plant-backup-restart fires: … tail holds records`: the 40-byte-larger Turn record
  moved the seal onto the plant's fixed 3-frame tail ("live 0 at base 8844"; seed 1 "live 1"); the plant now serves
  its tail in rounds until the live tail holds a record → `host-file-sim 2` ALL PASS; (3) THE BAR `no reopen with
  bytes past a base` — the row's OWN comment ("23 invokes leave 7912 bytes, under the 8192-byte seal floor; do not
  let the wire size choose this boundary"): 23 × 40 more = 8832, the seal fired on the tip; tail 20 invokes, and
  the stale-base plant's stated bite 5.260 → 6.069 → `ROW bar PASS`; (4) certificate-pin vocabulary [`Reject`] →
  `--emit-pin` re-emitted (1 line); (5) waste: seal grow-at-1000 3.491 → 3.551 re-pinned; the two `bar` rows wait
  on `scripts/bar.sh` (running, `logs/bar-1.log`); `open bytes-read…` fell (0.670 < 0.709: not red by the rule);
  (6) decls `stale path` Frame.lean: my Agree doc-line edit replaced 50bf961's text → main's line restored verbatim.
- FULL JUDGE attempt 2 (after the rebase onto f70a5f9) REFUSED on: three waste rows measured on the judge's tree
  (seal grow-at-1000 3.553, open grow-at-1000 0.735, rowbar reopen-bytes-per-byte-past-base 1.074 — re-pinned
  with WASTE lines) and the Frame.lean `stale path` AGAIN: gates/rebase.py wants every block 50bf961 added held
  CONTIGUOUS, and `Agree`'s new field sits inside its one 73-line hunk; decls.py then refuses every non-blank
  outside-declaration line of the block (two `omit … in` lines my copy holds verbatim) with no check that the
  landing holds them. Precedent R-0029 (`--reverts d7989d94: not an undo`): landing with `--reverts 50bf96195c7e`,
  the message says it is not an undo; GATES card 01a1786c-ab0d for the guard's false positive.
- Attempt 3 refused at once: main had moved a THIRD time (1bdd5ba0, META-2's `lang!` wire flag day: generators take a
  parameter) → rebased (SIZE.md only); the codec vectors are re-drawn on the rebased tree (both landings moved the
  wire); whole-tree build + `codec-vectors --write/--check` + `emit-rust --check` + `rows bar` running
  (`logs/typed-rebased-2.log`); attempt 4 follows with the same message and `--reverts`.

## FABLE-OBS-3 (real 2026-10-27; worktree hbox ~/nd-land/obs)

- STATUS (to the coordinator): no "attempt 4" lander is mine — that was FABLE-OBS-2's, and I have started no lander. BUILT on hbox ~/nd-land/obs, rebased onto origin/main e16403b (one conflict in testground.js's meterOf, resolved in the new plain register): the health receipt (`Protocol/Health.lean` + `Protocol/Proofs/Health.lean`: `check_sound`, `check_build`, `check_sound_sep`, green), `nd receipt --health [MEMBER]`, row `health` (ALL PASS with `receipt` and `journey`; plant trustReceipt caught at line 14), tg_meter = the checked receipt, KERNEL-71. LANDED: nothing yet. NEXT: `Protocol.Proofs.Command`'s `step_submit_planned`/`step_host_cancel` time out (whnf heartbeats) with the new `Cmd.health` arm; I fix that, then land with the new `scripts/commit`.
- BUILT + VERIFIED (commit 65282e5b on e16403be, hbox ~/nd-land/obs; the lander rebased it to e98768e7 on main): `Protocol/Health.lean`, `Protocol/Proofs/Health.lean` (`check_sound`, `check_build`, `check_sound_sep`, `counted_sound`, `counted_build`; no sorry), `nd receipt --health [MEMBER]` as `Cmd.receipt (ReceiptOf D)` (a sibling `Cmd.health` constructor pushed `step_submit_planned`/`step_host_cancel` past 200000 heartbeats; the one-arm shape builds: Proofs.Command 356 s, Incoming 202 s under load 120), row `health` (PASS, plant trustReceipt caught at line 14; `receipt` and `journey` PASS), tg_meter = the checked receipt, testground kernel rebuilt and `axes-run.mjs` GREEN 4/4 with "bob's health receipt (462 bytes, checked ok): ticks 2080232 of 2097152 · refusals 0 · total 0 · height 24" (refusals 0: follow's own admission refuses the 17th spin before signing, so nothing reaches the writer to record), KERNEL-71 written, docs/MEMBER.md row.
- LANDING (new scripts/commit, ND_LAND_DIR=~/nd-land/obs-land, log hbox ~/nd-land/logs/obs3-land.log): every Lean row this change touches ok (rows, rows --deployed, host-sim 1–3, host-file-sim 1–3, store-plants, all cargo client/attach rows); RED on two launcher rows it does not touch in substance: `cargo-untraced:launcher:fence` = `/usr/bin/env: …/nd-land/obs-land/cargo-target/…/fence-…: Permission denied` (the fence helper is exec'd as uid `nd`, and /home/hbox is drwxr-x---: GATES-28's NVMe build dir is untraversable by the second uid, so this row is red for EVERY lander on hbox), and `cargo:launcher:resident_bell` UNREAD (600 s wall clock at load ~120). NOT PUSHED: ROOT pushes 65282e5b (or re-runs scripts/commit once fence's build dir is reachable by `nd`).
- NEXT (not started): the bytes meter, `MeterSlot.bytes member win ↦ count Σcharge` (cv 01a176d9-0021) — a `kernel!` flag day: every Turn (charge > 0) writes a meter path, `CountedOk`'s meter bound doubles, ~200 meter sites across Refuse/RefusalsCounted/RowsComm/Refusals/RefusalsBound; then the health receipt gains a fourth `counted` key (one line in `check`, one in `pres`). The allowance stays outside the roots digest (KERNEL-71 critique 3).

## FABLE-OBS-4 (real 2026-10-27; worktree hbox ~/nd-land/obs; cv 01a176d9-0021) — the bytes meter

- READ: this report whole; DESIGN-OBS §1.3–§1.5, §5–§5.2; KERNEL-68, KERNEL-70, KERNEL-71 (critique 3); World.lean's meter
  family; the meter sites in Refuse/Refusals/RefusalsCounted/RefusalsBound/RowsComm/Frame/Local/StaleOnly; Protocol/Health(+Proofs);
  Follow.lean's genesis and carry; Codec World/Carried wires and their proofs; Host Deployed `Kept`/size proofs; Gen's probes.
- DESIGN (DESIGN-OBS §6, KERNEL-78): `MeterSlot.bytes member win` (kind 4) counts each Turn's `charge` (= `Turn.weight`, already
  exact by `chargeMismatch`), GROSS, at `refusalWindow (height + 1)`; the bound is `World.bytesBudget`, a genesis input committed
  in the origin, carried by a carry, written by no step; `checkBytes` → `Reject.bytesBudget member` (recorded, code 90);
  `bytesBudgetTooLarge` past `windowMax · weightMax` = 2^28; the leaf's fit is structural (`(h % W + 1) · weightMax`), so
  `RefusalsOk` needs no budget. Ticks and bytes are written as ONE `insertAll` batch (`meterWrites`); written as two inserts
  in turn, kernel-sim read `admit hashes-per-required` 1.003, so batched (proofs read it as two bumps, `commitMeter_eq`).
- BUILT on hbox, whole tree GREEN at 276ded81 (848 jobs, no sorry); then rebased onto 655ff42 (clean; one new journey,
  Lang/Journey/Readme.lean, threaded; docs/reference/kernel.md + protocol.md brought current: six counters, check 14
  `checkBytes`, code 90, `bytesBudgetTooLarge`, four health counters).
- MEASURED: kernel-sim --seeds 64 `admitted=4639 refused-as-expected=62544 failing-seeds=0`, arms `bytes-window:bytesBudget`,
  `bytes-window:sum`, `bytes-window:per-member` met; WASTE `admit hashes-per-required 1.000`, `trie-hashes-per-turn`
  14.297 → 17.853 (re-pinned in gates/waste.tsv with the reason); the `hash-count:empty-per-root` tooth now reads the
  roots of the World a Turn READS (only a genesis World has two empty tries once every Turn writes its bytes leaf), 1.028.
  lang-journey GREEN: M1 `bytes meter of B 65316 = the log's sum of B's charges 65316; net allowance spent 65133` (gross >
  net: G's retirement), M2 `next call charged 435: at exactly the budget admitted; one byte less: rejected bytesBudget`.
  rows ALL PASS (health PASS, trustReceipt plant caught at 14); host-sim 1/2/3, host-file-sim 1/2/3, hosting-sim 1,
  ledger-sim 1, adversary --seeds 200 --no-swap: ALL PASS. codec-vectors re-drawn (296 vectors of 59 sites, `--check` ok);
  emit-rust --check ok (no Rust re-emit).
- PLANT: `checkBytes` made to pass everything (`… || true`): lang-journey RED (M2 `one byte less: admitted`), kernel-sim
  `FAIL seed 0..: probe bytes-window: a Turn past the member's bytes budget was admitted`; restored, cmp-identical.
- Flag day: every Store re-geneses (World + carried wire +u64, genesis/carry input +u64, window key kind 4); refusal code
  `bytesBudget` appended; derived World bound 91,965,546 → 92,016,754 (`baseRecordMax` 92,016,882); ListingPin's World and
  carried pins gained eight zero bytes.
- LANDING 1 (scripts/commit, ND_LAND_DIR ~/nd-land/obs-land, log hbox ~/nd-land/obs-logs/land1.log; R 8fa84977 on 655ff42):
  build GREEN, 25 of 27 rows ok; the two not ok were wall-clock UNREADs, not reds: `rows --deployed` and
  `cargo:launcher:resident_bell` past 600 s at load ~50. Re-run untimed from the landing tree: resident_bell `1 passed`
  (542 s), `rows --deployed` ALL PASS. Main had moved meanwhile.
- LANDING 2 (land2.log; R a90c9d07 on 9cf567d): all 27 rows ok (judge GREEN), push refused (main moved), replay
  CONFLICT in Lang/Journey/Readme.lean (README journey RM0 added beside my genesis threading): resolved by hand (their
  lines, with the budget argument), rebased onto 57111733; tree GREEN (862 jobs), rows ALL PASS, lang-journey GREEN.
- FOLLOW-UP folded in (commit 2): the `health` row asserts the fourth counter — the sponsor's receipt must print its
  `bytes` line, and a new relay fault `forgeBytes` ("wrote nothing", bytes 0 over the same paths) is refused
  `pathMismatch`; `trustReceipt` plant still caught at line 14. Rows ALL PASS.
- LANDING 3 launched (land3.log): fddf566e (kernel!) + 308877b7 (protocol) on 8fe58cb.

- FROM OPS (2026-10-27, HOST-83, coordination only, nothing built on OBS's side): the writer's liveness is now the
  service manager's (nd-supervise pings `host serve`'s loop and keeps systemd's WatchdogSec alive per answer; the unit
  pages via `OnFailure=`). What a MEMBER can see of the writer from its own copy is the health receipt's to print, one
  line asked: every `log` page states the writer's newest base (PROTOCOL-47's `logReplyLayout` base fields), so follow
  knows the STEP of the writer's last seal and the local time of the last page it took from the writer. A receipt line
  such as `writer sealed at step S; last page from it at T (this machine's clock)` would let a member tell a dead or
  stalled writer from a quiet one. Bases carry no wall-clock time, so "last seal time" is the member's own clock at the
  page that first showed that base, never the writer's word. OPS owns nothing of it; take it or decline it here.
- LANDING 3 (lander pid 2919240 on hbox; its log file was removed by the coordinator's sweep, so it is read through
  /proc/2919240/fd/1 and copied to hbox ~/nd-land/obs4-land3.log): all 27 rows ok on 8fe58cb (R 3ec14ebd); the push
  found main moved over 5 of this change's paths (Lang/Journey/Gen.lean, Readme.lean, Web/Sim/Testground.lean, …),
  so scripts/commit is re-building and re-running by its own rule. Hashes: see the PARKED line below.

## Continuation (FABLE-OBS-4 parks here, by the coordinator's instruction)

- If the lander pushed: the two commits are on main (kernel! bytes meter, KERNEL-78; protocol health row). Nothing
  else of this lane is open.
- If it did not: hbox worktree ~/nd-land/obs holds the two commits (fddf566e, 308877b7 before any replay); rebase
  once onto origin/main, resolve (the conflicts so far were genesis-call threading in new journeys: add
  `Nanodregg.Kernel.Bounds.bytesPerWindowMax` after the allowance and `World.genesis X.env 0 0 0`), rebuild only what
  the rebase touched, and run `ND_LAND_DIR=$HOME/nd-land/obs-land scripts/commit` detached with a PID file.
- Handed off: the testground's bytes demo (a World with a small `bytesBudget`, a member writing until `bytesBudget`)
  and the wasm kernel rebuild are the testground lane's (TESTGROUND.report.md line). Cards still open from
  DESIGN-OBS §5: the meter fold theorem (01a176d9-0005), `Right.ticks`/`Right.bytes` per-member caps (01a176d9-0014),
  the window-trie rename (01a176d8-ffe9).
