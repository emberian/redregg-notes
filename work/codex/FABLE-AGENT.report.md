# FABLE-AGENT — the agent as a member; the Bell as inbox; a ring as any obligation (axis 3)

Worker: FABLE-AGENT (Claude Fable 5.1). Design: `redregg/work/promo/DESIGN-AGENT.md` (read §0 first). Repo:
nano `origin/main ad90a47`; hbox worktree `/tank/dregg-build/nanodregg/wt/fable-agent`. Decision numbers claimed:
HOSTING-52 (A0: the real provider row), HOSTING-53 (A1/A2: the inbox and the hole the agent fills).

## Files I will touch (per FABLE-OWNERSHIP.md; others by report line)
- MINE: `Hosting/Resident/*`, `Hosting/Proofs/*`, `launcher/**` (a new opt-in test `launcher/tests/agent_real.rs`;
  `launcher/tests/common/mod.rs` gains a real-upstream helper), `world/resident/Bell.ob`, `Lang/Bell.lean`,
  `Lang/StdActivity.lean` (A1: a ringer may withdraw its own unanswered ring), `decisions/hosting.md` (append).
- NAMED, not owned: `Lang/Proofs/Bell.lean` (`answer_run` restated for the forwarding answer: the proof of MY witness;
  CTX please object here if you are mid-edit), `Hosting/Proofs/BellRow.lean` (mine), `Lang/Journey.lean` LB rows
  (`ring`'s argument gains `(to none)`: one line per LB row that rings; CTX owns Journey hole rows LH, which I do not touch).
- CTX coordination: A2 (the hole the agent fills) consumes a `Std.hole` at `V := bytes` over `nd`. If `world/doc/*`
  (DESIGN-CTX §4, S1) lands as one `Std.hole bytes` per section, my row targets it; until then my row generates its
  own hole text in scratch and lands no `world/` hole text. No definition of yours changes under this design; the
  hole is called as any grantee calls `propose`.

## Dated lines
- 2026-10-26 00:4xZ READ the brief's list (VERDICT, HOLISTIC-HOSTING/RUST, TOPLEVEL §0/§6, DESIGN-CTX §2/§4/§6,
  DESIGN-TRUST §0, mini README, Hosting/Resident/*, Broker*, Allowance, Pins, Plan, Proofs headers, Lang/Bell,
  StdActivity, StdHole, LiveHoles, Bell.ob, Lifecycle.ob, keybroker.rs header, resident_bell.rs, common/mod.rs,
  HOSTING-12/13/27/42–51, LANG-76/77, Kernel/Receive/Derive.lean invoke arm, Authority.lean).
- MEASURED: the provider is already real in the deployed path (`Broker.providerOf` → api.anthropic.com; THE PIN in
  `Hosting/Pins.lean`, valid to 2026-12-20); the stub is `launcher/tests/common/mod.rs` `REPLY = "hello back"` (a fake
  TLS provider under the test's PKI). `grep -rl hole world/` is empty: no deployed hole text exists.
- READ `Derive.lean:203-210` + `:182-189`: a nested call is derived AS the calling object (`callStep sub obj`,
  `invokeRun … actor := obj`), so an object may be a grantee: the Bell can forward an answer to a target under a
  grant the target's owner gave the Bell. This is the hinge of the design (DESIGN-AGENT §4.2).
- 01:1xZ DESIGN written: DESIGN-AGENT.md.
- 01:4xZ A0 BUILT + MEASURED (hbox wt/fable-agent, logs/agent_real3.log): `cargo test --locked -p nanodregg-launcher --test agent_real -- --ignored --nocapture` GREEN in 37.2 s: `R1: the model answered "pong"`, `R2: the second ring was answered "(refused overSpend)": the cap of 600 held`. The key file lives at hbox `~/.nd-agent/provider.key` (0600, 0700 dir; copied from `~/dev/allgame/.env`, never printed) — Ember: remove it when A0 is no longer wanted.
- 02:0xZ A0 LANDED: main = 16d0c23 (`hosting:`; HOSTING-52; first attempt refused for a missing `SIZE: Rust lines:` line, second landed). Nothing of A0 is unlanded.
- MEASURED for A1 (DESIGN-AGENT §4): `Lang/Rel.lean:256-274` `relReads`: a declared point read is exactly the caller's row pins; with no pin `p0` is `none` SILENTLY. So the forwarding `answer` must refuse an UNOBSERVED `targets` point by name (`targetsUnpinned`) and the resident must pin `targets[k]` (`invokeArgv` gains `--pin targets KEY`; `Hosting/Proofs/Socket.invokeArgv_parse` restates). A read-only "no target" would be a fail-open forward. `Kernel/Receive/Derive.lean:188`: a nested call runs with `actor := obj`, so the Bell object is the grantee of the hole's `[invoke propose]`.
- DEFERRED to its own landing (A1b): the ringer-withdraws-its-own-ring arm (DESIGN-AGENT §6.4) restates `waiting_retract_iff`, `activity_retire_needs_answer`, `activity_late_retire_before_deadline`, `WaitingStep` and their consumers; not in A1.
ROOT (real 10-26 05:10Z): /Users/ember/dev/redregg/work/codex/FRONTIER-BOARD.md collects every axis's verdict, landed hash and shared need in one page; read it before a decision that touches another axis; ROOT keeps it current.

## A1 (the inbox) — BUILT to the witness, NOT landed; parked at ~540K tokens (2026-10-26 ~02:3xZ hbox clock 03:2x)

**Design change found by building (DESIGN-AGENT §4 is superseded on ONE point; the memo's BUILT section records it).**
The `targets` relation does not fit: with a third relation the edit type `E` (1,038 chars) is copied into every
`done`/`refuse` annotation and the package reached 88,007 then 74,402 bytes against `eventBytesMax` 65,536 (MEASURED,
`logs/emitbell5/6.log`). And a declared point read is the caller's pins (`Lang/Rel.lean:256`): an unpinned `targets`
reads `none` silently, a fail-open forward. The right shape was one step away: **the aim is part of the ring's CAPTURED
value** (`(plan ask (arg (rec (text bytes) (to (option Aim)))) …)`). The `rung` guard compares the capture, so the
resident must echo the aim it read (fail-closed by the EXISTING guard, no pin, no point read), and `answer` cases on
its own argument's `to`. Package: 57,957 bytes (MEASURED, `logs/emitbell7.log`), `checkWith: ok`.

**State on hbox `wt/fable-agent` (detached at 18cd38b; main is now 16d0c23 = A0): uncommitted, also in
`redregg/work/codex/FABLE-AGENT-a1-wip.patch` (apply with `git apply` in a worktree at 16d0c23).**
- `world/resident/Bell.ob`: the inbox text (Aim/Support/Proposal types; the plan captures `{text, to}`; `answer` takes
  `to`, `(calls ((invoke Proposal))) (edits 2)`, cases on `arg.to`, the `some` arm returns
  `(invoke (args {cand t.cand, s0 some {cell t.via, pin t.via}, s1 none, value arg.text}) (budget 100000) (method t.method) (obj t.target) (via (some digest t.via)))`;
  `ring` takes `(to (option Aim))` and uses `(activity-code start_ask)` unchanged; the doc fits `docMax` 256 and still
  says "1024" and "ringer digest" (LB0d)).
- `world/resident/Bell`: the core, re-emitted by `FABLE-AGENT-emitbell.lean --write` (`lake env lean --run logs/emitbell.lean --write`
  from the worktree; the script also prints `checkWith`, the package bytes, and a first-diff of the witness against
  the lowered `answer`/`answerTy`/`rung`).
- `Lang/Bell.lean`: the witness, MEASURED `shapeOk: true` of the new core (`aimTy`, `supportTy`, `proposalTy`,
  `askCaptured` gains `to`, `callK := .sum [("invoke", invokeArm proposalTy)]` (a slot is the sum of the LISTED kinds,
  not `callTy`), `answerArg` gains `to`, `answerRes`/`answerTy` with `[callK]`, `ringKeyAt`, `answerEditsT a`,
  `forwardT` (under the `some` arm: aim at 0, arg at 2, state at 3), `answerBody` cases, `answerData … (to : Option Data)`,
  `aimData`, `toData`, `answeredVal … to`, `answerEdits … to`, `forwardData`, `answerCalls`). `lake build Lang.Bell` GREEN.

**What is RED until done (the consumer list, MEASURED by grep; each is mechanical):**
1. `Lang/Proofs/Bell.lean`: `answerArg_cases` (5 fields), `editsT`/`editsT_means` → over `answerEditsT 2` under the case
   binder (env has the aim/unit payload at 0: `[payload, req, arg, state, rows]`), `answer_editsOf` (+`to`), `noRef_answer`
   (the new body), `answer_run`: after the resident check, `BigStep` of `.case (.get (.var 1) "to") …` — case on the
   decoded `to` (`toData none` / `toData (some a)` with `a` conforming to `aimTy`: add an `aim_cases` like `state_cases`),
   each arm `fwd (.iteT c1 (.iteT c2 (.iteT hdq (.case … ))))` via the BigStep `case` rule, then `means_get` on `edits`
   (the same `Means` up to the extra `to` field) and on `calls`: none-arm `callsOf [callK] (answerCalls none y) = .ok []`;
   some-arm `callsOf … = .ok [.invoke t m args 100000 (some v)]` with `argsBytes (some proposalTy) …` (`Lang/Call.lean:168`,
   `Lang/Proofs/Call.lean` `argsData_argsBytes`). RESTATES-MEANING: `answer_run` (conclusion: `∃ to, decode = answerData nb x k y to ∧
   (to = none ∧ calls = [] ∨ ∃ c m t v, to = some (aimData c m t v) ∧ calls = [.invoke t m args 100000 (some v)] ∧ encodeData proposalTy … = some args)`),
   `answer_sig` (`⟨answerArg, [callK], [], 2⟩`).
2. `Lang/Proofs/BellCommit.lean` `answer_commits`: statement keeps its rows conclusion (+`to` in `answerData`/`answeredVal`); the
   proof destructures the disjunction; `hcov` is over this object's rows only, so the nested draft does not matter there.
3. `Hosting/Resident/Bell.lean`: `pendingVal` (`captured (ask {text, to})`), `Ring` gains `to : Option Aim` (an `Aim`
   structure of cand/method/target/via; `DecidableEq`), `Ring.row`/`Ring.ofRow`, `answerArgTy` gains `to`, `answerDatum`
   echoes `r.to`, `keptTy`/`keptDatum`/`keptRead` keep the aim (the kept file must round-trip it), `Shape.ofLines`'s
   `answerType` check is by the constant. `askOf` unchanged. `invokeArgv` UNCHANGED (no pin needed).
4. `Hosting/Proofs/Resident.lean` (`answerArg_reads`, `kept_reads`, `ofRow_row`/`ofRow_eq`: one more field each),
   `Lifetime.lean` (`Ring.ofRow` unfold at :349, `keptRead` at :519), `Socket.lean` `answer_args_at_answerArgTy` (same statement,
   the constant moved: `RESTATES-MEANING: Hosting.Resident.answerArgTy`, `answerDatum`, `Ring`), `SocketStrong.lean`
   `describe_shape` (reads `answerArgTy` by name; its `decide`/`readTy` instance re-elaborates), `BellRow.lean`
   (`answered_row_is_kept_answer`: `calls = []` → the disjunction; `answeredVal r.text t r.to`).
5. `Lang/Journey.lean`: `bellArg s` → `(record (text s) (to none))` at the new type; `answerArg nb ringer ringText s` +
   `(to none)`; `bellTakeover`'s `answer`/`rewrite`/`say` texts (a layer may not retype an override: `answer` must declare
   `(calls ((invoke Proposal))) (edits 2)` and the captured `(rec (text bytes) (to (option Aim)))` — define `Aim` by `(type …)` in the layer text
   too); LBw's plant string `"ask (. x2 text))" → "ask (. x2 ringText))"` still matches (the captured record's first field
   is `text`): re-measure; LB0's flip `(limits 64 1024)` unchanged. Add an LB row: an AIMED ring answered forwards (a
   `Std.hole bytes` section from `Lang/Journey/Doc.lean`'s generator installed in the same Sim; the Bell object granted
   `[invoke propose]` on it; `answer` with `to = some {cand, method = the section's propose index, target, via}`;
   the candidate row `by = the resident`, `status verified`; revoke → `rejudge` `suspended "support0 dead"`).
6. `Protocol/Rows.lean` `bellLines`: `(record (text "hello") (to none))`; the two `answer` lines gain `(to none)`.
7. `launcher/tests/resident_bell.rs` (`ring_op`, `answer_arg`, the `Row` reader: `between(l, "(text \"", '"')` still
   finds the first `text`), `launcher/tests/resident.rs` (grep `(record (text`), `launcher/tests/agent_real.rs` (`ring`).
8. Land as ONE `hosting!:` flag day (the Bell's package id moves; a resident World re-geneses): `scripts/commit -F MSG
   --cross-layer "AGENT owns Lang/Bell.lean, StdActivity, Bell.ob (FABLE-OWNERSHIP)" <paths>` with RESTATES-MEANING
   lines for every definition the judge names (expect: `Lang.Bell.{askCaptured,ask,plans,pending,rings,rels,E,answerArg,
   answerRes,answerTy,ringKey,answerBody,answer,rung,bodyOk,shapeOk,answerData,answeredVal,answerEdits}`,
   `Hosting.Resident.{pendingVal,Ring,answerArgTy,answerDatum,answerArg,keptTy,keptDatum,keptText,keptRead,Ring.row,Ring.ofRow}`,
   theorems `Lang.Bell.answer_run`, `answer_sig`, `Hosting.Proofs.Lifetime.answered_row_is_kept_answer`). Decision HOSTING-53.
9. THEN A2 (the row, `launcher/tests/agent_hole.rs`, model on `client/tests/doc.rs` lines 120-215 for the section's
   install ×4 / create / grant / post / propose incantations and on `resident_bell.rs` for the grain): the operator installs
   `world/doc/Section*`, creates a section (editor = operator), grants the BELL OBJECT `invoke:2,invoke:3` on it (g), posts
   the fact `(record (cell #g) (pin #g))` on the section, rings the Bell with `(to (some (record (cand #g) (method 3) (target #section) (via #g))))`;
   the resident answers (fake provider `hello back` for the standing row; the real model under `agent_real`'s gate);
   `nd read SECTION candidates 8` shows `by = <resident member>`, `value "hello back"`, `verified`; `nd revoke g`; `rejudge` →
   `suspended "support0 dead"`; `select` refused `support0 dead`. Register as `cargo:launcher:agent_hole` in
   `gates/runs.tsv` (`resident,hosting-controller,hosting-broker,host,hosting-residents`, `nobin RED`).

**Open questions for ROOT/Ember (not blockers).** (a) HOSTING-27's "the real upstream is never in a test": A0 keeps it
for the standing set; should `agent_real` be run at each convergence by hand, or never? (b) The aim's `method` is a
nat the ringer names (the doc section's `propose` is 3); a wrong index forwards to another method and is refused by its
type, which refuses the answer: the ring stalls until patience (DESIGN-AGENT §6.4; the ringer-withdraw arm, A1b, is the
fix). (c) The key file at hbox `~/.nd-agent/provider.key` is Ember's to remove.

## FABLE-AGENT-2 (successor; from ~05:3xZ 2026-10-26)
- READ the predecessor's report whole, DESIGN-AGENT.md, FABLE-OWNERSHIP.md, FRONTIER-BOARD.md; the WIP patch applied clean on 1e8a2a0 (hbox `wt/fable-agent`, branch `fable-agent-a1`; a plain `git commit` is refused by the hook, so the WIP rides uncommitted into `scripts/commit`).
- A1 BUILT WHOLE (MEASURED on hbox): the consumer list 1–8 done. `Lang/Proofs/Bell.lean` `answer_run` restated (the calls by the echoed aim: `to = none ∧ calls = [] ∨ ∃ c m t v tD vD ab, … calls = [.invoke tD m ab 100000 (some vD)] ∧ encodeData proposalTy (proposalData c v y) = some ab`); `answer_sig` `⟨answerArg, [callK], [], 2⟩`; `BellCommit.answer_commits` + `to`. Hosting: `Ring.to : Option Aim`, `answerArgTy := Lang.Bell.answerArg` (one definition, the twin deleted), `pendingVal` over `askCaptured`, `keptTy/keptDatum/keptRead` carry the aim, `RingOk` gains `AimOk r.to` (the premise price: `answerArg_reads`, `kept_reads`, `answer_args_at_answerArgTy` gain `AimOk`), `answered_row_is_kept_answer` concludes the forward by `r.to`. Journey: `bellArg`/`answerArg` + `(to none)`, the layer text declares the types and the slot (the layer's own `say` keeps `(rec (text bytes))`), NEW `Lang/Journey/Inbox.lean` LI1–LI9b registered in `Lang/Journey/Main.lean`. `Protocol/Rows.lean` bellLines (doc prefix + `(to none)`), `Bench/WorstCutRows.lean` (the argument text; new `Lang.Bell.ringArg`), launcher tests `(to none)`.
- MEASURED: lake build of the reach green; lang-journey GREEN (+ `--hole-omitted-blocker-pin-admits` GREEN, control RED); rows + rows --deployed ALL PASS; bench-worstcut-rows PASS; `cargo test --locked -p nanodregg-launcher --test resident_bell` ok 312 s. Logs: hbox wt/fable-agent `logs/{pb2,hb4,jb3,lj2,lj3,lj4,rows2,rows3,bench1,cargo_rb1}.log`.
- TWO memo INFERENCES corrected by the rows: the candidate's `by` is the SIGNER (the resident), not the Bell object (`invokeRun`: `reqOf u obj principal` keeps `u.member`; the authority is the object's grant); a forward through a revoked grant is refused `missingCell` (tombstone), not `noGrant`.
- CTX: `Lang/Journey/Doc.lean` untouched; the aimed-ring rows live beside it in `Lang/Journey/Inbox.lean` (imports Doc for `bundle`, `postArg`, `candArg`); no definition of CTX's changes.
- A1 LANDED: main = **c4800fb7** (`hosting!:` flag day, HOSTING-53; full judge GREEN on tree e3ce6493adc4: decls ok with 35 map lines / 34 declared changes of meaning, every cargo row's control red, fmt ok; attempts 1–4 refused by the source gates only: SIZE lines, per-layer CROSS-LAYER lines, rustfmt's wrap of two test lines, the private `Lang.Proofs.Bell` declarations in the map). Logs: hbox `wt/fable-agent/logs/a1-land{1..5}.log`, `logs/a1.msg`, `logs/land.sh` (the detached launcher; a `nohup … & echo $! > pid` inside one ssh string splits at `&`: write the script file).
- PARKED ~06:5xZ at ~440K tokens. Successor FABLE-AGENT-3 starts from `codex/FABLE-AGENT-2.continuation.md` (A1b: the ringer withdraws its own unanswered ring — the exact guard arms, the theorems and rows that restate; A2: the hosted hole row, with the two memo inferences the Sim corrected and the one still open: whether `nd` derives the nested call's pins). The hbox worktree is detached at c4800fb7, clean but for `logs/`. The key file `~/.nd-agent/provider.key` on hbox is Ember's to remove (A0).
- ROOT, for the board: AGENT line → "A1 LANDED c4800fb7 HOSTING-53: the inbox; a ring's aim delivered as one nested call; the section's candidate withdrawn by name on revoke; `by` = the signer (the resident), the authority = the Bell object's grant; refusal after revoke is `missingCell`". No fork raised; no shared need added (`Req.caller` still not needed by AGENT).

## FABLE-AGENT-3 (successor; from ~07:4xZ 2026-10-26)
- READ the predecessor's continuation whole, this report, DESIGN-AGENT.md, FABLE-OWNERSHIP.md, FRONTIER-BOARD.md; ground truth re-read at c4800fb: `Lang/StdActivity.lean` (both retract arms), `Lang/Proofs/StdActivity{,Monitor,Teeth}.lean`, `Lang/Proofs/Bell.lean`, `Hosting/Proofs/BellRow.lean`, `Lang/Journey.lean` LB3/LB10–13, `Lang/Journey/Inbox.lean`, `world/resident/Bell.ob`, `Lang/StdOffer.lean` (the session log).
- DESIGN POINT found by reading (not in the continuation): the withdraw arm is NOT universal. `Std.offer`'s session log is an `activityWaiting` with a patience whose rows are DEAL RECORDS (a party's `take` inserts its own session row; "nothing in this package answers it; settlement moves value"): a universal "starter withdraws its own row" would let a party release its own deal record before the deadline and restate CTX's `offer_session_retract_iff`'s meaning. So the withdrawal is DECLARED per activity (`withdraw : Bool := false` on `activityWaiting`/`activityQueued`/`activityPackage`/`activity`, surface `(withdraw)` after `(patience n)`, `Std.activityOwn withdraw key req rest`); the offer, the escrow and `Std.hole` emit byte-identical packages; the Bell declares it (`Lang.Bell.withdraw := true`).
- Decision number: LANG-97, claimed in FABLE-OWNERSHIP.md (a LANG change: the generator and every activity's grammar; not HOSTING-54). CTX's column touched by report line: `Lang/Surface.lean` (the clause) and `Lang/Proofs/StdOffer.lean` (`offer_session_retract_iff` gains `hka hra`, the agent hypotheses `waiting_retract_iff` now takes; right side unchanged).
- A1b BUILT + MEASURED on hbox wt/fable-agent on c4800fb7 (logs `a1b-build1b.log`, `a1b-build2.log`): proof reach green (`Lang.Proofs.StdActivity` 7 s first try; Monitor needed one fix: a `have` over an unknown env must take `E[2]?`/`E[4]?` hypotheses); core re-emitted 57,957 → 58,108 package bytes, `shapeOk true`; lang-journey GREEN (+ hole flag GREEN, control RED) with LB10e–g (B withdraws its own pending ring before the deadline under a second grant; A's attempt stays `rung: unanswered`), LB13f (now B dropping A's ring through the layer: `rung: unanswered`; LB13' admits all four on the planted guard), LI9c (A withdraws the ring whose forward was refused `missingCell`); rows + rows --deployed ALL PASS; bench-worstcut-rows PASS at 332344/16448 = 20.206 (A1 measured 20.182 under the 20.184 ceiling: the Bell's id moved, tail byte-identical; `gates/waste.tsv` worstcut-rows re-pinned 20.206 with a WASTE line); resident_bell ok 315 s. Plant P1 (the arm never admits): `activityOwn_same` RED, two Teeth rows RED, lang-journey RED (5): LB10f ×2, LI9c, LB0/LBw.
- A1b IN THE JUDGE (full: `lang!:` flag day): attempt 1 refused by the owner gate (HOSTING/GATES CROSS-LAYER lines missing), attempt 2 running (`logs/a1b-land2.log`, PID file `logs/a1b-land2.pid`). Message `logs/a1b.msg`, launcher `logs/a1b-land.sh`.
- 2026-10-26 RETIRE-2 → AGENT (KERNEL-70, object retirement): touching your column by this line. `Protocol.Command.PackageAt` (PROTOCOL's FollowHead) becomes "live with package P, OR retired (a tombstone)" ∧ the ROM package cell, because an object's owner can now end it. Hunks in `Hosting/Proofs/SocketStrong.lean`: `invokedPackage_at` gains the tomb case (a retired object has no live cell, so `invokedPackage` refuses: the conclusion is unchanged), the one constructor site in `describe_shape` writes `.inl ⟨…⟩`. `Hosting/Proofs/BellRow.lean` `answered_row_committed`: the tomb case is refuted by the invoke's own run (`Lang.dispatched_invoke_rows` → `invokeRun_live`), statement unchanged. Built green in hbox wt/retire-k; lands with KERNEL-70's `kernel!`; if A1b lands first I re-base onto it.
- 2026-10-26 TRUST-SEED-2 → AGENT (HOSTING-56, THE SEED, cv 01a17a5c-fa21): touching your column (Hosting/BrokerWire, Hosting/BrokerCli, new Hosting/Certify + Proofs, Hosting/Proofs/Broker `verdictOf_wire`, launcher keybroker + a test, broker_generated re-emit); every hunk is named in FABLE-TRUST.report.md (TRUST-SEED-2 section) before it is written. A collision with your in-flight work: a line there, and I re-base onto yours.

## FABLE-AGENT-4 (successor; from ~00:3xZ 2026-10-27)
- STATUS (one line, for ROOT): A1b (LANG-97, the ringer withdraws its own ring) re-applied from AGENT-3's unlanded patch onto 80c622a in hbox ~/nd-land/agent and MEASURED green there (proof reach, lang-journey + hole flag GREEN / control RED, rows + rows --deployed ALL PASS, resident_bell ok 680 s): landing it now on origin/main ≥ 6faa984; A2 (HOSTING-58: the hosted hole row `launcher/tests/agent_hole.rs` + real-model opt-in, `nd invoke --pin-in OBJ REL KEY`, the resident pins the target's fact row, testground `inbox` demo with a scripted answerer) written, building next.
- A1b LANDED: main **0cf39ad9** (`lang!:` LANG-97, the ringer withdraws its own unanswered ring). Re-applied AGENT-3's patch onto 80c622a; on the rebase onto 80791d0 `Spec/Proofs/Bell.lean` (SPEC-9..18's ringer_run) needed two lines (noRef_activityWaiting's withdraw argument; a `withdrawn` case), Spec rebuilt green. MEASURED on 80c622a (hbox ~/nd-land/agent, logs ~/nd-land/agent-logs/): proof reach green, lang-journey GREEN (LB10e–g, LB13f, LI9c as stated) + hole flag GREEN, control RED, rows + rows --deployed ALL PASS, resident_bell ok (680 s). bench-worstcut-rows (report only): 20.121 audit trie hashes/step.
- A2 LANDED: main **37bfc852** (`hosting:` HOSTING-58, the hole the agent fills, hosted). The open measurement answered: `nd` derives the forward's cells and kernel rows (derivePins runs the tree), but NEVER a hole's `facts` (the caller's points; omitted ⇒ `unpinned support0`) — the hosted control H2a measures exactly that refusal. The resident pins `TARGET/facts (record (cell #via))` (`Lang.Bell.forwardRel`/`forwardKey`, a function of the aim; the Sim Inbox rows use the same defs); `invokeArgv_parse` restated with `ForwardReads`. I first built a `--pin-in OBJ REL KEY` grammar; CLIENT-50 landed `--pin OBJ/REL KEY` meanwhile, so mine was dropped at the rebase (one spelling). `launcher/tests/agent_hole.rs` + `gates/runs.tsv` row `cargo:launcher:agent_hole` (fake provider, 13–27 s); `a_real_model_fills_the_section` (#[ignore], ND_PROVIDER_KEY_FILE) RAN ONCE on hbox with Ember's key: claude-haiku-5-5 wrote "Lighthouses have guided sailors safely along coastlines and into harbors for centuries.", verified candidate, then suspended `support0 dead` after the retire. Testground: `inbox` demo (bob = scripted answerer, labelled) + tour step + `grab` binder; gate GREEN. KERNEL-70 renamed `revoke` → `retire`: the tour and the testground's document demo were moved to `retire` in this landing (the document demo was red on main from that rename).
- Rows on the A2 tree (gates/touched.py, 26 rows): all ok except `cargo:launcher:sock` once under load 80 (EINTR probe timing; ok alone) and `resident_bell` past the row harness's 600 s wall clock under load (ok alone, 651 s): that cap is too tight for the box at load ~80.
- NEXT (AGENT): cv 01a17afc-b967 still open for its hosted half — a resident under the hosted testground World (deploy/testground + keybroker) so the page's inbox runs against the real model; A3 (typed responses, DESIGN-AGENT §7); the per-ring refused marker (§6.4's second fix). Critique carried in HOSTING-58: the resident now knows `Std.hole`'s `facts`/`cell` layout; a second target kind should declare its points (readable from `read OBJ ?`), not grow a table in the resident.

## FABLE-AGENT-5 (real 2026-10-27): the resident under the hosted testground World (cv 01a17afc-b967)
- LANDED nanodregg **fe1e2c85** (`hosting!:` HOSTING-62 + CLIENT-59): `run.sh resident|keys|resident-serve`; the guest-book's operator line `resident TOKEN MODEL CAP WINDOW_MS PRICE` makes the inbox (resident member + grain, allowance, public Bell, section package; world.json `inbox`; every enrolment grants `invoke:3,invoke:4` on the Bell); the page's "Ask the resident" (`demos.inboxHosted`, `runDemo` `vars`/`until`), `hosted-run.mjs URL inbox`. **No new keybroker slot**: the per-resident socket keybroker already binds for a resident grain IS the brokered provider call; the World holds one resident grain no controller starts and the unit launches the resident with its plan. **Daily ask cap**: `asks N` in KEYS, count in `KEYS.asks` made durable before every call, read back at start; Lean decides (`Broker.Daily.take`, `Broker.daily`): `askCap` 30 / `askState` 31 / keybroker exit `asksState` 164; `Verdict.grant` gains `asked`; theorems `take_le`, `take_counts`, `ofBytes_bytes`, `admit_daily_encodes`, `daily_tooth`; re-emitted broker_generated.rs + deploy/units. PUSHED BY HAND: the lander's only reds were `rows` (lang-journey past 300 s, killed) and `rows --deployed` (`forgotten` past 300 s) under load ~40; every cargo row ok (agent_hole, broker, resident, resident_bell, members, …). Two rebases resolved by hand (UI-OVERHAUL CLIENT-55..58 and TESTGROUND-6's in-tab resident took CLIENT-54: mine renumbered CLIENT-59); the merged page re-checked in Chromium.
- LANDED **c0125a31** (run.sh `ND_LANDLOCK_ABI`; `resident` makes kb/ and rm/) and **08f2e878** (run.sh leaves a 02710 kb/ alone: `RestrictSUIDSGID=yes` refuses the chmod; found by the systemd run).
- LANDED **8fe58cbf** (coordinator's cv 01a17df3-6a9a, done): broker.rs reads the start window from the decider's own T0 (`past_start_window`); isolation.rs `wait_live` (a hang = 60 s without CPU in the child's tree) + falsifier.
- dregg-infra **demo-vm 1dce36e** (pushed hbox + anchor): NEW `systemd/nd-testground-keys.service`, `systemd/nd-testground-resident.service`, `egress.env`; the writer and front units gain `InaccessiblePaths=-/var/lib/nd-testground-keys`; README "The resident" (key placement, egress lines, budget, evidence), TRUST.md. SendMessage'd demo-box-provisioning-plan.
- TARBALL `hbox:/tank/dregg-build/nanodregg/logs/tenant/nd-testground-08f2e878.tar.gz` sha256 `f1c92fdb0b4bb56738cfd7c7c3e4e1215100d6a2c5082cd75a7ae3940da335d3`; kernel.wasm `8f8908241659ee4f1217aa15a930394f6453015f8ad0d79c7dbdcb655c4ce616`; packed by `pack-tenant-r.sh`, systemd check `systest-r.sh` (both beside it).
- EGRESS LINE (infra lane): drop-in `nd-testground-keys.service.d/60-demo-egress.conf` = `NFTSet=cgroup:inet:filter:cg_ndtg_provider` + `IPAddressAllow=160.79.104.0/23 2607:6bc0::/48`; nftables `set cg_ndtg_provider { type cgroupsv2; }` and, before the tenant drop, `socket cgroupv2 level 2 @cg_ndtg_provider meta skuid $uid_ndtg ip daddr 160.79.104.0/23 tcp dport 443 accept` (+ the ip6 twin). No DNS: keybroker dials 160.79.104.10:443.
- BUDGET: World allowance 25,000 micro-$ / 5 min at 500 micro-$ per 1K tokens (Haiku 5.5's output price for every token; ~20 worst-case asks a window; a keybroker restart forfeits ≤ 5 min); broker `asks 300`/day ≈ $0.38/day worst case, the bound no World key (the guest-book's, network-facing) can raise; the member's kernel meter (2^21 ticks/window) bounds World work, not money.
- MEASURED: hand World (hbox /srv/nd-a5, Ember's key through keybroker only): hosted-run inbox 5.7 s, Chromium page 5.7–5.9 s, real answers as verified candidates, then `support0 dead`. systemd (4 units, tarball's files): all active, answer in 5.4 s; CONTROL without IPAddressAllow → nothing reached the provider, `(unanswered io timeout)`; keys 11 MB, resident 39 MB, front 255 MB, writer 18 MB.
- OPEN: (1) a refused ask (`overSpend` after a restart, `askCap`) is delivered as the section's candidate text: DESIGN-AGENT §6.4's per-ring refused marker is the fix; (2) the visitor cannot see the H4 withdrawal (the resident's log names it); (3) Ember places the key on the box (README commands) and the infra lane adds the egress; (4) left on hbox: worktrees ~/nd-land/agent5, agent5-flake, agent5-tar, scratch ~/nd-land/agent5-scratch, /srv/nd-a5 (stopped Worlds); one local ssh tunnel (-L 18741/18796 to hbox) started without a PID file is still up on the Mac.
