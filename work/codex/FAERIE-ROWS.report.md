# FAERIE-ROWS: pushed 9508a28c (rebased onto 9c170a8b; lang-journey GREEN before the rebase)

| item | result |
|---|---|
| LE5 | tightened to `refused transferSpent` |
| L6 | tightened to program refusal payload `illTyped declared @top` (new `refusedProgramWith`) |
| LH8b, LH11b | kept only `refused grantRight` (the notChooser arm sits behind the grant check, unreachable) |
| P8-deadline | `rejected outsideWindow` only |
| P8.2 rows | no disjunction found (`rejected stale`, `support0 dead` already single names); only the deadline row was a disjunction |
| management-* (5 of 6 rows) | `lawDenied` with `codeChosen: notChooser / accepted / closed / unknownHole / unknownCandidate` (new `lawDeniedWith`); management-bootstrap is a positive `isOk` and unchanged |
| LC8 | exact payload `arguments: decode Nanodregg.Codec.Refusal.truncated 8 4` |
| HD5 | added row HD5b, the steps arm of badFork (fork at step 22, not the held 21): `head: badFork` |
| foreign.rs X1b + substring matches | already: asserts `keyTaken`; the others assert names (`pathMismatch`, `headMismatch`, `forkedHead`, `untrusted`, `early`, `settled`) |
| toy_budget_serves / deployed_budget_serves | already: deleted (only `decisions/*.md` prose mentions remain) |
| settle plant | already: `.trustLookup` at line 6, the lying lookup's own line; `rows settle` PASS |
| staleRange plant | already: the docstring and the Loopback code change only the range; `rangeInvoke` plant unchanged |
| lost_reply_policy / Peer.reliable | SKIPPED: nothing in the resident reads the Boolean, so the fix is a design (give the policy a reader) or deleting the theorem's plants |

Files: Lang/Journey.lean, Lang/Journey/OfferEscrow.lean, Lang/Journey/Head.lean, Lang/Journey/Contextual.lean.
Not touched: Protocol/Rows*, foreign.rs. Not run: the Rust tests (unchanged), `rows` (unchanged except the settle check above).
