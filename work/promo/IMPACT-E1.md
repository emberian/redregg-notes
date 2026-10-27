# IMPACT-E1 — the cross-object read (E1) and support pins on kernel cells (C1, shape B), one design, one `lang!`

Worker: CX-PROMO (Claude). Written 2026-10-22. Base: nanodregg `origin/main` = **f8d04ac**, worktree
`hbox:/tank/dregg-build/nanodregg/wt/promo`. Plan: `PROGRAM-20261022.md` §1 B1/B2, §3 P1 E1 + C1, §7 P1, §8.3.
Nothing built beyond the base and the two probes. Tags: READ (source at f8d04ac) / MEASURED / INFERRED.
Census artifacts beside this file: `E1-support-probe.txt` (the probes, whole output), `E1-grep-base.tsv`
(`git grep -lw` of 37 touched names), `E1-revdeps-base.tsv` (714 constants whose elaborated type or value uses
one of the 51 names in `E1-touched.txt`, exported from the whole-tree environment at f8d04ac).

## 0. Answer first

- **The two probes, MEASURED (`E1-support-probe.txt`).** (a) cv 01a1649d: through the real `Receive.submit`
  and the installed Std.hole (P8) package, a fact naming a cell the kernel never had (no entry before or after)
  at an arbitrary pin is admitted by `post`; a candidate citing it is admitted with status `verified`; `select`
  admits; `commit` admits and spends the one counted unit to the ghost-supported candidate (left 0). Defect (2)
  is real; LH14 is not narrowed. (b) REOR D.1: "revoke only" then a commit pinning g0 at its TOMBSTONE: admitted,
  the unit spent. "Revoke + unpost" as two calls: the commit refuses `support0 withdrawn`. "Revoke and unpost
  in ONE call" is not constructible: `Unsigned` carries one `Body` (READ `Kernel/Receive/Call.lean:96–111`),
  and a method's emitted calls (`callsOf`: grant/invoke/transfer, READ `Lang/Call.lean:157–170`) are made as the
  OBJECT, while g0's issuer is the member `a`. So nano cannot refuse the second row by construction: shape A
  leaves the gap reachable; C1 stands, and E1 is not only the fuse's foreign read.
- **The design.** The plan's synthesized `cited : cell → live` relation is built as a synthesized COLUMN of the
  cited relation's own point read (§1.2), declared by the method's read TYPE: a relation keyed by exactly one
  digest field may be read with each point's `live : bool`, which the Lang runtime fills from the caller's
  `Pinned` view (`cellLive look g`), and an unpinned cited cell refuses the kernel's `unpinned g` by name. No
  `reqTy`/`methodTy` change; no Term former; no new package field; liveness is never in `editTy`, so no method
  can type an edit of it (the plan's "generator rule refuses every edit of `cited`" holds by construction).
  The ROM grain: `SupportPin` (`.row rel key ver | .cell id`) replaces `HolePin` everywhere in a `HoleROM`
  (supports, hypotheses, guard pin); a `.cell` support holds iff the cell is pinned and live.
- **What changes on the wire: the ROM section** (a new support tag), so the package wire moves **4 → 5**
  (`Bounds.packageWireVersion`, the codec label `lang/package/5`, `lang/package-version/5`). Every package's
  bytes change in their first byte; every package id changes; every journey package re-emits. Nothing outside
  the journeys holds a package id (MEASURED: `grep -rl` over `deploy/`, `client/`, `rows/`, `gates/` finds only
  `gates/codec-vectors.tsv`). This is the `lang!`.
- **Premise price, INFERRED from the statements (to be MEASURED by the digest diff after the build): no landed
  theorem gains a hypothesis.** 8 `Lang/Proofs/LiveHoles.lean` statements gain the binders `digestOf look`; the
  statements naming `readsData`/`relReads` gain `look`; `selectHole_origin`'s conclusion changes MEANING (it now
  covers cells). Every other change is a re-proof.
- **Cross-layer files this needs (ASK, §8):** `Ledger/Proofs/EscrowWitness.lean` (a private lemma names
  `readsData`'s argument list), `Emit/Vectors.lean` (`HolePin` literals; one `.cell` support vector), the
  regenerated `gates/codec-vectors.tsv`; and, only if the build breaks them, proof-only ports in
  `Kernel/Proofs/{InvokeWitness,InvokeTreeWitness}.lean`, `Ledger/Proofs/{EscrowAdmitted,EscrowRun}.lean`,
  `Hosting/Proofs/{Allowance,Package}.lean`. The precedent is d7989d9 (the version-4 hole wire): CODEC, GATES,
  KERNEL, LEDGER grants for exactly these files.

## 1. The definitions changed [READ at f8d04ac; the new text is the intent, settled at build]

### 1.1 ROM grain (`Lang/HoleROM.lean`, `Lang/LiveHoles.lean`, `Lang/HoleWire.lean`, `Lang/Print.lean`, `Lang/Read.lean`)

| name | f8d04ac | after |
|---|---|---|
| `HolePin` (structure `rel key ver`) | `HoleROM.lean:7–11` | **deleted**; `inductive SupportPin \| row (rel : Nat) (key : ByteArray) (ver : Nat) \| cell (id : ByteArray)` |
| `HoleCode.supports` | `List HolePin` | `List SupportPin` |
| `HoleROM.hypotheses` / `guardPin` | `List (Option HolePin)` / `Option HolePin` | `List (Option SupportPin)` / `Option SupportPin` (one pin type in a ROM) |
| `cellLive` (new) | — | `cellLive (look : Pinned D) (g : D) : Bool := match look g with \| .ok (some _) => true \| _ => false` ("g is live", never "at a version": a grant's slots move on every spend, KERNEL-60) |
| `holePinHolds` | `LiveHoles.lean:79–82` | **renamed `supportLive digestOf look rv self`**: `.row` = the old body; `.cell id` = `(digestOf id).any (cellLive look)` |
| `supportPinned` (new) | — | `.row`: `holeRow` (unchanged refusal `unpinned`); `.cell id`: `look g` errors or `digestOf id = none` → `.unpinned` |
| `HoleRefusal.supportDead (hole)` (new) | 21 constructors | 22; wire `holeSupportDead {n}` |
| `changedHypotheses`, `runHoleGuard` | `rv self h` | `digestOf look rv self h`; the existing `holeRow` presence check becomes `supportPinned` |
| `selectHole` | `rv self h`; supports: `c.supports.all (holePinHolds rv self)` else `derivationMoved` | `digestOf look rv self h`; every `.cell` support `supportPinned` (else `unpinned`); row supports as today (`derivationMoved`); a dead cell → **`supportDead h.name`** |
| `resolveHole`, `instantiateHoles` | `rv self …` | `digestOf look rv self …` (pass-through) |
| `loadLive` (`Program.lean:207–210`) | holds `look` already | passes `digestOf look` to `instantiateHoles`; its signature is unchanged |
| `checkROMLits` (`Program.lean:159`) | term literals | also every `.cell id` must be a digest of the World (LANG-38's boundary for the new id) |
| `Wire.holePinTree/Of/Wire`, `holeOptPin*` | `HoleWire.lean:8–29` | `supportPinTree`: `.row` = the old `node 0 key [rel, ver]` byte for byte; `.cell id` = `node 1 id []` (new tag) |
| `Print.holePinSx`, `Read.holePin` | `(pin …)` forms | the same form for `.row`; `(cell #hex)` for `.cell` |

Asymmetry kept on purpose (reader question R1): an UNPINNED row support stays `derivationMoved` (today's
behaviour, `holePinHolds` maps it to false); an unpinned CELL support refuses `unpinned`. Unifying rows to
`unpinned` would change the meaning of `selection-support-version`-style checks and is not E1's.

### 1.2 The synthesized read (`Lang/Package.lean`, `Lang/Rel.lean`, `Lang/Program.lean`)

| name | f8d04ac | after |
|---|---|---|
| `RelRead` | `points range` (`Package.lean:172–176`) | `points range live` — `live : Bool` |
| `RelDecl.cellKeyed` (new) | — | `d.key` is exactly one field of type `.digest` |
| `livePointTy` (new) | — | `optTy (.record [("key", keyTy d), ("live", .bool), ("val", optTy d.val)])` |
| `relReadTy d x` | point slots at `pointTy d` | at `livePointTy d` when `x.live` |
| `relReadOf d T` | reads back `⟨n, r⟩` | reads back `⟨n, r, live⟩`; `live` only when `d.cellKeyed` (else `none`: the package check refuses the method's type) |
| `relReads` | `digestOf rv self i ℓ d x` | `digestOf look rv self i ℓ d x`; on a live read each point's `live` is `cellLive look g` for the key's digest `g`; `look g` erroring is thrown as is (the kernel's `.unpinned g`) |
| `readsData` | `digestOf rels rv self rs` | `digestOf look rels rv self rs` |
| `runSetupWith` | `readsData digestOf p.rels rv r.self sg.reads` | `readsData digestOf look …` (both the closed and the live setup: a leaf package reads the same rows either way, so `runMeasuredLive_leaf_closed` keeps its statement) |
| Surface `(reads …)` | `(points n)`, `(range m k)` | adds `(live)` |

### 1.3 Std.hole (`Lang/StdHole.lean`, `Lang/StdHoleModel.lean`) — C1

| name | f8d04ac | after |
|---|---|---|
| `holeFactsView`, `readFacts`, `readBoth` | `facts ⟨3, none⟩` | `facts ⟨3, none, true⟩` (facts is keyed by `cell : digest`: `cellKeyed`) |
| `holeProbePoint` (`:39–48`) | absent 0 · same pin 1 · moved 2 | absent 0 · same pin AND live 1 · moved 2 · **same pin, cell dead 3** |
| `holeSupportProbe` (`:52–61`) | `anyEq 1 → 1; anyEq 2 → 2; 0` | `anyEq 1 → 1; anyEq 3 → 3; anyEq 2 → 2; 0` (one point per key, so the order only orders `none`) |
| `holeVerdict`, `holeVerdictLabel`, `holeDecision` | 7 labels | 9: `support0Dead`, `support1Dead` |
| `holeStatusOf`, `holeVerdictCheck` | — | `suspended "support0 dead"` / refuse `support0 dead` (and `1`) |
| `HolePoint` (model) | `cell author pin` | `+ live : Bool`; `holePointData` adds the `live` field; `holePointObservation` returns 3 for a matching dead fact |
| `holeAdmission`, `holeRecordedStatus` (model) | 7 labels | 9 |
| `holePosted` (`:183–192`) | `by = req.agent` | **unchanged**: a fact stays the poster's claim (`hole_postArg g pin`); what changes is that every reader checks it against the cell |

### 1.4 Journey fixtures (`Lang/Journey.lean`, `Lang/Journey/*.lean`)
- `p8Rows`: `propose` pins the provider grant g (its fact is now read live); the comment at `:2309–2311` (the
  measured admission) is deleted; the probe becomes the row "P8.2 re-pinned tombstone" (§6).
- `holeRows`: every call pins both fact cells (`a.id`, `b.id`); LH14 added (§6).
- `Journey/ContextualCycle.lean`: `observedFact` cites cells 1 and 5 (arbitrary digests, not cells); they become
  the two members' cells, since a fact now asserts a LIVE cell. INFERRED: the LP E4 rows keep their text.
- `Journey/Contextual.lean`, `ContextualChecks.lean`, `ContextualReceive.lean`: `HolePin` literals → `.row`;
  `selectHole`/`resolveHole`/`instantiateHoles` gain `Sim.digestOf` and a view: `noCells` (every cell unpinned)
  where the ROM has no cell support, the real `pinned` view in `ContextualReceive`.
- `Emit/Vectors.lean` (CODEC, §8): the rich ROM section row gains one `.cell` support; `HolePin` literals → `.row`.

## 2. Every touched name across the layers [MEASURED `git grep -lw` at f8d04ac; full table `E1-grep-base.tsv`]

Outside `Lang/`: `HolePin`/`HoleCode`/`packageWireVersion` in `Emit/Vectors.lean`; `runSetupWith`/
`runMeasuredLive` in `Kernel/Proofs/{InvokeWitness,InvokeTreeWitness}.lean` (they `unfold … runSetupWith` and
`decide +kernel` a concrete counter run with no reads); `readsData`/`runSetupWith`/`runMeasuredLive`/`methodSig`
in `Ledger/Proofs/{Escrow,EscrowAdmitted,EscrowRun,EscrowWitness}.lean`; `methodSig` in
`Hosting/Proofs/{Allowance,Package}.lean` (statements `methodSig … = some ⟨unit, [], [], 0⟩`: empty reads, so
`RelRead`'s new field does not reach them); `relReads` only in a docstring of `Protocol/Command/Machine.lean:619`.
`Host`, `Hosting` (non-proof), `Protocol` (code), `Census`, `Codec`, `Bench`, `Ops`, `gates/*.tsv` rows other than
`codec-vectors.tsv`: none [MEASURED].

## 3. Reverse dependencies from the exporter [MEASURED `E1-revdeps-base.tsv`]

714 constants use a touched name (358 theorems, 316 defs, 30 ctors, 10 recursors): `Lang` 448, `Lang.Proofs` 205,
`Ledger.Proofs` 17, `Lang.Journey` 17, `Emit` 8, `Lang.Proofs.Contextual` 6, `Kernel.Proofs` 5, `Lang.Sim` 4,
`Hosting.Proofs` 4. The theorems whose STATEMENT (elaborated type) uses one, generated constants excluded, are
the list of §4.2; every other theorem in the TSV uses them only in its proof and must re-prove with its statement
byte-identical (the digest diff measures it).

## 4. The theorems AS STATEMENTS, each with its nano object and the DEPLOYED MUTATION that falsifies it

### 4.1 New (E1/C1)

1. **`cellLive_iff`** — `cellLive look g = true ↔ ∃ c, look g = .ok (some c)`. Object: `Lang.cellLive`, the one
   liveness predicate (ROM supports, the live read, C2's `kernelWorld`). Mutation: `cellLive look g :=
   (look g).isOk` (a pinned tombstone or absence reads live) → false at `look g = .ok none`.
2. **`cited_authenticated`** (sibling of `holeRow_authenticated`) — `relReads digestOf look rv self i ℓ d x =
   .ok v → x.live = true →` for every position j of the caller's points `rv.points self i`, slot `p{j}` of `v` is
   `some {key := k, live := cellLive look g, val := …}` where `k` is that point's key read back and `digestOf`
   (its one digest field) `= some g`. Object: `Lang.relReads`, the rows argument of every method run (both
   setups). Mutation: `relReads` writes `live := true` (drops the `look` read) → false at a tombstone. **B2's
   tooth.**
3. **`selectHole_cell_support`** — `selectHole digestOf look rv self h = .ok s → ∃ c, h.code[s.index]? = some c ∧
   ∀ id, .cell id ∈ c.supports → ∃ g cell, digestOf id = some g ∧ look g = .ok (some cell)`. Object:
   `Lang.selectHole`. Mutation: `supportLive (.cell _) := true` → false.
4. **`revoked_support_refused`** (B1) at both grains, one theorem per grain, named so:
   - ROM: `digestOf id = some g → look g = .ok none → (the selection row decodes i) → h.code[i]? = some c →
     .cell id ∈ c.supports → ∀ s, selectHole digestOf look rv self h ≠ .ok s`, hence `(resolveHole …).receipt =
     none` and demanding the hole faults with its named refusal in one step (`blocked_step`). Object:
     `selectHole`/`resolveHole`. Mutation: as 3.
   - Std.hole (`revoked_support_refused_hole`): if the facts read came from `relReads` on a live read
     (`cited_authenticated`), `look g = .ok none`, and the candidate's `s0 = (g's bytes, pin)` with the fact at
     `pin`, then the generated checked judge evaluates to `support0Dead` and its admission is
     `.error (.refused "support0 dead")` (`BigStep`, composed from `holeProbePoint_meaning`,
     `holeDecision_application`, `holeVerdictCheck_meaning`). Object: the generated `select`/`fill`/`accept`
     judgment and P8's `commit` (which runs `select`). Mutation: `holeProbePoint` ignores `live` → 1 → admits.
   The plan says "over `Receive.submit`". INFERRED price of that statement: no landed theorem relates `submit`
   to a Std.hole method body's evaluation (the run between them is `runSetup_spec` + `method_live_run_sound`,
   which give typing, not a value); a submit-level theorem is a new run-semantics layer. The through-`submit`
   evidence is the journey row (executed, real `submit`); the theorem stops at the deployed read + the deployed
   judge. Reader question R2: accept, or ask for the submit layer (then a second card).
5. **`posted_support_checked`** (B2) — `holePointObservation cell pin pt = 1 → ∃ p, pt = some p ∧ p.cell = cell ∧
   p.live = true`, with `holeProbePoint_meaning` (Term = model) and `cited_authenticated` (`live = cellLive look
   g`): a support the generated judge reads as current names a LIVE kernel cell. Object: the generated probe on
   the live read. Mutation: drop the `live` conjunct in `holeProbePoint` → the ghost fact of probe (a) reads 1 →
   false.
6. Teeth as named decided theorems (no `#guard`): `hole_probe_dead` (`StdHoleTeeth`: a matching fact at a dead
   cell probes 3); `cell_support_dead_refused` (`LiveTeeth` or `Journey/ContextualChecks`: a concrete ROM with a
   `.cell` support under a view with `look g = .ok none` selects `.error (.supportDead 0)`).

### 4.2 Changed statements (the census will print each; INFERRED here)

- **Binder only (`digestOf look`), the 8 of `Lang/Proofs/LiveHoles.lean`:** `selectHole_origin` :49,
  `resolveHole_refusal` :70, `instantiateHoles_typed` :83, `instantiateHoles_sources` :99, `runHoleGuard_cost`
  :119, `selectHole_nodes` :301, `resolutionMax_committed` :340, `instantiateHoles_cost` :362. (The plan's
  `loadLive_libTy` :261 / `loadLive_checked` :275 do NOT change: `loadLive` already takes `digestOf … look`.)
- **`selectHole_origin`'s conclusion changes MEANING.** Old: `c.supports.all (holePinHolds rv self) = true` —
  every support is a row of `self` at its exact version. New: `c.supports.all (supportLive digestOf look rv self)
  = true` — every row support at its version AND every cell support a pinned live cell. Its consumer
  `resolutionMax_committed` uses only the `c.body` conjunct [READ :354–357]; no other consumer [MEASURED grep].
- **Binder `look`** (statements naming `readsData`/`relReads`): `runSetup_spec`, `runSetupWith_spec`
  (`Proofs/Load`), `runMeasured_means` (`Extract`), `invoke_never_stuck`, `readsData_conforms`,
  `relReads_conforms` (`Invoke`), `invoke_live_never_stuck` (`LiveInvoke`), `readsData_digests`,
  `relReads_digests` (`Provenance`), `relReads_points`, `relReads_pins_past_slots`, `relReads_points_witness`
  (`Rel`; the last two also spell `⟨n, none⟩` → `⟨n, none, false⟩`), Ledger's private `setup_eq`, `hw0`.
- **`relReads_conforms`**: `Conforms v (relReadTy d x)` — same text, `relReadTy` now covers live reads; the proof
  gains the live arm (the `live` field is a `.bool`).
- **Std.hole**: `holeProbePoint_meaning` (`HolePoint` gains `live`; the observation is 3 for a dead match),
  `holePointCovered_meaning` (point data gains the field), `holeDecision_application`/`_meaning`,
  `holeStatusOf_*`, `holeVerdictCheck_*` (same text; the label set they quantify over grows by two),
  `HoleBridge.holeDecision_label` (its listed set gains `"support0Dead"`, `"support1Dead"`: a statement TEXT
  change, no hypothesis).
- **Wire**: `holePinOf_tree`, `tree_of_holePinOf`, `holeOptPinOf_tree`, `tree_of_holeOptPinOf` → renamed for
  `SupportPin`, both arms; `holeCodeOf_tree`, `holeROMOf_tree` and inverses re-proved; the nine version theorems
  (`packageCodec_label`, `encodePackage_version`, …) keep their text at value 5.
- **`DeployedContextual.*`** (`LiveJourney`, 8): their statements apply `selectHole` to concrete views; they gain
  the concrete `Sim.digestOf noCells` arguments, conclusions unchanged.

### 4.3 The rename map (for the digest diff; the file `E1-renames.tsv` is written at build)
`HolePin` → `SupportPin` (`.mk` → `.row`); `holePinHolds` → `supportLive`; `Wire.holePinTree/holePinOf/holePinWire/
holeOptPinTree/holeOptPinOf` → `Wire.supportPin*`; `Print.holePinSx/holeOptPinSx`, `Read.holePin/holeOptPin` →
`supportPin*`; the four `Proofs/Wire` pin theorems likewise.

## 5. The premise price

INFERRED from §4.2, to be MEASURED by the census statement-digest diff under §4.3: **zero landed theorems gain a
hypothesis.** A binder is not a hypothesis. The one meaning change is `selectHole_origin`'s (a strengthening:
the old conclusion is the new one restricted to row supports). Kernel semantics: unchanged (`receive_congr`
quantifies over `c.unsigned.pins`; the live read goes through `Pinned`, READ `Kernel/Receive/Call.lean:422–423`).

## 6. The row diff [INFERRED; MEASURED after the build]

- **P8.2 re-pinned tombstone: refused support0 dead** — NEW (B1). The probe's commit through the real `submit`;
  `refusedBy v "commit" "support0 dead"`; counted left stays 1.
- **LH14** — NEW (B2), on a scratch branch before LH9's acceptance: A posts a fact naming a digest the kernel
  never had (admitted: `post` reads nothing); proposing a candidate citing it with the cell UNPINNED: refused
  `unpinned`; with the cell pinned absent: admitted, recorded `suspended "support0 dead"`; selecting it: refused
  `support0 dead`. One `note` per verdict, all under "LH14 support of a digest the kernel never had".
- Text changes that are numbers only (the bundle re-emits, the probe reads more): the helper/package byte
  counts (`P8 install checked helper (N bytes)` ×3, `P8 install checked open artifact`, `LH0 installing helper
  ROM` ×3, `LH0 generated hole reads (N chars)`, `LH1 … (N package bytes)`, LP E4 helper sizes) and the
  `required steps / ticks` of LH7/LH8.
- `LV2`/`LV3` print the version: `version 4 → 5`, `lang/package-version/4 → /5` (LV3's literal is edited).
- Every other row's text unchanged.

## 7. The design alternatives, priced

- **(A, the plan's text) `Package.cites : List (rel, keyField)` + a synthesized relation `cited` in the rows
  record.** Price beyond the chosen design: a new package-tree node (`packageTree`/`packageOf`/`packageWire` and
  their round-trip proofs in `Proofs/Wire`), a `(cites …)` form in Print/Read/Surface with their round-trip
  proofs, and `readsOf`/`methodSig` taught a label that is not a relation (`rels ++ [cited]`), plus a generator rule
  refusing edits of it. What it buys over the chosen design: nothing a row needs; the chosen design is (A) with
  the declaration moved from a package field into the method's read type, and the "relation" into a column of
  the cited relation's own points.
- **(B) widen `reqTy` with a cells view.** `reqTy` is in every method's, law's and guard's type (`methodTy`,
  `lawTy`, `guardTy`, READ `Package.lean:64, 71, 198, 391`): every package's interface, every Std generator, the
  Bell, every journey package re-typed, and a law would gain a read of other objects (law semantics widen). The
  most expensive and the least targeted.
- **Chosen: the live column, declared in the read type.** Its price is §1–§5.
- P5's receipts (plan §2(a)) would use the same place: a relation keyed by a tx digest read with a `verified`
  column. INFERRED; not built here.

## 8. ASK — cross-layer files (ROOT rules; my GRANT R-0025 is `Lang/**`, `gates/tcb.tsv`, `CHARTER.md`, `decisions/lang.md`)

1. `Ledger/Proofs/EscrowWitness.lean` — `setup_eq`'s hypothesis `hw` and `hw0` spell `readsData`'s arguments;
   they gain `look` (proof-only, private lemmas, no exported statement). CROSS-LAYER: LEDGER.
2. `Emit/Vectors.lean` — `HolePin` literals → `.row`; the rich ROM row gains one `.cell` support (the new tag
   gets a vector); docstring version. CROSS-LAYER: CODEC.
3. `gates/codec-vectors.tsv` — regenerated by `lake exe codec-vectors --write`: the `lang/package/4` site
   (56 rows) becomes `lang/package/5`, every package vector's first byte 4 → 5, one new row; I will list every
   changed row in the decision. CROSS-LAYER: GATES.
4. Conditional, proof-only, statements byte-identical: `Kernel/Proofs/{InvokeWitness,InvokeTreeWitness}.lean`,
   `Ledger/Proofs/{EscrowAdmitted,EscrowRun}.lean`, `Hosting/Proofs/{Allowance,Package}.lean`, only if the build
   breaks them (they `unfold … runSetupWith` and decide a concrete run with no reads; INFERRED: they stay green).

## 9. Gate plan after RELEASE

1. Build: `lake build lang-journey codec-vectors` then the whole tree (`Lang Kernel Ledger Hosting Host Protocol
   Census Codec Emit Bench Ops`, 16G printed, never beside a bench).
2. `lang-journey` and `--contextual`: GREEN; the row diff against `logs/promo/journey-base.txt` exactly §6.
3. Plants, each read from the WHOLE output (grep `error|unbound|No such file|Traceback` as control):
   B1 = `relReads` writes `live := true` → P8.2 tombstone row and LH14 RED; B2 = `holeProbePoint` ignores `live`
   → LH14 (ghost reads verified, select admits) and P8.2 RED. Each a temporary edit, reverted, logged.
4. `codec-vectors --check` against the regenerated table; `--write` reproduces it byte-identical (`cmp`).
5. The census statement-digest diff (`mkdigest_rn.sh` with `E1-renames.tsv`) against f8d04ac: every type change
   is a §4.2 statement, every vanished name in §4.3, and no theorem gains a hypothesis (each listed by name).
6. `gates/check.py` GREEN from the worktree; then `scripts/commit` detached as `lang!: …` (FULL judge), PID file
   `logs/promo-E1-land.pid`, foreground wait, whole log read. Decision `## LANG-75 The promotion program` +
   `### LANG-75.1` (critique, and a meta-critique naming a BIAS). Re-genesis stated: every package id; the
   journey Worlds (re-run from genesis every run); no deployed Store.

## 10. Reader questions (defaults in bold)

- R1 the unpinned-row/unpinned-cell asymmetry (§1.1): **keep rows as today**.
- R2 `revoked_support_refused` stops at the deployed read + judge, the submit leg is the journey row: **accept**.
- R3 the live column instead of `Package.cites` + `cited` (§7): **the column**.
- R4 version 5 (a strict refusal of v4 bytes, though v4 bytes would decode to the same meaning): **bump**
  (the codec's own rule, `Package.lean:629–631`).

## BUILT (2026-10-22, after R-0027; the spec is READ-E1-grok.md where it replaces §6–§9)

Candidate: hbox `wt/promo` on f8d04ac, uncommitted until the landing. Whole tree GREEN (740 jobs, default targets).
- Premise price MEASURED: `diff-E1.txt` (census digest under `E1-renames.tsv`), `hyps-E1.txt` (top-level hypothesis
  count over every changed theorem: no user theorem gains one; 3 generated matcher equations do).
- Vectors: `E1-vectors-diff.txt` (54 + 2 rows; the package site is 54 rows, not 56: READ-E1 condition 3 counted the
  56 lines of both sites). Second `--write` byte-identical; `--check` ok.
- Plants (a), (a2), (b), (c), (d): `E1-plants/` (whole outputs; the runner refuses to read a verdict unless the
  journey exe was rebuilt under the plant). Distinct reds: (b) and (c) differ on LH14a.
- Rows: `lang-journey` GREEN 792 lines; the row diff is in LANG-75.1. Design deltas from §1: the plant split LH14 into
  LH14a/b; `relReads` factored into `readPoint` + `pointData`; `cellLive` lives in `Lang/Rel` (LiveHoles imports it);
  `pointRecTy` makes `optTy (pointRecTy d false)` the old `pointTy d`; the named refusal `liveNotCellKeyed`.
- Cross-layer edits made: `Ledger/Proofs/EscrowWitness.lean` (two private lemmas), `Emit/Vectors.lean`,
  `gates/codec-vectors.tsv`. None of the conditional ports was needed (Kernel/Ledger/Hosting witness proofs built
  unedited).
