# DESIGN-CAUSAL — causal pins: a call may name the head it was planned at, and the World can say whether that head is its own

Design memo, real 2026-10-27, by CAUSAL. Read against nano origin/main `57111733` (worktree `hbox:~/nd-land/causal`).
Inputs: DESIGN-TRUST whole (§2, §4, BUILT-1..8, §4.4c), CRIT-TRUST, PROTOCOL-82, DESIGN-CTX §1, §2, BUILT-7
(`Lang/Contextual/Slot.lean`, `slot_repair`), `Kernel/Receive/Call.lean` (`Unsigned`, `Req`, `checkPins`),
`Kernel/World.lean` (the World, the window trie, `checkWith`, `commitWith`), `Protocol/Command/Machine.lean`
(`planUnchecked`, `derivePins`, `absorbStep`), KERNEL-68 (the meter: the precedent for a Turn field and a window-trie
kind), KERNEL-69. Tags: READ (a path at that tip), MEASURED (a command run), INFERRED (attack these first).

## 0. The answer in one page

Ember's direction: build mechanisms, not a policy. The policy question "fork* or comparison only" (cv 01a17de0-1222)
assumed that one World-wide rule decides what a pin means. This memo separates the mechanisms, and then the
policies become values of them.

**The four mechanisms.**

1. **The pin (signer's choice, per call).** `Unsigned.causal : Option (CausalPin D)`, with `CausalPin = {steps, chain}`:
   the head of the signer's World when it planned the call. It is signed like every other pin, and the Turn
   records it (`Turn.causal`, re-derived from the event, as `member` and `ticks` are). A pin says: *this call is
   justified on the history that reached this head.* It is a third kind of pin beside the cell pins
   (`pins`, `rowPins`/`ranges`). It is a new kind and not a cell pin, because what it names is a position in
   the log, not a state of any cell. No cell holds the chain at step s.
2. **The World can judge a head (kernel).** The window trie (`World.refusals`, which already holds two
   kinds: the refusal window and the meter) gains a third kind, a ring of the last `Bounds.pinWindow` chain heads:
   key `chain (s mod K)`, leaf `(s, chain at s)`, written on every step (an admitted Turn or a recorded refusal) for
   the step it leaves. It is committed under the roots like the other two kinds. A World can then say of any
   `(s, c)` whether `c` is its own chain at `s`: **holds**, **forked** (`s` is within the ring and the chain
   there differs), **ahead** (`s > steps`) or **expired** (`s` is older than the ring).
3. **A present pin is always judged (kernel).** `World.admit` (and `submit`'s `checkPins`, before any receiver
   runs) refuses a Turn whose pin does not hold: `forkedPin s`, `pinAhead s`, `pinExpired s`, each by name and
   none recorded, like `stale`. No World can opt out of judging a pin a member signed. A World that ignored a
   signed assertion would weaken a check (CLAUDE.md pause item 2), and the field would be a no-op that its next
   reader trusts. The *policy* freedom is elsewhere: whether a pin is *required*, and what happens to calls when
   branches meet.
4. **Laws see it (LANG, landing 1b).** `Req.causal : Option (CausalPin D)`: an act's law reads the pin the call
   carried. Admission (3) guarantees that a pin that is present holds on this branch. So a law that requires a pin is the
   rule "this object moves only by calls justified on this branch". Library law `causal/strict`.

A fifth mechanism, **the fork object**, names two branches as World data. The kernel's job ends at naming the branches and
recording both logs, and a convergence law reconciles them. It is landing 2 (§2.3).

**The three policies, as values of the mechanisms.**

| policy | what is set | what admit does |
|---|---|---|
| `causal/none` (default) | no law requires a pin; `nd` pins every call by default; `--float` omits it | judges every present pin (3); admits unpinned calls as today |
| `causal/strict` | a library law in an object's laws (or every object of a package): `req.causal ≠ none` | the object refuses unpinned acts (`lawDenied … unpinnedCall`); pinned ones are judged by (3) |
| `causal/tolerant` (landing 2) | a fork object and its convergence law | floated calls may survive a reconciliation onto the chosen branch; pinned calls on a losing branch are withdrawn by name `forkedPin` and re-planned |

This corrects the brief in one place, and says so: in the brief, `causal/none` was "carried and recorded but not judged".
Here the pin is always judged. *None* means *not required*. A member who wants comparison only floats its call. The
per-payload choice (pin or float) is the flexibility Ember asked for: "allowing the payload to be causally pinned" while
"use cases that allow for forks" float theirs.

## 1. The guarantee, precisely (what the build proves)

- **K-a `admit_pin_holds`.** If `World.admit E w t = .ok w'` and `t.causal = some p`, then `p.chain` is `w`'s
  chain at `p.steps` (it is `w.chain` at `w.steps`, or the ring's leaf at `p.steps`).
- **K-b `fold_ring_chain` (the ring tells the truth).** For every World `w` that `World.fold E g l` reaches, a ring
  leaf `(s, c)` holds `c` only if a prefix of `l` folds from `g` to a World at `steps = s` whose `chain = c`.
- **K-c `pinned_no_join` (SUNDR's no-join, for pinned calls).** Let two folds from one `g` both admit a Turn whose
  pin is `(s, c)`. Then their prefixes up to step `s` are one log, or two of the listed inputs collide
  (`fold_head_binds` at the prefix). A pinned call is never shared by two histories that disagree before its pin.
- **P-a `plan_pins_own_head` (consent).** A call `plan` asks custody to sign carries `causal = some (headOf w)`
  for follow's own World `w`, or `none` exactly under `--float`.
- **P-b "a member's admitted calls form a chain".** Suppose member m plans each call at a head whose
  prefix holds m's previous call: m syncs past its own last call before the next one, which `nd` does after every
  `submit` that settles. Then every log, on any branch, that admits m's k-th call holds m's whole history up to its
  pin, and that history includes calls 1..k-1 in m's order. A writer can show m's calls on two branches only up to
  the fork point. Calls pinned at a head before the fork may be joined, and at most one per member when the member is
  sequential: that is fork*. A member that pipelines n calls at one head admits up to n joins.

**What each policy gives a member against a malicious writer** (the writer orders, serves pages and may fork).

- *Floated call (today's behaviour).* Nothing at the operation level: CRIT-TRUST's construction applies (the
  writer may admit it on every branch where its cell pins agree).
- *Pinned call.* No-join for that call, enforced by every auditor that re-executes: members, thin joiners above
  their base, the certify decider. A writer that forks M1 | M2 after M1's head cannot place M1's later pinned
  calls on M2's branch. M2's follow re-runs `admit`, gets `forkedPin s`, and refuses the page by name: the fork
  shows at the first relay. **Not given:** detection when the writer *withholds* (censorship stays silent,
  as in SUNDR; T1/T2 comparisons remain the answer); protection for a pin older than the fork point; protection
  past the ring (`pinExpired` is a refusal, never an admission, so "unchecked" is never "accepted").
- *`causal/strict` object.* Every act on the object is pinned, so the object's history is fork*-consistent for every
  writer of it, not only for those who chose to pin.
- *`causal/tolerant`.* A fork is an object members can read, and each member's view of it reconciles by one
  deterministic law. That is detection plus a named outcome. Integrity does not go further than the law's own theorem.

## 2. The contextual reading (one theory with the trust axis)

A causal pin is a SUPPORT in exactly `Lang/Contextual/Slot.lean`'s sense. The slot is the member's pending call:
candidates are the re-plannings of one intention (one per head), `supports c = c.unsigned.causal.toList`, the
judge is follow's own `plan`. The view is a log, and `holdsAt l (s, c)` says that `l` reaches chain `c` at step
`s`. **Permanence holds** for `forked`: along a fold the chain at a passed step never changes, so a pin that is
dead on a branch is dead at every later World of that branch. This is `Permanent holdsAt (· <+: ·)`, where
"later" is log extension. `slot_repair` instantiated (`causal_slot_repair`, Protocol) says:

1. a pending call is usable on a branch iff its pin holds there;
2. a refused call is withdrawn by the name of its dead support (`forkedPin s`, with s the coordinate);
3. once forked, it stays withdrawn on that branch at every later head;
4. re-planning at the branch's head is usable at once.

That is the member's repair loop: `forkedPin` → withdraw → sync → re-plan. `pinAhead` is *not* permanent (the branch
may grow to `s` again after a writer's rollback, with the same chain), and `pinExpired` is permanent but is not a
fork. Both read as "blocked" with their own names, never as forks. So the trust axis (a fork is a dead support)
and the contextual axis (a withdrawn assumption retracts by name, de Kleer) are one statement here.

### 2.3 Landing 2, designed: the fork object and convergence

- **Object.** `Std.fork`: a data object of a library package whose state is two heads `(s, a)`, `(s', b)` and their
  common step `k`, with relations `left`/`right` holding each branch's events after `k`. It is born by a member's (or
  the writer's) call carrying the two heads' evidence: two attestations (PROTOCOL-74) or two certificates
  (`certified_equivocation`). Its law checks the evidence (the attestation check is a pure Protocol function. It
  runs in LANG as a method guard over bytes; INFERRED: needs `Ed25519.verify` as a LANG builtin, which exists for
  the hosting decider but not in the language. Price: one builtin.) The kernel names nothing new. The fork is
  World data, as the brief asks: "the kernel's job ends at naming the branches and recording both logs".
- **Convergence law.** A relaw/adopt-style act `converge` on the fork object, judged by the law the World
  installed for it: a pure function `(prefix, left events, right events) → surviving events` over decoded calls.
  The library provides two policies. `lastWriterByChain` keeps the branch whose head chain digest is smaller,
  whole: deterministic, and it converges trivially, since it is a function of the fork object. `ownerWins`
  keeps, per object, the events signed by that object's owner, or by grants reaching the owner, from either branch.
  Its convergence theorem: the result is independent of the order of the two branches (commutativity of the
  selection), and re-running `converge` on its output is the identity. The output is then **re-submitted**. Floated
  calls go in as they are. Pinned calls from the losing side are refused `forkedPin`, and their signers re-plan
  them (§2). CRDT merges are a member program over the fork object as data.
- **Price (INFERRED).** One Std package and its two laws (`lang:`), a builtin (`lang!` if it changes the
  builtin table), a row with two lawful divergent histories, two calls of one member relayed across them
  (CRIT-TRUST's validation list), and a converge. No kernel change. Two lane-days.

## 3. What it costs, and what re-geneses

| piece | shape changed | re-emits / re-geneses | refuses by name |
|---|---|---|---|
| pin in `Unsigned` | one optional field (1 + 8 + 32 bytes when present), last in the signed bytes | the call wire: every client's calls; `codec-vectors` | an old client's call: `badCall` on decode (fixed shape, no reinterpretation) |
| pin in `Turn` | one optional field | every log record; every Store re-geneses | an old Store: `shapeMismatch` at open |
| the ring | a third window-trie kind; `pinWindow` leaves, 41-byte keys and 42-byte leaves | every World's roots; every Store re-geneses | a decoded base whose ring is not one (`refusalsFits`): refused |
| admission | three Reject constructors, `checkPins` + `checkWith` gain the pin | the refusal name table; `hintNames` | — |
| `Req.causal` (1b) | the request type every law and method sees | every shipped package text (K1's price, MEASURED there: all re-emitted) | an old package at install: method-type check, by name |

Per-step price: one window-trie insert, on every step, including in Worlds where nobody pins. Ring memory: K leaves.
At K = 128 that is about 11 KB of World state (INFERRED from the leaf shape; MEASURED at the build). K is a Bound,
and the honest member pins its follow's head, which is normally within a few steps of the writer. `pinExpired` is
the visible cost of a slow member, and its repair is to sync and re-plan.

## 4. The one way this is wrong

**The grain.** A head pin pins the *whole* prefix. Two branches that differ only in an object the call never read
refuse the call (`forkedPin`). That is exactly CRIT-TRUST's construction, now refused. For fork* of a member's
*view* that is right. For *convergence* it is too strong: a merge wants calls to survive on any branch where what
they *read* agrees, and that is the grain of the cell pins, not of the head. If tolerant Worlds turn out to be the main use, the right
pin is per-object causality (Depot's per-writer version vectors, which nano's cell pins already approximate), and
the head pin is useful only for the view-consistency claim. What would show it: a tolerant row whose convergence
re-submits pinned calls and wants them admitted where their read sets agree, so that the row author floats every call
to get the merge, and pins nothing. If floating becomes the default in such rows, the head pin was the wrong
default, and `nd` should pin the head only when it is asked to.

---

## BUILT — appended per landing
