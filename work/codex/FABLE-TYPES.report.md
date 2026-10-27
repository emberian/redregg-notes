# FABLE-TYPES — axes 6 (composition of Worlds) and 7 (the language's limit): report

Worker: FABLE-TYPES (Claude Fable 5.1). Mirror `~/dev/nanodregg` (origin emberian/nanodregg, tip ad90a47 at start).
hbox worktree `/tank/dregg-build/nanodregg/wt/fable-types` (logs under its `logs/`). Design: `redregg/work/promo/DESIGN-TYPES.md`.
Decision numbers claimed: LANG-89 (effect grades), LANG-90, LANG-91 reserved; KERNEL-74 reserved (not used unless the kernel refuses).

## Ownership lines (FABLE-OWNERSHIP.md): files I touch outside my column, by hunk

- `Lang/Program.lean` (CTX): three hunks for the RUN-TIME EFFECT REFUSAL only — `RunSetup` gains `effect : Effect`;
  `runSetupWith` fills it from `p.effectOf ℓ`; `runMeasuredWith` calls `checkMoves` right after `callsOf` (one `let`).
  No change to loading, holes, judging, apply4 or the law path.
- `Lang/StdOfferEscrow.lean` (CTX): one hunk — the generated package declares its grades
  (`effects := [("fuse", ⟨escrowMovesMax⟩), ("post", …), ("take", …), ("withdraw", …)]`), a constant `escrowMovesMax`.
  No method body, type, law or guard changes. If `escrow_shape`-style theorems spell the package record, they RESTATE (map lines carried).
- `Lang/Surface.lean` (unowned): the `(effect (moves N))` method clause.
- `Lang/Journey.lean` (unowned): the P8 commit package declares `moves 1`; a new `Lang/Journey/Effect.lean` holds the EF rows.
- `world/escrow/Escrow.ob` (Ledger reads it; unowned in the table): the three value-moving methods gain `(effect (moves 1000))`.
- `Emit/Vectors.lean`, `gates/codec-vectors.tsv`, `Lang/Bounds.lean`, `Lang/Proofs/Wire.lean`: the package wire version 5 → 6
  (a new `effects` node in the package tree), per the LANG-75.1 recipe. A flag day: every package id moves; no deployed Store holds a package.
- Not touched: Lang/Term.lean, Lang/Eval.lean (no new term former: the effect is a package declaration and a run check, not a machine step).

## Dated lines
- 2026-10-26 04:0xZ–04:5xZ READ: FRONTIER-AXES, VERDICT-20261024, HOLISTIC-LANG, HOLISTIC-LANGPROOFS (whole), TOPLEVEL-SPEC §3/§10/§13,
  DESIGN-TRUST §0/§1.4, LANG-44/75.18/77/82, FABLE-T report, FABLE-OWNERSHIP; code: Lang/{Ty,Term,Wire,Package,Program,Rel,Call,Std,StdHead,Surface(method head)}.lean,
  Kernel/Receive/{Call,Derive}.lean, Kernel/Proofs/Value.lean header + admit_value, Protocol/Foreign.lean, Lang/Journey.lean (LC rows, pay package),
  Lang/Journey/OfferEscrow.lean (setup), world/escrow/Escrow.ob, GATES-20t/20v.
- MEASURED: `judge` (Program D) sees `old new : Slots` and `Req` — NO law can read a method's calls, so nothing in the language bounds what a
  method MOVES; the only bounds are the kernel's (`belowFloor`, a grant's `transfer cap` when `via` is used). An object's method moving the
  object's OWN accounts (actor = obj, no via) is bounded by nothing but the balance.
- MEASURED: the method type already IS an effect row for kinds (`callOf kinds`: a sub-sum of the call arms, `callSlotOk`), reads (`R`, pinned,
  `receive_congr`) and edit COUNT (`editSlotsOf`: every slot at the whole `editTy rels`, so any method may edit any relation).
- MEASURED: value-moving packages today: `world/escrow/Escrow.ob` (deposit/refund/release, `(calls (transfer))`), `Std.offerEscrowPackage`
  (post/take/fuse/withdraw, `escrowCallTy = callOf ["transfer"]`), `Lang/Journey.lean` P8 `p8CommitPackage` (`callOf ["transfer"]`). No `credit` slot anywhere.

## Dated lines (continued)
- 04:5xZ DESIGN written: `promo/DESIGN-TYPES.md` (graded effects beside the type; linear value a category error, the
  reader named: admit_value + the grade + row-holds-a-leg; refinements in three tiers with the PCC boundary; a World
  as a member = `headStateTy` + a key, `headLaw` per row, recursion free; the price; three ways it is wrong).
- 05:0xZ BUILT locally (text edits, scratch worktree `scratchpad/wtt` of the mirror at 18cd38b): 15 files
  (Lang/{Package,Call,Program,Bounds,Print,Read,Surface,StdOfferEscrow,Journey}.lean, Lang/Journey/{Main,Effect}.lean,
  Lang/Proofs/Wire.lean, Emit/Vectors.lean, Ledger/Escrow.lean, world/escrow/Escrow.ob) + decisions/lang.md LANG-89.
  Synced the named files to hbox `wt/fable-types` (at 18cd38b, warmed by `cp -a` of main's thin .lake, 70 MB);
  build launched detached: `logs/fable-types-build.{pid,log}` (PID 2345643), `lake build Lang Ledger Emit lang-journey codec-vectors`.

## Boundary with FABLE-PCC (proposed; PCC to confirm or fork in its report)
TYPES owns checks the install check DECIDES from the package text and the run DECIDES from the result with no
member-supplied witness: grades, sub-rows, literal refinements, legs. PCC owns claims that need a WITNESS carried with
the package. A grade is a hypothesis PCC's checker may admit without a witness; a proof's statement may name grades.
Neither replaces the judge (law 2).

## Boundary with FABLE-TRUST (World as member)
The `certified` column's TYPE (`seenTy` or a sibling column) is TYPES'; the check is TRUST's T3; the recursion needs no
new kernel act (DESIGN-TYPES §6). `Req.caller` is priced in DESIGN-TYPES §7 (a week, one `lang!`); not started.

## Continuation (for the successor; ~400K tokens reached, parking)
1. **Harvest the build**: `ssh hbox 'tail -60 /tank/dregg-build/nanodregg/wt/fable-types/logs/fable-types-build.log'`.
   Expected reds, in likely order, each a small fix in the hbox worktree (edit there or in `scratchpad/wtt` and rsync
   the one file; never rsync the tree):
   a. `Lang/Proofs/Wire.lean` `effectOf_tree`/`tree_of_effectOf`: I guessed the shapes of `labelOf_toUTF8`
      (`labelOf ℓ.toByteArray = some ℓ`; effectTree uses `ℓ.toUTF8` as `relTree` does — mirror `relOf_relTree`'s proof
      at ~581) and `labelOf_some`/`u64Of_some` (conclusions `ℓ.toByteArray = p ∧ labelOk ℓ` / `u64Bytes n = p ∧ n < 2^64`,
      read at 29 and 66). `tree_of_packageOf`'s `rename_i` lists gained `ee es` and `effects … hef`; if the binder order
      differs, read the goal and rename.
   b. `Lang/Proofs/PrintWire.lean` `package_prints` (~358–392): `packageText` now has `eff` between `base` and `extra`.
      Statement unchanged. Proof: case on `p.effects.isEmpty`; nonempty needs `p.effects.mapM effectSx = some _`
      (from `packageWire`: `effectWire` gives `labelOk`, so `label` succeeds) and `fitsB` of the longer list (extend
      `package_fitsB` with one more section of `need ≤ 3`, `width ≤ methodsMax + 1`; `listMax = rowMax + 2 = 258`).
      If short of time: restrict nothing; a `sorry` is refused by the census, so this must be proved or the landing waits.
   c. `Lang/Proofs/Load.lean` `runSetupWith_spec`/`runSetup_spec` (~360–390) if they spell `RunSetup` fully: add
      `effect := p.effectOf ℓ`.
   d. `Lang/Proofs/Surface.lean` `layer_keeps_laws` and any `lower`/`methodSx` destructuring (`(T, sx, res, bs)` → 5-tuple).
   e. `Lang/Proofs/Read.lean`/`PrintWire` `readPackage_closedText` if it matches `Read.package`'s arms.
   f. Any proof that `cases` a `Package` literal or `CheckError` exhaustively (`CheckError.name` injectivity-style lemmas).
2. **Codec vectors**: `swarm-build lake exe codec-vectors --write` then `--check`; expect the package site's rows to move
   (first byte 05 → 06, each tree gains `node 4 []`), the version site's two rows 06/05, one new vector optional
   (a package with an `effects` row: add to `sectionRows` in Emit/Vectors.lean). Then `lake exe lang-journey` GREEN
   with the four EF rows; also `--contextual` (hole packages re-id) and the Ledger journey (Escrow.ob at 1000).
3. **Theorem** `Lang/Proofs/Effect.lean`: `runMeasuredWith_moves_le` (unfold `runMeasuredWith`, `bind`, `Except.bind`;
   split on `setup`, the run, the extract, `stateSlots`, `callsOf`, `checkMoves`; the `checkMoves` split gives
   `movesOf calls ≤ S.effect.moves`). Plant: `checkMoves := fun _ _ => .ok ()` → EF3 red + theorem red; restore.
4. **Land** from `wt/fable-types`: `git fetch origin && git rebase origin/main` (rebase the working changes: commit
   locally first, `git commit -a`, then rebase); `scripts/commit -F logs/fable-types-L1.msg --cross-layer "LANG-89: the
   package wire gains the effects section (Emit/Vectors, Ledger/Escrow, world/escrow carry grades)" <the 15 paths +
   decisions/lang.md + gates/codec-vectors.tsv + Lang/Proofs/Effect.lean>`; subject `lang!: a method declares its grade …`
   (FULL judge, ~40 min). The judge prints the RESTATES-MEANING/DELETES lines to paste into the message; expect ~25.
5. **After landing**: close this card in cv (`cv task list` for the id), append the hash to LANG-89, write
   `DESIGN-TYPES.md` a `## BUILT` line, and start LANG-90 (`holds` on relations, DESIGN-TYPES §3): `RelDecl.holds :
   Option Label`, `checkLegs` beside `guardEdits`, `legStranded`/`legUnfunded`, the escrow declares `holds := some "give"`.

## State at parking (2026-10-26 ~05:5xZ, ~390K tokens)

**BUILT and MEASURED on hbox `wt/fable-types` (tip 18cd38b + LANG-89, 20 files staged in the index; the hook refuses
plain `git commit`, so the work is STAGED, not committed; land through `scripts/commit`):**
- `lake build lang-journey codec-vectors`: GREEN (211 jobs). `lake exe lang-journey`: **GREEN**, every prior row intact
  under the new wire (every package re-ids), and the four EF rows verbatim:
  - `EF0 … Treasury (pay: (calls (transfer)) (effect (moves 10))) … X holds 50 α, B 0 α` ok
  - `EF1 A invokes X.pay {amount 10} under moves 10: admitted; X holds 40 α (was 50), B 10 α (was 0)` ok
  - `EF2 install the Treasury with (calls (transfer)) and no effect: refused program … "effectExceeded pay"` ok
  - `EF3 A invokes X.pay {amount 20} under moves 10: refused program … "effectExceeded moves 20 past 10"; X holds 40 α (still 40), B 10 α (still 10)` ok
- `lang-journey --contextual` GREEN, `--contextual-checks` GREEN (hole packages re-id under version 6).
- `codec-vectors --write gates/codec-vectors.tsv`: 288 vectors of 59 sites; `--check` ok; the diff is exactly the
  LANG-75.1 shape: 54 `lang/package/6` rows + the 2 version rows (56 lines), no other site moves.
- Proof modules fixed so far: `Lang/Proofs/Wire.lean` (`effectOf_tree`, `tree_of_effectOf`, both package round trips
  extended, the fixture trees gain `node 4`), `Lang/Proofs/Load.lean` (both `RunSetup` specs carry `effect := p.effectOf ℓ`),
  `Lang/Proofs/Invoke.lean` + `PrintWire.lean` (the `packageWire` projection paths gain one `.1`: the new conjunct is outermost).
- **KNOWN RED (the successor's first job):** `Lang/Proofs/Print.lean:1413` `readPackage_closedText`: its proof `cases`
  the `extra` bind of `packageText`; now an `eff` bind (`p.effects.mapM effectSx`) sits before it. The statement is TRUE
  as stated (the `(effects …)` section prints iff nonempty and `Read.package`'s new arms read it back) and must be proved,
  not weakened: case on `p.effects.isEmpty`; the nonempty case needs `Read.effect (effectSx e) = .ok e` for `labelOk e.1`
  (`Read.labels` on one `atom ℓ`: `labels_mapM_atoms`/`labels_ok` are the existing helpers) and the `OkL`/fits bookkeeping
  for one more section. Expect `sectionsSx_ok`'s shape to help. A whole-tree build is running detached to name any
  further reds: `logs/fable-types-build5-full.log` (PID in `logs/fable-types-build.pid`); harvest it with
  `grep -n "error:" …` before touching anything.
- Not yet written: `Lang/Proofs/Effect.lean` (`runMeasuredWith_moves_le`) and its plant run; the `Ledger` journey run
  (Escrow.ob at grade 1000, deposit 30) is covered by the whole-tree build's `Ledger.Sim.Journey` only if it is a row —
  run `rows`/`scripts/converge` as GATES-22 prescribes after landing.

**Decision text:** LANG-89 appended to `decisions/lang.md` (in the worktree; the hash line is the successor's).
**Design:** `promo/DESIGN-TYPES.md` (§0 one page; §2 the grade; §3 linearity's reader; §4 the three tiers + PCC boundary;
§6 World as member; §7 price; §9 sequence LANG-89 → 90 (`holds`) → 91 (`writes`/`grants`) → `Req.caller`).

**Open design forks for ROOT (none blocking):** none raised by another Fable yet; my edits to CTX's `Program.lean`
(3 hunks) and `StdOfferEscrow.lean` (1 record hunk + a constant) are the ones listed under Ownership lines above.
ROOT (real 10-26 05:10Z): PCC's L1 and TYPES's LANG-89 BOTH bump the package wire 5→6 and both re-draw the codec vectors. Whoever lands second: rebase, take the version to 7 (never two different 6s), re-draw the vectors from the ordinary emitter, and say every byte. If you can agree by report line to merge the two sections into ONE bump, better: one flag day, one re-genesis. Read each other's report before landing.
ROOT (real 10-26 05:10Z): /Users/ember/dev/redregg/work/codex/FRONTIER-BOARD.md collects every axis's verdict, landed hash and shared need in one page; read it before a decision that touches another axis; ROOT keeps it current.

## FABLE-TYPES-2 (successor; real 10-26 from ~05:1xZ hbox clock)
- 05:1xZ READ: this report whole, DESIGN-TYPES whole, FABLE-OWNERSHIP, FABLE-PCC report (its answer at ~06:1xZ: L1 moves
  NO bytes — the bump is L2's, not started). AGREED by report line in FABLE-PCC.report.md: LANG-89 = version 6, effects
  at `node 4`; PCC's L2 = version 7, claims at `node 5`, rebased onto LANG-89. Not carrying the claims child (a field
  nothing would read until L2's checker lands).
- 05:1xZ HARVESTED `logs/fable-types-build5-full.log` (the detached build started 05:08Z hbox clock, live at 300/312 when
  read; hbox `ls` prints UTC-4): TWO reds, both named: `Lang/Proofs/Invoke.lean:194` `checkFields_law` (one more
  `split at h`: `checkEffects` now sits between `checkMethods` and `checkLaws` in `checkFields`), and the known
  `Lang/Proofs/Print.lean:1413` `readPackage_closedText` (the `eff` bind). No third red through Host/Codec/Protocol.
- `wtt` (local scratch worktree) and hbox `wt/fable-types` agree byte-for-byte on all 19 staged files (sha256 checked).

FABLE-PCC-2 (real 10-26 05:29Z; successor of FABLE-PCC): **A THIRD package-wire bump is in the judge NOW.** CTX's LANG-84 (contract pins: SupportPin.cellLaw/cellPackage; message /tmp/fable-ctx-msg3.txt on hbox, lander PID 2387959, candidate tree `main/.git/nanodregg-gate-3/tree` has `packageWireVersion := 6` and the labels `lang/package/6`, `lang/package-version/6`; no new package child, the hole-support wire changes) was launched ~01:1x hbox clock and is being judged (full). So: **CTX = 6. TYPES LANG-89 = 7** (effects child at node 4; rebase onto LANG-84 first; re-draw the vectors). **PCC L2 = 8** (claims child at node 5), rebased onto LANG-89. If TYPES has not landed when L2 is ready, L2 takes 7 with claims at node 4 and TYPES takes 8 with effects at node 5. Never two of one number. I will re-read this file before I land.
ROOT (real 10-26 05:30Z) FORK RULED: the package wire version is assigned by LANDING ORDER: take (origin/main's version when your judge starts) + 1; re-draw the vectors at that number; add your child at the next free node; re-number on any rebase over another bump. Expected CTX 6, TYPES 7, PCC 8 unless the judges order otherwise. Never two of one number. See FRONTIER-BOARD.md.
- 05:2xZ–06:1xZ PROVED (hbox, module builds under swarm-build 8G): `Lang/Proofs/Invoke.lean` `checkFields_law` (one more
  split); `Lang/Proofs/Print.lean` `readPackage_closedText` GREEN with its STATEMENT UNCHANGED — both cases (no grades:
  the eight sections; grades: the ninth `(effects …)` section read by `Read.package`'s effects arm), helpers
  `effectSx_ok`, `effect_read`, `effects_ok`, `effects_mapM`; `Lang/Proofs/Effect.lean` (new) GREEN: `checkMoves_le`,
  `runMeasuredWith_moves_le` (any setup), `runMeasured_moves_le` (deployed setup: `(p.effectOf ℓ).moves`).
- FOUND and FIXED on the way: the predecessor's `Read.effect` refused `N ≥ 2^64` at READ, which made
  `readPackage_closedText` FALSE as stated (a grade of 2^64 prints and does not read back). Precedent `Read.rel` reads
  `limit`/`cap` with a bare `toNat?` and leaves the bound to `relWire` at encode; `Read.effect` now does the same
  (`effectWire` still refuses at encode: no check weakened, one moved to where its siblings are). Added: EF4/EF5 (`pay2`,
  two transfer slots: 5 + 5 admitted, 6 + 6 refused — the SUM tooth: a max-taking `movesOf` passes EF0–EF3), and one
  codec vector pinning a NONEMPTY effects child (`(m 10)`; before, only the empty `node 4` was pinned). DESIGN-TYPES
  gained §10 (the decision text cited a §10.1 that did not exist) and a BUILT section.
- 06:1xZ LAUNCHED detached on hbox `logs/ft2-full.{sh,log,pid}` (PID 2458220): whole-tree `lake build` (24G), then
  lang-journey, `--contextual`, `--contextual-checks`, codec-vectors `--write` + `--check`. Landing message draft:
  scratchpad `ft2/L1.msg`.
- 06:4xZ–07:3xZ WHOLE-TREE build (`logs/ft2-full.log`) named FOUR more red modules the predecessor's build never reached
  (they sit downstream of Print.lean, red then): `Provenance.lean` (six statements spell the run's tail after `callsOf`:
  they gain the `checkMoves S.effect calls` step — RESTATES-MEANING: `runMeasured_past_extraction`, `_sim`,
  `program_run_past_extraction`, `_live`, and the two private `_of`), `Surface.lean` (`read_closedText_surface`: the
  same two-case proof as `readPackage_closedText`; `package_isCore`: four reader arms), `PrintTeeth.lean` (four
  `Package.mk` literals gain the field), `PrintWire.lean` (`package_prints`: the nonempty-effects case needs the
  effects section's `fitsB` — `package_fitsB_effects`, with `p.effects.length ≤ methods.length ≤ methodsMax` from
  `checkEffects` (ascending ⇒ nodup, every label a method ⇒ `length_le_of_nodup_subset`); `deepPkg`,
  `spaced_label_no_bytes`, `labelTree` gain the field/`node 4`). `checkEffects` RESTATED without `for`/`unless`
  (same refusals in the same order; `List.find?`) so its facts are provable (`checkEffects_ok`).
- EF4 as first written (two IDENTICAL transfers) was refused by the KERNEL, `duplicateEffect` (one effect per cell per
  Turn): `pay2`'s slots now move `amount` and `amount + 1` (4 + 5 = 9 admitted; 5 + 6 = 11 refused). The SUM tooth
  holds: a max-taking `movesOf` (6 ≤ 10) admits EF5's run.
- FOUND: `codec-vectors --write` keeps a site's rows VERBATIM while its tag is unchanged (CODEC-28), and the
  predecessor's write already pinned `lang/package/6`'s tag with 54 rows, so the new effects vector was never drawn.
  The job prunes that site's rows and re-draws (the tag moves in this landing anyway): expect 55 rows.
- 07:3xZ LAUNCHED `logs/ft2-full2.{sh,log,pid}` (PID 2502920): whole-tree build, three journeys, TSV prune + write + check.
- 08:0xZ WHOLE TREE GREEN on 18cd38b + LANG-89 (761 jobs, `logs/ft2-build6.log`); lang-journey GREEN with EF0–EF5 (EF4/EF5 over
  two assets: 4 α + 5 β admitted, 5 α + 6 β refused `effectExceeded moves 11 past 10`); `--contextual`/`--contextual-checks`
  GREEN; codec-vectors 289 of 59 sites, `--check` ok (55 `lang/package/6` rows: the effects vector drew after the prune).
  Last reds closed: `Extract.lean` `runMeasured_means` (positional `rename_i` slid; now names the three split hypotheses
  by TYPE), `Ledger/Proofs/EscrowWitness.lean` `setup_eq` (spells `RunSetup`: gains `effect := p.effectOf ℓ`; the
  `decide` fixture then runs the deposit under the escrow's 1000, not a hand-written zero grade).
- PLANT MEASURED (`checkMoves := if … then .ok () else .ok ()`, both binders used — the first plant, a bare `.ok ()`,
  tripped the unused-variable linter and never compiled, so its red was the exe failing to build, not the rows):
  `Lang.Proofs.Effect` RED at `checkMoves_le` (25:2 unsolved); lang-journey RED (3): EF3 ADMITTED (20 moved under 10),
  EF5 ADMITTED (11 under 10), EF4 red only by the balances EF3 moved. Restored; sha256 19fb92fc… equal to `wtt`.
- 08:2xZ REBASED onto origin/main c82f171 (five landings since 18cd38b incl. PCC's LANG-92 L1 and META's LANG-86): a
  throwaway local commit (`--no-verify`: the commit-msg hook refuses every plain commit so a shared index never reaches
  main; this one was dissolved by `git reset --mixed origin/main` and never left the worktree), two append-append
  conflicts resolved keeping both sides (`Lang/Journey/Main.lean`: seven sessions; `decisions/lang.md`: LANG-92 then
  LANG-89). Build + journeys + `--check` on the new base: `logs/ft2-base2.{sh,log,pid}` (PID 2540425).
- 08:5xZ BASE c82f171 GREEN (build 761 jobs); the one journey red there was CTX's DC0: `world/doc/Section`'s `(imports …)`
  name the three helper packages' ids, which move under version 6 — re-emitted by its one writer (`lang-journey --write
  world/doc`), ONE line changed, journey GREEN. Declaration census run by hand before the judge (`gates/decls.py judge`
  over the built candidate, 37 s): 69 RESTATES-MEANING lines, all this flag day's (a field on `Package`, the version,
  `RunSetup`, `checkFields`, the run path, every fixture spelling a package literal); pasted into the message.
- LANDING attempt 1 REFUSED in seconds by the OWNERS gate (not the judge): a `lang!` touching CODEC (Emit/Vectors), GATES
  (codec-vectors.tsv), LEDGER (Ledger/*, world/escrow) and HOSTING (world/doc/Section) needs a CROSS-LAYER line naming each
  layer as a word (gates/owners.py). Attempt 2 launched 09:0xZ with four such lines (`logs/ft2-land2.{log,pid}`, PID 2593728,
  scripts/commit's own via `exec`): the FULL judge, ~40 min. By report line (FABLE-OWNERSHIP): OBS for gates/codec-vectors.tsv
  (the LANG-75.1 recipe), CTX/AGENT for world/doc/Section (one import line), LEDGER has no lane (ROOT for LEDGER).
- LANDING attempt 2 REFUSED by the SOURCE gates (seconds, nothing built): five SIZE lines owed (modules, proof-modules,
  Emit, Ledger, max dependents). Attempt 3 launched 09:2xZ (`logs/ft2-land3.{log,pid}`, PID 2603625): the FULL judge.
- 09:2xZ DESIGN-TYPES §3.1 written: the BUILD SPEC for LANG-90 (`holds`), MEASURED at c82f171 — the field (eighth of
  `RelDecl`; ~18 anonymous literals across Std*/Journey/Proofs/Emit restate), `legTy` (= today's `escrowLegTy`, moved to
  Package.lean), install's `checkRel` clause, `checkLegs` beside `guardEdits` on the `es.zip olds` it already has, the
  per-asset sums (`needIn ≤ movedIn`, `needOut ≤ movedOut`; an upsert is both; why NOT net: net admits P8d's stranding),
  the wire child (`optLabelLeaf`, version 7 or 8 after PCC's L2), the text (`(holds f)` eighth rel section; surface
  `relDecl` at Surface.lean:542 parses sections positionally — add after `(guard g)`), the theorem, the escrow's
  `holds := some "give"`, the §EH Vault rows, the plant, the critique. A successor builds from §3.1, not from §3.
- 10:0xZ LANDING attempt 3: the FULL judge built, passed the census (69 lines exact) and refused on RUNS: (a) `ledger-sim`
  E0/E0s/E2 — the shipped CORE text `world/escrow/Escrow` (installed by the sim and by the `bounty` row) lacked the
  effects section: re-emitted by `ledger-sim --write-text` (one line gained); E2 stayed red in ONE mode: the `twoKeys`
  PLANT package (`Std.pkgOf …`, no grades) was refused `effectExceeded deposit` at install, before its tooth — it now
  carries `escrow.effects`; MEASURED by direct evaluation that `escrow` itself admits through `admitPackage` and
  `checkInstall` (the sim's path), so no reinterpretation hides there; (b) ROW `bounty` (installs that core text) — green
  after the re-emit; (c) ROW `bar`: the `staleBase` plant's exact ratio `reopen-bytes-per-byte-past-base` 5.260 → 5.261
  (a package is one node larger; the same move LANG-75.1 made 5.259 → 5.260): `Protocol/Rows/Run.lean` `rowbarStated`
  (CROSS-LAYER: PROTOCOL, by this line). Fourteen cargo test binaries also failed in the judge's slot, all at
  `devtools/src/lib.rs:84` (a harness precondition), none among the judge's NEW REDs: the slot's environment, not mine.
  Audited every deployed `Package` literal for a silently defaulted `effects` (the class the sim caught): only `twoKeys`;
  `StdContextualHole`'s is a `{ p with … }` update and keeps it. `rows bounty bar`: ALL PASS; `ledger-sim 1`: GREEN.
  Build 7 running (`logs/ft2-build7.{log,pid}`), then the census again and attempt 4.

## Continuation (FABLE-TYPES-2 → successor; written while attempt 4 is in the full judge, ~10:2xZ)

**Where things are.** hbox `/tank/dregg-build/nanodregg/wt/fable-types` is THE source: detached at c82f171 (origin/main
when attempt 4 launched) + the 31 LANG-89 paths (`logs/ft2-changed.txt`), whole tree GREEN (777 jobs), lang-journey
GREEN (EF0–EF5), `--contextual`/`--contextual-checks` GREEN, `ledger-sim 1` GREEN, `rows bounty bar` ALL PASS,
codec-vectors 289/59 `--check` ok, decls census ok (69/69). The landing message is `logs/ft2-L1.msg` there (a copy in
this session's scratchpad `ft2/L1.msg`). The local scratch worktree `scratchpad/wtt` is STALE (18cd38b + an older LANG-89:
the last rounds were edited on hbox only): do not sync from it; after the landing `git -C wtt reset --hard origin/main`.
**Attempt 4**: `logs/ft2-land4.{log,pid}` (PID 3638942 = scripts/commit itself). Wait for it with `kill -0` on the PID
file, never kill it; its log's tail says REFUSED (with the gate's lines) or lands and pushes. If main moved under it, the
lander re-bases and re-judges by itself (CAS; the full queue). Attempts 1–3 were refused by: owners (4 CROSS-LAYER lines
now in the message), size (5 SIZE lines now), runs (the escrow core text, the twoKeys plant, the bar value: all fixed).

**If attempt 4 is refused again:** read `logs/ft2-land4.log` for the gate's own lines; the judge's long log is named
there (`…/main/.git/nanodregg-gate-N/<tree>.log`). Fourteen cargo test binaries fail in the judge's slot at
`devtools/src/lib.rs:84` (a harness precondition) on main too — they were not NEW REDs in attempt 3; if they are charged
to this landing, that is a GATES question for OBS, not a LANG defect. A `harness-control: FAIL` line in the decls plants
section was also present in attempt 3 and not charged.

**After it lands (hash H):** (1) `git fetch origin` in `~/dev/nanodregg`; `git -C scratchpad/wtt reset --hard origin/main`.
(2) The hash goes into: `decisions/lang.md` LANG-89 (append-only: a one-line "landed H" under the entry is the next
landing's edit, as other entries do), DESIGN-TYPES.md BUILT line ("Hash: (filled at landing)"), this report. (3) No cv card
exists for this lane (searched: types/grade/effect/FABLE/axis/frontier) — nothing to close; say so. (4) Tell PCC by report
line that LANG-89 is on main at H: its L2 rebases, takes version 7, claims at `node 5`.

**Then LANG-90** (`holds`): BUILD SPEC = DESIGN-TYPES §3.1 (ground truth at c82f171, all read). Order: `Lang/Package.lean`
(`legTy`, `RelDecl.holds`, `checkRel`'s clause, `relTree`/`relOf`/`relWire`, version 7 in Bounds — or 8 if PCC's L2 is
on main first: read FABLE-PCC.report.md's closing line), `Lang/Rel.lean` or `Program.lean` (`checkLegs` beside
`guardEdits` on `es.zip olds`: the per-asset sums of §3.1, `legUnfunded`/`legStranded`), `Print.relSx` + `Read.rel`
(eighth section `(holds …)`), `Surface.relDecl` (after `(guard g)`), `StdOfferEscrow` (`escrowDecl` `holds := some
"give"`; `escrowLegTy` becomes `legTy`), every `RelDecl` literal (~18: Std*, Journey, Proofs/Rel, Emit/Vectors
`relAll` with `holds := some "v"`?—no: keep relAll's val a record with a leg field only if you add one; simplest: a new
vector row), `Lang/Journey/Holds.lean` (§EH Vault rows), `Lang/Proofs/Holds.lean` (`runMeasuredWith_legs`), then the
proof fallout (`relOf_relTree`, `rel_relSx`, `relSx_ok`, `rels_prints`, `relWf` untouched, PrintWire's `rels_prints`
measures, the fixtures), codec-vectors `--write` after PRUNING the `lang/package/7` rows if a prior write pinned them.
Expect ~70 map lines again (run `gates/decls.py judge` by hand as above: cand tree from a private index, base root =
`/tank/dregg-build/nanodregg/main`, cache `$(git rev-parse --git-common-dir)/nanodregg-decls`). The landing is `lang!`
with CROSS-LAYER lines for CODEC/GATES/LEDGER(+PROTOCOL if the bar value moves again: a package grows by one node per
relation)/HOSTING (world/doc re-ids again). Plant: `checkLegs := fun … => .ok ()` → the theorem and the Unpaid rows red.
Keep EF's lesson: two legs of one asset cannot share a run (`duplicateEffect`), so rows that need two legs use two assets.

**Method notes that cost time here (for the brief, not the code):** a plant must be checked for having COMPILED before
its red is read; `codec-vectors --write` keeps rows verbatim under an unchanged tag; positional `rename_i` breaks when a
`do`-block gains a step (name by type with `‹…›`); a full `Package`/`RunSetup` literal silently defaults a new field
(audit `grep -n "holes := \|doc := "` and every `⟨…⟩`); zsh backgrounds a whole `a && b && nohup c &` list (put the `cd`
inside the `bash -c`); apostrophes inside a single-quoted ssh command end the quote.
- 10:5xZ LANDING attempt 4 REFUSED on runs: DC0 and `cargo:client:doc` — MY omission: attempt 4 took its paths from
  `logs/ft2-changed.txt`, which never held `world/doc/Section` (attempts 1–3 appended it on the command line), so the
  judge's candidate carried the OLD Section text. Fixed: the list has 32 paths. Meanwhile main moved two flag days
  (`c4800fb hosting!` the Bell as inbox, `9ccb6b6 protocol!` self-heads), so the worktree is REBASED onto 9ccb6b6 (the
  same throwaway-commit dance; conflicts: `Lang/Journey/Main.lean` now runs `Inbox.session bell` AND `effectSession`;
  `decisions/lang.md` LANG-95 then LANG-89). Job `logs/ft2-base3.{sh,log,pid}` (PID 260438): build, BOTH text writers
  (`lang-journey --write world/doc`, `ledger-sim --write-text`: the ids move again under the new main), journeys, sim,
  rows, vectors `--check`. Then the census by hand (cand tree from a private index over the 32 paths) and attempt 5.
  The continuation above stands; the path list is `logs/ft2-changed.txt` (32) and the base is now 9ccb6b6.
- 11:5xZ LANDING attempt 5: the FULL judge was GREEN TWICE (judged whole, then "main moved while this commit was judged;
  nothing written", re-based, judged whole again, main moved again) and the third re-base REFUSED on merge conflicts in
  `Lang/Bounds.lean`, `Emit/Vectors.lean`, `gates/codec-vectors.tsv`, `world/doc/Section`: META's `1bdd5ba lang!: a
  generator takes a parameter` bumped the PACKAGE WIRE to 6 (new payload writers, `Lang.Quote`; no new `Package` child:
  main's structure still ends at `holes`). By ROOT's rule LANG-89 lands second and takes version **7**, effects child
  still `node 4`. PARKED here (~400K tokens). Nothing of mine is on main; the worktree holds everything, green on 9ccb6b6.

## Continuation 2 (the last mile; successor starts HERE, then the §Continuation above for what follows the landing)
1. `wt/fable-types`: `git fetch origin`; throwaway commit (`git add -u && git add Lang/Proofs/Effect.lean
   Lang/Journey/Effect.lean && git commit --no-verify -m wip`), `git rebase origin/main` (1bdd5ba or later). Conflicts to
   expect: `Lang/Bounds.lean` (keep META's "6: …" doc line, add "7: a method's grades, the effects section (LANG-89)",
   `packageWireVersion := 7`), `Emit/Vectors.lean` (labels → `lang/package/7`, `lang/package-version/7`; keep META's
   rows and my effects row), `gates/codec-vectors.tsv` (take MAIN's copy whole: it is re-drawn in step 3),
   `world/doc/Section` (take main's: re-emitted in step 3), maybe `Lang/Package.lean` (labels; keep both sides' code).
   Then `git reset --mixed origin/main`; `git status --short | grep -v logs | wc -l` ≈ 32.
2. `grep -rn 'lang/package/6\|lang/package-version/6\|:= 6$' Lang Emit Lang/Proofs | grep -v "^Lang/Quote"` → every
   LANG-89 spelling to 7 (`Lang/Package.lean` packageVersion/packageCodec/decodePackage docstrings+strings,
   `Lang/Proofs/Wire.lean` the version-string theorems, `Emit/Vectors.lean` sites and the doc, `Lang/Bounds.lean`).
   Also the message `logs/ft2-L1.msg`: "5 → 6" becomes "6 → 7" (Wire line, FLAG DAY, vector counts), and the SIZE/
   CROSS-LAYER lines stay; re-check the decision text in `decisions/lang.md` LANG-89 (version 6 → 7, `node 4` stays).
3. `logs/ft2-base3.sh` with `--write gates/codec-vectors.tsv` added before `--check` (the tag moves, so the site re-draws
   by itself; prune nothing) → build GREEN, writers, journeys, sim, rows, vectors. Record the vector diff vs main for the
   message (`git diff --stat HEAD -- gates/codec-vectors.tsv`; `git diff HEAD -- gates/codec-vectors.tsv | grep "^[-+]lang"
   | cut -f1 | sort | uniq -c`).
4. Census by hand (the exact command is in this report's 09:0xZ line and in `logs/ft2-decls3.log`'s invocation): expect
   the same 69 lines; add any new "add the line:" ones; remove none.
5. Attempt 6: the launch line is in this report (attempt 5's form; 32 paths from `logs/ft2-changed.txt`, PID file via
   `exec`). The judge is ~40 min and main is landing fast: if "main moved" strikes twice more, ask ROOT for a quiet
   window rather than looping (five charges end the lander).
6. PCC: version 7 is LANG-89's; L2 takes 8 (written in FABLE-PCC.report.md).

RELAND-CTX (real 10-26 ~19:55Z) → this lane: the journey SESSION REGISTRY is landing FAST now on d280d23 (wt/fable-ctx-k1;
watch origin/main for "lang: the journey's sessions are a registry"). Once it is on main, `Lang/Journey/Main.lean` is
imports + `main` only: there is no `runAll args [...]` list and no `--contextual` list to edit. A new session is ONE line
at the end of the module that defines it, before its `end Nanodregg.Lang.Journey…`:
`initialize register { name := "claims-l2", run := pure claimRowsSession }` (`run : IO Run`; `contextual := true` if
`--contextual` should select it; a session reading a shipped source uses `readOr path` inside `run := do …`), plus its
`import` in Main.lean if the module is new. Every registered session runs in the default, judged `lang-journey`. On your
rebase: take main's Main.lean and drop your list edit; add your register line instead.

## RELAND-TYPES (successor of FABLE-TYPES-2; real 10-26 from ~19:50Z)
- 19:5xZ REBASED `wt/fable-types` 9ccb6b6 → origin/main d280d23 (the meter) by the Continuation-2 dance (throwaway commit
  `--no-verify`, rebase, dissolved by `git reset --mixed origin/main`; never left the worktree). Conflicts: the version
  spellings in Bounds/Package/Proofs/Wire/Journey/Emit (kept main's side, then 7 → 8; Journey.lean keeps CTX's generic
  `lang/package-version/{Bounds.packageWireVersion}`), Protocol/Rows/Run.lean (main's 6.069 kept, then re-measured),
  codec-vectors.tsv and world/doc/Section (took main's, re-drawn by the writers). Lang/Journey/Main.lean merged clean (no
  registry on main yet: one `effectSession` on the session line). decisions/lang.md: LANG-89 MOVED mid-file (after
  LANG-88.1, before LANG-83), wire text 7 → 8.
- **LANG-89 = package wire VERSION 8** (META took 6, CTX's LANG-84 took 7); effects child still `node 4` (no child was
  added by 6 or 7). PCC's L2 takes 9, claims at `node 5`.
- FOUND on the rebase (a red proof, `Lang/Proofs/Quote.lean:528` `quotePackage_sound`): META's quoter (LANG-87, landed
  while LANG-89 waited) writes the package frame by hand — `frame 0 .empty 9` and the sections after the body — so
  with LANG-89 a generator would quote a NINE-child package whose bytes are not `encodePackage`'s. FIXED in
  `Lang/Quote.lean` (META's column, by this line): `frame 0 .empty 10`, `sectionsAfter` appends `node 4 [effectTree*]`;
  the proof gains `lit9`; statement unchanged. GN0–GN11 green. Path list is now 34 (`logs/rt-changed.txt`).
- MEASURED on d280d23 + LANG-89 (`logs/rt-base5.log`; 6G OOM-killed one lean at 3.7G RSS on the first try, so 12G/2
  threads): whole tree GREEN; writers re-emitted world/doc/Section (1 line) and world/escrow/Escrow; lang-journey GREEN
  with EF0–EF5; `--contextual`/`--contextual-checks` GREEN; `ledger-sim 1` GREEN; `rows bounty bar` ALL PASS after the
  bar re-pin 6.069 → 6.070 (a package is one node larger); codec-vectors 293 of 59 sites `--check` ok (57
  `lang/package/7` rows out, 58 `lang/package/8` in, 2 + 2 version rows). Census by hand (`logs/rt-decls.sh`): ok, 73
  map lines (69 + four the merge with META made: `Std.boundedPackageWith`, `Std.ownedPackageWith`,
  `Std.templateGenerator`, `fillPackage` — their `{ p with … }` bodies spell the new field).
- ~20:2xZ LANDING attempt 6 launched: `logs/rt-land1.{sh,log,pid}` (scripts/commit by `exec`; message `logs/rt-L1.msg`).
RELAND-CTX (~20:10Z): the registry LANDED as f193a3e7 — rebase onto it; Main.lean takes no session list.
- 20:3xZ attempt 6 REFUSED at the source gates (one SIZE line owed: `Lean lines (Protocol)` +1, the bar comment);
  added. Attempt 7: the FULL judge GREEN (`PRE-PUSH GREEN tree 8e7d1a8e6889`), then displaced: main moved d280d23 →
  f193a3e (CTX's journey session REGISTRY), conflict in Lang/Journey/Main.lean. Rebased (same dance): Main.lean takes
  main's copy + `import Lang.Journey.Effect`; `Lang/Journey/Effect.lean` ends with `initialize register { name :=
  "effect", run := pure effectSession }`. lang-journey GREEN (1243 ok rows, EF0–EF5); census ok 73/73. Attempt 8
  launched `logs/rt-land3.{log,pid}`.
- 21:3xZ attempt 8 NOT JUDGED (a bench `bench-worstcut-rows` timed out twice under box load, load avg ~11; "not a
  verdict about this commit"). Main had moved seven commits (to 9a56dd5: TRUST's `kernel!` authority-at-genesis,
  OBS/ROOT Spec/, client). Rebased (no conflicts); one red: `Lang/Journey/Effect.lean` `genesis` now takes an
  `Authority` (passes `Authority.none`, as every other journey session). Whole tree GREEN on 9a56dd5 + LANG-89; writers,
  journeys, sim, rows, vectors 293/59 `--check` ok, census ok 73/73 (`logs/rt-base7.log`). Attempt 9 launched
  `logs/rt-land4.{log,pid}`.
- ANSWER TO EMBER (real 10-27 03:0xZ): (1) NOT landed yet. Attempt 9 is alive (`wt/fable-types/logs/rt-land4.pid` =
  3091613, `logs/rt-land4.log`): full judge GREEN THREE times (trees ea2764b1, d747c5e9, 3136a84e), displaced each time,
  now re-basing onto 914f2d7 for its fourth judge (2 of 5 charged). (2) Displacement, almost all of it: in this lane's
  nine attempts the judge was GREEN 5 times (attempts 7 and three times in 9) and every one was thrown away because main
  moved — by d280d23→f193a3e (CTX registry: a real one-hunk conflict in Main.lean), then 41af1fc (client), 5527b01
  (gates), 914f2d7 (client), NONE of which touches a LANG-89 path. Real reds: the Quote.lean quoter (META's LANG-87 hand-wrote
  a nine-child package frame; fixed), one SIZE line, `genesis` gaining an Authority (TRUST's kernel!), the bar value
  6.069 → 6.070. One NOT JUDGED (a bench timeout under load). (3) The one change: carry a GREEN verdict across a rebase
  whose merge touches none of the candidate's paths (or only disjoint modules outside its import reach) — re-judge
  only the reach, not the whole tree; with that, attempt 7 (green ~20:5xZ) or attempt 9's first green (~23:3xZ) lands.
  (4) The worktree is green on 9a56dd5 and the lander re-bases itself; nothing is needed from me unless a rebase
  conflicts; if FIX-QUEUE lands a verdict-carry, the next displacement should land it outright.
- 10-27 (WORK-RULES-20261027 rule 1, the judge gone): committed LANG-89 as one prose commit, rebased by hand over each
  move of main. Push 1 (c3a93f6f over 00b4f79, built green) REJECTED non-fast-forward (main moved to 7d30fc1); rebuilt
  green over 7d30fc1; main moved again (446fb59), and the rebase CONFLICTED in Lang/Surface.lean (the testground moved
  the grammar into one `grammar` text): kept main's, added `[(effect (moves n))]` to the method line of
  `Surface.grammar`. Then the build over 446fb59 named two reds in ROOT's new `Spec/`: `Spec/Sim/Exchange.lean`'s
  `escrowPackageWith` is a field-by-field TWIN of `offerEscrowPackageOf` (its `escrowPackageWith_fair` is `rfl`), and the
  lazy package it builds was ungraded, so install refused it `effectExceeded` before its unfair-legs tooth. FIXED by
  naming the table once (`Std.escrowEffects`), used by both; also `Lang.Read.grammar` (the core grammar the
  testground shows) gains `[(effects (l n)…)]`. Builds now go through `scripts/nd-build` (6 box slots).
  Wire: still 8 (main is at 7; PCC's L2 is racing at 8 — whoever lands second re-numbers; I check right before pushing).
- **LANDED 6e177d55** (real 10-27 ~08:0xZ): `lang!: graded effects — a method's declared grade bounds what one run of
  it may move (LANG-89)`, package wire **8**, effects child `node 4`, over 5c0c2055. Built and run green over 9c0e51e
  (whole tree incl. Spec, lang-journey 1244 ok, ledger-sim, rows bounty/bar, codec-vectors 293/59); the last rebase
  (hygiene, Spec, sandbox) was clean and pushed by rule 4; a post-push build runs (`logs/rt-post.{log,pid}`).
  PCC: LANG-89 is on main at wire 8; L2 re-numbers to **9** (claims child at `node 5`), per the race rule.
- POST-PUSH red (fixed forward): ROOT's `Spec/Proofs/Escrow.lean` `run_lazy_escrow` (landed in 87a1eb1 just before
  6e177d55): `Spec.Sim.Escrow.esLazy` is `Std.pkgOf …` with no grades, so install refused it `effectExceeded` before
  its double-payout tooth. It now carries `escrow.effects` (the deployed escrow's 1000). `lake build Spec` green;
  pushed **ca70d368**. The class (a plant/floor package built ungraded from `Std.pkgOf`) is the third instance after
  the ledger sim's `twoKeys` and Spec's `escrowPackageWith`: a floor package should be derived FROM the deployed one
  (`{ escrow with … }`), never re-spelled; worth a hygiene line for Spec.
- RELAND-PCC-2 → TYPES (real 10-27 ~08:2xZ): LANG-89 is on main at version 8 (6e177d55), effects at `node 4`. L2 (LANG-93) takes package wire VERSION 9, claims at `node 5`, rebased onto ca70d368 with the trial merge's recipe (`Print.optSection`, the four-case `readPackage_closedText`, `package_fitsB` over a tail of two sections, which replaces `package_fitsB_effects`). Nothing is needed from TYPES; the hash follows in FABLE-PCC.report.md.
- **LANG-90 LANDED b03731b6** (real 10-27 ~09:5xZ): `lang!: a relation may hold a leg — (holds f) …`, package wire **9**
  (relTree's eighth child), over eb674e79. Built from DESIGN-TYPES §3.1: `RelDecl.holds : Option Label := none` (a
  default, so named literals keep their meaning; 9 anonymous `⟨…⟩` literals gained `none`), `legTy` in Package.lean
  (`escrowLegTy` deleted), `RelDecl.holdsOk` in `checkRel`, `checkLegs` in Lang/Rel.lean called after `guardEdits`
  (per-asset sums, two inequalities, `legUnfunded`/`legStranded REL`), wire/text/surface, the escrow's `offer` holds
  `give`. Theorem `Lang/Proofs/Holds.lean` `runMeasuredWith_legs` (+ `checkLegs_backed`). Journey §HV (a Vault in the
  surface): HV1/HV4/HV5 admitted, HV2/HV3 `legUnfunded vault`, HV6/HV7 `legStranded vault`, rows and balances
  unchanged. PRICE PAID: `[DecidableEq D]` on 65 theorem binders over runs (4 `omit` lines lose it), Provenance's 5
  tail-spelling statements gain the `checkLegs` step. Re-emitted world/doc/Section, world/resident/Bell (from Bell.ob;
  no writer existed — `logs/scratch/WriteBell.lean` is the one-off), CappedTally's text gains `(holds)`. Whole tree,
  lang-journey 1263 ok, ledger-sim, rows bounty/bar (6.070 unchanged), codec-vectors 293/59 green on 79b1ffe; the last
  rebase over eb674e79 (protocol!) was clean and pushed by rule 4; post-push check `logs/rt-post2.{log,pid}`.
  No plant run (optional under the regime; the refusal names exist only in `checkLegs`). Open: the HISTORY theorem
  (Σ held legs ≤ the object's balance, from admit_value + this), and a writer for world/resident/Bell.
  PCC: L2 now takes wire **10** (claims at `node 5` of the package; the relation tree has eight children).
- POST-PUSH b03731b6: whole tree, lang-journey (1263), ledger-sim, rows, vectors GREEN on main (logs/rt-post2.log); writers re-emit nothing new.
