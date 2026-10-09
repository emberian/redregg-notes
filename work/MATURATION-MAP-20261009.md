# MATURATION MAP — 2026-10-09: what got built, what it must grow into, and the row that proves it

Frame (Ember 10-08): each thing passed once as a script; "fungus" it into a general capability other parts of the system use,
with a standing row as the proof and a planted fault showing the row can go red. Repair & recover first, maturation second,
intertwining third. main = 1c7e46da (kern landed). MEASURED unless marked INFERRED.

## 1. Inventory: built thing → state at main → the seam it must join → proof row → next step
| built | state at main | seam | proof row | next step |
|---|---|---|---|---|
| OB semantics (laws, grants, domains, upgrade turns) | landed; theorems over the OB model; R0–R2 join to `World.admit` landed (CheckedCommit, totality 422/422) | FD-1 (the Host's state IS a World); R3+ held behind the collision/trie rework | objective, call, send, domain, objectrecord, upgrade: PASS | FD-1 after the trie work; not before DEPLOYABLE-1 |
| Store light open / verify-at-use | landed; flat ~40 ms past-state reads | BIRTHS are linear in cell count (36.7 s/create @1000 after the partial root-cache fix; a second Θ(cells) host term + client full-root rebuild remain) | growth row measures UPDATES (p99 2.2 s) — NOT the bar; a BIRTHS row is absent | add the births row (the honest bar), finish the host cache, add the client cache; cv 01a11e1b-0adc |
| Clock v2 (flag day landed) | genesis needs `clock.genesisNow`; drivers behind | every driver's genesis | jpay2–4, welcomecontinuity, sshe2e: RED on missing genesisNow | one fill-at-init helper for every driver (lane/snap-prod-rowfix 3ad3a35d has a draft) |
| Derived StoreEpoch | on lane/train-prod 5019da6a, not main | old Store refused BY EPOCH | hostupgrade-EF: RED on main, PASS on 5019da6a | re-pin the 3 pin reds, merge; union with kern's PersistedCodecTags entries |
| SPK unprivileged broker + root helper | landed (per-store units) | §8: the powerbox IS OB grants; R7 retry subsumed by OB upgrade turns | m6grain: RED (needs GRAINS_ROOT) | set GRAINS_ROOT in the row; then §8 P1 after DEPLOYABLE-1 |
| Hermes, deterministic ACP peer | row PASS; SIGKILL recovery proven | LIVE Hermes: real inference + BYOK (salvaged 10-02 branches 4d0810f2 / ff96355d, old base) + Ember's providers.json + per-friend controller.json | HERMES-LIVE row: ABSENT | Ember supplies providers.json; rebase the salvage onto main (astra); write the row |
| Pay (devnet Token-2022, fixture rail) | JPAY1 PASS; 2–4 clock fallout; 6 needs TEST_PROVIDER | DEPLOY-4 devnet rehearsal | jpay: partial | genesisNow helper; TEST_PROVIDER into the service env |
| Fleet (m8, fleet-sign) | PASS | — | m8, fleetsign | keep green |
| fn exchange | row UNCONFIGURED (MINI_FN_LAUNCHER missing from the service env); fn builds 6679dae0e + qualified 4b22a49bc staged at /srv/fnbin | the runner box hosts a local fn node | exchange | set MINI_FN_LAUNCHER; re-pin dev to 4b22a49bc; production stays d420a2b5 |
| M7 reproducible candidate | manifest v2 + run.sh verify landed | a reference set per tip | m7: UNCONFIGURED (M7_REFERENCE) | publish the reference set with each artifact set |
| Host-upgrade journey | landed (`run.sh upgrade`) | derived epoch | hostupgrade: EF red, FG pass | lands with the epoch range |
| Certifier unit (public node) | dregg-infra `edge/mini-certify` 7c28bf7, unpushed | DEPLOY-3 prerequisite (the Store refuses past certified+256) | jcertify 320 records PASS; no-certifier plant red at 257 | EMBER pushes; include in the DEPLOY-3 candidate |
| DEPLOY-3 | rehearsed 67/67 on an Oct-1 candidate; never shipped; public node at 5688775a | needs a DEPLOYABLE main + clock v2 params + certifier + the dregg-infra WIP split (RustDesk/ignore_changes = Ember's call) | J-DEPLOY3 on the candidate, then the public journey | rehearse on scratch with the DEPLOYABLE sha, then Ember's go |
| Docuverse / hyperdocument | modules landed; no standing row | agentwiki (set aside) | none | later |
| Mutation sweep | 214 build-green survivors, journey verdicts never run (cv 01a11dec-a55d) | assurance of everything above | none | compute-only filler for idle boxes |
| Ledger/pins | admitted by attribution; 1/3 of commits are re-emits | pins that measure meaning | — | after DEPLOYABLE-1: derive persisted shapes from one source (the software rethink) |
| Runner / gate / hub on the box | runner reinstalled from main by hand; hub at f5f5bbf, logging | execute-from-tip (PROTOCOL §7) | drift row on the dashboard | the first infra item |

## 2. The path to DEPLOYABLE-1, in order (each step = one row turning green; nothing starts before its predecessor's red is pasted)
1. INSTRUMENTS: runner/gate/mk-lane execute from the tip; `scripts/dashboard`; the BIRTHS row (so the bar is measured honestly).
2. CLOCK FALLOUT: the genesisNow helper → jpay2–4, welcomecontinuity, sshe2e green. (one Sol worker)
3. EPOCH: re-pin + merge 5019da6a → hostupgrade green. (one Sol worker)
4. INPUTS: GRAINS_ROOT, M7_REFERENCE, MINI_FN_LAUNCHER, TEST_PROVIDER into the service env → m6grain, m7, exchange, JPAY6 run and go green or name a real red.
5. THE BAR: finish the host root cache, add the client cache, prove the per-create bound → births row green. (astra; the hard one)
6. HERMES LIVE: Ember's providers.json; salvage branches rebased; HERMES-LIVE row green. (astra)
7. DEPLOY-3: certifier pushed, WIP split decided, candidate built from the DEPLOYABLE sha, J-DEPLOY3 on scratch, ship with Ember's go, public journey green.
After 7: §8 powerbox (SPK×OB), FD-1 (OB×World), mutation kills, ledger-from-one-source. That is the maturation proper.

## 3. Required rows for DEPLOYABLE-1
activity · seats · call · send · domain · objectrecord · upgrade · chargedfailure · rooms · bounty · journey J0–J8 · rotation/audit · welcomecontinuity · sshe2e · m3 · m4 · hermes · HERMES-LIVE · m6grain · m7 · m8 · fleetsign · jpay1–6 · exchange · hostupgrade · BIRTHS (the bar) · jcertify.
