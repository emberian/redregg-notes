# Mini MERGE QUEUE (owner: lane MERGE-KEEPER, from 2026-10-04 ~10:50 EDT)

GitHub emberian/minidregg `main` is landed ONLY by MERGE-KEEPER. Root and lanes APPEND a request line
under REQUESTS; MERGE-KEEPER processes in order, rebases onto main, runs the POST-MERGE gate on a warm
copy, fast-forwards GitHub main, advances both warm bases, and records CI.

Request line format (one line, append at the bottom of REQUESTS):
  - [QUEUED] <lane> | <host>:<repo path> <branch> | <base>..<tip> (or commit list) | requester | notes
States: QUEUED -> TAKEN -> GATING -> LANDED <main sha> CI <run id> <result>  |  BOUNCED <reason, hunk/log path>

POST-MERGE gate (all on one warm copy at the rebased tip):
  lake build Minidregg +Host.Main:leanArts ObjectiveProofs; scripts/check-host-closure.sh;
  scripts/check-import-boundary.sh; scripts/check-proof-hygiene.sh; python3 scripts/lean-build-surfaces.py check;
  scripts/check-objective-proofs.sh; touched Rust rows of scripts/check-rust-tests.sh (filtered).

## MAIN / BASES
- GitHub main: 36fca3ac (at queue creation)
- persvati base (/home/ember/workbox/claude-lanes/persvati-base): see FROZEN
- hbox base (/tank/dregg-build/claude-lanes/warm-base): see FROZEN

## REQUESTS
- deploy3 | hbox:/tank/dregg-build/claude-lanes/deploy3/landable branch lane/deploy3 | b374fee3, 3ba7b139 (on 36fca3ac; deploy/candidate only: one Rust role list incl. mini-keys/mini-spk-broker/spk-hostd, keys role required; consent build refuses only on compiled-input change; test-package.py 13 ok, test-lane-build.sh 4 ok) | root | QUEUED

## LOG
