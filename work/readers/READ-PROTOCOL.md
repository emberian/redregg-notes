# READ-PROTOCOL — whole-file read of nanodregg `Protocol/` at f9657bd (2026-10-24)

Reader: one subopus, PROTOCOL layer. Checkout `/Users/ember/dev/nanodregg` at `f9657bd` (clean but for an
untracked README copy). Nothing edited. Tags: READ (path:line), MEASURED (a command I ran), INFERRED.

## Verdict

I read whole: `Command/Machine.lean` (1381 lines, twice over in parts), `Receipt.lean`, `Proofs/Receipt.lean`,
`Settle.lean`, `Command/Exit.lean`, `Exit.lean`, `Rows.lean` (all 1626 lines, every row's plant line counted by
hand against its line list), `Rows/Loopback.lean` (all 1260), `Rows/Run.lean`, `Rows/Writer.lean`,
`Rows/Params.lean`, `Rows/Judge.lean`, `Rows/Deployed.lean`, `Rows/Main.lean`, `Proofs/Rows.lean`,
`Proofs/Judge.lean`, `Foreign.lean`, `Proofs/Foreign.lean`, `Proofs/FollowHead.lean`, `Proofs/FollowJournal.lean`,
`Thin.lean`, `Invite.lean` (lines 36–191), `Envelope.lean`, `Attempt.lean`, `Use.lean`, `Frames.lean`,
`Command/Wire.lean`. I read the theorem statements, not every proof, of `Proofs/Command.lean` (lines 1–520 whole,
then the statements of the rest), `Proofs/Settle.lean` and `Proofs/Behind.lean`. And `Table.lean` 270–510,
decisions PROTOCOL-64, -65, -67, -68, -69 in full, and CHARTER. That is about 9,500 of the 15,900 lines.

The layer is mostly careful, and most of the brief's suspicions come back clean. Of the 45 rows, 44 have a plant
that moves the line it names, by the mechanism the row says it guards. The receipt check order is sound. The
`forkedHead` replay question is benign. The argv derivation is right as far as it goes. The three worst things:

1. **The frame budget is per field, never per frame. The deployed page budget leaves under 900 bytes for the
   continuation.** A command whose argv is longer than about 690 bytes cannot take back a full log page in its
   `resume` frame. That covers every deployed `receipt CALL` confirm of a call over ~335 bytes, which is an
   ordinary write, and every `install` of a real package. The write path's own `k` holds the call twice, plus
   the argv. PROTOCOL-68 derived the argv bound and stopped there. The rows cannot see any of this: their page
   budget is 65,541 rather than 261,120, and their harness and `Host.Follow.answer` bound each field, never the
   frame. (DEFECT, INFERRED from the arithmetic below.)
2. **`nd cancel CALL` exits `ok` ("cancelled TXID") on the Host's word.** `cancelAnswer` never checks follow's
   own World. This is the same class PROTOCOL-64 closed for step 4. A Host that admitted the call and answers
   `refused cancelled` makes the member's `nd cancel` succeed. No row plants that Host. (DEFECT, READ.)
3. **Statements and comments that say more than the code.**
   - `toy_budget_serves` and `deployed_budget_serves` are `Nat.le_refl` of the definition, a check of nothing.
   - The rows' "deployed parameters" are not the deployed page budget.
   - PROTOCOL-67's critique says that a step-0 World that is not this joiner's genesis "is not one follow can
     hold". `Kernel.carryWorld` sets `steps := c.height`, so a World carried at height 0 is exactly that.
   - Two rows' docstrings name a plant line and outcome that PROTOCOL-64 changed.
   - The `stepsPerCommandMax` doc says follow ends the command, but follow has no step counter: Rust's
     `client/src/run.rs` does.

   (DEBT and QUESTION, READ.)

The brief's specific questions are answered in §4, each with its tag.

---

## 1. DEFECTS

### D1. A command with more than ~690 bytes of argv cannot resume a full log page. The write path's continuation carries the call twice. (DEFECT, INFERRED)

**Where (READ):**
- `Protocol/Table.lean:416`: `frameBytesMax := 262144`, "One frame body (op or status byte and payload),
  either socket, either direction".
- `Host/Page.lean:78`: the deployed page budget, `budget := frameBytesMax - 1024`.
- `Protocol/Table.lean:297`: `resumeLayout := [.bytes "k", .bytes "result"]`. One resume frame carries the
  continuation AND the page.
- `Protocol/Command/Machine.lean:220-231`: `k` is the State frame, `argv ‖ phase ‖ acc`. It holds the WHOLE argv.
- `Protocol/Command/Wire.lean:23-30`: `Reply.frame` bounds each field (`Text.fit _`), never the sum.
- `Codec/Layout.lean` header: "Every byte-string field shares one bound `max`".
- `Host/Wire.lean:26,86`: the transport refuses a body over `frameBytesMax + 4`.
- `client/src/frame.rs:60`: the client refuses `pastBound frameBytesMax`.

**Why it is wrong:**
1. A full page is up to 261,120 bytes of events. With its header (~124 bytes) and status byte, the Host's reply
   is ≈ 261,249 bytes.
2. The client sends that reply back verbatim inside `resume (k, result)`. Each field costs 4 bytes of length,
   plus the op byte.
3. So the frame admits `|k| ≤ 262,144 − 261,249 − 9 ≈ 886`.
4. At phase 2, `k` is `argvSize + 1 + acc`. Its acc is `[startB, signedB, pagesB, upToB, triedB]`, ≈ 196 bytes
   (`signedB` is 32+32+64 plus framing at the deployed widths). So `argvSize ≲ 690`.
5. `receipt CALL` is `4 + 11 + 4 + 2·|call|`, so any call over ≈ 335 bytes breaks the confirm.

A deployed `write @shared 2 1 --via @g` call already exceeds that, INFERRED from its fields:
- world, member and key: 3 × 32;
- notBefore and validUntil;
- one pin, 2 × 32;
- the body's object, key, value and via;
- the 64-byte signature;
- framing.

`install TEXT` carries the package text. The Bell is 27.7 KB printed.

So any such command fails when follow is a full page behind: it is refused at the client's frame reader (or
`badLength` at the Host's), not `behind`. That is a confirm on an attempt's next run after time away, a cold
`receipt`, or an install by a member who has been away. The attempt reads a failed confirm as `uncertain`, so
the attempt never settles until the member happens to run `nd sync` first.

The write path is worse at the far end:
- Phase 3 → 4 hands `.submit (X.callBytes c) k` with `k = [startB, signedB, ub, out, callBytes c]` plus argv
  (`Machine.lean:1295`).
- The call travels three times in one frame: `ub = callMessage u`, `callBytes c` in `k`, and the `call` field.
- Phase 2 → 3's `.sign (X.callMessage u) k` carries `ub` twice, plus argv (`Machine.lean:1273-1274`).
- With a call near `eventBytesMax = 65,536` and an install text near the argv bound, the step reply exceeds
  `frameBytesMax`. That install was admissible but can never be signed or submitted.

PROTOCOL-68 states the bound "every admitted call can be confirmed" and proves only
`Command.receipt_argv_fits` (`Proofs/Command.lean:74`, argv ≤ 132,096) and `argv_fits_frame`
(`Proofs/Table.lean:105`, argv + 1 ≤ frame). Neither looks at `k + result` or at `call + k`.

**Why no row sees it (READ):**
- The rows' writer pages at `Params.pageBudget = pageEventBytesMax + 4 = 65,541`
  (`Rows/Params.lean:88`, `Rows/Deployed.lean:35`), "HOST's `Page.budget` is a frame, which no row's log
  reaches" (`Rows/Params.lean:55-56`).
- The rows' `resume` fits `k` and `result` separately (`Rows/Loopback.lean:651-652`).
- `Host.Follow.answer` decodes `resumeFrame` with per-field bounds (`Host/Follow.lean:77`).
- The in-process path has no frame-total check anywhere, so `rows --deployed` passes with frames the deployed
  transport refuses.

**What would decide it:** compute `(resumeFrame.bytes (k, page)).size` for the phase-2 `k` of
`receipt <hex of a deployed write call>` and a `Host.Page.build` page at `Page.budget`. Or run the deployed `nd`
confirm against a follower one full page behind. A Lean statement of the property: for every phase-2 `k` that
`step` emits and every page `Host.Page.build` serves at `budget`, the resume body is at most `frameBytesMax`.
Today that statement is false.

### D2. `cancel CALL` ends `ok` on the Host's word, unchecked by follow's World (DEFECT, READ)

**Where:** `Protocol/Command/Machine.lean:1136-1146` (`cancelAnswer`).

```lean
  | some (.refused, p), some c =>
      if hostName p = (Receive.Refusal.cancelled : Receive.Refusal D).name then
        printed s!"cancelled {hex X (txIdOf X c)}\n"
      else refusedAt X (.host (hostName p))
  | some (.ok, _), _ => refusedAt X (.host "committed")
```

**Why it is wrong:**
- PROTOCOL-46 says "a settlement is the member's word, never the Host's".
- PROTOCOL-64 found exactly this class at step 4 and made `settled` check `ownSettle` on follow's World. Its
  wording: "the only one of the nine that can make a reply say ok".
- Phase 9 (`sendCancel`, `:1119-1128`) checks that `Receive.cancel` WOULD record on follow's World BEFORE
  sending. The theorems `sendCancel_host` and `step_host_cancel` say only that. Between phase 9 and the Host's
  answer, the writer may have admitted the call (another relay held the bytes, the Host's attempt queue, or a
  lying Host). Phase 10 then prints `cancelled TXID` with exit 0, and nothing re-reads the World.
- The mirror arm `(.ok, _) => refused committed` also renders a Host claim as a verdict: "your call committed",
  on the Host's word.

**Mutation that shows it:** a writer that admits the call and answers the `cancel` op `refused cancelled`. The
member's `nd cancel` exits 0 and prints `cancelled`.
- No row has that writer. `cancelRow`'s plant is `cancelUndomained` (`Rows.lean`, the `cancel` row, line 8),
  which follow's OWN phase-9 pre-check catches before anything is sent.
- `cancelForgedRow` checks the follower's absorb, not the cancel command's exit.
- The later `rerun` line of `cancelRow` settles by follow's fold. That is the attempt, not the cancel command.

There is no theorem of the form "`cancelAnswer` = ok ⇒ follow's World records `cancelled` at the id". Compare
`settled_ok`.

### D3. Exit `ok` from a phase-4 continuation names a call that `k` chose, not the call the argv planned (QUESTION, bordering on DEFECT; documented in PROTOCOL-64's critique)

**Where (READ):**
- `Machine.lean:1312`: `| _, 4, [_, _, _, out, cb] => same (settled X me w out cb result)` matches ANY `cmd`.
- `cb` and `out` both come from the unauthenticated `k` (`State.ofBytes`, `:233`).
- `settled_ok` and `step_settled_ok` (`Proofs/Command.lean:271`, `:296`) quantify over whatever `cb` the `k`
  holds.

Answer to the brief's question ("ok only if settleOf on follow's own World is committed: is there any other path
to exit ok?"):
- (a) The `cancel` arm above.
- (b) Any `k` whose last item is ANY committed call's bytes. For example, a relay that replays an earlier
  attempt's phase-4 `k` with a `committed` action byte makes `nd write …` print the OLD write's `out` (`tx …`,
  `id …`) and exit 0. Follow never compares `cb` with a re-plan of the argv's command, and it could: phase 3
  already re-plans and compares `callMessage u ≠ ub`.
- (c) `out` is printed verbatim from `k` (`:1057`), never re-derived from the journal (PROTOCOL-64 says so).

PROTOCOL-64 calls `k` swapping "outside" the trust of byte relay. That holds only if `k` never crosses an
untrusted hop. PROTOCOL-64's own measurement counted Rust's relay of `k` as a decision path, and the rows relay it
honestly, so no plant can see it.

**What would decide it:** whether any deployed hop that carries `k` is outside the member's own process tree
(`client/src/run.rs`, the `nd --stdio` resident path, HOSTING's member socket).

---

## 2. QUESTIONS

### Q1. `atGenesis` accepts a step-0 World that no genesis of this joiner built (QUESTION, READ + INFERRED; the brief's question)

**Where (READ):**
- `Machine.lean:1077-1087`: `atGenesis w := w.steps == 0 && w.trie.toList.all genesisLeaf`.
- `genesisLeaf` accepts ANY live member or grant cell.
- `Kernel/Receive/Follow.lean:177-180`: `carryWorld … steps := c.height`.

**Reachable?**
- A World carried (OPS-P1, `host import`) at height 0 has `steps = 0`. A height-0 World has only had recorded
  refusals, and refusals change no cell. Its trie is the OLD lineage's founders' member and grant cells,
  re-keyed under nothing new (KERNEL-40: founder ids are the lineage's names).
- A member re-invited to that carried World (`acceptCarry`, `host join` with a carried start) holds it, and its
  `atGenesis` is true.
- PROTOCOL-67's critique says: "a step-0 World whose member cells differ from the joiner's inputs would pass.
  That World is not one follow can hold". That sentence is false for the carried case.
- No step-0 World other than `genesisWorld` and `carryWorld` at height 0 is constructible through follow. The
  only cell-adding move is admission, and admission advances `steps`.

**Is it harmful?** INFERRED: no.
- Such a World holds no object (`atGenesis_object` still holds), so `step_keeps`' consumers stand.
- The adopted base is pinned by a sponsor-signed invitation, origin-checked (`Machine.lean:1349`).
- What is lost is the predicate's NAME: "a World a genesis builds". It is "a step-0 World of members and
  grants", and its docstring (`:1081-1085`) and PROTOCOL-67 should say that, or the check should compare with
  the carried and genesis start held in `Self`.

The trie test also ignores `w.rows` and `w.journal`. A carried height-0 World can hold neither, so no reachable
case is affected.

### Q2. `badCall` at step 3: is it reachable? (QUESTION; the brief's question, answered READ)

On the canonicity part of the question:
- The deployed codec is canonical: `Codec/Proofs/Kernel.lean:373 eq_callBytes_of_decodeCall` gives
  `decode b = some c → b = callBytes c`.
- So a non-canonical encoding of a call does not decode at all. It is never "a non-canonical call that decodes".
- At `receipt CALL` it is refused `badCall` (`Machine.lean:965-967`).
- In a logged event it is refused `eventMismatch` at its position (`:451-452`).

Step 3's `X.decodeCall (X.callBytes c) ≠ some c` (`:1292`) can fire only for a `c` outside `Call.Fits`
(`Codec/Proofs/Deployed.lean:35 decodeCall_callBytes` needs `Fits`). Whether a `plan` that `World.admit`
accepted can produce a non-`Fits` call (a field past the codec's u32 or the bound, which `checkBounds` does not
bound) decides whether this refusal is reachable or is an assertion that cannot fail. PROTOCOL-69 says "on a
call the deployed codec never produces from a `Fits` plan". No theorem says `plan` yields `Fits`.

### Q3. Receipt check order: is a forged root ever `pathMismatch`? (answered: no, READ)

- `Receipt.check` (`Receipt.lean:98-102`) refuses `otherTx`, then `headMismatch` on
  `rootsDigest r.root r.jroot r.rroot r.rowsroot ≠ roots`, then the paths (`answerOf`).
- A forged value of ANY of the four roots reaches `pathMismatch` only through a `rootsDigest` collision
  (`check_committed`'s first `CollidesAmong` list names `rootsPre` of both).
- Row X2's `pathMismatch` (the stated height forged) is the journal leaf, behind correct roots, as PROTOCOL-65
  says.

On the `Foreign` path, though, `otherTx` is dead: `Foreign.check` (`Foreign.lean:43`) passes the receipt's OWN
`r.txId` as the id to check. The column checks "some committed tx at this head" and reports which one (`s.tx`).
Use-once and binding to a particular call are left to the acceptor package. That is intended (PROTOCOL-65 §4),
but `Receipt.Refusal.otherTx` cannot fire there, and `foreign_receipt_sound` concludes about `r.txId`, not about
a call the consumer names. (DEBT, a refusal that cannot be reached on that path.)

### Q4. The head object's `forkedHead` with same steps AND same roots, a replay (answered: benign, READ)

`Lang/StdHead.lean:45-47`: from `at` to `at`:
- `steps` never falls (`staleHead`);
- equal `steps` requires `eqData headAtTy o n` (same height and roots), else `forkedHead`;
- `height` never falls (`badHead`).

So a byte-identical re-post is admitted as a no-op, and a replay of an older post is `staleHead`. Neither moves
the head. The real gap is the one PROTOCOL-65's critique names: a poster fed a fork posts a consistent lie at a
NEW step count, which no law sees. And `fork`'s `other` roots are the poster's word, so any grantee can freeze
the object.

### Q5. Is the argv limit derived from the kernel's call limit enough? (answered: argv yes, frames no, READ)

- `Kernel/Receive/Call.lean:574` makes `t.event = X.callBytes c`, and `Kernel/World.lean:898` bounds it by
  `eventBytesMax`.
- So `receipt_argv_fits`' premise `call.size ≤ eventBytesMax` is the admitted bound. The argv is
  `4 + 11 + 4 + 131,072 = 131,091 ≤ 132,096`, and the command frame fits.
- What it does not cover is D1: the continuation that echoes the argv, alongside a page, or alongside two more
  copies of the call.
- The theorem's link to admission is by docstring. Its premise is a bare size, not `World.admit … = .ok`.

### Q6. `chainMismatch` when follow's World moved between frames (QUESTION, READ)

- A phase-1 `k` records `startB` (follow's `w.steps` at `start`). The envelope asks the writer for a page from
  `startB`.
- `absorbPage` folds the page onto follow's CURRENT World (`Machine.lean:1218`), with no check that the page
  starts at `w.steps` (`LogPage` carries no start).
- If another command's frames moved follow's World in between (two `nd` commands of one member interleaving on
  one follow), the fold ends off by the difference and the refusal is `chainMismatch STEPS`. That names the
  writer's chain, though the writer did nothing wrong. Law 7 says a refusal names the fault.
- What would decide it: is a member's follow ever driven by two commands at once (the attempt store's confirm
  beside a user command, or a resident and its owner)? `Host.Follow.loop` serializes frames, not commands.

### Q7. A read envelope does not bind its op (QUESTION, READ)

- `Envelope.message` (`Envelope.lean:84-86`) has one domain, `nanodregg/protocol/read-envelope/v3`, for both
  `log` (`start` = a step count) and `read` (`start` = a byte offset into the newest base, `adoptEnvelope`,
  `Machine.lean:839-840`).
- So one signature authorizes both a log page from position S and a base page from byte S, inside the window.
- Both are reads the signer may perform, so INFERRED this widens nothing a member could not ask itself. But
  "the message signed is exactly the request" is not true, and PROTOCOL-39's disjoint-domains census
  (`Proofs/Domains.lean`) does not cover op separation.

### Q8. `staleRange`'s plant changes two things (QUESTION, READ)

`Rows/Loopback.lean:943` routes any `--range` command under `staleRange` through `forged`. That path does NO
catch-up AND skips follow's own admission (`planUnchecked`, `:911-933`). The row's `declined stale` is the
writer's verdict on a call signed at the stale listing. If a deployed change let a stale range through follow's
own admission, nothing here distinguishes "follow admitted it" from "follow was skipped". The tooth holds the
writer's check, not follow's.

### Q9. The rows never exercise what follow persists (QUESTION, READ)

`Rows/Loopback.lean:516-518`: "What follow would persist is not modelled here: the actor's state is in memory."
`Command.Persist` (`.steps ts`, `.adopt w`) is dropped in every row, so the append-then-answer rule
(`Host.Follow.loop`'s docstring) and the adopt-then-seal-as-own-base path have no member row. Any tooth for them
lives in HOST, which I did not read.

---

## 3. DEBT

### B1. `toy_budget_serves` and `deployed_budget_serves` are identity carriers (DEBT, READ)

`Protocol/Proofs/Rows.lean:32,35` prove `pageEventBytesMax + 4 ≤ toy.pageBudget` by `Nat.le_refl _`, for a field
DEFINED as `pageEventBytesMax + 4` (`Rows/Params.lean:88`, `Rows/Deployed.lean:35`).
- The statement can fail only if someone edits the definition, which the definition's own docstring already
  says.
- Law 6's vacuity read names "identity carriers".
- The fact that matters for the deployed writer is HOST's `budget_fits_event` (`Host/Proofs/Page.lean:49`), and
  it is not what these name.

### B2. The rows "at the deployed parameters" do not page at the deployed budget (DEBT, READ)

PROTOCOL-50 and the `Rows/Params.lean` header say the deployed run instantiates "host's own" pipeline. The page
budget is the one place it does not: 65,541 against `Host.Page.budget` = 261,120. That is deliberate (so rows
see page ends), but the header's list of what the deployed run swaps in should say the budget is a row stand-in.
It is also why D1 is invisible.

### B3. Two rows' docstrings name the plant shape PROTOCOL-64 replaced (DEBT, READ)

- `Rows.lean:1331` (`settleRow`): "The plant is a store that takes the Host's status: line 6 reads the lie,
  `refused stale`". The plant (`:1358`) is `.caught .trustLookup 1 (.contradicted "committed open")`.
- `Rows.lean:857` (`refusedRow`): "line 13 is `refused stale`". The plant (`:908`) is
  `(.contradicted "refused open")`.
- The comments in the plant lines are right. The docstrings above them lie.

### B4. `settleRow`'s plant bites at line 1, a generic effect, not the row's subject (DEBT, READ)

The row is about a lying LOOKUP (line 6, fault `lieLookup`).
- Under `trustLookup` the first SUBMIT of the run is caught. That submit is the welcome's `enroll` at line 1: the
  store ends on the Host's `ok` without a confirm, and follow is not caught up.
- The runner checks only the declared line (`Rows/Run.lean`, `caught`), so the plant would stay "caught" even if
  line 6's lying-lookup path were broken in some other way.
- A plant that names line 6 would tie the tooth to the row.

### B5. Follow's own settlement rendered as `Refusal.host`, and a name round-tripped through text (DEBT, READ)

`Machine.lean:1062-1063`:

```lean
refusedAt X (.host (settledName ((Settle.Verdict.refused code : Settle.Verdict D).text X.env.bytes)))
| some .expired => refusedAt X (.host "expired")
```

- `.host` is documented "the Host refused, by its name" (`:78-79`), but this is follow's verdict.
- `settledName` (`:975-979`) parses `Verdict.text`'s output back with `splitOn " "` to reach `Receive.codeName`,
  which it could call directly.
- That is two definitions of one name (law 1), and a text parser on a value that never left Lean.

### B6. Follow uses nd's "client" exit for the attempt's `badReply` (DEBT, READ)

- `Machine.lean:1071`: `| some .badReply => .done CommandExit.client.code …`.
- `Command/Exit.lean:28`: `client` is "nd itself could not run the command (its argv, a socket, the
  workspace)".
- A reply that cannot answer its request is a different end that shares one code.

### B7. The continuation carries duplicate state (DEBT, law 1, READ)

- Phase 9's acc `[cb]` (`Machine.lean:1252`, read at `:1314`) duplicates the argv's `.cancel cb`. Phase 9 reads
  the acc copy and ignores the argv's.
- Phase 3's `ub` is compared with a re-plan, so it is a check, but phase 4's `k` keeps both `ub` and
  `callBytes c` (`:1295`). That is two encodings of one call, and it feeds D1's size.

### B8. Docstrings that lie about the code (DEBT, READ)

- `Protocol/Table.lean:423`: `stepsPerCommandMax` is "Steps one command may take before follow ends it with a
  refusal". Follow's `State` has no step counter. The bound is enforced in Rust (`client/src/run.rs:53,99`,
  `StepsExhausted`) and in the rows' harness (`Rows/Loopback.lean:643`). It is a table constant Rust consumes,
  which law 2 allows, but follow ends nothing.
- `Rows/Writer.lean:13`: "The one deviation is a plant (`Params.gateLog = false`)". `machine` and `pager` carry
  nine plants (`ignoreNotBefore`, `forgetSpent`, `admitsRecorded`, `unstatedExpiry`, `forgottenRefused`,
  `forgeBase`, `lieTip`, `lieBase`, `forgetJournal`).
- `Machine.lean:273-277`: `custodyPhase`'s docstring lists phases 1, 2 (init), 3, 5, 6 and 8. The code
  (`:279`) also has 9, the cancel signature.
- `Machine.lean:849-856` / `:22` (`inviteInput`): "checks that INPUT makes the member's own World". For a
  `.carried` input, `Invite.startOrigin` returns the STATED origin unchecked (`Invite.lean`, `startOrigin`), so
  the sponsor signs any carried fields whose stated origin matches. The import recomputes the origin later, so
  this is INFERRED harmless. The claim is still stronger than the check.

### B9. A wire name that is not the constructor's (DEBT, law 7, READ)

`Invite.lean:97`: `| .carried => "carriedWorld"`. Every other refusal's wire name is its constructor's.

### B10. A decoded field nothing reads (DEBT, READ)

`Thin.lean:54`: `Page.chain` is decoded (`:60`) and never read by `accept`. The World bytes carry the chain, so
the field is either redundant on the wire or should be compared.

### B11. `Use.uniq` evaluates `uniq xs` twice per element (DEBT, law 4, INFERRED)

`Use.lean:51-53`: `if x ∈ uniq xs then uniq xs else x :: uniq xs`. Unless the compiler shares the two calls, this
is exponential in the list's length. It is rows-only (`Act.used`) over ~20 calls today.

### B12. Output-rewrite plants (DEBT, READ; judged acceptable)

These plants rewrite the deployed machine's OUTPUT in the harness after the real `step` ran, rather than mutate
the deployed function:
- `rawSlots`, `dropRow`, `noReadLimit`, `flatProgram`, `dropDoc` (`Rows/Loopback.lean:944-990`);
- `pageIoFatal` (`:665-667`);
- `maskIncoming` (`:691-694`);
- `actOnBeforeLog` (`:945-950`).

Each shows that the row's expectation reads the printed text. Each expectation is exact (`prints`, `exact`, or a
refusal name), so the deployed regression each one models would move the same line. I counted every plant line
against its row (§5), and all of them land where the plant says.

---

## 4. The brief's questions, one line each

- **`atGenesis`:** yes, a step-0 World not built by this joiner's genesis passes. It is a World carried at
  height 0 (`carryWorld steps := c.height`), which a re-invited member holds. It is harmless (no object can be
  there) but contradicts PROTOCOL-67's critique. See Q1.
- **`settled`:** `ok` comes only from `ownSettle … = committed` of the `cb` that `k` holds (`settled_ok`). The
  other paths to exit 0 for a writing command are `cancel` on the Host's word (D2) and a swapped `k` (D3).
- **`badCall`:** at the deployed codec a non-canonical encoding does not decode. It is `badCall` at `receipt`
  and `eventMismatch` in a page, never admitted. Step 3's check is reachable only for non-`Fits` calls, and
  whether a plan can be one is open (Q2).
- **Check order:** a forged root is `headMismatch`, never `pathMismatch`, absent a `rootsDigest` collision. On
  the Foreign path `otherTx` is dead (Q3).
- **`forkedHead` replay:** same steps, same roots, same height is a no-op re-post. Older is `staleHead`. Benign
  (Q4).
- **The argv limit:** it covers the largest admissible call's confirm argv and the command frame. It does not
  cover the continuation echoed beside a page or beside the call (D1).

---

## 5. The rows: what each pins, and whether its plant moves (READ, counted by hand)

Each line below gives the row, its plant, and the 0-indexed line the plant names, with what happens there under
the mutation. Every one lands on the line it names, with the outcome it states (`plants_differ` checks only that
the outcome differs from the declared one). The `welcome` prefix is lines 0–5 and each `join` is 3 lines.

- `journey` · `openLog` 8: the stranger's read is served.
- `reopen` · `forgetJournal` 9: the retry is `absent`.
- `laws` · `skipJudge` 9: the sealed write is admitted.
- `rotate` · `advanceOnSend` 11: the probe cannot read, so `uncertain`.
- `audit` · `followVerifyAll` 13: a flipped signature byte is absorbed and caught at the page's chain.
- `paging` · `lieTip` 11.
- `coldCatchUp` · `unstatedExpiry` 10.
- `inflatedHeight` · `ignoreNotBefore` 10.
- `forgotten` · `forgottenRefused` 13.
- `refused` · `settleDecline` 13 (docstring stale, B3).
- `refusedFinal` · `admitsRecorded` 17.
- `invite` · `trustFirstUse` 14.
- `use` · `oneMember` 14.
- `describe` · `guessMethod` 7.
- `state` · `rawSlots` 6.
- `receipt` · `trustReceipt` 10.
- `settle` · `trustLookup` 1 (B4).
- `carry` · `importTrustsFile` 7.
- `carriedInviteWrongWorld` · `importTrustsFile` 7. The plant moves line 7 because `acceptCarried`'s pin becomes
  the file digest and skips the origin check (`Rows/Loopback.lean:342`). So it is a real tooth, though it reuses
  the carry row's mutation.
- `thin` · `forgeBase` 17.
- `thinStale` · `unstatedExpiry` 15.
- `seal` · `sealIgnored` 19.
- `basePin` · `lieBase` 11.
- `pageIo` · `pageIoFatal` 9.
- `wrongWorld` · `nonceRepeats` 7.
- `wrongWorldRead` · `nonceRepeats` 6.
- `pay` · `writerForgetsSpent` 4.
- `well` · `accountByAsset` 3.
- `bounty` · `skipJudge` 18 (`belowFloor`).
- `grain` · `skipJudge` 6.
- `hermes` · `resendFresh` 10.
- `bar` · `zeroDeadline` 0.
- `range` · `dropRow` 10.
- `rangeLimit` · `noReadLimit` 6.
- `bell` · `flatProgram` 10.
- `bellDoc` · `dropDoc` 9.
- `bigEvent` · `guessedBudget` 6.
- `wrongFollower` · `maskIncoming` 6.
- `uncertainHint` · `dropHint` 6.
- `rangeInvoke` · `staleRange` 10 (Q8).
- `rangeFlag` · `dropRange` 10.
- `beforeLog` · `actOnBeforeLog` 9.
- `cancel` · `cancelUndomained` 8 (caught by follow's phase-9 pre-check, D2).
- `cancelForged` · `followVerifyAll` 8.
- `lang-journey` is an `exe` row with an internal plant, not read.

Not pinned by any row:
- the frame total (D1);
- the cancel command's `ok` on the Host's word (D2);
- a swapped `k` (D3);
- follow's persistence (Q9);
- the deployed page budget (B2).

---

## 6. Files NOT read (or read only in part), with sizes

Not read:
- `Protocol/Command/Verb.lean` (442). I read only `argvSize` and the parse bound, `:234`, `:431`.
- `Protocol/Command/Describe.lean` (78)
- `Protocol/Command/Stdio.lean` (63)
- `Protocol/Command/Text.lean` (52)
- `Protocol/Proofs/Incoming.lean` (521)
- `Protocol/Proofs/Envelope.lean` (224)
- `Protocol/Proofs/Describe.lean` (140)
- `Protocol/Proofs/Invite.lean` (144)
- `Protocol/Proofs/Domains.lean` (167). I saw only the theorem names.
- `Protocol/Proofs/ReceiptWire.lean` (135)
- `Protocol/Proofs/Table.lean` (118). I read only `:105-116`.
- `Protocol/Proofs/Attempt.lean` (114). Theorem names only.
- `Protocol/Proofs/Use.lean` (87). Statements only.
- `Protocol/Proofs/Page.lean` (73)
- `Protocol/Proofs/Wire.lean` (68)
- `Protocol/Proofs/Exit.lean` (59)
- `Protocol/Proofs/Thin.lean` (52)
- `Protocol/Proofs/Stdio.lean` (49)
- `Protocol/Proofs/Frames.lean` (40)

Read only in part:
- `Protocol/Table.lean` (510): read 270–510.
- `Protocol/Invite.lean` (191): read 36–191.
- `Protocol/Proofs/Command.lean` (1417): read 1–520 whole, the remaining statements by grep plus
  `sendCancel_host`, `step_host_cancel`, `staleBehind_spec`, `step_persists_admitted` and `step_verified`.
- `Protocol/Proofs/Settle.lean` (500): statements, plus 296–500 whole.
- `Protocol/Proofs/Behind.lean` (376): `staleBehind_final` and `receive_pins` only.

Nothing was built or run. All verdicts above are READ or INFERRED, none MEASURED. D1's arithmetic is the first
thing a measurement should check.
