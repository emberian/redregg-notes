# FABLE-CTX-6 continuation (real 2026-10-27; written by FABLE-CTX-6 at ~350K context, parking)

Read first: DESIGN-CTX §11 (the holes table), §1.4, BUILT-9; decisions/lang.md LANG-109; FABLE-CTX.report.md's CTX-6
lines. hbox worktree /tank/dregg-build/nanodregg/wt/fable-ctx4 (state: see the report's last CTX-6 line).

## Landed this session (hashes in the report)
- (1) The document's read with evidence (LANG-109): `Lang/Contextual/Section.lean`, `Lang/Proofs/Contextual/Section.lean`,
  `nd read --evidence S…` (Protocol `Look.evidence`; every read verb is now `Cmd.read (q : Look D)`, answered by
  `Machine.inspect`), lang-journey DC6e–DC14, `client/tests/doc.rs` (three members, two sections).
- (3) The restart row: agent_hole H4 stops and starts the grain after the withdrawal; the new process asks nothing more.

## Owed, in order
1. cv 01a17e0d: the section PACKAGE admits a substituted or omitted support 0 that the read blocks. Design: a contract
   support pin `cellGrant g target grantee` beside LANG-84's `cellLaw`/`cellPackage`, demanded at `select`/`fill`/
   `accept`; refuse `support0 notGrant` by name; re-emit world/doc. Then `Fact.advertised` restates the package.
2. §11's `pins r` — the finding first: "do we need this hole at all?" The resident's pin rule (HOSTING-58: an aimed
   ring pins `TARGET/facts` at `{cell: via}`) exists because `Std.hole` reads `facts` as the CALLER's points and no
   derivation can choose them. The attractor is not a hole in the resident but a package that DECLARES the points a
   method needs as a function of its argument (a method's reads clause with key terms over `arg`: for `propose`,
   `facts` at `arg.s0.cell`, `arg.s1.cell`, `arg.blocker.cell`), printed by `read OBJ ?`, and derived by `nd invoke`
   (`derivePins`) like the kernel's own asks. Then the resident's `--pin` goes away and every member's `propose` stops
   needing `--pin facts …` by hand (doc.rs passes it four times). That is LANG + CLIENT work; the resident only deletes.
3. §11's `text r` — measure before building. HOSTING-59's critique: `serve` re-states `decideTick`; the candidates of
   `text r` (kept text, an ask, `(unanswered WHY)`) are today the order inside `actOn` and the intent on the volume. A
   `text` hole adds a decision only if a candidate can be blocked by a support the resident reads: the ring's capture
   (pending with the same text and aim) at a READ AFTER the ask (a model call takes seconds to a minute; a ring retired
   or a via revoked meanwhile is today found by a refused invoke and the `use` hole). Build it if a fresh read before
   delivery is worth one read per answer; otherwise write that finding into DESIGN-CTX §11 and delete the row. Either
   way the proofs to carry are `Proofs.ResidentRun.tick_order`/`tick_counts`, BellConform, ResidentSlots.
4. TESTGROUND: two lines in TESTGROUND.report.md (FROM FABLE-CTX-5 and FROM FABLE-CTX-6) brief the inbox demo and the
   section inspector; the inspector needs the testground kernel rebuilt (testground/build/build.sh) to run
   `read --evidence`.
5. cv 01a17d68 (member refusal lines name their coordinates) is still open; a protocol lane.

## Box safety (verbatim)
Never kill by pattern. No `pkill -f <anything>`, no `pkill -x <bare word>`, no `killall`, no `kill -u`. A process you
started is stopped by the PID in its PID file, and only that; no PID file, no kill. Never `git stash`. Never run an
unfiltered `-p <crate>` test suite. Never delete anything outside your own worktree/scratch.
