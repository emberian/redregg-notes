# persvati (Ember's laptop) disk, 2026-10-05 ~00:15 — for Ember's decision; nothing deleted by the root
`/`: 1.9T, 121G free (94%); mk-lane floor is 120G. All Mini builds moved to hbox at 00:12, so nothing new should be written here.
Largest swarm lane dirs under /home/ember/workbox/claude-lanes (du; inflated by hardlinks to persvati-base's .lake/packages, so
real reclaim per lane is smaller):
 28G persvati-base (KEEP: the warm base)      15G schema-v2 (landed)       15G elaborator (landed)     15G agreement (landed)
 14G pn-fixture                               13G rollup-2 (queued; warm in case of bounce)            13G ob-roadmap (queued; warm)
 13G native-exercise (landed)                 12G ob-ltuo-2 (queued; warm)  12G native-exercise-2 (queued)
 12G fn-wire (landed)                         12G activity-native-2r (landed) 12G activity-native (landed)
 11G resume-view (landed)                     11G activity-native-gc
Candidates if you want space back: the .lake/build dirs of LANDED lanes (schema-v2, elaborator, agreement, native-exercise,
fn-wire, activity-native*, resume-view); every branch is on GitHub main or in bundles/. Your call.

## hbox, ~05:10Z (KEEPER-NIGHT report; root deleted nothing)
- ZFS `tank` SPECIAL vdev (nvme0n1p3, 13.6G, single/unmirrored) is 100% FULL -> small blocks + metadata spill to the 2x3TB HDD
  mirror; tank 87% used; IO pressure 55-70% full stall. Writers today: fn proof_artifacts.py/certs.py on /tank/fn, a du of
  ~/dregg-build/evidence, Mini gate builds. Mini's gate moved to ONE clone on rpool (/home, NVMe, ~129G free) per root approval.
- persvati fell to 119G (under the 120G floor) with no Mini writes since 00:12 (fn certifies or something else is writing).
Decisions for Ember: whether to free special-vdev/tank space, and what to clear on persvati (ranked list above).
