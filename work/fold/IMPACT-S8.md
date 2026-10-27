# IMPACT-S8 — the live, closed and law-receiver proofs leave `Contextual`: `Lang/Proofs/{LiveHoles,LiveInvoke,LiveNeed,LiveClosed,LawMeaning,LawReceiver,LiveTeeth,LiveJourney}` (consolidation step S8; CROSS-LAYER: KERNEL, LEDGER import lines)

Worker: CX-FOLD-2 (Claude). Written 2026-10-22. Base: nanodregg `origin/main` = **3944bbf** (S7). Candidate:
uncommitted in `hbox:/tank/dregg-build/nanodregg/wt/cxfold`; the whole diff is `fold/S8-candidate.patch`.
Map: §2.1 "Deployed-subject proofs", §3.2 (Kernel/Ledger import lines), §4.2 row S8. Tags READ / MEASURED /
INFERRED.

- **Rename map:** `fold/S8-renames.tsv`. It has 9 user names, ContractTeeth's 8 teeth and its private
  `identityCandidate_typed` (`Nanodregg.Lang.Contextual.X` → `Nanodregg.Lang.X`), plus 12 private-prefix rows (old
  module → new module).
- All other moved constants were already in `Nanodregg.Lang`: their names do not change, only their module.

## 0. Answer first

- **After S8, Kernel and Ledger reach no `Contextual` module.** The proof closures of
  `Kernel/Proofs/InvokeWitness` (94 → 93), `Kernel/Proofs/Logic/History` (120 → 120) and `Ledger/Proofs/EscrowRun`
  (138 → 137) contain no module whose name includes `Contextual` [MEASURED `fold/S8-closures.txt`, source import
  closure]. The only modules they gain are the renamed homes of what they lost; no new dependency enters.
- `Lang/Proofs/Contextual/` now holds only the spine, the CMTT core and the R1 protocol modules (19 files, listed in §5).
- **No landed theorem gains a hypothesis; no user statement changes** [MEASURED `fold/diff-S8.txt`, full lists]:
  - type-digest changes 0; new constants 0;
  - 3 vanished and 5 value changes, all explained in §3;
  - 555 module changes; the 3 that do not leave a moved module are lazily realized equation lemmas of
    `Need.runBy` (§3).
- **Two deviations from the map's grouping, both forced or measured** (§1):
  - `LiveNeed` stays its own module: merging it into LiveHoles is an import cycle;
  - `LiveInvoke` stays its own module: merging it would widen the Kernel closure.
- Whole tree with `host` and `lang-journey` GREEN (623 jobs); the journey GREEN (787 lines); `gates/check.py` GREEN
  with the generated SIZE [MEASURED]. No deployed module, wire byte or table changes. The Host closure stays 89.

## 1. What moves [MEASURED: each source body appears verbatim inside its own `section … end` in the target]

| target (new) | sources (deleted files) | consumers |
|---|---|---|
| `Lang/Proofs/LiveHoles.lean` | `P/LiveHoles` (273), `P/LiveCost` (101) | LiveClosed, LiveInvoke, LiveJourney |
| `Lang/Proofs/LiveInvoke.lean` | `P/LiveInvoke` (49) | `Lang/Proofs/Provenance.lean`:36 |
| `Lang/Proofs/LiveNeed.lean` | `P/LiveNeed` (80) | leaf |
| `Lang/Proofs/LiveClosed.lean` | `P/ClosedDeployment` (188), `P/ClosedLeaf` (68) | `Kernel/Proofs/InvokeWitness`:38, `Ledger/Proofs/EscrowRun`:59, `Lang/Proofs/Provenance`:37, LawMeaning |
| `Lang/Proofs/LawMeaning.lean` | `P/LawMeaning` (418) | LawReceiver |
| `Lang/Proofs/LawReceiver.lean` | `P/LawReceiver` (177) | `Kernel/Proofs/Logic/History`:51, `Ledger/Proofs/EscrowRun`:60, LiveTeeth |
| `Lang/Proofs/LiveTeeth.lean` | `P/ContractTeeth` (87), `P/LawReceiverTeeth` (107) | leaf |
| `Lang/Proofs/LiveJourney.lean` | `P/Deployed` (89), `P/DeployedCycle` (31) | leaf |

Each source keeps its own `section`, so its `open`s and `variable`s keep their old scope. `P/LiveNeed` has a
top-level `variable {D} {bytesOf} {digestOf}` that would otherwise leak into the next part.

**`P/ContractTeeth` no longer imports the spine.** It imported `P/LangInstance` but uses only `Lang.Proofs.Fill`'s
theorems (`fillHoles_typed`, `hasType_declaresHole`, `fieldsTy_declaresHole`, `armsTy_declaresHole`) [READ the
file]. `LiveTeeth` imports `Lang.Proofs.Fill` and `Lang.Proofs.LawReceiver`. Its 8 teeth and its private helper
leave namespace `Contextual` (rename map rows 1–8, 21).

**The two deviations from map §2.1:**
1. **`LiveNeed` is not merged into `LiveHoles`** [MEASURED first candidate build, `logs/cxfold/S8-build.log`:
   `build cycle detected`]. `P/LiveNeed` imports `Lang.Proofs.NeedComplete`, which reaches `Lang.Proofs.Provenance`
   through `Need` → `Extract`, and `Provenance` imports the live-hole facts. Merged, that is a cycle. So it is its own
   module, `Lang/Proofs/LiveNeed.lean`.
2. **`LiveInvoke` is not merged into `LiveHoles`** [MEASURED second candidate, `closure2.py`]. Merged, it adds
   `Lang.Proofs.Invoke` and `Lang.Proofs.Read` to every importer of `LiveHoles`, including
   `Kernel/Proofs/InvokeWitness` through `LiveClosed` (94 → 95), for two theorems that only `Provenance` uses. Kept
   separate, InvokeWitness goes 94 → 93.

   The map's grouping was INFERRED without the closure. A merge that widens a consumer's closure does not serve law 8.

### 1.1 CROSS-LAYER: the four foreign import lines (R-0002 S8) [the whole Kernel/Ledger diff]

```
Kernel/Proofs/InvokeWitness.lean:38   import Lang.Proofs.Contextual.ClosedLeaf   -> import Lang.Proofs.LiveClosed
Kernel/Proofs/Logic/History.lean:51   import Lang.Proofs.Contextual.LawReceiver  -> import Lang.Proofs.LawReceiver
Ledger/Proofs/EscrowRun.lean:59       import Lang.Proofs.Contextual.ClosedLeaf   -> import Lang.Proofs.LiveClosed
Ledger/Proofs/EscrowRun.lean:60       import Lang.Proofs.Contextual.LawReceiver  -> import Lang.Proofs.LawReceiver
```

These are the only edits to Kernel/ and Ledger/. The theorems they use were already in `Nanodregg.Lang` (map §1.1), so
no name changes in those files, and their digests are unchanged (§3). The Lang-side consumer is
`Lang/Proofs/Provenance.lean`:36–37 (`LiveInvoke`, `LiveClosed`). The commit carries
`CROSS-LAYER: KERNEL …` and `CROSS-LAYER: LEDGER …` lines at column 0.

## 2. Deleted

No declaration is deleted. These 12 files are deleted as files, their content moved: `Lang/Proofs/Contextual/
{LiveHoles,LiveCost,LiveNeed,LiveInvoke,ClosedDeployment,ClosedLeaf,LawMeaning,LawReceiver,ContractTeeth,
LawReceiverTeeth,Deployed,DeployedCycle}.lean`. This list is the deletion authorization for the paths.

## 3. The digest residual [MEASURED `diff-S8.txt`]

```
before 51138 after 51135; vanished 3 (undeclared, generated); new 0; type-digest 0; value-hash 5
module changed 555, of which outside a moved module 3 (Need.runBy.eq_1/eq_2/eq_def: Lang.Proofs.Need -> Lang.Proofs.CostTeeth)
```

1. **`foldMax_member` (user theorem, from `P/LiveCost`): value changed, statement unchanged.**
   - `simp at ha` (`LiveHoles.lean`, `foldMax_member`, nil case) used to create the auxiliary lemma
     `foldMax_member._simp_1_1`.
   - In the merged module an auxiliary lemma with the identical statement already exists: the S7 build created
     `loadAllUsing_inv._simp_3` in the `P/LiveHoles` part. Lean reuses an auxiliary lemma of the same type within a
     module, so the proof now cites that one.
   - Result: `foldMax_member._simp_1_1` vanishes, and the proof value changes by that one constant name.
   - [MEASURED: the vanished lemma's type is byte-equal to `loadAllUsing_inv._simp_3`'s, the only constant of that
     type in `Lang.Proofs.LiveHoles`; `foldMax_member`'s type is unchanged.]
2. **`selectHole.match_5`/`match_8` splitters** (private, generated): the `_sparseCasesOn_3` helpers are shared in the
   merged module. 2 vanished; 3 value lines (`match_5.splitter`, `match_8.splitter`, `match_8.eq_2`).
3. **`Need.runBy.eq_1/eq_2/eq_def`**: lazily realized equation lemmas that both `Lang.Proofs.Need` and
   `Lang.Proofs.CostTeeth` realize. The census environment keeps whichever import loads first, and the new module
   names change that order. Types equal, and the kept copy's `eq_def` proof differs (1 value line). Neither file is
   edited. [INFERRED mechanism; MEASURED types equal.]

No user statement is in a TYPE line (there are none), and the only user value change is item 1.

## 4. `grep` and tables [MEASURED]

- `git grep` of the 12 old module paths and names outside `decisions/`: 0 hits.
- No gates row, lakefile target or rows fixture names them.
- The journey (`Lang/Journey/*`) imports none of them. `P/Deployed` imported `Lang.Journey.Contextual`, which is
  unchanged.

## 5. SIZE [MEASURED `fold/S8-size-preview.txt`]

| row | before | after | why |
|---|---:|---:|---|
| Lean modules | 498 | 494 | 12 proof modules become 8 |
| Lean proof-modules | 269 | 265 | the same |
| Lean lines (Lang) | 42,185 | 42,279 | +94: eight module headers and the `section`/`end` wrapping that keeps each source's scope |
| max dependents of a non-foundation module | 349 | 346 | |
| Host closure, theorems | unchanged | | |

`Lang/Proofs/Contextual/` after S8 (19 files):
- the spine: Certificate, ClosureStatements, History, HoleBridge, Judge, LangInstance, Operations, Outcomes,
  Provenance, ProvenanceTeeth, Repair, Soundness, Trace;
- the CMTT core (R3): Core, CoreInstance, Typing;
- the protocol (R1): Negotiation, Protocol, ProtocolTyping.

## 6. Inverted question: is anything that survives weaker?

No.
- Every statement is identical, with zero type changes.
- The one user proof that changed cites a lemma with an identical statement.
- No check is touched.
- The Kernel/Ledger consumers build against the same theorems under the same names.

## 7. Planned landing

The paths of `fold/S8-candidate.patch` plus the 8 new files; `### LANG-74.8`; subject `lang: the live, closed and
law-receiver proofs leave Contextual — Lang/Proofs/{LiveHoles,LiveInvoke,LiveNeed,LiveClosed,LawMeaning,LawReceiver,
LiveTeeth,LiveJourney} (S8 of the consolidation)`. Commit message lines:
- `CROSS-LAYER: KERNEL Kernel/Proofs/InvokeWitness.lean, Kernel/Proofs/Logic/History.lean (import lines only; R-0002 S8)`;
- `CROSS-LAYER: LEDGER Ledger/Proofs/EscrowRun.lean (import lines only; R-0002 S8)`.

Fast path. Then S9 (the `lang!`).
