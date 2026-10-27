# IMPACT-C7 · acyclicity over the pin graph (`support_precedes` over `touchCheck`)

CX-PROMO-3, 2026-10-22, against nano main `100ad08` (hbox `wt/promo`, clean). Plan: PROGRAM-20261022.md §3 P2 C7, §8.2.
Grant: R-0042 (Kernel/Proofs/** proof-only, lands ONLY with its plant; else a docstring on the hole model).
Artifacts: `promo/C7/` (scratch statement + proof, both plants' diffs and whole logs, restore logs).

**Verdict: DOCSTRING.** The plant goes red, but by the name of a theorem already landed (`touchCheck_pin`), upstream of
any module that can hold `support_precedes`. The statement composes four landed facts, and nothing reads it: no hole's
support can name another hole's selection. Theorem count for C7: 0. The criterion is §8.2 as R-0031 applied it to C9.

## 1. The statement, as built (scratch, GREEN at 100ad08)

Built at the end of `Kernel/Proofs/Versions.lean`, because it needs the private `touchCheck_adv`. `lake build
Kernel.Proofs.Versions`: EXIT 0 (`C7/scratch-green.log`). Removed again; the tree is at HEAD.

```lean
theorem support_precedes {E : Env D} {w w' w'' : World D} {t : Turn D} {l : List (Step D)}
    (hf : w.CellsFit Cell.Fits E) (h : World.admit E w t = .ok w') (hl : World.fold E w' l = .ok w'')
    {x : Touch D} (hx : x ∈ t.touches) (hact : x.act ≠ .keep) :
    x.seen = pinOf E (w.entry E x.cell) ∧
      (x.seen ≠ pinOf E (w''.entry E x.cell) ∨
        CollidesAmong E.hash [pinPre E (w.entry E x.cell), pinPre E (w''.entry E x.cell)])
```

**Nano object.** A pin the receiver checks (`Touch.seen`, from `Unsigned.pins` via `touchesOf`, `Kernel/Receive/Call.lean:479`)
on a cell the Turn writes or retires. A Lang `.cell g` support is such a pin: `cellLive look g` reads `pinned E w pins`
(`Call.lean:422`), which is `w.live` at the World before the Turn. The statement says the pin names the entry before the
Turn, and that no World from the post-state onward holds that pin again, except through a collision among the two pin
inputs compared. The collision list is explicit (`CollidesAmong` over a two-element list), so the disjunct is not the
pigeonhole-vacuous shape.

**Why "height" is not in the statement.** The kernel keeps no "written at height" record for an entry. The order that
exists is `EAdv`, each cell's entry advancing strictly along the fold (`Versions.lean:59`, `fold_entryStep :170`). The
plan's "well-founded by height" is that order in disguise: an edge goes from the entry before the Turn to an entry
strictly after it.

**Proof (READ, as built).** `touchCheck_pin` (`Kernel/Proofs/Admit.lean:70`) gives the first conjunct. `touchCheck_adv`
(private, `Versions.lean:81`), carried through `commit` (a copy of `admit_entryStep`'s touched branch, `:116`), gives
`EAdv` (pre, post). `fold_entryStep` + `eAdv_trans` carry it to w''. Then `pinPre_adv_ne` + `pinOf_eq_pre` give the
second conjunct. This is `stale_behind_forever` (`:240`) with w₀ = the pre-state, plus `touchCheck_pin`. It contains no
fact of its own: two new private lemmas (`touchCheck_acts`, `admit_touch_adv`) and a composition.

## 2. The plant the brief names, built and run first

`C7/plant-post-entry.diff`: `touchCheck` checks the pin against the entry the act LEAVES. A keep still compares against
`cur`; a write compares against `.live post (ver+1)`; a retire compares against `.tomb`. Built with `lake build
Kernel.Proofs.Versions` and the scratch theorem appended (`C7/plant-post-entry.log`, whole):

| module | line | name | why it is red |
|---|---|---|---|
| Kernel/Proofs/Admit.lean | 74 | `touchCheck_pin` | statement FALSE under the plant (the pin now equals the post-entry's) |
| Kernel/Proofs/Admit.lean | 162 | `touchCheck_stale` | statement FALSE (a pin that is stale against the pre-entry now passes) |
| Kernel/Proofs/Admit.lean | 459 | `touchCheck_some` | proof script only (its statement still holds) |

Lake stops at `Kernel.Proofs.Admit` (44/70). `Versions` imports it, so `support_precedes` never elaborates. **The plant
cannot red `support_precedes` by name.** The red it produces belongs to `touchCheck_pin` ("a touch that passes saw what
the signer saw"), which has been landed since KERNEL-54. Any home for `support_precedes` has to import `admit_ok` /
`touchCheck_pin`, so this is not a question of where the file sits.

**The other mutation class** (`C7/plant-no-advance.diff`). A write keeps the version (`.live post ver`), which is the
only other way the second conjunct fails. It stops at `Kernel/Proofs/CellsFit.lean:165` (`touchCheck_cellFit`), a proof
script whose statement stays true. So it measures nothing further. INFERRED: past that point it falsifies
`stale_behind_forever` (write then write-back gives the old pin again) and `touchCheck_adv`, both of which are upstream
of or equal to the new statement.

Restored after each plant: `lake build Kernel.Proofs.Versions` EXIT 0 (`C7/restore.log`, `C7/restore2.log`). `git
status` clean.

## 3. The plan's §8.2 refuter: is it a rename of `touchCheck`?

Yes, up to composition. At the `touchCheck` grain, the statement's content is `touchCheck_pin ∧ touchCheck_adv`: the
definition read twice (check against `cur`, then build the post from `cur`). At the fold grain, it is
`stale_behind_forever` started at the pre-state. Every mutation that falsifies it also falsifies a landed statement that
reds first. Grok's fourth question gets the answer "the post-entry comparison", and that mutation is already
`touchCheck_pin`'s tooth.

## 4. The consumer: none today (both hole layers)

- **ROM layer** (`SupportPin`, `Lang/HoleROM.lean:7`). A `.row rel key ver` support is a row of the hole object itself,
  read through `holeRow rv self`. A `.cell id` support says only that the cell stands (`cellLive`).
- **Row machine** (`Std.hole`, `Lang/StdHole.lean`). A support `(cell, pin)` is looked up in the hole's OWN `facts` rows
  ("Keys are rows under self, never cell pins", `holePointCovered`). Activities design card F ruled option (2), "a
  support is never a hole's row", and its finding 8 enforces it by the relation index. Since E1 the cell a fact names is
  checked for liveness only; the fact's `pin` is the poster's claim, compared only with the candidate's (`holeProbePoint`).
  So a candidate MAY name another hole object's cell, but what it asserts is that the cell stands, never what the cell
  selected. Two holes that name each other's cells form no justification cycle. Every support is a kernel fact of the
  World before the Turn.
- So the deployed support graph has depth one. The trigger for a theorem is card F option (3), already dated in
  `ACTIVITIES-DESIGN-20261022.md:576`: "a row that needs a hole to cite a hole". That row would make supports
  transitive through selections, closed to `callDepthMax`, and give `support_precedes` a reader over selection rows
  (`rowStep_pin`, `Kernel/Proofs/Rows.lean:498`, beside `touchCheck_pin`). No card in PROGRAM-20261022.md P3–P7 is that
  row. `cv task list` holds no task for it (searched); one is opened at landing (Q3).

## 5. Premise price

0. Nothing lands in Kernel. No landed statement changes.

## 6. What lands: one docstring, `lang:` fast, decision LANG-75.7

**Home of the decision: `decisions/lang.md` `### LANG-75.7`, not a KERNEL number.** The convention read: the program's
card list lives in `## LANG-75`, and every card so far has been a `### LANG-75.n` (LANG-75.2 recorded its kernel-side
docstring there and only appended a paragraph to KERNEL-60 under R-0030). KERNEL-n entries are decisions about kernel
definitions. C7 changes none, and with the docstring verdict it touches no Kernel file. If ROOT rules THEOREM instead,
the home is `Kernel/Proofs/Versions.lean` (the private `touchCheck_adv`), CROSS-LAYER: KERNEL under R-0042. The
decision would still be LANG-75.7, with a one-line pointer appended to KERNEL-54 (the pin-reads-the-entry decision).

Docstring, appended to `SupportPin`'s in `Lang/HoleROM.lean` (the hole model):

> Every support precedes the Turn that reads it (C7, LANG-75.7). The receiver judges each pin on the World before the
> Turn (`touchCheck_pin`; a row pin on its row as it stood before the Turn, since a Turn's row slots are distinct, `rowStep_pin`), and an admitted write leaves its cell
> strictly past that entry (`stale_behind_forever`). So no Turn's support names what the Turn writes. A row support is
> a row of this hole object, and a cell support says only that a cell stands. No support names another hole's
> selection (activities card F (2)), so there is no graph of holes to be acyclic. A theorem lands with card F (3),
> the first row that needs a hole to cite a hole.

The commit message plant line says the plant was built and run, and that it reds `touchCheck_pin` / `touchCheck_stale`
upstream (promo/C7). Journey, vectors, statements: unchanged (comment only).

## 7. Reader questions (defaults)

- Q1: is DOCSTRING right, or is the composition worth a name (a theorem that is a corollary, with a red that belongs to
  another theorem)? Default DOCSTRING, per §8.2 and R-0031.
- Q2: is LANG-75.7 the right home? Default yes.
- Q3: should the docstring's trigger also be a `cv task`? Default yes, opened at landing: "C7 theorem: support_precedes
  over selection rows, on the first card where a support is another hole's selection row".
