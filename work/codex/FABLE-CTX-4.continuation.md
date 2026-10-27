# FABLE-CTX-4 continuation (real 2026-10-27 ~12:30Z; written by FABLE-CTX-4 at ~390K context, parking)

Read first: DESIGN-CTX §11 (the plan), CRIT-CTX.md, FABLE-CTX.report.md's CTX-4 lines, and ROOT's redirect (Ember: the
resident goes INTO the open calculus first; NanoBridge is deleted only together with its replacement).

## 1. K2 / S3 `notFuser` (LANG-100) — LANDING, detached
- Worktree: hbox `/tank/dregg-build/nanodregg/wt/fable-ctx-s3` (10 files over origin/main 176110a7; built green there:
  whole tree, lang-journey every mode, ledger-sim, rows ALL PASS — logs /tmp/fable-ctx/s3r-*.log).
- Lander: `nohup bash /tmp/fable-ctx/land-s3.sh` (scripts/commit -F /tmp/fable-ctx/msg-s3-r1.txt, the prose message),
  pid file /tmp/fable-ctx/land-s3-r1.pid, log /tmp/fable-ctx/land-s3-r1.log.
- Attempt 1 (log land-s3-r1-attempt1.log): build ok, lang-journey ok, rows ok, store-plants ok, `rows --deployed`
  UNREAD (600 s wall clock under load 12-17), so "RED". Attempt 2 relaunched ~11:43 local; at parking it had passed
  lang-journey, the blocker-pin mode and rows, and was in `rows --deployed`. If it is unread again: that row is a wall
  clock, not a verdict; ask ROOT whether to push by hand under rule 1 (RELAND-CTX did so for K1).
- After it lands: append the hash to FABLE-CTX.report.md and DESIGN-CTX BUILT-6.

## 2. The resident inside the calculus — BUILT IN PART, uncommitted, hbox `/tank/dregg-build/nanodregg/wt/fable-ctx4`
(a fresh worktree at origin/main 5fe0bff1, `.lake` copied from wt/fable-ctx-s3; one agent per worktree: it is yours.)
Local scratch copies (my edits; the worktree is the truth): `/private/tmp/claude-501/-Users-ember-dev-breadstuffs/01a17d0c-0eb7-7011-8d13-6d5685e98374/scratchpad/ctx4/`.

GREEN (`scripts/nd-build lake build Hosting.Proofs.ResidentRun`, 0 errors):
- `Lang/Contextual/Slot.lean` (NEW): `Slot` (supports, judge), `dead`, `evidence`, `usable`, `alternatives`, `Reading`
  (empty | rejected | usable c evidence | blocked c dead), `Slot.read`; theorems `usable_iff`, `read_usable_iff`,
  `read_blocked_names`, `Permanent`, **`slot_repair`** (the one repair theorem: usable iff every support holds; a
  blocked read names exactly the dead supports; a dead PERMANENT support keeps it blocked by that name at every later
  view; a usable alternative reads usable the moment it is selected, the slot unchanged); `Out` (done | withdrawn |
  bound), `runAlg`, **`interp`** (monadic, holes resolved when reached, depth-bounded; defined by `fold`), `RunsR`,
  `runsR_withdrawn`; `Slot.resolve`, `resolve_ok`, `resolve_error`.
- `Hosting/Resident/Run.lean`: `Prog α := Prot sig (fun _ => Hole) (fun _ => α) ()` — the resident's tick IS a term of
  the calculus. `Eff` (5 effects), `Eff.Resp`, `sig`, `Hole := serve w sh m pending | use sh m ring n line pending`,
  `@[match_pattern]` abbrevs `Prog.done/cmd/keep/forget/ask/hole/sayK` and builder `Prog.say`; `Handler.call`;
  `Mem.withdrawn : List (Ring × String) := []`; the SERVE slot (`ServeFact`, `serveSlot` over `Act`, `stands`,
  `serveHolds`, `serveOrder`, `serveChoice`, `live`) and the USE slot (`aimCells` = hex of the aim's via and target,
  `names`, `UseCand closed|withdraw c|stop`, `UseFact`, `useSlot`, `useHolds`, `useOrder`, `useChoice`);
  `refusalLine`; `readP` ends in `.hole (.serve …)`; `deliverP`'s refused arm ends in `.hole (.use …)`; `useP`
  (closed → forget; withdraw c → say "answer withdrawn …: its support c is refused", forget, `withdrawn := (ring,c)
  :: …`; stop → answerRefused); `fill`; `holesMax := 2`; `Prog.interpN` = `Slot.interp` + `fill`; `Prog.interp`.
- `Hosting/Resident/Trace.lean`: `interpTwice` as a `fold`.
- `Hosting/Proofs/ResidentRun.lean`: `Runs` monomorphic at Tick with `hole` (path of `fill h`) and `say` over `sayK`;
  `DeliverAfter`'s refused branch reads `useChoice r (refusalLine rr) p = .stop`; `ReadCore c sh m` acts on
  `live m p`; new `serveChoice_eq` (serveChoice = decideTick over live rings), `live_prune`, `useP_core`,
  `useChoice_gone`, `useChoice_stop`, `useChoice_withdraw`, `useP_kept`, `useP_lt`; `read_counts`/`tick_counts`
  restated over `live`; `order_refuses_forget_while_pending` gains `hn` (the refusal names no cell the ring cites);
  `ask_path_exists` over live; `Fits` (+ `mono`, `fits_walk`), `forgetThen_fits` … **`tickP_fits`**, `interpN_call`,
  **`interp_runs`** (for every term that fits), `interp_order`, `interpTwice_no_path` (at Tick).
- Deleted: `Hosting/Contextual/NanoBridge.lean`, `Hosting/Proofs/ContextualNano.lean` (git rm). Renamed
  `Hosting/Proofs/ContextualFailures.lean` → `Hosting/Proofs/LostReply.lean` (namespace
  `Nanodregg.Hosting.Proofs.LostReply`; `Peer`, `Peer.reliable`, `Peer.req`, `lostReply` moved in from NanoBridge).
  Doc references fixed in Lang/Contextual/Protocol.lean, Lang/Proofs/Contextual/{Negotiation,Protocol}.lean,
  Hosting/Proofs/BellConform.lean (docstring only).

RED (next, in order) — `T="Hosting Spec"` build:
1. `Spec/Sim/Bell.lean:169` `bellMem := ⟨some bellShape, none, 0⟩` → add `[]` (Mem has 4 fields). Then check
   `Spec/Proofs/Bell.lean`: `tickWith_actOn` was `rfl`; tickP now has `.hole (.serve …)` where tickWith has `act …`
   inline: restate as `Runs (tickWith actOn w m) es a ↔ Runs (tickP w m) es a` (one `Runs.hole` step + `live_prune`)
   or make Spec's `ringAct` the serve hole's filling (the System chooses the hole's filler: that is the theory).
2. `Hosting/Proofs/BellConform.lean` (the round/debt model) — THE DESIGN POINT: a withdrawal forgets the kept answer
   while its ring still waits, so `Owes` breaks and the next ask (another ring) breaks the one-round `debtStep`. The
   honest fix: a withdrawal DISCHARGES the obligation by name, so `Frees r` gains the invoke arm "refused, its line
   naming a cell r's answer cites" (`(aimCells r).any (names (refusalLine rr))`), and `frees` the same. Then
   `deliver_debt`'s refused branch splits on `useChoice` (closed/withdraw → freed, d' = none; stop → kept, d' = some r).
   `act_debt`/`read_debt` need the owed ring to be LIVE (`stands m r`): thread `Owes` as "kept holds it AND it stands"
   — needs a `withdrawn_follows` over ticks (the withdrawn list grows only in `useP`, where the ring was freed, and
   shrinks by `fill`'s prune). Price it before starting; it is the one real proof left.
3. `Hosting/Proofs/Lifetime.lean:55,112,182,449` — same pattern as ResidentRun (split on the old `if ring ∈ pending`
   → `cases h with | hole h => simp only [fill] at h; …useP lemma`; `actOn_*` → hole step).
4. Then: whole tree (`SWARM_MEM_MAX=24G scripts/nd-build lake build`), every importer of Hosting.Resident.

THE RESIDENT REPAIR THEOREM still to state (in ResidentRun or a new Hosting/Proofs/ResidentSlots.lean), as an instance of
`Slot.slot_repair`: (a) `serveChoice m p` is usable at the read (every support holds: the ring pending and standing);
(b) a refused answer whose ring still waits and whose line names a cell it cites is withdrawn by THAT name
(`useChoice_withdraw` + `useP`: `.next m'` with `(r, c) ∈ m'.withdrawn`, or `stop volume`); (c) a withdrawn ring is never
served: `(r,c) ∈ m.withdrawn → serveChoice m p ≠ .ask r ∧ ∀ t, ≠ .answer r t`; (d) repair: when the head of
`live m p` is q, `serveChoice m p = .ask q` (no restart, no reinstall). Owed and named: the withdrawn list is in memory,
so a restart asks a withdrawn ring once more (one meter charge) and withdraws it again; persisting it is a volume change.

THE DEPLOYED ROW (H4, not yet written) in `launcher/tests/agent_hole.rs`, after H3 (gs is retired by then), before the
drops: ring `(record (text "through a retired grant") (to <aim>))` (the same `aim` string as H2a), then
`(record (text "a plain question") (to none))`; `until` `answers().len() == 2` (150 s); assert the log has
`resident: answer withdrawn` and `gs`, the first ring still pending, and no `answerRefused`. It is also the MEASUREMENT
of the real refusal line for a retired `via`: if the line names neither via nor target, the `use` slot stops the queue
and H4 fails showing the line — then `aimCells`/`names` must read what the kernel actually prints.
Run: `scripts/nd-build lake build resident hosting-controller hosting-broker host hosting-residents` then
`scripts/nd-build cargo test --locked -p nanodregg-launcher --test agent_hole -- the_agent_fills` (filtered).

## 3. Still owed from the brief (after 2 lands)
- The testground's inbox demo showing the holes filled and withdrawn: a line in TESTGROUND.report.md (do not edit
  testground/).
- The document (CRIT-CTX's third requirement): `read` of a section returns its text WITH evidence via `Slot.read`
  (stored vs usable; blocked by name), a row where the contributor substitutes the advertised support and is blocked
  by name, a row where another member's alternative repairs it — the SLOT's second instance.
- DESIGN-CTX §1 baseline paragraph (ACL row store with a nullable selected id: what the slot gives beyond it).
- Decision entries: LANG-101 (the SLOT and `interp`), HOSTING-next (the resident as a Prot term; NanoBridge deleted;
  LostReply), each with critique + meta-critique. Check the next free numbers on origin/main first.
- One prose commit per landing, by rule 1 (WORK-RULES-20261027.md); say what breaks (the resident's `Mem` gains a
  field; `Prog` is a `Prot`; `ResidentRun.Runs` is at `Tick`; `ContextualFailures` is `LostReply`).

## Box safety (verbatim from the brief)
Never kill by pattern. No `pkill -f <anything>`, no `pkill -x <bare word>`, no `killall`, no `kill -u`. A process you
started is stopped by the PID in its PID file, and only that; no PID file, no kill. Never `git stash`. Never run an
unfiltered `-p <crate>` test suite. Never delete anything outside your own worktree/scratch.
