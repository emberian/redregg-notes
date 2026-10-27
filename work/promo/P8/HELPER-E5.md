# CX-PROMO-8/promo8-e5 — the two items E5 owes (LANG-75.19)

Read /Users/ember/dev/redregg/work/promo/P8/HELPER-COMMON.md first, whole. Worktree NAME = promo8-e5.

Context: E5 (1f09446, LANG-75.14 + PROTOCOL-65) landed receipts between Worlds: `Std.head` (a head object
of another World, Lang/StdHead.lean), a `(receipt)` read column checked by Protocol's `Receipt.check`
through a `Lang.program` parameter, `foreign_receipt_sound`. 7fec6d7 added the live column on RANGE rows
(`Lang.keyColumns`, `live_range_read_kept`). Read LANG-75.14 and its addendum in decisions/lang.md
(grep `### LANG-75.14`), and `cv task show` both tasks below. Then do, as ONE landing (`lang:`):

1. cv 01a1671d-09bf: a theorem concluding the RANGE row's `receipt` field (`receiptRow` over `receiptSeen`,
   Lang/Rel.lean), the arm the deployed acceptor uses (client/tests/fixtures/foreign/Accept.ob reads
   `(heads (range 1 1) (receipt))`). State `receipt_range_read_kept` (or `receipt_row_authenticated`; pick the
   name that matches its sibling) beside `live_range_read_kept`, as the range twin of
   `receipt_column_authenticated`. Plant: `receiptRow` fills the field without `receiptSeen`'s check -> the
   theorem red by name (and, if a journey/client row reads the range receipt, that row too; say which).
2. cv 01a1671d-09d7: Lang journey rows over the real `Receive.submit` for `Std.head`'s refusals: HD1-HD5
   (otherWorld / staleHead / forkedHead / badHead / badFork, plus the frozen head), RC1 `headDead` (a
   retired head object, look = none), RC2 `notCommitted` (a receipt of a call never committed). Each row
   passes only on its expected verdict, each with a plant that reds it by name. Put them in a new module
   Lang/Journey/Head.lean (namespace Nanodregg.Lang.Journey, a `headSession : Run` like
   Lang/Journey/Offer.lean's `offerSession`) and add it to Lang/Journey/Main.lean's `runAll args [...]` list
   and imports. If a refusal cannot be reached through `Receive.submit` (e.g. it needs two Worlds the Sim
   cannot build), say so in the decision and file a cv task; do not build a twin beside the substrate.
Decision text: `### LANG-75.19 E5 owed items · the range receipt theorem and the head journey rows`.
Close both cv tasks with the hash.
