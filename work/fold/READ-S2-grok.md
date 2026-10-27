VERDICT: RELEASE S2

The diff can land as written. Do not add a journey row for the tombstone admission, red or green. File the LANG task before the commit, as IMPACT-S2 §5 already says; that filing is not a change to this diff.

## (1) No surviving row, theorem, or check is a weaker exercise of a live behaviour

Three near-misses, none of them a live weakening:

- **P8.1 asserts less, and the dropped conjunct is the toy.** Base predicate is `usable == "admitted" && pass.rejudged.isEmpty` where `pass` is `Contextual.Trace.repair` on `p8Guard`/`p8World` [READ `Lang/Journey.lean:2340–2343` at 6eb92fe]. The candidate keeps only `usable == "admitted"` and drops the words `trace rejudged` from the label [READ `fold/S2-journey.diff`]. `Trace.repair` / `Trace.seed` occur nowhere else in `*.lean` [MEASURED grep below]. Map §3.4 lists this half as a row that vanishes. The kernel half (the plan signed before the unrelated `.issue` still submits) is unchanged.

- **Label prefix `P8.2 mismatched live authority pin` survives; the subject changes, and the new subject is stronger.** Base: `Contextual.judge` on `p8Iface false` / `p8World` / `p8Candidate 0` over the synthetic list `[(providers[1]!, 0)]`, expecting `.conflict .guardFails` [READ `Lang/Journey.lean:2354–2358`]. Candidate: a real `commit` of `b.id` whose signed pin for `providers[1]!` is that same literal `0`, expecting `rejected stale` [READ diff]. Every signed pin becomes a touch (`touchesOf`, `Kernel/Receive/Call.lean:478–480`) and `touchCheck` refuses when `pinOf E cur ≠ seen` (`Kernel/World.lean:1000–1003`, including `.keep`). The map had this row vanishing; retargeting it onto the kernel is not a weakening. The old verdict string `conflict guardFails` does not survive, so the printed line is not the same label with a silent subject swap.

- **`P8 initial authority was live for both candidates` keeps its text; the bools are the same.** `p8Available` is `P9.provenance` of candidates 0 and 1, each `eval`'d at `p8World`. For this session that is `[env 0, env 1]`: candidates are `(i, false)` against iface repr `false`, so `check` passes; supports and blockers are `[]`, so `eval` reduces to `I.guard env filling`; `Guard.install` makes that `env i`; `p8World.env i` is `(w.live).isSome && pinOf entry == pin` of `supports[i]` [READ `Lang/Contextual/Provenance.lean:18–43`, `Trace.lean:16–17`, `Closure.lean:75–77,226–228`, `Journey.lean:2220–2244,2309`]. `supports` is exactly the two provider grants in order (`Journey.lean:2302–2309`). `p8Live` is that predicate mapped over `supports`. Same two bools. The withdraw row renames `live provenance` to `live authority` and keeps `rejected stale`, the `[false, true]` check, and `headCount … == some 2`.

Deleted, not surviving, and not a live exercise: `P8.2 re-pinned tombstone` (toy `judge`, see (2)); `P8.3 checked representation false -> true; unknownCertificate refused` (`TransportKinds.recheck` on `p8Registry`; `unknownCertificate` has no other use outside `RepairObjects`/`TransportKinds`). `let chosen := 1` matches map §3.4 (`chooseCode r 1`). `p8Swap` preserves `.1`, so the old transport also fed index 1 into the same `chooseCode` / `commit` / `hole_selectedOf == b.id` chain (`Journey.lean:2367–2398`), which the diff does not edit.

No `theorem` or `lemma` declaration exists in `Lang/Journey.lean` or `Lang/Journey/{Main,HoleChecks,Activity}.lean` [MEASURED]. The diff's hunks are the three imports, the `p8Data`…`p8Available` block, and the `p8Rows` body.

## (2) Delete the tombstone row and assert nothing in the journey. Acceptable. Do not carry a RED refuse row.

Yes: the candidate deletes `P8.2 re-pinned tombstone: conflict guardFails` and adds no row whose subject is a fresh commit pinning that tombstone [READ diff]. A comment next to the mismatched-pin row states the admission. A comment cannot go red.

The base row never called the kernel. `unavailable tombSupport` is `judge` returning `.conflict .guardFails` because `I.guard` is false when `w.live` is `none`, even though the pin in `tombSupport` is `pinOf` of the current entry [READ `Journey.lean:2353–2357`, `Closure.judge` at `:226–228`, `World.live` at `:774–778`]. The live path does the opposite. `pinOf (some .tomb)` is its own digest (`Kernel/World.lean:342–347`); `touchCheck` accepts it when `seen` matches, then `.keep` (`:1000–1003`). `pinned` ignores the digest and returns `w.live`, which is `none` for a tombstone (`Kernel/Receive/Call.lean:422–423`). P8's `commit` does not read that cell: it runs `select` and transfers `via` the cap argument (`Journey.lean:2175–2188`). The cap grant is not the revoked provider authority (`:2297–2308` vs `:2346–2347`). Fact rows are what `pinF` pins (`:2316`). So a fresh commit that pins the tombstone, leaves the posted support in place, and spends `cap` is admitted. The probe line is the builder's measurement of that, not a run I repeated [READ `fold/S2-tombstone-probe.txt`].

A reader of the printed journey six weeks out sees withdraw admitted, the old plan `rejected stale`, live authority `[false, true]`, and a bad pin `rejected stale`. They do not see a fresh pin of the tombstone. That silence can be read as "withdrawal is the whole story." It is still the right S2 artifact:

- A row expecting REFUSE is red on every run while the probe is `admitted`. `gates/runs.tsv:22` judges the line `lang-journey: GREEN`, not a row count [READ]. Map §4.2 types S2 as a fast journey edit, 0 theorems. A standing red couples S3+ to a product choice IMPACT §5 correctly leaves open (retract the fact, teach the package to read the grant cell, or change kernel pin domains).
- A green row asserting `admitted` is what that reader would take as the requirement. The fix would then turn the journey red. The builder is right not to mint that check.
- The false green being deleted (`conflict guardFails` while the live call admits) is worse than silence. Map §3.4 already lists this row among those that vanish; it did not know the claim was false of the kernel. Deleting it is the consolidation. The detection belongs to the task, which is the only place that reader will find the gap after the comment rots.

`StdHole.lean:63–64` is the sentence quoted ("Keys are rows under self, never cell pins"), on `holePointCovered`, not on P8's commit. The commit body above is the direct evidence.

## (3) Confirmed: no theorem change; the digest names are all `Lang.Journey.p8*`

I did not re-elaborate (no build). Source and the census listing agree:

- The diff is one file, `Lang/Journey.lean`. No `theorem`/`lemma` line in that file or the diff.
- `fold/diff-S2.txt` lists 17 vanished, 3 new, 6 type-digest and 6 value-hash changes. Every name on that list is `Nanodregg.Lang.Journey.p8*`. `p8Iface._proof_1` is the `by simp` field of the deleted iface, not a `theorem` declaration.
- Nothing outside `Lang/Journey.lean` names `p8Data`/`p8World`/`p8Available`/`p8Rows` except `Lang/Journey/Main.lean:14` (`p8Session`, unchanged) and `decisions/lang.md` prose [MEASURED]. The three dropped imports have no other use in `Journey.lean` (the `Provenance` hit at `:88` is prose about `Lang.Proofs.Provenance`). After the diff, `Trace`'s cache half (`seed`/`repair`), `Provenance`, and `TransportKinds` have no importer outside `Lang/Contextual` and `Lang/Proofs/Contextual`; `Lang/StdHoleModel.lean` keeps `Trace.collect` only [MEASURED].

`Kernel/World.lean:315` is the tombstone-domain docstring (`domTomb`), not the three-domain sentence. That sentence is at `:342–343` and `:995–996`. The pin-of-a-tombstone claim is still true, via `pinOf` and `touchCheck` as cited in (2).

## Spot-checks

Tree: `git -C /Users/ember/dev/nanodregg fetch origin` then `rev-parse origin/main` → `6eb92febb0e939bf8aca29b444a324a2cd64af20`, log `-1` → `6eb92fe lang: delete Integration.lean, the fourteenth S1 module of the consolidation (S1c)`. Worktree `HEAD` is `7e02852`, `main...origin/main [behind 28]`, so every read is `git --git-dir=/Users/ember/dev/nanodregg/.git` at that object. `git -C … grep origin/main` was rejected by the sandbox (it treated the rev as a path).

**StdHole quote.** `git --git-dir=… grep -n -C 2 "Keys are rows under self" 6eb92fe -- Lang/StdHole.lean`

```
Lang/StdHole.lean-63-/-- Presence is independent of liveness: an observed absent row is covered,
Lang/StdHole.lean:64:but an omitted point is not. Keys are rows under self, never cell pins. -/
Lang/StdHole.lean-65-def holePointCovered : Term :=
```

**Tombstone pin is a real pin, and a matching seen-pin passes.** `git --git-dir=… grep -n -A 6 "What a pin asserts" 6eb92fe -- Kernel/World.lean` and the `touchCheck` site:

```
Kernel/World.lean:342:/-- What a pin asserts about a cell id's entry (KERNEL-54): absence, a tombstone, or a live cell's
Kernel/World.lean-343-version and bytes, three distinct digests (one domain each). -/
Kernel/World.lean-344-def pinOf (E : Env D) : Option Entry → D
Kernel/World.lean-345-  | none => E.hash domAbsent ByteArray.empty
Kernel/World.lean-346-  | some .tomb => E.hash domTomb ByteArray.empty
Kernel/World.lean-347-  | some (.live c v) => E.hash domCell (…)
```

```
Kernel/World.lean:995:the pin is checked against its ENTRY (the one staleness refusal: absent, tombstone and live are three
Kernel/World.lean-1000-  let cur := w.entry E x.cell
Kernel/World.lean-1001-  req (pinOf E cur = x.seen) (.stale x.cell)
Kernel/World.lean-1003-  | .keep, _ => pure none
```

`live` is `none` on a tombstone (`Kernel/World.lean:774–778`). `touchesOf` maps every signed pin to a touch (`Kernel/Receive/Call.lean:478–480`).

**Consumers and the GREEN gate.** `git --git-dir=… grep -n -E "p8Data|p8World|p8Available|p8Rows|p8Session|…" 6eb92fe -- '*.lean' '*.md'` hits only `Lang/Journey.lean`, `Lang/Journey/Main.lean:14`, and `decisions/lang.md:5080,5220`. `git --git-dir=… grep -n "lang-journey" 6eb92fe -- gates/runs.tsv`:

```
gates/runs.tsv:22:lang-journey	(none) ; --hole-omitted-blocker-pin-admits	lang-journey: GREEN	--harness-control
```

`git --git-dir=… grep -c` / `grep -n "theorem"` on `Lang/Journey.lean` → `0`. `git --git-dir=… grep -n "theorem \|lemma "` on `Lang/Journey.lean` and `Lang/Journey/{Main,HoleChecks,Activity}.lean` → no output.

**Census listing inspected, not re-run.** `fold/diff-S2.txt` begins `before 53666 after 53652` / `vanished 17` / `new 3 type-digest changed 6 value-hash changed 6 module changed 0`, and every following name is `Nanodregg.Lang.Journey.p8*`.
