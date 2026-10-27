# IMPACT-S9 — the P7 conformance card (`lang!`): refusal constructors, named bounds, one preparation charge, no default hole signature (consolidation step S9)

Worker: CX-FOLD-2 (Claude). Written 2026-10-22, BEFORE any S9 build: this is the design and its statement price,
for the pre-build read (map §5.3). Base: nanodregg `origin/main` = **ac34521** (S8). Map: §1.5 F7, §3.3, §4.2 row S9.
Tags READ / MEASURED / INFERRED. Judge: FULL (`lang!`).

## BUILT — the candidate as built under R-0014 (CX-FOLD-3, 2026-10-22; this section supersedes §0–§4 where they differ)

Candidate: uncommitted in `hbox:/tank/dregg-build/nanodregg/wt/cxfold` on ac34521; the same diff is
`fold/S9-candidate.patch` (28 files, +255/−166, all under `Lang/`). Census diff: `fold/diff-S9.txt`; per-theorem token
diff of every changed theorem type: `fold/S9-typediff.txt`.

**The five conditions, as built** [READ the patch; MEASURED where tagged]:
1. **The recheck arm keeps its own constructor.** `HoleRefusal.instanceRecheck` (wire exactly `holeInstanceType`, no
   text) is thrown by `instantiateHoles`' closed re-check; `instanceType e` (wire `holeInstanceType {e.text}`) is only
   `admitContextual`'s re-check. §1's "one wire change, on a path proved unreachable" is WITHDRAWN: no wire byte moves.
   **Plant `recheck-arm-reachable`** (`Lang/Journey/ContextualChecks.lean`, a `--contextual-checks` row): a hole named
   `10^300` (selection absent, so the hole is blocked and its `.refuse` carries `holeSelectionAbsent 1000…0`, wider than
   `Bounds.reasonMax`) makes the filled body ill-typed, and `instantiateHoles` refuses `.instanceRecheck`; the control
   (name 0) prepares `.ok`. MEASURED: the row is `ok`; with the arm mutated to throw `.instanceType e` (mutation
   asserted present by grep, then reverted) the row is `FAIL` and `contextual-checks: RED (1)`
   (`fold/S9-cchecks-plantoff.txt`). The arm the old design called unreachable is reachable today.
2. **One guard allowance.** `Lang.Bounds.holeGuardFuel := 256` is `runHoleGuard`'s `run` fuel and the per-hole
   coefficient of `Package.holeCharge`; `runHoleGuard_cost` is `used ≤ Bounds.holeGuardFuel` and its proof applies
   `run_used_le` at that name. §0's second name `holePreparationPerHole` does not exist. `holeCandidatesMax := 64`,
   `holeSignatureMax := 16` are their own fields; none aliases `reasonMax`/`docMax`/`methodsMax`/`importsMax`. No
   literal 256/64/16 remains in `Lang/LiveHoles.lean`, `Lang/Program.lean` or `Lang/Proofs/LiveHoles.lean` [MEASURED grep].
3. **(A), Ω named.** The seven defaults are gone (`Lang/Check.lean`); no wrapper. Every checker call in the tree names
   its signature: `git grep` of `inferE|inferFields|inferArms|inferSubst|checkE` lines without `Ω` returns only prose
   and two `unfold checkE`; the short `infer`/`check` likewise [MEASURED]. Closed calls are `(Ω := [])`, never positional.
4. **One charge formula, two m's.** `Package.holeCharge p m := if p.holes.isEmpty then 0 else Term.nodes p.body *
   (m + 1) + Bounds.holeGuardFuel * p.holes.length`. Actual: `p.holeCharge (resolutionMax rs)` (foldl init 1 over the
   resolution bodies). Static: `Package.preparationCost p := p.holeCharge (foldl (max · nodes) 1 over p.holes.flatMap
   (·.code))`. Same formula, not the same number: `instantiateHoles_cost` stays `i.cost ≤ p.preparationCost`, now
   proved by unfolding both through `holeCharge` (the old `Nat.add_comm` alignment is gone because `(1 + m)` is now
   written `(m + 1)` once).
5. **No widening.** `contextualPrintMismatch`/`contextualPrintRead` stay `Except String` (`Print.contextualText`); the
   `StdContextualHole` generator strings stay strings (its two `checkContextual` calls map with `.mapError
   HoleRefusal.wire`); `holeUnresolved`, `holeTicks`, `resultName`/`refusedBy` rows and `ContextualChecks`'
   `admission-prepared-type` prefix check on `Refusal.program` are unchanged; the two `fillBounded` rows compare
   `ExpansionBound` (`.work`, `.size`). The closed-admission sentinel is `.error .provenance` with a comment that it is
   never called; no constructor was added for it.

`fillBounded`'s refusal reaches `HoleRefusal.expansion` by an explicit `match` in `instantiateHoles` and
`unresolvedBody` (not `Except.mapError`), so the existing `split`-style proofs see `fillBounded … = .ok t` directly.

**Proof repairs (statements re-spelled only):** `Lang/Proofs/LiveHoles` (`why : HoleRefusal`, `why.wire.toUTF8`;
`runHoleGuard_cost` at the name; `instantiateHoles_cost` through `holeCharge`), `LawMeaning.unresolvedBody_field`
(one extra `split` for the explicit match), `LiveClosed.preparationCost_closed` (unfolds `holeCharge`),
`LiveJourney.strengthening_factor` (`ε := HoleRefusal`), `used_hypothesis_suspends` (`.error (.supportMoved 0 1)`,
still `rfl`). No `sorry`, no new axiom.

**Census digest diff ac34521 → candidate** (`fold/diff-S9.txt`, no rename map) [MEASURED]:
- 2 vanished, both generated `_simp_1_N` auxiliaries (`instantiateHoles_sources`, `unresolvedBody_field`).
- **27 user theorems change TYPE, all in §3's 33**; the other six of §3 (`loadLive_checked`, `loadLive_libTy`,
  `loadLive_of_load`, `resolutionMax_committed`, `method_live_run_sound`, `invoke_live_never_stuck`) do not move.
  `fold/S9-typediff.txt` is the token diff of each: every change is `String` → `HoleRefusal` (`ExpansionBound` for
  `fillBounded_bounds`), `why` → `HoleRefusal.wire why` (`blocked_step`, `resolveHole_refusal`), the literal
  `"holeSupportMoved 0 1"` → `.supportMoved 0 1`, and `256` → `Bounds.holeGuardFuel`. **0 binders added: no landed
  theorem gains a hypothesis.**
- 18 user definitions and 1 constructor change type: the seven checkers (the default left the binder), the nine
  preparation functions of §5, `HoleResolution.blocked` (+ `.elim`), `fillBounded`. The other 85 type changes are
  generated (`match_`, `eq_`, `inj`, `sizeOf_spec`, splitters) of exactly these definitions and their consumers.
- **Kernel/Ledger/Host: 0 type changes, 0 source edits.** One Kernel value-hash change,
  `Kernel.Receive.object_history_start`: its proof term instantiates `loadContextual_top`, whose type now says
  `HoleRefusal`; its statement is unchanged.
- The Ω edit: 0 theorem TYPE changes (every theorem in `Lang/Proofs/Check.lean` keeps its digest; `inferE._mutual`'s
  aux statements move with the definition's type).

**Gates** [MEASURED]: `lake build Lang` GREEN (226 jobs); whole tree `Lang Kernel Ledger Census Host Hosting Protocol
Codec Emit Bench Ops host lang-journey codec-vectors` GREEN (626 jobs). `lang-journey` (default mode) byte-identical
to ac34521's (787 lines); `--contextual` byte-identical (182 lines); `--contextual-checks` byte-identical except the
ONE new row `ok   LP recheck-arm-reachable` (base built from `git archive ac34521` in scratch). `codec-vectors
--check gates/codec-vectors.tsv` ok (263 vectors of 56 sites) and `--write` leaves the file byte-identical.
`gates/check.py` GREEN with the generated SIZE. Re-emit: none; no wire byte moves.

## 0. Answer first

S9 removes the four conformance debts P7 landed with (review M5, map F7) [READ `Lang/LiveHoles.lean`,
`Lang/HoleBudget.lean`:83–87, `Lang/Program.lean`:160–216, `Lang/Check.lean`:90–234 at ac34521]:

1. **Refusals.** The live contextual preparation returns `Except String` built by `s!"…"`. It becomes
   `Except HoleRefusal`: one inductive, a constructor per refusal, and **one** printer `HoleRefusal.wire` that
   produces today's exact strings. The bytes a refusal puts on the wire (the kernel `Refusal.program` text, and
   the `.refuse T why` bytes of a blocked hole) are unchanged by construction. The gate (§4) checks that they are
   unchanged.
2. **Bounds.** The inline `≤ 64`, `≤ 16`, guard fuel `256` and the per-hole `256` become named constants in
   `Lang.Bounds` (`holeCandidatesMax`, `holeSignatureMax`, `holeGuardFuel`, `holePreparationPerHole`), each with its
   docstring, and every use cites the name.
3. **One preparation charge.** `instantiateHoles`' actual cost (`LiveHoles.lean`:163) and the static
   `Package.preparationCost` (`Program.lean`:212–216) are two written copies of one formula. Both become
   `Package.holeCharge p m := if p.holes.isEmpty then 0 else Term.nodes p.body * (m + 1) +
   Bounds.holePreparationPerHole * p.holes.length`. The actual cost is at `m := resolutionMax rs`, the static
   charge at `m := max over the committed code`.
4. **No default hole signature.** `(Ω : HoleSignature := [])` is removed from `inferE`, `inferFields`,
   `inferArms`, `inferSubst`, `infer`, `checkE` and `check`, so every caller states its signature. Closed
   callers write `[]` [default (A), §2].

**No landed theorem gains a hypothesis.** The statements that change (§3, 33 user theorems by name) change the
refusal TYPE (`String` → `HoleRefusal`), a refusal literal (→ its constructor), or a bound literal (→ its name).
None gains a premise. The Ω change leaves every elaborated statement byte-identical: the default already
elaborates to `[]` (map §3.3), and the census digest checks it.

## 1. The refusal type [READ every `throw`/`.error` in the live path]

`Lang/HoleBudget.lean` gets `inductive ExpansionBound | work | size`, and `Term.fillBounded : … → Except
ExpansionBound Term`. That is the expansion module's own two refusals, so the type is not a second vocabulary.
`Lang/LiveHoles.lean` gets:

| constructor | thrown by (today) | `wire` (byte-identical to today) |
|---|---|---|
| `type n` | `HoleROM.check` | `holeType {n}` |
| `context n` | `HoleROM.check` | `holeContext {n}` |
| `candidates n` | `HoleROM.check` (`≤ Bounds.holeCandidatesMax`) | `holeCandidates {n}` |
| `guardType n` | `HoleROM.check` | `holeGuardType {n}` |
| `candidateType n i` | `HoleROM.check` (both arms) | `holeCandidateType {n} {i}` |
| `package e` (`e : CheckError`) | `Package.checkContextual` (shape, fields) | `e.wire` |
| `signatureBound` | `checkContextual` (`≤ Bounds.holeSignatureMax`) | `holeSignatureBound` |
| `duplicate` | `checkContextual` | `holeDuplicate` |
| `bodyType e` (`e : TypeErr`) | `checkContextual` | `holeBodyType {e.text}` |
| `unpinned` | `holeRow` | `holeUnpinned` |
| `supportMoved n i` | `changedHypotheses` | `holeSupportMoved {n} {i}` |
| `guardBlocked n` / `guardFault n` | `runHoleGuard` | `holeGuardBlocked {n}` / `holeGuardFault {n}` |
| `selectionAbsent n` / `selectionType n` / `selectionIndex n` | `selectHole` | `holeSelectionAbsent {n}` / `holeSelectionType {n}` / `holeSelectionIndex {n}` |
| `derivationMoved n` | `selectHole` | `holeDerivationMoved {n}` |
| `expansion b` | `instantiateHoles`, `unresolvedBody` (via `fillBounded`) | `holeWorkBound` / `holeSizeBound` |
| `provenance` | `instantiateHoles` | `holeProvenance` |
| `instanceType e` (`e : TypeErr`) | `instantiateHoles` and `admitContextual` | `holeInstanceType {e.text}` (see below) |

- `HoleResolution.blocked` carries `reason : HoleRefusal`. Its body is `.refuse T reason.wire.toUTF8`, the same
  bytes as today.
- `admitContextual`'s `prepare` has type `List Ty → Package → Except HoleRefusal Term`. Its refusals reach the
  kernel as `.program r.wire`, the same text as today.
- **One wire change, on a path proved unreachable.**
  - Today `instantiateHoles`' defensive re-check throws the bare string `holeInstanceType`, and `admitContextual`'s
    re-check throws `holeInstanceType {e.text}`. That is two spellings of one refusal.
  - With one constructor, the `instantiateHoles` site also carries the path.
  - `instantiateHoles_typed` (`Lang/Proofs/LiveHoles.lean`) proves the filled body typed, so that `checkE` never
    fails and the bare spelling is unreachable. Nothing on disk carries it: no journey row, vector or row
    compares it exactly; `ContextualChecks.lean`:97 tests the `admitContextual` path by prefix [READ].
  - **Default: unify.** The alternative keeps two constructors for one fact.
- **Not in S9:**
  - `"holeUnresolved"` is the machine's own fault name (`Lang/Eval.lean`:189, `BigStep`, `Derives`), which
    `unresolvedBody` reuses for its refusing body, not a preparation refusal.
  - `StdContextualHole`'s generator strings (`holeSelectionKey`, `holeRoot*`, `holeImports`) are bundle-generation
    errors, outside the live path F7 names.
  - `Program.lean`:439's `holeTicks` is the budget check.

## 2. The hole signature: a design fork, default (A)

- **(A) explicit `Ω`, no default, no second name** (default). Every closed call site writes `[]`.
  - [MEASURED `git grep -ow`] 141 occurrences of `inferE|inferFields|inferArms|inferSubst|checkE` in 12 files (6 Lang,
    1 Journey, 5 Lang/Proofs). 27 of them already pass `(Ω := …)`. Plus the uses of the short `infer`/`check`.
  - Elaborated statements are unchanged, so the census digest proves the change touched no statement.
  - One function keeps one name (law 1).
- **(B) named entry points** (`checkClosed := checkE · · · []`, the map's suggestion).
  - The 13 closed checker theorems P7 kept byte-identical would be restated over a wrapper constant.
  - Every proof that unfolds `inferE` would go through the wrapper.
  - And the checker would get a second name.
  - It reads better at call sites. That is its whole advantage.

## 3. Statements that change, by name [MEASURED: every theorem in the ac34521 census whose elaborated type mentions an affected definition]

Each is the same statement with the refusal type `String` → `HoleRefusal` (and `ExpansionBound` for
`fillBounded`), or a literal → its constructor or bound name. No premise is added.
- `Lang.Proofs.LiveHoles` (15): `holeRow_authenticated`, `blocked_step` (`.refused why.wire.toUTF8`), `checkContextual_shape`, `resolutionMax_committed`, `instantiateHoles_typed`, `selectHole_nodes`, `instantiateHoles_sources`, `instantiateHoles_cost` (its right side `p.preparationCost` unchanged; the proof goes through `holeCharge`), `selectHole_origin`, `runHoleGuard_cost` (`used ≤ 256` → `used ≤ Bounds.holeGuardFuel`), `blocked_has_no_receipt` (`why : HoleRefusal`), `resolveHole_refusal` (`why : HoleRefusal`; `.refuse h.ty why.wire.toUTF8`), `loadLive_checked`, `loadLive_libTy`, `admitContextual_inv`.
- `Lang.Proofs.LiveClosed` (5): `loadLive_of_load`, `admitContextual_closed`, `load_closed_live`, `loadUsing_leaf_closed`, `loadAll_closed_live` (the `prepare` binder's type).
- `Lang.Proofs.LiveJourney` (7): `DeployedContextual.strengthening_uses_argument`, `kept_context`, `replacement_filling`, `used_hypothesis_suspends` (`.error "holeSupportMoved 0 1"` → `.error (.supportMoved 0 1)`), `selected_uses_context`, `alternative_same_filling`, `strengthening_factor`.
- `Lang.Proofs.LiveInvoke` (2): `method_live_run_sound`, `invoke_live_never_stuck`.
- `Lang.Proofs.HoleBudget` (1): `fillBounded_bounds`.
- `Lang.Proofs.LawMeaning` (1): `unresolvedBody_field`. `Lang.Proofs.LawReceiver` (1): `loadContextual_top`.
- `Lang.Proofs.Provenance` (1): `admitContextual_lits`.
- Generated: `HoleResolution.blocked.inj/injEq/sizeOf_spec`.

Several of these mention an affected definition only through its type (e.g. `loadLive`). Their digest moves because
the definition's type moved, and their source text may not change at all. **Kernel/Ledger: no statement there
mentions an affected definition** [MEASURED, same query]. If a Kernel/Ledger proof needs repair, I stop and ask
for a GRANT; none is expected, since they cite `judgeOneContextual_leaf_closed`, `runMeasuredLive_leaf_closed`,
`judgeContextual_mem`, … whose statements are not in the list.

The journey's checks become constructor comparisons:
- `Lang/Journey/ContextualChecks.lean`:60–97: `named x "holeType 0"` → `x = .error (.type 0)`.
- `Lang/Journey/Contextual.lean`:145: `why == "holeCandidateType 0 0"` → the constructor.

The rows that compare a refusal's printed bytes as seen by an executing caller (`refusedBy v "execute"
"holeSupportMoved 0 1"`, `Contextual.lean`:132–153, `ContextualReceive.lean`) stay string comparisons. They read
the wire, and the wire is unchanged, so they are the gate.

## 4. Gates (FULL judge)

- Census digest diff ac34521 → candidate (no rename map):
  - the TYPE changes ⊆ §3's list;
  - the Ω edit contributes 0 TYPE changes;
  - no Kernel/Ledger/Host TYPE change.
- `lang-journey` output byte-identical to ac34521's except the check rows' own labels (expected: identical).
- `codec-vectors --check` and `--write` byte-identical (the refusal strings are not package bytes; this is the
  control).
- Whole tree + `host` + `lang-journey`; `gates/check.py`; `scripts/commit` FULL (`lang!`).
- Re-emit: none expected. If the journey output differs anywhere, the diff is the finding and S9 stops.

## 5. What breaks (said in the commit)

- `Except String` → `Except HoleRefusal` on `HoleROM.check`, `Package.checkContextual`, `holeRow`,
  `changedHypotheses`, `runHoleGuard`, `selectHole`, `instantiateHoles`, `unresolvedBody`, and `admitContextual`'s
  `prepare`.
- `Term.fillBounded` → `Except ExpansionBound`.
- The checker's `Ω` is required.
- A caller that matched refusal strings must match constructors.

The only in-tree callers outside Lang: none (`StdContextualHole` maps with `.wire`).
