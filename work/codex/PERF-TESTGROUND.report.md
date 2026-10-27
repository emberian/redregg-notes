
## WORKLOG
- 2026-10-27 START: PERF-TESTGROUND. Read WORK-RULES, TESTGROUND report, DESIGN-TESTGROUND, CHARTER, transport.js, nd.js, Web/Sim and Command/Machine. Own detached hbox worktree ~/nd-land/perf-testground at 8fe58cbf. No builds started. Disk 58G available on NVMe.
- 2026-10-27 READ: WASM exports are synchronous on the browser main thread. Web.Sim.Member already persists Command.Follow, and followOf saves fs' after each answer; investigating repeated work within each event rather than assuming replay from genesis.
- 2026-10-27 ASK: Worker transport makes kernel methods asynchronous. pub/sign/forge currently receive page-held seeds. May these existing calls send their bytes to the same-origin dedicated worker, keeping seed generation/storage/rotation unchanged? This is a custody boundary change under the worker contract. Alternative is a separate main-thread WASM instance solely for existing custody calls (extra initialization and memory, but seeds stay on the main thread). Continuing measurement and non-custody worker transport meanwhile.
- 2026-10-27 ASK: Brief explicitly asks to republish Pages (Ember: publish whenever), but worker contract lists publishing as a pause item. Please confirm publication for the landed performance changes; preparing and checking artifacts independently.

- 2026-10-27 MEASURED baseline, Chromium on hbox (shared x86 build host; NOT an M2 result), kernel source 8fe58cbf: 14-command document correctness green. UI demo 9110 ms and one 9194 ms main-thread long task. Direct command timings below separate writer kernel, follower kernel (planning + auditing), WASM byte-copy boundary, and other kernel calls. Full report/screenshot at hbox:~/nd-land/perf-testground/.perf/baseline.{json,png}. Rendering isolation and invoke CPU profile next.

| command | wall ms | writer ms | follow ms | boundary ms | other kernel ms |
|---|---:|---:|---:|---:|---:|
| install | 565.7 | 60.0 | 417.4 | 1.1 | 16.0 |
| install | 326.8 | 46.5 | 257.4 | 0.7 | 10.0 |
| install | 159.0 | 33.0 | 109.4 | 0.7 | 8.4 |
| install | 569.7 | 74.2 | 476.7 | 0.9 | 7.7 |
| create | 519.0 | 67.8 | 441.9 | 0.2 | 7.8 |
| grant | 42.6 | 23.7 | 9.9 | 0.4 | 7.3 |
| invoke 2 | 904.6 | 125.2 | 761.5 | 1.0 | 12.1 |
| invoke 3 | 752.1 | 100.0 | 643.6 | 0.2 | 6.6 |
| invoke 9 | 1136.0 | 173.3 | 954.8 | 0.3 | 6.4 |
| read | 47.5 | 9.0 | 36.0 | 0.0 | 2.3 |
| retire | 33.3 | 19.7 | 6.2 | 0.2 | 6.6 |
| invoke 5 | 902.8 | 96.3 | 795.7 | 0.3 | 9.5 |
| read | 46.0 | 9.1 | 34.4 | 0.1 | 2.1 |
| invoke 9 | 211.3 | 9.2 | 199.5 | 0.1 | 2.0 |

- 2026-10-27 READ/INFERRED: followOf persists fs' after every Host.Follow.answer, and Command.absorbPage calls absorb from fs.world. No genesis refold on ordinary commands. Do not introduce a second audit implementation. Boundary copying in this baseline is <2 ms per command; it cannot explain the slow invokes. Worker code drafted; no custody calls added pending ASK.
- 2026-10-27 UI-OVERHAUL coordination: UI extracted compositor.js and toolkit.js, changing the top of testground.js. UI will own demo progress/cancel and yielding between commands, renderLog batching/incremental DOM, and inspector refresh lifecycle. Please own async kernel/bootstrap/secondWorld integration in testground.js and teach.js; these will need a rebase. Keep the existing openWindow({id,title,body,...}) API and ctx.$. Do not change compositor/toolkit. UI has not changed nd.js, transport.js or Web/Sim. Source hbox:~/nd-land/ui-overhaul; reports UI-OVERHAUL.report.md. Please append any required interface guidance there. Existing async runIn is the boundary UI will use for command progress.
- 2026-10-27 UI reply: Accepted Promise-valued K methods; UI leaves await propagation/bootstrap to PERF. Added ctx.readIn(m, argv) in teach context, serialized through the same inMember queue as runIn but without printing/refresh recursion. Inspector, relation list and Lesson state reads now use ctx.readIn. A running demo uses withActivity/job.run around each runIn and yields before/after each command; cancellation stops future commands without aborting an in-flight signed call. Current browser runs waiting on build slots; first compositor push follows the actual check result.
- 2026-10-27 UI clarification: TESTGROUND.report.md contains an older instruction for UI to own bootstrap/secondWorld, while your newer reply in UI-OVERHAUL.report.md says PERF owns both plus await propagation. I read your live worktree and see those edits already in your testground.js/teach.js. Proceed with your integration as the live owner; UI will not duplicate it. Inspector reads in my four prepared commits all use ctx.readIn now. Gate just acquired slot 6 after ~12 minutes queued; compositor check next. Prepared UI tip 81430b03, first compositor 97711b00; not pushed until checks pass.

- 2026-10-27 MEASURED CPU profile: Chromium document trace, 6299 ms sampled. Disjoint categories: package decoding 4088 ms (64.9%), hashing 458 ms (7.3%), typechecking 133 ms (2.1%), evaluator 99 ms (1.6%), other 1521 ms. Follower audit stack 1247 ms; other follower work/planning 4358 ms; writer 316 ms. Main culprit is repeated package decoding, not evaluator ticks. Trace hbox:.perf/document.cpuprofile; symbol-bearing WASM was linked from the same object files for profiling.
- 2026-10-27 MEASURED worker smoke: bytes-only requests agree with direct kernel for expressions, types, refusal, package text, missing member, and attempt action; closing the worker rejects a queued request. No custody operations used. Node gate: lies 7/7, honest 5/5, axes 6/6 (document included), tutorial 46 commands green. Hosted harness caught an await inside an unmarked helper; fixed and gate retry queued.
- 2026-10-27 FOUND/FIXED in build recipe: Emscripten 6.0.9 excludes wasmBinary from its default INCOMING_MODULE_JS_API. The old glue ignored the page's supplied hashed bytes and fetched kernel.wasm again. Added wasmBinary explicitly, with web,worker,node targets. This is needed for both hash provenance and worker initialization. Browser check will refuse secondary fetches.
- 2026-10-27 WORKLOG: await propagation prepared in testground.js/teach.js after UI lane yielded those changes to PERF; UI still owns compositor, lifecycle, frame batching and demo controls. No commit landed yet. ROOT custody/publication answers remain pending.
- 2026-10-27 UI LANDED af3248d8 compositor on origin/main; rebase now. Three prepared commits follow after full-page browser retry: 6647d695 controls, ea6ef5e0 lifecycle, 4a9a99c9 progress/queue. Final UI tree at hbox:~/nd-land/ui-overhaul. The gate is green; compositor browser green (60 FPS, stable listeners after 50 cycles). Preserve ctx.readIn serialization and job.run wrapper when merging await propagation.

- 2026-10-27 MEASURED non-custody worker experiment: document 14/14 correct, 6022 ms total, first result 471 ms; 394 animation frames, maximum interval 16.8 ms, zero main-thread long tasks. Ordinary writes 32.6–51.3 ms (10 samples). Only one WASM fetch; later fetches were blocked by the harness, proving the supplied hashed bytes were used. Custody in this experiment stays in an unchanged direct WASM instance; no seeds sent to worker while ASK is pending. This proves responsiveness, not the <1 s target and not the final worker custody path. Details hbox:.perf/worker-document.json.

| command | wall ms | writer ms | follow ms | WASM boundary ms | worker transit ms | paint wait ms |
|---|---:|---:|---:|---:|---:|---:|
| install | 470.5 | 57.0 | 357.8 | 1.1 | 4.2 | 10.7 |
| install | 283.1 | 36.3 | 211.5 | 0.9 | 5.1 | 10.9 |
| install | 166.5 | 32.5 | 99.2 | 0.6 | 7.4 | 10.1 |
| install | 517.4 | 61.1 | 425.1 | 1.4 | 13.0 | 3.5 |
| create | 432.4 | 60.8 | 349.3 | 0.5 | 4.1 | 10.6 |
| grant | 33.2 | 16.5 | 5.8 | 0.1 | 2.2 | 2.8 |
| invoke | 751.3 | 102.2 | 629.9 | 0.3 | 3.2 | 4.6 |
| invoke | 818.0 | 130.1 | 652.9 | 0.1 | 19.0 | 4.4 |
| invoke | 1149.1 | 108.2 | 1012.0 | 0.2 | 10.8 | 7.9 |
| read | 65.8 | 8.6 | 35.3 | 0.0 | 1.9 | 17.6 |
| retire | 50.1 | 20.5 | 7.0 | 0.1 | 10.6 | 2.7 |
| invoke | 949.8 | 92.8 | 828.4 | 0.4 | 9.0 | 11.7 |
| read | 81.9 | 9.8 | 50.7 | 0.3 | 8.6 | 10.4 |
| invoke | 216.4 | 11.6 | 192.7 | 0.2 | 5.1 | 3.7 |

- 2026-10-27 WORKLOG: local-only prepared commit 630e001a rebased over UI compositor af3248d8. Not pushed: default worker does not yet expose pub/sign/forge pending custody ASK. New uncommitted fixes attach the kernel's lied bit to each host reply atomically and terminate discarded secondary-World workers. UI further landings still to rebase. Gate retry uses an owned warm cache .perf/wasm, under the shared build slot; no changes to the shared cache in future runs.
- 2026-10-27 NEXT algorithm proposal: a bounded exact-byte cache of successful package decodes with each entry carrying the Lean proof decodePackage bytes = .ok package. A PackageDecoder returns a subtype certifying equality to the ordinary decoder; all such decoder functions are propositionally equal, so a cached program can be proved equal to the deployed program without weakening any typecheck, live-hole check, law, receipt, pin or audit. Populate from newly absorbed package creates, not a World scan. Draft proof hbox:.perf/DecodeCache.lean (scoped elaboration queued). Program-loader parameterization and wiring are not yet implemented; land worker first as brief requests.
- 2026-10-27 UI integration detail: runOne now captures its World and suppresses rendering when that World changes (both after command await and after paint yield). inMember rejects queued reads/commands from a replaced World. Please ensure async newWorld/genesis waits for active member queues or retires the old kernel worker; otherwise an nd continuation already in flight could resume against a reset shared kernel. UI's demo reset guard prevents resetting during a demo, but typed commands also need this boundary. Full UI retry caught a new background inspector stacking above progress; fixed, retesting.

- 2026-10-27 MEASURED single invoke: first document invoke (method 2) took 1020 ms under Chromium CPU sampling on hbox. Sample categories: package decode 717 ms, hash 92 ms, typecheck 18 ms, evaluator 16 ms, other 246 ms (sampling includes profiler boundary overhead). Confirms the whole-demo attribution. Files .perf/invoke.cpuprofile and .perf/invoke-summary.json.
- 2026-10-27 GREEN: testground/build/gate.sh with owned cache .perf/wasm passed lies 7, honest 5, axes 6, tutorial 46 commands, hosted basic/document/door. New testground/worker-check.mjs passes all 11 checks, including direct-kernel byte agreement, closed-worker rejection, invalid-WASM rejection, and exactly one WASM fetch. The publish-check script passed its four local checks through a test-only main-thread custody adapter; this is NOT a full-worker custody test. Screenshot /Users/ember/dev/redregg/work/promo/perf-testground-pending-custody.png. No public site changed.
- 2026-10-27 GREEN prototype: .perf/DecodeCache.lean and .perf/Program-cache.lean elaborate with no errors. Program-cache contains loader parameterization and theorem program_decoder_eq: for any certified decoder, the whole Lang.program is equal to its ordinary decoder instance. Existing source files/theorem statements are untouched. Before using this: split cache definitions/proofs into proper modules, have a second reader review the new statements per CHARTER, wire the cache to newly absorbed package creates in Web.Sim.Member/Ground, measure, build the changed closure and dependents. The cache is not active and no speedup from it is claimed.
- 2026-10-27 WORKLOG current: hbox ~/nd-land/perf-testground, local commits 630e001a and 2be8d093 above UI compositor af3248d8. CLIENT-59 records the worker transport decision. Tracked tree clean; .perf is private scratch. No commits pushed. Latest fetched main 0ef740b1; rebase after ROOT answers and UI finishes its remaining landings. API adaptation and worker protocol are complete except exposing pub/sign/forge pending custody authorization; therefore the default page is NOT ready to land. UI progress/cancel/lifecycle patches remain to integrate and validate. newWorld now clears controls and awaits member queues before resetting the shared kernel, then closes extra-World workers. All measurements are hbox Chromium; M2 targets remain unmeasured.
- 2026-10-27 BLOCKED: ROOT custody decision is pending: allow existing pub/sign/forge byte calls in the same-origin worker, or retain a separate direct WASM instance for custody. The contract explicitly pauses custody changes.
- 2026-10-27 BLOCKED: Pages publication answer is pending under the contract’s outward-facing pause. Nothing was published or pushed.
- 2026-10-27 STATUS: Worker transport and gate checks pass; the responsiveness experiment has no long tasks. Document throughput remains about 6 s on hbox. Cache integration, final UI checks, M2 measurements and landings remain. Not DONE.
- 2026-10-27 UI all four landings now on origin/main, latest fbe2dd82. Please rebase through fbe2dd82, not just compositor. ctx.readIn uses inMember; all inspector/relation/Lesson reads use it. withActivity/job.run implements progress and cooperative cancellation; runOne checks World identity before and after paint yield. toolkit.listen + disposeEvents explicitly clean node listeners when the compositor closes/replaces a window; preserve these imports and uses in await propagation. Main UI browser check GREEN (512 ms interactive, ~60 FPS drag, 44→44 listeners after 50 terminal cycles); page gate and local publish-check GREEN. UI publication still awaiting ROOT; refresh of landed-tree artifact underway.
# How a lane builds (real 2026-10-27, Ember): reason across the whole change; build once

Ember: "too many parallel lanes fighting for the CPUs and all redoing the same proof work constantly. It's something systematic about the way we're using lake and iterating one statement at a time instead of iterating across the whole system and using mental simulation and reasoning to develop without wasteful rerun loops."

Measured: 50 private copies of the build (27 under ~/nd-land, 20 under /tank wt), each seeded from a different stale tree; every rebase onto a moved main rebuilds everything downstream of the change, in every lane, again; the disk at 95%.

THE RULE, effective now, for every lane (Claude, GLM, Astra):

1. **Reason first, build once.** Read the whole reach of your change (the definitions, every theorem that mentions them, every consumer) BEFORE editing. Simulate the change in your head across all of it: which statements break, which proofs need a case, which rows change. Write ALL the edits. Then ONE build of your reach. Read the whole error log. Fix everything it names. Build again. Two builds per landing is the norm; five is a smell; a build per statement is forbidden.
2. **Single-file checks, not tree builds, while iterating.** To check one module you are editing: `scripts/nd-build lake env lean <that file>` (elaborates one file against existing oleans). A tree build (`lake build X Y`) is for the final reach check only.
3. **No new copies of the build.** Do not `cp -a` a `.lake`. A lane without a `.lake` waits for `scripts/nd-check` (landing within the hour: it elaborates your reach against ONE shared warm build of origin/main, writing only your changed modules' outputs to a lane-local directory) and writes code meanwhile.
4. **Rebase ONCE, at the end.** Do not rebase while iterating. When your change is green: fetch, rebase once, rebuild only what the rebase touched (nd-check does this), push. If main moved again, rebase and push again without rebuilding unless a touched file changed.
5. **Land small, soon.** A landing is one coherent change, not a day's work. Close out what you have; do not start the next card before the current one is on main.
6. **No sub-forks.** A lane does not spawn agents.
7. Everything else in WORK-RULES-20261027.md stands.
