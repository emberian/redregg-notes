# ACTIVITIES — lane log and handoff

## ACTIVITIES-1 (real 2026-10-20; LANG-66/67)

Scholar → deputized prototyper (Ember, confirmed to ROOT). Design: `redregg/work/ACTIVITIES-DESIGN-20261022.md`
(§1–8 the first design, partly REFUTED; §9–9.4 what was built, measured, corrected and landed — read §9 first).
Proposal: `redregg/work/ACTIVITIES-PROPOSAL-20261022.md`. Decision entries: nanodregg `decisions/lang.md` LANG-66, LANG-67.

**Landed on nanodregg main (each `lang:`, PRE-PUSH FAST GREEN, no wire/re-id/re-genesis, no landed premise or
statement changed):**
- `1e94183` — CMTT core (`Lang/Contextual/Core.lean`; `Lang/Proofs/Contextual/{Typing,Core}.lean`): well-scoped
  simply-typed contextual modal type theory, box closed to its ambient context, explicit substitutions, `subst_lemma`,
  `msubst_lemma`, `strengthen` (`t ≡ t₀[π]`), exact checker, weak-head `Step` + `subject_reduction`, blocked-metavariable
  teeth; + the guarded contextual closure (`Lang/Contextual/Closure.lean`; `Lang/Proofs/Contextual/{Closure,Experiments}.lean`)
  over `CalculusData` + `CalculusLaws D HasTy : Prop`: versioned tokens, interfaces with polarity, retained candidates
  with reasons, five outcomes, `Derivable` ≠ `Available`, conditional soundness, `repair_agrees_from_scratch` under
  `Coherent`, locality with the re-judged log, `withdraw_never_refutes`, `executed_prefix_blocks_replan`,
  `provenance_iff` (world-free polynomial), the EIGHT EXPERIMENTS as theorems; + `Lang/Journey.lean` rows LH0–LH11 (the hole
  as a surface package through the receivers; `lang-journey` GREEN 704 rows).
- `56c79a0` — the real instance: `Lang/Contextual/CoreCalculus.lean` (`cmttData`, `holeEnv`) +
  `Lang/Proofs/Contextual/CoreInstance.lean` (`theorem cmttLaws`, every law discharged; `bell_template_toy`).
- `6bf2585` — the reader's last fixes: `tpl0_typed`, `tplH_typed`, `s1_derivable` (a concrete FILLED closure is Derivable),
  `session_preserves_tpl`, `weaken_never_var`; Core's `beq` + four private theorems replaced by structural `decEq`.
- `8c31ace` — open protocols (`Lang/Contextual/{Protocol,NanoBridge}.lean`; `Lang/Proofs/Contextual/{ProtocolTyping,
  Protocol,Negotiation}.lean`, 101 theorems): `Prot := ret | call | hole`, Ω interfaces with polarity/affine tokens/
  obligations, `HasProt` (Φ an upper bound), `Started`/`Dispatched`, `Open.replan` + guard `Replan`, admission separate
  from typing; the four families; `foresight_iff_names_separate` (scope is a NAMING discipline); the two-cell one-use-
  capability negotiation with its four changes; `nano_interp_runs` = HOSTING-37's `interp_runs` re-derived.

**The reader pattern (keep it).** One adversarial reader per theory, read-only, briefed with KERNEL-56's rule ("a disjunct
provable from the premises alone is vacuous"), required to name PER THEOREM which side of each iff and which ∃ witness it
checked, two passes + skims: READER-CONTEXTUAL `a883dc3fb9dca28c8` (Core+Closure, 235 theorems, found two HIGH
vacuities a green build could not: a `drop := id` instance, then a `uses ≡ false` instance satisfying the strengthening
laws → the anchor fields `weaken_avoids`, `var`/`lookup`/`hasTy_var`/`uses_var`); READER-PROTOCOL `aeb565a5931fae761`
(Protocol, 90 theorems; found the prose claim "a filling cannot depend on a response" FALSE → `foresight_iff_names_separate`).
Findings go back to the LANE THAT OWNS THE FILE (the veteran), never to a fresh agent.

**Two gates that refused, so the successor avoids both.** (1) `gates/closure.py` C3/C4: a def module exports NO
Prop-typed declaration; a proof module (a `Proofs` path component) exports ONLY Prop-typed ones (private helpers allowed
either side); a def module never imports a proof module. A Type-valued def that packages proofs can live nowhere: split
DATA (def module) from LAWS (`structure … : Prop`, proof module) — the `Env`/`Ctx.Lawful` pattern; judgments
(`HasTy`, `Step`, `HasProt`, `Started`…) live in proof modules; fixtures `private`. Run `python3 gates/closure.py .`
(→ `closure: ok (0)`) BEFORE `scripts/commit`. Also: bare `lake env lean` does NOT apply the lakefile's `leanOptions`
(`autoImplicit=false`, `warningAsError=true`); check with `SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build lake build
<module>` or pass the options. (2) SIZE lines: every metric that rises needs `SIZE: <metric>: <why>` in the message —
refused twice for `Lean lines (deployed)` (a def module grew) and `max dependents of a non-foundation module`
(`NanoBridge` imports `Hosting.Resident.Trace`). Pre-compute with `python3 gates/size.py --write .` then `git diff SIZE.md`.
Commit messages go through a FILE (`-F`): zsh substitutes backticks in `-m`.

## ACTIVITIES-2 HANDOFF

**The quest.** The `Std.activity` / `Std.hole` generators that make the Bell an INSTANCE of the landed closure theory
(design §3.2–3.3, cards A–F in §7, with §9's corrections, which OVERRIDE §3–4 where they conflict). Not started; the
successor builds, ACTIVITIES-1 did not touch it.

**Build order (one `lang!` day, in this sequence):**
1. `Std.activity` generator in `Lang/Std.lean` beside `quorum`/`windowed`/`machine`: a relation `waits` (the continuation
   ROW; key `(notBefore nat)(agent digest)` as LANG-58; value `rec {plan : sum plans, captured : K, dispatched : bool,
   answered : optTy (sum resps)}`), one `resume_<plan>` method per plan whose `case` on the response is the edge, a
   `start_<plan>` that inserts the row; guard `waiting` = LANG-59's `rung` plus the equalities `new.plan = old.plan`,
   `new.captured = old.captured` (a resumption never rewrites what was captured; exactly-once by the guard). The PHASE
   lives in the `waits` ROW, never in state (LANG-58's refutation; §9 correction 4). Meaning theorems over `BigStep`
   in `Lang/Proofs/Std.lean`/`StdTeeth.lean`, LANG-48 (6)'s `pending_fill_binds` shape (both directions).
2. `Std.hole` generator over it: relation `candidates` (`value : V`, `status : sum {verified, suspended bytes, pruned bytes,
   conflict bytes}`, two supports as `(cell, pin)` records, `by`), relation `facts` (assumption TOKENS posted/re-pinned/
   withdrawn only by their poster — the §9 restatement: a support is a ROW ON THE HOLE OBJECT, never a pin on another
   cell, because a method sees no cell pins and reads rows under `self` only), methods `propose/prune/select/accept/
   rejudge/retire`; the METHOD computes the status from the clause and the guard `proposed` RE-CHECKS it (a guard returns
   only ok|refused; §9 correction 6). `Hole.ob` (below) is the hand-written instance to generate from.
3. The bridge theorem: the hole package as a model of `Lang/Contextual/Closure.lean` — a `CalculusData` instance over Lang
   data + rows (`Tm := Data`, `check := the clause`, `uses/drop/strengthen/weaken` trivial-but-anchored? NO: §9.2 finding 1
   forbids a degenerate instance; if the instance cannot discharge `weaken_avoids`/`uses_var` honestly, state the model
   over a RESTRICTED `CalculusLaws` (data-only laws) and say so) and `select`'s admission ⇒ `Available`.
4. The Bell re-cut as `Std.activity`'s instance: `world/resident/Bell.ob` re-emits (HOSTING's path: CROSS-LAYER with
   HOSTING's yes), the Bell re-ids, LB0 re-pins ("the Bell became an activity"), LB rows re-cut, `Hosting/Resident/Bell.lean`
   `Shape.read` and `launcher/tests/resident_bell.rs` cut over in the same commit (HOSTING-11's pattern). Keep
   `answerArgTy` or restate Hosting's ~6 statements (§4.5).
5. Journey rows LH0–LH11 re-pointed at the generated package (today they read `holeText`, the hand text).

**Real signatures to build against (pasted from main `8c31ace`):**

`Lang/Contextual/Closure.lean`:
```lean
structure CalculusData where
  Ty : Type
  Ctx : Type
  Tm : Type
  tmEq : DecidableEq Tm
  msubst : (Nat → Option Tm) → Tm → Tm
  check : Ctx → Tm → Ty → Bool
  uses : Tm → Nat → Bool
  drop : Ctx → Nat → Ctx
  strengthen : Nat → Tm → Tm
  weaken : Nat → Tm → Tm
  var : Nat → Tm
  lookup : Ctx → Nat → Option Ty

structure Iface (D : CalculusData) (E : Type) where
  name : Nat
  ctx : D.Ctx
  ty : D.Ty
  hyps : List (Nat × Token)
  hyps_real : ∀ h ∈ hyps, (D.lookup ctx h.1).isSome = true
  guard : E → D.Tm → Bool
  budget : Nat
  chooser : Party
  acceptor : Party

structure Candidate (D : CalculusData) where
  filling : D.Tm
  supports : List Token
  blockers : List Token
  cost : Nat
  by_ : Party
  status : Status

inductive Edit (E : Type) where
  | withdraw (t : Token)
  | assert (t : Token)
  | setEnv (e : E)

inductive Status where
  | verified
  | suspended (missing : List Token)
  | pruned (by_ : List Token)
  | conflict (ev : Evidence)
  | uncovered (cost budget : Nat)

def judge (I : Iface D E) (w : World E) (c : Candidate D) : Status :=
  if D.check I.ctx c.filling I.ty = false then .conflict .illTyped
  else if I.guard w.env c.filling = false then .conflict .guardFails
  else if (c.blockers.filter w.live).isEmpty = false then .pruned (c.blockers.filter w.live)
  else …   -- Closure.lean:230

def select (w : World E) (p : Party) (u i : Nat) (cl : Closure D E) : Except Refusal (Closure D E)   -- :318
def propose (w : World E) (u : Nat) (c : Candidate D) (cl : Closure D E) : …                        -- :306
def fill … ; def rejudge (w : World E) (u i : Nat) (cl : Closure D E) : Closure D E                   -- :336, :391
def repair (w : World E) (e : Edit E) (cl : Closure D E) : Closure D E × List Outcome × List (Nat × Nat)   -- :478
```
`Lang/Proofs/Contextual/Closure.lean`: `structure CalculusLaws (D : CalculusData) (HasTy : List (HoleDecl D.Ctx D.Ty)
→ D.Ctx → D.Tm → D.Ty → Prop) : Prop` with fields `msubst_lemma check_sound check_complete strengthen_lemma
strengthen_factor weaken_avoids hasTy_var uses_var` (exact statements in that file, lines after the structure);
`def Template.Typed (tpl : Template D E) (HasTy) : Prop`; `Derivable HasTy cl`, `Available w cl`, `Coherent w cl`.

`Hosting/Resident/Run.lean:281-310` (the proved continuation structure the activity generalises):
```lean
inductive Prog (α : Type) where
  | done (a : α)
  | cmd (c : Cmd) (k : Except String Reply → Prog α)
  | keep (r : Ring) (t : ByteArray) (k : Bool → Prog α)
  | forget (k : Bool → Prog α)
  | ask (r : Ring) (q : Broker.Ask) (k : AskEnd → Prog α)
  | say (s : String) (k : Prog α)
structure Handler (M : Type → Type) where
  cmd : Cmd → M (Except String Reply)
  keep : Ring → ByteArray → M Bool
  forget : M Bool
  ask : Ring → Broker.Ask → M AskEnd
  say : String → M Unit
def Prog.interp {M} [Monad M] {α} (h : Handler M) : Prog α → M α
```
`Hosting/Proofs/ResidentRun.lean:700`:
```lean
theorem interp_runs (o : Oracle) {α : Type} (p : Prog α) (n : Nat) (es : List Ev) :
    ∃ es', ((p.interp (recorder o)).run (n, es)).2.2 = es ++ es' ∧
      Runs p es' ((p.interp (recorder o)).run (n, es)).1
```
(`nano_interp_runs` in `Lang/Proofs/Contextual/Protocol.lean` re-derives exactly this from `interpret_record`.)

`Hole.ob` (the hand-written instance; the lane's `world/hole/Hole.ob`, and inline as `holeText` in `Lang/Journey.lean`):
```
(package
  (type Status (sum (pruned bytes) (suspended bytes) (verified (rec))))
  (type Support (rec (cell digest) (pin digest)))
  (state (rec (accepted bool) (acceptor digest) (cap nat) (chooser digest) (closes nat) (selected (option digest))))
  (rel candidates (key (cand digest))
    (val (rec (by digest) (s0 (option Support)) (s1 (option Support)) (status Status) (value nat))) (limit 64) (guard proposed))
  (rel facts (key (cell digest)) (val (rec (by digest) (pin digest))) (limit 64) (retract) (guard posted))
  (method post …) (method repin …) (method unpost …)        ; a fact is its poster's token
  (method propose (arg (rec (cand digest) (s0 (option Support)) (s1 (option Support)) (value nat))) (edits 1) …)
  (method prune (reads (candidates (points 1))) (arg (rec (cand digest) (why (bytes 1 64)))) (edits 1) …)
  (method select (reads (candidates (points 1)) (facts (points 2))) (arg (rec (cand digest))) …)   ; refuses support0 moved | withdrawn | accepted | notChooser
  (method accept …)
  (guard proposed …) (guard posted …)
  (law shape (on invoke m (all ((== new.cap old.cap) "cap") …)) (else ok)))
```
Measured on it (rows LH7/LH7b/LH7c/LH8): a re-pinned or withdrawn support refuses `select` BY NAME, the method speaking
first; with the method's pin check planted out, the same select over the old view is `rejected stale` by the KERNEL
(two judges). select of the surviving candidate: 139 required steps / 179 ticks.

**Deferred cv tasks (each with what it needs):**
- `01a1587d-9a98` first-class substitutions (Cave–Pientka): a `Sub` type mutual with `Tm`, closures vs projections;
  needs a redesign of `Tm` in `Lang/Contextual/Core.lean` and re-proofs of `subst_lemma`/`msubst_lemma`/`subject_reduction`;
  trigger: a repair hint parametric in a substitution.
- `01a158c0-dd90` LANG-67 follow-up: a non-trivial `accepts` instance + refusal tooth (acceptance is exercised by no
  instance), and a SET-valued buyer guard so `separate_witnesses_over_substitutions`'s emptiness is a clash of two conditions.
- `01a158c0-ddae` law-8 split of `Lang/Proofs/Contextual/Closure.lean` (1,510 lines): Judge / Repair / Soundness /
  History / Stability; names unchanged; a reader confirms only that names moved.
- `01a158c0-ddbf` the generators above (this handoff's quest): needs §9's corrections read first.

**Worktree state.** `/tank/dregg-build/claude-lanes/activities` on hbox: a `git worktree` of nanodregg at main
(`8c31ace` at handoff; `scripts/commit` moves it on each landing), clean except: `lane-logs/` (commit messages and logs
`commit{1,1b,2,3,3b,4,4b}.log`, `lang-journey.out`, `lang-hole.out`, `plant-pin-equality.out`, the three lanes' logs
`cmtt-core.md`, `closure.md`, `protocol.md`, `JourneyHole.lean.txt` the lane-only driver, `Hole.ob.orig`/`Hole.plant.ob`)
and `world/hole/Hole.ob` (the DEMO; `world/` is HOSTING's, so it is NOT landed: its text landed inline as `holeText`
in `Lang/Journey.lean`, which is the landed form — the demo file stays in the lane for the successor's generator work
and becomes nothing on main; a `lang-hole` exe was removed before landing). Its `.lake` is a copy of the standing tree's
warm build plus the Contextual modules (about 1.1 GB; mine, deletable with the lane). Cargo: no Rust touched; no private
cargo target created. Build under `SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build lake build <modules>`.

**Parked sub-lanes (ids; my word on each):**
- CMTT-CORE `a888f90ed44334d88` — holds the whole Core/Typing/CoreInstance context (113 theorems, the MEnv redesign, the
  structural decEq). RESUME it for cv task `01a1587d-9a98` (first-class substitutions: it already named the two options)
  and for any Core change; retire otherwise.
- CLOSURE `a83d9a318939a86ad` — holds Closure/Experiments (89 + 40 theorems, the Data/Laws split, every reader fix).
  RESUME it for the law-8 split (`01a158c0-ddae`) and for the bridge theorem in build-order step 3; it knows which
  `CalculusLaws` field each experiment needs.
- PROTOCOL `aa81e09afb7452039` — holds Protocol/NanoBridge/Negotiation (101 theorems). RESUME it for `01a158c0-dd90`
  (accepts instance, set-valued guard) and for any multi-party extension inside the charter (two members, one writer).
- Readers `a883dc3fb9dca28c8` (Contextual) and `aeb565a5931fae761` (Protocol): resume for the next read of the same
  files (they hold their per-theorem records); a NEW theory gets a fresh reader.

**The one question I would want answered first.** Build-order step 3: can the hole package be an HONEST
`CalculusData`/`CalculusLaws` instance — i.e. what are `uses`/`drop`/`strengthen`/`weaken` for a Lang DATA filling
(a value, not a term with variables) such that `weaken_avoids` and `uses_var` are discharged non-degenerately — or is
the bridge stated over a data-only sub-structure of the laws? The reader's HIGH finding (a degenerate instance satisfies
the strengthening laws) means the generator's bridge must answer this before a single row is written, because the whole
point of the generators is that the Bell becomes an instance of the proved theory, not a lookalike beside it.

## ACTIVITIES-2 (real 2026-10-20; successor; quest cv 01a158c0-ddbf)

**Read (whole):** this log's handoff; design §3.2–3.4, §9–9.3; LANG-66/67; the 18 lane rules. Main on hbox is `7473d77`
(HOST-69 landed after `8c31ace`); the lane worktree sits at `8c31ace`, clean but lane-logs/ and world/hole/.

**First act — the handoff's question, as a measurement.** The honest instance is NOT over Lang DATA (a `Data` value has no
variables, so `uses_var`/`hasTy_var` cannot be discharged except by bolting a variable onto data — the lookalike the
reader refused). It is over Lang's DEPLOYED TERM: `Tm := Lang.Term` (de Bruijn `.var`, `Lang/Term.lean:44`), the real
checker `infer Δ Γ t` with `infer_iff : infer Δ Γ t = some T ↔ HasType Δ Γ t T` (`Lang/Proofs/Check.lean:227`),
`uses`/`weaken`/`strengthen` as a binder-aware variable rename (Core's `shiftAt/unshiftAt` ported to the 17 constructors,
`relocate_typed`'s mutual pattern in `Lang/Proofs/Relocate.lean:27`). A HOLE in a Lang term can only be a `ref n`
(`Term` has no `mvar`; `ref` is typed from `Δ[n]?`, `HasType.ref`), so hole `n` ↦ `Δ` position `n`
(name-indexed `ΔOf Ω`, the `holeEnv` move) and `msubst` = `fillRefs`. A `ref` carries no local context, so the instance's
`LangHasTy Ω Γ t T` holds only when every declared hole has `ctx = []`: the laws discharge honestly (var shift is real),
but `Template.Typed` templates have CLOSED holes, so `Iface.hyps = []` and the `strengthening` outcome is unreachable
from any Lang template — to be stated as a THEOREM (`langHasTy_closed_holes`), not prose. The contextual (Ψ ≠ []) route
needs `msubst` to see Ω (curried `fnOf Ψ A` holes, `lams`) = a `CalculusData` signature change; ROOT's fork if wanted.
Builder: CMTT-CORE `a888f90ed44334d88` resumed (it holds the shift/unshift/uses proofs this port mirrors).

**Step 1 design (`Std.activity`), decided while the measurement runs (READ at source: Std.lean 296–414, Surface.lean
740–810, Package.lean 150–200/384, LANG-48/58/59, the Bell's `.ob`):**
- The generator emits CORE terms like `machine`/`stepTo` (`Except StdRefusal`), assembled by the surface form
  `(activity cursor log (resumer clause) (plan p (arg K_p) (resp R_p) (start body) (resume body))…)` the way
  `(machine f init (methods …) edges…)` expands at Surface.lean:782–790 (law + step methods for undeclared labels).
- Rows, not state (§9 correction 4): TWO relations, as the Bell has: `cursor` (`pending`): `(agent digest)(notBefore nat)
  → rec {captured : sum{p : K_p}}`, limit, retract, guard `queued` (= the Bell's verbatim); `log` (`rings`): same key →
  `rec {answered : optTy (sum{p : R_p}), captured : sum{p : K_p}}`, limit, retract, guard `waiting` = LANG-59's `rung`
  with `beq text` replaced by STRUCTURAL equality on `captured`. The phase of a suspension IS `answered`.
- Methods, generated: `start_p {K_p}` = `check pre_p; done state'_p (insert cursor k {captured}) (insert log k {answered
  none, captured})`, `k = {agent req.agent, notBefore req.notBefore}` (LANG-58's key); `resume_p {agent, notBefore,
  response : R_p}` point-READS `rows.log.p0` (§9 finding 12: a method reads rows under self; the signer pins that row
  for the upsert anyway, so the read costs no extra pin and LANG-59 critique (5)'s re-send of ≤2000 bytes goes away),
  upserts `log k {answered some (inj p response), captured (from the row)}`, retracts `cursor k`, and the author's
  `resume body` computes the new state under the method binders (rows 3, state 2, arg 1, req 0); `retire {agent,
  notBefore}` retracts `log k`. The Bell = one plan `ask {text}` resp `bytes`, resumer `deq req.agent state.resident`,
  pre `state.open`.
- NEW shared primitive both generators need: `Std.eqData (T : Ty) (x y : Term) : Term`, structural equality of two data
  terms at a data type (records field-wise, sums by nested `case`; `eqAt` is its scalar case), with the meaning theorem
  `eqData_true : BigStep … (eqData T x y) (.ok (.bool b)) → Conforms dx T → Conforms dy T → (b = true ↔ dx = dy)`.
  The hole's `candidates` guard (`new.value = old.value` for a general `V`) is its second consumer.
- Meaning theorems (Lang/Proofs/Std.lean, the `Admits`/`runLaw` idiom at :186, `quorum_change` :593 the shape):
  `waiting_insert_iff`, `waiting_upsert_iff` (LANG-48 (6)'s both-directions form: admitted ↔ the signer is the
  resumer ∧ old present ∧ old.answered = none ∧ new.captured = old.captured ∧ new.answered = some _),
  `waiting_retract_iff`; run-level `resume_p` result = the upsert + the arm's state (StdRun's `stepTo_run_moves` shape).
- OWNERSHIP: `gates/OWNERS` says `Lang/` → LANG; my brief says `Std.*` is not mine without its owner's yes through
  ROOT. Raised with ROOT together with the first-question answer.

**First act MEASURED (real 10-20; built-unlanded in the lane worktree):** `Lang/Contextual/LangCalculus.lean` (def, 564 lines)
+ `Lang/Proofs/Contextual/LangInstance.lean` (proof, 808 lines, 47 theorems): `theorem langLaws : CalculusLaws langData
LangHasTy`, every law, none weakened (msubst_lemma ← `fillRefs_typed`; check ← `infer_sound/complete`; strengthen_lemma ←
`hasType_unshiftAt`; strengthen_factor ← `shiftAt_unshiftAt`; weaken_avoids ← `usesVar_shiftAt`; hasTy_var ← `HasType.var`;
uses_var by simp). `LangHasTy Ω Γ t T := (∀ d ∈ Ω, d.ctx = []) ∧ RefsDeclared Ω t ∧ HasType (ΔOf Ω) Γ t T`. Reach theorem
`langTemplate_no_hyps : Template.Typed tpl LangHasTy → ∀ I ∈ tpl.Ω, I.hyps = []`. Log lane-logs/act2-langcalc-1.log
(green, 0 warnings); closure ok (0); check.py all ok but `size` (SIZE.md regenerated by scripts/commit). Sent to ROOT with
the fork (A) closed-hole fragment now / (B) a `hole n σ` Term constructor, `lang!`) and the Std ownership question.
WAITING on ROOT for both before Std work.

**ROOT rulings (real 10-20):** FORK (A) now; `langTemplate_no_hyps` named in the decision text as the closed-hole fragment's
boundary; the three empty closure paths listed by name as EMPTY ON EVERY LANG TEMPLATE. (B) is Ember's card (below) + a
cv task. Ownership: `Lang/Std.lean`, `Lang/Proofs/Std.lean` are mine (no existing Std statement changes, no landed theorem
gains a premise, or name it); `Hosting/*` off-limits without the owner's yes through ROOT.

## (B) `hole n σ` in Lang's term language — a card for Ember (design fork; two honest shapes, the choice is scope)

**What (A) is.** The generators bridge the hole package to the closure theory over `Lang.Term` with every hole CLOSED:
`LangHasTy Ω Γ t T := (∀ d ∈ Ω, d.ctx = []) ∧ RefsDeclared Ω t ∧ HasType (ΔOf Ω) Γ t T`; a hole is a `ref n` (a closed
package reference: it carries no local context and no substitution). All eight `CalculusLaws` discharge non-degenerately
(`langLaws`), and `langTemplate_no_hyps : Template.Typed tpl LangHasTy → ∀ I ∈ tpl.Ω, I.hyps = []` is the boundary: on
EVERY Lang template the closure's `strengthening` outcome, its alternative-by-hypothesis outcome, and hypothesis-derived
supports (`effSupports`' second summand) are EMPTY.

**What (B) is.** CMTT's `u[σ]` as an 18th `Term` constructor `hole (n : Nat) (σ : List Term)`:
- `HasType` rule: `Δ' n = some (Ψ, A)` (holes in a name-indexed meta-env beside the package context Δ), σ checked
  pointwise against Ψ under Γ, the occurrence typed at A;
- `fillRefs` (`msubst`) at a hole with `σ n = some M` yields `subst σ M` (M typed under Ψ, closed otherwise);
- `LangHasTy` drops its `d.ctx = []` conjunct; `RefsDeclared` becomes "every hole occurrence is declared".
- Touched recursions, each one new case: `Term.decEq`, `inferE` (checker), `BigStep`/`run` (a hole must not be
  evaluable: a template reaches the machine only fully filled, so the evaluator's case is a fault or the install check
  refuses a hole-bearing body), `Print`/`Read` (printer/reader), the `lang/package` wire (CODEC review), `relocate`,
  `digestLits`, every Term induction in Lang/Proofs (one case each).
- A `lang!`: every package re-ids (the wire gains a tag). Premises added to landed theorems: NONE known; each touched
  proof gains one case, no statement changes.
- (A) does not foreclose (B): the generators' statements are over `LangHasTy`, and they survive it losing the
  `d.ctx = []` conjunct; (B) is a later `lang!` day, not a redo.

**The argument for (B) that I did not make to ROOT.** Under (A) the strengthening outcome is a theorem OF THE MODEL
only: exercised by `cmttLaws` (the CMTT core), reachable by no deployed package. That is the "honestly labelled caveat"
class Ember has refused before (a caveat that is UNDONE WORK in its clothes, not a theorem of the model). The question
for Ember is whether nano's deployed language should carry what its theory proves — a hole whose filling may use its
context — or whether closed holes (a filling is a closed term, contexts are lambda-abstracted by the author) are the
deployed shape and `u[σ]` stays the theory's.

**Landing 1 launched (real 10-20):** `lang: … (LANG-68)` — LangCalculus + LangInstance + decisions/lang.md LANG-68;
`lane-logs/act2-land1.{log,pid}`, message `lane-logs/commit5.msg`. Reader (a883dc3fb9dca28c8, resumed): LAND-WITH-FIXES,
nothing vacuous, premise question: none; two LOWs applied (projection `langHasTy_closed_holes` deleted; `ΔOf` docstring);
MEDIUM filed cv 01a158da-017c (CLOSURE: no operation requires `Template.Typed`). (B) fork filed cv 01a158da-0192.
SLIP to correct in the next decision text: LANG-68 and the message say LangCalculus is 568 lines; it is 567.
STD-ACTIVITY (fresh, ae06b2334b81f087e) building Std.eqData + Std.activity + the surface form + LA rows in the worktree.
CMTT-CORE a888f90ed44334d88 is at ~405K: at ceiling; a successor starts from lane-logs/cmtt-core.md.
