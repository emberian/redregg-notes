# GLM-J — nd retire + the retire tour step (2026-10-27)

JOB: RETIREMENT is on main (KERNEL-70, 79b1ffe) but a MEMBER cannot reach it: check whether `nd` has a `retire` subcommand; if not add it through the write path; a client test (retire admitted, non-owner notOwner, read of a row under it refused by name); MEMBER.md's table row; a testground tour step "retire an object"; a CLIENT-57+ decision entry. Report here, LESSONS at the end.

-

## Findings (before any edit)

- The subcommand EXISTS: `retire` has been a planned verb since KERNEL-70 itself (79b1ffed added `Verb.retire`, `parseVerb`'s `.retire, [x]`, and `Machine.body`'s `.retire x => .ok (.retire x)`; the arm has its theorems — `machine_retire_refused` in Hosting/Proofs/Package.lean). nd passes argv unread to follow; follow parses, plans, signs, submits. No Machine arm was needed. The brief's premise was half right: a member could already REACH it (pin.rs:151 and doc.rs:239 retire grants through nd), but no test ever drove an OBJECT's retirement, MEMBER.md's command table had no retire row, and client/tests/foreign.rs:24 still said "`nd` has no verb that retires an object".
- The deliverable is therefore evidence and surfaces, not a verb: the client test, the doc row, the stale comment's repair, the scene, the tour step, the meter's allowance.

## What was built

(filled after landing)

ROOT (real 10-27): NEW METHOD, effective now: read /Users/ember/dev/redregg/work/METHOD-20261027.md. Reason across your whole change first; write all edits; ONE build; fix everything from its log; build again; a build per statement is forbidden. Single-file checks (`scripts/nd-build lake env lean FILE`) while iterating. Do NOT cp -a a .lake (disk at 93%): if you have no build yet, write the code and wait for scripts/nd-check (within the hour). Rebase once at the end. Land small, soon. Spawn nothing.
