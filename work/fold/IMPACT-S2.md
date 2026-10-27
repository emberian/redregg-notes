# IMPACT-S2 — the journey's p8 toy rows dropped, consumers first (consolidation step S2)

Worker: CX-FOLD (Claude). Written 2026-10-22 (after LAND 6eb92fe). Base: nanodregg `origin/main` = **6eb92fe** (S1
complete: f665e94, 82ac944, 6eb92fe). Candidate: uncommitted edit of ONE file, `Lang/Journey.lean`, in
`hbox:/tank/dregg-build/nanodregg/wt/cxfold` (diff: `fold/S2-journey.diff`, 130 lines, +18/−67). Nothing landed. Map:
§1.5 F4, §2.2 D-WRAP, §3.4 "Journey rows that vanish in S2", §4.2 row S2. Tags READ / MEASURED / INFERRED.

## 0. Answer first

1. **No surviving theorem, module, gates row, lakefile target or rows fixture is weaker.** Census diff of the whole
   tree (11 libraries) against 6eb92fe: 17 constants vanish, all `Lang.Journey.p8*` toy definitions or compiler
   matchers of `p8Rows`; 3 new (`p8Live`, two renumbered matchers); the only type/value changes are `p8Rows` itself and
   its compiler-generated `match_*`/`_sparseCasesOn_*` auxiliaries; **0 theorems change** (Lang.Journey's 21 theorem
   constants all identical) [MEASURED `fold/diff-S2.txt`]. The journey is GREEN at 787 lines (was 789).
2. **The toy rows were hiding a real admission.** Replacing the toy judge's "P8.2 re-pinned tombstone: conflict
   guardFails" with the same call through the REAL kernel and package gives **`admitted`**: after provider 0's
   authority grant is revoked (`live` = false), a fresh commit that pins the grant's TOMBSTONE is admitted, the
   artifact is accepted with provider 0 selected, and the counted unit is spent (left 0) [MEASURED
   `fold/S2-tombstone-probe.txt`: `admitted; PROBE live0 false accepted (some true) selected-is-a true left (some 0)`].
   `p8World`'s docstring said "A tombstoned grant or a changed pin cannot specialize to true" — true of the toy only.
   The cause [READ]: the deployed hole reads its own fact rows, never the provider's grant cell ("Keys are rows under
   self, never cell pins", `Lang/StdHole.lean`:63–64; "the package's fact rows alone do not inspect arbitrary kernel
   cells", LANG-P8 Critique); the kernel accepts a pin of a tombstone as a valid pin by design (`Kernel/World.lean`:315,
   :995: absent, tombstone and live are three pin domains). So "withdraw one authority" defeats only plans signed
   while it was live (their pin goes stale); it does not defeat a fresh plan. That is a product gap in the deployed
   P8 composition, not a fold defect. **§5 is the ASK.**

## 1. The definitions S2 deletes or adds [READ `Lang/Journey.lean` at 6eb92fe]

Deleted (map §2.2 D-WRAP: the journey's fifth `CalculusData`, an identity calculus — `msubst _ t := t`,
`uses _ _ := false`, `strengthen _ t := t`):
`p8Data` (:2206), `p8Guard`, `p8Iface`, `p8Candidate`, `p8Swap`, `p8Correspondence`, `p8Registry`, `p8World`,
`p8Available`; the three imports `Lang.Contextual.Trace`, `Lang.Contextual.Provenance`, `Lang.Contextual.TransportKinds`
(:108–110).

Added: `p8Live (w) (supports) : List Bool := supports.map fun (g, pin) => (w.live Sim.env g).isSome && (pinOf Sim.env
(w.entry Sim.env g) == pin)` — the same per-support value `p8World`'s `live i` computed, read straight from the kernel
view, with no calculus around it. It feeds the two rows that observe that the revoke took effect.

Changed: `p8Rows` (the rows below). `p8Session`, `p8Text`, `p8CommitPackage`, `p8ContextBundle`, `p8Arg`, `p8Left`
unchanged.

## 2. Consumers [MEASURED `git grep -lw` over the whole repo]

- `p8Data`, `p8Iface`, `p8Registry`, `p8World`: `Lang/Journey.lean` and `decisions/lang.md` (prose) only.
  `p8Guard`, `p8Candidate`, `p8Swap`, `p8Correspondence`, `p8Available`: `Lang/Journey.lean` only. Their one Lean
  consumer outside the journey, `P/Integration`, left in S1c.
- `p8Rows`/`p8Session`: `Lang/Journey.lean` (`journey` :2788) and `Lang/Journey/Main.lean`:14. No other module,
  gates table, rows fixture or golden names a P8 row text (`git grep '"P8'` outside Journey: only a binary match in
  the gzip golden `gates/certificate-grant.json.gz`, which is `grant_moves_le_cap`'s closure and contains no Journey
  declaration, §4).
- `gates/runs.tsv`:22 `lang-journey (none) ; --hole-omitted-blocker-pin-admits  lang-journey: GREEN
  --harness-control`: judges the final GREEN line, not a row count. The candidate is GREEN.
- After S2 nothing outside `Lang/Contextual` + `Lang/Proofs/Contextual` imports `Trace`'s cache half, `Provenance` or
  `TransportKinds` except `Lang/StdHoleModel` (`Trace.collect`, S11) — which is what S4 needs (map §4.1).

## 3. Journey rows: before → after [MEASURED `diff` of the two runs; base 789 lines, candidate 787, both GREEN]

| row (base text) | after | why |
|---|---|---|
| `P8.1 old signed plan after unrelated update: admitted; trace rejudged []` | `… : admitted` | the "trace rejudged" half ran `Trace.repair` on the toy; the kernel half (the old plan still submits) stays |
| `P8.2 withdrawn instantiation: rejected stale; live provenance [false, true]` | `… rejected stale; live authority [false, true]` | same value, read from the kernel (`p8Live`) instead of `P9.provenance` over the toy |
| `P8.2 re-pinned tombstone: conflict guardFails` | **deleted** | the toy judge's verdict; the real call is ADMITTED (§0.2, §5). Not replaced by a row asserting `admitted` (that would make a gap a green check) |
| `P8.2 mismatched live authority pin: conflict guardFails` | `P8.2 mismatched live authority pin: rejected stale` | now the REAL commit with the live provider pinned at version 0: the kernel's pin check refuses. Plant: the same row with the correct pin turns the journey `RED (1)` with `FAIL … admitted` [MEASURED `logs/cxfold/S2-journey-plant.txt`; error/Traceback grep of the plant output: 0] |
| `P8.3 checked representation false -> true; unknownCertificate refused` | **deleted** | `TransportKinds.recheck` over the toy `p8Registry`; the index it produced (1) is now the live ROM's own selection |
| `P8.3 transported provider selects contextual ROM candidate: admitted` | `P8.3 second provider selects contextual ROM candidate: admitted` | `chooseCode r 1` on the live ROM; P8.4 then checks the commit admitted with `hole_selectedOf … == b.id` (unchanged row) |
| `P8 initial authority was live for both candidates` | same text | `p8Live ready … == [true, true]` instead of `p8Available` (map §3.4 missed this sixth toy-fed row) |

Every other P8 row (the installs, cells, authorities, posts, P8.1 unrelated update, P8.2 withdraw, cancel, deadline,
contract deadline, support correspondence moved, P8.4 re-execute / replay / freshly re-executed / competing use,
receipt, recovered suffix) is byte-identical in the output.

## 4. Census statement-digest diff, 6eb92fe → candidate [MEASURED; same tool as IMPACT-S1 §3/§5]

```
before 53666 after 53652
vanished 17   new 3   type-digest changed 6   value-hash changed 6   module changed 0
```
- vanished: `p8Data`, `p8Guard`, `p8Iface`, `p8Iface._proof_1`, `p8Candidate`, `p8Swap`, `p8Correspondence`,
  `p8Registry`, `p8World`, `p8World.match_1`, `p8Available`, and six `p8Rows.match_*`/`_sparseCasesOn_*`;
- new: `p8Live`, `p8Rows.match_11`, `p8Rows.match_13`;
- type changed: six `p8Rows.match_*`/`_sparseCasesOn_*` (renumbered compiler matchers); value changed: `p8Rows` and
  five of those matchers;
- **no theorem, no definition outside `p8*` changes.** Whole-tree build of the 11 libraries + `lang-journey` GREEN
  (618 jobs, 16G printed). `gates/check.py` GREEN with the generated SIZE (Lean lines (Lang) 46,116 → 46,067; tooling
  21,308 → 21,259).

## 5. ASK — the withdrawn-provider admission (a LANG product gap the toy rows hid)

What is measured: a commit citing a revoked provider authority is admitted when the caller pins the tombstone. What
I infer [INFERRED]: the P8 composition's "provider authority" is enforced only through the pin set the caller
chooses to sign; the package's hole reads fact rows (posted supports), and nothing retracts a provider's fact row
when its grant is revoked. Three shapes for the fix, none of them S2's:
- (A) the support fact must be retracted (a `withdraw` edit) for the withdrawal to count, and the journey's P8.2
  should withdraw that way; the grant revoke then is not the withdrawal at all;
- (B) the package reads the provider's grant cell (a pinned read of a kernel cell by a program: the capability the
  LANG-P8 critique says fact rows do not have) and refuses a tombstone;
- (C) the kernel refuses a pin of a tombstone for an id the call also cites as authority (a KERNEL semantics change).

S2 as proposed does not depend on the answer: it deletes the mirror row and asserts nothing about the gap. I will
open a `cv task` (LANG, P8 withdrawal) with the probe and this section before S2 lands, unless you RULE that the fix
is part of S2 (then S2 becomes a real row asserting refusal, after the fix). Default: S2 lands as above; the gap is a
task.

## 6. Gates S2 will run before landing [plan]

1. the journey run GREEN on the rebuilt candidate, with the row diff of §3 exactly;
2. the digest diff re-run against main at that moment: changes confined to `Lang.Journey.p8*`, 0 theorem changes;
3. `gates/check.py` GREEN from the worktree; the reached build;
4. `scripts/commit` fast path, subject `lang: drop the journey's p8 toy calculus; P8 rows read the live kernel and
   ROM (S2 of the consolidation)`, decision `LANG-74.2` with the row table and the §5 finding.
