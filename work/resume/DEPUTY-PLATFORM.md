# DEPUTY-PLATFORM — resume note (wound down on ROOT order, 2026-10-07 ~01:30Z)
Charter: work/DEPUTIES-20261006.md, DEPUTY-PLATFORM section. Briefs: scratchpad
/private/tmp/claude-501/-Users-ember-dev-breadstuffs/ce776c01-2f59-4f57-8177-23008d71bf57/scratchpad/platform/briefs/
(BOX-BLOCK.txt + P1..P4). My read clone: scratchpad/platform/mini (scratchpad/mini belongs to DEPUTY-KERNEL; I moved its HEAD once by
mistake ~00:48Z, root informed). Workers ran on burst2-a lanes /srv/lanes/<item>, slots 2-4; bundles -> hbox:/tank/dregg-build/claude-lanes/bundles/.
Worker outcomes: see "WORKER OUTCOMES" at the bottom (appended as they report).

## Item 1 — fn wire re-pin + M4 + hand parsers
- TARGET fn d420a2b5e2b3db18be134ba5a503160da84a31c3 (READ by me: 211503 octets, BLAKE3 d00558d0…24a5, 1028 vectors, 12 families; fn
  integrate/20261004, integrate/20261006n, lane/consumer-boot carry the identical file). The 6 families Mini pins today (fn 930c67414) are
  byte-identical inside it; no new node kinds. ROOT/fn: PIN d420a2b5, do NOT follow fn dev until fn sends a converged sha.
- The hbox lane fn-wire-repin is STALE (targets 7e542c054, unbuilt): ignore.
- Worker P1-FNWIRE-REPIN (sonnet, agent af9c6fe9f3dcb6449), lane burst2-a /srv/lanes/P1-FNWIRE-REPIN.
- fn AGREEMENTS (via root, 10-07): (Q1) NO direct FNCT on fn's 0600 control socket (not a contract; no Rust pipe). fn adds `--frame` to
  `fn identity` and the consumer verbs (prints the reply frame hex), keeping fn-ncr-cli-after the single copy of the bootstrap-retry logic.
  Mini then calls `fn … --frame` and decodes with the pinned interpreter. (Q2) fn adds grammar node ["sized", width, min, max, <grammar>]
  (width = octets of the length prefix; min/max bound the declared length; content consumed exactly; over/underrun a named refusal),
  extends its round trips, exports fnct.consumer.poll-reply (kind 6); fn lane `lane/fnct-sized`, fn sends the sha. Mini has NO draft of it.
- NEXT: (a) land the re-pin. (b) when fn's sized sha arrives: add `sized` to Compiler/FnWireGrammar (decode/encode) + FnWireRoundTrip
  theorems, re-pin to that sha. (c) when `--frame` lands: M4 = Host calls `fn identity --frame CONTROL`, decodes fnct.store-identity.reply,
  refuses unless grammar digest == pinnedDigest, binds node/schema into FnPollScopePin; then replace Host/FnOutcome.answerLine/ackStatus
  callers (Host/Main ~3180-3420, 4340-5750, 8420-8540) with frame decodes; delete the text parsers. P1 is the veteran for all of it.

## Item 2 — plan-scoped replay (P0)
- Design DONE: work/platform/PLAN-SCOPED-REPLAY-DESIGN.md (opus worker P4, agent af9c1e0b9fff1fdfb). Status: work/platform/P4-STATUS.txt.
- Core: witnesses against a Host-chosen root prove nothing (fake tree); tying the root to the client's chain = whole-log replay. Sound path:
  bind the plan's value-read set R into the signature; executor runs on R only (outside read refuses by name); admission re-checks R
  (footprint stale refuses). A lying Host can only cause a refusal.
- MY RULINGS: F1 sign value reads only, gates on current state + theorem gate_refuse_only over the REAL gate list; F2 no root openings in v1,
  root shown "Host-claimed"; F3 delete expectedTargetRoot; F4 reader-monad port of planner+executor; F5 interval guard (balance >= debit),
  commit must say why that is not a weakening (consented debit exact); F6 worker picks, reasons written; F7 delete op 155 / do not land W06b
  (its frames 228/229 also collide with schema-v2-2's); F8 browser consent = cv 01a113e6.
- P7 (suspected kind-definition WYSIWYG gap in landed code): by READING main the worker found it most likely NOT a defect (definition cell feeds
  only gates + a readGuard; post-state = target pre-state + signed actions). UNCONFIRMED: the scratch-world run is step 0 of Phase B. Not
  reported to root as a defect.
- Phase B order: (0) P7 run, (1) signed R + executor check (P5/P6 red), (2) scoped view + frame lemma (P2-P4), (3) re-genesis notes.
- Store epoch: agreed with DEPUTY-KERNEL (abc2735a4c6715430): neither range waits; whoever lands second rebases and takes the next epoch
  number; both refuse older shapes by name; queue adjacent if close together (one re-genesis).

## Item 3 — journeys: worker P3-JOURNEYS (sonnet, a56cea42ca9c3af63), lane burst2-a /srv/lanes/P3-JOURNEYS
- call/send rows in scripts/pipeline/journey-rows (drivers objective-call/send-native-journey.py, plants as red controls), seats row run,
  JP2 row 10 (join --remote) fixed at its cause (never by editing assertions), runner on burst2-a (burst2 has no runner/artifacts/e2e VM).

## Item 4 — SPK v4 fixture + cv 01a10b3e: worker P2-SPK-FIXTURE (sonnet, ad4b770b732db1296), lane burst2-a /srv/lanes/P2-SPK-FIXTURE
- Source: lane/protocol-night-fixture (3 WIP commits on d94a8817) pulled read-only from hbox into
  scratchpad/platform/bundles/pn-fixture-hbox.bundle. Wire BEGIN(op22->23)/CLAIM(op26->27) restart lookups for v3+v4 (never resubmit) or delete
  dead paths; --restart rows for lost op22/op26 replies; the retryAfter mutation red; squash.

## Item 5 — cv backlog: NOT STARTED (SPK-DISPATCH-FEE 01a0f616, K-SPK-2 01a0f63f, PAY observer blinding 01a0f674, WEB-ENTRANCE, P-AFFORDANCES).

## Cross-deputy: `mini store audit` (DEPUTY-KERNEL request)
- Kernel's worker KN2-STORE-OPEN (afdfcf33f426df0d7) writes the Lean side (full genesis re-check + theorem) and will send the spec (CLI, Host op
  + frame, refusal names, exit codes, base sha) DIRECTLY to DEPUTY-PLATFORM, cc kernel. My lane then adds the subcommand in
  native/resource-client main.rs + the Host/Main audit-arm dispatch. Spec NOT yet received. Kernel warned of heavy Host/Main churn
  (~200 serving-path reads, store v5, epoch bump).

## WORKER OUTCOMES
- P1-FNWIRE-REPIN: DONE, reviewed by the deputy (diff + red logs read). Range 4ef4e808..22afac97 (1 commit). pinned_vectors ⟨12,109,919⟩, 211503 octets,
  digest d00558d0…; build 7311 jobs rc=0; check-fn-wire PASS with fn compare branch; reds: octet flip in fnct.consumer.reply -> RED, digest digit -> pin FAIL.
  Bundle+logs hbox:/tank/dregg-build/claude-lanes/bundles/P1-FNWIRE-REPIN.*. Told to QUEUE. Follow-ons wait on fn (--frame, sized sha).
- P4 step 0 (P7) EXECUTED on main 4ef4e808: SAME-EFFECT, no landed defect (kind revised between consent and admission; identical call bytes
  commit exactly the consented vote under the instance's own descriptor). Regression hook journey.d/jkind-revise-consent.sh (step P7KR),
  commit c93b7fba on lane/P4-PLAN-SCOPED-REPLAY; artifacts work/platform/bundles/p7/; bundle work/platform/bundles/P4-PLAN-SCOPED-REPLAY.bundle
  (deputy mirrored to hbox bundles/). P4 now on (1) signed R + executor check.
- P4 re-scope (deputy ruling): value reads already signed twice (expectedTargetRoot + Request.preStateRoot) = twin. Order: (2) scoped view +
  frame lemma + observe filter, WITH (1b) name the stale cell in the footprintStale refusal ONLY if inside the signer's observe authority
  (else undisclosed; theorem/pole), queued as range 1; then (1a) delete the twin (one ReadSet in the header, codec epoch) as range 2.
- P4 F4 WITHDRAWN -> (2') RULED: the planner decodes the whole authority cell (CredentialAuthorityDomainReceiver.lean:131), so a thin client
  cannot re-run it under an observe filter. Thin consent instead checks the signed header's VALUE fields against observe-filtered served
  target bytes + its draft, displays targetPatch, and theorem thin_consent_is_commit (displayed post-state = committed) carries soundness;
  gates stay admission's. Conditions: deployed root fn as carrier (no identity), every targetPatch input signed (incl. blinding height),
  4 planted faults + skip-root-compare mutation red. ScopedRead.lean kept in -wip for cv 01a113e6. Then (1a) twin deletion.
- P4: Kernel/NativeThinConsent.lean green (thin_display_is_commit, RootBinds premise = deployed-hash collision resistance, inhabited by
  honest_binds). (1a) DROPPED: preStateRoot/height are zeroed by planOf, expectedTargetRoot is the one binding (no twin). Thin consent refuses
  content/append/computeFunding/moneyConsent by name (unsigned inputs); worker files cv THIN-CONSENT-MONEY before queueing.
- fn DELIVERED (via root): lane/fnct-sized@e215cd9d7 (sized node; poll-reply kind 6 exported; malformed is the refusal word) + --frame on
  identity/status/position/ack (fn 3f0309256). Re-pin waits for fn's DEV sha after the integrator regenerates specs/wire-grammar.json (root
  relays). P1 resumed as P1b (lane/P1b-FN-FRAMES on 22afac97): (A) sized arm + round trips, (B) M4 identity --frame + delete FnOutcome
  text parsers for status/position/ack; poll stays text until re-pin. No fn image build on boxes without asking.
- KERNEL: kn2-forcing-2 queued (eefea10c..f42eea9c): deliver/exhaust refuse heapUncovered unless envelope declares extra.heap. Activity
  drivers/SDK/journeys must declare it = cv 01a113f0-5027 (my area, NOT started; no new items in this burst). P3 told: such reds are expected.
- P1b (A) sized: 6ada805a on lane/P1b-FN-FRAMES, reviewed OK (build 7312 rc=0; leftover mutant red). Dormant until fn dev sha re-pin. (B) in progress.
