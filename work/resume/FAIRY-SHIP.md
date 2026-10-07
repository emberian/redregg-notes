# FAIRY-SHIP resume (2026-10-04 evening)

State: lane/fairy-ship = a9c30a81 on GitHub main 259a2fb0, burst-gate:/srv/lanes/fairy-ship/src; bundle at persvati:/home/ember/workbox/claude-lanes/bundles/fairy-ship.bundle; queued in MERGE-QUEUE.md.

## Decisions and reasons
- J12X client rows: the CLIENT was wrong, with a Host half. `mini author` runs the client's own pure Host as a one-shot process; local_process called every non-zero exit "request status uncertain". 4c5c58a3 fixed the session path (255 by name) but not the one-shot path. A verb that reads no Store cannot have been accepted, so its failure is definite. Fix: Host exits 2 + encoded Outcome (stdout) + decoded outcome (stderr) for author/inspect/signatures/observe-assemble/assemble; client turns exit 2 + decoded `refused` into HostDecision::RefusedFrame with the socket path's message (shared fn refused_frame_message). Other exits stay "uncertain".
- J12X "describe with payload 254 vs 255": journey expectation was stale, not a defect. 8ac769d7 makes `mini serve` refuse a body on ops 0/6 as 254 "operation takes no request body", never forwarded (certain). j12x.sh now asserts that for op 0 and op 6. The Host's 255 path remains covered by RequestRefusal theorems.
- Row 16: HOST drifted. Client sends before = annotation["canonical"] = full StoreCodec entry (address+record), which Host/Json.lean itself emits; both Host grammars decoded it with annotationRecordStream (bare record). Guard is now the entry, checked canonical, annotations namespace, id = rewrapped annotation. Contract doc updated.
- No re-emit/re-genesis; Lean changed so keeper re-pins host-closure/surfaces/objective-proofs snapshot. Old/new client+Host pairs mismatch (rebuild both).

## Evidence (burst-e2e ember@152.236.4.24, ~/fs)
- run-base/ J12X on the 259a2fb0 green artifact: 9 client rows FAIL "request status uncertain" (+ op0 row 254). run-fix/ with lane binaries (~/fs/bin, manifest-fix.json): J0-J3 + J12X PASS, all 19 rows.
- pd-out/protected/jprotected-docs.tsv: protected-documents journey (same-store adapter, world wfix on a candidate dir with the lane host/mini/consent swapped in, ~/fs/cand-fs) rows 1-52 ok incl. 16, 17-18 (share recovery), accept, edits, revoke. Red-before: DEPLOY-3B g3/composed/state/documents-protected/protected/log/16.err (same journey, old Host).
- cargo: tests::one_shot_pure_refusal_is_named_not_uncertain + one_shot_other_exit_stays_uncertain pass; planted fault (exit-2 arm -> 99) turns the first red.
- Lane logs: burst-gate:/srv/lanes/fairy-ship/logs.

## Next step (not done): row 53 of the protected-documents journey
`owner: submit pd-blocked` (a fresh protected post against a revoked holder) is refused by the Host as `refused: undisclosed: request refused (phase admission)`; the journey expects a reason matching `audience.*transition|transition.*audience`. Submission refusals are blind by Host policy (J12X's "blind submission refusal" row asserts the same shape), so the assertion in scripts/protected-document-journey.sh (ALL_HOLDER_REASON on submit) is stale. A correct fix must still attribute the refusal to the all-holder gate (not accept any refusal): e.g. assert the undisclosed refusal AND that the same post is admitted once the revoked holder is out of the roster, or name the gate via a disclosed channel (dry-run op 130). Rows after 53 (54+, same-atoms, reopen) are unrun. Proposed workboard row: PD-ROW53.
