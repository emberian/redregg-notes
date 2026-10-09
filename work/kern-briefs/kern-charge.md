# kern-charge — the exact storage-charge equality (R0 item, train `kern`)

You are a Codex worker (gpt-6-astra) on the Mini repo, lane at the train head a4c06ebc (R0 checkpoint 1 merged).
Deputy: DEPUTY-KERNEL (Claude). Sibling kern-r0 owns World/TurnOfIntent/DeployedHistory; you own ONE new file:
`Kernel/ObjectiveTurnTotalityStorage.lean` (imports Kernel.DeployedHistory, Kernel.ObjectiveActivityReceiver; add it to
the umbrella import list in Kernel.lean).

## Context (ROOT ruling, 10-08)
The receiver charges the storage lane as the sum of full post images (ObjectiveActivityReceiver.lean ~:920-928; read it).
The World debits `storageOf DeployedHistory.history creates legs` with `legBytes` = encoded NEW value bytes only
(DeployedHistory.lean: objective_{allocate,write,free}_bytes, objective_post_bytes = payload + 40,
objective_free_below_retired = +4). NO PRICE CHANGES in this range. The gap must be stated EXACTLY as a named equality;
at FD-1 (R3) the charge switches to legBytes and the framing constants go to 0.

## Deliver
1. `receiver_charge_eq_legBytes_plus_framing` per post kind (as kern-r0 measured; confirm each by proof):
   activity live (allocate/write) post: image = legBytes + 40; Book live post: + 26 (4 lifecycle+4 registry+16 resource
   frame+1 kind+1 option); seat live post: + 25 (4+4+14+2+1); retired post: legBytes (=0) + 4; an UNCHANGED post (the
   whole-blob diff normalizes it to a read): legBytes = 0 while the receiver charges its full image (payload + frame).
2. The intent-level equality: for the intent the receiver emits (intentOf / finalIntent; read the real signatures and paste
   them in WORKLOG first), the receiver's storage charge = storageOf DeployedHistory.history creates legs
   + 40·#activityChanged + 26·#bookChanged + 25·#seatChanged + 4·#retired + Σ_unchanged image bytes.
   Equality, not ≤. Counts defined from the posts (not from the conclusion). As a corollary, ≤ (rules out storageAboveCharge).
3. Plant: change a frame length (e.g. the 29-byte "DREGG/OBJECTIVE/ACTIVITY-CELL" customization, or the version width) in
   a scratch copy and confirm the equality goes red; record in WORKLOG, restore.
No sorry/admit/axiom/native_decide; `#assert_axioms` on each headline. No conclusion that holds without the receiver's
charge definition. Builds only via request_build (end your turn after each; never poll). Submit with the umbrella green.
