# LANDED-VERIFY closure, 2026-10-04 (lane S8-HYGIENE)

Verified against GitHub main 6909eaf9 (clone /tank/dregg-build/claude-lanes/s8-hygiene/src on hbox). Standard: `git merge-base --is-ancestor <commit> origin/main` AND a grep/read of the named file, function, theorem or test. Evidence class is READ (source read at 6909eaf9) unless the row says otherwise; nothing here was rebuilt or rerun (no warm Lean base). Commits are those in the task notes plus the substance commits found by tracing the named thing.

## Counts

- 74 tasks tagged `landed-verify`; 65 are minidregg scope (two of them, 01a0f814-b32e and 01a0fb7a-7a2d, carry no repo field but are Mini work), 9 are other projects (cv, phoenix-strip).
- Closed (`cv task done`, note citing commit and evidence): 62
- Kept open, tag `lv-kept-open`, note says what is missing: 3
- Untouched (repo is not minidregg/breadstuffs): 9
- Tag `ember`: none of the 74 carried it; nothing tagged `ember` was touched.
- The `landed-verify` tag itself was left on the tasks (cv tag is additive); closed tasks are terminal, the 3 kept tasks also carry `lv-kept-open`.

## Kept open (3)

- `01a0f52e-76f2-73a2-86fb-b87d3c6cfbe4` MUD lanes 7-16 (tidewrack playable) + SheetLaw regen from the fixed laws
  - commit S5 cited: 8280b8d7 (partial)
  - missing/contradicted: present: deploy/shell/templates/mud/{item,market,org,area}, Assurance/SheetLaw.lean theorem smite_refused (SheetLaw regen done). ABSENT: no jmud* journey in native/resource-client/journey.d, no area/look/go/exits verbs in resource-client/src (grep), no referee/combat/mobs/GM journeys: "MUD lanes 7-16 (tidewrack playable)" is not landed beyond the laws and templates

- `01a0f52e-76fd-756d-90e1-4508ea5d2084` JOIN-SOLANA: the friend-side self-enrollment client + FRIENDS.md section
  - commit S5 cited: 5f1f79db (partial)
  - missing/contradicted: present: native/resource-client/src/join_solana.rs (--solana --wait --renew; PayEnrolMemo encoder), deploy/pay/README.md. ABSENT: deploy/shell/FRIENDS.md has no "enrol yourself"/"joining by yourself" section (git grep -i solana FRIENDS.md: 0 hits) although deploy/pay/README.md:186-187 points readers to it

- `01a0f814-b32e-731b-9b06-d0637e9b4c2e` K-RENOUNCE follow-up: run renounce after rotation and an agent renounce live
  - commit S5 cited: fdd3f61d (partial)
  - missing/contradicted: present: journey.d/jrot.sh renounce() row after rotation (old key refused, current key revokes). ABSENT: the second deliverable, a Hermes/agent row renouncing a grant it was handed without --i-know: no renounce row in j14.sh, hermes.rs or any agent journey (git grep -i renounce)

## Table

| id | title | commit | evidence | result |
|---|---|---|---|---|
| 01a0f52e-76c9 | HERMES-TARIFF: per-route tariff so own-key calls pay only the per-op fee | 97644f8f | Kernel/ProviderRoute.lean (route field, per-route fee schedule); Kernel/ProviderMetering.lean Schedule.perOp : Route -> Nat | closed |
| 01a0f52e-76d3 | K-ROOM 3c: room verbs + birth gate + J7 pole for room capabilities | 3f30a38c | native/resource-client/journey.d/j10c.sh: gate row (notRoomMember), J7 pole (law change keeps grants; birthRefused); Kernel/ResourceBirthController.lean:478 RoomBirthGate.Refusal; shell.rs room new/invite/kick | closed |
| 01a0f52e-76e8 | PLACE 6/7/8: concierge+credit verbs, Hermes-in-a-room, the story verbs | 14f6dd98 8582425f 176792ce | native/grain-runtime/src/concierge.rs + native/resource-client/src/credit.rs, hermes.rs (summon), story.rs; journey.d/j17.sh j14.sh j15.sh; Assurance/StoryLaw.lean:265 theorem sealed_story_scene_monotone | closed |
| 01a0f52e-76f2 | MUD lanes 7-16 (tidewrack playable) + SheetLaw regen from the fixed laws | 8280b8d7 (partial) | present: deploy/shell/templates/mud/{item,market,org,area}, Assurance/SheetLaw.lean theorem smite_refused (SheetLaw regen done). ABSENT: no jmud* journey in native/resource-client/journey.d, no area/look/go/exits verbs in resource-client/src (grep), no referee/combat/mobs/GM journeys: "MUD lanes 7-16 (tidewrack playable)" is not landed beyond the laws and templates | **KEPT** |
| 01a0f52e-76fd | JOIN-SOLANA: the friend-side self-enrollment client + FRIENDS.md section | 5f1f79db (partial) | present: native/resource-client/src/join_solana.rs (--solana --wait --renew; PayEnrolMemo encoder), deploy/pay/README.md. ABSENT: deploy/shell/FRIENDS.md has no "enrol yourself"/"joining by yourself" section (git grep -i solana FRIENDS.md: 0 hits) although deploy/pay/README.md:186-187 points readers to it | **KEPT** |
| 01a0f52e-7783 | COLD-READ: 24 s first signed read after a Store restart | a83df5db | native/resource-client/src/main.rs:368 "hashed once per file identity per ..."; scripts/check-host-cold-start.sh (bb2ea51e); Compiler/Emit.lean demo descriptors noncomputable (f903137c) | closed |
| 01a0f546-51e3 | WELL-BIRTH-GATE: gate births into rooms so strangers cannot list fake realm assets | 3f30a38c e14ea85b | Kernel/RoomBirthGate.lean + Kernel/ResourceBirthController.lean:755 "The room gate first ... notRoomMember"; j10c.sh gate row; j10c header "carl ... refused bearing a cell into lab by name (notRoomMember)" | closed |
| 01a0f5d3-e6d9 | K-DOC-INDEX: link/backlink index as a cached fold, coverage-filtered | 28008e8a | Kernel/LinkIndex.lean; shell.rs:3904,3934 doc-backlinks / doc-links actions; journey.d/j12i-links.sh | closed |
| 01a0f5d4-b7f2 | K-TRANSCLUDE: range transclusion with disclosure at transclusion time | 6402be4b | Compiler/HyperdocumentCell.lean:233 transclusionRecordStream (TransclusionRecord); journey.d/j12t-kernel.sh; shell.rs transclude\|transclusions\|follow | closed |
| 01a0f5d7-d167 | K-DOC-HISTORY: doc history / show --at / diff over the signed log | 76513bf9 | Kernel/DocumentHistory.lean; Kernel/NativeObservationController.lean:1295 atCovered; journey.d/j12h-history.sh | closed |
| 01a0f5d8-4382 | WEB-ENTRANCE: mini web, read-only loopback hypertext over signed reads | aae807c7 | native/resource-client/src/web.rs:3-12 (loopback, 127.0.0.1 only, Host-header guard); journey.d/jweb.sh | closed |
| 01a0f5e5-d817 | P-AFFORDANCES: can NAME — prepare-not-submit each held verb | 88c0ec3d 5f030418 d2b8d1cd | native/resource-client/src/can.rs; Host/DryRun.lean theorems dryRun_commits_nothing (:104), submit_storage_irrelevant (:121), dryReceive_refusal_agrees (:144) (the agreement theorem is named dryReceive_*_agrees, not dryRun_agrees_with_submit); journey.d/j12a.sh | closed |
| 01a0f5e6-b2aa | P-DOC-WRITE: doc pull / doc push @FILE, stale by line | 8af442e5 | native/resource-client/src/workspace.rs:5154 staleAtom comments + shell.rs:3848 test doc_push_and_pull_are_one_client_operation_each; journey.d/j12w.sh | closed |
| 01a0f5ef-d69f | WEB-ENTRANCE: stream tail, at-height and room who routes after k-stream/k-index land | b415da04 | web.rs:483-498 /doc/NAME/history, :488 /at/H/doc/N + /doc/N/diff/H1/H2, :914-954 room members via who view; journey.d/j12h-history.sh jweb.sh | closed |
| 01a0f5fe-30fd | CLOCK-SUBJECT: tick under a dedicated clock subject, not the sponsor's workspace; prune at | 8a69da0f | deploy/clock/mini-clock-tick.service:2-11 dedicated clock subject, /var/lib/mini/clock, C_tick, ephemeral attempts; native/resource-client/src/clock.rs:17 "Attempts are ephemeral" | closed |
| 01a0f605-d8f2 | K-DOC-ORDER: an ordering field for document lines (push inserts by id bisection) | eb44a043 | Kernel/ContentElementTree.lean:8,25 editElement splice/move/remove; workspace.rs:7427 "Inserts are placed by the element tree (K-DOC-ORDER closed)" | closed |
| 01a0f611-ea7b | K-TRANSCLUDE follow-up: wire doc transclude/follow/show into the shell | de327c39 | native/resource-client/src/shell.rs:1383 doc verb arms transclude\|transclusions\|follow; deploy/shell/DOC-VERBS.md | closed |
| 01a0f612-7aa8 | K-DOC-INDEX merge: replace final's fold doc_backlinks with the view; add shell 'doc links' | d9ffd503 | git grep doc_backlinks in native/resource-client/src: 0 hits (fold deleted); shell.rs:1383 "links"\|"backlinks" arms, shell.rs:3904,3934 map to actions doc-backlinks/doc-links | closed |
| 01a0f612-7abd | LinkIndex: transclusion targets under their source document | 0c6d54b5 | Kernel/LinkIndex.lean:627 transclusionKeys_sound, :648 transclusion_backlink_complete | closed |
| 01a0f64e-c637 | MUD-BRAID: final-mud ready for the integrator | d7f6b650 a2ac159b | a2ac159b "Merge final-mud (d7f6b650 ...)" is an ancestor of origin/main; journey.d/jclock.sh; Assurance/SheetLaw.lean; scripts/gen-sheetlaw.py | closed |
| 01a0f64e-c645 | Signed reads see no clock slots: an unguarded clock law locks out observation | 8a69da0f | Kernel/ResourceObservationAdmission.lean:3-5 "the deployment s one clock ... exactly as a resource invocation sees them; read_law_sees_clock" | closed |
| 01a0f65d-f895 | K-DOC-ORDER finish: doc push places inserts by element edit (merge p-doc-write onto the el | ef041cf4 8af442e5 | journey.d/j12w.sh:216 "K-DOC-ORDER: 100 lines inserted at one place", :235 check; workspace.rs:7427 K-DOC-ORDER closed | closed |
| 01a0f65d-f8a3 | Host serve exits on a malformed proposal draft (availability: one bad request stops the se | 4c5c58a3 | Host/RequestRefusal.lean (new); journey.d/j12x.sh; journey.d/jserve.sh (hostile client against the live service) | closed |
| 01a0f65d-f8b0 | Shell verbs for the element tree: doc move / remove / insert --at / transclude --at | de327c39 | shell.rs:1382-1383 doc arms move\|remove\|insert\|transclude; deploy/shell/DOC-VERBS.md | closed |
| 01a0f674-fa35 | PAY-BRAID: final-pay ready for the integrator | 8231f17c ed8fcac7 | "Merge fix: final-pay s PayEnrolReceiver ..." 8231f17c is an ancestor; Kernel/PayEnrolReceiver.lean; journey.d/jpay-e1..e4.sh jpay1..4.sh jpay6.sh; docs/evidence/2026-09-30-hermes-keys/run.sh | closed |
| 01a0f674-fa61 | PAY: drive self-enrollment (ops 117-120) from the observer's tick | 5f1f79db | native/resource-client/src/pay.rs:13,30,50 observer quartet ops 117-120 (plan/assembly/submit/lookup, operator socket only); journey.d/jpay-e3.sh | closed |
| 01a0f682-5a59 | HOST FAIL-STOP: a malformed JSON request kills minidregg-host for every client | 4c5c58a3 10e2cc2b | Host/RequestRefusal.lean; journey.d/jserve.sh (JSERVE hostile client); journey.d/j12x.sh | closed |
| 01a0f699-cd4f | FLEET-COMPAT: Pug's dregg-client-sign journey against a Mini host | a88f2c6a | native/resource-client/src/main.rs:36 mod fleet_sign, :565 "mini fleet-sign join\|send\|transfer\|receipt\|retry"; native/resource-client/fleet-sign-journey.sh; docs/FLEET-SURFACE.md | closed |
| 01a0f69a-f7d1 | DOCUVERSE-BRAID: one branch for the docuverse lanes + the web face on it | 52c56775 b415da04 0c6d54b5 | journey.d/jweb.sh j12h-history.sh j12i-links.sh jdocuverse.sh; Kernel/LinkIndex.lean:648 transclusion_backlink_complete; web.rs history/at/diff routes | closed |
| 01a0f69b-d96c | SPK-APPS: the host side on the new store + a survey of real Sandstorm apps | 24b0870a fe29db5b | docs/evidence/2026-10-01-spk-apps/{survey/apps-all.tsv, survey/v-*, jspk1/, market-qualify.txt} | closed |
| 01a0f69e-4718 | K-PREROTATE: key pre-rotation — a stolen daily key cannot rotate | 8234d225 | Assurance/KeyPreRotationAudit.lean:36,46 accepted_old_key_refused, host_stolen_daily_key_refused; Compiler/CredentialSigningKeyCodec.lean:20 nextKeyDigest; journey.d/jrot.sh | closed |
| 01a0f6ad-8d4a | Shell verbs doc mark / doc unmark (K-MARKS client actions exist; shell not on this tree) | de327c39 | shell.rs:1382 doc arms "mark"\|"unmark"; deploy/shell/DOC-VERBS.md | closed |
| 01a0f6ad-8d6f | K-MARKS x K-FIELDS: reviewer rows via a fields={annotations} grant at merge | 0a00cb27 | journey.d/j12m.sh:7,138 R_ANNOTATE grant with {"fields":["annotations"]}, row r-edits-line1 refused | closed |
| 01a0f6b9-7ae7 | K-NARROW-HIDE: a narrowed view must not carry the cell root; prove independence of uncover | c8bb4c15 | Compiler/StoreHiding.lean:134 narrowed_view_independent_of_uncovered_given_salts, :31 ..._across_writes; Kernel/NativeObservationController.lean:327-335 narrowedFields | closed |
| 01a0f6e0-92be | C1 JOB-LAW: Kernel/Job.lean — the job lifecycle as a Pred law with both poles per edge | 0af0521b | Kernel/Job.lean:588 caller_cannot_forge_truth, :630 bond_slashed_iff_mismatch, :1003 no_double_settle, :1130 settle_requires_match_or_timeout; deploy/shell/templates/job/law.job.json; journey.d/jjob1.sh | closed |
| 01a0f6e3-28d0 | C3 K-JOB-MONEY: job escrow, payout and slash as conservation-checked Book turns | 759ff314 | Kernel/JobMoney.lean:658 escrow_conserved, :709 fund_requires_caller, :742 settle_requires_terminal, :762 no_double_settle, :440 slash_split_sums_to_bond, :460 provider_paid_iff_unchallenged_or_upheld; journey.d/jjob-money.sh | closed |
| 01a0f6e3-3f03 | C14 TAIL-BOUND: a node cannot run more than L heights past its last certified checkpoint | 88b18d26 4caf8c0b | Kernel/TailBound.lean:125 tail_bounded, :158 certified_monotone, :221 checkpoint_restores_progress; journey.d/jtail.sh | closed |
| 01a0f6f0-6a5f | C2 K-RUN-PIN: pinned program context, noun output slot, ABI v3 | 7a7b3881 | Compiler/Evaluator.lean:174 Machine.sampleOf_pinned_of_fields; Compiler/NockProgramCodec.lean:29; journey.d/jnock3p.sh | closed |
| 01a0f6f3-58ad | T1 WORLD-COMPLETE: Turn/World gain spent, allowance, the parent home, the no-cell turns —  | de5e0f55 | Kernel/World.lean:1954 spent_monotone, :1994 charge_le_allowance; Kernel/TurnCensus.lean step_conserves | closed |
| 01a0f6f6-8ef4 | P-DOC-RENDER: doc show renders marks, transclusions, annotations, links, outline; --raw | 6ff106d6 37ffc270 | native/resource-client/src/render/mod.rs (text + html backends, outline); journey.d/j12r.sh, j12r.golden.txt | closed |
| 01a0f70e-4a73 | P-DOC-RENDER follow-up: mini web renders /doc through render::html (delete web.rs's own li | 0a00cb27 | web.rs:838 body.push_str(&rendered.html(name)); web.rs:1088-1104 crate::render::render; git grep view-quotes native/resource-client: 0 hits (loop deleted) | closed |
| 01a0f71e-1251 | E1 K-EVAL: Evaluator structure + Nock instance (EVAL §7 E1) | f6a77427 | Compiler/Evaluator.lean:433 registry_ids_distinct (+ #print axioms pin :659); Theory/Eval.lean | closed |
| 01a0f726-aaab | C-SAT-1: law satisfiability as witness-or-certificate (Pred/Satisfiable.lean) | dced89b7 38073014 | Pred/Satisfiable.lean:429 witness_sound, :808 difference_faithful, certificate_unsat; Pred/SatisfiableTotal.lean:1002 decide_never_unknown | closed |
| 01a0f728-e08a | G-NORM: Patch.normalize + normalize_run/valid/footprint/idem — the diff is the cut-free no | 7305de19 | Theory/StoreNormalize.lean:412 normalize_valid, :423 normalize_run, :524 normalize_idem, :400 normalize_validFrom_iff | closed |
| 01a0f72e-fcb9 | CH-CELL: channel cell codec, schedule, assemble/fanout, trace theorems (Theory/Channel) | 8eedc274 | Theory/Channel/{Cell,Lease,Trace,Audit}.lean; Theory/Channel/Audit.lean:81-88 #assert_axioms fill_is_cell_shaped, Schedule.slot_rate_bounded, Schedule.no_lease_no_cell | closed |
| 01a0f751-cb79 | T3 HOST-REFINES-WORLD: Turn.ofIntent, Represents, deployed_refines_step, trace_represents_ | 19194952 | Kernel/HostRefinesWorld.lean:18-31 deployed_refines_step, host_trace_represents_fold, appendOnly_rewrite_has_no_turn; Kernel/TurnOfIntent.lean | closed |
| 01a0f783-65d6 | CH-EPOCH: EpochRecord + AbsentOpening codecs, ChannelLaw, omission_evident (opening holder | 415d84b8 | Kernel/DomainEpoch.lean:24-26 own_omission_evident, omission_evident, relay_equivocation_transferable, silent_and_dropped_indistinguishable; Kernel/DomainEpochStream.lean; journey.d/jchan-epoch.sh | closed |
| 01a0f791-e9de | T4 input from T3: ROM policy-source births are not turns (decide create-with-image vs appe | adff009d | Kernel/HostRefinesWorld.lean:78 host_submit_is_step, :295 policy_source_birth_is_turn; Kernel/DeployedBridge.lean | closed |
| 01a0f796-17f4 | C1xC3: gate the job law's money columns on the job-money slot; pin Job.law | 6cc2da9c 759ff314 | Kernel/Job.lean:22-23,71 money columns carry authority/operation/job-money slot; Kernel/JobMoney.lean:840-843 receiver pin decide (law = Job.jobLaw p); deploy/shell/templates/job/law.job.json:1888 job-money slot (note: the commit S5 cited, 6cc2da9c, is a client change; the substance is in Job.lean/JobMoney.lean) | closed |
| 01a0f798-7cdd | NC-2: symbolic loop summaries + declared field maxima — cost O(program), B polynomial in d | 06aba852 78db5af1 | Theory/NockCost/Summaries.lean:645-647 pole_forge_symbolic, costSym; Compiler/NockProgramCodec.lean:106 fieldOverMax; Kernel/NockProgramCell/Sample.lean:958 shapeOf | closed |
| 01a0f7c5-1c95 | CH-RELAY-1: mini relay — real ticks, exported assemble/fanout/seal, epoch appends, constan | d967933c | Kernel/DomainEpochExport.lean:14-18 relay_pipeline_is_sealEpoch; Kernel/DomainEpochAudit.lean:178 #assert_axioms; native/resource-client/src/relay.rs (dlopen); native/resource-client/channel-lib/{build.sh,closure.lean,shim.c}; journey.d/jchan-relay.sh | closed |
| 01a0f7c7-6799 | DOCUVERSE onto final: TRANSACTION v5 twice, one QueryView, atCovered as RefusalReason, K-F | 8787e8d3 29b56a6f a561c4b6 | Kernel/ResourceTransaction.lean:243-287 frames 4,5,6,7 refuse decode, current commandFrame 10 (Compiler/NativeProtocolFrames.lean:50); one `inductive QueryView` (Compiler/NativeObservationCodec.lean:26); Kernel/NativeObservationController.lean:1295 atCovered : Except RefusalReason; narrowedFields K-FIELDS | closed |
| 01a0f7e0-78de | C-SAT-2: law-sat Host op, law check, can --any, install-time explain | c32a8414 | Host/LawSat.lean, Host/LawSatWire.lean (session op 150); native/resource-client/src/lawsat.rs (law check, can --any, --allow-unsatisfiable); journey.d/jlawsat.sh | closed |
| 01a0f814-b32e | K-RENOUNCE follow-up: run renounce after rotation and an agent renounce live | fdd3f61d (partial) | present: journey.d/jrot.sh renounce() row after rotation (old key refused, current key revokes). ABSENT: the second deliverable, a Hermes/agent row renouncing a grant it was handed without --i-know: no renounce row in j14.sh, hermes.rs or any agent journey (git grep -i renounce) | **KEPT** |
| 01a0f88a-68b6 | K-ROOM: a non-member can birth a cell into any room (births check room presence, not membe | 3f30a38c | Kernel/ResourceBirthController.lean:755-756 room gate first, notRoomMember; Kernel/RoomBirthGate.lean; j10c.sh gate row: carl (no grant) refused notRoomMember | closed |
| 01a0f8c4-6cd4 | P-STORY x K-FIELD-CLOSURE: story invite must declare player_fields at birth | 176792ce | native/resource-client/src/story.rs:272 player_fields(table), :482 "fields": player_fields(&table) at invite birth; Assurance/StoryLaw.lean | closed |
| 01a0f9e1-50d3 | AUDIT: a kicked member keeps reading, writing and delegating every cell they created in th | a304501a 7ee8dc3a | Kernel/RoomKick.lean:48 kick_revokes_room_born_authority, :63 kick_revokes_born_grant; j10c.sh kick section "a born grant carries the creator s room-grant lineage" | closed |
| 01a0f9e1-50ef | AUDIT: in a paid room, kick does not end a paid window, and a kicked or never-invited subj | 10fd5835 a304501a | native/grain-runtime/src/concierge.rs:17 "A kicked subject holds no standing ..." (refund path); commit 10fd5835 "the concierge refunds what it will not honour"; journey.d/j17.sh kick/concierge refunds (4fefe4c7) | closed |
| 01a0f9e1-c59a | AUDIT: a payment at the posted price is journaled underpaid if the founder raises the pric | 10fd5835 | native/grain-runtime/src/concierge.rs:10,95-97 PRICE_SLACK = 64, memo "room R week W at H", tariff read at H | closed |
| 01a0f9e2-5fde | AUDIT: sealing a room cell ends kick, invite and re-law while members keep writing its cel | 10fd5835 | native/resource-client/src/shell.rs:518-522 sealing a room cell is refused unless --freeze-roster (said out loud); shell.rs:80 law usage lists --freeze-roster | closed |
| 01a0f9f9-4e52 | Timers race friends: a tick/certify between observe and submit refuses stale-root; mini do | 349c1e58 f55a7fb9 04661f19 | native/resource-client/src/workspace.rs:2992-3047 crate::replan::replan under --replan-max; journey-timers/{hostile,ticker}.sh | closed |
| 01a0fa13-a3ac | SPK-WS-PROXY: the loopback TLS browser proxy splices a WebSocket after 101 | 3a159154 b106ae15 6ffe5a6f | native/spk-host/src/bin/spk-browser-proxy.rs:207,314,400 upgrade splice, drain deadline; deploy/spk-host/BROWSER-WEBSOCKETS.md; docs/evidence/2026-10-02-spk-browser-tls/ | closed |
| 01a0fb7a-7a2d | Member docuverse search and actionable navigation over authorized current collections | 46cb353b 79999cc7 | native/resource-client/src/doc_search.rs; shell.rs:91 "doc search QUERY NAME[,NAME...]"; web.rs hits | closed |
| 01a104fe-95c2 | SDK Linux control on hbox (mini-sdk + discord-entrance lib/mirror/endpoint rows) | d19bb7bf | commit message cites hbox Linux logs/linux-mini-sdk-4.log (29 unit + 3 golden) and repeat100 100/100; SWARM-LEDGER 05:25 line: discord-entrance lib 18/18, mirror 5/5, endpoint 6/6 pass on Linux (READ ledger, not re-run) | closed |
| 01a10505-9a79 | Compiler/DurableReceiverIO.lean:1091 unsolved goals on a fresh clone of c8fdd000 (Mac darw | aa929eeb | commit message: original fails "unsolved goals" (logs/dri-orig.log), fixed file passes `lake env lean` (logs/dri-check.log); Compiler/DurableReceiverIO.lean judge_tail present. Not rebuilt by this lane (no warm base) | closed |

## Not touched: other projects (9)

| id | repo | title |
|---|---|---|
| 019f6e94-5c35 | cv | sim: synthetic fleet generator + replay-cost bench |
| 019f6e94-5c52 | phoenix-strip | sim: dogfood-loop scenarios — refute path, rubber-stamp, crashed worker, N-task fleet |
| 019f6e94-5c6a | cv | honesty fixes: receipts overclaim wording, Done-attestation carve-out label, trust-model (solo-fleet |
| 019f6e98-0e41 | phoenix-strip | G9 followup: resume argv may persist secrets — allowlisted launch manifest instead of raw argv repla |
| 019f6eef-dc51 | cv | provenance: freshness on the debt/landed surface (verified_at + age on every landed/suspect row; Unk |
| 019f6ef7-0455 | cv | excellence: TOFU per-worker credentials — close pin_identity (bind token on first use; store rejects |
| 019f6ef7-0469 | cv | excellence: verifiable Done — cv task done --check-cmd/--check-http/--check-file that cv RUNS and re |
| 019f6ef7-047c | cv | excellence: harden saw_change past echo — require opened-changed-file / diff-in-context / ran-repo-t |
| 019f6f36-7715 | cv | close sesh ls --json gaps (#15): sizeBytes, git.branch, title fallback, freshness doc |

Notes on the closed rows
- Rows citing a client/journey commit whose subject is not the task's subject (for example c2d7ba89 'tariff usage names the open field' cited for the four AUDIT tasks) were closed on the substance commit named in the evidence column, not on the cited one: 10fd5835, a304501a, 7ee8dc3a, f666901e, 4fefe4c7 are ancestors of origin/main (checked) and carry the fixes. The AUDIT rows name the code that implements each fix (RoomKick theorems, concierge PRICE_SLACK/refund, --freeze-roster).
- 01a0f796-17f4: the commit S5 cited (6cc2da9c) is a client change; the substance is Kernel/Job.lean (money slot) and Kernel/JobMoney.lean (jobLaw pin).
- 01a104fe-95c2 and 01a10505-9a79 were closed on the commit message's own named logs plus the ledger (05:25 line) and a source read; they were not rerun.
- No row was closed on a journey transcript alone: the named file, function, theorem or journey step exists on main in every closed row.

## Swarm-tagged LIVE tasks checked against `git log c8fdd000..origin/main` (81 commits)

Closed with code-plus-log evidence (not subject only):
- 01a1056c-c498 C backend: port perform/done/yielded/sharedEffect/resume -> done. runtime.c implements them; evidence/differential-03-cohort.log `TOTAL pass=300 fail=0` (+ stress/fixtures, 340/340), mutation controls red. Landed 041a0207/6909eaf9.
- 01a10505-4708 .variant arm in the preview template; Sums.obend into the cohort -> done. No preview template exists any more; Host/ObjectiveBendPreview.lean:35 has the arm; preview-cohort.json row SumsTotal (expected 22) is in the cohort; the differential log shows `SumsTotal typing=accepted` and PASS rows. check-preview itself was NOT rerun (needs a built tree).

Candidates, NOT closed (evidence is a subject, a log from another lane, or only part of the work):
- 01a10500-6f2f front-end checks in gates: implemented in this lane (fa993a90, unlanded). Open until the four Lean rows run green on a warm base.
- 01a10564-84a1 Sums.total refused by the type checker: differential log says `typing=accepted` for SumsTotal; confirm with check-preview on a warm base, then close.
- 01a10510-6e02 grain-runtime stale paused_parent test: fix 56920e9e exists only in the followups lane clone, not on main.
- 01a10510-6e33 discord-entrance durable_restart race: fix d73303ef exists only in the followups lane clone, not on main.
- 01a104fd-9015 arm private-rooms refusal tests: main (391311a0) arms 11 of the 13 names in the rooms STATUS; two remain (filed as 01a105b3-f288).
- 01a104fe-94a5 SDK pins intent bytes to the Lean contract codec: precondition met (Kernel/Contracts/{Identities,Cuts,Snapshot,Futures} landed in f5c7cfac, 48895f77, ba75b245, 17a6489c) but native/mini-sdk/src/contracts.rs still carries `TODO(W2.A)` and its own encoder: work not done.
- 01a10500-6eef re-emit captures/pins after the parser change: examples were regenerated and are checked by check-objective-examples.sh (4c1eee3d, 370e972d); `PIN_PARSER`/objective-source-package.ts no longer exist in the tree, so the task text is stale. Needs a decision by the task owner on what remains.
- 01a104fd-9132 execution_source_semantics into Kernel/ObjectiveBendPreparedOutput: not done (git grep over Kernel/ finds nothing; the theorem lives in Theory/ObjectiveBendDemandDataSoundness.lean).
- 01a10501-825a, 01a10503-6c57, 01a10501-8293: Theory/CertF.lean, Kernel/AgreementEvidenceRegime.lean, Kernel/GenericSimplexReconfig.lean do not exist on main; not done.
- All other swarm-tagged LIVE tasks (native, agreement, spk, tenancy, rooms schema, traffic, mine, backends) have no matching commit in the 81 since c8fdd000 beyond what is listed above.

