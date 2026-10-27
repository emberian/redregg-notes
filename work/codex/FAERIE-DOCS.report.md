# FAERIE-DOCS report (2026-10-27)

Landed: nanodregg main a2b89265 ("docs: every line that described a deleted mechanism now describes the tree"), pushed from ~/nd-land/faerie-docs on hbox (rebased over a03855ed; one conflict in gates/readset.py, resolved to origin's 262d5b4d, which deleted the bwrap code there).
Prose only. Lean docstrings checked: Codec/Refusal, Codec/Tag, Lang/Std elaborate clean; Host/Base, Host/Cli, Lang/Eval, Lang/Sim/Need, Host/Sim/Run parse past every edit (errors only at code lines, from the stale warm tree); the other edited .lean files could not be checked (the warm main tree lacks their imports), but every edited comment is delimiter-balanced. No full lake build was run.
Decision entries were never rewritten; where text was wrong I appended an "Amended" line or changed a status line/title.

| Item | Result |
|---|---|
| CHARTER law 4 / HOST-19 (lock = key file handle) | already fixed by bace75a3 (HOST-76) |
| Page.lean:10 wrong function | already fixed by f3a00e22 |
| Body.transfer/credit docs | already fixed by 7c857683 (KERNEL-67); file is Kernel/Receive/Call.lean, held anyway |
| duplicateEffect "unreachable" (Call.lean, Gen.lean planted) | already fixed by 7c857683 |
| KERNEL-17/23/55 status lines, "not yet built" titles of 23/24/25/26 | already fixed by 7c857683 |
| KERNEL-41 title "DESIGN, not yet built" | fixed (title now points to the amendment and PORTED entry) |
| World.lean header's order of checks (B13) | already fixed (95f4ea92 / 7c857683) |
| CODEC-3/4/5/11/18 status lines | already fixed by 95f4ea92 |
| CODEC-22 (label `kernel/carried/v1`) | fixed (status line) |
| CODEC-36 (labels /2) | fixed (Status line appended: label is `lang/package/7`) |
| Codec/Kernel.lean Unsigned layout; Stream.lean:9/16 | already fixed by 95f4ea92 |
| Codec/Tag.lean "no census / no fingerprint is pinned" | fixed |
| Codec/Refusal.lean badTag doc | fixed |
| rawList_refuses_overclaimed_count claim | fixed (section now says the theorems state the verdict and cannot see the reservation) |
| Base.lean layout/open | already fixed by bace75a3; leftover `originMax` docstring on chainBytesMax fixed |
| host seal "only write" / "writes nothing" | already fixed by bace75a3 (HOST-77) in Cli.lean:427-440; header line 32 now fixed too |
| Backup.lean "append-only" under --retain | fixed |
| Sim/Run.lean toy-handler disclosure | fixed |
| stepsPerCommandMax doc | already fixed by 0a299c8c |
| settle/refused rows' plant docstrings | already fixed by 0a299c8c |
| custodyPhase doc (phases 9, 11), inviteInput claim, Refusal.host doc, Rows/Writer "one deviation" | fixed |
| client/DESIGN.md | fixed (ops, step tags, spawn, custody shapes, attempt store, refusal names, sandbox, size) |
| CLIENT-29 argv / STATE layout / fdLimit 73 / hidden STATE | fixed (Amended line); the "no safe way ... parent-death" sentence not amended: F2's replacement is not a single fact I could cite |
| client/tests/foreign.rs comments (F16) | already fixed; client/tests/pin.rs cite CLIENT-33 -> CLIENT-35 fixed |
| Escrow header (matcher, retract guard) | already fixed by 0829f4ec; Lang/Proofs/StdOffer.lean still said "matcher" (fixed), StdOfferEscrow proofs header "fuse makes no row act" (fixed) |
| LANG-77 entry naming removed `hne` | fixed (Amended line; also PT3 scope) |
| "KERNEL-25 not yet built": Lang/Std.lean | fixed; decisions/lang.md LANG-20 Amended line |
| Wire tag table missing `hole 18` | not fixed: Lang/Wire.lean is held (TYPES/PCC). Still open |
| Other lies found in the memos: Eval.lean "only a primitive faults", Need.lean "deployed runSetup", take_iff_compliant grain, take_resolve args, LiveHoles module path, jointLaw_sound peerOf | fixed |
| LEDGER-15 (Invokes deleted) | fixed (Amended line) |
| Hosting memo docs (crash-stop, textMax, unread, Socket.lean advert) | already fixed by 37772b9c / 0c9b14e3 / earlier |
| Rows/Params header budget stand-in (PROTOCOL B2) | not found (rows now use Page.budget) |

## bwrap / nd-bwrap / AppArmor / sandbox-exec sweep
Fixed: CHARTER.md CLIENT row; client/DESIGN.md; gates/runs.py and gates/tcb.py comments. deploy/RUNBOOK.md and deploy/live/README.md already say bwrap is retired (CLIENT-48); README.md's run logs are dated history.
Left, by rule: decisions/*.md entries (client CLIENT-2/8/9..., hosting, ops, gates, host, perf) and DECISIONS.md CLIENT-7/8 describe bwrap in the past tense of their date and are append-only; CLIENT-48 supersedes them. gates/tcb.tsv still pins sandbox-exec (macOS), which is real. sandbox/*, launcher/*, launcher/tests/* hold the rest and are off limits (launcher/tests/fence.rs and broker.rs comments, sandbox/src/lib.rs and tests/connect.rs mention bwrap/sandbox-exec accurately or in the past).
gates/readset.py: origin's 262d5b4d had already deleted the bwrap translation; my comment edits there were dropped in the rebase.

## Noticed
The shared session scratchpad .../scratchpad/nd was being modified by another agent while I worked there (Kernel/Sim/Gen.lean, Protocol/Rows*.lean, lakefile.lean appeared as changed). I took only my own patch from it and applied that on hbox; nothing from the other agent landed in a2b89265.
