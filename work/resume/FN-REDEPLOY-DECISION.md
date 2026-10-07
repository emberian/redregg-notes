# fn public-node redeploy: decision for Ember (root summary; nothing executed)
Packet: /Users/ember/dev/fn/build/coordinator/REDEPLOY-PACKET.md (section 6 filled); gates: REDEPLOY-GATES-ANSWER.md.
Release fn 6.6.1-pre, REV 90393a5c, tarball sha256 e8e43551…d6ac (hbox:/tank/fn/scratch/redeploy-rehearsal/out/), ACL2 production
image, floor OpenSSL 3.5.8 (glibc <= 2.36).
Rehearsal R1-R11 GREEN: init within the 2G budget (reservation 1569 MB, heap 1094 MB; no MemoryMax change); hybrid PQ TLS
negotiated, cleartext AUTHINFO refused (483); kill -9 recovery kept the post; peering both directions; rollback to the old node
clean. Peer tier 28/31: operator_walk test CORRECTED (not relaxed, teeth shown, fix merges after the release REV); the other two reds
accepted in the packet; hostile_campaign TLS "owner-death-like" is OPEN until a fresh-source probe (classified harness oracle error).
Touches on the anchor (5.75.245.0) ONLY fn's own: fn user, fn.service + drop-ins, fn-health, fn-cert-sync, ports 119/563,
/var/lib/fn + /opt/fn retired by rename, reset-failed of two rehearsal units. Not Caddy, portal, Mini's backup pull, DNS, firewall.
Mini's candidate is on the workhorse, unaffected.
Finding: 6.6.1 imports the 6.6.0 `store export` (5 records) though the packet expected a refusal; init stays fresh per D34; the
export is a working import route, not a migration claim.
Root recommendation: GO, after the hostile_campaign fresh-source probe is green (one short run), executed in daylight with the
rollback route (R10) ready. Afterward Mini lands its PQ-only fn client once fn confirms each host.

## Option for Ember (from the fn root): keep the public node's history?
(i) init fresh as planned (D34): simplest; the old content stays in the retired store and its export.
(ii) init, then `store import` the 6.6.0 export, so readers and peers keep the history: fn recommends this IF the node holds
anything worth keeping, but only after one more rehearsal step importing a FULL-size export from a copy (the rehearsal only
imported 5 records).
Root view: greenfield says history is not owed; choose (ii) only if there's content you want readers to keep, and then require
the full-size import rehearsal first.
