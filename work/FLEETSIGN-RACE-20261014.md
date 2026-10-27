# FLEETSIGN RACE: interleaved turns refused "remote challenge differs from locally prepared intent"

Measured on hbox (i9-12900, 24 threads) on 2026-10-14 at tip d37eee80. d37eee80 touches only perf/docs; its
parent is main 7dea0626, where fleetsign PASSED on burst3. Row `fleetsign` (native/resource-client/fleet-sign-journey.sh,
step J6 interleaved: three profiles alpha/bravo/charlie, sends and transfers in parallel):

- standing run 2026-10-14T07:09Z: FAIL, 1 turn (charlie 7 send)
- rerun 1: FAIL, 1 turn (bravo 4 transfer); rerun 2: FAIL, 3 turns (bravo 12/17/20)
- direct driver run kept here (run1/): FAIL, 3 turns (charlie 7 send, charlie 12 transfer, charlie 21 send)

Every failing turn has the same client stderr:
    mini: local consent refused before signing: remote challenge differs from locally prepared intent

## Where it comes from
Kernel/NativeClientConsent.lean:47-55. The client derives the challenge from ITS opened basis
(`NativeObservationController.challenge (observationContext config basis.opened) …`). If the Host's challenge bytes
are not byte-identical (`challengeCodec.encode challenge = candidate`), consent refuses. This is TERMINAL: there is no
supersede/replan. Under interleaving, other profiles' turns move the world between the client's basis open and the
Host's challenge (worldRoot, height, footprint values), so the Host's challenge is built over a newer state. My
inference, not yet verified at the byte level: this is a stale-basis CONTENTION and belongs on the replan path
(the driver already counts `superseded.json` reasons stale-root-at-plan / stale-root-at-observation / contention).
It is reported as a refusal instead. On burst3 the timing never opened the window.

## Evidence (run1/, test keys deleted; every key was generated inside the run)
- run1.err / run1.out: driver stderr/stdout.
- run1/evidence/interleaved.tsv: per-turn table. run1/evidence/interleaved/<profile>-<i>.json.stderr is each turn's client stderr.
- The failing turns' attempt directories, matched by mtime to the turn's stderr:
  - charlie-7  -> run1/fleet-home/profiles/charlie/workspace/attempts/a-323910352897738077485083538758214087380
  - charlie-12 -> …/attempts/a-254118261697985026363285262371405858863
  - charlie-21 -> …/attempts/a-42844422835207255431456106701190083920
  Each holds intent.json/.bin, intent-signature.bin, challenge.json/.bin (the REMOTE challenge), view.json/.bin,
  observation-signatures.*, attempt.json, config.json. It holds no signature and no outcome. challenge.intent equals
  the local intent (subject, nonce, purpose, grants), so the difference is in the observation context the challenge
  embeds (worldRoot, height, headers, signing[0].message/footprint), not in the intent.
- run1/fixture/public/serve*.log: the Mini server log. It prints only its socket and pid, so there is NO Host
  per-request trace; that is itself a gap for whoever owns this.
- Not kept: the client's own locally-derived challenge bytes. The refusal does not persist the candidate it
  compared against. Persisting it in the attempt dir (e.g. local-challenge.bin) on refusal would make the diff exact.

Reproduce: `bash native/resource-client/fleet-sign-journey.sh $SET/bin/{minidregg-host,mini,minidregg-link-sqlite-store,minidregg-credential-signature-verifier} RUN`
with SET=/tank/dregg-build/pipeline/artifacts/d37eee80fbb96c9afc3638ae18cc34d54cc1accb. 3 of 3 reproductions on hbox failed.
