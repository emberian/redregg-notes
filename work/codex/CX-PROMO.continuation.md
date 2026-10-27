# CX-PROMO continuation (written by CX-PROMO at ~710K tokens, 2026-10-22 ~21:35Z; PARKED per the brief's ~400K rule)

Successor: read your brief `codex/CX-PROMO.brief.md`, then THIS file, then `RULINGS.tsv` rows R-0024..R-0032, then
`promo/READ-C2M-grok.md` (the spec for your next card) and `promo/IMPACT-C2-MEASURE.md`.

## Where the program stands (nano main e9c126f)
- LANDED 4916f3a `lang!` E1 + C1 (LANG-75, LANG-75.1) + charter scope item 3 (Writers). Full judge GREEN.
- LANDED e9c126f `lang:` C9 as DOCSTRING (LANG-75.2): cellLive docstring, KERNEL-60 addendum, row `P8.2s two-Turn split`.
  The two C9 theorems were built then removed per R-0031 (rename of invoke; cellLive_pinned waits for C2's kernelWorld).
- C2-MEASURE done: (a)=7 as stated, 3 real per the read (a2 hsel, a6 hpinned, a7 hchecked); (c)=2 (pruned, uncovered).
- OPEN, yours: **R-0032 = BUILD IMPACT-C2 for the OTHER BRANCH** (verbatim in RULINGS.tsv): judge/Status/provenance
  (and what only they serve) leave `Lang/Contextual/Closure.lean`; `CalculusLaws` + `langLaws` stay; HoleBridge's
  closed-fragment bridge goes; C3 (live label), C4(a) (receipt monomial), C5 (repair with transport) restated DIRECTLY
  over `selectHole`/`resolveHole` with the five LiveJourney instances as teeth (`strengthening_factor`,
  `kept_context`, `alternative_same_filling`, `replacement_filling`, `used_hypothesis_suspends`); Outcomes' repair
  theorems restated over live objects; READ-C2M §4: `Closure.lean` is DELETED, `CalculusData` moves into
  `Lang/Contextual/LangInstance.lean` beside `langData` (a def module, law 8), `Lang/Contextual` keeps LangInstance +
  the protocol calculus (Protocol, NanoBridge; R-0021 keeps it) + Core/CoreCalculus until R3. R3 (delete the CMTT core,
  R-0022) rides in the same or the next landing. Statement price measured; digest diff under a RESTATES/DELETES map;
  READY-IMPACT C2, then the read, then the release. `cellLive_pinned` (built once, see LANG-75.2) is C2's: it lands
  WITH `kernelWorld` only if the restated C3 has a world at all; under the other branch probably not — say so.
- **R-0033 (RULE, fixes the shape; ACKed by me):** DELETE `Closure.lean` whole; `CalculusData` → `LangInstance.lean`;
  `CalculusLaws` stays in the proof module; Outcomes' abstract repair theorems are superseded by their deployed teeth
  in `Proofs/LiveJourney.lean` over `selectHole` (restate what C5 needs there; delete the abstract statements BY NAME);
  `Lang/Contextual` = LangInstance + Protocol + NanoBridge (+ Core/CoreCalculus until R3, same or next landing). Every
  deleted statement listed by name with its successor or its reason; the digest diff proves nothing surviving weaker.
- Not started: P3+ (PROT cards), per the plan, after P2.

## Worktree and tools (hbox)
- Worktree: `/tank/dregg-build/nanodregg/wt/promo` (clean at e9c126f; own CARGO_TARGET_DIR=$PWD/target; `.lake` warm,
  whole tree built at 4916f3a+). Logs: `/tank/dregg-build/nanodregg/logs/promo/`.
- My local mirror for editing: `/private/tmp/claude-501/-Users-ember-dev-breadstuffs/3a1e01fe-da72-4c08-b7dc-2de77511c341/scratchpad/wt`
  (same content as the worktree at e9c126f except SIZE.md) with `push.sh` (rsync --checksum --relative of Lang Emit
  Ledger Kernel Hosting decisions CHARTER.md gates/codec-vectors.tsv ONLY), `hb.sh LOG TARGETS…` (MEM=, N= env),
  `plant.sh NAME FILE OLD NEW MODS…` + `plant-remote.sh` (temporary edit on hbox, builds lang-journey FIRST and checks
  it was relinked, then proof mods, runs journeys, restores from the mirror and rebuilds GREEN). A successor without
  that scratch dir: re-create from the worktree (`rsync hbox:wt/promo/ ./wt --exclude .lake --exclude target --exclude .git`).
- Census digest: `logs/promo/digest/` (copies of the fold's mkdigest_rn.sh, digest_rn_cmd.lean, diff_rn.py).
  Base digest: run mkdigest_rn.sh on a tree at the base commit with a rename map (wt/cxfold is at f8d04ac; for C2
  make or reuse a base tree at e9c126f — wt/promo itself before editing). ~15 s per digest.
  Hypothesis counter used for the premise price: see `promo/hyps-E1.txt` (python over the digest's type column,
  counting top-level `->`).
- Reverse deps: `logs/promo/revdeps_cmd.lean` (#promo_revdeps OUT TOUCHED) — import-all file generated like mkdigest.

## Lessons paid for (each cost a landing attempt or a false verdict)
1. `scripts/commit`'s stale-path guard reads a RE-STATED theorem of a recent commit as a revert: use
   `--reverts <sha>` and say "not an undo" in the message (precedent: GATES-9 ruling; I did this for d7989d94af13).
2. My first push script rsynced all of `gates/` from the mirror and silently put the BASE codec-vectors back; the
   full judge went RED (census + generated vectors). The script now pushes only `gates/codec-vectors.tsv`.
3. A plant whose edit breaks a module the exe depends on, or any failed module in the SAME `lake build` call, stops
   lake before it relinks the exe: the journey you then run is the previous binary. Build the exe alone first and
   check "Built «lang-journey»" before reading a plant's verdict. Unused-variable linting is an error here; keep
   planted code referencing its variables.
4. The full judge's cargo `FAILED` lines are the nobin controls; read `runs: ok (…)` (lane rule 6).
5. `relReads` proofs: work through `readPoint_ok` / `pointData_ok` (Lang/Proofs/Invoke) rather than splitting the do
   block; record types: `pointRecTy` makes the non-live point type the old `pointTy` definitionally.
6. Building theorems while a read is out is fine for measurement, but the read decides (C9: both built theorems were
   renames). Measure the plan's §8.2 refuter yourself before building.

## Report / ledger
- REPORT: `codex/CX-PROMO.report.md` (ACKs through R-0032 except the last line I write now).
- Artifacts: `promo/` (IMPACT-E1 with BUILT section, E1-* census files, E1-plants/, diff-E1.txt, hyps-E1.txt,
  E1-vectors-diff.txt, IMPACT-C9.md, C9-plants/, IMPACT-C2-MEASURE.md, C2-measure-statement.lean).
