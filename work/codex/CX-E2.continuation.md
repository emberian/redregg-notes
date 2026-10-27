# CX-E2 continuation (written 2026-10-23 by CX-E2 at ~490K tokens; the successor builds E2b)

## Who / what
CX-E2: E2 (the member-socket model) + PROT-3's host half, beside the Lang worker. NEVER edit Lang/**.
Grants: R-0052 (Hosting/Proofs/**, gates/tcb.tsv, launcher/tests/**); R-0054 (Protocol/Command/Machine.lean,
Protocol/Proofs/{Command,Incoming}.lean, excluded from CX-P5 "for the duration"); R-0060 (Protocol/Rows/Loopback.lean);
R-0061 (Protocol/Rows.lean, decisions/protocol.md one entry: USED for PROTOCOL-64). CX-P5 holds the rest of Protocol/**
and (R-0055) Hosting/Proofs ripple of 3 EXISTING files: never edit a file another worker holds; new modules are safe.
Read first: promo/IMPACT-E2.md (§1 measurement, §4 T0 as built, §5 E2b design), promo/READ-E2-grok.md,
promo/READ-E2b-grok.md (the conditions), RULINGS R-0058, R-0062, the report codex/CX-E2.report.md tail.

## Landed
- b4a7f38 hosting: bell_resident_conforms (Hosting/Proofs/BellConform.lean; cross-tick; plant = decideTick re-asks the
  kept pending ring, reds act_debt:248 with decide_* sorried in the plant run; ResidentRun green).
- e2905e7 protocol: T0 / PROTOCOL-64 (settled checks ownSettle on follow's own World; settled_ok, step_settled_ok;
  4 settled_* RESTATES-MEANING; Loopback rerun; rows plants settleDecline 13 / trustLookup 1 -> contradicted).
Worktree hbox:/tank/dregg-build/nanodregg/wt/e2 is CLEAN at e2905e7 (main). .lake warm (whole tree built, 727 jobs).

## Open: E2b, RELEASED TO BUILD by R-0062 under READ-E2b-grok's two conditions
1. THIS theorem's plant (not T0's): `Hosting/Resident/Run.lean:268-273` Cmd.argv's invoke arm prints
   `answerArg r r.text` instead of `answerArg r t`. Expected: delivered_answer_committed RED; settled_ok,
   step_settled_ok, tick_counts, bell_resident_conforms, answerArg_reads GREEN; launcher/tests/resident_bell.rs's
   answer-text row RED (deployed). Measure all of it; the log must show settled_ok green.
2. The module docstring (and IMPACT §5.3) says: a commit whose reply is lost (committed, reply never arrives: follow
   appends then dies before port.send, Host/Follow.lean loop) is PROT-5's at-most-once and OUT of this card; this
   card does not claim the converse of ok => journaled.
Then land `hosting:` fast (with --cross-layer for any Protocol/Proofs file) + the gates/tcb.tsv row EXACTLY as quoted in
IMPACT §5.1 / READ-E2b §1. Before landing: READY-IMPACT E2b-BUILT? R-0062 says "Then hosting: fast; the tcb row as
quoted" (no second read demanded); IMPACT §5.5 promised READY-IMPACT E2b-BUILT: do it (a WORKLOG + READY line) and poll
briefly; if ROOT says land, land.

### What to build (IMPACT §5.2-§5.3; names fixed by the reads)
- Hosting/Proofs/Socket.lean (new): `FollowRun` (inductive Prop: start reply, then step on each `r.cont = some k`
  with SOME result, follow's World may fold-extend between frames — use `∃ l, World.fold X.env f.world l = .ok g.world`
  unless a named Extends exists; ends in `.done e o r`), `SocketRel` (.error -> True; .ok rr -> rr.exit = ok ->
  ∃ f₀, FollowRun … (Command.start X me f₀ (c.argv conf)) (done of rr)), `StdioLeg` (∀ .cmd c x ∈ es, SocketRel),
  `resident_argv_on_stdio` (every Cmd tickP builds starts "read"/"invoke"; Verb.onStdio, Protocol/Command/Stdio.lean:23),
  `deliverAfter_unsettled` (exit ∉ {ok, refused}: DeliverAfter tail = the .error tail; ResidentRun.lean:75-84),
  `delivered_answer_committed` (statement IMPACT §5.3). Docstring: the row is NOT stated; `answered_row_is_kept_answer`
  is a named docstring waiting for the Bell witness (LANG card); LITP's journey-row sentence NOT deleted; lost reply = PROT-5;
  stdout of an ok reply is NOT the journal entry (settled returns step 3's pre-submit `out`).
- Protocol lemmas (Protocol/Proofs/Command.lean, R-0054; or private in Socket.lean if the grant is in doubt — ASK first):
  `invoke_done_ok_phase4` (an invoke command's only done ok is the phase-4 settled arm; prove like step_submit_planned,
  Command.lean:303: unfold step next; repeat' split; dispatch), `step_submit_cont` (a `.submit call k` reply has
  State.ofBytes k = some ⟨argv, 4, acc⟩ with acc.getLast? = some call: `next` = State.bytes, Machine.lean:243, plus the
  state codec roundtrip), `invokeArgv_body` (parse of invokeArgv conf sh arg (Hosting/Resident/Bell.lean) is the invoke
  cmd on conf.bell / sh.answer / arg / --via conf.grant (Protocol/Command/Verb.lean:349-352); body's invoke arm is
  Lang.argsOf of the arg text (Machine.lean:331-334); with answerArg_reads (Hosting/Proofs/Resident.lean:168) at a method
  of type answerArgTy the args are answerDatum r t; the method type = answerArgTy because Shape.read refused anything
  else on follow's own description: the description/readTy roundtrip is the LARGEST piece — measure it first, and if it
  needs Lang-side lemmas that do not exist, STOP and ASK (Lang/** is not ours)).
- Committed => journal: `step_settled_ok` (landed) then `Settle.settle_committed` (Protocol/Proofs/Settle.lean:158), NO
  CollidesAmong disjunct (check_committed route withdrawn).

## Tools / lessons (measured this session)
- Edit scripts: write python locally in the scratchpad, scp to hbox:/tank/dregg-build/nanodregg/logs/e2/, run there.
  Heredocs inside ssh quoting break. Use `ssh -n` for detached jobs; record PIDs inside the remote shell with an
  ABSOLUTE pid path (a relative path after `cd … &&` in a backgrounded list wrote nowhere once).
- Build: `SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build lake build <targets>`; whole tree ~5 min warm (727 jobs).
  rows: `.lake/build/bin/rows`, `--deployed`, `--harness-control` (must be RED). ~1 min each.
- Plants that break a lemma the new proof imports: `sorry` those lemmas IN THE PLANT RUN ONLY with a file-level
  `set_option warningAsError false` after the imports (per-decl `set_option … in` before a docstring does not parse);
  and make the new proof read the definition's own arms, not the broken lemma, so its red is its own.
- C3 (gates/closure.py): a Proofs module may export only Prop-valued defs and theorems; computational helpers PRIVATE.
- scripts/commit refusals seen: C3; missing `SIZE: <metric>: <why>` lines (the judge names each metric). Fix forward.
- decls: RESTATES-MEANING: <full name> lines for any changed statement (a binder change counts).
- Rows judge is NOT in the fast judge (convergence reads it): run rows yourself before any Protocol landing.

## Not mine / do not touch
Lang/**, CX-P5's Protocol files, the three existing Hosting/Proofs files CX-P5 ripples under R-0055.
