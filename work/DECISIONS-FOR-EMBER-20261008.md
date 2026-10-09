# Decisions for Ember — 2026-10-08

Fifteen open items the task store says are yours. For each: the question in plain words, why it exists and what
sits waiting on it, the options as consequences, a labelled recommendation, whether it is yours at all under
`breadstuffs/CLAUDE.md` (pause only for key custody, weakening a check, outward/irreversible acts, genuine taste
forks), and the exact command for each answer. Nothing in the store was changed by this memo.

Evidence labels: **READ (path)** = I read it; **INFERRED** = my inference from what I read. Where the triage's
one-line gloss was wrong, I say so.

Order: the three that touch THE BAR (cv `01a0f9c0-521b`: two friends + hosted Hermes over ssh on the public
node, 1000 records, write ≤ 5 s, cold reopen ≤ 60 s) or DEPLOY-3 (rehearsed, never shipped; the public node
still runs candidate `5688775a`) come first. Everything after #3 gates nothing on 10-13.

Where the store needs a `--from`, use `--from ember` (or set `CV_ENDPOINT=ember` once).

---

## 1. `01a0f54c-d1dd` — EMBER's consolidated list: the Hermes inputs are what actually gate THE BAR

**Question.** Of the ~30 items parked on you in this one task, which still need you, and will you do the two
that THE BAR cannot run without: fill `providers.json` (model ids, optional pool key) and author one
`controller.json` per served friend?

**Why it exists.** This task is the 10-01 catch-all of "things only ember can do". Much of it has since been
done or superseded. **READ** (SWARM-LEDGER-20261004 line 106): on 10-04 you gave the DEPLOY-4 enrollment
address (`5N2uUG4T…`), the 50 DREGG/week rate, and the age backup recipient (`age13p72…`; identity in
`~/mini-backup-age`). **READ** (deploy-3.md §"What turns on"): the Hermes component stays OFF until
`/etc/mini/providers.json` validates and `/var/lib/mini/hermes/controller.json` exists — both marked **EMBER**.
THE BAR requires a *hosted Hermes*; so this is the one input on this list that blocks the bar. Also still
open on your machine, **READ** (`ls`): `~/.ssh/id_portable` is not owned by you and is mode 644 (the
`sudo chown ember … && chmod 600` ask); the six `~/.ssh/mini-j9-*` test keys still exist; `~/dev/dregg-assortia`
is 2 commits ahead of its remote. `~/dev/dregg-infra` local main equals its `origin` (the anchor), so that push
is done — INFERRED from `git log origin/main..main` = 0.

**Options.**
- (a) Do the two Hermes inputs now from the templates in `~/dev/dregg-infra/edge/mini/templates/` (10 minutes;
  the runbook §7 has the exact commands); the rest of the list is handled by the root as ordinary work.
- (b) Tell the root to run THE BAR with a *scripted* provider (no real model) — then "hosted Hermes" on 10-13 is
  a fixture, which the bar's own text refuses ("nothing counts until it runs joined", and the 10-02 notes say
  synthetic providers cannot close the environmental rows).

**Recommendation: (a).** Yours only because the pool key and provider credentials are key material; everything
else on the list (pushes, Sigilante note, Discord app) is yours for being outward, but none of it gates 10-13.
The Discord app and the Sigilante note can wait past the bar.

**Commands.**
- Keep the task but mark what remains: `cv task note 01a0f54c-d1dd "10-08: remaining EMBER items = providers.json + controller.json (gate THE BAR), chown id_portable, delete mini-j9-* keys, push dregg-assortia (2), Discord app, Sigilante note, GitHub drafts. Everything else done or moved." --from ember`
- If you want it split into per-item decisions the inbox can show: `cv task split 01a0f54c-d1dd`

---

## 2. `01a1052c-6e3a` — DEPLOY-3 sponsor key: rotatable or not (decision, OVERDUE since 10-07)

**Question.** When DEPLOY-3 re-genesises the public node, should the genesis sponsor's key be generated
on the box with *no* successor committed (as `run.sh init` does today), or do you generate the sponsor key and
its next key off-box first so the sponsor can later rotate without another re-genesis?

**Why it exists.** **READ** (`deploy/candidate/run.sh:66-75` on Mini origin/main): `init` runs `mini keygen
--no-prerotation` for the sponsor whenever `genesis-params.json` has `sponsor.nextKeyDigest == null`, and
`dregg-infra/edge/mini/genesis-params.json` has no such field (READ, `jq`). Rotation itself is real on main
(K-PREROTATE: journey `jrot.sh`, `Kernel/SubjectKeyCommitmentAdoption.lean`), it is just not offered to the
sponsor. With option A a leaked sponsor key means re-genesis; with B it means one rotation turn. The sponsor's
secret lives on the box either way (`$state/keys/sponsor.key`). **READ** (ledger line 106): on 10-04 you said
"will read later (default A stands in 3 days)" — that deadline passed yesterday, so A already stands.
Nothing in DEPLOY-3 waits on this: A needs nothing from you; B needs an off-box keygen before step 4.

**Options.**
- A (default): non-rotatable devnet sponsor key, as built. A box compromise = re-genesis, which we do anyway.
- B: generate `sponsor` + `next` off-box, put the digest in `genesis-params.json`, bootstrap by hand (run.sh
  refuses to init against a non-null digest — READ line 73; a small `run.sh init --sponsor-key` is a lane's hour).
  You then hold a second secret (the next key) off-box.

**Recommendation: A, now.** The doctrine says re-genesis is the answer to "what does it cost"; B adds custody
of a second key for a devnet whose friends are told their state is wiped on reset anyway. Yours only because
it is key custody; the default is right and already stood by your own 10-04 statement. Revisit B at DEPLOY-4
when real DREGG enrolments give the sponsor something worth not re-genesising.

**Commands.**
- A: `cv task resolve 01a1052c-6e3a --accept-default --from ember`
- B: `cv task resolve 01a1052c-6e3a --choice "B: pre-rotation: generate sponsor pair + next key off-box, digest into genesis-params, add run.sh init --sponsor-key" --from ember`

---

## 3. `01a0f6db-c50a` — CLOCK TICKERS: a leaked clock key moves `now` forward forever; replacing a ticker needs re-genesis

**Question.** Two things: (i) should the kernel cap how far one tick may advance the clock, and (ii) do you
want a way to replace the clock ticker subject without a re-genesis?

**Why it exists.** **READ** (`Kernel/ClockTickReceiver.lean:75` on main): `decideTick` accepts any `next` with
`current.now < next.now`; no step bound exists anywhere (grep for max/step/bound in Clock files: empty). The
clock key is generated by `run.sh init` and installed at `/var/lib/mini/clock/clock.key` on the box
(READ clock-subject.md:209,219). So whoever holds that file can set `now` to the year 3000 and monotonicity
makes it permanent — every lease, `valid_until`, freshness window then misbehaves at once. **READ**
(clock-subject.md §6): the clock design is already a flag day (GENESIS-SOURCE/v3), and DEPLOY-3 is itself a
re-genesis, so a bound landed before the candidate is cut costs nothing extra. Nothing is deployed with a clock
yet (public node = `5688775a`, pre-clock), so nothing is at risk *today*; it becomes a live hazard the moment
DEPLOY-3 ships. The triage gloss ("accept re-genesis + add a step bound") was a guess — but it is the right one.

**Options.**
- (i) Step bound: a genesis parameter `maxTickStep` (e.g. 1 hour of `now` units) checked in `decideTick`;
  a leaked key can then only drift the clock at the ticker's own cadence, which the operator sees in the tick
  journal. Strengthens a check; a Lean change + one theorem + re-genesis.
- (ii) Ticker replacement: (ii-a) none — replacing the ticker = re-genesis (we do that anyway); (ii-b) a
  `clock-control` capability held by a separate cold key you keep off-box — a new secret in your custody.

**Recommendation: do (i) now, before the DEPLOY-3 candidate; pick (ii-a).** (i) is not your call — it tightens
a check and the doctrine says just do it; the root should land it. (ii) is yours only in the (ii-b) branch
because it mints a cold key; (ii-a) is the greenfield default. The step size itself (an hour? a day?) is a
one-word answer if you have a preference; otherwise the lane picks 1 h and says so.

**Commands.**
- (i)+(ii-a): `cv task note 01a0f6db-c50a "ember 10-08: land a per-tick step bound (genesis param) before the DEPLOY-3 candidate; ticker replacement = re-genesis, no cold key." --from ember` then let the root reassign it as a lane task.
- (ii-b) instead: `cv task note 01a0f6db-c50a "ember 10-08: step bound yes; also a clock-control capability on a cold key I hold off-box." --from ember`

---

## 4. `01a0f52e-7777` — TEARDOWN-LEFTOVERS: old PoA data, two old images, TELEGRAM secrets, portal links, DNS

**Question.** May the root delete the 4.8 GB of dead PoA chain data and the two pre-09-30 node images on
the workhorse, and will you rotate or revoke the Telegram bot token that is still in the box's `.env`?

**Why it exists.** **READ** (task body; product/teardown-arcade.md): the arcade/Telegram/PoA-web teardown of
09-30 archived everything (sha-pinned tarballs, incl. `telegram-secrets.env`) but left: `/var/lib/dregg/poa`
(4.8 GB, masked), images `dregg-node:pre-20260930` etc. (2.4 GB), `TELEGRAM_*` lines in `/opt/dregg-edge/.env`
(dead since the bot was torn down — READ `edge/deploy.sh:328`), portal links that now 308 to dregg.net, and the
`dregg.gg` / `dregg.tech` / `pathofangels.network` Gandi zones in `edge/dns/main.tf`. Nothing on 10-13
depends on any of it; the only *risk* item is the live Telegram token sitting in a file.

**Options.**
- Data/images: delete now (frees 7 GB; the archives exist) vs keep until DEPLOY-3 proves out (the task's own
  default — INFERRED that it was written when a rollback to the old image was still plausible; it no longer is,
  DEPLOY-3 is a re-genesis not a rollback).
- Telegram token: revoke at @BotFather (one tap; the bot is gone) and let the root strip the lines, vs leave.
- Portal links + DNS: edit the portal page (cosmetic) vs leave; DNS records stay until you choose to drop the
  domains — the 308 blocks are harmless and the doctrine's "outward act" pause applies to deleting zones.

**Recommendation.** Revoke the token yourself (key material: yours, two minutes); tell the root to delete the
PoA data and old images (deletion of box state is yours by your own disk rule, so one word is needed); leave
DNS and the portal page. Not a 10-13 item.

**Commands.**
- `cv task note 01a0f52e-7777 "ember 10-08: TELEGRAM token revoked; root may rm /var/lib/dregg/poa and the two pre-20260930 images; DNS + portal links stay." --from ember`
- Or keep everything: `cv task note 01a0f52e-7777 "ember 10-08: keep all leftovers until after 10-13." --from ember`

---

## 5. `01a0f52e-7763` — GITHUB: post the finalized Bread review comments and closures

**Question.** Will you post the 30-odd drafted GitHub comments/closures on `emberian/dregg` (Bread), and fill
the three `[ember: …]` judgement slots in `issue-66.md` first?

**Why it exists.** **READ** (`claudesplosion/prs/github-drafts/INDEX.md`, `FINALIZE-LOG.md`): the drafts were
finalized 09-30 with every sha on `bread-union`, "post only after main contains bread-union". **READ**
(`git log origin/main` in breadstuffs): main now contains the union merges, so the precondition is met; the
`pr-81` HOLD was cleared (`[ember: sha]` = `d60277843`). **READ** (`gh`): nothing has been posted — #55 #59 #65
#68 #69 are all still OPEN, PRs #72–#96 have 0–2 comments, only #90 is closed. What remains for you: the three
slots in `issue-66.md` (fee recycling as substrate answer or devnet policy; coordination turns as a fee class;
the leash/oversight-attestation direction). The contributor (akapug) has been waiting since 09-29. Nothing on
Mini's 10-13 depends on this; it is Bread goodwill and the "we do the work, then tell contributors what changed"
rule (memory: CONTRIBUTOR PRs).

**Options.**
- Post everything in INDEX order after writing the three slot answers (an evening).
- Post only the five closures + the landing comments now, hold `issue-66`/`issue-74` until you have the slot
  answers (the INDEX's own split: closures "can go any time").
- Hand the root a `gh` token and let it post under your name — refused by the drafts' own design ("ember reads
  first") and by the doctrine (outward act).

**Recommendation: the second** — closures and landing comments this week, `issue-66` when you have twenty
minutes for the three opinions. Yours because it is outward and the slots are your judgement.

**Commands.**
- When posted: `cv task done 01a0f52e-7763 --observed "ember posted INDEX order; issue-66 slots filled"`
- If you will not post: `cv task abandon 01a0f52e-7763 --reason "ember: not posting the Bread drafts" --from ember`

---

## 6. `01a105b6-8396` — COMMON-WORLD: the hbox demo world lost its store directory

**Question.** The "common OO world" on hbox (the one the seven Studio web servers point at) had its store,
sponsor dir and binary deleted in the 10-04 workbox cleanup; do you want it restored from the 22:55 copy or
simply re-born fresh?

**Why it exists.** **READ** (ssh hbox, today): the Host pid 1189053 is still running from the deleted inode
(uptime 5 d 02 h) and six Studio ports still listen; its next store access fails. The survivor is
`/tank/claude-evidence-20261004/common-oo-world` (genesis, params, keys, store copy from 22:55). This is a dev
demo world on hbox, not the public node, and not on THE BAR's path. The triage filed it STALE-WIP; it is
really a 30-second choice.

**Options.**
- (a) Re-home from the 22:55 copy: units rewritten to `/tank` paths, binary rebuilt from the warm base; state
  written after 22:55 is lost anyway.
- (b) Re-genesis a fresh common world from current main (post-cut), rewrite the units once. Studio demo state
  is recreated by the Studio journey.

**Recommendation: (b).** Nothing depends on its history (READ task body; MORNING-MAP decision 1 says the same).
Not your call under the doctrine — it is a dev world; the root should take (b) and only tell you.

**Commands.**
- (b): `cv task note 01a105b6-8396 "ember 10-08: re-genesis fresh; kill pid 1189053 and the Studio servers; rewrite the units." --from ember`
- (a): `cv task note 01a105b6-8396 "ember 10-08: re-home from the 22:55 evidence copy." --from ember`

---

## 7. `01a10500-f300` — SPK: the live r2 world's app 8502, generation 4, is stuck behind a refused v3 attempt

**Question.** On hbox's r2 world, the SPK (hosted-app) resident for app 8502 cannot start its generation-4
attempt because the directory still holds a *refused* v3 begin-attempt and the v3 freshness check refuses to
proceed there; the lane wants to know whether it may "close" that refused attempt (by a receipt, not by deleting
files) as part of cutting r2 over to the v4 retry protocol. Is that your decision?

**Why it exists.** **READ** (ssh hbox): `mini-spk-a8502-g2` and `-g4` units are `failed`, the r2 supervisor is
`failed`, the r2 store/broker/sshd are running. **READ** (`docs/SPK-LIFECYCLE.md` §"Cutover for the live r2
world" on main; the W2.F v4 code `dd97fcc6` IS on main): the cutover is written out in six steps; step 4 is this
question, with the constraint "must not be done by deleting the attempt files". r2 is a dev world, not the public
node, and SPK apps are not in THE BAR. The triage gloss ("Ember/ROOT cutover decision") inflated it.

**Options.**
- (a) Do the written cutover on r2 (stage v4 Host + spk-host, close the refused attempt with a v4 receipt,
  restart g4). Exercises the real retry path on real history — the thing the v4 work exists for.
- (b) Re-genesis r2 (or a fresh r3) from main and never touch the stuck directory. Cheaper; loses the only
  live instance of the "host-refused, effect-free attempt" case.

**Recommendation: (a), by the root, and (b) if (a) takes more than a lane-day.** Not yours: no custody, no
weakened check, a dev world.

**Commands.**
- `cv task note 01a10500-f300 "ember 10-08: root decides; try the written cutover on r2, else re-genesis r3." --from ember`

---

## 8. `01a10564-84ef` — Use the C machine as the admission executor? (dissolved by measurement)

**Question.** Should Objective admission re-execute programs with the C runtime (900–2900× faster than the
Lean machine measured on 10-04), trusting a differential gate to keep it equal to the Lean specification?

**Why it exists.** **READ** (ledger line 103): the C backend landed as a *differential oracle* (224/224 cases).
**READ** (ledger line 125; `Theory/ObjectiveBendDemandData.lean:64` on main): the next day the proved fast Lean
machine landed — `forceWith_eq_fast` and siblings are `@[csimp]` theorems (axioms `[propext, Quot.sound]`), so
admission already runs the fast code with every theorem unchanged; runBounded went 15–38 s → 25–292 ms, within
2–4× of C. **READ** (GPT-6 T2.5): "profile now; don't switch admission to a C backend on a few matching outputs".
MORNING-MAP decision 2: "Lean stays the executor; can close on your word".

**Options.**
- No (Lean stays the admission executor; C remains an oracle and a future fast path). Admission trusts no C.
- Yes (C in admission behind the gate). Buys ~2–4×; puts unverified C in the trust base; contradicts the "Lean
  must be the implementation" law in memory.

**Recommendation: No.** Not your call — it would *weaken* the trust base, which the doctrine says never to do
for speed. The task should simply be closed.

**Commands.**
- `cv task done 01a10564-84ef --observed "Lean stays the admission executor (fast machine a2a8a203, forceWith_eq_fast); C machine = differential oracle only; GPT-6 T2.5 agrees"`

---

## 9. `01a0f53e-f651` — QUOTE-DISCLOSE: already ruled; just close it

**Question.** Should a quote carry the quoted text to readers who can only read the quoting room (a disclosure),
or stay a reference that renders `unavailable` unless the reader can read the source?

**Why it exists.** **READ** (task body; `planning/place/k-content-actions.md`): quote is built as a reference
with proven theorems (`transclusion_respects_source_coverage`: a reader without source coverage sees
`unavailable`, identically across stores). You already chose "reference-only for October, `--disclose` later",
and the 10-06 DEPUTY-PRODUCT ruling recorded it with a full design for the later `quote --disclose` (a
disclosure act the SOURCE law must permit). Nothing is waiting; the task is open only because no one closed it.

**Options.** Reference-only now (chosen) vs. build `--disclose` now (a lane; interacts with the read-target
authorization fix `ea93`, which should land first).

**Recommendation: close as decided.** Yours in principle (a disclosure is a privacy-shape choice) and already
made.

**Commands.**
- `cv task done 01a0f53e-f651 --observed "ember: reference-only for October; quote --disclose = later disclosure act per the 10-06 DEPUTY-PRODUCT design"`
- To change your mind: `cv task note 01a0f53e-f651 "ember 10-08: build quote --disclose now, after ea93." --from ember`

---

## 10. `01a0f96b-34f4` — CHANNELS §10.10: how sealed room messages are keyed (decision)

**Question.** In the constant-rate channel design, is a message to one member sealed under a *pairwise* key
(sender↔recipient, ML-KEM, lazily set up per key period), under an MLS/TreeKEM-style *group* key that rotates on
every membership change, or under *one static group key per room*?

**Why it exists.** **READ** (task body; CHANNELS.md §10.10): the 10-01 inbox click "one group key per room" was
an accident of the page; the orchestrator re-posed it. Today's code (READ `native/resource-client/src/channel.rs:23`)
seals per cell with fresh X25519 and says ML-KEM pairwise keys are the CH-KEM-EPOCH lane — i.e. option (2) is
what is being built toward; nothing MLS-shaped exists. Private rooms (the non-channel feature) do an O(n) rewrap
on kick by hand, which is what TreeKEM would make O(log n). The codex note cites a research README that is NOT on
main (`docs/research/2026-10-02-private-objects/` — READ, `git ls-tree`: absent). Nothing on 10-13 touches
channels; this gates only the CH-KEM-EPOCH lane's target.

**Options.**
- (2) default: pairwise ML-KEM per correspondent + a group key only for room-wide messages. Recipient hidden
  from other members; +3–4 cells on the first message to each correspondent per period (+3.5 s at P1, measured
  in sim); simplest to prove.
- (1) MLS/TreeKEM group keying now: forward secrecy + post-compromise security on membership change at
  O(log n); every member reads every room message (a room); a real Lean lane (~2 days) plus a PQ TreeKEM variant
  that is still standards-in-progress.
- (3) one static group key per room: cheapest; a leaked key reads the room's whole past and future until a
  manual rotation. The orchestrator "would not ship (3)".

**Recommendation: (2) now, (1) as the lane's stated target** (the task's own default). Your stated preference
"PQ/hybrid, not MLS" is compatible: (2) is PQ (ML-KEM) and hybrid is one line (X25519 ‖ ML-KEM). Yours because
it is a genuine taste fork with key-material consequences; the default is sound and reversible (channels have no
users).

**Commands.**
- (2): `cv task resolve 01a0f96b-34f4 --accept-default --from ember`
- (1): `cv task resolve 01a0f96b-34f4 --choice "(1) MLS-style TreeKEM group keying for rooms now, 2-member groups for DMs" --from ember`
- (3): `cv task resolve 01a0f96b-34f4 --choice "(3) one static group key per room (what got clicked)" --from ember`

---

## 11. `01a10afe-eda1` — OB V2: `compose(a, b)` — which argument wins?

**Question.** In Objective Bend, `compose(a, b, c)` is least-specific-first (the rightmost wins, Nix's
`composeManyExtensions` order) while `spec S extends A, B` and the precedence list are most-specific-first
(A wins). Do you want one convention, and which?

**Why it exists.** **READ** (OB-FAREOO-REVIEW V2): LTUO §5.4.2 says the mix order "should match" the class
syntax order; the review found no stated reason for Mini's mismatch, only the convention in the tutorial
(`docs/OBJECTIVE-BEND-TUTORIAL.md:563,707`). **READ** (GPT-6 rows, T3 and Row G): "defer the compose-order flag
day"; "prioritise composition/method-contribution semantics over the compose-order edition change". A flip
re-emits every `compose` site (today: tutorial, 16 `.obend` examples, the law/compose tests — INFERRED small).
Gates nothing.

**Options.**
- Keep: two conventions, record the reason ("compose is a function pipeline; extends is a class list").
  Every reader learns two orders; the doctrine's "two shapes that agree today will disagree later" applies.
- Flip compose to most-specific-first: one convention; one re-emit, cheapest now while the only compose sites
  are ours; bundled with the LT3 composition-semantics slice GPT-6 wants first so there is one flag day.

**Recommendation: flip, but *when* the LT3 slice lands, not as its own lane.** Yours — this is exactly the
doctrine's "genuine taste fork". One word from you ("Nix order" or "C3 order") is the whole decision.

**Commands.**
- Flip: `cv task note 01a10afe-eda1 "ember 10-08: one convention: most-specific-first (extends order) for compose too; re-emit with the LT3 composition slice." --from ember`
- Keep: `cv task done 01a10afe-eda1 --observed "ember: keep compose least-specific-first (Nix); record the reason in OBJECTIVE-BEND.md"`

---

## 12. `01a10afe-ecd0` — OB U10: does Objective Bend get multiple dispatch (multimethods)?

**Question.** Should methods be chosen by the runtime types of *several* arguments (CLOS-style generic
functions), or stay single-dispatch on `self` with LT2's F-bounded binary methods for the two-argument cases?

**Why it exists.** **READ** (OB review U10 and the OB7/OB8 note): LTUO §9.3 treats multimethods as part of a
full OO calculus; Mini has no construct; the review's own lesson is "if ever built, it belongs to the calculus,
not to `send`". No program or theorem waits on it; the review filed it as "decide", not "build".

**Options.**
- No (default): single dispatch; binary methods via F-bounded self types; record the deviation with LTUO §9.3
  cited. Zero work.
- Yes: a global dispatch-table construct in the calculus plus its no-refusal/determinism theorems — a real lane,
  and the first feature that would make a method's choice depend on state outside the object.

**Recommendation: No, record the deviation.** Not yours — language design the root can take, reversible, no
custody. Flagged to you only because the review tagged every LTUO gap "decide".

**Commands.**
- `cv task done 01a10afe-ecd0 --observed "single dispatch + F-bounded binary methods; no multimethods; deviation recorded"`

---

## 13. `01a10afe-ecf9` — OB U11: should types become first-class values (class = prototype for a type)?

**Question.** LTUO's class OO makes a class a prototype for a type descriptor that exists at run time; Objective
Bend's types are static only. Do you want run-time type descriptors as values?

**Why it exists.** **READ** (OB review U11, V4, MODULAR-TYPING D1): templates not polymorphic Core4 terms was a
*deliberate* choice to keep every machine proof unchanged; first-class type descriptors would have to meet the
no-refusal theorem (a value that is a type must not be able to make admission refuse late). No consumer asks for
it; it is on the list because LTUO has it.

**Options.**
- Keep static (default): record the deviation with the reason (no-refusal theorem; proofs unchanged).
- Build descriptors as values: reopens the typing discipline and every proof over `State`; a multi-week lane
  with no present consumer.

**Recommendation: keep static, record it.** Not yours — design default, reversible.

**Commands.**
- `cv task done 01a10afe-ecf9 --observed "types stay static; deliberate deviation from LTUO §6.2 recorded with the no-refusal reason"`

---

## 14. `01a0f6ac-3722` — NOCK-PACK: send the Nockchain contribution pack to Chris? (and the other Nock rows)

**Question.** A 0.8 MB pack (`~/workbox/nockchain-pack-2026-10-01/`, READ, present) proves the Goldilocks prime
in Lean, reproduces their constraint artifact (noun-equal, 4 padding bytes different), prices their deployed
STARK's soundness (query term 2^-7.8 unique-decoding, 2^-23.9 Johnson; their 2^-48 conjecture disproved in Lean),
and lists runtime findings + 5 questions. Do you send it to Chris Allen?

**Why it exists.** Built 10-01 for Chris's swim-lanes doc; nothing sent. You said today "i thought we abandoned
nock for the most part". **READ** (`redregg/designs/BEND-DIRECTION-20261003.txt:17,92`): "retain Nock support,
but prefer Bend as broadly as possible … Further Nock-specific machine expansion stopped". So the *Mini-internal*
Nock rows are presumptively obsolete: NOCK-FEE `01a0f96d-f34c` (STALE-WIP, branch only), NOCK carriers
`01a0f52e-7730`, MINK-JET-2/3 `01a0fad6-6713`/`-6732`, HELD-PROGRAMS `01a0f8a2-9e3d`. The pack is different in
kind — it is about *their* chain's cryptography, not Mini's Nock support — so the Bend pivot does not decide it;
only you do (outward act). Its 7.4 GB `.lake` was deleted on 10-01 for disk; the packet-4 project rebuilds in
~20 min if you send.

**Options.**
- Send (after a lane rebuilds packet 4 and you read `README.md` + `QUESTIONS.md`): a substantive, flattering
  contribution; it also tells them their 2^-48 claim is false, which is the point and the risk.
- Don't send; abandon the task; keep the directory as research.

**Recommendation: don't send unless you still want a relationship with that project; abandon the four Mini-side
Nock rows regardless.** Yours (outward). The Mini-side abandonments are the root's.

**Commands.**
- Don't send: `cv task abandon 01a0f6ac-3722 --reason "ember: not sending; nock de-prioritised 10-03 (BEND-DIRECTION)" --from ember`
- Send: `cv task note 01a0f6ac-3722 "ember 10-08: send; rebuild packet4 .lake first and I will read README+QUESTIONS" --from ember`
- Nock rows (root): `cv task abandon 01a0f96d-f34c --reason "nock expansion stopped 10-03"`; same for `01a0f52e-7730`, `01a0fad6-6713`, `01a0fad6-6732`, `01a0f8a2-9e3d`.

---

## 15. `01a0f961-721d` — tokeman: `per_session_reserve` has no input after drain-truth

**Question.** In your tokeman daemon, the rotation score subtracts `sessions × per_session_reserve` for
"stranded" sessions; the drain-truth work proved live sessions are never stranded, so the term is always zero.
Delete the knob or re-ground it on a real signal?

**Why it exists.** **READ** (`~/dev/tokeman`): `drain-truth` (f64c474, 10-01) is NOT merged to `main`
(main = 90e79b0), and the installed `~/.cargo/bin/tokeman` is dated Sep 29 — older than the branch. So the
question is moot until you install drain-truth (`cargo install --path . && tokeman rotate uninstall && tokeman
rotate install`, READ ledger note 10-01 17:45). Not a Mini item; tagged other-project.

**Options.**
- Delete `per_session_reserve` / `loaded_dwell_score` and the config field when merging drain-truth (default).
- Re-ground on the "untrusted-workspace straggler" signal the drain doc mentions but did not chase.

**Recommendation: delete, at the drain-truth merge.** Not yours under the doctrine (no custody; your own tool,
reversible); the root/lane merging drain-truth takes the default unless you veto.

**Commands.**
- `cv task note 01a0f961-721d "ember 10-08: delete per_session_reserve with the drain-truth merge" --from ember`
- Veto: `cv task note 01a0f961-721d "ember 10-08: re-ground on untrusted-workspace stragglers instead" --from ember`

---

## (A) The 16 "landed but unverified" close candidates (`/tmp/landed-recheck.tsv`, UNVERIFIED rows)

Verified by `git merge-base --is-ancestor <sha> <main>` in the repo each task names. 14 close, 2 keep.

| task | repo | cited sha(s) on main? | command |
|---|---|---|---|
| `019f6e94-5c6a` honesty fixes (cv) | cv | 66bec7b0 yes (cv main) | `cv task done 019f6e94-5c6a --observed "cv main 66bec7b0"` |
| `019f6eef-dc51` provenance freshness (cv) | cv | fd55d6d3 yes | `cv task done 019f6eef-dc51 --observed "cv main fd55d6d3"` |
| `019f6ef7-0455` TOFU per-worker creds (cv) | cv | 34c61847 yes | `cv task done 019f6ef7-0455 --observed "cv main 34c61847"` |
| `019f6ef7-0469` verifiable Done --check-cmd (cv) | cv | 970d0a71 yes | `cv task done 019f6ef7-0469 --observed "cv main 970d0a71"` |
| `019f6ef7-047c` harden saw_change (cv) | cv | 440e52b0 yes | `cv task done 019f6ef7-047c --observed "cv main 440e52b0"` |
| `019f6f36-7715` sesh ls --json gaps (cv) | cv | 4b3c602b yes | `cv task done 019f6f36-7715 --observed "cv main 4b3c602b"` |
| `01a0f52e-76fd` JOIN-SOLANA friend client + FRIENDS.md | minidregg | 243fb343, 408acb23 yes | `cv task done 01a0f52e-76fd --observed "mini origin/main 243fb343 408acb23"` |
| `01a0f63a-233a` STORE-OPEN O(history) | minidregg | 3df668ef, 16633f66, 7f5ea838 yes; the ≤60 s *measurement* belongs to THE BAR task | `cv task done 01a0f63a-233a --observed "light open 3df668ef + checkpoint v3 16633f66 on main; cold-reopen number measured under 01a0f9c0-521b"` |
| `01a10500-6f6f` OB compose/fix checks, final-self | minidregg | 1f595131, 0c1d6d58 yes | `cv task done 01a10500-6f6f --observed "mini origin/main 1f595131 0c1d6d58"` |
| `01a10500-f341` land+compile W2.F SPK v4 | minidregg | dd97fcc6, 374549d4, a183acf8 yes | `cv task done 01a10500-f341 --observed "mini origin/main dd97fcc6 374549d4 a183acf8"` |
| `01a10503-6c57` AgreementEvidenceRegime | minidregg | 493b2377, 95bfab2d yes | `cv task done 01a10503-6c57 --observed "mini origin/main 493b2377 95bfab2d"` |
| `01a10556-496e` Objective laws → sums, audit | minidregg | 66a54085, 6a6cbdda yes | `cv task done 01a10556-496e --observed "mini origin/main 66a54085 6a6cbdda"` |
| `01a1056f-0066` yielded activity responses + checkpoint | minidregg | 8194e09d, 7dd88709 yes | `cv task done 01a1056f-0066 --observed "mini origin/main 8194e09d 7dd88709"` |
| `01a105d4-4a7c` VERBNAME-PLACE Lean change | minidregg | 35508a6f yes | `cv task done 01a105d4-4a7c --observed "mini origin/main 35508a6f (same change as 01a0f72b-7dae)"` |
| `019f6e94-5c52` dogfood-loop scenarios | mission-control (phoenix-strip) | f28b5277 exists but NOT on that repo's main | keep open: `cv task note 019f6e94-5c52 "10-08 recheck: f28b5277 is on a phoenix-strip branch, not main"` |
| `019f6e98-0e41` G9 redact launch_argv | mission-control (phoenix-strip) | d5004d3f exists but NOT on main | keep open: `cv task note 019f6e98-0e41 "10-08 recheck: d5004d3f not on mission-control main"` |

## (B) The 141 other-project tasks

**READ** (`cv task show` over every row): 128 are `~/dev/don` (opened 08-11 by the DoN reverse-engineering
agents — `closure/opcode: AttackCommand`, `closure/group: repair`, … — untouched for 57–58 days), 7 are
`~/dev/cv`, 2 `~/dev/tokeman`, 1 `mission-control-worktrees/phoenix-strip`, plus #15 above. `~/dev/don` is
still an active repo (last commit 10-04 on `dev`), so these are a real backlog that belongs to *that* project,
not stale Mini work; abandoning 128 tasks you may want when you next open DoN would destroy a day of a swarm's
enumeration for no gain. **Recommend park, not abandon or move**: they are already partitioned by `repo`, so
the only thing needed is that Mini triage filters by repo (`cv task list --repo ~/dev/minidregg`) and the inbox
stops counting them. The one command that does it (tags every don row so any view can exclude `--tag parked`):

```
cv task list --all --repo /Users/ember/dev/don --tsv | cut -f1 | xargs -n1 -I{} cv task tag {} parked
```

If instead you are done with DoN: replace `tag {} parked` with `abandon {} --reason "don: parked project 10-08"`.
The 7 cv and 2 tokeman rows stay LIVE in their own repos (cv's `distill` work is current).
