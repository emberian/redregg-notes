# P7 (GPT-6 row F, send) — continuation from the P5 worker

**Not started.** The P5 worker reached about 485K tokens when P5 was queued, which is past the 420K handoff line. It stopped without reading the P7 brief, so it learned nothing about row F itself. Start fresh with these two documents:

- the brief: `/private/tmp/claude-501/-Users-ember-dev-breadstuffs/ce776c01-2f59-4f57-8177-23008d71bf57/scratchpad/platform/briefs/P7-ROW-F-SEND.txt`
- row F of `/Users/ember/dev/redregg/work/grounding/GPT6-RESPONSE-ROWS-20261006.md`

## Box procedure that worked for P5 (EXECUTED, 10-07)

- **Lanes:** `ssh -F ~/.ssh/burst2-20261006.conf burst2-a '/srv/warm-base/mk-lane.sh <lane> --verify'`. Then `git fetch https://github.com/emberian/minidregg.git next` and `git checkout -B lane/<lane> FETCH_HEAD`.
- **Rebasing:** `next` gets rewritten. Rebase before queueing, and check whether the old base is still an ancestor.
- **Builds:** run them in tmux through a script that calls `/srv/pipeline/scripts/slot.sh env swarm-build lake build ...` (`. /srv/pipeline/box.env` first). Never write a flock chain.
  - Watch for completion with a background `until ssh ... grep -q ^EXIT log; do sleep 30; done`.
- **Inner loop:** `/srv/pipeline/scripts/lean-ask check FILE[:LINE]`. Add `--reload` after a rebase or an edit to an imported module.
- **Journeys:** the journey runs on the real Host from the lane's own binaries.
  1. Build the Lean exes `minidregg-host` and `minidregg-client-consent`.
  2. Build the Rust binaries `mini`, `minidregg-credential-signature-verifier` and `minidregg-link-sqlite-store`. Use `CARGO_TARGET_DIR=<lane>/rust-target` and `cargo build --bins` in `native/<crate>`. A sample script is at `burst2-a:/srv/lanes/plat-read-target-leg/cargo.sh`.
  3. Copy all the binaries into `<lane>/bin`, then write `manifest.json` as `{host, mini, store, verifier}`.
  4. Run `JOURNEY_STEPS="J0 J1 J2 J3 J4 J5 <STEP>" ./journey.sh manifest.json /run/user/1001/<short>`. The socket path needs a short root.
- **Main-tree comparison:** published artifacts for c1df1f08 exist under `/srv/artifacts`, and `fetch-artifacts` can pull them.
- **File modes:** editing a journey.d script through `cat > file` drops its exec bit, and the hook then fails with exit 126. Check with `git ls-tree`.
- **Objective gate:** it now uses manifests plus a ledger (`scripts/check-objective-proofs.sh proofs --draft`).
  - At next e92cbf10 it was red on about 4200 upstream-drift rows.
  - Give the keeper a ledger proposal for your own rows. Classify rows by the `# … via` lines; P5's classifier is `burst2-a:/tmp/p5ledger.py`.
- **Assurance.NativeAcceptedFixture:** red at next ("no image", seed frame). It does not count against your range.

## P7-ROW-F worker (10-07, second worker) — state at ~270K tokens

- STEP 1 QUEUED: queue/p7-row-f.txt, a10b62ae on e8ba7239 (c3fix). Reviews: OB-ENG approved, DEPUTY-PLATFORM passed. Status: work/platform/P7-STATUS.txt.
- Lane burst2-b:/srv/lanes/p7-row-f (scripts: build-host.sh, run-send.sh TAG [PLANT], run-call.sh TAG; BIN=jbin2 = READY 33fea1fe rust + lane host/consent).
  Plant lane /srv/lanes/p7-plant (check removed + sorry; NEVER commit).
- STEP 2 APPROVED by OB-ENG (abfb6abb71f0a4311) with the SENDER OBJECT's frame as authority. Its conditions:
  (1) delivery_deciders gains a CancelsMessage disjunct, and lawful_fifo is restated with withdraw. Both are explicit statement changes in the commit, with no wildcard.
  (2) The slot codec goes to v3, and v2 refuses.
  (3) A theorem: a cancel's refunds = message.postage + the sum of the queued (pipelined) postage.
  (4) P7 takes cv 01a113fe-13ca (retire decided delivery slots) and -140a (deliverMessage checks slot.activity = its inbox cell). OB-ENG keeps -1351 and -1390.
  (5) Ack at yield, effect at commit. A journey row where the message is delivered BEFORE the cancel commits shows a no-op that refunds nothing.
- Design being built:
  - Frame Plans `stop {slot}` and `cancel {slot}`, answered `acked {slot}`. framePlans gains stop and cancel; frameResponses gains acked. deliveredPlans stays ["call"], and runMessage refuses controls too.
  - Journal.controls are applied AFTER all the turn's sends (documented).
  - stop: on an open slot, refunds the pipelined sends and sets watched := false; the message is still delivered, and deliverMessage RETIRES an unwatched slot instead of writing its decision. On a decided slot it retires the slot (that closes -13ca). A retired slot is a no-op.
  - cancel: on an open slot whose message is queued, it withdraws (Inbox.Step.withdraw), refunds postage plus pipelined sends from the inbox purse, and decides `Decision.cancelled` (or retires the slot if unwatched). On a decided or retired slot it is a no-op.
  - Authority for both: the inbox at slot.activity has sender = the cancelling frame's object, else a named refusal.
  - holdSlot refuses an unwatched slot (notPipelinable).

### STEP 2 implementation state (P7-ROW-F second worker, stopping at ~345K tokens; a fresh worker should continue)
WIP branch: lane/p7-row-f-step2 on the shared remote (on top of a10b62ae). Its commit message says WIP / not queued.
DONE in the WIP (lean-ask clean per file; the closure build result is in logs/build-host.log):
- Kernel/AnswerSlot.lean: `Decision.cancelled` (kernel-only); `Slot.watched : Bool` (last field); frame v3 with a `v2_refuses`
  theorem (`decide +kernel` handles toUTF8); `stopWaiting`, `cancelDelivery` plus `_spec` theorems and samples.
- Kernel/Inbox.lean: `extract`/`extract_spec`, `Inbox.withdraw`, `Step.withdraw`, `withdraw_step`, and `Step.keeps` extended.
  `lawful_fifo` is RESTATED through `FifoAccount` (sublist + perm-with-withdrawn + head). `reorder_unlawful` is RESTATED: it used to be
  ¬Lawful, which is now false (withdraw-then-push is lawful); it is now "no account with withdrawn = [] reorders". `sample_withdraw`.
- Downstream one-liners: ObjectiveActivity (openSlot gets `true`; `outcomeOfDecision .cancelled => .broken`),
  ObjectiveCall openSlot `true`, Host decisionJson/slotJson (cancelled, watched).
TODO (designed; I read the code for every item):
1. ObjectiveCall:
   - framePlans gains stop and cancel; frameResponses gains acked; update loadMethod's error text.
   - `ControlKind`/`Control {sender, kind, slot}`; `Yield.control`; decodeYield `stop {slot}` / `cancel {slot}`;
     `ackedData id = acked {slot}`.
   - `Journal.controls` as the LAST field. Fix the positional `⟨…⟩` in Journal.start and in exec `.enter`.
   - The exec branch mirrors `.send`.
   - New refusals: notControllable(slot), notSender(slot, sender), slotInbox(slot, reason).
   - holdSlot refuses unwatched slots (notPipelinable).
   - Mail gains `closed : List Closed` (name, clean, decided : Option Slot (cancelled) | none = retire) and
     `refunds : List (purse × payer × amount)`. Every positional Mail ⟨…⟩ needs the two new fields (Mail.empty, Mail.send, seedMail in ObjectiveSend).
   - `controlSlot` (gone | decided | held open; checks mail.closed, then mail.slots, then the snapshot; isRetired → gone; missing → notControllable).
   - `controlInbox` (a held inbox whose cell = slot.activity, else readInbox at that cell → holdInbox, and check the cell matches, else slotInbox).
   - `Mail.control`. Authority: held inbox.sender = control.sender, else notSender.
     - stop on open: queued refunded, slot {queued := [], watched := false}.
     - stop on decided: closed += retire.
     - cancel on open: withdraw (missing → slotInbox); closed += (watched ? some cancelled : none);
       refunds += `cancelRefunds purse message held.now.queued`.
     - cancel on decided, or gone: no-op.
   - `postControls` runs AFTER postMail. Invocation: `sent/sentExact` (postMail) and `mail/mailExact` (postControls).
     invokeBatch adds `refundTransfers` (purse → payer, zero and self dropped).
   - Mail.posts adds the closed posts (slotPost or slotRetire). Restate `Mail.posts_shape` with a retired-image alternative
     (its consumers are ObjectiveCheckpointInvariant :710 and :760).
   - Theorem (3): `cancelRefunds_escrow` (sum = postage + Σ queued postage), plus the control-level statement.
2. ObjectiveSend:
   - runMessage refuses non-empty controls.
   - deliverMessage checks slot.activity = Inbox.cell (sender, target), else `replySlot "not this inbox's"` (cv -140a).
   - An unwatched slot posts `slotRetire` instead of the decided slot (cv -13ca, with stop on a decided slot).
   - Fix seedExact and the retention theorems: postMail_credits / Invocation.escrows_every_send now use `sentExact`;
     Invocation.retention_cells_have_payer covers closed posts.
3. ObjectiveCallReference: FrameResponse gains the acked case; the exec_run_reference proof gains a branch mirroring send.
   Check exec_invariant and active_frame_view_stability in ObjectiveCall the same way.
4. ObjectiveCheckpointInvariant:
   - New `AdmittedTurn.CancelsMessage` (invoke arm: some control is a cancel). delivery_deciders concludes
     `DeliversMessage ∨ CancelsMessage` (OB-ENG condition 1, an explicit statement change).
   - Sends invoke arm: `outbox ≠ [] ∨ controls ≠ []`.
   - invocation_mail_nil / invocation_decides_nothing get `controls = []` / no-cancel premises. No wildcards.
5. Journey (send journey):
   - Package methods `cancelOf(view, n)` / `stopOf(view, n)`, with Plan `sum PlanC: cancel: Slot` / `stop: Slot` and
     response `sum Acked: acked: Slot`.
   - Rows:
     - S10 cancel-queued: FIFO of the others kept, refund = PRICE, slot decided cancelled; delivering it is then refused.
     - S11 the pole: delivered before the cancel commits → no-op, refund 0 (OB-ENG condition 5).
     - S12 stop: the pipelined send is refunded, the message is still delivered, and the slot is retired at delivery; a stop on a decided slot retires it.
     - S13: another object's cancel → notSender; an unknown slot → notControllable; chase onto a stopped slot → notPipelinable.
   - Plants for each.
6. Commit message: state that slot v3 refuses v2, that lawful_fifo and reorder_unlawful are restated, the delivery_deciders statement
   change, and the frame Plan/response label growth (methods declaring the new labels). Re-genesis: slots are a v3 frame.

## STEP 2 — QUEUED (P7b-ROW-F, 10-07 ~12:00Z)
queue/p7-row-f-step2.txt, adbbdfb1..ad766d3f. OB-ENG APPROVED, DEPUTY-PLATFORM PASSED. Evidence and plants: see P7-STATUS.txt.
Lane burst2-b:/srv/lanes/p7-row-f is warm at ad766d3f.
- build3.sh = full closure build; build2.sh = narrow closure build.
- jbin2 holds the lane Host plus the 33fea1fe rust binaries (native rust is unchanged up to adbbdfb1).
- Plant tree: /srv/lanes/p7-plant/src2 (planted; NEVER commit).
Box lesson: never `pkill -f` from inside an ssh command line. It matched its own ssh and dropped the session.

## STEP 3 — bounded prepaid continuation allowance (NOT STARTED; written by P7b at ~350K tokens)
DEPUTY-PLATFORM's spec (10-07):
- A delivered method may send only if its message carried an allowance, with bounded fan-out and depth.
- Conservation across forward, cancel and refund must be ONE theorem over the real ledger.
- notDeliverable relaxes ONLY for messages carrying a sufficient allowance.
- Function first: one journey row where a delivered method's onward send succeeds out of its allowance, one where it exceeds the allowance and is refused by name, and a plant.
- OB-ENG reviews the kernel hunks.

Where it plugs in (READ while doing step 2, at ad766d3f):
- ObjectiveCall.deliverable / Deliverable.callsOnly (deliveredPlans = ["call"]): the send-time refusal to relax, conditioned on the message's allowance.
- Inbox.Message has (id, sender, method, args, envelope, postage, refund) and Inbox.messageStream encodes them. An allowance field means the message codec grows; INBOX frame v1 -> v2 must refuse v1, as AnswerSlot did with v2_refuses.
- ObjectiveSend.runMessage refuses `journal.outbox` non-empty (the backstop). With an allowance, postMail the delivered call tree's outbox paid from the allowance, held in the popped inbox purse: the delivery's own escrow, so deliveryBatch debits only that purse (debits_only_purse must stay true).
- Depth: a message needs a depth counter (bound like Inbox.bound). Fan-out: the length of the outbox per delivery is <= the bound.
- Conservation candidates:
  - MessageDelivery.conserves (Postings.conserves).
  - The per-message escrow equation: postage + allowance = fee + Σ onward postage + refunds. Prove it as a sum over deliveryBatch, analogous to cancelRefunds_escrow.
- A cancel must refund postage + allowance: cancelRefunds currently refunds `postage` only. Extend Refund (or cancelRefunds) and restate cancelRefunds_escrow / control_cancel_withdraws.
- Journey: native/resource-client/objective-send-native-journey.py (S1-S13 now) and world/send/Sends.obend (bounce = a sending method; relay/relayVia exist). New rows S14+. The Host invoke JSON needs an allowance field (Host/Json invoke parser, plus the mini client if it builds the body; check `cap(...)` in activity_world).

## STEP 3: QUEUED (P7c-ROW-F, 10-07 ~11:30Z)
- Queue file: queue/p7-row-f-step3.txt, range b57ef817..4407d9f9, branch lane/p7-row-f-step3. Bundle and logs: hbox bundles/p7-row-f-step3{.bundle,-logs.tgz}.
- Reviews: OB-ENG (ae08d68a5af5a4612, renewed id) APPROVED. DEPUTY-PLATFORM informed.
- Design: send-yield `allowance?`, capped by the signed InvokeRequest.allowance (COMMAND v9). Inbox.Message.continues relaxes deliveredPlans. ObjectiveSend.continueMessage enforces fanOut 4, continuationDepth 3 and allowanceExceeded, and refunds the remainder via payOut. escrow_conservation is ONE theorem over Operation.posting. onward_bounded and chain_total give the bounds.
- Lane: burst2-b:/srv/lanes/p7-row-f.
  - jbin3 = rebased Host and consent + 33fea1fe rust.
  - build-s3full.sh TAG = full closure build, copied into jbin3.
  - Logs: step3-*, send-final3, call-final3, send-fpl-* (plants), plant-theorem-*.
- Remaining for row F: stable operation ids for retries; deeper pipelining only with recorded dependencies.
- OB-ENG waits for step 3 to land in next, then starts -1351/-1390. TELL IT when it lands.

## ROW F REMAINING (P7c, 10-07, checked against 4407d9f9)
- Refuse sends from delivered methods at the interface: DONE (step 1). Relaxed only by the allowance (step 3).
- STOP-WAITING separate from CANCEL-IF-QUEUED: DONE (step 2).
- Conservation across forward/cancel/refund, and bounded fan-out and depth: DONE (step 3: escrow_conservation, onward_bounded, chain_total).
- Timeouts don't break never-expiring slots: DONE by construction (READ). AnswerSlot.expire refuses every delivery slot (`.delivery _ => .error .deliveryDecides`, AnswerSlot.lean ~206), and delivery slots carry no deadline semantics. Still OPEN: a named theorem `expire_delivery_refused`, a small Lean-only addition. No timeout feature exists for sends; if one is added, it must leave delivery slots untouched.
- Stable operation ids for retries: OPEN.
  - Code: Inbox.sendId turn index, with turn = ObjectiveCall.invokeTransaction, which hashes request.nonce (ObjectiveCall.lean ~1767). So a retried invocation (new nonce) mints NEW message ids and duplicate messages; for deliveries, turn = messageTransaction message.id, which is stable.
  - Needs a design: a sender-chosen operation id per send, plus a claim (StableNullifier) that dedupes. That is a genuine design fork (where the id lives: the send yield or the request), not one journey row.
- Deeper pipelining only with recorded dependencies: OPEN, and safe today (READ).
  - Pipelining is one level deep. Mail.send `.slot` needs holdSlot to read an OPEN slot. A pipelined message's own slot is opened only when ObjectiveSend.forward queues it, so a send onto it before then is refused notPipelinable.
  - Allowing more needs the recorded-dependency design: acyclic, a single terminal decision, exactly-once escrow, bounded cascades.
- FIFO by entry into the RESOLVED destination queue: DONE (READ). ObjectiveSend.forward pushes slot.queued in order onto the resolved inbox at the deciding turn (Mail.send `.object`), and Inbox.lawful_fifo covers that inbox. There is no dedicated journey row asserting cross-sender order; S5 forwards a single send.
- Step 3 ended at ~370K tokens (over the 300K line), so no step 4 was taken. The most important OPEN item is stable operation ids; it needs a design decision first.

## STEP 3 EJECTED -> REBASED, NOT YET RE-VERIFIED (P7c, 10-07 11:27Z, stopping at ~385K tokens)
- The keeper ejected 4407d9f9: a COMMAND v9 clash with row-a3 487b54fb (registerDomain).
- Rebased onto next 103c5b35 as e919c5fe (lane/p7-row-f-step3, pushed to the shared remote).
  - Conflict resolved in Kernel/ObjectiveActivityReceiver.lean: COMMAND v10 carries BOTH changes, the docstring lists v10 (allowance) and v9 (registerDomain), and v9 and older refuse.
  - The `authorized` arm keeps registerDomain and invoke's extra field. The commit message says v9 -> v10.
- TODO for a successor (small):
  1. Build e919c5fe in a FRESH lane: mk-lane, then `git fetch burst2-a:/srv/git/minidregg.git lane/p7-row-f-step3`; full `lake build Kernel Host ObjectiveProofs minidregg-host minidregg-client-consent`.
  2. Re-run send S1-S18, call, and the 5 plants with the rust binaries from jbin3 (copy the scripts from /srv/lanes/p7-row-f).
  3. Re-queue queue/p7-row-f-step3.txt with range 103c5b35..e919c5fe and COMMAND v10 in breaks. Message the keeper; tell OB-ENG (ae08d68a5af5a4612) when it is in next.
- WARNING: /srv/lanes/p7-row-f/src is now ALSO used by another agent on branch lane/p7-row-f-opids (created 11:20 from 4407d9f9, rebased to 080549b4, no own commits).
  - My rebase briefly moved that branch; it is restored to 080549b4 and checked out.
  - Do not build or rebase in that tree without asking its owner.

## STEP 3 RE-QUEUED and LANDED; OPIDS QUEUED (P7d, 10-07 ~12:20Z). Row F stops here tonight (root).
- Step 3: re-verified at e919c5fe in burst2-a:/srv/lanes/plat-p7-opids. Full build green; send 153/153; call 57/57; the 5 plants are each red on their own row. Re-queued as 103c5b35..e919c5fe; it LANDED in next as 6b2db1f9. OB-ENG was told and is doing inbox retention on top.
- OPIDS: queue/p7-row-f-opids.txt, fed1e74e..4de329aa, branch lane/p7-row-f-opids (shared remote and hbox bundle). OB-ENG APPROVED.
  - Design: an invoke's Command.nonce IS its op id, so there is no second field. Host JSON $.turn.opId is required. mini takes it from the caller.
  - replay returns Replayed.exact|retry. A retry is answered only after verifyRetry (admission's verifyNative over planOutcome, on retrySnapshot).
  - Theorems: prepare_spent_refused, replay_invoke_recorded, replay_exact, retry_unverified_refused, command_v9_refuses.
  - Journey rows S19 retry, S20 same-op-other-call, S21 forged-retry.
  - Plants: world fresh-op -> S19; Host no-claim (needs a planted consent too) -> S20; Host retry-unverified -> S21; Host replay-exact -> S19 and S21.
- Lane burst2-a:/srv/lanes/plat-p7-opids:
  - build.sh TAG (full closure into jbin); cargo.sh (mini only); run-send.sh TAG [WORLD-PLANT]; run-call.sh TAG (BIN=...).
  - build-plant.sh PLANT (plants Kernel/ObjectiveActivityReceiver.lean via plant.py, builds host and consent into jbin-PLANT, restores the file; never commits).
  - jbin-s3 = step-3 binaries; jbin-op = OPIDS binaries.
- burst2-b:/srv/lanes/p7-row-f is P7c's tree. Do not work there.
- ROW F REMAINING after OPIDS:
  - Deeper pipelining with recorded dependencies: OPEN (safe today; one level, notPipelinable).
  - A named never-expiring-slot theorem (AnswerSlot.expire refuses delivery slots): OPEN, Lean-only, small.
  - A retry's plan shows no `report` (INFERRED: re-deciding at the op's own post-state). If clients need it, the plan could show the recorded result for a recorded txid.
