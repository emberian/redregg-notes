# FABLE-CTX-5 continuation (real 2026-10-27; written by FABLE-CTX-5 at ~360K context, parking; hbox wt/fable-ctx4 is clean at 2efa6a57)

Read first: DESIGN-CTX §1.4 (baseline), §11 and BUILT-6/7; FABLE-CTX.report.md's CTX-5 lines; decisions/lang.md LANG-101 and
decisions/hosting.md HOSTING-59 on main.

## Landed this session
- K2 `notFuser` (LANG-100): 48232e7b.
- The resident inside the open calculus (LANG-101, HOSTING-59): 2630ea32. `Lang/Contextual/Slot.lean` (SLOT, slot_repair,
  interp), `Hosting/Resident/Run.lean` (Prog = Prot with `serve`/`use` holes; `Cmd.probe`; `refusedP`/`probesP`),
  `Hosting/Proofs/ResidentSlots.lean` (the repair theorem as slot_repair's instance), BellConform's set-of-owed-rings round,
  NanoBridge/ContextualNano deleted, ContextualFailures → LostReply, agent_hole H4.

## (5) the withdrawn list persisted — LANDED 2efa6a57
`Eff.note l` / `Ev.note` / `Handler.note` / `Oracle.note`; `Where.noted` + `Where.notedAt := { w with kept := w.noted }`
(a note IS a keep at another name: every ResidentVolume theorem applies); `withdrawnTy`/`notedText`/`notedRead`/`notedSeed`;
`run` seeds `Mem.withdrawn` from `vol/withdrawn-<bell>`; `ResidentRun.UseCore`; agent_hole H4 asserts the volume file.
Not done: a restart row (kill the resident grain after H4; see it NOT ask the withdrawn ring).

## Owed (in order)
1. (7) THE DOCUMENT'S READ WITH EVIDENCE — the SLOT's second instance (CRIT-CTX's third requirement; DESIGN-CTX §11 (7)).
   Today: the section (`world/doc/Section`, LANG-83: `Std.hole` at bytes) selects by a stored `selected` and re-judges only on
   an explicit `rejudge` (`nd read S candidates 8` shows `suspended "support0 dead"`). Build: a read of a section that
   returns its selected text WITH evidence, as `Slot.read` over the hole's candidate supports (`SupportPin`s:
   `supportLive`/`supportObserved`, Lang/LiveHoles.lean) at the reader's pinned view: `usable c [(pin, true)…]` or
   `blocked c [dead pins]` — stored-but-blocked vs usable, read at read time, no rejudge needed. Rows (lang-journey DC/LG
   family, then client/tests/doc.rs): (a) usable with its supports and liveness; (b) the grant revoked → blocked by the
   grant's name while still stored; (c) the contributor substitutes the advertised support (posts a fact naming a different
   grant than the one its candidate cites) → blocked by name; (d) another member's alternative selected → usable at once
   (`slot_repair` (4)). Theorem: `slot_repair` at the hole's slot; tie to `holeDecision_verified_iff`.
2. cv task 01a17d68: member refusal lines name their coordinates (`refused missingCell <hex>`); a protocol lane.
3. §11's `text r` and `pins r` holes (the model's answer as a candidate with the ring's capture as its support).
4. TESTGROUND: the line in TESTGROUND.report.md (10-27 FROM FABLE-CTX-5) is the brief for the inbox demo.

## Box safety (verbatim)
Never kill by pattern. No `pkill -f <anything>`, no `pkill -x <bare word>`, no `killall`, no `kill -u`. A process you
started is stopped by the PID in its PID file, and only that; no PID file, no kill. Never `git stash`. Never run an
unfiltered `-p <crate>` test suite. Never delete anything outside your own worktree/scratch.
