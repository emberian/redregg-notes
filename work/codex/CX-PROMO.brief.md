**REGIME (real 2026-10-24, supersedes every READY/RELEASE/second-read instruction below):** land when YOUR build and tests are green (fast judge; a flag day takes the full judge); validation is a convergence per batch; a cross-family read only on a genuine design fork you name; no polling for RELEASE rows; GitHub origin/main is the truth; the plant-per-theorem rule is NOT a requirement: a plant is a vacuity check you may run when cheap. Box safety and the report file stand.

Name: CX-PROMO. THE ONE LANG WORKER of the promotion program. Read WHOLE, in this order: /Users/ember/dev/redregg/work/PROGRAM-20261022.md
(the approved plan: §0 context, §1 the ten behaviours, §2 the writer model, §3 P1 = YOUR cards E1 → C1 → C9 → the charter text, §5 the
method, §7 verification, §8 the refuters), /Users/ember/dev/redregg/work/REORIENTATION-20261022.md Part B.1 and C1 (the literature's exact
reasons for shape B and the Lean-level design points), /Users/ember/dev/redregg/work/fold/IMPACT-S2.md §5 + fold/S2-tombstone-probe.txt (the
measured admission), the ledger /Users/ember/dev/redregg/work/RULINGS.tsv (R-0001 HOLD; R-0024 RELEASE for the program's cards in order;
R-0025 your GRANT; write `ACK R-0024 R-0025` in your REPORT /Users/ember/dev/redregg/work/codex/CX-PROMO.report.md), the method files
/Users/ember/dev/redregg/work/codex/CX-FOLD.brief.md §method and one of the fold's impact files (fold/IMPACT-S6.md) + its read
(fold/READ-S6-grok.md) so you know the shape a cross-family reader checks, and the lane rules /Users/ember/dev/redregg/work/LANE-RULES-NANODREGG.md.

nano: hbox (ssh hbox), main /tank/dregg-build/nanodregg/main (tip f8d04ac+); make your worktree `git -C /tank/dregg-build/nanodregg/main
worktree add /tank/dregg-build/nanodregg/wt/promo main` (own CARGO_TARGET_DIR; `SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build lake build
…`; 16G printed only for whole-tree Lang.Proofs, never beside a bench). The census exporter + the fold's digest tools are at
/tank/dregg-build/nanodregg/logs/cxfold/ (mkdigest_rn.sh, digest_rn_cmd.lean, diff_rn.py, closure2.py): reuse them.

CARD E1+C1 (one IMPACT file if the design is one; the plan §3 P1 says what lands, the consumer, what it deletes, the price, the gate, the
refuter). ORDER OF WORK: (0) FIRST, the two probes, before any design: (a) the 01a1649d probe: through the real Receive.submit and the
installed Std.hole package, post a support fact naming a digest the kernel never had, at a pin, then select/commit against it: is it
admitted today? Record the whole output as promo/E1-support-probe.txt. (b) the refuter row for shape B (REOR D.1 / plan §8.3): "revoke g
and unpost g's fact in ONE call" and "revoke only": does nano refuse the second by construction today? (measured 10-22: it admits;
re-measure at your tip). (1) /Users/ember/dev/redregg/work/promo/IMPACT-E1.md per plan §5.2: the definitions changed (Package.cites;
the synthesized `cited` relation in the method's rows view; `cellLive look g`; `SupportPin.cell`; `HoleRefusal.supportDead`; the
`holeSupportProbe` `live` conjunct; `look` threaded through selectHole / changedHypotheses / runHoleGuard / resolveHole /
instantiateHoles), `grep -rln` of every touched name across Lang Kernel Ledger Host Hosting Protocol Census Codec Emit Bench Ops gates
rows, reverse deps from the exporter, every gates row / fixture whose subject moves (the Std.hole bundle re-emit; package ids; journey
rows re-pin), THE THEOREM LIST AS STATEMENTS (new: cellLive_iff, cited_authenticated, selectHole_cell_support,
revoked_support_refused, posted_support_checked; changed: the eight Lang/Proofs/LiveHoles.lean statements gaining a binder;
selectHole_origin's conclusion changing meaning: old → new), each tagged with its nano object and its DEPLOYED MUTATION that makes it
false, the premise price MEASURED (which landed theorems gain a hypothesis: expected none; a binder is not a hypothesis), the row diff
(P8.2 becomes "refused support0 dead"; LH14 new; every other row's text unchanged), and the design alternative the plan names (a
synthesized relation vs widening reqTy) with its price. Append `READY-IMPACT E1` and POLL the ledger (sleep 300, foreground) for
`RELEASE E1`. (2) On release: build; the journey byte-identical but the named rows; codec vectors byte-identical unless the ROM wire
changes (then say every byte: lang!); the digest diff under the rename map; gates/check.py; land as lang! through the FULL judge
(detached scripts/commit; PID file logs/promo-E1-land.pid; foreground-wait; whole log; a refusal read whole and fixed forward; a NEW
ground = ASK). Decision text `## LANG-75 The promotion program` (once) + `### LANG-75.1` with critique and a meta-critique naming a
BIAS. Report the hash. (3) C9 the same way (small; fast path), then the CHARTER scope item 3 rewrite with plan §2(d)'s words in C1's
decision landing (--cross-layer). Then write promo/IMPACT-C2-MEASURE.md: the plan's §3 P2 D.2 measurement (write selectHole_judge as a
STATEMENT at your tip; count (a)/(b)/(c)); `READY-IMPACT C2-MEASURE`; poll. Never exit with an open ASK (an ASK is a report line
followed by polling); near ~400K tokens write codex/CX-PROMO.continuation.md and append PARKED.

BOX SAFETY (verbatim): Never kill by pattern. No `pkill -f <anything>`, no `pkill -x <bare word>`, no `killall`, no `kill -u`. A process you
started is stopped by the PID in its PID file, and only that; no PID file, no kill: say so instead. Never `git stash`. Never run an
unfiltered `-p <crate>` test suite. Never delete anything outside your own worktree/scratch. Disk pressure: stop writing, report, wait.
