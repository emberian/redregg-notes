latitude-burst2-20261006: the hand-run provisioning of burst2-a/b (2026-10-07). SUPERSEDED on 10-07 by the repo's
scripts/burst/ (minidregg, lane/coord-audit-2 -> next): `burst-up` takes fresh Ubuntu boxes to the full current state
(packages, user, swarm-build, slots sized from nproc/RAM, sccache, pipeline scripts, persistent units, shared remote,
peer/mirror/hbox-puller keys, warm base by relay, briefs), `burst-check` diffs a box against that promise, `burst-down`
mirrors everything to hbox. bootstrap.sh / cold-build.sh / make-warm-base.sh / relay-b2.sh here are kept as the record
of what was run; do not run them for a new burst. mk-lane.sh here is a copy of the repo's (see README-mk-lane.txt).
