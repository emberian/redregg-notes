# DESIGN-OBS — the World measures itself; the outside enters as a judged fact (axes 4 and 5)

Design memo, real 2026-10-26/27, by FABLE-OBS. Read against nano `origin/main` **18cd38b** (worktree
`hbox:/tank/dregg-build/nanodregg/wt/fable-obs`, `.lake` a real copy of `wt/fable-ctx`'s at that tip; nothing
`cp -al`). Inputs: FRONTIER-AXES-20261026.md (4, 5), VERDICT-20261024.md, HOLISTIC-GATES.md, HOLISTIC-KERNEL.md,
TOPLEVEL-SPEC.md (§5, §7, §9, §11), DESIGN-TRUST.md whole, `gates/waste.tsv` + `gates/waste.py`,
`scripts/converge`, `scripts/bar.sh` + `gates/bar.tsv`, `decisions/perf.md` PERF-2, `decisions/kernel.md`
KERNEL-44/50/55, `Kernel/World.lean` (refusal windows, `refusalsCounted`, `checkRefusal`, `commitRefusal`,
`pruneRefusals`), `Kernel/Turn.lean`, `Kernel/Receive/{Call,Derive,Submit,Rederive}.lean`, `Kernel/Bounds.lean`,
`Protocol/Foreign.lean` + `Protocol/Proofs/Foreign.lean`, `Lang/StdHead.lean`, `Lang/Rel.lean` (the receipt
column), `Lang/Journey/Head.lean`, `client/tests/foreign.rs` + `fixtures/foreign/Accept.ob`, `world/escrow/Escrow.ob`,
`Lang/Surface.lean` (grammar), `Kernel/Sim/Required.lean`. Tags: **READ** (path) · **MEASURED** (a command I ran)
· **INFERRED** (attack these first).

## 0. The answer in one page

**Axis 4.** The instrument panel is outside the system because it measures three different kinds of number
and only one of them is the World's to know. (A) **Counters that are functions of the log** — steps, height,
allowance, refusals per member per window — the kernel already maintains, members already re-derive, and a
receipt already proves (the refusals trie: a window counter as a trie leaf under the chain, KERNEL-44/50).
The two that are missing are the two a member can spend without bound today: **ticks** (a signed invoke
runs `min budget treeTicksMax` = 131072 ticks per call, at every height, forever; READ `Derive.lean:365`)
and **bytes** (one World allowance, no owner; HOLISTIC-KERNEL §3.2(3)). (B) **Bounds that are theorems
about the implementation** — hashes per required, trie hashes per turn, bytes per turn (READ
`gates/waste.tsv` rows 9–15, 45) — are not the World's state: the World cannot count its own hashes without
an instrumented twin (which is what `Gen.countingEnv` and `Kernel/Sim/Required.lean` are), and the honest
form is `theorem hashes(admit t) ≤ requirement(t)` beside a sim that prints the ratio, which is what exists.
Moving them into cells would be a twin of the sim inside the kernel. (C) **Wall time** — THE BAR's two
limits (`write-p99-ms 5000`, `reopen-ms 60000`, READ `gates/bar.tsv`) — the World can never know; and
**PERF-2 already ruled it** (READ `decisions/perf.md:58`): "THE BAR … gates counts, never a clock"; every
count the bar pins is a WASTE row, the clock is a liveness deadline reported beside its load. So the question
"can the bar's limits become a law the World refuses to violate" has the kernel's answer already in it: the
kernel refuses WORK past a bound (`overBound`, `overTicks`, `overAllowance`), never time; what it can add is
the RATE, which is what the window counters are.

So the design is one object: **the meter leaf**, `RefusalSlot.ticks member win ↦ RefusalLeaf.count n`, a
fourth key kind of the trie the kernel already prunes by window (the "refusals trie" is the WINDOW trie: it
holds per-window per-member counters and the records that justify them), written by `World.admit` for every
Turn whose `ticks > 0`, refused `ticksBudget` by name when a member's window would pass
`Bounds.ticksPerWindow`, pruned at the window's end exactly as the refusal counts are, read by a member from
its own fold (`nd meter`), and provable to a third party by a path against the refusals root beside TRUST's
attested or certified head. For that the Turn must say who signed it and what it spent: two fields, `member`
and `ticks`, both RE-DERIVED by every follower from the event (READ `Rederive.lean`: a page carries the
call, never the writer's Turn; `submit` on the follower builds the Turn, and a writer that wrote another
`ticks` is `eventMismatch`). The writer cannot fake the meter for the same reason it cannot fake a refusal
record. A **health receipt** is then: a head (own, attested or certified: DESIGN-TRUST §1.2) and the paths of
the counters one wants under it; "is this system healthy" becomes `nd meter` on one's own follow (no
signature: the fold IS the measurement) or a receipt a phone checks with one head. What stays outside, and
should: the hash and byte ratios (theorems + sim), the clock (THE BAR), and the gates over the TREE (the
size ratchet on code, the census), which are about the Lean, not the World — until axis 1 makes packages
installed objects, at which point "a package's bytes" is already a charge and a size law is one line.

**Axis 5.** nano's clock is the height and nothing else is time: `notBefore`/`validUntil` are heights
(READ `Turn.lean`, `checkWindow`), `Req` carries them so a law can say "not before h" without reading the
World (READ `Call.lean:318-330`), `(patience n)` is in heights (READ `Surface.lean` header). Real time enters
in ONE place: the writer chooses which height a call lands at inside its window. The writer is therefore
already an oracle — of ordering — trusted for liveness only (CHARTER §Scope 3; TOPLEVEL-SPEC §7 "delay or
withhold"), and confined by the window. An OUTSIDE fact must enter the same way everything enters: as a
member's signed call, admitted by a law, read by other laws from the state. Three places to put the trust,
priced below: **(i) an oracle is a World** (E5): a fact is a call A admitted, proved to B by a receipt
against a head of A that B holds; the trust is the head's provenance, which is exactly DESIGN-TRUST's
`Authority` (none → the poster; 1 → A's writer; 2f+1 → A's committee). **(ii) an oracle is a member with a
grant**: a fact is a post into a fact object; the trust is a key, or a key list under the `quorum` law the
surface already has (READ `Surface.lean` header: `(law ℓ (quorum f k #hex…))`). **(iii) an oracle is a cell
kind with a provenance field**: the kernel verifies a foreign signature at admission; refused (a verifier of
foreign keys in the kernel, a second leaf kind, the trust model moved from laws into the TCB). The pick is
(i) BETWEEN Worlds with (ii) INSIDE the oracle World: an oracle World's members are its committee, the
`quorum` law is its agreement, and the head's authority is what a consumer World trusts. That makes the
oracle problem the trust-model question DESIGN-TRUST already answered, with the same three rows, and not a
transport question. The prototype is time, because time is the fact every escrow wants and the only one the
kernel can state honestly: a receipt from World A shows the HEIGHT at which A admitted a call; a law in B
requires `receipt.height ≥ deadline`. That is Roughtime's shape — a signed midpoint with a radius — where the
midpoint is a height and the radius is A's window; what B learns is "A's writer ordered this at ≥ h and a
member of B who follows A says A's head is there", never a second of UTC. The one way it is wrong is the one
every oracle has: liveness. A stalled A never reaches `deadline`, and the timelock never opens; the honest
remedy is the fallback clause every heartbeat oracle has — "or B's own height ≥ deadline + slack" — which is
`(patience n)` in B's own clock, and the design says so rather than hiding it.

**What is built in this lane** (§4): the timelock fixture over two real Stores (zero kernel change, one
package text, journey rows TL0–TL3, one `client/tests/foreign.rs` row), landed first; then the meter: `Turn.member`,
`Turn.ticks`, the `ticks` key kind, `ticksBudget`, `Bounds.ticksPerWindow`, `nd meter`, the kernel-sim
exhaustion probe and the journey row that reads it back — a `kernel!` flag day (the Turn codec and the
refusal code table move; every Store re-geneses; a pre-meter Store refuses `shapeMismatch`).

---

## 1. SELF-MEASUREMENT

### 1.1 What is measured today, and from where (MEASURED)

| instrument | what | where it runs | who can check it |
|---|---|---|---|
| `gates/waste.tsv` (84 rows) + `waste.py` | work ÷ required work per operation; ceilings only fall; exact rows (`=1`) for THE BAR's forced contention | Python over `WASTE op metric v` lines the sims and benches print, one box, at convergence | whoever runs `scripts/standing.sh` on the tree |
| `scripts/bar.sh` + `gates/bar.tsv` | counts per command (pinned via waste rows, op `bar`), and the clock (`write-p99-ms`, `reopen-ms`) judged in every run beside the load | one box, three `nd` actors over real sockets | the same |
| `scripts/converge` | the standing verdict over the tree, attributed to commits, reverting a red still red at the next convergence | one box, a systemd timer, a flock | ROOT reads `convergence.log` |
| `Kernel/Sim/Required.lean` | the hashes a transition REQUIRES, read off the tries it built, so the ratio is 1.000 on every draw | the sim, with `Gen.countingEnv` as an instrumented `Env` | the sim's run |
| **`World.refusals`** (READ `World.lean:201-229`, `refusalsCounted` :1739) | per member per window: refusals recorded; per World per window: the total; the records that justify both | **the kernel, at every `World.refuse`**, under the chain, pruned by window | **every follower by re-execution; any holder of a head by a path (`Receipt.check`'s `rpath`)** |

The last row is the only one inside the system, and it is complete in the sense the brief asks for: the
counter is a function of the records (KERNEL-50: "a World's refusal counts are its records'"), a decoded base
is refused unless the counts are the tally, a forged count is a `kernel/refusals-counted` refusal by name, and a
17th refusal is `refusalBudget`, declined and unrecorded. HOLISTIC-KERNEL §1.3(f) called it "a rate limiter
written as a ledger invariant, because there is no fee". That is the shape to copy, not a thing to apologise
for: a ledger invariant is what a self-measurement IS when the system's product is checkable statements.

### 1.2 Three kinds of number, and which the World can own

A measurement cell is honest only if a member can recompute it from the log alone. That sorts every row above:

**(A) Functions of the log.** `steps`, `height`, `chain`, `allowance` (World fields, READ `World.lean:273-297`),
the refusal counts, and — not yet — a member's **ticks** and **bytes** per window. Each is decided by
`World.step` and nothing else; a follower that folds the same log holds the same value; a path against the
head proves it to a stranger. These are the only candidates for cells. Two are missing, and both are DoS
holes the refusal window closed for refusals and nobody closed for admissions: a member may burn
`treeTicksMax` per call and `weightMax` bytes per turn at every height it can get a call into, bounded only by
the World's one allowance (bytes) and by nothing (ticks). The journal already knows which turns landed in a
window; it does not know who signed them or what they ran, because `Turn` carries neither (READ
`Turn.lean:107-120`: txId, window, touches, creates, nullifiers, charge, event, rows, ranges). The event does
(opaque to the kernel by design). `Refused` carries `member` for exactly the reason a Turn should (KERNEL-50:
"so a window's count is a function of its records, and a receipt names WHO was charged").

**(B) Properties of the implementation.** Hashes per required, trie hashes per turn, bytes-per-turn,
fsyncs per batch, index bytes per appended byte. These are statements about `Trie.insertAll`, the record
codec and the Store's group commit — true of the CODE, measured on any World, independent of the log's
content beyond its shape. The World cannot observe its own hash count: `Env.hash` is a function, not a
counter, and counting it means an instrumented `Env` (`Gen.countingEnv`, READ `Sim/Gen.lean:188-420`) beside
the deployed one — a sim twin, which is the right place for it. What the World CAN own of (B) is the
REQUIREMENT, which is already a function of the Turn and the trie shape (`Required.insertReq`, `batchReq`,
`fresh`): a theorem `hashes (admit t) ≤ k · required t` is the honest form, and the sim's 1.000 is its
witness, not its replacement. Do not move these into cells.

**(C) Time.** The bar's two limits. The World has no clock; a writer that fsyncs slowly is indistinguishable,
in the log, from one that fsyncs fast. PERF-2 ruled this the day THE BAR was built: counts are gated, the
clock is reported with its load and judged as a liveness deadline only. A "latency law" the kernel enforces
would be a law about something it cannot read; the kernel's honest contribution to latency is the WORK bound
per turn (every number in `checkBounds`, READ `World.lean:898-927`: touches, ops, creates, event bytes,
weight, rows, ranges; and `treeTicksMax` for the run) and, after this design, the work RATE per member per
window. THE BAR then measures work → time on one box, which is what a bar is.

### 1.3 The meter: what a self-measurement cell IS

**Definition.** A self-measurement cell is a leaf of the window trie whose value is a function of the log's
steps in the current window, maintained by `World.step`, bounded by a `Bounds` constant whose breach is a
kernel refusal by name, pruned when the window turns, and re-derived by every follower from the events alone.

**The object.** In `Kernel/World.lean`:

```lean
inductive RefusalSlot (D : Type)
  | tx (id : D)
  | count (member : D) (win : UInt64)
  | total (origin : D) (win : UInt64)
  | ticks (member : D) (win : UInt64)        -- NEW: the member's ticks this window (kind byte 3)
-- leaf: the existing `RefusalLeaf.count n` (kind byte 1, eight bytes): no new leaf constructor
```

The key bytes keep one width (kind byte, digest, eight bytes: `refusalKeyBytes_size` unchanged), so the
trie's prefix-freeness and CODEC's key order are untouched (READ `World.lean:472-480`). `RefusalLeaf.fits
(.ticks ..) (.count _) = true`; `refusalFits height (.ticks _ win) (.count n) := win = refusalWindow height ∧
1 ≤ n ∧ n ≤ Bounds.ticksPerWindow`; `keptRefusal H (.ticks _ win) _ := win = refusalWindow H` (pruned with
the counts at every multiple of `windowMax`, READ `World.lean:1555-1565`).

**The Turn.** `Kernel/Turn.lean` gains `member : D` and `ticks : Nat`, in the log record (`logWeight` +
`digestWeight + counterWeight` = 40 bytes; `Codec.Kernel.turn` gains `dc` and `nat64`; `turn_size_logWeight`
restates by the two fields). `Receive.sealTurn` sets `member := c.unsigned.member` and `ticks := poolOf
c.unsigned.body − wk.pool` (the Walk's pool after the tree; `derive` today drops the Walk, READ
`Derive.lean:371-374`: one `.map` becomes a pair). `checkBounds` adds `t.ticks ≤ Bounds.treeTicksMax` (a
forged log cannot jump the meter) under `overBound .ticks`.

**The check and the commit** (beside `checkWindow`/`commitWith`):

```lean
def ticksUsed (E : Env D) (w : World D) (m : D) : Nat :=
  match w.refusalAt E (.ticks m (refusalWindow (w.height + 1))) with | some (.count n) => n | _ => 0
-- in `check`: req (ticksUsed E w t.member + t.ticks ≤ Bounds.ticksPerWindow) (.ticksBudget t.member)
-- in `commitWith`: refusals := pruneRefusals E (w.height + 1)
--   (if t.ticks = 0 then w.refusals else w.refusals.insert (refusalSpec E) (.ticks t.member win) (.count (used + t.ticks)))
```

The window is `refusalWindow (w.height + 1)`: the height the Turn LANDS at, as a journal entry's, so the leaf
and the journal agree on which window a turn is in. A turn with `ticks = 0` (everything but an invoke)
writes nothing: the meter costs one trie path per INVOKE, not per turn (the waste row `admit
trie-hashes-per-turn` moves only for invoke turns; the sim's `Required` gains the path, §1.7).

**The refusal.** `Reject.ticksBudget (member : D)`: "the member's ticks this window would pass
`Bounds.ticksPerWindow`". It is a KERNEL rejection of a derived Turn (class (A) of KERNEL-44: authenticated,
after the pins), so `judge` RECORDS it like `overAllowance`: the member spent a refusal slot and the call is
final within its window. That is the right severity: a member that can exhaust its window has done 16
full-budget runs in 1024 heights and should re-sign later, and a recorded refusal is what lets the writer
answer the retry without re-running the program (the receipt names the code).

**The bound.** `Bounds.ticksPerWindow := 16 * treeTicksMax = 2^21` (2,097,152). Sixteen full-budget trees per
member per window, by analogy with `refusalsPerWindow = 16`; at THE BAR's 30 ticks per invoke (READ
`Bounds.lean:80-85`) it is ~70,000 invokes per member per 1024 heights, which no honest row approaches. A
taste number, like its sibling; the critique in §1.8.

**Why the window trie and not a cell.** A kernel-owned cell in the cells trie would be touched by a Turn
that did not name it: `admit_frame` (an untouched cell is unchanged), `fold_potential` (weight accounting),
and every pin theorem would gain a case, and a member's own calls would serialise on the meter cell's pin if
the receivers wrote it as a touch (the same reason KERNEL-54 kept refusal counts out of the pins). The window
trie exists for per-window per-member counters and is pruned on the schedule the meter wants. **Why not a
fifth trie:** HOLISTIC-KERNEL §2.2 already judged the fourth instance a wrong cut; a fifth with its own
`_sep` family and head read is the thing to stop doing.

**Why the member is in the Turn and not recovered from the event.** The kernel never reads the event (law:
the Turn is "everything the follower needs … and nothing it would have to trust", READ `Turn.lean:1-20`);
`Ctx.decodeCall` lives in the receive layer. A `memberOf : ByteArray → Option D` in `Env` would put a call
decoder in `World.admit`'s hot path and in every kernel theorem's premises. Two fields, re-derived, is the
KERNEL-50 shape and costs the kernel no premise.

**Reading it.** `nd meter [MEMBER]` (CLIENT, Rust: prints what follow's World holds; decides nothing) over a
new follow frame `meter`, answered from follow's OWN fold: `(ticks, refusals)` for the current window, and
the window's end height. No Host round trip, no trust: the member's follower re-derived every Turn that
moved it. A third-party form is the receipt: `Receipt.check` gains the `.ticks` key as a `refused`-arm
sibling (a `count` leaf at a `ticks` key under the refusals root), checked against a head the party holds —
own, attested (T1) or certified (T3). That is the "health receipt" of §1.5 and it is NOT built in this lane
(the own-fold read is; the path form waits for TRUST's `Head` so it is one object, not a fourth spelling).

### 1.4 The size ratchet as a law

Two ratchets wear one name. **The World's** is already a law: `fold_potential` (`145·weight + 84·allowance`
never rises) and `allowance_bounds_world` (KERNEL-55; READ `World.lean:838-850`), with `overAllowance` as
the refusal and a World allowance set at genesis. What it lacks is an OWNER (HOLISTIC-KERNEL §3.2(3)): one
allowance, any member can exhaust it, nothing retires. The meter design gives the owner half for free: a
second meter key `bytes member win ↦ count (Σ charge)` with `Bounds.bytesPerWindow` is the same leaf, the
same check, the same prune, and `charge` is ALREADY in the Turn and exact (`chargeMismatch`), so the kernel
computes it with no receive-layer trust at all. It is the second meter, not the first, because ticks has no
cousin and bytes has the allowance. **The tree's** ratchet (SIZE.md: modules, lines, theorems, Rust lines;
law 12) is about the Lean, which the World does not hold. It cannot be a World law and should not pretend
to; HOLISTIC-GATES §2a is right that a theorem-count ratchet punishes lemma-splitting, and TOPLEVEL-SPEC §12
already makes the trusted reading a file rather than a count. The honest bridge is axis 1: when packages
are installed objects with generators judged by the kernel, "a package's bytes" is a charge the signer
already pays (`install`'s `Turn.weight`), and a law `(bounded size max)` on a registry object is one surface
line. Until then the size ratchet stays a gate on the tree, and this memo does not move it.

### 1.5 The health receipt and the convergence verdict

**What a health receipt says.** For a window `win` of World `W`: the head `(origin, steps, height, roots,
chain)` (DESIGN-TRUST §1.2's one spelling), and under its refusals root: this member's `ticks`, `count`,
and the World's `total`; and under the World fields: `allowance`. That is the whole honest state of "is this
system healthy" as the World can know it: who is spending what this window, how many refusals, how much
storage is left. Everything else a human means by healthy — latency, disk, a stuck writer — is (C) and lives
where THE BAR and the Host's journal put it.

**Who signs it.** Nobody, for the member's own follower: `nd meter` reads the member's own fold, which is a
re-execution of the log, which is the measurement. For a party that holds no World: whoever TRUST's
authority says certifies a head — a member's attestation (T1, built by FABLE-TRUST) lets a second member of
`W` check it with keys it already holds; the writer's certificate (T3, blocked on the seed ruling) lets a
stranger. The meter adds nothing to that question and must not: a "health signer" would be a fourth
authority beside the three DESIGN-TRUST priced.

**The convergence verdict.** `scripts/converge` is about the TREE: it cannot be a receipt because the World
holds no tree. The World-side convergence that EXISTS is the writer's standing reopen every 4096 batches
(`reopenDiverged`, READ via TOPLEVEL-SPEC §5.FLOOR; HOST: "the one idea others should copy"): the writer
re-opens its own Store and refuses if the result differs. Today that verdict is a line in the writer's log
that no member sees. The right exposure is NOT a new step (steps are member-signed; a writer step would be
the first unsigned one, and A1 would gain a case): it is a clause in the writer's CERTIFICATE at T3 —
`reopenedAt : Nat` (the step at which the last standing reopen matched) — so a certified head carries "the
writer checked its own recovery path at step s". Until T3 it is an operator fact; this memo files it as
T3's one addition and builds nothing.

### 1.6 THE BAR as a law: what the kernel can know

The kernel can know, and already refuses by name: per Turn, every count in `checkBounds`; per run,
`treeTicksMax` (`overTicks`); per World, the allowance (`overAllowance`); per member per window, refusals
(`refusalBudget`), and after this design, ticks (`ticksBudget`) and bytes (the second meter). Those ARE the
inputs to every latency claim: a turn's cost on any box is a function of its ticks, its bytes, its trie
paths and the box. What the kernel cannot know: the box. THE BAR's limits stay in `gates/bar.tsv` as the
charter wrote them, judged per run with the load, never a ratchet (PERF-2). What moves INWARD from the bar:
nothing needs to, because PERF-2 already routed its counts through the waste rows; what the bar gains is a
fourth actor row it could not write before — a member that exhausts its ticks window is refused by name and
the row asserts the name (THE BAR's "forced contention" pattern, exact rows `=1`, READ `waste.py` header).

### 1.7 The price, in the spec's and the tree's terms

| item | expected (INFERRED until the build measures) |
|---|---|
| TOPLEVEL-SPEC top claims restated | none. §3 INTEGRITY gains one lemma-level fact, `fold_ticks_meter`: along an audited log, the meter at `(m, win)` is the sum of `ticks` of the window's Turns by `m`, and never exceeds `ticksPerWindow`. It is B2-shaped (a conservation-like kernel invariant of any Turn `admit` takes, forged ones included), not a new claim |
| hypotheses added to landed theorems | 0 (the meter is a new key kind in an existing trie; `refusalsCounted`'s clause for it is `true` — see the critique) |
| theorems restated by binder (Turn literals) | 26 construction sites in 18 files (MEASURED: `grep 'charge :='`), 14 destructurings (MEASURED), the codec's `turn` and its three theorems (`turn_lawfulOn`, `turnBytes_injective`, `turn_size_logWeight`), `Receive.sealTurn` |
| theorem families gaining a case | `refusalFits`/`refusalsFits`, `keptRefusal`, `refusalsCounted`, `RefusalLeaf.fits`, `refusalKeyBytes`, `refusals_bounded` (RefusalsBound), the refusals head read (`RefusalsHead`), `Refuse.lean`'s frame (`refuse_frame`: a refusal still writes no `ticks` leaf), Codec/World's listing refusal (`kernel/refusals`), Host/Proofs/Size (one leaf per invoking member per window: ≤ `windowMax` leaves, bounded by the turns-per-window argument) |
| refusal names | `rejectNames` + `ticksBudget` → `codeTable` changes → every pre-meter Store `shapeMismatch` (READ `Submit.lean:139-146`); `Reject.overBound .ticks` |
| waste | `admit trie-hashes-per-turn` (14.092) rises for invoke turns by one path; `Required` gains the meter insert; `submit bytes-per-turn` FALLS (both numerator and denominator gain 40 bytes); a `WASTE: admit: the meter leaf` line |
| re-genesis | every Store (`kernel!` flag day): the Turn record, the refusal code table |
| Rust | `client/src/generated.rs` re-emitted (`emit-rust`); `nd meter` is one verb (21/20 — the verb ceiling moves by one, or `meter` is a form of `whoami`: `nd whoami --meter`, which keeps 20/20 and is what this lane builds) |

### 1.8 The one way this is wrong, and the critique

**Wrong if** the meter is a second budget nobody owns either. A per-member cap with no way to RAISE it (a
grant of ticks, a purchase, a sponsor's allowance) is the refusal budget's shape, and the refusal budget is
tolerable only because honest members never approach 16 refusals. Sixteen full trees per window is the same
bet. If a row (the Bell's resident answering many rings, an agent-member of axis 3) approaches 2^21 ticks in
a window, this design must grow an OWNER: `Right.ticks (cap)` as a counted right carved from a founder's
World grant, spent per invoke like `enroll n` (READ `Call.lean:26-47`: the counted-right shape exists). That
is the honest next step if the plain cap bites, and it is cheaper than the cap was.

**Critique.** (1) `refusalsCounted` cannot validate a `ticks` leaf from the trie alone, because the Turns
are not in it; a decoded base with a forged meter passes the state check and is caught only by the trust the
base already needs (`CheckpointTrusted`, sponsor pin). KERNEL-50's property ("a function of its records")
holds for refusals and NOT for ticks. The alternative — a `ticks` field in each journal entry so the meter
is a tally of the journal — restates the journal leaf, its injectivity and every `JournalHead` theorem for a
check whose only reader is a base decode. Priced and declined; the docstring says so. (2) The member in the
Turn is 32 bytes on every record for a counter that only invokes need; the alternative (a member only on
invoke Turns, as an `Option`) makes a forged-log probe shape a wire shape. Declined; the receipt gains "who
signed" for every Turn, which B1 (authority confinement) wants anyway. (3) The cap is a taste number.

**Meta-critique.** I chose the refusals trie because KERNEL-44 built it and it is the one place the kernel
already measures itself; a reader who thinks the trie's name should change ("the window trie") is right and
that rename is not this lane's. I was briefed "ticks per window per member is the obvious one" and built that
one; the bytes meter is cheaper and more honest (the kernel computes `charge` itself) and I nearly built it
first — the reason not to is that bytes have a global budget today and ticks have none, so ticks is the hole.

---

## 2. TIME AND THE OUTSIDE

### 2.1 What nano's clock is (READ)

Height, and only height. `checkWindow`: `notBefore ≤ height + 1 ≤ validUntil` (READ `World.lean:955`);
`validUntil ≤ notBefore + windowMax` (`checkBounds`); `Req.notBefore/validUntil` so a law judges "not
before h" from the call alone (READ `Call.lean:318-330`); `(patience n)` in heights for an unanswered
activity row (READ `Surface.lean`); the journal forgets by height (`journalForgets`). The resident's ticks
and the loop's fuel are process counts, not time. Real seconds enter through one party: the writer, which
decides which height a signed call lands at inside its window (and whether), and that power is exactly the
one TOPLEVEL-SPEC §7 lists as the writer's ("choose the order … delay or withhold … decline forever"),
bounded by the window and charged nothing. So the system already has an oracle for ORDER, trusted for
liveness, with the window as its radius. Every other outside fact has to come in as a signed call.

### 2.2 Three places for the trust, priced, and the one way each is wrong

**(i) The oracle is a World (E5).** A fact is a call World A admitted; B holds A's head in a `Std.head`
object posted by a member of B who follows A (READ `Lang/StdHead.lean`, `Protocol/Foreign.lean`); a method
of B reads a `(receipt)` column keyed by that head object and the run shows `{height, turn, tx}` of the
committed call (READ `Lang/Rel.lean:184-209`); `foreign_receipt_sound` says: under `hr` (the held head is a
head of a fold of A), the call was admitted in A at that height, or the hash collides among listed inputs
(READ `Protocol/Proofs/Foreign.lean:72-110`). The TRUST MODEL is `hr`: today the poster's honesty
(PROTOCOL-42's thin-member trust); at T1, a member of A's attestation checkable by anyone with A's genesis
and keys; at T3, A's writer's certificate; at T4, 2f+1 of A's committee. **Price:** zero kernel, zero
Protocol: it is landed. **Wrong one way:** a receipt proves ADMISSION, never CONTENT. B's law sees the
height, the turn digest and the transaction id; it does not see what the call wrote. A "price" or a
"document hash" as a fact needs one of: a cell-inclusion receipt (a path under A's cells root — the kernel
has the lemma, `head_*_read`, the Receipt type has no cell path), or the fact ENCODED in what the receipt
does show. The prototype uses the latter honestly: the fact IS the height.

**(ii) The oracle is a member with a grant.** A fact object in B with a method `post` and a law that
requires `req.agent` to be the oracle member — or k of n members under `(law ℓ (quorum f k #hex…))`, which
the surface already lowers (READ `Surface.lean` header). **Price:** zero kernel, one package. **Wrong one
way:** the trust is a key list frozen in a package (rotation is a `law` call; revocation is `revoke` of the
poster's grant, fine), and nothing binds the post to an outside artifact: the committee attests to its own
agreement, which is Chainlink's model exactly and is honest about it. It is the right shape INSIDE an
oracle World — the oracle World's members are the committee — and the wrong shape across Worlds, where
(i) gives the consumer a receipt it can check without being a member of the oracle.

**(iii) The oracle is a cell kind with a provenance field.** `Cell.kind = kindFact`, slots
`{source, signature, payload}`, verified by the kernel at admission with a verifier for the source's key
scheme. **Price:** a kernel leaf kind, a verifier in `Env` or `Ctx` for foreign schemes, a `Lawful` premise
per scheme, a Codec tag. **Wrong one way:** it moves the trust model out of laws (where it is a package a
member can read) into the TCB (where it is a premise), to buy nothing (ii) does not already buy with a
member key — a TLSNotary or enclave attestation is just a signature a member relays, and the member is the
one who is accountable in the World. Refused.

**The pick.** (i) between Worlds, (ii) inside the oracle World, (iii) never. Stated as an instance of
DESIGN-TRUST §1.3's table: a FACT from A consumed in B is sound under the same three rows as a HEAD of A
held in B, because it is one — the fact's whole provenance is the head's. The "oracle problem" (what makes
a reported outside value trustworthy) is answered by saying who certifies A's history, and nano already has
that object in design; the oracle adds no fourth authority, no committee of its own, and no transport.

### 2.3 The prototype: a timelock on a foreign clock

`client/tests/fixtures/foreign/Timelock.ob` (CLIENT's fixture directory, beside `Accept.ob`; a demo of
"an escrow settles on an outside event", which the charter's escrow demonstration covers):

```lisp
(package
  (doc "A time-lock on a foreign clock: release only on a receipt, checked against the trusted head of
        World A, of a call A admitted at or past `deadline` (A's height). heads: the owner's trust anchors.")
  (state (rec (deadline nat) (released bool)))
  (rel heads (key (cell digest)) (val (rec)) (limit 16) (retract))
  (method trust (arg (rec (cell digest))) (edits 1) (done state (insert heads (record (cell arg.cell)) (record))))
  (method distrust (arg (rec (cell digest))) (edits 1) (done state (retract heads (record (cell arg.cell)))))
  (method release (reads (heads (range 1 1) (receipt))) (arg (rec (receipt bytes)))
    (case rows.heads.range.rows.r0 (none _ (refuse "untrusted"))
      (some h (if (<= state.deadline h.receipt.height)
                  (done (with state (released true)))
                  (refuse "early")))))
  (law timelock
    (on invoke m (if (== m (index release)) (all ((not old.released) "settled") (new.released "badPhase")) ok))
    (on (relaw write) (refuse "frozen"))))
```

The fact is `h.receipt.height`: the height at which A admitted the call the receipt names. The law makes
`release` once. What the member of B learns when `release` is admitted: a member of B posted a head of A
at `(height, roots, steps)`; the receipt's roots open that head; A's journal at those roots holds the call at
`height ≥ deadline` (P2); so A's writer ordered that call at or past `deadline` — "A's clock passed
`deadline`", with A's window as the radius and A's head authority as the trust. Rows:

* **TL0** (journey, `Lang/Journey/Head.lean` beside RC0–RC3; `lang-journey`): B installs the timelock with
  `deadline = wA.height` and trusts HA; `release` with A's receipt of its committed call (height
  `wA.height`): admitted; `released` reads back true. **TL1** `early`: the same with `deadline = wA.height +
  1`: refused by the program, by name. **TL2** `settled`: a second `release` after TL0: `lawDenied` (the law's
  `settled`). **TL3** `untrusted`: after `distrust`, refused.
* **X6** (`client/tests/foreign.rs`, two real Stores, the real `host`): the timelock created with
  `deadline` = the height of A's receipt + 1; `release` → `early`; A's founder writes once more; a fresh
  receipt of the SAME call at A's new head is `headMismatch` until B's head advances (as X2h); after the
  post, `release` → admitted, and `read` of the object shows `released`. The plant: the `<=` flipped to `<`
  makes TL0 `early` and the row RED by name.

**What is NOT claimed.** No second of wall time. A stalled A (a writer that stops, a poster who stops
posting) keeps the lock shut: the escrow's liveness is now the oracle World's and the poster's. The honest
remedy is the fallback every heartbeat oracle carries — a second arm `(or (<= (+ state.deadline slack)
req.notBefore) …)` on B's OWN height, which `Req.notBefore` already gives a law — and whether a given escrow
wants it is the row author's choice, named in the package's doc. The prototype does not add it, so that the
row shows the pure dependence.

### 2.4 Price and the flag day

None. No kernel, Codec, Protocol or Host byte moves; the fixture is a package text; `headPackageId` is
unchanged; the journey session `headSession` gains rows; `foreign.rs` gains one test function. Owners
crossed: LANG (`Lang/Journey/Head.lean`), CLIENT (`client/tests/`): one `lang:` landing with a CROSS-LAYER line.

### 2.5 The one way this is wrong

The timelock reads a height and calls it time. If a row ever needs a REAL timestamp (a contract that
settles at 17:00 UTC), the oracle World is a clock World whose writer admits one signed `tick` per second
from a member that reads a Roughtime server, and B's law reads that member's post through a CELL-inclusion
receipt — which does not exist (§2.2(i)). The next step for axis 5 is therefore the cell receipt: a path
under A's cells root in `Protocol/Receipt`, checked by `Receipt.check` against the same head, with
`head_cell_read`'s lemma behind it; it turns "A admitted a call" into "A's cell `c` holds `v` at this head",
which is the fact shape every other oracle (a price, a document hash) needs. One lane-week; no kernel.

---

## 3. What is built here, in order, and what each refuses

**Status (05:00Z):** item 1 LANDED (`fab2875`); item 2 BUILT to within two proof modules (`RefusalsCounted`'s
admission preservation, `admit_comm`'s meter premise), the whole diff in `METER-wip.patch`; see
`codex/FABLE-OBS.report.md` closing state for the exact obligations and the measured premise price (four, not zero).

1. **TL (axis 5), first, `lang:` fast landing.** The fixture, TL0–TL3, X6, the plant. Refuses: `early`,
   `settled`, `untrusted`, `headMismatch` by name.
2. **The meter (axis 4), `kernel!` full judge.** `Turn.member`, `Turn.ticks`, `RefusalSlot.ticks`,
   `Bounds.ticksPerWindow`, `Reject.ticksBudget`, `overBound .ticks`, `ticksUsed`, the check and the
   commit, `refusalFits`/`keptRefusal`/`refusalsCounted`/`RefusalLeaf.fits`, the codec and its three
   theorems, the 26 literal sites, `Required`'s meter path, the kernel-sim probe (a member's seventeenth
   full-budget tree in one window is `ticksBudget`; the sixteenth is not), the journey row (M0: after the
   escrow rows, the founder's meter reads back the ticks the rows spent, exact by `decide`), `nd whoami
   --meter`. Refuses: `ticksBudget MEMBER`, `overBound ticks`, `shapeMismatch` on every pre-meter Store.
3. **Next (not this lane):** the bytes meter (§1.4) as the second key kind; `Receipt.check`'s `ticks` arm
   once TRUST's `Head` lands; `reopenedAt` in T3's certificate (§1.5); the cell receipt (§2.5); the owner of
   the ticks budget (`Right.ticks`, §1.8) when a row bites the cap.

## 4. Literature, as used

- Gas as a kernel-maintained counter every node agrees on: Ethereum's yellow paper (Wood, 2014); the model
  for "a meter is a ledger invariant".
- Accountable logging where a fault is evidence: PeerReview (Haeberlen et al., SOSP 2007); here the meter
  and the refusal record are the evidence, re-derived.
- Self-certifying state: SUNDR and CT (DESIGN-TRUST §7) — a health receipt is a path under a signed head.
- Mutation-adequate oracles that prove they can fail (the gates): kept as is; HOLISTIC-GATES Part 3.
- Oracles: Chainlink (committee attestation, heartbeat/deviation updates: the fallback clause), Town Crier
  (Zhang et al., CCS 2016: enclave attestation as a relayed signature), TLSNotary (the same, for TLS), and
  the "oracle problem" literature's conclusion that the question is who you trust, not how bytes move.
- Signed time with a radius: Roughtime (Google; IETF draft): a midpoint and a radius, here height and window.
- Observability-as-state (the counters live in the replicated state, not in a side channel): the design
  choice in Sui's and Fabric's per-object version counters, which HOLISTIC-KERNEL §1.2(b) already named.

---

## 5. BUILT (FABLE-OBS-2, real 2026-10-26/27) — the meter as the second KIND of one typed window trie

**The question the brief put before landing.** The first build (§3 item 2, `METER-wip.patch`) put the meter in
`RefusalSlot` as a fourth constructor, and the build measured a premise price §1.7 had estimated at zero:
`admit_refusalAt` +1 hypothesis (`k ≠` the turn's meter key), `Frame.refusals` +1 premise, `Agree` +1 field,
`admit_comm` +2 (pending). Is there a shape where the meter key is excluded by the DEFINITION of the refusal
window — its domain — rather than by a hypothesis on its theorems?

**Answer: yes, and it is the law-1 shape.** The window trie's key type is typed by kind:

```lean
inductive RefusalSlot (D) | tx (id) | count (member) (win) | total (origin) (win)   -- UNCHANGED
inductive MeterSlot (D) | ticks (member : D) (win : UInt64)                          -- the meter's keys
inductive WindowSlot (D) | refusal (k : RefusalSlot D) | meter (k : MeterSlot D)     -- the trie's keys
abbrev Refusals D := Trie.T (WindowSlot D) (RefusalLeaf D) D
def refusalAt (E) (w) (k : RefusalSlot D) : Option (RefusalLeaf D) := w.refusals.get (refusalSpec E) (.refusal k)
def meterAt   (E) (w) (k : MeterSlot D)   : Option Nat := match w.refusals.get (refusalSpec E) (.meter k) with
  | some (.count n) => some n | _ => none
```

The wire is the first build's (kind byte 3, the `count` leaf, one key width). What changes is who can NAME what:
`refusalAt` cannot name a meter key, so `commitMeter_get_refusal : (commitMeter E w t).get (.refusal k) =
w.refusals.get (.refusal k)` holds by constructor disjointness with no hypothesis, and the two landed statements
(`admit_refusalAt`, `Frame.refusals`) are unchanged. The meter has its own kind's theorems, over its own domain:
`admit_meterAt` (every meter leaf but the turn's own — its member's in the window it lands in, which is in the
turn's footprint as its cells are; the exclusion is honest there), `admit_meterAt_self` (the turn's own leaf,
bumped by what it spent; the prune never drops it, since it is keyed by the window the prune keeps), and
`Frame.meter` as a NEW clause of the frame. Every `refusalAt`-reader in the tree (~130 lines, 16 files) is untouched.

**What is not removable, with the reason each is a theorem of the model, not undone work.**
- `Agree.meter` (+1 field): `Agree` IS `check`'s read set and `check` now reads the meter (`checkTicks`). The only
  shape that keeps `Agree`'s statement is not checking the meter — a no-op, which CLAUDE.md forbids keeping.
- `admit_comm`: `RefusalsCanon` → `RefusalsOk` (at a window boundary `(h+2) % windowMax = 0` the second turn's
  meter key is in a NEW window; that its leaf is absent needs every leaf to fit the current window, which is `Ok`,
  every reached World's), and `hmeter : t₁.member = t₂.member → 0 < t₁.ticks → 0 < t₂.ticks → ticksUsed E w
  t₁.member + t₁.ticks + t₂.ticks ≤ Bounds.ticksPerWindow`: two turns of ONE member that BOTH spend ticks commute
  only if together they fit the window — otherwise the second is `ticksBudget`, so the theorem is FALSE without
  it. Guarded so zero-ticks turns (every write, the two-rains tooth) owe nothing. No proof consumes `admit_comm`
  (MEASURED: doc comments only).
- `World.RefusalsOk` RESTATED over the trie's keys (`w.refusals.get (refusalSpec E) k = some l`, `k : WindowSlot`):
  through `refusalAt` it would no longer bound the meter leaf, and `refusals_bounded`/CODEC's `kernel/refusals`
  need it to.
- `Checked.ticks` (+1 field, the record of `check`'s clauses); `receiveWith_sealed`/`receive_of` gain the ticks binder
  (`derive` returns the Walk's pool) — the first build's, unchanged.

**The price table, as landed** (KERNEL-68 §Price holds the full one): hypotheses on landed theorems 0 for the
refusal window's theorems; `Agree` +1 field (intrinsic); `admit_comm` Canon→Ok and +1 guarded premise (no
consumer); `RefusalsOk` restated to cover both kinds. The rename of the family (`refusals` → `window`,
`refusalSpec` → `windowSpec`, `RefusalLeaf` → `WindowLeaf`) is a card (cv task 01a176d8-ffe9), not this landing:
a binder-only sed across ~16 proof files that collides with every live lane and has no theorem behind it.

**Deferrals, as cards** (cv task, repo nanodregg): the rename (01a176d8-ffe9); the meter's fold theorem — along an
audited log the meter at `(m, win)` is the sum of that window's Turns' ticks by `m`, which `refusalsCounted` cannot
state (01a176d9-0005); the ticks OWNER, `Right.ticks cap`, when a row bites the cap (01a176d9-0014); the bytes
meter as `MeterSlot.bytes` (01a176d9-0021).

**Landed.** (hash: see FABLE-OBS.report.md FABLE-OBS-2 lines.)

### 5.1 The next step: the health receipt, now that `Protocol.Head` is on main

TRUST's T1 landed (`5fa281d`): `Protocol/Head.lean` holds THE head object (`Head = {origin, steps, height,
roots, chain}`) and a member's `Attestation` of its own fold's head. `Receipt.build E w txId` already opens
four roots (`root, jroot, rroot, rowsroot`) against a head's `roots` digest (`rootsDigest`) and carries two
paths. A HEALTH RECEIPT is therefore the same object with a different subject: `{member, win, root, jroot,
rroot, rowsroot, answer : MeterAnswer (ticks n | absent), mpath : Trie.Proof (WindowSlot D) D}`, checked against
a `Head` by `rootsDigest … = head.roots`, `win = refusalWindow head.height` (a past window's leaf is pruned:
`forgotten`'s twin), and `Trie.verifyInclusion (refusalSpec E) rroot (.meter (.ticks m win)) (refusalDigest E
(.count n)) mpath` (or exclusion for `absent`); sound by `refusal_inclusion_sound`/`refusal_exclusion_sound`
(RefusalsHead, over `WindowSlot` keys after this landing) + `head_roots`: "at this head the World holds `n` ticks
for `m` this window, or a listed input collides". Its trust is the head's provenance — own fold, a T1
attestation, a T3 certificate — and nothing of its own (§1.5). The own-fold read `nd whoami --meter` answers
`(ticks, refusals, window end)` from follow's World (`meterAt`, `refusalCount`) with no signature: the fold is
the measurement. Both are one `protocol:` landing (CLIENT cross-layer for the verb), no kernel byte. THE BAR
gains the fourth actor row §1.6 names (a member exhausting its window refused `ticksBudget` by name, an exact
`=1` row). The size ratchet stays a gate on the tree (§1.4) — META's `install`-from-a-body (`c82f171`) makes a
package's bytes a charge the signer already pays, so a `(bounded size max)` law on a registry object is now a
surface line for LANG, not a kernel law; not this lane's.

### 5.2 BUILT (FABLE-OBS-3, real 2026-10-27): the health receipt

`Protocol.Health` as §5.1 drew it, with one simplification the build forced: the answer is three naturals
(`ticks`, `refusals`, `total`), not `ticks n | absent` — a zero counter is an exclusion path, a positive one an
inclusion of `count n` (the kernel's `refusalFits` forbids a zero leaf), decided by one `counted` predicate and
proved once (`counted_sound`). Windows come from the HEAD: ticks at `refusalWindow (height + 1)` (what `ticksUsed`
reads), refusals and total at `refusalWindow height` (what `refusalCount`/`refusalTotal` read). `check_sound`,
`check_build`; `nd receipt --health [MEMBER]` (`Cmd.receipt (ReceiptOf D)`); row `health`; the testground's meter
is the checked receipt (462 bytes at deployed parameters). KERNEL-71. Commit 65282e5b (see FABLE-OBS.report.md
OBS-3 for whether it is on main).

## 6. The bytes meter (FABLE-OBS-4, real 2026-10-27; KERNEL-78)

**What is counted.** A Turn's `charge`: what it pays for the storage it costs, exactly its `Turn.weight`
(`checkCharge` refuses anything else by `chargeMismatch`), which is its log record plus what it adds to the
World — born cells with their ids, written ops, spent nullifiers, row inserts and declares, package bytes
(an install's package is a born ROM cell). The kernel already computes it and already refuses a Turn that
states another, so the meter trusts nothing of the receive layer. It is GROSS: what a retirement, an
overwrite, an upsert or a retract gives back is credited to the World's allowance (KERNEL-19, KERNEL-70) and
is NOT subtracted from the meter. The meter is a rate limit on what a member WRITES per window, not a
statement of what it holds; a member that writes and retires the same kilobyte sixteen times has written
sixteen kilobytes. A recorded refusal is not counted: its record costs the World 82 wire bytes of window trie (`refusalEntryBytes`),
bounded per member by `refusalsPerWindow` already.

**Where.** A second meter key of the window trie, `MeterSlot.bytes member win ↦ count (Σ charge)`, kind
byte 4, beside KERNEL-68's `ticks` (kind 3): the same leaf, the same window, the same prune, the same
typed reader (`meterAt`), under the refusals root and therefore under every head's roots digest. Every
Turn writes it (every admitted Turn has a positive charge), so every Turn writes one more trie path than
before; an invoke writes two.

**The window rule.** As ticks: a Turn is charged to the window it LANDS in, `refusalWindow (height + 1)`
(`bytesUsed`, read by `checkBytes`); a refusal is recorded in the World's current window. The health
receipt reads both meters at `height + 1`, the refusal counters at `height` (KERNEL-71's asymmetry, now
with four counters).

**The bound is the World's.** `World.bytesBudget`, set at genesis (`host genesis --bytes-budget N`,
default `Host.Bounds.bytesBudgetDefault` = 8 MiB per member per window), committed in the origin (the
genesis input gains it after the allowance; a carry carries it and its input commits it), written by no
step (`step_bytesBudget`, `fold_bytesBudget`). `checkBytes`: `bytesUsed + charge ≤ bytesBudget`, else
`bytesBudget` naming the member, recorded like `ticksBudget`. Genesis and carry refuse a budget past
`Bounds.bytesPerWindowMax = windowMax · weightMax` (2^28) by name (`bytesBudgetTooLarge`): no member can
write more than that in a window anyway (one Turn lands per height, each at most `weightMax`), so a
larger budget bounds nothing. The leaf's own bound in `refusalFits` is that structural one —
`n ≤ (height % windowMax + 1) · weightMax` — so the invariant needs no budget and no extra check
(`refusalFits_succ`'s bytes arm, `bytesUsed_le`).

**What the third party checks.** The meter's leaf opens under the roots (the health receipt's fourth
path, `bpath`). The bound does not need a path: it is fixed for the World's life and committed in the
origin the head names, so a party holding the genesis input (every member does; it is what an invitation
carries) knows it. The receipt states the counter; `receipt --health` prints it beside the member's own
World's budget.

**Price.** Every Store re-geneses (World wire gains a u64; carried wire gains a u64; genesis input gains
a u64; the window trie gains a key kind; refusal codes gain `bytesBudget` at the end). Kernel
statements: `Checked` +1 field (`bytes`), `Agree` +2 (`bytes`, `bytesBudget`: `check` reads both),
`Frame` +1 (`bytes`, the bytes meter's frame clause), `admit_comm` +1 premise (`hbytes`: two Turns of one
member commute only if both charges fit its budget together — a theorem of the model), `CountedOk`'s
meter bound doubles, `refusals_length_le` +windowMax, `genesis_inj`/`carry_inj` conclude the budget's
equality too, `GenesisFits`/`CarryFits` +1 clause. The refusal window's theorems (`admit_refusalAt`,
`Frame.refusals`) are unchanged: the domain typing of FABLE-OBS-2 carried the second meter for free.
