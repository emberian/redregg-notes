burst3 (2026-10-08), project dregg (proj_jmlR57Ro4NWgY), team Lunar Town
host:      burst3-a   (ssh alias in ~/.ssh/burst3-20261008.conf; ssh ember@67.213.117.177)
server id: sv_BDXM5E4JzNrpk
plan:      f4-metal-medium (EPYC 4564P Zen5 4.5GHz, 16c/32 threads, 187G RAM, 2x480G + 2x1.9T NVMe), hourly
site:      LON2 (US out of stock for this plan; LON2 is where burst2 ran)
IP:        67.213.117.177
cost:      $1.52/h
tag:       burst3-20261008 = tag_WKWl1qg7Ovswq6lOprlocpBwQby ("burst3, KEEP through the reorient (Ember 10-09); review before 2026-10-15")
ssh key:   ssh_dmkONWq9oajL1 (Mac id_ed25519, same as burst2)
created:   ~2026-10-08T02:27Z
state:     burst-up --id burst3 at tip cfdaf64df8f869f5e45c86a85055457345fc5ae1; warm base FROZEN cfdaf64d (cold build 1023 s);
           burst-check 0 DIFF. 6 lane slots x 6 threads + 2 gate slots.
shared remote: /srv/git/minidregg.git seeded from GitHub (main/next/green) + all 441 refs/heads/lane/* (325 archive-*) from hbox burst2-minidregg.git (tips identical).
hbox puller: pull-burst3-remote.timer (10 min) -> /tank/dregg-build/claude-lanes/bundles/burst3-minidregg.git. burst2's timer left disabled.
script fixes: none needed (scripts used as-is from origin/main cfdaf64d).
