# READ-LANGPROOFS — reader of `Lang/Proofs/` (nanodregg origin/main f9657bd, 2026-10-24)

Reader: one subopus, layer LANG PROOFS, per `redregg/work/readers/BRIEF.md`. Nothing in nanodregg
was edited. Tags: READ (path:line), MEASURED (a command I ran; all were `grep`/`git grep`/`git show`
on the checkout at f9657bd, no builds), INFERRED (my reasoning from read statements).

## Verdict

I read the statements of every theorem the 10-22..10-24 cards landed (LANG-75.1–75.24, LANG-76,
LANG-77 L1+L2), WHOLE for the offer/fuse/escrow stack (`StdOffer`, `StdOfferFuse`,
`StdOfferEscrowFuse`, `PeerRead`, `DispatchRows`, `MethodRun`, `BellCommit`, `StdHoleCells`,
`Contextual/Failures`) and the generators they are about (`Lang/StdOffer.lean`,
`Lang/StdOfferEscrow.lean`, `Lang/Bell.lean`), and the statement-bearing parts of `Rel`,
`StdActivity`, `StdActivityMonitor`, `StdOfferEscrow`, `LiveHoles`, `Bell`, `StdHead`, `CallLive`,
`Data`, `Call`, `Load`, `Provenance` (header and statement list), `Contextual/*` (statement lists).
About 9,000 of the layer's ~32,000 lines read, weighted to the cards. MEASURED clean: no `sorry`,
`admit`, `native_decide`, `set_option`, `@[simp]` attribute, `unsafe`/`implemented_by`, or `axiom`
anywhere in `Lang/Proofs/**` (one `decide +kernel`, one `open Classical in` for a Prop `if`, both
honest); `gates/axioms-allow.tsv` holds no Lang row. The proofs are not where the trouble is; the
STATEMENTS are. The three worst things: **(1)** the escrow instance moves value on a judgment that
never reads the leg a party RECEIVES — `JointOk` reads only `role` and `terms`, θ moves nothing, so
`escrow_fuse_admitted` ("both legs moved") is true of a fuse that pays 5 α for 1 unit of anything;
**(2)** `posted_support_checked` and `revoked_support_refused_hole` (LANG-75.1's B1/B2 at the
generated judge) quantify a cell `g` that is tied to nothing — the "cell it cites" in their names
and docstrings is not in their statements; **(3)** the deployed arms keep outrunning the proved
arms: the LIVE range read CLIENT-36 made drivable has no authentication theorem (the exact gap
LANG-75.14 named for receipts and LANG-75.19 closed only for receipts), and after e7c2b13 the FUSE
method — which now judges first in every fuse — has no term-grain iff, only `fuse_run_sound`.

---

## Answers to the brief's named questions (each detailed in the findings)

* **`fuse_atomic` is about ONE fuse call** — it says: if `receive X w c = .ok t` for a signed
  `x'.fuse`, then `t.rows` holds the RETRACT touch (slot and act) of each party's offer row at the
  key the deal names for it. "Neither" is the no-Turn branch, excluded by name in the docstring.
  It does not say the session rows (that is `jointLaw_sound`), nor that the Turn admits (that is
  `invitation_once` / `escrow_fuse_admitted`). It is honest at its grain (READ
  `Lang/Proofs/StdOfferFuse.lean:602-643`). PT4 (the fuse drops its call) falsifies it with every
  premise satisfiable (INFERRED: `hy` still holds, `y'`'s retract is absent).
* **`take_iff_compliant` after e7c2b13** — still an iff at the method-term grain and still only
  soundness at the run grain, and now NARROWER than LANG-75.11's sentence reads: it is about
  `offerTakeBody` of `Std.offer` only (READ `StdOffer.lean:579-614`). There is no term-grain iff for
  `fuse` (which since e7c2b13 is the method that judges first and retracts in every fuse), none for
  the escrow's `take` or `fuse`, and its environment is not the receiver's (F5).
* **`run_edits_guarded`** — every edit of a RETURNING run (READ `Rel.lean:1208-1218`). That equals
  every row edit of an admitted Turn only because `Kernel/Receive/Derive.lean:222` is the one place
  a run's rows enter a Draft (MEASURED: `git grep "program.run"` in Kernel); no theorem states the
  Turn-grain composition (F14).
* **`activity_program_safe` — which deployed packages meet it** — MEASURED (`grep` over the five
  emitted `world/*/*` packages): only `world/resident/Bell` declares an activity log; Escrow, Head,
  Lifecycle, Allowance have no waiting guard, so the theorem says nothing about them. The Bell meets
  the premises through `bell_monitored` (READ `Bell.lean:61-73`). `Std.offer` and
  `Std.offerEscrow` (fixtures, not deployed per LANG-77) meet the premises syntactically (no imports,
  no holes, record body, `session_waiting = activityWaiting …`) but no instance theorem names them
  (MEASURED: `git grep activity_program_safe` hits only Bell, StdActivityTeeth, a docstring in
  StdOffer). `Std.hole` is outside (an application body with imports), as documented.
* **Bell theorems over `shapeOk pk`** — the premise is discharged at run time by a Lean decision the
  resident runs (`Hosting/Resident/Bell.lean:142`: `if Lang.Bell.shapeOk p then pure p else throw
  "notBell"`), carried by `Hosting/Proofs/SocketStrong.lean:531-574` (`describe_shape`), and by
  journey row LBw on the shipped core (`Lang/Journey.lean:2921-2932`). That is a real discharge, not
  an undischarged `wf`. What `shapeOk` checks is narrow (F11).

---

## Findings, ranked

### DEFECT

**F1. The escrow's judge never reads the leg a party receives; θ moves nothing.**
`Lang/StdOfferEscrow.lean` (READ, whole) types `offerJoint theta roles (escrowValTy …)` at the escrow
value, and `offerJoint` (READ `Lang/StdOffer.lean:102-110`) reads exactly `.get _ "role"` and
`.get _ "terms"` of each offer. `escrowTakeDone` / `escrowFuseDone` pay the OWN offer's `give` to
the PEER's `payTo` (READ `StdOfferEscrow.lean`, `escrowPay (.get (.var 5) "self") (.get (.var 1)
"payTo") (.get (.var 3) "give")`). Nothing compares the peer's `give` to anything the party
declared, and θ (the only thing the boxes constrain) is written to the session row's capture and
read by no transfer. So an "acceptance box" accepts any counter-leg.
WHY wrong: the object is named and documented as an escrow / DvP leg ("an offer that moves value",
LANG-75.18), and `escrow_fuse_admitted` (READ `StdOfferEscrowFuse.lean:113-133`) is stated as the
exchange theorem, but `EscrowLegMoved … P` has no conjunct about what `P` RECEIVES — only that its
own leg left and went to the peer's `payTo`. The theorem is true of a one-sided gift.
MUTATION / INPUT that shows it: X posts `give {5, α}`, box price `[5,10]`; Y posts `give {1, β'}`
(any minted denomination, any amount the kernel accepts), role ≠ X's, box price `[9,12]`; A invokes
`X.fuse` at price 9. Both takes return `JointOk`, both legs move, `escrow_fuse_admitted`'s
conclusion holds (INFERRED from the statements; journey LE1 is the same shape at 5 α / 7 β). No
judge refuses. LANG-75.18's critique says "the legs are fixed per offer and do not depend on θ …
a limit of the instance": that sentence prices the θ/price decoupling, not the fact that no
party's acceptance names what it wants to receive. This is the "honest label" on a transmutable
gap: the fix is a `want` field judged by the peer's take (or legs as functions of θ), not a
docstring.

**F2. `posted_support_checked` and `revoked_support_refused_hole` do not mention the cell they are
named for.**
READ `Lang/Proofs/StdHoleCells.lean:39-48`: `(cell pin : ByteArray) (p : HolePoint) … (look) (g : D)
(hlive : p.live = cellLive look g) (h : …probe… = 1) : p.cell = cell ∧ p.pin = some pin ∧ ∃ c,
look g = .ok (some c)`. `g` is a free parameter connected to `cell` (or `p.cell`) by nothing — no
`digestOf cell = some g`, no `keyCell`. Same at `:55-65` (`revoked_support_refused_hole`: `hdead :
look g = .ok none`, `hlive : p.live = cellLive look g`, no tie between `g` and `cell`).
WHY wrong: the docstrings say "the caller's pinned view holds THAT kernel cell live" (`:34-38`)
and "a fact … whose cell the caller pinned at its tombstone" (`:50-54`); the statements say "if
the bit equals `cellLive` of some `g`, that `g` is live / dead". Decision LANG-75.1 lists
`posted_support_checked` as "names a fact at the support's cell and pin AND, with the runtime's bit,
a cell the caller's pinned view holds live". The binding of `g` to the fact's key is only in
`cited_authenticated` (`Rel.lean:364-401`, which does bind `g` via `keyCell k = some b ∧ digestOf b
= some g`), at a different grain (the rows record), and no theorem composes the two or relates
`HolePoint.cell` to `keyCell k`.
MUTATION that the statement cannot see: `pointData` fills `live` from the cell of a DIFFERENT key
(say the first pinned point's) — `cited_authenticated` reds, but `posted_support_checked` and
`revoked_support_refused_hole` stay provable with `g` chosen as that other cell (INFERRED).
Severity DEFECT under the brief's definition: the theorem does not say what its name claims.

### DEBT (high)

**F3. The LIVE range read has no authentication theorem.**
CLIENT-36 (7fec6d7, MEASURED `git show --stat`) put the `live` column on range rows via
`Lang.keyColumns` and made `(facts (range 0 4) (live))` drivable from `nd --range` (its plant
`client/tests/pin.rs scan`). The Lean statements: `cited_authenticated` concludes only the POINT
slots (`Rel.lean:364-375`: `v = .record (slotsD "p" x.points ps ++ rest)`, `rest` unconstrained);
`receipt_row_authenticated` (`Rel.lean:476-495`) concludes range rows but requires `x.receipt =
true`. For `live = true, receipt = false, range = some _` no theorem says a listed row's `live` is
`cellLive look g` of the cell its key names. The 7fec6d7 message lists only install-side teeth
(`live_range_read_kept/typed/…`, READ `Rel.lean:1080-1108`) and its mutation M2 was observed red in
Rust only. This is LANG-75.14's own critique ("the most-used arm of the feature the least-proved
one") recurring one column over; LANG-75.19 closed it for `receipt` only.
MUTATION invisible to Lean: `keyColumns` returns `live := true` on range rows when `receipt =
false` — no Lang theorem reds (INFERRED; `keyColumns_ok` would, if it states the arm, but it is a
helper, and no PUBLIC statement about range-row liveness exists to be named red).

**F4. The fuser's run (the first judge of every fuse since e7c2b13) has soundness only, and the
escrow has no term-grain characterisation at all.**
`offerFuseBody` is `offerTakeTree … (offerFuseDone …)` (READ `Lang/StdOffer.lean:248-250`): the same
case tree as `take`, so a returned fuse has judged (`fuse_run_sound`, `StdOfferFuse.lean:297-326`,
gives `NamedKey ∧ JointOk`). But `take_iff_compliant` (`StdOffer.lean:579-591`) is stated at
`offerTakeBody theta roles rels od sd` with `offerValTy`; there is no `fuse_iff_compliant`, and none
for `escrowTakeBody` / `escrowFuseBody`. So the brief's question: LANG-75.11's "iff at the
method-term grain, soundness at the run grain" is still TRUE but now covers one of the four judging
method bodies (Std.offer take), and not the one every fuse runs first. The refusal teeth
(`take_offerUnpinned` … `take_notCompliant`, `fuse_refused_disjoint`) likewise name only
`offerTakeBody`. Since `offerTakeTree_inv` is generic over `done` and `V`, the fuse and escrow iffs
are a few lines each; their absence is undone work, not a theorem of the model.

**F5. `take_iff_compliant` is not at the receiver's grain, and its docstring says it is.**
READ `StdOffer.lean:570-591`: docstring "the generated `take` as the receiver applies it, over the
env `[req, arg, state, rows]` it builds". The statement applies `activityApply (activityMethod …)
[.var 3, .var 2, .var 1, .var 0]` INLINE in the env `rq :: arg :: state :: rows :: env`, so the
body runs under `rq :: arg :: state :: rows :: rq :: arg :: state :: rows :: env`
(`method_app`, `:485-492`). The receiver runs `apply4 g "take"`: the field is fetched from the
closure as `.clo _ []` and the body runs under exactly `[req, arg, state, rows]`
(`MethodRun.apply4_method`, READ `MethodRun.lean:55-72`; `Program.lean:324`). This is the same
doubled-environment mismatch LANG-75.9 named as the reason `waiting_*_iff` are NOT the monitor. For
a closed body the two agree, but no lemma transports the iff, and `NoRef` (no closure ref) is not
closedness. Every `take_*` refusal tooth and `fuse_refused_disjoint` share the grain. The
`StdActivity` `waiting_*` theorems (LANG-76's `waiting_retract_iff` etc., READ `StdActivity.lean:
112-215`) share it too — documented there as the "transparency half", which is accurate; the
offer's docstring is not.

**F6. `lost_reply_policy`'s Boolean has no deployed reader; its plants mutate a definition only the
theorem reads.**
READ `Lang/Proofs/Contextual/Failures.lean:223-229`: `lost_reply_policy (p) : (p.reliable = true →
LostKept p) ∧ (p.reliable = false → LostSpent p)`, proved by `cases p` into `kernel_lost_kept` and
`broker_lost_spent`. MEASURED (`git grep "reliable\|lostReply" -- '*.lean'`): `Peer.reliable` is
defined at `Lang/Contextual/NanoBridge.lean:83` and read only by this theorem and docstrings —
no resident, Host or Hosting code consults it. So "flip either Boolean and the theorem reds"
(PL5b/PL5c, LANG-75.16) is a tooth of a lookup table the theorem itself introduced; flipping it
changes no deployed behaviour. The content is `kernel_lost_kept` and `broker_lost_spent`; the
Boolean is decoration that reads as a policy the system enforces (the "a check that cannot fail"
class: no input to the system reaches it). LANG-75.16's critique half-says it ("defined by cases");
it should not be a named theorem with plants.

**F7. Stale comments that lie about the code below them (post-e7c2b13 / LANG-75.24).**
All READ:
* `Lang/Proofs/StdOffer.lean:2` "what the generated offer judge, its take and its matcher decide";
  `:11-12` "The matcher's code is not a premise" (also in `take_iff_compliant`'s docstring,
  `:574-575`). The matcher was deleted in e7c2b13.
* `Lang/Proofs/StdOffer.lean:749-750` (`take_resolve`): "argument `{pair, theta}`" — it is
  `{keys, pair, theta}` since LANG-75.20.
* `Lang/Proofs/StdOfferEscrow.lean:14-16`: "`fuse` makes no row act and `post` only inserts." Since
  e7c2b13 the escrow fuse retracts its own offer and pays its leg; the proof's `| 0` case
  (`:1060-1067`) handles exactly that. The theorem's own docstring (`:1043`) was updated; the module
  header was not.
* `Lang/StdOfferEscrow.lean` header: "Both takes run in the matcher's one tree, so both legs move or
  neither"; "`offer_guard` admits a retract only from `take` or `withdraw`" — the guard admits
  `fuse` too (`Lang/StdOffer.lean:129-132`); there is no matcher.
* `Lang/Proofs/LiveHoles.lean:15`: "From `Lang.Proofs.Contextual.LiveHoles`" — that module was
  moved out of `Contextual` at LANG-74.8.
* `Lang/Proofs/StdOfferFuse.lean:645-653` (`jointLaw_sound` docstring): "the pair names exactly the
  two parties (each one's `peerOf` is the other)" — the conclusion (`:669-689`) has no `peerOf`
  conjunct; it has `kx = kqy ∧ ox = qy ∧ ky = kqx ∧ oy = qx`, which is the consequence.

**F8. Decision entries the code no longer matches.**
* LANG-77 second landing (decisions/lang.md, "Theorems" and "Critique" of the L2 addendum, lines
  6869, 6878 and 6899 of the file): "the theorem takes `x' ≠ y'` … it is left as a premise to keep the
  Dispatched-based proof"; "Hypotheses gained: `escrow_fuse_admitted`'s `hne`". LANG-75.24 removed
  it (READ `StdOfferEscrowFuse.lean:113-128`, no `hne`). LANG-77's text is not annotated as
  superseded; a reader of LANG-77 alone gets the wrong statement.
* LANG-75.21: "In the proof, fuse has no row acts (`fuse_calls`)". `fuse_calls` is deleted and the
  fuse retracts (READ `StdOfferEscrow.lean:1060-1067`).
* LANG-75.22's critique: the coupling (`qx = oy`, `x' ≠ y'`) "follow[s] from the same proof once
  those helpers are public". Since e7c2b13/LANG-75.24 `methodReads_offer`, `peer_of_pair`,
  `readsData_offer` are public (READ `StdOfferFuse.lean:193-234, 429-448`) and `x' ≠ y'` is gone,
  but `EscrowLegMoved` still does not carry the coupling (F10). The owed item is unblocked and
  open, with no cv task named in the entry.

**F9. Law-1 twins in the proof layer, after a card titled "Law 1 … twins deleted".**
MEASURED (`git grep "theorem conforms_opt\|theorem conf_opt\|theorem conforms_empty\|theorem
conf_unit"`): `Lang/Proofs/CallLive.lean:99,102` (`conf_unit`, `conf_opt`, public),
`Lang/Proofs/StdActivityMonitor.lean:70,73` (`conforms_empty`, `conforms_opt`, private),
`Lang/Proofs/StdOffer.lean:794,798` (`conforms_empty`, `conforms_opt`, public): three copies of one
fact (the `optD none` vs `.inj "none" (.record [])` spelling is definitional). Also
`StdActivityMonitor.bigStep_get_data` (`:113`) beside `MethodRun.get_data` (converse direction,
fine) and the private `slot_p1/slot_e2/slot_c1` `decide` lemmas repeated in `StdOffer`,
`StdOfferFuse`, `StdOfferEscrow`, `Bell`. The duplicated `fuseOkEnv` abbrev is acknowledged in
LANG-75.24 as forced by gate C3. LANG-75.24 lists the twins it deleted and is silent on these.

**F10. `EscrowLegMoved` does not say the fuser's leg goes to the payTo of the offer its peer
consumed.**
READ `StdOfferEscrowFuse.lean:44-64`: for party `P`, `q` is "the offer `P` read under its peer", at
whatever key `kq` the peer slot held; the conjunct `NamedKey (bytesOf P) keys pair k` is about `P`'s
own key only. That `kq` is the key `y'` consumed (`ky`) is TRUE — both reads are `readsData` of the
one pinned point `p0` of `y'`'s offer relation (`readsData_offer_args`, `StdOfferFuse.lean:246-250`)
— and `jointLaw_sound` proves the analogue for `Std.offer` (`kx = kqy ∧ ox = qy …`). The escrow
statement omits it, so a reader of `escrow_fuse_admitted` cannot conclude "X paid the payTo of the
offer Y retracted" from the statement. INFERRED: no attack (the pins make it one row); a statement
gap. Docstring (`:102-112`) says "into its peer offer's `payTo` account", which reads as the
coupling.

**F11. `Lang.Bell` restates the Bell's terms by hand, and `shapeOk` checks only two of its fields.**
READ `Lang/Bell.lean:26-104`: `ask`, `resumer`, `answerBody`, `answer` are hand-written Lean terms
restating `world/resident/Bell.ob`'s `answer` and plan; `shapeOk` (`:108-111`) compares imports,
holes, state, rels, `answer`'s iface type and the body fields `answer` and `rung` by equality. It
is a pinned twin (LBw refuses drift, so it fails loud), but it is two definitions of one fact (law
1), and the theorems over it cover `answer` and `rung` only: `ring`, `retire`, `open`, `close`, the
`queued` guard and the law `bell` can change freely under `shapeOk`. `bell_monitored` is safe for
ANY method (its premise is `rung`), but `answer_commits`' "no `pending` row" relies on `answer`'s
edits, and nothing pins `queued`'s refusals.

### DEBT (lower)

**F12. LANG-75.24's plant C6 cannot red the statement whose premise it was about; the premise was
redundant by a second route the decision does not name.**
LANG-75.24 drops `hne : x' ≠ y'` from `escrow_fuse_admitted` because "the peer is not `x'`: `x'` is
already in the walk" (`revisited`), and plants C6 (`revisited` check → `req true`), which reds
`Kernel.Proofs.Tree.invoke_ok` and `Authority` (decisions). Re-derived from the statements
(INFERRED): if the peer `p` were `x'`, the fuser's own read and its peer read are `readsData` of the
same object, relation and pinned point (`readsData_offer_args`), so `o = q`, so `o.field "role" =
q.field "role"`, so `JointOk` (first conjunct `≠`) is false and `fuse_run_sound` cannot return —
the fuser refuses `sameRole` before it ever invokes. So under C6 `escrow_fuse_admitted` without
`hne` is still TRUE (the plant breaks a proof route, not the statement), and `hne` was derivable
from `JointOk` alone even before `dispatched_invoke_fresh` existed. Not wrong, but the plant is not
evidence for the premise drop, and the decision's "the premise was needed because `peerOf`'s
`samePeer` check compares bytes" is half the story.

**F13. `WaitingStep.answer`'s `Resumes` is existential over the environment.**
READ `StdActivityMonitor.lean:36-38`: `Resumes lib resumer req state := ∃ env, env[3]? = some
state ∧ env[2]? = some req ∧ BigStep lib env (activityApply resumer [.var 3, .var 2]) (.ok true)`.
For a resumer closed under its two lambdas this is its meaning (LANG-75.9's critique says so). The
premise `activity_program_safe` takes is `NoRef resumer` (no closure `.ref`), not closedness; a
hand-written package whose `activityWaiting` resumer refers to the guard's own binders (the edit
input at var 0 under the guard's lambdas) typechecks, and then `Resumes` is satisfiable by an env
the receiver never builds. QUESTION: does `checkWith` refuse such a resumer? If not, the monitor's
`answer` step over-approximates for every non-generated package. The deployed Bell's resumer is
closed (READ `Lang/Bell.lean:42`), so the Bell is unaffected.

**F14. No Turn-grain "every row touch passed its guard".**
`run_edits_guarded` (READ `Rel.lean:1208-1218`) is at the run; `dispatched_invoke_rows`
(`DispatchRows.lean:196-226`) puts a dispatched run's rows in `t.rows`. Their composition — every
row touch of a Turn `receive` sealed is an edit of some dispatched run whose guards accepted it —
is not stated. It holds only because the one row source is the invoke run (INFERRED from
`Kernel/Receive/Derive.lean:222-230`, READ); a second source (a future `Body` that edits rows) would
not red anything in Lang.

**F15. Refusal arms that cannot be reached.**
`offerGuard` (READ `Lang/StdOffer.lean:125-137`) refuses a retract on occasions `adopt`, `birth`,
`relaw`, `write` (`notConsumer`); `activityWaiting`-guarded relations have the same occasion
arms. Guards run only from `runMeasuredWith`'s `guardEdits` (`Program.lean:506`), whose request is
`invokeRun`'s, occasion `.invoke method` always (`DispatchRows.invokeRun_req`,
`DispatchRows.lean:300-305`). So those four arms are total-match filler, never a reachable
refusal. Minor, but law 7 counts names on the wire, and these names can never appear.

**F16. Offer theorems carry `hR : (offerRoleTy roles).wf = true`, discharged by no lemma from the
generator's own check.**
Every offer/escrow run theorem takes `hR` (e.g. `StdOffer.lean:1006`, `StdOfferFuse.lean:302`,
`StdOfferEscrow.lean:419`). `offerPackage` refuses `tooFewRoles`, `duplicateRole` and runs
`checkWith []` (READ `Lang/StdOffer.lean:301-309`), but there is no `offerPackage … = .ok p →
(offerRoleTy roles).wf` lemma; the fixture discharges it by `decide` (`roles_wf`, `:1102`). QUESTION
only: the premise is satisfiable and decidable; it is not vacuous.

**F17. `fuse_atomic`/`jointLaw_sound`/`invitation_once` take the peer's package as a premise that
`receive = .ok` already implies.**
`hy : ∃ cl, w.live X.env y' = some cl ∧ cl.slots.get slotPackage = some (X.env.bytes pkg)`
(`StdOfferFuse.lean:625`). The fuser's peer read refuses `peer: another package` unless the peer's
package slot is `bytesOf pkg` (`PeerRead.peerReads_package`, `PeerRead.lean:110-133`). So `hy` is
derivable from `hc` (modulo the pinned-vs-live and `X.env.bytes` vs `bytesOf` spellings). Weaker
than it could be, not vacuous. QUESTION.

**F18. Definitions living in proof modules.**
`Lang/Proofs/Contextual/ProtocolTyping.lean` defines `HasProt`, `Runs`, `Reach`, `Started`,
`SubBag`, `Fills`, `SubstOK`, `Open.WF` (READ, `grep ^inductive|^def`); `Proofs/Contextual/
Protocol.lean:385` `def IsCall`; and the spec Props `JointOk`/`InBox`/`NamedKey` (StdOffer),
`ViaReads` (StdOfferFuse), `EscrowLegMoved`, `WaitingStep`/`Resumes`, `AtOk`, `LostKept`/`LostSpent`.
The Prop-valued specs are arguably statements, but `ProtocolTyping` is a definitions module under
a `Proofs` path. QUESTION for GATES: does `gates/closure.py` C3 intend to allow it (law 8: "a module
exports definitions OR proofs")? The calculus has no deployed consumer (LANG-75.17), so the cost
is only the law.

---

## The plants, re-derived from the statements (three cards and two more)

1. **LANG-75.24, plant C6 (`revisited` → `req true`)** — see F12. Re-derivation: under C6 the
   statement of `escrow_fuse_admitted` without `hne` stays true (the fuser's `sameRole` refuses a
   self-pair before any invoke); C6 reds only the Kernel lemmas it was reported to red. The plant
   is a tooth of `dispatched_invoke_fresh`, not of the dropped premise. (INFERRED.)
2. **LANG-76, P1 (the log arm's comparison dropped, `some _ => okT`)** — `waiting_retract_
   unanswered_meaning` (`StdActivity.lean:112-140`) concludes `if n + P ≤ m then ok else refused`;
   under P1 the guard answers `ok` at `m < n + P`, so the statement is false: a real tooth. P1 also
   falsifies `waiting_body_step` (the admitted retraction is no `WaitingStep`: `timedOut` needs
   `n + p ≤ m`, `retire` needs an answered row), so the MONITOR has a tooth here too; LANG-76's red
   list does not name it because `StdActivityMonitor` is in the unbuilt cone below the red
   `StdActivity` (INFERRED; LANG-75.9's lesson about cones). **P2 (the arm refuses always)** is
   correctly reported as a tooth of the transparency theorems only: refusing more keeps every
   safety statement true, so no monitor theorem can see P2.
3. **LANG-75.20 PA (the name check skipped), after e7c2b13** — `take_iff_compliant` (→) is false
   at LF8 (the take returns with `NamedKey` false); post-e7c2b13 the fuser shares `offerTakeTree`,
   so PA also makes `fuse_run_sound`'s `NamedKey` conjunct and `fuse_atomic`'s first conjunct false
   at a fuse whose own pin is not the named key. A real tooth of four statements (INFERRED).
4. **LANG-75.16 PL5b/PL5c (flip `Peer.reliable`)** — reds `lost_reply_policy`, but the flipped
   definition has no reader outside that theorem (F6): the plant tests the table, not the system.
5. **LANG-75.21 P8g (the take pays its own offer's `payTo`)** — reds `escrow_take_run_sound`
   (its call conjunct names `q.payTo`), and, as LANG-75.21 itself says, NOT the statement of
   `escrow_retract_moves_leg`, whose payee is a disjunction (`o.payTo ∨ peer's payTo`, READ
   `StdOfferEscrow.lean:1046-1058`); it reds that theorem only through its proof. Confirmed from the
   statement.

## What I checked and found right (so the next reader need not)

* `fuse_run_sound` (`StdOfferFuse.lean:297-326`): every conjunct is about the deployed run
  (`Lang.program … .run`), the call is the ENCODING of exactly `{keys, pair, theta}`, the rows are
  exactly two. PT3/PT4 each falsify it. No disjunct.
* `jointLaw_sound`'s one-θ claim is the codec's canonicity (`Wire.decodeData_eq_ok_iff`,
  `:699-702`), not a forwarded blob. The coupling `kx = kqy ∧ ox = qy` is genuinely proved via
  `readsData_offer_args`.
* `invitation_once` reads `Kernel.admit_retract_row` directly (the LANG-75.24 alias is gone); its
  `RowsCanon` premise is discharged from genesis (`Kernel/Proofs/Rows.lean:451-461`).
* `escrow_fuse_admitted`'s value conjunct is literally `admit_value hcan ha d` (`:176`), not a
  second count; `hcan`/`hrc` are the kernel's canon invariants, dischargeable by fold.
* `cited_authenticated`, `receipt_column_authenticated`, `receipt_row_authenticated` bind the
  checked cell to the key (`keyCell k = some b ∧ digestOf b = some g`) — the binding F2 lacks.
* `selectHole_hypotheses` / `selectHole_live_selects` / `selectHole_factor` / `selectHole_cell_
  support` / `revoked_support_refused` (ROM grain): no free cell, each conclusion is about
  `selectHole` itself; `selectHole_live_selects` restates the refusal arms as premises, as
  LANG-75.5's critique says.
* `submit_at_most_once` and `reach_submit_at_most_once` (Failures.lean:52-73): real, no premise at
  the reach form.
* `peerOf_party`'s `a ≠ b` is byte inequality, honestly stated; the private `LawfulBEq ByteArray`
  instance (`PeerRead.lean:17-25`) is proved, not assumed.
* `callsOf_live` keeps its conclusion with `callSlotOk` carrying `dataTy` (`CallLive.lean:436-446,
  563-570`); `encodeData_of_conforms` (`Data.lean:365-368`) is the totality LANG-77 claims.
  `callData_isSome` gains exactly the one honest hypothesis LANG-77 names (`Call.lean:228-231`).
* `head_*` (StdHead): over `Admits` and BigStep, `IsChange` excludes birth/adopt; no vacuous form.

## Files NOT read (sizes in lines, `wc -l` at f9657bd)

In the brief's list, read only in part (statements / headers):
`Provenance.lean` 1433 (header + statement list + `keyColumns_digests`; proofs not read) ·
`Rel.lean` 1220 (lines 1-80, 284-525, 1000-1220) · `StdOfferEscrow.lean` 1112 (statements and the
linear corollary; `*_core` proofs not read) · `LiveHoles.lean` 789 (1-130, 225-300, 395-420) ·
`CallLive.lean` 707 (99-113, 414-578) · `Subst.lean` 641 (header, `hasType_usesVar_lt`) ·
`Load.lean` 516 (header, `runSetup*_spec`) · `Fill.lean` 525 (header, statement list) ·
`StdActivity.lean` 507 (statements of LANG-76 arms) · `StdActivityMonitor.lean` 439 (1-210,
355-439; `waiting_body_step` proof body 200-290 skimmed) · `Bell.lean` 315 (1-120, 260-315) ·
`StdHole.lean` 211 (statement list) · `LiveJourney.lean` 162 (statement list) ·
`Contextual/Protocol.lean` 929, `Contextual/Negotiation.lean` 260, `Contextual/ProtocolTyping.lean`
131, `Contextual/LangInstance.lean` 161 (statement lists and headers only).

In `Lang/Proofs/` but outside the brief's list, not read: `Print.lean` 1658 · `Std.lean` 1100 ·
`Wire.lean` 1024 · `Extract.lean` 843 · `Invoke.lean` 805 · `Need.lean` 792 · `Receiver.lean` 645 ·
`Call.lean` 590 (statements of LANG-77 only) · `KeyOrder.lean` 537 · `PrintWire.lean` 522 ·
`StdRun.lean` 503 · `LawMeaning.lean` 433 · `StdFits.lean` 418 · `Data.lean` 370 (statement list) ·
`Check.lean` 361 · `Surface.lean` 359 · `Agree.lean` 342 · `DispatchRows.lean` 323 (read 1-35,
80-323) · `Sound.lean` 319 · `StdChain.lean` 318 · `Complete.lean` 317 · `CallTeeth.lean` 307 ·
`StdActivityTeeth.lean` 295 (statement list) · `BigStep.lean` 283 · `StdTeeth.lean` 271 ·
`LiveClosed.lean` 268 · `Canon.lean` 267 · `PrintParse.lean` 255 · `StdData.lean` 248 ·
`Prints.lean` 232 · `LiveTeeth.lean` 206 · `LawRun.lean` 198 · `StdHead.lean` 194 (statements read)
· `Derives.lean` 193 · `LawReceiver.lean` 189 · `NeedComplete.lean` 186 · `Run.lean` 176 ·
`Chain.lean` 175 · `HoleBudget.lean` 168 · `Cost.lean` 167 · and the small teeth/leaf modules
(`CostTeeth`, `StdHoleCoverage*`, `StdHoleLookup`, `StdHoleTeeth`, `StdDataTeeth`, `Teeth`,
`WireTeeth`, `PrintTeeth`, `SurfaceTeeth`, `JourneyTeeth`, `LiveInvoke`, `LiveNeed`, `Meaning`,
`PrintLine`, `Read`, `Relocate`, `Row`, `RunTy`, `Typing`, `Index`), each under 200 lines.
