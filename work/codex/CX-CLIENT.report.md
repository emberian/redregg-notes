# CX-CLIENT report — cv 01a166e9-a543 (nd cannot pin a point read; E1's live column from the deployed client)

2026-10-23 ~01:20Z start. Worktree hbox:/tank/dregg-build/nanodregg/wt/cx-client (from origin/main 360e1ed; .lake/target copied from wt/e2 at d5275d8). Scratch hbox:/home/hbox/scratch/cx-client.

## (a) CLIENT half — LANDED eb77b78 (pushed to origin)

- 2026-10-23 READ: `nd` argv is parsed in Lean (`Protocol/Command/Verb.lean`), so the client half is Protocol code + a client/tests plant; Rust `nd` passes argv through unchanged.
- READ: the cause. `derivePins` (`Protocol/Command/Machine.lean`) pins a cell on `unpinned` and a row on `rowUnpinned`. A method's POINT read asks for neither: `Lang.relReads` reads `rv.points self i`, the caller's row pins, and an unpinned point is just an empty slot. So the gap was silent.
- BUILT: `invoke OBJ METHOD ARGS [--range REL K [PREFIX]] [--pin REL KEY]... [--via GRANT]`. `Cmd.invoke`'s 4th field is `InvokeReads`. `Command.signedReads` (returns `SignedReads`: ranges + `RowKey` points) replaces `rangesOf`. `invokePoint` reads KEY at `Lang.keyTy`; its bytes are `Lang.keyBytes`. New refusal `badKey`. `planUnchecked` starts the call with `rowPins := points.map (rowPinAt X.env w)`. The key's cell gets pinned by the existing `unpinned` loop, because `pointData`'s `look` raises it.
- MEASURED: full `lake build` green (727 jobs). `cargo test -p nanodregg-client --test pin` green (0.79 s). clippy and fmt clean.
- MEASURED: what `client/tests/pin.rs` shows, on two real Stores:
  - no `--pin` refuses `program` / `unread`;
  - `--pin facts (record (cell #G))` commits while grant G is live;
  - after `revoke G`, the same argv refuses `program` with hint `use: refused grantDead`;
  - `badKey`, `unknownRelation` and `usage` each refuse by name.
- MEASURED: plant M1 (`rowPins := []`, `host` rebuilt) is RED at the live commit (`hint program: use: refused unread`). Restored, then GREEN.
- READ: `nd install` takes CORE text (`Lang.Read.readPackage`), not surface. So the fixture `client/tests/fixtures/pin/Live` is core text printed by LANG's printer, with the surface quoted in the test's doc.
- Premise price: none. The changes of meaning are declared (14 RESTATES-MEANING, 2 DELETES). The judge reported `decls: ok — 16 map line(s), 14 declared change(s) of meaning`.
- Decision text: CLIENT-35 in decisions/client.md. CLIENT-33/34 were already taken.

## (b) LANG half — built and green on an E5 overlay; lands after E5

- 2026-10-23 READ (decided by the new teeth): `(live)` on a RANGE read was DROPPED SILENTLY. `rangeRowTy` had no live column, so a range-only live read had the plain type, and `relReadShape` read it back with `live = false`. Consequences (INFERRED from the code):
  - a body that never read `.live` installed as a plain range read;
  - a live range read of a relation that is not cell-keyed installed instead of being refused `liveNotCellKeyed`;
  - E5's receipt range rows dropped `live` on a read that was both live and receipt.
- BUILT in hbox:/tank/dregg-build/nanodregg/wt/cx-client-b. That worktree is eb77b78 with E5's uncommitted patch overlaid from wt/promo (read-only copy). Changes:
  - `Lang.keyColumns` is the one core for a point and a range row;
  - `pointData` and `columnRow`/`columnRows` (were `receiptRow`/`receiptRows`) both use it;
  - `rangeRowTy d live receipt`.
  - Proofs: `keyColumns_ok`; `pointData_ok` (statement unchanged); `columnRow_conforms`, `columnRows_conforms`, `columnRows_digests`, `keyColumns_digests`; teeth `live_range_read_kept`, `live_range_read_typed`, `live_range_not_cell_keyed_refused`, `live_range_cell_keyed_admitted`.
- MEASURED:
  - full `lake build` green (734 jobs);
  - `client/tests/pin.rs` (now also `scan`: a live range read through nd `--range facts 4`, refused `grantDead` after revoke) green;
  - E5's `client/tests/foreign.rs` green on the shared core;
  - mutation M2 (`columnRows` only on receipt) RED (`scan: stuck`); restored.
- The patch relative to E5 is in hbox:/home/hbox/scratch/cx-client/my-b.patch. The decision draft is CLIENT-36.
- Waiting on E5 (its FULL lander was REFUSED once at 02:0x: many cargo tests red in its judge, `STATEMENT-CENSUS RED (4)`, logs/promo-E5-land.log). It was relaunched as pid 4100346 and is judging.

## LANDED (b) 7fec6d7, on E5 1f09446 (pushed to origin)

- 2026-10-23 MEASURED on 1f09446 + my patch:
  - full `lake build` green (735 jobs);
  - `--test pin` and `--test foreign` green; fmt and clippy clean;
  - `lang-journey` GREEN (810 ok lines, 6.8 s);
  - FAST judge GREEN (`decls: ok — 5 map line(s), 3 declared change(s) of meaning`).
- cv task 01a166e9-a543 marked done (self-reported).

## Hashes
- eb77b78 protocol: nd invoke --pin REL KEY (CLIENT-35)
- 7fec6d7 lang: the live column on RANGE rows, Lang.keyColumns (CLIENT-36)

## Follow-ups (not done; no ASK)
- E5's `client/tests/fixtures/foreign/Accept` reads its trust anchors by RANGE only because a point could not be pinned from nd (IMPACT-E5). `--pin heads (record (cell #H))` now exists, so the acceptor could read one head as a point. That is P5's call.
- `pointRecTy` and `rangeRowTy` spell the column list twice (CLIENT-36 critique).
- E5's Accept fixture (core text + .ob) has no shipped-row check like the Bell's LB0. My pin fixture keeps only core text, so it has no second copy to drift.
- My earlier landing (eb77b78) displaced E5's FULL judge once (about 45 min of judge time). R-0069 allows it; noted as a cost.
