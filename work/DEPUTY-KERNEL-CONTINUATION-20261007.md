# DEPUTY-KERNEL continuation (written by DEPUTY-KERNEL a05080ba6a9b148a8 itself, 2026-10-07 ~15:00Z, at ~450K)

For a FRESH deputy (not a distill). Read with: DEPUTY-KERNEL-STATUS-20261006.md (running decision log; tail = newest),
the DEPUTY-KERNEL section + all amendments of DEPUTIES-20261006.md, queue/README.txt, BURST2-BRIEF-20261006.txt (+amendments).
Tell ROOT ("main"), the keeper (a6ac8c6c04f9b7d97) and the workers below your new id on start.

## Rules in force
- Queue: one file per range, work/queue/<lane>.txt, written whole (lane/source/branch/range/what/evidence/breaks/notes); then SendMessage
  the keeper "queued <lane>". Keeper moves files to innext/landed/ejected. Ejected => worker rebases on GitHub `next`, re-queue.
- Workers build on GitHub `next`; shared remote burst2-a:/srv/git/minidregg.git (GIT_SSH_COMMAND="ssh -F ~/.ssh/burst2-20261006.conf").
  Review clone: /private/tmp/claude-501/-Users-ember-dev-breadstuffs/ce776c01-2f59-4f57-8177-23008d71bf57/scratchpad/kernel/mini
- Slots only via slot.sh / build-anywhere / lake-slot (never flock); mem cap 48G default. No polling; act on events.
  Blocks >15 min -> ROOT. Fixture regeneration (NativeAcceptedFixture) is the KEEPER's, never a worker's.
- No new workers unless ROOT says (ROOT allowed replacements of agents at ceiling; prefer FRESH from the agent's own continuation
  file over repeated distills, which compound). GPT-6-wave work = Opus. Function first.
- Review standard: read theorem STATEMENTS; a planted fault per check (EXECUTED where it's a refusal); no field projection renamed as a
  theorem (TokenCensus now refuses it); no silent reinterpretation (refuse, don't reduce); one route per op; the full-Loaded callers
  ratchet only shrinks; private mk is forgeable by `by constructor` (layer 1 = proof fields, layer 2 = TokenCensus).
- Ownership: OB-ENG files (Kernel/ObjectiveActivity*, ObjectRecord*, ObjectiveCall/Send, Inbox, AnswerSlot, Seat*) -> DEPUTY-OB-ENG
  a7ce8f0f4cba1d908 reviews hunks before queue. Host/Main, Host/* JSON, native/resource-client, journeys -> DEPUTY-PLATFORM
  a4b57de3eee5c4307 clears hunks (resumed 15:00Z). DeclaredResourceController, receivers, Store/Durable*, Theory, Pay*, Receiving*,
  TokenCensus, hyp ledger, fixture authority: ours.

## State at writing
GitHub main = next = 74a4a12d. EVERYTHING I queued is in (queue/innext): kn2-forcing(1,2), hyp-ledger, pay-family 1-2, store-open 2a/ii/
i-12/i-34/i-session/revoke, ratchet-fix, port-b-1, port-d, linkindex, fixture-authority (+p5, +values), token-sound (+token-fix),
pay34 (re-genesis), row-e-1 (rebased INBOX v4; the copy in queue/ejected is stale). Nothing pending in queue/.

## Active workers
1. adfa8411d9baf092b (opus) KN2-STORE-OPEN-v (fresh successor; its files: scratchpad/kn2-store-open/CONTINUATION-i..iv.txt, STATUS.txt).
   NOW: rebase lane/kn2-store-open-invoke beb73d8a (23 commits) + PORT-B's bbd63645 (lane/kn2-port-b-callers) + delegate
   (lane/kn2-store-open-delegate e2bfc892) + renounce (lane/kn2-store-open-renounce-wip) onto 74a4a12d; fix Kernel/ApplicationDispatchUpper
   (passes Durable to CheckedCandidate/checkCurrent); rerun plants invoke-undeclared, scratch-reader, authority-undeclared, renounce (never
   executed), port-b-tamper, port-b-undeclared; history-tamper; J0-J8 + JPRIV1 with lane binaries swapped into next's artifacts. Then it
   REPORTS the invoke range -> review + queue (PLATFORM already cleared bbd63645's Host hunks; marker-snapshot question answered: same
   snapshot by construction, type index). Then delegate, renounce, install, birth as separate ranges; then session drops the full shape +
   300/3000 served-request timings. Accepted designs: Ground inductive (.light/.full), Grounded/Ground.At head tie, Ground.At.fullPast,
   Ground.recorded (undeclaredTransaction), scratchReader (StoreOrigin deployment|scratch, Commitment check, Opening.live; docstring must
   say the scratch MAC key authenticates nothing).
2. a3ca8f60d7d9f2932 (opus) KN2-ROW-E (scratch scratchpad/kn2-row-e/STATUS.txt). Range 1 landed. Range 2 (lane 2, r2wip): signature-first
   activity receiver + charged failure receipt. My conditions: funding before the run (theorem nothing runs unfunded); outcome mismatch is
   charged with its own receipt kind; failed_charges_and_rolls_back / malformed_no_charge over the REAL receiver with plants; time the
   refusal alone (not plan+submit); DEPLOYED tariff nonzero rates for replayBytes/coreBytes (Tariff.valid refuses 0;
   decodePolicy_prices_front_end), coreBytes at the WORST per-byte cost up to maxArtifactBytes (core generation is superlinear: ~74 ticks/
   byte at 9.4 MB vs ~20 avg); clients (activity_world.cap + 4 acceptance drivers) read op-214 pins[].frontEnd instead of 4194304;
   journey row with fees differing by exactly the tariff on the quote difference. OB-ENG conditions: COMMAND numbering second-lander
   renumbers; charged-failure arm in the turn census posting only the marker + one Book entry; capacity lanes only in Host/CapacityJson.
   Native DRC free failure + unbounded extractTicks: cv tasks (fix in the DRC retype).

## Waiting for the next free Opus (in this order)
1. cv 01a1163e-62a7: resource-birth families admit NEUTRAL births with no naming authorizer (a check gap, ROOT: ahead of polish).
   Continuation: scratchpad/kn2-pay-family/CONTINUATION-neutral-births.txt (single choke point BirthExportAdmission.check,
   Kernel/ResourceBirthController.lean:619; rule = 7ec55694's namesBirth/authorizerSteps/neutralBirthUnjudged; lane kn2-enrol built).
2. Store full-path leftovers (cv 01a114d4-6651; scratchpad/kn2-port-b/CONTINUATION.txt): JointControl*, Carried*/PreservedPrefix,
   NativeObservationController, the replay walk; fleet ops 101/180 index (cv 01a114aa-6780); 2b-3 deletion (cv 01a11476-4ddb).
3. Row E remainder: ungated payers (cv 01a11636-201e), elaborator pre-core + C4 fuel sufficiency + unpaid publish core gen (01a11636-203c),
   then the LT3 compose-order/C4-ancestry vertical slice with a lowering check that catches a swapped-layer compiler.

## Retired/stood down (don't resume)
pay/token add1f67644cdd474a (and a5162ba6), PORT-B a2c1fbf/a14b0ae/aa285c3, PORT-D ac007f7 is ALIVE on doc-history cv 01a0f60e-2dcf (lane/kn2-doc-history from next); earlier note: check whether it
ever reported; if not, it's open), store a7c778c/ae236ac/a75cc32, hyp-ledger a9ecd76, forcing a51f9e4.

## Other open cv I filed/hold
01a1147a-f80e (exe roots), 01a11477-0c15 (Theory unbounded Digest / injective premises), 01a115dd-d1a6 (strict decoder, not landed),
01a113f0-4ff6 (stored vs lazy differ only in resources: unproved), 01a11429-e42d (pay closed-state tooth), 01a11609-0512 (PLATFORM has it).
