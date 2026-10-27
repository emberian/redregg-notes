# PERF ATTACK ORDER — 2026-10-13 (root's merge of perf-trace/{CREATE,JUDGE,READ}.md + SINS-LEDGER; LOCAL first)
Regime: the workload's Host is WARM (`mini serve`); a cold Host spawn is ~0 G there (CREATE). Per-record growth ~1 G/record on
resource (32→73 G) and create (20→50 G) steps comes from whole-Store work INSIDE the warm server per request. Price first:
one workload run with MINIDREGG_HOST_TRACE=1 MINI_OPEN_TIMING=1 (both exist, both were off), then attack in this order.

## LOCAL (no persisted bytes, no theorem statements change) — expected effect order
A. SERVER op 212 `NativeHost.confirmed` (NativeHost.lean:1245) cold-opens the WHOLE Store (openExisting: full log, replay from genesis,
   full tree, validateLoaded) to read back ONE receipt; same `confirmed` on 12+ session routes → sessionConfirmed/sessionExactConfirmed. [CREATE N1] The O(h) term on every step.
B. SERVER a commit never advances the openings it came from → every record re-executed/re-verified 2–3× (extendFrom + extendVerified), each light
   refresh rebuilds the root from ALL cells (RootCache.ofEntries, RootsExact.ofEntries maybe twice) → adopt the .exact readback into both openings
   (Light.adopt / receiveServed) + kern-grow's incremental `advance` (patch in work/kern-briefs/). [CREATE N2, ledger 1]
C. SERVER+CLIENT activityPlanLoaded decides the turn 5× (NativeHost.lean:2350-2365), submit 2–3× more, consent provider repeats 5× → decide ONCE, project
   header/report/outcome/verdict/frontEnd from it. [JUDGE 1, CREATE N3] ~20 decisions → 4 per update.
D. SERVER every frame load re-runs the whole source front end on a content-addressed package (parse, 2 elab, 4 packet renders [one only for a length],
   3 checker runs, 2 hashes; ObjectiveCall.lean:437-462, ObjectiveActivity.lean:936-955) → memoize per turn/package digest in-process. [JUDGE 2 local part]
E. SERVER the Objective gate's loadDirectory decodes EVERY cell per admission; result unread (ObjectiveActivityReceiverCore.lean:818) → delete; gate_spent_refused loses one hypothesis. [JUDGE 5]
F. SERVER cold open recomputes the world root up to 6× (root before the MAC that binds it; body re-encoded for the MAC; both opens rebuild twice;
   DurableCheckpointCodec.lean:620-666) → open once, MAC first, reuse the tree. [READ 4 local part; ledger 1]
G. CLIENT every `mini` process SHA-256s the 173 MB Host image (main.rs:483-530) → use the workspace's pinned hostSha256 (remote path already does). [READ 3, CREATE N7]
H. CLIENT codec verbs spawn a fresh Host per call (4/resource step, 3/create; 5–6 per at-read; client_consent.rs:559-575) though the server answers ops 7–11 → route over the socket / keep one codec child. [READ 2, CREATE N7]
I. CLIENT/WORKLOAD `mini query --view at` without --socket → 2 full cold opens per signed read → use the socket (ops 4/5 run on the session). [READ 1]
J. CODEC fixedStream.decodePrefix calls `octets.length` on the whole remaining buffer per field (Tower256ConcreteBackend.lean:309) → O(fields·bytes) per decode → bounded take / ByteArray cursor, @[csimp]. [CREATE N4]
K. SESSION rebase sets base := head (DurableReceiverCore.lean:1185) → after 128 records every `at` replays from genesis → keep a list of checkpoint bases in Loaded. [READ 5 local part]
L. CLIENT two cold processes per invoke (--prepare-only probe + submit; activity_world.py:337-387) → one process (interim). [JUDGE 3]
M. SESSION: Store binary run twice per request when nothing changed; Session.start does a full AND a light open; op 214 re-decodes the authority cell it holds; spent-nullifier + journal lookups are linear scans; full open chain-hashes the whole log from height 1. [READ extras]
## DESIGN (Ember decides; after the LOCAL pass is measured)
- `at` through Reader.stateAt from the nearest kept checkpoint (changes atCovered_sound) [READ 5]; drop the root recompute behind a valid MAC (removes a check) [READ 4];
  consent provider re-execution (which process consent trusts) [JUDGE 4, READ 2]; front-end results cached across turns (persisted) [JUDGE 2]; the quote the probe
  exists to learn, published per package (op 214) so the probe process goes away [JUDGE 3]; keep the root tree on disk / compressed tree [ledger 1]; Turn as the persisted entry [ledger 4].
## NOT offenders (don't chase): inbox lookup (O(1) via generation cursor), judgeDomains (touched domains only), law eval (once per object), grant check (digest compare), no runtime census. [JUDGE]
