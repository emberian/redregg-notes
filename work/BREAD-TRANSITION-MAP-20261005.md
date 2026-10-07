# BREAD-TRANSITION — every Bread PRODUCT capability, mapped onto Mini (2026-10-05)

Author: SCHOLAR-BREAD-META, for QUEST BREAD-TRANSITION (Ember: "mini is taking the crown and we want the
transition to be thorough… maybe it isn't time yet etc."). Products only; the metatheory is mapped in
`work/SCHOLAR-BREAD-METATHEORY-20261004.md`. Read-only over Bread (`/Users/ember/dev/breadstuffs`, "B");
Mini read at GitHub main `3b709c87` ("M"). Two Opus sub-readers took the census (Bread product status with
deployment and user evidence; Mini's current artifacts and evidence classes); I re-checked the headline
claims I rely on at source (the bounty-board escrow admission, `FLEET-SURFACE.md`, the market and commons
worlds, the preview harness) and marked the rest LANE.

**What this map adds, and what it does not redo.** `M/ATLAS.md` (08-06) is the Lean mining map and skips
games (§8.5); `work/scouts-20261003/R2-4-bread-mining-map.txt` maps nine Bread areas at the Lean/spec level
with a top-6 BRING (several of which have since LANDED: `Theory/CertF`, `Theory/ResearchRegime`,
`Kernel/AgreementEvidenceRegime`, `Theory/{Disputation,OptimisticAdjudication}`, `Kernel/GenericSimplexReconfig`,
`Theory/Bfv*` compiled but unimported); `work/scouts-20261003/G-product-journey-public-node.txt` maps Mini's
product journey; `M/docs/FLEET-SURFACE.md` maps the one Bread capability that had users. None of them is a
per-product census of what RAN or HAD USERS in Bread, with a Mini shape and a verdict under the program model
that landed on 10-04/05 (Core4 activities with answer slots and resume-with-view, seats and offer safety,
native Objective admission, the object record). That is this file.

Verdicts: **NOW** = an implementable lane today on main `3b709c87`; **SOON** = after a named Mini prerequisite
(lane names from `MERGE-QUEUE.md` and the design's §6 build plan); **LATER** = valuable, but needs something
not yet planned; **NEVER** = do not port (reason given).

---

## 0. Verdict

1. **Only one Bread capability ever had users, and it is already carried over.** Pug's agent fleet signed
   ~800 turns with `dregg-client-sign` on his homelab devnet (B/docs/REVIEW-pr72.md:315, 341;
   B/docs/OPERATOR-ONBOARDING.md:6); Mini's `mini fleet` / `Kernel/FleetTurn` is its built and measured
   counterpart (M/docs/FLEET-SURFACE.md, `docs/evidence/2026-09-30-fleet-surface/`). Every other public
   Bread surface (node.dregg.net, the Discord bot, the arcade and Telegram Mini App, the Path of Angels beta
   behind Basic Auth, one Base-Sepolia settlement with a fixture proof, one Mina Devnet zkApp, a kubo node)
   ran with **no evidenced users** and was torn down on 09-30 (LANE: B/docs/LIVE-SURFACE-TRUST.md:21-58;
   INF/edge/README.md:198-208; MEM/project-path-of-angels-platform.md). $DREGG has ~900–1700 holders and
   bought nothing in-protocol (HORIZONLOG:9995).
2. **So the transition is about IDEAS that make friends do real things, not about migrating anyone.** The
   ship target (a re-genesised public node with Objective, activities, seats, split tenancy and
   pay-to-enrol) is exactly the machinery Bread lacked for its best apps: Bread's bounty board could not hold
   its own reward (B/starbridge-apps/bounty-board/src/lib.rs, "the reward is a PROMISE, not an escrow"), its
   DrEX cleared in a client, and its long-running work lived outside the kernel. Mini's seats + activities
   are what those apps were missing.
3. **NOW, ranked:** (1) the bounty board (implemented, §6); (2) standing dues/subscriptions for rooms;
   (3) a sealed-ballot (commit/reveal) vote; (4) a two-party commit/reveal game; (5) the co-authored story;
   (6) Pug's fleet onboarding kit; (7) a world-cohort gate row. Everything with money in it is preview-level
   NOW and native SOON after OBJECT-RECORD (R2) + SEATS-NATIVE + the activity native route.
4. **SOON:** DrEX as seats + Cert-F (after SEATS-NATIVE), cards for every package (after L12),
   governed namespaces and protocol-object workflows (after L8/L10), Hermes in a room on the node (after
   DEPLOY-3B + providers), the Discord entrance (after Ember's Discord app), scoped-grant agent mandates
   (after L5/L6).
5. **NEVER:** the deos-js/SpiderMonkey applet host, starbridge-v2 cockpit code, CapTP swiss numbers inside a
   domain, the shielded pool as built, the four light-client AIRs, Pickles-in-Lean as a verifier claim,
   the launchpad, the dreggnet-* game crates, Matrix, orb, durable-workflow/pg-dregg. Reasons in §4.

---

## 1. NOW, ranked by value to the ship target

Each is an `.obend` package (or a small client/gate piece) that runs TODAY in the effect-free preview, with a
named native path that becomes executable when the SOON prerequisite lands. "Friends do real things" is the
ranking criterion: money with a guarantee first, then coordination, then play.

### N1. Bounty board with a real escrow — IMPLEMENTED (§6)
- **Bread:** `starbridge-apps/bounty-board` (seeded at genesis, B/node/src/starbridge_seed.rs:479-490; RAN on
  the solo node, no users). Lifecycle open → claimed → submitted → paid, first claimer wins, reward
  write-once. Its own header: the bounty cell cannot hold the reward ("StrictMonotonic(STATE) … a Transfer
  whose `from` is not the action's target requires … `AuthRequired::None` … no common solution"), so the
  poster pays at payout time from its own balance — a poster could take the work and never pay.
- **Mini shape:** `world/bounty/BountyBoard.obend` + `world/bounty/preview-cohort.json` (lane bread-meta,
  `183c75ae`). The reward leaves escrow exactly once, whole, to exactly one party; silence past the review
  window pays the claimant; cancel only while unclaimed; expiry refunds an unclaimed or unsubmitted bounty.
- **Native path (SOON):** a seat per bounty (give = reward, want = approved work or the reward back, exit
  at the deadline: `Kernel/Seat.lean` `seat_offer_safe_forever`, `exit_enabled`, landed in `3b709c87`); the
  poster's decision is an answer slot (decider = poster, deadline = review end); the disbursement is the
  seat's payout. Prerequisites: OBJECT-RECORD R2 (queued), SEATS-NATIVE, the activity native route.

### N2. Standing dues and subscriptions (rooms that pay for themselves)
- **Bread:** `Deos/StandingObligation.lean` (`cursorAt t k := t.start + k * t.period`; `cursor_strict_mono`,
  `replay_rejected`, `behind_schedule_rejected`), `Deos/PrepaidLease.lean` (meter and draw fused in one
  write), `starbridge-apps/subscription` (seeded at genesis). TESTED; Lean over a 1-felt heap root (META §9.5).
- **Mini shape now:** nothing; pay-to-enrol is 50 DREGG/week (`deploy/pay/enrol-terms.json`) but there is no
  recurring obligation object.
- **Lane seed (NOW):** `world/dues/StandingDues.obend` + cohort: an Activity that awaits `height{at: next}`,
  writes `cursor := add 1` and proposes one `pay{from payer seat, to room purse, amount}` per period; skips
  are refused, catching up pays each missed period once; cancellation by the payer only at a period
  boundary; a prepaid lease variant draws from a seat. Acceptance: cohort rows for on-time, late catch-up
  (k periods → k payments, never k+1), double-trigger refused, cancel mid-period refused; one mutation
  (drop the cursor check) turns a row red. Native SOON after the activity route (height awaits exist).

### N3. Sealed-ballot vote (commit/reveal) for rooms
- **Bread:** `starbridge-apps/privacy-voting` (seeded), `collective-choice` (1.8K), Polis apps; TESTED.
- **Mini shape now:** `world/collective/CollectiveAdoption.obend` (unique ballot, absolute-YES quorum; preview
  42 rows; ballots are public) and `Kernel/SealedMarket.lean` (commit/reveal pattern, compiled).
- **Lane seed:** extend CollectiveAdoption with a commit phase (`commit{voter, digest}`) and a reveal phase
  (`reveal{voter, choice, salt}` checked against the digest), tally at the reveal deadline; unrevealed
  commits count as abstain; a result is published with the ResearchRegime label `ballot` (never rendered as
  witness: `Theory/ResearchRegime.lean` `Publication.honest`). Acceptance: rows for honest reveal, mismatched
  reveal refused, double commit refused, late reveal refused, quorum not met; a mutation that skips the
  digest check turns a row red.

### N4. Two-party commit/reveal game (friends play without trusting each other)
- **Bread:** `dice` (drand; RAN inside Descent, fell back to a pinned round, LIVE-SURFACE:37), the
  dreggnet arcade, automatafl (verified, no players).
- **Lane seed:** `world/play/CommitReveal.obend`: rock-paper-scissors / coin-flip with a stake held in a seat
  per player, commit then reveal, forfeit on reveal timeout (the non-revealer's stake goes to the other).
  Same shape as N3 with money; the cheapest demonstration that a game on Mini cannot be won by walking away.
  Native SOON with N1.

### N5. Co-authored story (crowd-voted branches)
- **Bread:** `spween-dregg` (8.2K), `narrator` (2.8K, $20 cap), `interactive-fiction-demo`; RAN locally
  (B/GOAL-COLLECTIVE-FICTION-DEMO.md:3-6). R2-4 calls it a product spec.
- **Mini shape now:** hyperdocuments with transclusion and backlinks (main), ballots (N3), the station world.
- **Lane seed:** `world/story/CoAuthor.obend`: a story object whose next passage is chosen by a ballot among
  proposed passages (each a hyperdocument link), one round per height window; the chosen passage is
  appended by the activity. Acceptance: rows for a three-round story, a tie rule, a late proposal refused.

### N6. Pug's fleet onboarding kit
- **Bread:** the only users (§0). **Mini:** `mini fleet` built and measured (FLEET-SURFACE), not on the node.
- **Lane seed:** a one-page migration guide plus a shim mapping each `dregg-client-sign` subcommand Pug's
  agents call (join, send, transfer, receipt by hash/head, topic publish/poll) to `mini fleet`, with a
  recorded run against a scratch world. Acceptance: Pug's own command transcript (from his fork) replays
  through the shim with every call answered. Deploy SOON after DEPLOY-3B + re-genesis.

### N7. A gate row for world cohorts
- No gate runs `world/*/preview-cohort.json` today (`scripts/check-objective-frontend.sh` runs only
  `tests/objective-bend-source/preview-cohort.json`). Market (196), commons (64), collective (42), station
  (36), workshop (44) and bounty (19) rows are evidence only on the day a lane ran them. Seed: add a
  `world-cohorts` row to `check-objective-frontend.sh` that runs every `world/*/preview-cohort.json` through
  `check-preview.ts`; acceptance: one planted wrong `expected` turns the row red.

---

## 2. SOON (after a named Mini prerequisite)

| item | Bread (status) | Mini now | prerequisite | lane seed |
|---|---|---|---|---|
| **DrEX as seats + Cert-F** | drex-web(-v2) + `intent` `drex_clear` ring solver, RAN privately on hbox :8781 (DEVNET-DEPLOYMENT-REALITY:30-52); clearing computed client-side; SetField allocation unprovable at the deployed VK | `world/market/*.obend` (preview, 196 rows), `Kernel/SealedMarket`, `Kernel/CanonicalEscrowMarket` (compiled), `Theory/CertF` (compiled, unconsumed) | SEATS-NATIVE | each order a seat (give/want with limit price); a batch activity awaits the window, an untrusted clearer proposes a uniform-price allocation **with a Cert-F certificate**, the law checks `certifies_epsilon_optimal` and every seat's `offerSafe`; refuse on gap > ε. Acceptance: a two-sided batch settles natively; a crossed-but-suboptimal allocation is refused by the certificate check |
| **Cards for every package** (deos affordances, HIG) | deos-js applets + cards (TESTED); affordance algebra (META §9.1) | `can NAME`, `mini web`, Studio (lane-only) | L12 presentation | `Host/ObjectProjection`: Hidden / Disabled(reason) / Possible / Enabled per affordance, preview and commit gates one function; first cards: bounty, dues, ballot |
| **Counter applet family** | deos-js counter (attach.rs:112), todo/poll siblings | `tests/objective-bend-source/DeosCounter.obend` (authored) | L12 + OBJECT-RECORD | promote DeosCounter to `world/applets/` with a card; the reset requirement stays the object's law |
| **Governed namespace / constitutional amendments** | starbridge-apps governed-namespace (seeded), polis app (M-of-N + cooling), Lean Polis | CollectiveAdoption (preview), `ObjectRecord.UpgradePolicy` (queued R1/R2) | L10 upgrade | an amendment is an ADOPT turn whose new law must entail the frozen floors (decided, certificate) and whose authorization is a ballot result labelled `ballot` |
| **Workflow mandates** (compartment-workflow-mandate, agent-orchestration) | seeded / TESTED; Mandate budget never enforced (META §6.5) | none | L8 protocol objects, L5 `call`, scoped grants | a protocol object whose residual global type is the workflow; scoped grants cap each worker's spend in the Book |
| **Hermes in a room on the node** | deos-hermes (24K; reported commands it never ran, CS #14) | AgentGrain, J14 PASS with a scripted provider; off on the node | DEPLOY-3B + Ember's providers | turn on J14 on the node with one real provider; every tool call a metered turn with a receipt the model is shown verbatim |
| **Discord entrance** | discord-bot (78.7K; RAN publicly, custodial clerks from `BOT_SECRET`, no users) | `native/discord-entrance` (30 tests vs a fake Discord) | Ember's Discord app | ship the entrance; NEVER port custodial clerks |
| **Equivocation evidence as a witnessed atom** | `federation/src/court.rs` (547) | Simplex safety compiled; fault attribution absent | AGREEMENT landed; L14 | a Simplex fault record (two conflicting signed votes) as a typed evidence object, labelled witness |
| **Verifiable randomness** | dice/drand (RAN in Descent) | none | an observation source (pay-watcher pattern) | a drand-round observation cell; games prefer commit/reveal (N4) until then |
| **Time travel / branch-and-stitch for residents** | `turn/src/reversible.rs` Clean/Contextual/Committed (TESTED, round trip unproved), stitch_pair | checkpoint codec exact; no undo | L10 + L12 | reversibility tier per Plan action (total match), proved round trip for Clean/Contextual; fork-a-world as a confined branch, stitch evaluated at the settlement tip |

## 3. Full capability table (everything that ran, had users, or was designed with intent)

Status tags (Bread): **USERS** · **RAN** (public or private deployment evidence) · **TESTED** · **DESIGNED**.
Mini evidence classes: authored / compiled / executed / integrated / deployed.

| capability | Bread (status; key evidence) | Mini shape now | verdict |
|---|---|---|---|
| Agent fleet SDK (`dregg-client-sign`, sdk 63.5K) | **USERS** (Pug, ~800 turns) | `mini fleet`, `Kernel/FleetTurn` (executed, measured) | **NOW** N6 (onboarding kit) |
| SDKs (sdk-ts, sdk-py, dregg-sdk-net) | TESTED; npm/PyPI never published | `native/mini-sdk` (Rust/wasm), `mini-sdk-ts`, intent bytes from Lean (executed) | absorbed |
| Cipherclerk (sdk/src/cipherclerk.rs 10K; MV3 extension 73K; node `/cipherclerk/unlock`) | RAN (custodial unlock on the edge; Discord clerks from `BOT_SECRET`) | `docs/CLIENT-SIGNING-CONSENT.md`, mini-sdk explain→confirm→sign | absorbed (signing); **LATER** browser extension (after a Studio route); **NEVER** custodial clerks |
| Bounty board | RAN (seeded), reward a promise | `world/bounty` (executed, preview) | **NOW** N1 done; native SOON |
| Subscription / standing obligation / prepaid lease | RAN (subscription seeded); Lean TESTED | none | **NOW** N2 |
| Privacy voting / collective choice / Polis app | TESTED; Polis "one theorem" a shape identity | CollectiveAdoption (preview) | **NOW** N3; Polis code **NEVER** |
| Nameservice / identity | RAN (seeded) | `docs/SHARED-NAMES.md`, credential authority (compiled/executed) | absorbed |
| Escrow / vault / allowance / obligation / queue factories | TESTED (FactoryProbes) | seats, Book, rooms; streams (`Compiler/StreamCell`) | absorbed by seats + streams; allowance as scoped grants SOON |
| Storage-gateway mandate | RAN (seeded) | fn archive, durable store | **NEVER** (fn and the durable store cover it) |
| DrEX web + ring solver | RAN privately (hbox :8781) | market worlds (preview), SealedMarket, CertF | **SOON** (seats + Cert-F); drex-web UI **NEVER** |
| fhEgg FHE clearing / dark AMM / dark bazaar | TESTED; attribution not computation integrity | `Theory/Bfv*` compiled, unimported; `native/private-backend` MPC research | **LATER** (needs Selvage or MPC at admission); PoA Bazaar was NO-SHIP |
| Launchpad (DreggLaunchpad.sol, launchpad-web) | TESTED (anvil 29/29); innerHTML XSS (CS #16); never broadcast | none | **NEVER** (securities exposure, no users; a sealed-bid batch is DrEX SOON) |
| $DREGG | external memecoin; ~900–1700 holders | pay-watcher reads finalized SPL transfers (fixtures) | absorbed as the enrol currency; pay-to-enrol ships with DEPLOY-3B |
| Payments: dregg-pay, Payable DSI | TESTED; zero real $DREGG accepted | Book, PayEnrol*, pay-watcher (executed with fixtures) | absorbed |
| Stripe mirror / DECO / TLSN money-in | TESTED; notary semi-honest | none | **LATER** (fiat on-ramp after the node has friends) |
| x402 | DESIGNED | none | **LATER** (pay-per-call face for Hermes/commons services) |
| TEE produce/verify, zkOracle | TESTED; SNP ignores guest policy (CS #2) | none | **LATER**; never in admission |
| deos-js (SpiderMonkey) + deos-js-runtime (boa) applets | TESTED / ran locally | `.obend` packages + preview | **NEVER** the JS host (two engines, unchecked authority, nondeterminism; META §2.3); the applet IDEA lives as packages + cards (SOON) |
| deos-view / leptos / web-cells / starbridge-web-surface | TESTED (render bakes) | `mini web` (main), Studio (lane-only) | **NEVER** the code; HIG + affordance algebra into L12 |
| deos-terminal (pty_ws) | TESTED; WebSocket handshake gates a shell (CS #4) | `mini` shell over ssh roster | **NEVER** |
| deos-matrix / deos-homeserver | TESTED (boots) | native chat in rooms | **NEVER** |
| deos-zed / zed-full | ran in the cockpit; remove_file no-op | Studio source workspace | **LATER** (editor integration after Studio routes) |
| starbridge-v2 cockpit, seL4, Android | RAN locally; root-by-header authorization (CS 14 F1) | Studio, website | **NEVER** the code; desktop shell **LATER** |
| Hyperdocuments / transclusion / DocMerge | TESTED | hyperdocuments, transclusion, backlinks, merge (main; doc verbs deployed) | absorbed; DocMerge conflict-as-state where Mini's merge lacks it SOON with L12 |
| Hermes (deos-hermes), dreggnet-hermes | TESTED; one live Copilot run | AgentGrain, J14 (executed, scripted provider) | **SOON** |
| Agents / confinement (dregg-agent, demo-agent, agent-host, agent-platform, confined-swarm) | TESTED | grains, tenancy B (mini-keys), AgentGrain | absorbed; forkable confined session **LATER** |
| MCP (node 54 tools; dregg-mcp 22) | TESTED | M5 "Hermes via MCP" (grain-runtime MCP tools) | absorbed |
| Grains / Sandstorm | TESTED; Mini pins Bread's sandstorm-package | spk-host, spk-rpc, grain-runtime (integrated on dev worlds) | absorbed |
| Blocklace / federation / coord / CapTP / net / wire | RAN (node.dregg.net solo; PoA 3-of-3 then 1) | Generic Simplex (executed 4-node), joint agreement, LaceMerge | absorbed; CapTP sturdy refs/swiss inside a domain **NEVER**; interfederation **LATER** (L14) |
| 2PC (`/turn/atomic`, Lean verdict) | RAN (Lean-decided on the node) | joint reservation/agreement | absorbed; cross-domain deals L14 **LATER** |
| Stingray bounded counters | RAN (node state) | escrow quotas in the design (F) | **SOON** with L9 parallel admission |
| Shielded pool / encrypted turns | TESTED; value never entered the pool; ∃-image vacuous; `claimed_nonce`/`min_fee` compared to nothing (CS #23) | private rooms (compiled, KAT), `Compiler/NoteSpend` (own work) | **NEVER** as built; private value **LATER** after Selvage reaches admission |
| Mina zkApp + Pickles/Kimchi in Lean | RAN on Mina Devnet (block 539534); placeholder Schnorr; deployed VK ≠ source VK | none (docs/PROOF-SYSTEM-SURVEY.md) | **NEVER** for now (no proof system in admission; Pickles-in-Lean is a differential, R2-4) |
| EVM settlement + ETH/Base light client | RAN once (Base-Sepolia, fixture proof) | EVM fragment (Stage-0), no bridge | **NEVER** the AIRs (vacuous folds); bridges **LATER** |
| Solana / Cosmos locks + settlement | TESTED; replay holes (CS bridges) | pay-watcher (finalized reads) | **NEVER** the locks; mine `sol_no_forgery` (R2-4) into the watcher's finality rule if it ever verifies votes itself |
| Midnight bridge, Stripe mirror (bridge/ 48K) | TESTED, mock observer | none | **LATER** |
| Path of Angels (poa-web 30K, poa-curator, node/src/poa_*, Lean Games/PathOfAngels 86.7K) | RAN behind Basic Auth 08-03→09-30; no players; node stale with `healthy:true` | none; `world/station` is the nearest content line | **LATER** as content for Sentyr if he returns; the code **NEVER** |
| Galley (PoA maintenance organ) | TESTED, trusted-host beta | none | **NEVER** |
| Discord bot | RAN publicly, no users | discord-entrance (executed vs fake) | **SOON** (entrance); bot code **NEVER** |
| Telegram Mini App / WeChat | RAN (arcade.dregg.net/tg), retired | none | **LATER** (a second entrance after Discord) |
| dreggnet-* games, arcade, Descent, MUD | RAN (funnel/arcade/dregg.gg), torn down; self-asserted cookie identity | FRIENDS.md lists Descent/MUD as plans | **NOW** N4 (commit/reveal play); the crates **NEVER**; Descent **LATER** as a package family |
| automatafl (verified 11×11 game) | TESTED (one 1663 s fold) | none | **LATER** as an `.obend` game (rules as law, no AIR) |
| Fiction stack (spween, narrator, IF demo) | RAN locally | none | **NOW** N5 |
| Storage / IPFS | IPFS RAN (kubo on hbox); rest TESTED | fn archive, durable store, portable archive | absorbed |
| durable-workflow / pg-dregg | TESTED | activities (Core4) | **NEVER** (activities are the durable workflow) |
| orb (in-repo engine) | TESTED; ship gate passes on failure (CS #9) | none | **NEVER** here |
| web-studio, site/ | prototype / RAN (Pages) | Studio, website (deployed Pages) | absorbed |
| ResearchRegime display rule | DESIGNED/proved | `Theory/ResearchRegime` compiled (ResearchWip) | **SOON**: render every badge through it with L12 |

## 4. NEVER, with the reasons that make them NEVER (not "later")

- **deos-js / boa applets, starbridge-v2, web-surface code:** authority asserted by the client
  (`x-dregg-held-rights: root`), two engines disagreeing on the fire contract, `Math.random`/`Date` live,
  per-process private ledgers (R2-4 (7); META §2.3 of the first report). Mini's re-executed packages remove
  every cause; the code would bring them back.
- **CapTP swiss numbers and sturdy refs inside a domain:** Mini's kernel holds capabilities; bearer secrets
  inside a domain are a regression. Cross-domain references are L14.
- **The shielded pool as built:** the pool never held value; its key predicate was ∃-image vacuous
  (MEM/project-shielded-apex-campaign.md); private value waits for a proof system Mini owns.
- **Light-client AIRs, Pickles-in-Lean as a verifier, the Mina zkApp:** hash-fold theorems vacuous at
  deployed width; no proof system in Mini admission (10-01 decision).
- **Launchpad:** never broadcast, an XSS on the token page, and a token-sale surface is not a friends
  product.
- **dreggnet-* crates, Galley, poa code:** self-asserted identity, replay-not-proof, no players; their
  content can return as packages.
- **Matrix/homeserver, orb, durable-workflow, pg-dregg, deos-terminal:** each is replaced by a Mini native
  (rooms, the Host, activities, the shell) or is a liability (pty over WebSocket).

## 5. What Mini's last day changed in older maps

- **G (product journey)** maps DrEX, collective adoption and co-authoring to `world/Workshop/*.bend` on the
  Gen-1 path; Gen-1 and BendTT are deleted (ledger), the live forms are `world/*/…obend` in preview.
- **R2-4 top-6:** #1 ResearchRegime chain and #4 Cert-F LANDED (compiled, research targets); #3 Bfv compiled
  but not imported; #6 Simplex reconfiguration LANDED as `Kernel/GenericSimplexReconfig`. Their consumers
  are the SOON rows above (badges in L12; Cert-F in DrEX-as-seats).
- **Activities replace three Bread mechanisms at once:** the pending registry, conditional turns and the
  durable-workflow crate. Every Bread "await X then do Y" product maps to an activity with an answer slot or
  a height await, resumed with a view (RESUME-WITH-VIEW landed).
- **Seats replace Bread's escrow/obligation verb families and its promise-only payouts.** Any Bread app that
  moved value on an outcome (bounty, trade, sealed auction, lending) is a seat now.
- **Native Objective admission** means a package's method runs at admission from its pinned source; Bread's
  client-computed effects (META first report §0) have no Mini analogue to port.
- **The object record** (queued R2) is the precondition for every native row above: no activity birth or
  state write without a created object and its law.

## 6. What I implemented

`world/bounty/BountyBoard.obend` and `world/bounty/preview-cohort.json`, commit **`183c75ae`** on persvati lane
`bread-meta` (`/home/ember/workbox/claude-lanes/bread-meta/src`, on main `3b709c87`), queued in
`MERGE-QUEUE.md` (`bread-meta-bounty`).
- Two layers, as in `world/commons`: pure transitions over `State = open | claimed | submitted | paid |
  refunded` with an escrow law `escrowConserved` (escrow holds the whole reward until one disbursement pays it
  whole to one party), and an Activity `bounty(p)` that yields `await{phase, deadline}` and
  `disburse{to, amount}` Plans and is resumed with typed events (`claim`, `submit`, `approve`, `reject`,
  `cancel`, `expire`) or kernel acknowledgements (`settled`, `refused`).
- Evidence **executed** (effect-free preview): 19/19 rows through `tests/objective-bend-source/check-preview.ts`
  (12 closed checks including `escrowLawHolds`, `firstClaimerWins`, `silencePays`, `posterCannotClaim`;
  6 activity runs ending `paid` or `refunded` with the last Plan pinned; 1 run stopped at the review await).
  Teeth: a claim-stealing mutation turns 2 rows red; paying `reward + 1` turns 6 rows red (lane
  `logs/mut.err`, `logs/mut2.err`).
- Not native: no seat is opened and no Book posting is made; that is SOON (N1 native path).

Also on the same lane, from the review quest: **`901422b3`** (`Kernel/ObjectiveResumeContract`: a delivery
advances the record one generation; `second_delivery_refused`'s premise is an `awaitId` collision), queued as
`bread-meta-resume`.
