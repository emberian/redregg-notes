# cv task garden: fn scope (2026-10-08)

Scope (ember, via coordinator): only fn's tasks. Cross-checked against
/Users/ember/dev/fn/build/coordinator/CONVERGE-20261007-3.md and
/Users/ember/dev/fn/planning/repair/items/ (417 items).

## Result: the cv task ledger holds no fn tasks

Searched all 779 tasks (`cv task list --all --json`: 427 in the default view,
132 hidden open, 178 done, 33 resolved, 8 superseded, 10 rev:landed) and 3287
events (90 days):

- repo = /Users/ember/dev/fn: 0 tasks. Repos present: minidregg 554, don 128,
  breadstuffs 25, cv 23, dregg-infra 20, unset 23, phoenix-strip 3, tokeman 3.
- Any of the 417 repair item ids (CL01, BM01, CSP-OWED-..., etc.) in a title,
  body, issue or note: 0 matches.
- CONVERGE row or `CONVERGE-2026...` / `repair/items` reference: 0 matches.
- No event names an fn path. fn's coordination runs on CONVERGE rows and
  repair items, not on cv task.

Verdict counts (fn): close 0, supersede 0, decide 0, keep 0, stale 0.
Write-ops performed: none (nothing in scope).

## Tasks that mention fn but belong to other projects (not touched)

These name fn as a dependency or a word; they are minidregg tasks, map to no
CONVERGE row or repair item, and are outside this garden:

| id | state | why fn appears |
|---|---|---|
| 01a0f70c-6e4d | done | CH-FN-CONTRACT: fn stays the mail transport (contract written) |
| 01a0f71b-cf75 | done | CHANNELS-REV2 folds the fn-contract findings |
| 01a0f6e9-bba8 | open | CHANNELS.md design; cites the fn contract |
| 01a1062d-35c9 | open | S13 PQ TLS: needs the fn NNTP server to offer X25519MLKEM768 (an fn-side precondition, not an fn task) |
| 01a1167a-73f5 | open | SELECTED-EXCHANGE-PREPARE: run against fn 6679dae0e on lane/plat-fn-frames |
| 01a1177f-1ba6 | open | GATEWAY-DIRECT-REFUSAL: journey against fn's --frame gateway setup |
| 01a105f2-0f0f | open | stale docs: fn TRAVELLER/RETURN portals claimed LANDED |
| 01a0f52e-76a0 | open | minidregg standing integrator; notes mention a real fn node |
| 01a0f6bb-c108 | open | K-PQ-FLEET; ML-DSA-65 at the fn helper portals in Host/Main.lean |

Other hits were the Rust keyword `fn` or disk-usage notes about the fn
session's scratch (on ember's task 01a0f54c-d1dd).

If fn work should live in cv task, it would need opening there (one task
per open CONVERGE row or repair item); nothing exists to garden today.
