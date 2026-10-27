VERDICT: RULE E1

The shape is accepted: the live column, not `Package.cites` and not a wider `reqTy`; `cellLive` as "the entry is `.live`", never a version and never a slot predicate; the eight LiveHoles changes are binders (the plan's line list is wrong, the IMPACT's is right); no landed theorem gains a hypothesis; R1 keep, R2 accept, R3 the column, R4 bump. Do not start the build against IMPACT-E1 §6–§9 as written. Three conditions, then it is the spec:

1. **Name the package-check refusal.** A `(live)` read of a relation that is not `cellKeyed` is refused by a wire name (law 7), not by `relReadOf` returning `none`.
2. **Three plants, three reds.** The two edits in §9.3 both redden P8.2 and LH14 and are not yet shown to be different failures. Specify, and run: (a) `cellLive` / `supportLive (.cell _) := true` reds the ROM tooth `cell_support_dead_refused` and, because `relReads` calls `cellLive`, P8.2; (b) `relReads` writes `live := true` and drops the `look` read — P8.2 and LH14 red, **including LH14's unpinned note**; (c) `holeProbePoint` ignores `live` — P8.2 and LH14's dead-cell note red, **LH14's unpinned note stays green**. (b) and (c) must not be the same log line.
3. **Rewrite the byte list (§8.3 is not what `--write` does).** Both refine sites move, `lang/package/4` (56 rows) and `lang/package-version/4` (2 rows). `--write` re-draws a site whose **name** changed (`Emit/Vectors.lean:857–862`); it does not patch a first byte. A second `--write` is byte-identical because `packageVecs` is a pure list. The diff is: ok-package first byte `04`→`05`; the previous-version probe (`packageWireVersion - 1`, vector 50) `03`→`04`; `lang59Package` bytes unchanged, its refusal text `lang/package-version/4`→`/5`; the version site's `04`/`03` become `05`/`04`; vector 42's decoded pins change Repr (`HolePin` → `SupportPin.row`) even where the `.row` tree is byte-identical, plus the one new `.cell` arm. Refusal text on every `lang/package/4` row moves with the label.

---

## 1. The design

The plan's object is a runtime observation, `cell → live`, filled from `cellLive look` for the pinned points of a declared cell-keyed read, set beside the method's rows, never stored. That is the right shape against widening `reqTy`. [READ] `reqTy` is the record of agent, window, occasion, principal, self (`Lang/Package.lean:64–71` in the plan's cite; the definition is the record at the `reqTy` def). It is the argument of `lawTy`, of `methodTy`, and of every guard (`holePosted` binds `req` at `reqTy`, `Lang/StdHole.lean:187`). Widening it would give every law and every guard a read of other objects. [READ] The method environment is already four arguments and no pins: `apply4` binds rows, state, args, req (`Lang/Program.lean:305–308`; the plan's `:299–305` is `reqData` and `apply3`). [READ] `readsData` builds that rows argument from `rv.points self` only (`Lang/Rel.lean:11–13, 131–141`). Cells are the one thing `look` already sees that rows do not: `pinned` returns `w.live` for a pinned id and `.error (.unpinned c)` otherwise (`Kernel/Receive/Call.lean`, `def pinned`). Putting the observation in the rows view uses that view; it does not open a second admission path.

Law 1, as chartered, is "One of everything" (`CHARTER.md`, law 1), not a stored-fact slogan. Applied here: one liveness, `World.live`, projected by `cellLive`. The posted fact stays the poster's claim. [READ] `holePosted` checks `by = req.agent` and nothing else (`Lang/StdHole.lean:183–192`). [READ] `editOf` accepts only `insert`/`upsert` of `(key, val)` at `RelDecl.val`, and `retract` of a key (`Lang/Rel.lean:190–198`). `relEditTy` is that sum (`Lang/Package.lean`, `relEditTy`). A `live` field that exists only on the **read** record (`pointTy` / the proposed `livePointTy`) and is written only inside `relReads` is not a second fact and not a second writer. A separate `cited` relation in the rows record would be a second name for the same cells, plus a package-tree node, plus a rule that has to be enforced by a checker. The plan's "generator rule refuses every edit of `cited`" is a convention until something refuses the edit: the Std.hole generator declining to emit one does not stop a hand-written method. The column makes the refusal a type. A method cannot construct an edit at `editTy` that mentions `live`, and it cannot overwrite the rows argument the runtime passed as `var 3`. That is a real refusal. Do not also build `Package.cites`.

It does not give a pin a second meaning. [READ] A pin is a pair; `pinned` matches on `p.1` (the id) and returns the current entry, version and all, or `none`. The version half is the staleness check, elsewhere. [READ] `World.live` is `some cell` only on `.live cell _`, and `none` on a tombstone or an absence (`Kernel/World.lean:775–778`); the version counter is discarded. `cellLive` is that `some`. The fact's stored `pin` stays the poster's claim, compared by `holeProbePoint` to the candidate's recorded support pin (`Lang/StdHole.lean:39–48`: absent 0, same pin 1, moved 2). After the change, code 1 is same pin **and** `live`, code 3 is same pin and dead. The pin is still a claim. `live` is the entry shape. Two fields.

The opt-in is the residual, and it is why condition 1 is a name rather than a redesign. `(live)` is per read. A method that reads `facts` without it sees today's point and can treat pin-match as current — the probe's bug, still typeable. The plan's always-on `cited` has the same hole one step later: a method can ignore the relation. B1–B3's deployed reader is the generated judge, which must request the column (`facts ⟨3, none, true⟩`). The rows lock that. They do not lock a stranger package. That is shape B, and the probe says shape A is not available (below).

## 2. `cellLive`

[READ] KERNEL-60 (`decisions/kernel.md`, the amount-right section): a counted right is an append-only slot series in the grant cell (`transferBase = 2048`, at most 256 spends); a transfer appends `left - amount` as an effect on that same cell. [READ] The grant is born `.appendOnly` with grantee, target, issuer and rights in the birth slots (`Kernel/Receive/Derive.lean:314–322`). Append-only slots are never overwritten (`Kernel/Cell.lean`, `Discipline.appendOnly`). [READ] Revoke is `(g, .retire)` (`Derive.lean:324–329`), and `live` then returns `none`. A version-exact support would pin `.live cell v`. Any spend of that grant writes a slot, bumps the entry's version (KERNEL-54, the counter `live` throws away), and the pin goes stale while the grant is still the same grant with a smaller remainder. "Never at version v" is the right cut.

It is not too weak for B1–B3. A re-issue to another grantee, or with another right, is another cell: the old one is a tombstone, and the birth slots cannot be rewritten. B1 is that tombstone (`look g = .ok none`). B2 is a digest with no entry, same `none` once pinned, `.unpinned` if not. B3's authority is `spendVia_ok` (kind, grantee, right, remainder) under the same `receive`, not a second copy of those tests inside `cellLive`. The plan does not literally say "slot predicates, optional"; the thing it declines — version, and by the same sentence the grant's slots — is what `walk` / `spendAt` already decide. Putting them in `cellLive` would be a second definition of the same fact (law 1) and would withdraw a support on an unrelated spend (the failure KERNEL-60 is cited to avoid). None of B1, B2, B3 needs them.

## 3. The statement price

[READ] The eight the plan names, at f8d04ac:

| line | theorem | what the statement actually has |
|---|---|---|
| 49 | `selectHole_origin` | binders `rv self`; hypothesis `selectHole rv self h = .ok s`; conclusion includes `c.supports.all (holePinHolds rv self) = true` |
| 70 | `resolveHole_refusal` | binders `rv self` |
| 83 | `instantiateHoles_typed` | binders `rv self` |
| 99 | `instantiateHoles_sources` | binders `rv self` |
| 119 | `runHoleGuard_cost` | binders `rv self`; conclusion `used ≤ holeGuardFuel` |
| 261 | `loadLive_libTy` | **already** binds `look : Pinned D` |
| 275 | `loadLive_checked` | **already** binds `look` |
| 362 | `instantiateHoles_cost` | binders `rv self`; conclusion `i.cost ≤ p.preparationCost` |

[READ] `loadLive` already takes `look` and does not pass it to `instantiateHoles` (`Lang/Program.lean:207–210`). So :261 and :275 gain nothing. The plan missed two that must gain the binder, because they call `selectHole` / `resolveHole`: `selectHole_nodes` at :301 (conclusion `Term.nodes s.body = Term.nodes s.original`) and `resolutionMax_committed` at :340. The IMPACT's eight is the right eight. Each change is a binder (`digestOf`, `look`) on an existing hypothesis (`= .ok`). A binder is not a hypothesis.

`selectHole_origin`'s conclusion changes meaning, and on the row fragment it is the same strength. [READ] `holePinHolds` is `holeRow` yielding `.ok (some (.row _ _ ver))` with `ver == p.ver`, else false (`Lang/LiveHoles.lean`, `holePinHolds`). The IMPACT defines `supportLive` on `.row` as that body. For a candidate whose supports are all `.row`, `supports.all supportLive = true` is the old conclusion. The new conjunct (every `.cell` is a pinned live cell) is vacuous there. The consumer `resolutionMax_committed` binds the support conjunct to `_` (`Lang/Proofs/LiveHoles.lean:354–357`) and uses `c.body`. No weakening.

No landed theorem in the IMPACT's list gains a hypothesis. Watch two that change text without gaining one. `holeDecision_label` (`Lang/Proofs/Contextual/HoleBridge.lean:45–48`) is membership of the label in a list of seven; the list grows by `support0Dead` / `support1Dead`. That is a weaker sentence, and it is forced: the old sentence becomes false once the function can return the new labels. It is not a new assumption. The `readsData` / `relReads` family gain `look` in the same binder position. `relReads_conforms` keeps its text; `relReadTy` grows a `.bool` on the live arm, which is a stronger conforms, not a hypothesis.

The new theorems, four questions each. None is a disjunct `∃ a b, a ≠ b ∧ h a = h b`. The census shape does not hit them.

- **`cellLive_iff`.** Object: `Lang.cellLive`. Nothing landed is weaker without it; it is the unfolding the other four and C2's `kernelWorld` cite, and the mutation below makes the unfolding worth a name. Not a disjunct: `cellLive look g = true ↔ ∃ c, look g = .ok (some c)`. Mutation: `cellLive look g := (look g).isOk`, false at `look g = .ok none` (a pinned tombstone, which the probe produced). Keep.
- **`cited_authenticated`.** Object: `Lang.relReads`, not a `cited` relation (R3). Without it, `posted_support_checked` has a `live` bit with no theorem tying it to `World.live`; the journey row would be the only tooth. Not a disjunct: an implication from `relReads = .ok v` and `x.live = true` to each point's `live = cellLive look g` for that point's key. Mutation: `relReads` writes `live := true` and drops the `look` read; false at a tombstone. This is plant (b). Keep. It says nothing when `x.live = false`; that is the opt-in, not a vacuous hypothesis.
- **`selectHole_cell_support`.** Object: `Lang.selectHole`. `selectHole_origin`'s new conclusion does **not** replace it: that conclusion says `supportLive` holds, so `supportLive (.cell _) := true` leaves `selectHole_origin` true while a dead cell is selected. This theorem talks about `look`, so the same mutation makes it false. Not a disjunct: the `∃ c` is the selected candidate, and the `∀ id` forces `look g = .ok (some cell)`. Mutation: `supportLive (.cell _) := true`. Plant (a). Keep.
- **`revoked_support_refused`.** Do not state it over `Receive.submit` (R2). ROM arm: object `selectHole` / `resolveHole`; without it, `blocked_step` still says a blocked term faults and does not say a dead cell produces one. Mutation: the same as `selectHole_cell_support`. Std.hole arm: object the generated judge; without it the model can return 1 for a dead match. Mutation: `holeProbePoint` ignores `live` and returns 1. Plant (c). Not a disjunct. Keep, under the names the IMPACT gives, not under "over submit".
- **`posted_support_checked`.** Object: the generated probe composed with `cited_authenticated`. Without it, `holeProbePoint_meaning` can say "1 means the point's `live` field" and a forged field still satisfies it; this is the theorem that 1 means a live **kernel** cell. Mutation: drop the `live` conjunct in `holeProbePoint`; the ghost fact of probe (a) reads 1. Not a disjunct. Keep.

`hole_probe_dead` and `cell_support_dead_refused` are the concrete teeth of those mutations. They are not docstrings: each is false under one of the plants above.

## 4. The wire

[READ] `packageWireVersion : UInt8 := 4` (`Lang/Bounds.lean`). [READ] `packageVersion` refines `u8` to that constant and refuses anything else as `lang/package-version/4` (`Lang/Package.lean:615–617`). `decodePackage` runs `packageStream`, which is that byte **then** the tree (`:648–654`). A version-4 package fails the refine and never reaches `packageOf`. It is not reinterpreted. The journey already shows the refusal (`E1-support-probe.txt` LV1–LV3).

[READ] The bump is required, not polite. `holePinOf` accepts only `.node 0 key [rel, ver]` (`Lang/HoleWire.lean:8–16`). A `.cell` tag of `.node 1 id []` is today `none` — a refused boundary — and becomes a read. That is the case the codec comment names (`Lang/Package.lean:628–631`: a new tag that turns a refused boundary into a read moves the version and the label `lang/package/N`, or `packageCodec_label` fails the build). The parenthetical in R4 ("v4 bytes would decode to the same meaning") is true only of a **well-formed** v4 package, and only if the version byte is ignored: `.row` is defined to be the old `holePinTree` byte for byte. It is false of the boundary the rule exists for. Bump.

`RelRead` is not a package-tree field (`packageTree` is imports, state, iface, body, methods, laws, rels, doc, holes). A live column appears on the wire only inside the terms of a method that requests it. Std.hole's generated body is such a term, so the hole packages change past byte 0; the journey size rows move, as §6 says. Packages that never mention the column change only in the version byte and, where they carry a row pin, not in the pin tree.

The ordinary emitter is `lake exe codec-vectors --write`, and condition 3 is the list it will actually produce. `--check` then `cmp` of a second `--write` is the right gate (`Emit/Vectors.lean:24–29, 857–862`).

## 5. The row diff

P8.2's new sentence is the refusal, and LH14 is new. That part of §6 matches the plan and the probe. "Every other row's text unchanged" is false, and §6 already admits it: helper and package byte counts, LH7/LH8 step and tick counts, LV2/LV3's `version 4` → `5` and `lang/package-version/4` → `/5`. Those are the mechanical rows. The landing's diff is §6, not the plan's sentence. Nothing else may move.

The two plants in §9.3 are real mutations and, as specified, **not** different failures. Both are defined to redden P8.2 and LH14. (b) forges the observation; (c) ignores a correct observation. They come apart only on LH14's unpinned note, and only if (b) drops the `look` read rather than overwriting `live` after a successful one. Neither is the plan's B1 plant (`cellLive g ↦ true`), so neither reds the ROM grain on its own. Condition 2.

## 6. The residual the probe used

[MEASURED] `E1-support-probe.txt`. A fact naming a cell with no entry, at an arbitrary pin, is admitted by `post`; the candidate is `verified`; `select` admits; `commit` admits and spends the unit (left 0). After revoke, the entry is a tombstone, the fact row is still there, and a commit pinning that tombstone admits and spends the unit. Revoke then unpost, as two calls, makes the next commit `support0 withdrawn`. [READ] One call cannot do both: `Unsigned` carries one `body` (`Kernel/Receive/Call.lean:95–111`), and `bodyOf` / `callsOf` emit `account`/`credit`/`grant`/`invoke`/`transfer` as the object (`Lang/Call.lean:151–172`), not a `revoke`. Revoke requires the issuer (`Derive.lean:328`), who is the member. Shape A does not close the gap. The plan's §8.3 refuter failed to refute; C1 stands. (The IMPACT's cite `Lang/Call.lean:157–170` is `bodyOf`'s grant/invoke/transfer arms; `callsOf` itself starts at 172. The claim is right.)

What let the pins stand in: the caller pinned the tombstone, `pinned` returned `.ok none` only if someone had asked, and nobody asked. The kernel accepted the pin because a tombstone at its current version is not stale (`live` is `none`, the pin still matches the entry). The method compared the fact's stored pin to the candidate's pin, got "same", and treated that as live.

The design closes that on the deployed path, and only there. `relReads` must fill `live` from `cellLive look` of **that point's key**, and code 1 must require it. A pin of the tombstone then yields `.ok none`, `live = false`, code 3, `support0 dead`. A pin of the fact row does not satisfy `look` of the cell; an unpinned cell is the kernel's `.unpinned`, thrown as is. A pin of some other live cell does not move this point's bit, which is what `cited_authenticated` has to say. `holePosted` staying blind is correct: the cell can die after the post, so the check belongs on the read.

What would reopen it, and is forbidden by the conditions: computing `live` as "the id occurs in the pin list" (`(look g).isOk`); treating code 1 as same-pin alone; requesting `facts` with `live = false`. Nothing in the design lets the caller's pin version equal the fact's pin and have that equality count as liveness. Do not add that comparison. It is the version-exact support §2 refuses.

## 7. R1–R4

- **R1, keep.** [READ] An unpinned row support never reaches `holeRow`'s `.unpinned`. `holePinHolds` maps every failure to false, and `selectHole` throws `.derivationMoved` (`Lang/LiveHoles.lean`, `selectHole`'s `unless c.supports.all`). LH7's row text is `support0 moved`. Renaming that to `unpinned` is a row-diff outside §6, and it is not this card. A cell support is new, so it takes the kernel's name `.unpinned` when `look` errors, and `supportDead` when `look` returns `.ok none`. The asymmetry is the deployed row behaviour.
- **R2, accept.** The through-`submit` tooth is the journey row, which the probe already executed on the real `Receive.submit`. No landed theorem connects `submit` to a Std.hole body's value; `runSetup_spec` and `method_live_run_sound` give typing. A submit-level value theorem is a second card. The theorem that lands is the ROM arm plus the generated-judge arm. It must not be named as a theorem over `receive`.
- **R3, the column.** §1. The separate `cited` relation buys a wire node and a convention. The column is the observation, in the read the method already has, uneditable because it is not in `editTy`.
- **R4, bump.** §4. The codec rule at `Lang/Package.lean:628–631` is the reason. The parenthetical is not.

---

## Spot-checks

Base: `git -C /Users/ember/dev/nanodregg rev-parse origin/main` → `f8d04ac825460d49d8cb9524d37a20f482e1199d`. Local HEAD is `7e02852`, an ancestor; every quote is `git show origin/main:<path>`. No build. No tree edit.

**`holePosted` is the poster's claim.** `git show origin/main:Lang/StdHole.lean | nl -ba | sed -n '183,192p'`

```
183  def holePosted : Term :=
184    let yours (x : H) := hp .deq (hg x "by") (hg (hv "req") "agent")
...
189        ("insert", "x", hguard (yours (hg (hv "x") "val")) "notYours" (hc okT)),
```

No `cell`, no `pin`, no `look`. The comment above it (`:194–196` in the same file, just below) says fact liveness is rechecked by the methods. Today that sentence is false; the card is what makes it true.

**`loadLive` already holds `look`, and does not give it to the holes.** `... | nl -ba | sed -n '207,210p'`

```
207  def loadLive (rv : RowView D) (self : D) (look : Pinned D) (fuel : Nat)
209    loadUsing digestOf (admitContextual digestOf (fun Δ p =>
210      (instantiateHoles rv self Δ p).map (·.body))) look fuel idb acc
```

**`apply4` is rows, state, args, req.** The plan's `:299–305` is `reqData` / `apply3`. The function is `:305–308`:

```
305  /-- Apply method `ℓ` ... bound as `var 3, var 2, var 1, var 0` (LANG-49: rows first). -/
307  def apply4 (g : Nat) (ℓ : Label) : Term :=
308    .app (.app (.app (.app (.get (.ref g) ℓ) (.var 3)) (.var 2)) (.var 1)) (.var 0)
```

**`receive_congr` quantifies over the caller's pins, and over `World.live` of those ids.** `Kernel/Proofs/Receive.lean:38–41` (the plan's `:36–41` is the docstring through this line):

```
38  theorem receive_congr ... (ho : w₁.origin = w₂.origin)
39      (agree : ∀ p ∈ c.unsigned.pins, w₁.live X.env p.1 = w₂.live X.env p.1)
40      (rows : rowView X.env w₁ c.unsigned = rowView X.env w₂ c.unsigned) :
41      receive X w₁ c = receive X w₂ c
```

A `cellLive` read through `pinned` is a projection of a quantity this theorem already equates. Kernel price zero.

**The eight statements.** `Lang/Proofs/LiveHoles.lean`, numbered as in §3. `loadLive_libTy` at 261 and `loadLive_checked` at 275 both quantify `{look : Pinned D}` in the hypothesis' binders today. `selectHole_nodes` at 301 and `resolutionMax_committed` at 340 do not. `selectHole_origin` at 49–55 ends `c.supports.all (holePinHolds rv self) = true`. `resolutionMax_committed` at 355 discards that conjunct: `obtain ⟨c, _, _, _, _, hc, horig, _⟩ := selectHole_origin he`.

**`live` drops the version; a tombstone is `none`.** `Kernel/World.lean:775–778`

```
775  def live (E : Env D) (w : World D) (c : D) : Option Cell :=
776    match w.entry E c with
777    | some (.live cell _) => some cell
778    | _ => none
```

**The grant cannot be re-issued in place.** `Kernel/Receive/Derive.lean:322` births `kindGrant` at `.appendOnly`; `:324–329` `revoke` is `[(g, .retire)]` after checking the issuer. KERNEL-60 (the `decisions/kernel.md` section of that name) appends the remainder to that cell's ledger on every spend.

**The version refuse, and why the tag forces the bump.** `Lang/Package.lean:615–617` and `:628–631`; `Lang/HoleWire.lean:12–16` (`holePinOf` is node 0 or `none`). `Lang/Bounds.lean`, `packageWireVersion := 4`.

**The column is not stored today, and the edit path cannot grow it by accident.** `Lang/Rel.lean:141` builds `record [("key", key), ("val", optD val)]`. `editOf` at 191–197 matches `insert`/`upsert` of exactly those two fields.

**`--write` re-draws by site name.** `Emit/Vectors.lean:857–862`: keep rows whose `site` and `tag` both match; otherwise `fresh`. The site name is the refine label, so `lang/package/4` → `lang/package/5` is a new site, not a patched byte. `packageVecs` (`:718–729`) is a fixed list, including `rawPackage (version := packageWireVersion - 1)` and the hardcoded `lang59Package`. The tsv at f8d04ac has 56 `lang/package/4` rows (0–55) and 2 `lang/package-version/4` rows; row 42 is the ROM whose pins print as `{ rel, key, ver }`; row 50 begins `03` and is refused `lang/package-version/4`.
