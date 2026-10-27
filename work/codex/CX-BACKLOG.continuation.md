# CX-BACKLOG-2 update (2026-10-23): cards 3, 4, 5, 7 LANDED (e96c9a5 PROTOCOL-69, a639421 HOSTING-45,
# 9fd88d0 LANG-75.23, 1eae61f HOSTING-46). Only card 6 is open. It waits on FABLE-T's L2: built, not landed,
# and it rewrites StdOffer/StdOfferFuse. Card 6's list below still stands. Card 3's design section below is
# SUPERSEDED: the collision form with c' chosen is the census's red shape; the landed theorem uses a second
# preimage of the premise call's id, plus a step-3 read-back check (PROTOCOL-69).

# CX-BACKLOG continuation (parked 2026-10-23 at ~360K tokens; successor starts HERE)

State: cards 1 and 2 LANDED (2c3bb09, 506bf2c; both pushed to origin). Cards 3-7 open, in order.
Worktree hbox:/tank/dregg-build/nanodregg/wt/backlog sits on 506bf2c (scripts/commit left it there), warm .lake.
FABLE-T report /Users/ember/dev/redregg/work/codex/FABLE-T.report.md did NOT exist at park time (card 6 waits on it).

## How I landed (gotchas, MEASURED)
- Edit in a local mirror, scp to the worktree, build there: shell-quoting Python heredocs through ssh broke twice.
  `swarm-build lake build <Module>` with SWARM_MEM_MAX=6G; never Hosting.Proofs.Reply alone at 10G.
- scripts/commit -F MSG --cross-layer "LAYER: why" PATHS... (fast judge, ~5-10 min). It refuses until the message has
  one `SIZE: <metric>: <why>` line per metric that rose (it prints them), and decls map lines:
  a private decl is named by its mangled name, e.g. `RENAMES: _private.Lang.Proofs.StdOfferEscrow.0.Nanodregg.Lang.Std.fuse_resolve → Nanodregg.Lang.Std.escrow_fuse_resolve`.
- Plants: copy the file to /tmp, mutate, `lake build <target> > logs/backlog/plants/<name>.build.log`, restore, `git diff --stat` must be empty. Logs: hbox /tank/dregg-build/nanodregg/logs/backlog/plants/.
- Lean: `obtain ... -` on a var that a later `rfl` substitutes can drop hypotheses: use `_`. `refine ⟨_, ?_⟩` for an existential version fails; rw first, then `exact ⟨_, rfl⟩`.

## Card 3 (cv 01a16821-5835) — DESIGN, not built (READ, INFERRED where marked)
Goal: from `wf.journalAt X.env (txIdOf X c) = some e` on follow's World to the commit step of c.
Pieces that exist (READ): Kernel `fold_journal_turn` (Journal.lean:332), `commit_journal_mem`, `refuse_journalAt`,
`admit_journalCanon`, `submit_ok` (Receive.lean:149: submit = journal none ∧ receive ∧ admit);
Protocol `absorbStep` (Command/Machine.lean:435: a Turn event = decodeCall (e.extract 1 e.size) then submit),
`absorbStep_step`, FollowHead `step_keeps` (any P kept by absorbStep and refuting atGenesis is kept by every
Command.step; adopt only from atGenesis), `step_packageAt`; Hosting `Reach`/`Moves` (Socket.lean:282).
Plan:
1. Protocol/Proofs/FollowHead.lean (or a new Protocol/Proofs/FollowJournal.lean): for a predicate Q kept by absorbStep
   and refuting atGenesis (PackageAt of the bell is the instance), P w := Q w ∧ w.JournalCanon X.env ∧
   ∀ k e, w.journalAt k = some e → w₀.journalAt k = some e ∨ ∃ v v' t b' c', Q v ∧ X.decodeCall b' = some c' ∧
   receive X v c' = .ok t ∧ World.admit X.env v t = .ok v' ∧ t.txId = txIdOf X c' ∧ txIdOf X c' = k ∧
   e = (v.height + 1, turnDigest X.env t). absorbStep keeps it (Turn arm via submit_ok + commit_journal_mem; refusal
   arms keep the journal). Lift with step_keeps; Hosting lifts over Reach.
2. Collision disjunct, sound form (memory: explicit list only): from txIdOf X c' = txIdOf X c,
   `X.callBytes c' = X.callBytes c ∨ CollidesAmong X.env.hash [(domTx, X.callBytes c'), (domTx, X.callBytes c)]`;
   with Hosting's hX (decodeCall b = some c → callBytes c = b) on BOTH calls, equal bytes give c' = c.
3. The "w₀ had it" disjunct stays (INFERRED: plan does not prove the planned call's txId absent at the planning
   World). Then join with `Lang.Bell.answer_commits` (card 2) in Hosting/Proofs/BellRow.lean: needs at v the bell
   object live with package P (Q), `readPackage (pinned X.env v c.pins) P = .ok pk` (pinned vs worldLook: check
   whether the planned call pins P; `readPackage_live` is how SocketStrong moves package reads), and v.RowsCanon
   (add to Q: kept by admit_rowsCanon/refuse_rowsCanon). That gives answered_row_is_kept_answer's conclusion on
   the committing World: the card's real payoff.

## Cards 4-7: as briefed (not started). Card 6: read FABLE-T's report first. Things card 6 must also delete
(left as twins because StdOfferFuse.lean is FABLE-T's): StdOfferFuse's private `invokeRun_pkg` (public copy now in
Lang/Proofs/DispatchRows.lean) and the alias `Lang.admit_retract_absent` (= Kernel.admit_retract_row; StdOfferFuse:619-620
names it); and making `methodReads_offer`/`peer_pair` public would let `escrow_fuse_admitted` carry the coupling qx = oy
and x' ≠ y' (LANG-75.22 critique).
