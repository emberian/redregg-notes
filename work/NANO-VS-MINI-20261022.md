# NANO-VS-MINI-20261022: where the repair-capable, contextual, open, multi-party system can be BUILT with meaningful theorems

Scout (Claude, read-only architect; wrote only this file). Ember, today: "how does this compare to mini? maybe nano is
too limited and we need to go visit the minidregg metatheory to really express this stuff. Or maybe we can upgrade
nano … previously nano avoided 'distribution' in favor of single-node things, clearly our present focus is bigger
than that old restriction; we either need to elevate nano or start working on mini probably right??"

"This stuff" = REORIENTATION-20261022.md Parts A–C (cited REOR) and LITERATURE-PROTOCOLS-20261022.md Parts A–C (cited
LITP). The prior comparison NANO-VS-MINI-20261017.md (cited NVM-17) is about scope and product; this memo is about
where the two memos' PROGRAMS can be stated over a deployed object.

Trees measured (nothing built, no Lean run, neither repository edited):
- **nano** `origin/main` = **f8d04ac** (fetched into `~/dev/nanodregg`, read by `git show origin/main:<path>`; hbox
  `/tank/dregg-build/nanodregg/main` is at the same f8d04ac, MEASURED by `git log -1` over ssh).
- **mini** `~/dev/minidregg` HEAD = **334316df** (2026-10-17). hbox `pipeline/warm-base/src` `github/main` is the same
  334316df dated 2026-10-17 (MEASURED): mini main has not moved for five days.
- **CX-MINI-COLL** at hbox `/tank/dregg-build/claude-lanes/cx-mini-coll/` (`LANE-ORIGIN.txt`, `logs/…ready-readme.txt`,
  `SERIES.tsv`, the final gate log).
- Memory: `project-2026-10-16-nanodregg-rebuild.md`, `project-no-proof-system-in-mini-admission.md` (verified at source
  below; one path in it is wrong).

Tags: **READ (path:line)** I opened it. **MEASURED** a command I ran (`git grep`, `wc`, an import walk). **RECORD** taken
from a decision file or memo whose author read it; I did not re-open the source. **INFERRED** my reasoning: attack these.

---------------------------------------------------------------------------------------------------------------------

## THE ANSWER IN ONE PARAGRAPH

Neither memo's program needs multi-node agreement. Every card in REOR C1–C9 and LITP PROT-1..8 is stated over ONE
World with ONE writer. That includes the Bell across two members, fuse between two cells, support pins, repair and the
live bridge. What those cards need that nano lacks is three things, none of them "distribution" in the charter's sense:
(1) a Lang-side read of ANOTHER object's kernel state inside one Turn (the `look` that REOR C1 and LITP PROT-6 both
need); (2) a model of the **member socket**, the multi-PROCESS leg (resident ⇄ `nd --stdio` ⇄ follower ⇄ writer) that
LITP names as its one unmodelled object; (3) joint laws across two objects in one Turn, which KERNEL-45 already deferred
with a trigger that PROT-6 fires. All three are single-node work, and their premise price on nano's landed theorems is
zero or a binder, not a hypothesis.

Mini's metatheory does not have what the memos are about. It has no contextual holes, no substitutions, no TMS, no
provenance and no repair (MEASURED: grep). Its distribution assets are an in-progress BFT engine (safety over the
executable step, liveness not a theorem, membership change only stated), quorum/finality/CRDT theory that is **outside
the deployed Host closure**, and rooms. Its theorems sit on a kernel World that the writer does not run: `World.admit` has
no caller on the native host's path. Its main still carries the vacuous `∨ Collision` class, and the fix sits unlanded
behind a known-red umbrella. Mini's real contributions are SPECS to restate: Zoe invitations and offer safety for
PROT-6, and Core4's persisted activity checkpoints and interaction trees for PROT-1/3.

**Elevate nano, narrowly. Do not move the program to mini. Do not bridge the kernels.** Amend the charter's scope item 3
so it separates "many parties and processes over one writer" (in scope; the programs need it) from "many writers"
(still out, and nothing in either memo needs it). Part E gives the refuters.

---------------------------------------------------------------------------------------------------------------------

## SIZES (MEASURED)

| | nano f8d04ac | mini 334316df |
|---|---|---|
| Lean lines | Kernel 36,207 · Lang 41,549 · Host 18,001 · Codec 13,750 · Protocol 11,724 · Hosting 9,761 · Ledger 2,905 (SIZE.md, generated) | 598,409 total; Kernel 211,260 (566 files) · Compiler 105,468 · Theory 86,653 · Selvage 78,130 · Assurance 59,841 · Host 38,955 |
| theorems | 6,057 (SIZE.md) | 18,334 `theorem` lines (git grep) |
| `sorry` / `#guard` | 0 / **0** | 0 (simple pattern) / **4,258 `#guard` lines in 519 files** |
| deployed Host closure | 89 modules, ceiling 150 (SIZE.md) | 788 modules (CX-MINI-COLL final checks: "the Host closure equals the pin (788 modules)") |
| statement census | `Census/Statements.lean:1`: elaborated theorem types inspected for an outer `Or` and an unbounded `Collision` | ObjectiveManifest: 610 tsv / 42,711 lines (41,610 rows per the lane's pin log). Pins statements; no outer-Or check on main |
| main moving? | yes (S12 of the fold today) | no; `github/main` is 334316df of 2026-10-17. Ember's 10-17 call: "minidregg = finish-only … it stays the spec" (RECORD, rebuild memory) |

---------------------------------------------------------------------------------------------------------------------

## PART A — CAPABILITY BY CAPABILITY

Columns: the object; the theorem; whether that theorem is about what the **writer runs** ("gates": the decision the
Host commits is the theorem's object). In both trees no *cryptographic* proof gates admission, so "gates" here always
means "Lean's decision, with a theorem over that decision".

| capability | nano: object · theorem · gates? | mini: object · theorem · gates? |
|---|---|---|
| **cells, pins, use-once rights** | `Entry.live cell ver \| tomb` (`Kernel/World.lean:46`), a pin names a monotone VERSION (KERNEL-54); `stale_behind_forever` (`Kernel/Proofs/Versions.lean:240`, `CollidesAmong` over two named preimages); counted value rights in the grant (KERNEL-60, RECORD); `admit_value` (`Kernel/Proofs/Value.lean:402`). **Gates**: `World.admit` IS the receive path (`Kernel/World.lean:1-5`, CHARTER law 1). | `Turn.pins : List (CellId × D)`, a pin names a cell DIGEST (`Kernel/World.lean:386-392`), `pinCheck` (`:534`); nullifiers in the system cell (`:1-20`). **Does not gate the writer**: `World.admit` (`:647`) has no caller in `Kernel/NativeHost*`, `Kernel/Durable*` or `Host/*` except the exporter/follower `Host/TurnLogFollower.lean` header ("derive the Turn … admit it (`World.admit`)") (MEASURED grep). The writer runs `DurableReceiver`/`NativeHost` receivers (`Kernel/NativeHost.lean:1-8`). |
| **contextual holes in deployed code** | `Term.hole n σ`; `HoleROM`/`HoleCode.supports : List HolePin` (`Lang/HoleROM.lean:7-18`; a pin is `{rel, key, ver}`, a row under SELF only); `selectHole`/`instantiateHoles` (REOR B.2, READ-REOR). **Gates** (deployed Lang). Theory (`Lang/Proofs/Contextual/*`, 322 theorem lines) has **no deployed importer** (MEASURED: no `import Lang.Contextual…` under Host/Kernel/Hosting/Protocol/Ledger). | **Absent.** Core4 is "lazy open recursion over first-class, partial, composable specifications" (`docs/OBJECTIVE-BEND.md:3-8`); "open" there means extensible objects (`mix`/`fix`), not metavariables. No `hole`/contextual/metavariable object in Theory/Kernel (MEASURED: two incidental comment hits). |
| **repair at runtime** | `receive_congr` (`Kernel/Proofs/Receive.lean:38`), `audit`/`rederive` (`Kernel/Proofs/Audit.lean:205, :275`), `instantiateHoles` re-check; the P8 withdrawal gap is OPEN (REOR C1: support liveness read from a self-row copy). **Gates**: yes for audit; the repair theory is not yet a consumer. | No TMS, provenance or repair object (MEASURED: `provenance` hits are only in `Theory/Bfv*`). Re-execution of runs: `checkRun_sound`, `no_accepted_of_output_mismatch` (`Kernel/Run.lean:316, :383`). |
| **provenance over supports** | `label_iff`, `provenance_iff` (abstract, Lang theory; REOR A.13); source provenance in the deployed hole only. Not gating. | Absent. |
| **multi-party protocols between cells** | `Std.activity` (`Lang/StdActivity.lean`): start → captured `waits` row → resume by a designated resumer; teeth in `Lang/Proofs/StdActivityTeeth.lean` (RECORD LITP C.0). The Bell is its instance. One-party `Prot` calculus (LITP A.1). **Gates** for the activity rows (kernel guard). | Core4 `perform plan`/`done` (`docs/OBJECTIVE-BEND.md` term table); `Kernel/ObjectiveActivity.lean` header: "a Core4 activity persisted between turns … the exact machine checkpoint … a mandatory deadline height"; reference semantics as interaction trees with `spin` (`Theory/ObjectiveBendInteraction.lean` header). **Zoe**: `Kernel/Invitation.lean` ("the exclusive, assayable right to play one role of one contract instance"), `Kernel/Seat.lean` offer safety `seat_offer_safe_forever` (`:1651`) over Seat's OWN `World {book, registry, seats}` (`:769`) and `step` (`:925`), lifted per decided turn by `Kernel/SeatStore.lean` ("`Decided.inv`"). All in the Host closure (MEASURED import walk). |
| **between HOSTS** | None. `wrongWorld` is receive's FIRST check; "A joint turn across Worlds is agreement machinery, and nano has one writer per Store by charter" (`decisions/kernel.md:1909`, KERNEL-45 item 4). Receipts against a member's head exist (PROTOCOL-45; `Protocol/Proofs/Receipt.lean:27–235`). | Generic Simplex engine (`Kernel/GenericSimplex*.lean`, 35 files, 7,282 lines; MEASURED). "The four-logical-node native harness passes with actual TCP, ML-DSA … The actual workdesk fixture has not run" (`docs/GENERIC-SIMPLEX-NATIVE.md:3-8`). Live mesh: "Nothing here has been run against the live mesh"; call 00f711 abandoned (`docs/agreement/CUTOVER.md:3-5, :27-31`). `JointReceiver`, `JointControlCell`: cross-source joins (headers). |
| **membership / join** | Enrolment, revoke, rotate as Turns (`Kernel/Receive/Derive.lean:86, :97, :325`); follow gated by `mayFollow` (`Kernel/Receive/Follow.lean` header, PROTOCOL-3). Signed invitation: `Invite.accept` refuses `badInvitation \| notSponsor \| pinMismatch`, then `Receive.genesis` (`decisions/protocol.md:1091-1167`); carried starts pin the origin (PROTOCOL-61, `:1928-2005`); the real two-workspace join over sockets (`client/tests/join.rs:112`). **Gates.** | Seats + invitations (above); `NativeCurrentMemberKey`; `docs/SEATS.md` (not read). For a COMMITTEE: fixed `n = 3f+1`; "Changing membership, mobile faults and perpetual storage compaction are separate work" (`docs/GENERIC-SIMPLEX-NATIVE.md:10-13`); `Kernel/GenericSimplexReconfig.lean:1-25` STATES four rules; `EpochChain` "(STATED)". Not in the Host closure (MEASURED). |
| **crash / omission across Turns** | Resident: `Runs` over EVERY reply, including `Except String Reply` failures and every `AskEnd` (`Hosting/Proofs/ResidentRun.lean:1-37, :51`); `tick_order :273`, `tick_counts :410`, `interp_runs :700`; keep/forget durable under the volume contract (HOSTING-37/39, RECORD). Writer: replay recognition (`Kernel/Receive/Submit.lean:1-7`); settlement only from the member's own receipt (`settle_final_never_admits`, `Protocol/Proofs/Settle.lean:201`). Follower readiness before binding the member socket is a Rust ordering plant, "no theorem added" (`decisions/hosting.md:2270-2276`, HOSTING-41). | `Kernel/DurableCommitProtocol.lean` header: crash before or after the atomic install, retry explicit; "a verified protocol model, not a proof about a particular database … the required implementation-refinement premise as a proof-relevant simulation relation". In the Host closure. |
| **agreement / consensus** | None, by ruling (CHARTER.md:16, :32-33). | Engine safety over the executable step: `actual_committed_prefix_consistency`, `actual_certified_next_record_unique`, `honest_execution_faithful` (`Kernel/GenericSimplexEngineSafety.lean:62, :84, :99`); "Liveness is NOT a theorem here" (GENERIC-SIMPLEX-NATIVE.md). Quorum-finality model + decider `ReplicatedSettlementFinality`/`FinalityGate`/`FinalityLiveness`: **NOT in the Host closure** (MEASURED). `Kernel/GenericSimplexQuorum.lean`: one `honest_intersection` theorem. The engine IS in the closure (`Host/Main.lean:97, :343-360` `JointConsensusSettings`, optional). |
| **world-root merge** | None. One root per World (cells trie root in every chain link, KERNEL-23, RECORD); `admit_comm` (`Kernel/Proofs/RowsComm.lean:791`) commutes two Turns at one World; it does not merge divergent sequences. | `Theory/LaceMerge.lean` (CRDT laws over content-address keysets, `merge_converges`): **not in the Host closure**. `Kernel/WorldRoot.lean` is a root, not a merge; its binding premise `RootBinding` (`:356`) is, per CX-MINI-COLL patch 0005, "impossible global separation" on main. |
| **rooms** | None (MEASURED: no `room` object in Kernel/Lang). | `World.parent` rows in the system cell (`Kernel/World.lean:285-287`); `Theory/RoomAuthorization.lean` (`under R`, `room_confidentiality`), `Kernel/RoomKick.lean`, `RoomBirthGate`, private-room keys. In the closure. |
| **proofs that gate admission** | Charter: "Nothing. Admission is re-execution; the proof slot stays empty" (CHARTER.md:26-28). | `.witnessed _ => (cst 0, [])  -- first-party fail-closed: the indicator is constant 0` (`Compiler/PredCompile.lean:602-603`, doc `:18`); the constructor `witnessed (vk : Vk)` (`Pred/Core.lean:193`). **Same as nano.** |
| **a judge that reds** | Standing verdict fail-closed (GATES-15: every verdict exe carries a known-red control, RECORD); `scripts/commit` fast path + convergence (GATES-22, RECORD); first whole-tree GREEN 10-17 (RECORD). | `known-red-verdict` rule; main's umbrella is RED on `Fixtures.NativeAcceptedFixture` (cv 01a146dd), accepted as a known-red row; CX-MINI-COLL: "This is NOT literal umbrella PASS and does NOT authorize landing … ROOT reserved any proposed landing-gate change to Ember" (ready-readme). Red is the steady state. |
| **a census of statements** | `Census/Statements.lean` (outer Or + unbounded `Collision`, mechanised); `Census/Axioms.lean` the one axiom census (CHARTER law 6); the disjunct check written into every vacuity read (`decisions/protocol.md:1966-1975`, PROTOCOL-61). | ObjectiveManifest pins 41,610 rows; `proof-hygiene` and `guard-discipline` ratchets PASS (lane log). On main, `Theory/AuthTrie.lean:81` `def Collision : Prop := ∃ a b : NodeIn K V D, a ≠ b ∧ dig a = dig b` and `:135` `Reports t es ∨ Collision dig`: the unbounded disjunct that pigeonhole makes provable, 23 `∨ Collision` hits (MEASURED). |

### A.1 What the table says (INFERRED)

1. On the memos' axis (holes, supports, repair, provenance, protocols over the receiver), nano has the deployed objects
   and mini has none. Mini's "open" means open recursion, which is a different idea.
2. On the distribution axis, mini has more MATERIAL: an engine, rooms, Zoe seats, persisted activity checkpoints and a
   crash protocol model. Most of the theorems that make that material mean something (quorum finality, liveness,
   LaceMerge, revocation consensus, reconfiguration) are outside the deployed closure or only STATED.
3. "Proofs do not gate admission in mini" is true, and **it is equally true of nano**. It does not tell the two apart.
   What does is whether the theorem's object is what the writer commits. In nano it is, by law 1. In mini the clean
   kernel (`Kernel/World.lean`, DATAMODEL) is a follower-side re-derivation beside the writer's DurableReceiver path,
   which is the "two state machines" defect NVM-17 named.

---------------------------------------------------------------------------------------------------------------------

## PART B — THE DISTRIBUTION NANO ALREADY HAS, WHAT IT REFUSED, AND WHAT ELEVATING IT MEANS

### B.1 What nano already has (READ)

nano is single-WRITER, not single-party or single-process:
- **Members over sockets.** Each member is its own process with its own Store. A follower re-derives every Turn
  (`audit_ok`: a log is accepted iff it folds AND every step is what its signed event re-derives,
  `Kernel/Proofs/Audit.lean:275`; PROTOCOL-4, `decisions/protocol.md:93-110`).
- **Invitations and sponsors.** A joiner derives its genesis World from inputs a trusted sponsor key signed
  (`decisions/protocol.md:1091-1110`). `join_genesis_iff` gives refuse-before-write. Carried Worlds now arrive under a
  sponsor-signed origin (PROTOCOL-61 `:1928`). The deployed two-workspace join refuses a forged invitation (`pinMismatch`)
  and a wrong key (`notSponsor`) and serves a write (`client/tests/join.rs:112-190`).
- **Followers and segments.** Atomic adoption picks a fresh segment generation, and readers never mix histories
  (HOST-71, `decisions/host.md:3244-3290`). Checkpoint trust is bound to the recorded origin (`CheckpointTrusted`,
  `Host/Proofs/Trusted.lean:76`; `writer_life_trusted :269`).
- **Residents.** A resident is a member whose program is a `Prog` tree. `tick` performs exactly one path (`interp_runs`),
  and the theorems hold over every reply the member socket and the broker could give (`ResidentRun.lean:1-8`). The member
  socket waits for the follower's command loop before it binds (HOSTING-41).
- **Many parties in one World.** Several members, grants, an escrow with at most one payout over a history of admitted
  Turns (LEDGER-15, RECORD), and the Bell's queue with two founders' rings landing over one view (RECORD).

### B.2 What it refused, in its own words (READ)

- CHARTER.md:16-33: "nano has nothing to do with proof systems, host-hiding, or multi-node agreement … One writer per
  Store; followers re-derive every Turn … There is no agreement mesh, no second writer, no replication of the writer."
  The reason: "an agreement mesh with one host" was a measured failure of the tree before it (`:38-40`).
- KERNEL-45 (`decisions/kernel.md:1888-1913`): "A Turn is the hyperedge for ONE signer". Multi-signer atomic Turns are
  DEFERRED, triggered by "two members must exchange value in one turn". **Joint laws across objects** are DEFERRED,
  triggered by "the first row whose invariant spans two objects changed in one turn". Cross-World joint Turns are
  DEFERRED behind "a second writer for one World". The KERNEL-45 critique: "Nothing in the gates notices 'two members
  needed one turn'".

### B.3 Does the refusal still make sense for Ember's present focus? Card by card (INFERRED unless tagged)

| card | what it touches | writers | what nano lacks for it |
|---|---|---|---|
| **The Bell across two members** (LITP PROT-3) | ringer member, bell object, resident member (its own socket + follower), broker (a host process) | ONE World, one writer | the **member-socket model**: the join of the resident's `cmd` trace to the writer's admitted history. ACT-D §4.4: "would need the member-socket model, which no proof has" (READ `ACTIVITIES-DESIGN-20261022.md:408-411`) |
| **Fuse between two cells** (PROT-6) | two offer rows under two objects, one fusing call | ONE World | a guard that reads the OTHER object's row (a method reads rows under self only: REOR C1, ACT-D §9); the KERNEL-45 joint-law trigger fires (an invariant over two objects changed in one Turn). Multi-signer is NOT needed if each offer is posted in its owner's own earlier Turn and the fuse consumes both (LITP D.3) |
| **Support pins** (REOR C1) | a hole object and a grant cell | ONE World | `look` in `selectHole`/`instantiateHoles` and `SupportPin.cell`; today `HolePin` is `{rel, key, ver}` under self (`Lang/HoleROM.lean:7-11`) |
| **Repair** (REOR C5) | `resolveHole` across a multi-edit `Change` | ONE World | C1's World plus a multi-edit statement |
| **The live bridge** (REOR C2) | `selectHole` ↔ `judge` | ONE World | C1's `kernelWorld` |
| **Crash / omission** (PROT-5) | `submit` replay; resident `AskEnd.lost` | ONE World + host processes | nothing new in the kernel; roles + reliability as a parameter (PROT-2) |
| **Between HOSTS** | two operators | TWO Worlds | not demanded by any card in either memo (LITP D.2: "there is no message in flight between two CELLS") |

So the refusal that matters is not "multi-node agreement". It is the narrower habit of stating the resident's side
(every reply) and the kernel's side (every admitted history) separately and never joining them. Ember's "bigger focus"
is multi-PARTY and multi-PROCESS. The charter already permits both; it never built the model that joins them.

### B.4 What ELEVATING nano means: the objects, their premise price, the order

PRICE PREMISES rule: for each object, which LANDED theorem gains a hypothesis. A new theorem's own hypotheses are not a
price.

**E1. `look` in Lang: a pinned read of another object's kernel state inside a method's judgment.**
- Shape: REOR B.1's `SupportPin.cell id` plus the threading of `look : Pinned D`, which is already in scope at
  `Lang/Program.lean:210` (READ-REOR). PROT-6's compliance guard is the SAME read: a pinned read of a second object's
  offer row.
- Price (READ-REOR B.1): kernel **zero**, because `receive_congr` already quantifies over `c.unsigned.pins`. Lang: eight
  `Lang/Proofs/LiveHoles.lean` statements gain a **binder, no hypothesis**. `selectHole_origin`'s conclusion changes
  meaning. Re-emit: the Std.hole bundle, P8, journey rows; package ids re-genesis.
- Blocker: RULINGS R-0001 HOLDs `Lang/**` to S1–S15 of the fold (`RULINGS.tsv:2`). Ember releases it, or E1 waits.

**E2. The member-socket model.** This is the multi-process object.
- Shape (INFERRED): a relation `SocketRel` between the resident's `Ev` trace (`.cmd c x`) and the member's own follower
  World. `x = .ok reply` for a submitting command implies a Step whose receipt the follower built and checked
  (`check_committed`/`check_refused_sound`, `Protocol/Proofs/Receipt.lean:43, :134`; `settle_final_never_admits`,
  `Settle.lean:201`). `x = .error _` covers a crashed or unready follower or stdio child, so **crash-stop on this leg is
  already quantified**, because `Runs` ranges over every `Except String Reply`.
- The new theorem: "every `answered` row is the text of some tick's kept answer" (ACT-D §4.4). It is a conclusion from
  `tick_counts` + `object_history_chain` (`Kernel/Proofs/Logic/History.lean:357`) + the receipt check + `SocketRel`.
- Price: **zero** on landed theorems. `tick_order`/`tick_counts`/`interp_runs` already quantify over every reply;
  `audit_ok` and the receipt theorems are used as stated. The new theorem carries ONE transport premise: the stdio
  reply bytes are the follower's Lean `done` step for that command (PROTOCOL-40: "replies are the `done` step",
  `decisions/protocol.md:998`). That premise is about Rust moving bytes (law 2), and it must be NAMED in
  `gates/tcb.tsv`, not hidden.
- What it deletes: LITP's "the join stays a journey row, named". The row becomes a tooth of the theorem.

**E3. Joint laws across objects (KERNEL-45 item 3), triggered by PROT-6.**
- Price (READ `decisions/kernel.md:1906`): "a separate judge (as LANG-44's row guards are), so the 85 law theorems in
  `Lang/Proofs/Receiver.lean` keep their statements": **zero** hypotheses on landed law theorems. The new judge carries
  its own soundness.
- Order: with or right after PROT-6. It is the same day as E1 if the cross-object read IS the joint law's input
  (INFERRED: it is).

**E4. Roles with declared reliability (LITP PROT-2 + PROT-5).** This is Barwell et al.'s crash-stop with a reliable set:
the kernel is reliable, the broker and provider are not.
- Price (RECORD LITP): `Polarity` is replaced by roles; about 12 theorems that mention `.ours` are restated (LITP's
  INFERRED count; the impact file must measure it). These are restatements, and no deployed theorem gains a hypothesis
  because the calculus has no deployed consumer (LITP A.5).

**E5 (only on a cross-host card). Receipts between Worlds, no agreement.**
- Shape (INFERRED): World B admits a call that carries World A's receipt, checked against an A-head that B's member
  holds under A's sponsor-signed origin (PROTOCOL-45 receipts, PROTOCOL-61 origin pins).
- This is mini's `EpistemicConsensus` point made deployed: "a discharged claim is distributed knowledge … no Byzantine
  subset can forge it" (READ `Theory/EpistemicConsensus.lean` header). A verified receipt is world-independent.
- Price: **zero** on landed theorems. The new theorem's premise is head freshness: A's operator can fork A, and B holds a
  head, not THE head. That is the same trust as a thin member today (PROTOCOL-42 critique).
- It buys asynchronous cross-host protocols (offer in A, acceptance in B, an escrow on each side). It does NOT buy
  atomic cross-host commitment.

**E6 (only if a row needs it). Multi-signer atomic Turns (KERNEL-45 item 2).**
- Price (READ `decisions/kernel.md:1897-1904`): `receive_ok`'s signed clause, `write_authorized`, `invoke_authorized`
  and `enroll_authorized` gain a **signer index**. PROTOCOL-39 gains a signed shape. `stale_refused`, `admit_value` and
  the frame theorems are untouched. The call codec changes and every Store re-geneses.

**E7 (not demanded). Agreement that replicates the writer's total order.**
- Price (INFERRED; theorem names READ): the kernel theorems quantified over "any log `l` folded from `w`"
  (`stale_behind_forever`, `settle_final_never_admits`, `staleBehind_final` at `Protocol/Proofs/Behind.lean:219`,
  `audit_ok`) are **unchanged**. A replicated total order is still one log.
- The hypothesis lands at the consumers: "the folded log is a prefix of the decided log". It enters every follower and
  settlement path, and `WriterLife`/`writer_life_trusted` (`Host/Proofs/Trusted.lean:239, :269`) must be restated over
  "the decided log's writer" instead of the file-lock writer. Charter law 4's lock text (the writer lock IS the append
  fd) stops being the safety argument.
- The KERNEL-44 recorded refusal ("final for its transaction id") becomes final only once the refusal STEP is decided.
- Mini's engine is the spec to read here (safety over the executable step; liveness absent).

**E8 (never, on this evidence). World-root merge of divergent histories.**
- Price (INFERRED): every theorem stated over `World.fold` extensions loses its object, because a merge of two forks is
  not a fold extension of either. That covers `stale_behind_forever`, `settle_final_never_admits`, `staleBehind_final`,
  `object_history_chain`, the escrow's at-most-once over a history (LEDGER-15) and `audit_ok`'s `Honest`.
- `admit_comm` commutes two Turns at one World and gives no merge.
- Mini's own `LaceMerge` is outside its deployed closure, and its `crossCanonical` hypothesis was the named gap (`Theory/LaceMerge.lean`
  header).

**Order: E1 → E3 (with PROT-6) → E2 (with PROT-3) → E4 (with PROT-5) → E5 on the first cross-host row → E6 on the
KERNEL-45 trigger → E7 only for writer availability → E8 not at all.**
- E1 comes first because REOR C1 and LITP PROT-6 both state their theorems over it, and C2–C5 quantify over its World.
- E2 comes before any claim that "the Bell is a multi-party protocol". Without it, PROT-3 proves the two projections
  separately and the conformance claim is two theorems plus a journey row.

### B.5 The charter amendment (INFERRED wording; the choice is Ember's)

Scope item 3 today says "Multi-node agreement. Nothing … no replication of the writer". Add: "Multi-party and multi-process
protocols over ONE writer are IN scope: residents, member sockets, followers and the protocols between objects, with the
member socket modelled. A protocol between two Worlds runs on receipts (no atomic commitment) until a row needs atomicity;
that row is the trigger for agreement." The amendment does not drop the refusal. It says what the refusal never
covered, because the 10-21 wording ("multi-node agreement") reads as "nothing distributed", and Ember's question shows
it was read that way.

---------------------------------------------------------------------------------------------------------------------

## PART C — WHAT MOVING TO MINI MEANS

### C.1 What mini's metatheory can express that nano cannot (READ)

- **Persisted activities with machine checkpoints.** "the exact machine checkpoint (the bytes of
  `ObjectiveBendCheckpoint.encodeState`, never a summary) … its phase … one `Await` … a mandatory deadline height"
  (`Kernel/ObjectiveActivity.lean` header). nano's `Std.activity` keeps a captured ROW, not a machine.
- **Interaction-tree semantics with divergence.** `Vis(p, k)`, `ret`, visible faults, `malformed`, and `spin`: "ignoring
  internal steps never equates spinning forever with eventually yielding" (`Theory/ObjectiveBendInteraction.lean`
  header). nano's `Prot` is inductive and has no `Tau` (LITP A.1).
- **Zoe.** Invitations as single-use role tokens, and offer safety as a law judged on every reallocation
  (`Kernel/Invitation.lean`, `Kernel/Seat.lean:1651`, lifted per decided turn by `SeatStore`). This is the
  literature's object for PROT-6, already shaped as a contract host.
- **Rooms** (`under R` scopes, kick, birth gates).
- **A BFT engine** with safety theorems over its executable step, plus a stated reconfiguration discipline.
- **A crash-protocol model** of durable install (`DurableCommitProtocol`).
- **Candidate-independent distributed theory**: Finality tiers ("tier 1 requires I-confluence"), revocation needs
  consensus while collection does not, epistemic verification and LaceMerge. Every one of these is outside the Host
  closure (MEASURED).

### C.2 What mini cannot express that the memos need (MEASURED)

- Contextual metavariables, σ, `fill`, CMTT: absent.
- TMS justifications, labels, provenance, minimal repairs: absent.
- A one-party `Prot` with holes, or anything shaped like LITP A.1: absent. Core4's `perform`/`done` is the effect half
  with no holes.
- **Version pins.** Mini pins name a digest (`Kernel/World.lean:386-392`), so a value written back to an old digest makes
  a stale pin fresh again (INFERRED: ABA). REOR C1's retraction is "a re-pinned tombstone is refused for ever", and
  PROTOCOL-57 is "BEHIND is final by theorem". Both rest on `stale_behind_forever`, which is a monotone-version fact
  (`Kernel/Proofs/Versions.lean:232-245`). They do not transfer to digest pins without adding versions to mini's kernel.

### C.3 What it costs that the theorem object is not the writer's (the real version of "proofs do not gate")

If the contextual, repair and protocol theorems were built in mini today, they would be theorems ABOUT mini's
DATAMODEL World, not theorems THAT mini's writer runs on:
- `World.admit` (`Kernel/World.lean:647`) has no caller on the writer path (MEASURED). Its one deployed consumer is
  `Host/TurnLogFollower.lean`, which derives Turns from the Store's accepted records after the fact (READ header).
- Activities and seats are decided by their own `step` over their own `World` (`Kernel/Seat.lean:769, :925`), then
  lifted into stored cells (`SeatStore`). That is a third state shape beside the DATAMODEL World and the DurableReceiver
  image.
- So a REOR-style "live bridge" stated in mini would have to pick which of three worlds is "the kernel World". In nano
  there is one (CHARTER law 1).

### C.4 What mini would need from nano's discipline before the work meant anything there

1. **The disjunct check, landed.** CX-MINI-COLL did this for ONE class: 7 patches, 61 files, +1,978/−297 (MEASURED
   `git diff --stat 334316df HEAD` in the lane), 48 sites (the brief said 47; the lane's own commit says "all 48"), each
   with a dropped-list mutant. It took one lane-day, and it is **not landed**: "the WHOLE umbrella output, exit 1. Only
   failing module: `Fixtures.NativeAcceptedFixture` … This is NOT literal umbrella PASS and does NOT authorize landing"
   (ready-readme). Until it lands, `Theory/AuthTrie.lean:135`'s disjunct makes the trie, world-root, durable-index and
   receipt-continuity binding theorems true by pigeonhole. Per patch 0005's message, `WorldRoot`'s carrier on main asks
   for "impossible global separation", so its premise is uninhabitable at deployed parameters.
2. **A judge that can be green.** Mini's verdict has known-red as a standing row. Any new mini theorem lands into a tree
   whose literal verdict is red. Per the memory rule "red as steady state hides everything", that verdict cannot see the
   next wound.
3. **#guard → named theorems.** There are 4,258 `#guard` lines (MEASURED); nano has 0. Each one checks an instance with
   no term and no axiom record.
4. **One state machine.** Pick the writer's world as THE World, or the contextual theorems describe a follower.
5. **A Host closure under a ceiling.** Mini's is 788, while nano's is 89 against a ceiling of 150. Every contextual
   module added to mini's closure enters an umbrella of 1,560 library modules (lane final checks).
6. **A moving main.** Mini main is frozen at the 10-17 finish-only call; changing that is Ember's call.

**Port cost (INFERRED from the measured lane):** items 1–2 are about a lane-week on mini's own landing machinery, and that
machinery is currently red. Item 4 is the twin-deletion campaign mini's KERNEL-TWIN-AUDIT (2026-09-04) already named
("twins with one shared abstract object", `docs/KERNEL-TWIN-AUDIT.md:141-143`), and it has not been done in six weeks.
Only after that do the contextual/TMS/protocol objects get built from nothing, because mini has none of them.

### C.5 The memory fact, verified at source

"no proof system in mini admission: `witnessed` compiles to FALSE; runs are checked by RE-EXECUTION; proofs are an empty
carrier slot":
- TRUE at `Compiler/PredCompile.lean:602-603` (`.witnessed _ => (cst 0, [])  -- first-party fail-closed: the indicator is
  constant 0`), with the doc line at `:18`. The oracle that discharges `witnessed` lives outside the AST
  (`Pred/Core.lean:261`).
- Re-execution: `checkRun_sound` and `no_accepted_of_output_mismatch` are at **`Kernel/Run.lean:316, :383`**. The memory
  names `Kernel/NockRun.lean`, which **does not exist** at 334316df (MEASURED). Correct the memory.

---------------------------------------------------------------------------------------------------------------------

## PART D — THE HYBRID

### D.1 Is there a shared kernel shape? (READ, MEASURED)

| | nano `Kernel/World.lean:268-300`, `Kernel/Turn.lean:107-119` | mini `Kernel/World.lean:265-267, :371-392` |
|---|---|---|
| state | `trie : Cells D` (one binary Merkle trie over `Slot` = cell id or nullifier, path-compressed per KERNEL-49), plus `journal`, `refusals`, `rows` tries; `height`, `steps`, `chain`, `allowance`, `origin` | `cells : Π₀ CellId, Option (Cell R)` + one system `Store` with namespaces journal/head/retired/parent/spent/allowance |
| cell | `{kind : Nat, discipline, slots}` (`Kernel/Cell.lean:44-47`) | `{kind : R.Kind, store : Store (R.layout kind)}` with ROM/RAM/append-only layouts per registry |
| pin | monotone version per entry; tomb terminal | digest of the cell (`History.cellDigest`); retired = refused |
| turn | `touches (cell, seen, act)`, `creates`, `nullifiers`, `charge`, `event`, `rows`, `ranges`; ONE signer (KERNEL-45) | `creates (id, cell, room?)`, `legs` (guarded patches), `retires`, `event`, `nullifiers`, `charge`, `subject`, `keyEpoch`, `capability`, window, `absent`, `pins` |
| root | cells-trie root inside each chain link | `WorldRoot.rootOf`: `AuthTrie` over slot roots (`Kernel/WorldRoot.lean:1-25`); a two-level root |
| identity of a World | `origin` set at genesis, the FIRST check (`wrongWorld`) | none in this record; deployment identity in NativeHost settings |
| rooms | absent | `parent` namespace |

They are not the same trie, the same pin or the same cell. The one shared idea is "pinned pre-state, then one atomic
admit", which both inherited from mini's TURN-LOG design (NVM-17 §3.1–3.3, RECORD).

### D.2 Nano's theorems stated over mini's objects through a bridge (INFERRED)

- A bridge needs a map from mini's state to nano's World. Digest pin → version pin is **not a function**: versions
  count writes, and a digest forgets them (ABA). So `stale_behind_forever` and everything built on it (REOR C1, C9;
  PROTOCOL-57; KERNEL-54's "final by structure") has no image.
- The bridge's target would be mini's DATAMODEL World, which the writer does not run (C.3), so the theorems would be
  about mini's follower.
- What survives a bridge: theorems that never mention pins or finality, such as CMTT typing of a hole's filling or
  `label_iff` over an abstract World. Those are exactly the parts REOR flags as "abstract duplicates" to delete once the
  deployed instance exists (REOR B.2/C2). A bridge would keep the abstract half alive and lose the deployed half: the
  reverse of the fold.

### D.3 Mini re-based on nano's kernel (INFERRED; it is NVM-17 path (a))

Breaks:
- rooms: nano needs a parent relation, and that raises a premise-price question on the authority walk theorems;
- the registry's ROM/RAM/append-only layouts, mapped onto `Discipline`/slots;
- the ~18k mini theorems stated over `Π₀` cell maps and the system Store;
- the seat and activity worlds, which become nano cell kinds or rows;
- the Generic Simplex engine's source records, which assume mini's DataIntent record shape (`Kernel/JointReceiver.lean`
  header);
- every mini Store re-geneses (cheap here).

Ember's 10-21 reframe made (a) "OPEN, not the plan": "brief nano lanes as demonstrations mini can take, never as mini's
replacement" (RECORD, rebuild memory). Re-basing mini is the mini-replacement move by another name, and it would not
put a single contextual theorem into the system any sooner than E1 in nano would.

### D.4 The hybrid that works (INFERRED)

The hybrid that works is spec-level, which is law 11 as written: "If a minidregg definition is right, restate it from
its theorem, smaller" (CHARTER.md:107-108). Concretely:
- **Zoe → PROT-6.** Restate `Invitation` (a single-use role token, spent like a nullifier) and offer safety
  (`safeAt … = true` for every open seat) as the fuse generator's law. PROT-6's `fuse_iff_compliant` becomes offer safety
  over two real offer rows. Price: the same as E1 + E3.
- **ObjectiveActivity's checkpoint → PROT-1.** Measure whether `Std.activity`'s captured row loses anything a machine
  checkpoint keeps: a resumption that depends on more than the captured argument and the response. If it does, nano's
  activity needs a checkpointed continuation. If it does not, ignore the difference.
- **ObjectiveBendInteraction's `spin` → PROT-3/4.** If any activity body can diverge under the step meter, the global
  type needs a `Tau`/divergence node or the monitor theorem is about terminating bodies only. State which.
- **Generic Simplex → E7's spec,** if ever.

---------------------------------------------------------------------------------------------------------------------

## PART E — RECOMMENDATION, AND THREE WAYS IT IS WRONG

### E.0 The recommendation

1. **Build the dream system in nano.** Land E1 (`look` + `SupportPin.cell`; this is REOR C1, which needs R-0001
   released), then PROT-6 with E3, then E2 (the member-socket model) with PROT-3, then E4 with PROT-5. Each lands with
   its consumer (P8 journey row, the fuse row, the Bell rows) and its tooth.
2. **Amend charter scope item 3** as in B.5. It is a clarification of what was never forbidden, not a widening.
3. **Read mini as spec for four objects** (D.4: Zoe seats/invitations, the activity checkpoint, interaction-tree
   divergence, the Simplex engine). Restate them; do not port or bridge them.
4. **Do not move the program to mini.** Mini has none of the memos' objects. Its theorems stand on a World its writer
   does not run, its main is frozen, its verdict is red by standing rule, and its binding theorems are vacuous until an
   unlanded 48-site series lands. Moving would trade a tree where a new theorem is about the deployed object for one
   where it is about a follower model, with C.4's six debts paid first.
5. **Separately**, and independent of where the dream system is built: CX-MINI-COLL's series should land in mini if mini
   is to stay the spec of anything. Until it does, mini's trie/world-root/receipt-continuity statements cannot be cited
   as binding. That is ROOT-for-Mini's item and Ember's literal-PASS call (ready-readme step 2).

### E.1 Refuter 1: some card needs more than one writer

**Claim at risk:** no card in REOR or LITP needs a multi-writer total order or a cross-World atomic commitment, so
nano's refusal of agreement costs the program nothing.
**Measurement:** for every card (REOR C1–C9, LITP PROT-1..8) and every consumer row it names, list the Worlds whose state
the row changes, and whether two of them must change atomically. Also run LITP D.2's measurement: grep the receivers for
any state recording "dispatched, awaiting" across Turns between two CELLS of DIFFERENT Worlds.
**Refuted if** any row needs two Worlds changed atomically, or Ember's "bigger focus" names a concrete two-operator
protocol where E5's receipts (asynchronous, no atomicity) are not acceptable to that row's owner. Then E7 is on the path,
mini's Generic Simplex is the spec, and the charter's scope item 3 must change, not just be clarified.

### E.2 Refuter 2: the member-socket model cannot be stated without making nano a model of its Rust

**Claim at risk:** E2 costs one named transport premise ("the reply bytes are the follower's Lean `done` step").
**Measurement:** trace one resident `cmd` from `Hosting/Resident/Sockets.lean` through `nd --stdio`, nd-members and the
follower's `Follow.loop` to the writer's `submit`. Count every point where Rust decides something: selection, retry,
ordering or synthesis of a reply. HOSTING-41's readiness probe is already one ordering decision made in Rust
(`decisions/hosting.md:2276`).
**Refuted if** the count is greater than zero beyond byte transport and process lifecycle. In that case E2's theorem
would quantify over a Rust behaviour that Lean does not decide (a law-2 violation, or a twin of the Rust in Lean). The
honest alternative is to move that decision into Lean first (a Lean `stdio` decider), and E2's price rises by that
move.

### E.3 Refuter 3: mini already delivers PROT-3/PROT-6 over its writer, cheaper

**Claim at risk:** mini's Zoe seats are spec only, and nano must rebuild them.
**Measurement:** read `SeatStore`'s `Decided.inv`/`Decided.conserves` statements and trace whether the native host's
seat receiver commits exactly `Decided`'s posts. Then check whether any history-level theorem ("every seat in every
world the WRITER reaches is safe") exists over the native route's admitted records, rather than over `Seat.Reachable`
from an empty seat world (`Kernel/Seat.lean:1640-1655`). Also confirm that none of its premises routes through
`Theory/AuthTrie`'s unbounded `Collision`.
**Refuted if** offer safety holds over the writer's admitted history with premise-clean statements. Then the cheapest
PROT-6 is to state compliance-fuse as a seat instance IN mini (once C.4 items 1–2 land), and the recommendation narrows
to "contextual/TMS in nano, Zoe-negotiation in mini". What I measured so far: the forever-theorem is over Seat's own
`World`/`step`, and `SeatStore` lifts PER DECIDED TURN. The history lift over the native log is unverified either way.

---------------------------------------------------------------------------------------------------------------------

## APPENDIX — commands behind the MEASURED tags

- nano sizes: `git show origin/main:SIZE.md`; per-layer `git ls-tree -r … | wc -l`; theorem lines per area by
  `git grep -h -E '^(private |protected )?theorem '`; `#guard` by `git grep -h -E '^#guard' origin/main` → 0.
- nano contextual consumers: `git grep -l -E '^import Lang\.(Contextual|Proofs\.Contextual)' origin/main -- Host Kernel
  Hosting Protocol Ledger` → none.
- mini sizes: `git ls-tree -r --name-only HEAD | grep .lean | xargs cat | wc -l` → 598,409; theorem lines 18,334;
  `#guard` 4,258 in 519 files; `∨ Collision` hits 23.
- mini Host closure membership: a Python walk of `^import` lines from `Host/Main` + `Host/ClientConsentSession` (my walk
  reaches 800 files; the lane's gate pins 788 modules; the membership results above do not depend on the difference).
  In: `Kernel.World`, `Kernel.GenericSimplex`, `Kernel.DurableCommitProtocol`, `Kernel.ObjectiveActivity`,
  `Theory.ObjectiveBendInteraction`, `Kernel.Seat`, `Kernel.Invitation`, `Kernel.RoomBirthGate`,
  `Theory.RoomAuthorization`, `Kernel.MultiCellHyperedge`, `Kernel.JointReceiver`, `Kernel.WorldRoot`,
  `Kernel.ReceiptContinuity`. Out: `Kernel.FinalityGate`, `Kernel.ReplicatedSettlementFinality`,
  `Kernel.NativeJointAgreement`, `Kernel.GenericSimplexReconfig`, `Theory.LaceMerge`, `Theory.EpistemicConsensus`,
  `Theory.RevocationConsensus`.
- mini `World.admit` callers: `git grep -n -E 'World\.(admit|step|fold)\b' HEAD -- Kernel Host Compiler` outside
  `Kernel/World.lean` → none; `open Minidregg.Kernel.World` appears in `Host/TurnLogFollower.lean`,
  `Host/ObjectiveTurnTotalityRunner.lean` and `Host/WorldFoldBench.lean` only.
- mini main date: `git log -1 github/main` on hbox warm-base → 334316df 2026-10-17.
- CX-MINI-COLL: `git log --oneline 334316df..HEAD` in the lane src → 7 commits; `git diff --stat` → 61 files,
  +1,978/−297; final gate log and ready-readme quoted above.
