# IMPACT-C5 — repair over `selectHole`: which hypotheses a selection drops, and when a live candidate selects

Worker: CX-PROMO-2. 2026-10-22. Base: nano main `528c9a9` (C2+R3 landed `e33a9b1`, C3+C4(a) docstrings `528c9a9`).
Rulings: R-0038 (C5 is its own card: three statements, Grok's §3 mutations as plants). Spec read:
`promo/READ-C2-grok.md` §3. Artifacts: `promo/C5/`.

## 0. Answer first

- **Two theorems proved** (scratch `C5/T2.lean`, elaborated at `528c9a9`, no `sorry`, no error) [MEASURED]:
  `selectHole_hypotheses` (T2) and `selectHole_live_selects` (T4), statements unchanged from IMPACT-C2 §6.
- **Both plants measured** (Grok §3), each: teeth (`Lang.Proofs.LiveJourney`) GREEN, `lang-journey` GREEN, a
  witness flips, the C5 file RED [MEASURED `C5/plants/`]:
  - T2's plant — a dead unused hypothesis pin that is a `.cell` is not appended to `strengthened`: witness
    `strengthened [0]` → `strengthened []` (the pin is dead and not strengthened: T2's ↔ is false).
  - T4's plant — refuse `guardBlocked` when the guard pin is live, before the guard runs: witness `index 0` →
    `refused holeGuardBlocked 0` (every T4 premise holds, no selection).
- **T3 (`selectHole_factor`) is a design fork, not a proof task** (§3). Proving `s.body = s.original` shows the
  strengthening factor is the identity on the run, and nothing reads the factor (C4(a): no receipt reader). **Default
  B: delete the factor from the run path and the receipt** (`factorHole`, `HoleSelection.{context, filling,
  embedding, original}`; `body := c.body`): Grok's T3 plant becomes impossible by construction instead of guarded by
  a theorem. Alternative A: keep it, compute the embedding in the same fold as the context, prove T3. ROOT rules.
- **Price.** No landed theorem gains a hypothesis under A or B. A: 0 statement changes. B: `selectHole_origin` and
  `instantiateHoles_sources` change `s.original` to `s.body` (a renamed field, same meaning); three node lemmas and
  four journey/teeth projections are rewritten (§3.2). No wire byte moves either way (a selection receipt is never
  encoded) → `lang:` fast.
- **Deployed refactor in both:** `changedHypotheses`'s step becomes a named `def` (`hypothesisStep`) so the proofs
  read the deployed step itself (today the scratch proof re-states it and a mutation reds the restatement's `rfl`, not
  the false statement: the T2 plant's RED is at that `rfl` [MEASURED `C5/plants/pT2-thm.log`]). Behaviour identical;
  journey byte-identical is the check.
- **Count:** T2 + T4 + three private fold/inversion lemmas = +5; B deletes `selectHole_nodes`, `factorHole_nodes`,
  `factor_fold_nodes` (−3) → net +2. A: +6 (T3 and its fold lemma(s), estimate) → net +6 or more.

## 1. The statements [MEASURED: elaborated and proved, `C5/T2.lean`]

Objects: `selectHole`, `changedHypotheses`, `runHoleGuard`, `supportLive`/`supportObserved`/`supportPinned`
(`Lang/LiveHoles.lean`). Placement: `Lang/Proofs/LiveHoles.lean` after `revoked_support_refused`.

```lean
/-- T2: a selection strengthens away EXACTLY the hypotheses whose pins do not hold, and the selected code uses none. -/
theorem selectHole_hypotheses (hs : selectHole digestOf look rv self h = .ok s) :
    ∃ c, h.code[s.index]? = some c ∧ s.original = c.body ∧
      ∀ x p, h.hypotheses[x]? = some (some p) →
        (x ∈ s.strengthened ↔ supportLive digestOf look rv self p = false) ∧
        (supportLive digestOf look rv self p = false → Term.usesVar x c.body = false)

/-- T4: when the row names `i`, code `i`'s supports are observed and hold, every hypothesis pin is observed and every
used one holds, and the guard runs to `true` on its observed pin, the hole selects `i` at the row's version. -/
theorem selectHole_live_selects
    (hrow : holeRow rv self h.selectionRel h.selectionKey = .ok (some (.row amount bytes ver)))
    (hdec : Wire.decodeData .nat bytes = .ok (.nat i)) (hc : h.code[i]? = some c)
    (hsup : ∀ p ∈ c.supports, supportObserved digestOf look p = true ∧ supportLive digestOf look rv self p = true)
    (hhyp : ∀ x p, h.hypotheses[x]? = some (some p) →
      supportPinned digestOf look rv self p = .ok () ∧
      (Term.usesVar x c.body = true → supportLive digestOf look rv self p = true))
    (hgp : ∀ p, h.guardPin = some p → supportPinned digestOf look rv self p = .ok ())
    (hguard : run [] Bounds.stackMax Bounds.holeGuardFuel 0
      (State.init h.guard [.bool (h.guardPin.all (supportLive digestOf look rv self))]) = .value (.bool true) used) :
    ∃ s, selectHole digestOf look rv self h = .ok s ∧ s.index = i ∧ s.version = ver
```

(Under B, T2's `s.original = c.body` reads `s.body = c.body`.) Successors (IMPACT-C2 §1): T2 of
`strengthening_sound`, `suspended_sound`'s hypothesis arm, `hyp_var_cites`; T4 of `judge_verified_iff` (←) and
`select_ok`. Together with `selectHole_origin` they are the deployed `selectHole_judge` without a judge: T4 is the
completeness half, `selectHole_origin` + T2 the soundness half.

## 2. The plants [MEASURED `C5/plants/`, script `C5/plant5.sh`, witnesses `C5/Witness.lean`]

| plant (edit to `Lang/LiveHoles.lean`) | teeth build | `lang-journey` | witness at tip → under plant | C5 file |
|---|---|---|---|---|
| T2: in `changedHypotheses`, a dead unused `.cell` pin → `.ok removed` | GREEN | GREEN | `ok strengthened [0]` → `ok strengthened []` | RED (at the restated step's `rfl`; §0 refactor moves it to the false conjunct) |
| T4: in `runHoleGuard`, `if h.guardPin.any supportLive then throw guardBlocked` | GREEN | GREEN | `ok index 0` → `refused holeGuardBlocked 0` | RED (`selectHole_live_selects`, the guard step) |

Witnesses: T2 — `declaration` with hypothesis 0 (the unused bool) pinned as `.cell` of a tombstoned cell (77),
selection 0; T4 — `declaration` with `guard := .bool true`, guard pin live (`blocker := some 1`), selection 0. Each
plant was restored and rebuilt GREEN after (`*-restore.log`). The exe was relinked under each plant (lesson 3:
"Built lang-journey" counted).

## 3. T3 — the fork

### 3.1 What T3 would prove, and what it shows

`selectHole_factor (hchk : h.check Δ = .ok ()) (hs) : HasType Δ s.context s.filling h.ty ∧ s.body = s.original`.
Its second conjunct says the run's body (`renameVar embedding (factor of c.body)`) IS the ROM code. So on every
live path the factor computation returns its input; its only other outputs (`context`, `filling`, `embedding`) are
receipt fields, and nothing reads a receipt (LANG-75.4). The deployed effect of strengthening is entirely T2: a dead
UNUSED hypothesis does not block the selection. The factor is a no-op on the run kept for a certificate nobody checks.

### 3.2 B (default): delete the factor

- `Lang/LiveHoles.lean`: delete `factorHole`; `HoleSelection` loses `context`, `filling`, `embedding`, `original`;
  `selectHole` returns `body := c.body`; the provenance check reads `s.body.digestLits`.
- `Lang/Proofs/LiveHoles.lean`: `selectHole_origin` `s.original = c.body` → `s.body = c.body`;
  `instantiateHoles_sources` `s.original.digestLits` → `s.body.digestLits`; delete `factor_fold_nodes`,
  `factorHole_nodes`, `selectHole_nodes` (now `rfl`-trivial); `resolutionMax_committed` re-proved from
  `selectHole_origin`.
- Teeth (`Lang/Proofs/LiveJourney.lean`): `selected_uses_context` projects `(s.strengthened, usesVar 1 s.body)`;
  `strengthening_factor` becomes `(s.strengthened, s.body) = ([0], .var 1)` (its `inferE` conjunct has no object);
  `replacement_filling` projects `(index, strengthened, body) = (2, [0, 1], .nat 9)`; `kept_context`,
  `alternative_same_filling`, `used_hypothesis_suspends`, `strengthening_uses_argument` unchanged.
- Journey rows "strengthened-context" (`Journey/Contextual.lean:137`) and "LP strengthened over deployed ROM"
  (`Journey/ContextualReceive.lean:131`) check `s.strengthened = [0] ∧ s.body = .var 1`; row TEXT unchanged.
- The CMTT strengthening (`t ≡ t₀[π]`) stays where it is a theorem over real terms: `langLaws.strengthen_lemma`,
  `strengthen_factor`, `hasType_unshiftAt_live`.
- Grok's T3 plant (a second kept variable mis-embedded) has no object to mutate.

### 3.3 A: keep the factor, prove T3

Compute the embedding in the factor's own fold (`(ctx.eraseIdx x, renameVar (lowerIdx x) t, emb.eraseIdx x)` from
`(h.ctx, c.body, List.range h.ctx.length)`) instead of `(List.range n).filter (!removed.contains ·)`: one fold, the
index list erased in lockstep with the context (today two computations of "which positions remain"). Then T3 is an
induction with the invariant "typed at the current context, re-embeds to `c.body`" (`hasType_unshiftAt_live`,
`renameVar_renameVar`, `getElem_eraseIdx`). Plant: Grok's (two kept variables after one strengthening; no tooth has
that shape). Cost: the deployed fold changes shape (behaviour identical, journey the check), +1–2 lemmas, and the
factor stays on the run as a no-op whose correctness is a theorem.

**Why B is the default:** law 1 and the doctrine's "never keep a no-op": A spends a theorem proving that deployed
work returns its input; B deletes the work. A is right only if the receipt's typed factor is going to be READ
(an audit row, a kernel record of selections) — then A's fold is the right shape and T3 its theorem. No such reader
exists or is planned before P7.

## 4. Gates and landing

`lang:` fast (no wire: a `HoleSelection` is never encoded; no codec vector, bundle or package id moves) + build of
`Lang.Proofs.LiveHoles`, `Lang.Proofs.LiveJourney`, `lang-journey`; journey byte-identical (B: identical output, the
two rows' checks rewritten, same text); plants re-run on the landed shape with the C5 theorems IN the module (the
plant must red `Lang.Proofs.LiveHoles`, by name); `gates/check.py`; digest diff under the map (B: RENAMES none;
RESTATES `selectHole_origin`, `instantiateHoles_sources` (field `original` → `body`, meaning identical: `body =
c.body` by definition); DELETES the three node lemmas). Decision `### LANG-75.5`.

## 5. Reader questions (defaults in bold)

1. T3: **B — delete the factor** (§3.2) — or A (§3.3).
2. The step refactor (`hypothesisStep` named in `Lang/LiveHoles.lean`): **yes** (the proofs then read the deployed
   step; a plant reds the false conjunct, not a restatement) — or keep the restated step in the proof module.
3. T4's `hguard` premise states the machine run (`run … = .value (.bool true) used`) rather than an abstract "the
   guard holds": **keep** (it is the deployed object; `guardFault`/`guardBlocked` are its two other outcomes).
