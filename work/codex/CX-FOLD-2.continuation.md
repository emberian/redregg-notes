# CX-FOLD-2 continuation — written by CX-FOLD-2 (Claude), 2026-10-22, after LAND ac34521 (S8) and READY-IMPACT S9

Next step: **finish S9's candidate** (the `lang!` conformance card).

- **Ruling.** R-0014 RELEASED S9 TO BUILD on (A) under the five conditions of `fold/READ-S9-grok.md` (read them whole).
- **Where the candidate is.** It is UNCOMMITTED in `hbox:wt/cxfold` on top of ac34521; the same diff is saved as
  `fold/S9-wip.patch`. It is the deployed half plus the journey:
  - `HoleRefusal` (with `instanceRecheck`, bare wire `holeInstanceType`, for condition 1) and `ExpansionBound`;
  - `Bounds.holeCandidatesMax`, `holeSignatureMax`, and ONE `holeGuardFuel` used as the guard fuel and the per-hole
    charge (condition 2);
  - `Package.holeCharge` at both m's (condition 4);
  - the Ω default removed, every call passing `(Ω := …)` named (condition 3);
  - the journey rows switched to `refusedAs` constructor checks, the print rows and wire rows unchanged
    (condition 5);
  - the PLANT row `recheck-arm-reachable`: hole name 10^300, selection absent → `.instanceRecheck`; control name 0
    → ok.
- **Scripts.** `fold/S9-s9edit.py`, `S9-s9journey.py`, `S9-s9plant.py`, `S9-omega.py`. The omega pass rewrites
  closed calls of `inferE|inferFields|inferArms|inferSubst|checkE` and names positional Ω. Do NOT run it for the
  short `infer`/`check`: it hits prose and other `check`s. Fix those from the build errors by hand.
- **Last build** `logs/cxfold/S9-b5.log`: `lake build Lang` red in 6 files.
  - `Lang/Proofs/LiveHoles.lean`: 21 errors. These are the real proof repairs:
    - `resolveHole_refusal`, `blocked_step` and `blocked_has_no_receipt` take `why : HoleRefusal`, with
      `why.wire.toUTF8`;
    - the `admitContextual` lemmas' `prepare` binder becomes `Except HoleRefusal Term`;
    - `instantiateHoles_cost` goes through `holeCharge` (rs.length = p.holes.length);
    - `runHoleGuard_cost` is `≤ Bounds.holeGuardFuel`.
  - `HoleBridge` (7): `Lang.infer`/`langData.check` now need `(Ω := [])`.
  - `PrintTeeth` (8) and `StdChain:312`: short `infer`/`check` missing `(Ω := [])`.
  - `StdFits:410`.
  - `ContextualChecks:108` (a `]` parse error in the plant row; check the parenthesization).
- **Then.** Build the whole tree with `host`, `lang-journey`, `codec-vectors`.
  - The journey output must be byte-identical to `logs/cxfold/S9-journey-base.txt`, apart from the new
    `recheck-arm-reachable` row.
  - Codec vectors byte-identical.
  - Census digest: `mkdigest_rn.sh WT S9-after.tsv ""` and `diff_rn.py S9-before.tsv S9-after.tsv …`, where
    `S9-before.tsv` = ac34521. The TYPE changes must be ⊆ IMPACT-S9 §3; Kernel/Ledger 0.
- **After the candidate is green.** UPDATE IMPACT-S9 to the built candidate (R-0014 asks for that), write
  `READY-IMPACT S9-BUILT`, and wait for the second Grok read. Then land `lang!` (FULL judge, ~40 min).
  - The decision names the recheck arm as reachable, the plant, the single allowance, and the five conditions.
  - The commit says what broke: `Except String` → `Except HoleRefusal` on the preparation functions, `fillBounded`
    → `Except ExpansionBound`, Ω required. Re-emit: none.

## State on main (all fast-judged GREEN, pushed)

S1–S5 by CX-FOLD (f665e94 … a27b2da). By CX-FOLD-2:
- d3e850d **S6**: Lang/Index, Lang/Subst, Lang/HoleDecl, C/LangInstance (+HoleModel); ΔOf/holeBound deleted;
  tyOf→holeTy; Host closure 91→89. R-0011.
- 3944bbf **S7**: Lang/Proofs/{Index,Subst,Fill,HoleBudget}; the Kernel/Ledger proof closures lose C/Core, P/Core,
  P/Typing. R-0012.
- ac34521 **S8**: Lang/Proofs/{LiveHoles,LiveInvoke,LiveNeed,LiveClosed,LawMeaning,LawReceiver,LiveTeeth,LiveJourney};
  four Kernel/Ledger import lines under CROSS-LAYER; Kernel/Ledger reach no Contextual module. R-0013.

Decisions LANG-74.6/.7/.8 are in decisions/lang.md. Rulings ACKed: R-0001..R-0003, R-0011..R-0013 (R-0004..R-0010 read).
cv task 01a16201-ef03 = gates/size.py "deployed" meaning (GATES).

`Lang/Proofs/Contextual/` now holds 19 files:
- the spine: Certificate, ClosureStatements, History, HoleBridge, Judge, LangInstance, Operations, Outcomes,
  Provenance, ProvenanceTeeth, Repair, Soundness, Trace;
- the CMTT core (R3): Core, CoreInstance, Typing;
- the protocol (R1): Negotiation, Protocol, ProtocolTyping.

`Lang/Contextual/` holds Certificate, Closure, Core, CoreCalculus, LangInstance, NanoBridge, Protocol, Provenance,
Trace.

## Tools (hbox, scratch, never landed; copies in redregg/work/fold/S6-…/S7-…/S8-…)

`/tank/dregg-build/nanodregg/logs/cxfold/`:
- `mkdigest_rn.sh WT OUT RENAMES|""` + `digest_rn_cmd.lean`: digest of every constant (name, module, kind, type
  string, value hash, renamed-from). A rename file holds `old<TAB>new` rows with component-prefix semantics, plus
  `_private:<OldMod><TAB>_private:<NewMod>` rows that rewrite the module part of private names.
  - Run it on the BEFORE tree with the map, and on the AFTER tree with "". The before oleans must be the base:
    digest BEFORE editing.
  - If you must redo the base: restore the sources, build (0 jobs if untouched), digest, then reapply the edit
    script.
- `diff_rn.py BEFORE AFTER DELNAMES MOVEDMODS full`:
  - erases hygienic binder names (they embed module + counter);
  - prints VANISHED/UNDECLARED/NEW/TYPE/VALUE/MODBAD lists, plus AUX: for each value-changed theorem, the multiset
    of its `._proof_*` statements before vs after.
- `closure.py REV|WT ROOT…`, `closure2.py BASE ROOT` (closure gained/lost from source imports).
- `s6edit.py`, `s7edit.py`, `s8edit.py`: the move scripts (each asserts its anchors). `S*-candidate.patch`.
- Whole-tree build: `SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build lake build Lang Kernel Ledger Census Host Hosting
  Protocol Codec Emit Bench Ops host lang-journey [codec-vectors]` (about 8 min after a move).
- Landing:
  - cat the decision file >> decisions/lang.md;
  - `python3 gates/size.py --write . && python3 gates/check.py .`;
  - `git checkout -- SIZE.md`;
  - `scripts/commit -F MSG $(git status --short | grep -v '^?? logs/' | awk '{print $2}')`;
  - CROSS-LAYER lines go in MSG at column 0.

## Lessons that cost something (this run)

- **A build or commit started by `nohup … &` inside `ssh hbox '…'` dies with the ssh session** (twice: rc=143).
  Run long hbox jobs as a Bash tool `run_in_background` call whose ssh stays open, then foreground-wait on a log
  marker with a ≤10 min loop.
- **A move's census diff is not a string diff.** What looks like statement change is mostly these:
  - hygienic binder names (erase them);
  - Lean re-sharing matchers and `_simp`/`._proof_N` auxiliaries within a merged module;
  - lazily realized `.eq_N` attributed to whichever import loads first.

  Name each class in the decision. The reader asked for exactly that.
- **The map's merges were INFERRED.** Two of S8's merges were wrong: LiveNeed would make an import cycle, and
  LiveInvoke would widen InvokeWitness's closure. Run closure2.py on every merge before calling it done.
- **A namespace move can shadow an `open`ed sibling:** `tyOf` vs `Lang.Wire.tyOf` under `open Lang.Wire`. Prefer a
  name that says its subject over qualifying the consumer.
- Never edit a landed decision's text (append-only). I nearly changed LANG-74.6's Status line; reverted.
- Grok reads arrive about 20–30 min after READY-IMPACT, as fold/READ-S<n>-grok.md plus a ledger row.

## S9 implementation notes (from reading ac34521)

- The refusal sites are `Lang/LiveHoles.lean` (all), `Lang/HoleBudget.lean`:83 (`fillBounded`), and
  `Lang/Program.lean`:166–190 (`unresolvedBody`, `admitContextual`; `.program e` → `.program e.wire`) and
  :212–216 (`preparationCost` → `holeCharge`).
- `StdContextualHole.lean`:73/80 call `checkContextual` inside `Except String`: map with `.mapError HoleRefusal.wire`.
- Statement-change list: IMPACT-S9 §3. Expect proof repairs in Lang/Proofs/LiveHoles (cost proof via `holeCharge`;
  `runHoleGuard_cost`), LiveJourney (`rfl` on constructors), and LiveClosed/Provenance (`prepare` type).
- Ω: remove the 7 defaults in Check.lean:90–234; the build lists every call site missing `[]`. Expected: 0 TYPE
  changes from this part.
- The journey output must be byte-identical. Save the ac34521 journey output FIRST
  (`.lake/build/bin/lang-journey > logs/cxfold/S9-journey-base.txt`; the current oleans are ac34521's).

## After S9

- **S10:** P9's all-env `provenance` replaces `Closure.provenance` (the env-specialized one) and its
  `Judge.provenance_iff`; `P/ProvenanceTeeth` is deleted with it. `P9.provenance_iff` becomes
  `Contextual.provenance_iff`; C/Provenance is merged into C/Closure. Also drop `tm_decEq_toy`'s reflexive conjunct
  (map §2.2). Experiment 4 is already gone (S5).
- **S11:** `Trace.collect` → `Lang/StdHoleModel.lean` (namespace `Nanodregg.Lang.Std`), its 3 lemmas →
  `Lang/Proofs/StdHoleCoverage.lean`; the rest of C/Trace + P/Trace deleted (17 theorems, map §3.1).
- **S12:** C/Certificate + P/Certificate → `Census/CertificateReader.lean` + `Census/Proofs/CertificateReader.lean`;
  consumers `Census/{Certificate,CertificateData}`, `Census/Proofs/Certificate`, `Lang/Journey/Certificate*`; and the
  `certificate-tests` root in lakefile (map §3.2; R-0002 grants Lang/**; Census paths need the map's GRANT CENSUS
  for S12 — check the ledger, and ASK if there is none).
- Stop at S12. S13–S15 wait for Ember.
