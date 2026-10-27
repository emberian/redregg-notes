# READ-LANG — the LANG definitions layer of nanodregg, read whole (2026-10-24)

Reader: one whole-file reader (BRIEF.md), layer LANG DEFINITIONS: `~/dev/nanodregg/Lang/` minus
`Lang/Proofs/`, at origin/main `f9657bd` (the checkout is at that commit; `git status` clean but for an
untracked README copy). Nothing was edited. Measurements were run once, read-only, against the built
`f9657bd` worktree `/tank/dregg-build/nanodregg/wt/backlog` on hbox (`SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2
swarm-build lake env lean /tmp/reader-lang-probe/ReaderProbe.lean`; the probe file is in this session's
scratchpad, `.../scratchpad/probe/ReaderProbe.lean`, and at `hbox:/tmp/reader-lang-probe/`). Tags:
READ (path:line), MEASURED (the probe), INFERRED.

## Verdict

I read in full: Program, Package, Call, Rel, Eval, Term, Law, Bounds, Data, Wire/Data, Row, Std, StdData,
StdActivity, StdOffer, StdOfferEscrow, StdHead, StdHole, StdHoleModel, StdContextualHole, LiveHoles,
HoleROM, HoleWire, HoleDecl, HoleSyntax, Bell, Contextual/LangInstance, Contextual/NanoBridge, all 2949
lines of Journey.lean, and Journey/{Offer, OfferEscrow, Head, Contextual, Hole, HoleChecks}. I read Wire.lean's
term codec half, the headers and definition lists of Check, Ty, Sim/Need and Contextual/Protocol, and the
assertion lines of Journey/{ContextualReceive, ContextualWire}. In decisions/lang.md I read LANG-75.14,
75.19, 76 and 77 (both landings) whole, and grepped the rest for the claims I checked. The runtime (Program,
Package, Call, Rel, Eval) is careful. Its one decision for each fact is real where the brief asked: the live
and receipt columns are computed by ONE `Lang.keyColumns` for points and range rows, and the invoke encoder
is applied at ONE site. The generators' de Bruijn bookkeeping checks out at every binder I counted. There is
no `partial`, `unsafe`, `native_decide` or `sorry` in the layer's definitions.

The three worst things:

1. **A plain package cannot import an installed contextual package, and the refusal blames the importer.**
   Install chooses its loader from the ROOT's holes. The run chooses one per package. So install refuses
   what the deployed run would load. The refusal comes out as `illTyped noHole @execute…`, a typing error
   inside the import's body. The importer itself is well typed. (MEASURED)
2. **The hole's complete-observation check renders a missing pin as the verdict it guards.** An omitted
   support pin and a withdrawn fact both refuse `support0 withdrawn`. An omitted blocker pin and a live
   prune both refuse `pruned`. A plant that deletes the support half of the check changes no `select`
   output, and no journey row runs the one method where it does show (`rejudge`). (MEASURED)
3. **`Std.offer`'s session rows can never leave.** The log has a constant-false resumer, no patience and
   no `retire`. So every object of `Std.offer` and `Std.offerEscrow` stops taking deals after
   `sessionLimit` (1024) fuses or takes. That is the defect class LANG-76 fixed for activities, and LANG-76
   says these packages were left byte-identical. (READ)

Behind those are a set of conformance rows that pass on a prefix or a disjunction (LE5 accepts any refusal),
one LANG-77 claim that depends on its parameters (MEASURED: the PT3 mutation generates cleanly at `theta =
[a, b]`), stale headers that describe a deleted matcher and an unbuilt KERNEL-25, and the law-1 twins
`Program` keeps "for their landed statements".

## Answers to the brief's specific questions

- **Live and receipt columns, points and ranges (4916f3a, 7fec6d7): one definition?** Yes for the
  VALUES. `Lang/Rel.lean:212-229` `keyColumns` is the only producer. It is called by `pointData` (:232)
  and by `columnRow`/`columnRows` (:240-251). `git grep` finds no other producer of a `live` or `receipt`
  column outside `Lang/Proofs` (READ). The column TYPE is written twice: `rangeRowTy` (`Package.lean:195-197`)
  and `pointRecTy` (:218-220) each spell `(if live …) ++ (if receipt …)` (see D-12). One quirk is that on a
  read that is both `live` and `receipt`, the `live` field is always `true` (F-9).
- **Typed invoke arm (LANG-77, e2eecce).** The encoder is applied exactly once: `Call.lean:168-174`
  `argsBytes`, called only from `bodyOf`'s invoke arm (:189-191) (READ). Is a wrong value a generation-time
  error? Only when it is ill-TYPED, and that depends on the generator's parameters. MEASURED: LANG-77's PT3
  (fuse sends `keys` as `theta`) is refused at `theta = [price]` but generates and checks at `theta = [a, b]`,
  where `offerThetaTy = offerKeysTy` (F-7). Can a package still carry raw bytes to a typed callee? Not
  verbatim: a `bytes`-typed slot sends `encodeData .bytes b` (length-prefixed). But the callee decodes
  STRUCTURALLY at its own type, so a `bytes` slot can still build values for unrelated callee types whose
  encoding happens to match. LANG-77's critique says this (INFERRED from `Wire/Data.lean:53-64`).
- **The fuse as one party's method (e7c2b13).** `Y.take` re-checks its own offer slot pinned and present,
  the peer's (X's) offer slot pinned and present, and that its own pinned offer is the one `keys` names for
  it (`offerNamedOkT`, `StdOffer.lean:157-159`). It also re-runs the joint judge on both pinned values and the
  θ it decoded. It trusts three things it does not check. (a) That X's pinned offer is the one `keys` names
  for X: only X's run checks that, and the nested take reads the same pin. (b) That its caller is X: `Req`
  has no caller-object field, `reqOf` at `Kernel/Receive/Call.lean:440`. (c) That X's own offer was
  retracted in the same tree. In the fuse all three hold by the tree. A root `take` (the owner, or any
  grantee of `[invoke take]`) gets none of them; see F-8.
- **The deadline arm (LANG-76).** Can a caller lie about `notBefore`? Only downward, and that only hurts
  the liar. `World.admit` enforces `notBefore ≤ height+1 ≤ validUntil ≤ notBefore + windowMax`
  (`Kernel/World.lean:905,947`, `windowMax = 1024`). So a retirer cannot sign a `notBefore` past the height
  its Turn lands at, and `activityDue` (`StdActivity.lean:79-80`) is sound for the retirer. A starter's key
  `notBefore` can be backdated by up to 1024 heights, as LANG-76 states. The bound is a property of the
  generated `start` method, not of the guard (F-11).

## Findings, ranked

### DEFECT

**F-1 · A plain package importing a contextual package is refused at install, under a name that blames the
importer.** `Lang/Program.lean:247-251`: `checkInstallContextual` sends any root with `p.holes = []` to
`checkInstall`. That loads imports with `loadAll` → `admitPackage` → `Package.checkWith` (`Package.lean:631-638`),
which runs `checkE … (Ω := [])` on the IMPORT's body. A deployed run of the same importer loads every package
through `loadLive` → `admitContextual` (`Program.lean:193-227`), which accepts the holed import. WHY wrong:
the header (`Program.lean:8-10`) and LANG-35 say install "loads its imports' closure exactly as a run does".
For contextual imports it does not (law 1: two loaders decide one closure). Law 7: the refusal names a rule
inside a package that already installed and checks. MEASURED (probe1): importer `{imports := [the linked
Journey.Contextual hole package]}` → install refused `illTyped noHole @execute.body.body.body.body.cond.arg`.
`loadLive` of the same holed package → `ok`. A side effect: `CheckError.contextualSignature` (:636) is
reachable only for a body that declares holes and uses none, because `checkE` with `Ω = []` refuses every
hole node first. A layer (`Surface` `layer`) over any contextual package is therefore uninstallable.

**F-2 · Complete observation renders a MISSING pin as the VERDICT it guards (law 7).**
`Lang/StdHole.lean:85-91` `holeCoverageCheck` refuses an unobserved `s0` / `s1` / blocker with
`"support0 withdrawn"` / `"support1 withdrawn"` / `"pruned"`, which are the judgment's own verdict names
(:176-181). The same names are in `StdHoleModel.lean:81-86` `holeCoverageOutcome`. WHY wrong: law 7 ("a
parse failure is never rendered as a verdict"), and the minted class "refusal renders as the expected
verdict". Clients derive pins from refusals (`Rel.lean:345-347`'s docstring says so of `rowUnpinned`). Told
"support0 withdrawn", a client concludes the fact is gone, not that it forgot a pin. MEASURED (probe3, the
generated `holePackage .nat holeCapClause`):
`select` with the support's fact pin omitted → `refused support0 withdrawn`; pinned absent → `refused support0
withdrawn` (identical). PLANT "support coverage always true" → `select` omitted still `refused support0
withdrawn` (the plant is invisible to `select`/`fill`/`accept`). Only `rejudge` tells the two apart: honest
omitted → `refused support0 withdrawn` (at extraction); planted omitted → `ok, status = suspended "support0
withdrawn"`, a false record of a live fact. The journey's omitted-pin rows (`Journey.lean:2226-2237`) cover
only the BLOCKER. No row runs `rejudge` with an omitted SUPPORT pin (INFERRED from the rows; the
`Lang/Proofs/StdHole*` theorems were not read).

**F-3 · `Std.offer` (and `Std.offerEscrow`) session rows are permanent; an object takes at most `sessionLimit`
deals, ever.** `StdOffer.lean:117-118` makes the session log `activityLog … "session_waiting"`, guarded by
`activityWaiting S [plan] sd offerResumer` (:275) with no patience. `offerResumer` is `λ_ _. false` (:140).
So: an upsert (answer) is refused `notResumer`; a retract of an unanswered row is refused `unanswered`
(`StdActivity.lean:86-87`, patience `none`); the package has no `retire` (it is emitted without
`activityPackage`, :260-283). Every take/fuse inserts one row at each party (:199-206), and the kernel
refuses `relationFull` past `limit` (default 1024, :301). WHY wrong: LANG-76 names exactly this ("an
unanswered row waits forever and holds one of the log's slots") as a defect and fixes it for activities.
It then says "Without a patience … `Std.hole`, `Std.offer` and the escrow emit byte-identical packages"
(decisions/lang.md:6683), which leaves the defect in the two offer packages. Mutation/input: 1025 fuses on
one object; the 1025th is `rejected relationFull` and no method can free a slot (READ). A smaller edge: the
session key is `(req.agent, req.notBefore)` (:204), so two deals at one object by one signer at one
`notBefore` collide (`keyTaken`). Every journey row signs `notBefore := 0` (`Journey.lean:737`), and no row
makes a second deal.

### DEBT

**F-4 · Conformance rows that pass on any refusal, or on a disjunction whose Lang arm is never reached.**
Each row below stays green under the mutation it is meant to catch, or matches more than the name the code
emits (READ):
- `Journey/OfferEscrow.lean:138-141` LE5 ("a post whose grant is smaller than its leg"):
  `vp5.startsWith "refused"`. Any refusal passes (an `unpinned` from a forgotten pin, a decode refusal); the
  balance checks hold for every refusal.
- `Journey.lean:2704` L6 (ill-typed install): `startsWith "refused program"`. Any program refusal, a decode
  one included, passes; `illTyped` is never named.
- `Journey.lean:2217` LH8b and `:2283` LH11b: `startsWith "refused grantRight" || refusedBy … "notChooser"`.
  B holds no grant for `select` or `prune` (LH3, :2121), so the kernel always refuses `grantRight` first and
  the `notChooser` arm is never exercised on the receive path. LH11b's comment, "the guard refuses it"
  (:2281), is false. `notChooser` has a tooth only at evaluation level (`Journey/HoleChecks.lean:99,124`).
- `Journey.lean:2466-2468` P8.2: `refusedBy … "support0 dead" || startsWith "rejected stale"`, and
  `:2519` P8 deadline: `rejected outsideWindow || refused outsideWindow`.
- `Journey/Contextual.lean:148-155` the six `management-*` boundary rows assert `!= "ok"`. Any refusal,
  including a fault, passes.
- `Journey.lean:1922` LC8, the LANG-77 tooth for a caller/callee shape mismatch, checks only the substring
  `"arguments:"`. `arguments: not a digest` would pass.
- `Journey/Head.lean:135-136` HD5 reaches only the `other = held roots` arm of `headAtFork`
  (`StdHead.lean:51-57`). The `steps ≠ held steps` arm (also `badFork`) has no row, and HD5c always forks at
  the held steps (21). One name for three conditions means the row cannot say which one it caught.

**F-5 · The twins `Program` keeps "for their landed statements" (law 1).** `Program.lean:155-161` `load`/`loadAll`,
:216-227 `loadContextual`/`loadAllContextual`/`loadLive`, :348-361 `judgeOne`/`judge` beside `judgeContextual`,
:454-457 `runSetup` beside `runSetupLive`, :512-524 `runMeasured`/`runMethod` beside `runMeasuredLive`,
:235 `checkInstall` beside `checkInstallContextual`. `program` (:563-570) uses only the contextual/live ones.
They are bridged one way, closed ⇒ live (`Lang/Proofs/LiveClosed.lean:122-200`, `runMeasuredLive_closed`,
`program_run_closed`), so a theorem stated on `runMethod` or `runSetup` speaks of the deployed run only
under a closed-closure premise. The comment at :454 says why they stay. The charter says to delete the old
shape (READ).

**F-6 · `Need.requiredOf` (the BAR's denominator) is the closed twin, and its header says it is the deployed
one.** `Lang/Sim/Need.lean:16-18`: "`requiredOf` … starts from … the deployed `Lang.runSetup`". The deployed
setup is `runSetupLive` (`Program.lean:463-467`). `requiredOfLive` (`Need.lean:268-278`) exists beside it,
counting `S.preparation` that `requiredOf` (:255-266) omits: two definitions of "the steps an invoke
requires". The journey's `measure` uses the Live pair (`Journey.lean:724-725`). THE BAR's
`Protocol/Rows/Loopback.lean:284-285` uses `runMeasured`/`requiredOf`, and on any `.error` returns `none`
(:296-298). For a contextual package `runSetup` refuses (F-1's `checkWith`), so the measurement is silently
absent (INFERRED; the Protocol half is PROTOCOL's).

**F-7 · LANG-77's "a wrong value is a type error at generation" holds only for some parameters.** LANG-77 L2
plant PT3 (decisions/lang.md:6886-6890) says the typed arm "catches the wrong value at generation, before
any run". MEASURED (probe4): the PT3 mutation (`("theta", .get arg "keys")` in the fuse's call) is refused
`illTyped payload @fuse…calls.c0.some` at `theta = [price]`, and CHECKS at `theta = [a, b]`, because
`offerThetaTy [a, b] = offerKeysTy` (`StdOffer.lean:41,145`). Well-typed wrong values (a swapped pair, the
peer's keys) are never generation errors at all. The claim is a property of one fixture's parameters, stated
as one of the language.

**F-8 · `Std.offerEscrow`'s header promises atomicity a `take` alone does not have, and names a deleted
matcher.** `StdOfferEscrow.lean:16`: "Both takes run in the matcher's one tree, so both legs move or
neither". The matcher was deleted (LANG-77 L2). `:20-21`: "`offer_guard` admits a retract only from `take`
or `withdraw`". It also admits `fuse` (`StdOffer.lean:130-132`). A root `Y.take` (Y's owner, or any grantee
of `[invoke take]` on Y) pays Y's leg to X's `payTo` and leaves X's offer and leg in place (`:93-95`).
`take` cannot tell, because `Req` has no caller-object field (F-answers). The escrow's safety therefore
rests on the invitation grant naming the peer OBJECT (as LF/LE do, `Journey/OfferEscrow.lean:87`). A grant
of `[invoke take]` to a MEMBER would give that member a one-sided take of Y's leg, and nothing in the
package refuses that grant (INFERRED; see Q-1).

**F-9 · On a read that is both `live` and `receipt`, the `live` column is constant `true`.** `Rel.lean:214-218`:
the receipt arm calls `receiptSeen` first, which refuses `headDead` on `look g = .ok none` (:197). It then
reports `live := cellLive look g`, which is `true` for every `.ok (some _)`. The column can never be
`false`: it carries no information. 7fec6d7's message says it "dropped `live` on a live+receipt read" and
fixed that. It now carries a field that cannot vary (READ).

**F-10 · Unreachable named refusals in live preparation, and one name for two constructors.**
`LiveHoles.lean:281-282` `.provenance`: the instantiated body's digest literals come only from `p.body` and
the selected candidates' `original` bodies (renaming adds none), so the check cannot fail. Its only
occurrence outside its definition is a plant argument (`Journey/ContextualChecks.lean:68`). `:285-286`
`.instanceRecheck` and `admitContextual`'s `checkE` (`Program.lean:206-207`) re-check what substitution
preserves. The "recheck-arm-reachable" plant (`ContextualChecks.lean:46,97`) reaches it with a hole name
`10^300`, which `holeROMWire` (`HoleWire.lean:74`, `name < 2^32`) refuses. No package that decodes can be
that input. Its name is `"holeInstanceType"`, the same prefix as `.instanceType e` (`LiveHoles.lean:62-63`).
The row `admission-prepared-type` (`ContextualChecks.lean:107-109`) matches `startsWith "holeInstanceType"`
and cannot tell them apart. Law 4: an assertion inside total Lean re-checks the compiler. Law 7: one name
for two refusals.

**F-11 · The activity log guard does not pin the key's `notBefore`; LANG-76's deadline bound is the start
method's, not the guard's.** `StdActivity.lean:100`: the `insert` arm checks only `key.agent = req.agent`.
`activityStartMethod` writes `key = (req.agent, req.notBefore)` (:165,169-171), and the Bell's `ring` uses it.
But a guard is the law of every object of that kind. Any method that inserts a log row (a hand-written
method, a layer's) may pick any `notBefore`. With 0 the row is due at once. With one near `natLimit`,
`activityDue`'s add faults (:79-80, "a fault is a refusal"), so it is never due and holds a log slot forever.
Both stay inside the inserter's own objects, so this is debt in the statement, not an attack. Also,
`Std.activity` refuses only `patience = some 0` (:292) "anyone could abandon at once". Any `patience ≤
windowMax = 1024` allows the same thing through a backdated start (READ).

**F-12 · Two spellings of one column layout; the peer reads resolved apart from the method's signature.**
`Package.lean:195-197` `rangeRowTy` and :218-220 `pointRecTy` each build `[key] ++ live? ++ receipt? ++ [val]`.
`keyColumns` must produce that order, and nothing forces the two type spellings to agree with each other.
`Program.lean:363-364` says `resolveMethod` is "the one resolution". `Package.peerReads` (:372-375)
re-derives the peer reads from the interface through `methodPeer` → `rowsOf`, because `methodSig`
(`Package.lean:506-514`) computes `(rs, ps)` and drops `ps` from `Sig` (READ).

**F-13 · Live admission type-checks every contextual package twice per load.** `Program.lean:200` calls
`p.checkContextual ifs`, then `prepare` = `instantiateHoles`, which calls `p.checkContextual Δ` again
(`LiveHoles.lean:275`). It then runs `checkE` on the instantiated body (:285), and `admitContextual` runs the
same `checkE` again (`Program.lean:206`). It also runs `checkLits` on a body whose literals `checkROMLits`
just covered (:209). Per run, for every package in the closure. Law 5 waste, law 1 twins. None of it is in
the preparation charge (`Package.preparationCost`, :231-232, counts expansion and guard fuel only) (READ).

**F-14 · Comments that say more than the code.**
- `Eval.lean:21-22`: "`Lang.Proofs.Sound` proves … that only a primitive faults". `step_sound`
  (`Lang/Proofs/Sound.lean:145-148`) says "faults by a name other than `stuck`". `refuse` and `hole` fault
  with `refused` (`Eval.lean:188-189`), so no primitive is involved.
- `Std.lean:129-136`: "Once KERNEL-25 lands (ruled 10-17, NOT YET BUILT … an invoke does not)". KERNEL-25 is
  built: LB12n/o/q (`Journey.lean:1489-1496`), LF6a (`Journey/Offer.lean:164`).
- `Wire.lean:20-26`: the term tag table stops at `refuse 17` and omits `hole 18 n [σ*]` (:175).
- `StdOfferEscrow.lean:16,20-21`: F-8.
- `Journey.lean:2281`: F-4.

**F-15 · The contextual calculus is a theory island beside the substrate.** `Lang/Contextual/Protocol.lean`
(628 lines, with the toy instances `Coin` and `Negotiation`, a model of the P8 negotiation beside the real
P8 rows) and `LangInstance.lean` have no deployed importer. `git grep "import Lang.Contextual"` finds only
`NanoBridge` and three `Lang/Proofs/Contextual` files. decisions/lang.md:6444 and :6491 say "the Contextual
calculus has no deployed consumer". `LangInstance.lean:46` sets `check Ψ M A := infer [] Ψ M = some A`
(`Δ = []`), while the deployed candidate check is `HoleROM.check Δ` at the imports' interfaces
(`LiveHoles.lean:67-77`). So "the DEPLOYED term language as a contextual calculus" (:2) is the
import-free fragment. `NanoBridge.lean:16` makes a Lang definition module import `Hosting.Resident.Trace`.
That inverts the charter's layer order (LANG above HOSTING) (READ; memory "iterate inside the substrate").

**F-16 · Two refusal channels for one generator family; two `HoleRefusal` types.** `StdHole.lean:352`
`Lang.Std.HoleRefusal` (generator) and `LiveHoles.lean:14` `Lang.HoleRefusal` (runtime) share a short name
across namespaces. `HoleBundle.link` (`StdHole.lean:372`) refuses by constructor, `linkContextual`
(`StdContextualHole.lean:77`) and `contextualHole` (:35-37) by `String` (`throw e.name`,
`mapError HoleRefusal.wire`). The generators' `.package why` arms render `why.text`, the human text, not
`CheckError.name` (`StdOffer.lean:298`, `StdActivity.lean:33`, `StdHole.lean:360`). Law 7 (READ).

### QUESTION

**Q-1 · Should `take` be reachable at all except as the peer's half of a fuse?** F-8. What would decide it: a
statement of the invitation discipline. Either the grantee of `[invoke take]` must be an object of this
package, and something refuses other grants, or a root `take` that moves value is a documented gift.
LANG-77's critique (decisions/lang.md:6898-6901) keeps "one session row is not a fuse". For the escrow, one
session row is a one-sided transfer of value.

**Q-2 · A `(receipt)` read over several rows checks ONE receipt against EVERY head.** `Rel.lean:199` reads the
method's single `receipt` argument for each point and each listed range row, so any listed head that does
not validate it refuses the whole run. The deployed acceptor reads `(range 1 1)`, which hides this.
LANG-75.14 does not say whether a multi-row receipt read is meant to be a conjunction over heads. What
would decide it: a second fixture with `(range 1 2)` and two heads.

**Q-3 · Is `headDead` the right name for a key whose cell never existed?** `Rel.lean:197`: `look g = .ok none`
covers a tombstone and an absent id alike. LANG-75.19 notes no object can be retired in nano, so the only
dead anchor is "a retired cell of another kind". What would decide it: whether `absent` should be its own name.

**Q-4 · `selectBody` and `acceptBody` have no `closes` check.** `StdHole.lean:296-316`: `propose` and `fill`
refuse `closed` past `state.closes`, `select`/`prune`/`accept` do not. Intended (closes = proposals close)
or an omission? The `shape` law freezes `closes` but does not bound acts by it.

**Q-5 · `Std.head`'s `fork` needs no evidence.** `StdHead.lean:83-89`: any holder of `[invoke fork]` freezes the
head forever by naming any `other` roots at the held step count. Same trust as `post`. Is a one-member
freeze intended, or should a fork carry the other poster's signed head?

**Q-6 · Preparation work outside the charge.** `runSetupWith` (`Program.lean:441-452`) performs the whole
contextual load (F-13) before it compares `S.preparation` with the budget (:495). The work is bounded by
static constants, so law 4 holds. Should the re-checks be charged, or measured on a WASTE row?

## Checked and found right (so the next reader can skip them)

- **The generators' binder arithmetic.** Every de Bruijn index in `activityWaiting`, `activityQueued`,
  `activityStartMethod`, `activityResumeMethod`, `activityRetireMethod` (`StdActivity.lean:93-238`),
  `offerGuard`, `offerTakeTree`, `offerTakeEdits` (`StdOffer.lean:125-230`), the escrow's `escrowTakeDone`,
  `escrowWithdrawBody` (`StdOfferEscrow.lean:93-133`), `headPost`, `headFork`, `headCase`
  (`StdHead.lean:41-89`) and `eqDataBody`'s sum arm (`StdData.lean:16-20`) names the variable its comment
  says it names. I counted the binders by hand; that is READ, not MEASURED.
- **The escrow legs.** The fuser pays its own `give` to the peer value's `payTo`. The nested take pays its own
  `give` to the fuser's `payTo`. Withdraw pays to the offer's own `payTo`, never to the caller. Post draws
  from `req.agent`'s account through the poster's own grant (`StdOfferEscrow.lean:81-121`).
- **The offer guard.** A retract is admitted only from the `fuse`, `take` or `withdraw` indices (:128-133). An
  upsert is `final`. An insert's box must be non-empty (`badTerms`).
- **The nested invoke.** A nested call's `Req` copies the root signer and window
  (`Kernel/Receive/Call.lean:439-440`). So `activityDue` and the session key read the same `notBefore` in
  the fuser and in its peer.
- **`peerOf`.** It refuses `samePeer`, `notParty` and a non-digest by name (`Program.lean:380-389`). The peer
  must be a live object of the SAME package before any of its rows are read (:401-402); LF4 is its row.
- **Escapes.** The layer's definitions contain no `partial`, `unsafe`, `implemented_by`, `native_decide` or
  `sorry`. The two `termination_by` clauses (`Program.lean:138,151`) are structural on fuel and on list length.

## Files not read whole (sizes in lines)

- `Lang/Surface.lean` 1089 (grepped only), `Lang/Subst.lean` 664, `Lang/Read.lean` 490, `Lang/Print.lean` 277,
  `Lang/Check.lean` 240 (header and constructors), `Lang/Resident.lean` 191, `Lang/Resident/Main.lean` 22,
  `Lang/Ty.lean` 112 (header), `Lang/HoleBudget.lean` 94, `Lang/Index.lean` 16, `Lang/Sim/Need.lean` 346
  (header, `requiredOf*`, `runTicksBy`, `extractTicksTwice`).
- `Lang/Contextual/Protocol.lean` 628 (header, definition list, lines 340-400).
- `Lang/Journey/ContextualReceive.lean` 205 and `ContextualWire.lean` 36 (assertion lines only),
  `ContextualCycle.lean` 116, `ContextualChecks.lean` 110 (lines 30-110), `Activity.lean` 28, `Main.lean` 24.
- `decisions/lang.md` 6906: LANG-75.14, 75.19, 76 and 77 read whole; LANG-P7 lines 4650-4665 and 4828-4840;
  the rest grepped.
- `Lang/Proofs/**`: another reader's. Only `Sound.lean:145-262` and `LiveClosed.lean:120-200` were opened,
  to check a comment and the twins' bridge.
