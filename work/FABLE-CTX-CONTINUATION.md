# FABLE-CTX-3 — continuation (real 2026-10-26, from ~09:20Z; the third designer-builder of DESIGN-CTX)

Read first: `redregg/work/promo/DESIGN-CTX.md` (BUILT-1..6 are the record), this file whole, then
`redregg/work/codex/FABLE-CTX.report.md` (the FABLE-CTX-2 and -3 lines) and `FRONTIER-BOARD.md`. FOUR worktrees on hbox,
all mine (one agent per worktree; the predecessors are finished). Scratch on hbox: `/tmp/fable-ctx/` (every script, log,
pid, message; the Mac scratchpad copies are at
`/private/tmp/claude-501/-Users-ember-dev-breadstuffs/01a167c9-1142-7bc2-a1e6-b2cf23dfde66/scratchpad/`).

| worktree | base | holds | state |
|---|---|---|---|
| `wt/fable-ctx-k1` | c82f171 | the journey SESSION REGISTRY (`lang:`, FAST) | READY; re-apply on the next main by `registry-reland.sh` |
| `wt/fable-ctx` | c82f171 (dry-run reland at V=6 done) | S2 contract pins (LANG-84, `lang!`) | READY; `s2-reland.sh` carries it to the next main at N+1 |
| `wt/fable-ctx-caller` | c82f171 | K1 `Req.caller` (KERNEL-76 + LANG-85, `kernel!`) | BUILT, whole tree green; lands after S2 |
| `wt/fable-ctx-s3` | = caller tree + LANG-96 | S3 `notFuser` (`lang:`) | BUILT, whole tree green, journeys GREEN; lands after K1 |

Landing ORDER (each later one is built on the earlier): registry (fast) → S2 (full, its wire number N+1) → K1 (full,
kernel!) → S3 (fast; it reads `Req.caller`). Never `git stash`; never edit a worktree while a `lake build` of it runs.

## The queue and the fast window (READ scripts/commit, gates/land.py)
Five full landers sat on main since 02:30Z local with main at c82f171; at 09:14Z: META 270 (~2 h in), AGENT 272, TRUST 273,
TYPES 274, PCC 275 (relaunched), plus OBS's fast pre-push. A full lander discovers a moved main only at ITS OWN
compare-and-swap (after its judge): it is "displaced", charged one of 5 only while not head, and re-bases. A FAST lander
holds no ticket and lands by CAS unless a twice-displaced full lander is alive (then it waits up to 1 h). So a fast
landing costs the full landers mid-judge one displacement each — the FREE window is right after a full landing: the
displaced ones re-base onto whatever main is at their CAS, so a fast commit that lands before their CAS costs nothing.
Watch: `tail -1 /tmp/fable-ctx/main-watch.log` (a loop, pid in `main-watch.pid`, one line a minute: time, origin/main,
the lander tickets) and `ps -eo pid,etime,args | grep scripts/pre-push`.

## 1. The registry (FAST) — `registry-reland.sh`
STATE at 12:30Z: the registry is IN THE JUDGE — lander pid in `/tmp/fable-ctx/land-reg2.pid` (3967714; the inner lander
p3967715), log `/tmp/fable-ctx/land-reg2.log`, recorded on c4800fb7 with the 12 files (Inbox included). Attempt 1 was FAST
GREEN (build, decls 0 changes of meaning, census ok) but main moved twice under it (TRUST T2 9ccb6b6e, T3 f70a5f9e); attempt
2 re-based and has waited an hour+ for a gate slot behind six full landers (on the board as friction). If it lands:
`scripts/commit: main = …` in the log; write DONE on the board's friction line. If it gives up (12 displacements) or is
refused, re-run `registry-reland.sh` on the new main and relaunch as below (registry-msg.txt now carries both SIZE lines
and names Inbox). Do NOT kill it.
`nohup bash /tmp/fable-ctx/registry-reland.sh > /tmp/fable-ctx/reg-reland.log 2>&1 & echo $! > /tmp/fable-ctx/reg-reland.pid`
→ detaches wt/fable-ctx-k1 at origin/main, runs `registry2.py` (Main.lean's session lists are PARSED: a session another
lane landed — AGENT's Inbox, TYPES's Effect — gets its own `initialize register` line in the module defining it, named
from its identifier; the Journey.lean edits are anchored and assert), builds lang-journey (~5–40 min), runs the five
modes, ends "REG READY". Then launch (the file list from `git status --short`; add any new session module):
`cd /tank/dregg-build/nanodregg/wt/fable-ctx-k1 && nohup bash -c 'exec scripts/commit -F /tmp/fable-ctx/registry-msg.txt
--cross-layer "LANG journey files of PCC (Claims) and META (Gen) [and AGENT (Inbox), TYPES (Effect) if landed]: one
register line each, by FABLE-CTX report line" <paths>' > /tmp/fable-ctx/land-reg.log 2>&1 & echo $! > /tmp/fable-ctx/land-reg.pid`.
Then write DONE on the board's friction line. registry2.py reproduces the built tree on c82f171 byte for byte (tested).

## 2. S2 (full, `lang!`) — `s2-reland.sh` then `s2-finish.py`
STATE at 12:55Z: S2 is IN THE JUDGE at VERSION 7 (lander pid `/tmp/fable-ctx/land-s2.pid` = 915331, log
`/tmp/fable-ctx/land-s2.log`, message `/tmp/fable-ctx/msg-s2.txt`, the 20 paths in the launch line below), on main
1bdd5ba0 (META's LANG-87, wire 6). If another wire bump (TYPES LANG-89, PCC) lands first, the attempt is refused on its
generated files: re-run `s2-reland.sh` (it reads N from main) and relaunch at N+1 — the two conflicts seen (Journey.lean
LV rows → mine; Bounds docstring → main) recur; REBUILD `bench-worstcut-rows` before measuring. Every refusal so far
was a missing SIZE:/RESTATES-MEANING:/WASTE: line named in the log.
When the bumps ahead have landed: `nohup bash /tmp/fable-ctx/s2-reland.sh > /tmp/fable-ctx/s2-reland.log 2>&1 &` (pid file
`s2-reland.pid`). It saves the 19 files, normalises MINE's `lang/package[-version]/6` strings to main's N, merges each
non-generated file with `merge-onto-main.sh` (MINE/BASE=c82f171/THEIRS=origin/main by `git merge-file`; a CONFLICT stops it
with markers: resolve, then `bash /tmp/fable-ctx/s2-reland-2.sh N V SAVEDIR`), then renumbers N → V=N+1 in Bounds, Package,
Proofs/Wire, Emit/Vectors (the vector SITE labels too) and Journey.lean, adds the Bounds docstring note, inserts the LANG-84
block from the saved copy after LANG-83 (renumbered), handles Main.lean (registry present → import only + a register line
in ContextualLaw.lean; else the two-line edit), takes main's vectors + Section, builds (Lang lang-journey codec-vectors
host), runs `verify-m1.sh`, benches worstcut-rows, ends "S2 READY at V=…". DRY RUN on c82f171 at V=6: clean, all green,
bench 20.184 = the ceiling (no waste move on THIS main; it re-measures at the real V). Then
`cd wt/fable-ctx && python3 -I /tmp/fable-ctx/s2-finish.py V HASHES` (HASHES from `grep "trie-hashes" s2-bench-rows.log`,
the raw count; if the rows are unchanged, drop the `WASTE:` line from the message instead) → `/tmp/fable-ctx/msg-s2.txt`;
launch: `nohup bash -c 'exec scripts/commit -F /tmp/fable-ctx/msg-s2.txt --cross-layer "GATES: gates/waste.tsv
worstcut-rows re-pinned (WASTE line) [or: unchanged]; CODEC: Emit/Vectors.lean site labels /V; HOSTING: world/doc/Section
re-emitted (its imports are the helper ids, which moved)" <the 19 paths + Emit/Vectors.lean [+ gates/waste.tsv]' >
/tmp/fable-ctx/land-s2.log 2>&1 & echo $! > /tmp/fable-ctx/land-s2.pid`. Every earlier refusal was a missing
SIZE:/RESTATES-MEANING:/WASTE: line named in the log: add it and relaunch (a full judge ≈ 2 h, a queue ticket).

## 3. K1 (full, `kernel!`) — after S2
STAGED: `nohup bash /tmp/fable-ctx/k1-reland.sh > /tmp/fable-ctx/k1-reland.log 2>&1 &` (after S2 is on main) does the
whole recipe below mechanically — merge of every hand-written file onto origin/main (stops on CONFLICT: resolve, then
`bash /tmp/fable-ctx/k1-reland-2.sh SAVEDIR`), the KERNEL-76/LANG-85 blocks into main's decisions files, main's copies
of every generated file, `lake build` of the whole tree (~1.5 h), the emitters (emit-cores, hosting-sim --write-text,
lang-journey --write world/doc, codec-vectors --write/--check), the four journey modes, verify-k1.sh (harness-control,
rows, cargo doc/foreign, bench) — and ends "K1 READY" printing the bar plant and the hash counts to re-pin
(`rowbarStated` in Protocol/Rows/Run.lean; the two worstcut-rows waste rows, LANG-76's form). Then fill
`/tmp/fable-ctx/msg-k1.template2` (the 81 RESTATES-MEANING lines are in; @V@ = main's wire version, @WASTE@, @JOURNEY@
= the LF/LE/… rows unchanged + LB rows, @DECLS@ = "gates/decls.py export of both trees, diffed: 87 restated, 23
redefined", @FIXTURES@ = foreign/Accept, foreign/Timelock, pin/Live) and launch with FABLE-CTX-2 §3's cross-layer line.
`client/tests/fixtures/pin/Live` is merged as a hand-written file (no generator in the tree).
Re-apply onto the new main with `merge-onto-main.sh wt/fable-ctx-caller SAVE c82f171 <the non-generated files of
`git status --short`>` (overlaps S2 only in Lang/Package.lean (different hunks), Lang/Journey.lean (one line),
decisions/lang.md (LANG-85 after LANG-84: take main's file and insert the LANG-85 block as s2-reland-2.sh does for 84)),
then re-draw the generated files with the emitters (`lake env lean --run /tmp/fable-ctx/emit-cores.lean`, `hosting-sim
--write-text`, `lang-journey --write world/doc`, `codec-vectors --write`; `client/tests/fixtures/pin/Live` by hand to the
printer's form), rebuild everything (`SWARM_MEM_MAX=24G LEAN_NUM_THREADS=4 swarm-build lake build`, ~1.5 h), run
`/tmp/fable-ctx/verify-k1.sh` (rows → re-pin `rowbarStated` in Protocol/Rows/Run.lean to what it measures, 5.292 on
c82f171; bench → the two waste rows), fill `msg-k1.template` (@RESTATES@ from `/tmp/fable-ctx/decls-diff.out`: 87 restated
+ 23 redefined names, the Kernel.Receive.* and Ledger/Lang ones — the `Journey.*` and `initFn` lines there are the
registry's noise), launch with the cross-layer line in FABLE-CTX-2's §3 recipe.

## 4. S3 (fast, `lang:`, LANG-96) — after K1
wt/fable-ctx-s3 is the caller tree + 8 Lang files + decisions/lang.md (LANG-96 before LANG-92). After K1 lands: copy those
nine files onto a fresh detached origin/main in wt/fable-ctx-s3 (`merge-onto-main.sh` with BASE = the K1 landing commit),
`lake build Lang lang-journey`, run lang-journey (LF9/LE9 `take: refused notFuser`), launch
`scripts/commit -F /tmp/fable-ctx/msg-s3.txt Lang/StdOffer.lean Lang/StdOfferEscrow.lean Lang/Proofs/StdOffer.lean
Lang/Proofs/StdOfferFuse.lean Lang/Proofs/StdOfferEscrow.lean Lang/Proofs/StdOfferEscrowFuse.lean Lang/Journey/Offer.lean
Lang/Journey/OfferEscrow.lean decisions/lang.md` (fast judge; the decls judge names any missing RESTATES-MEANING line).
Next after S3: `offer_safe_forever`'s second conjunct over `row_turn_cases`; the market (DESIGN-CTX §2.5b.2, K6).

## Box safety (verbatim, standing)
Never kill by pattern. No `pkill -f <anything>`, no `pkill -x <bare word>`, no `killall`, no `kill -u`. A process
you started is stopped by the PID in its PID file, and only that; no PID file, no kill. Never `git stash`. Never
run an unfiltered `-p <crate>` test suite. Never delete anything outside your own worktree/scratch.
