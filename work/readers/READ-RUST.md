# READ-RUST · nanodregg's Rust layer (client/ + launcher/), whole-file read

Reader: the RUST layer, 2026-10-24, nanodregg checkout at origin/main `f9657bd`. I edited nothing.
Tags: **READ** (path:line at f9657bd), **MEASURED** (a command I ran, named), **INFERRED** (my
reasoning from what I read; what would decide it is said).

## Verdict

I read every file of `client/src/` whole (run, attempt, stdio, sockets, frame, mux, custody,
fsx, join, lib, table, bin/nd, bin/nd-supervise, and generated.rs whole), every file of
`launcher/src/` whole except `bin/probe.rs` (head only) and the two emitted files (read where the
code uses them), the client tests the brief names (stdio, join, foreign, pin) and attempt.rs whole,
`launcher/tests/resident_bell.rs` whole, `launcher/tests/common/mod.rs` and `devtools/src/lib.rs`
for the teardown, plus the T0 Lean (`Protocol/Command/Machine.lean:960-1062`,
`Protocol/Attempt.lean`), CLIENT-24/25/27/29/30-34, and the runner (`gates/runs.py`,
`gates/readset.py`) for the leak. Law 2 mostly holds where it matters most: T0 (`e2905e7`) is real,
and I re-counted **16 Rust decision sites on the stdio leg, none of which can make a member or the
resident see `exit ok`**. Follow answers ok for a submitted call only when its own World settles it
committed (`Machine.lean:1051-1071`). The three worst things:
**(1)** An ordinary (non-rotation) attempt left open is never looked up again by anything. The
"next run looks it up" promise is in attempt.rs:18-21, Protocol/Attempt.lean:38/90/99, CLIENT-25
and CLIENT-27. Only `reconcile` ever calls `Attempt::load`, and only for an armed rotation. The
tests that "show" the next run drive `Attempt::load` by hand. So a re-run after `uncertain` or
`open` signs a NEW call beside the old one, which is the double-effect window the Lean docstring
names.
**(2)** The process model has no parent-death link anywhere in our own binaries. Teardown is
`Drop`-only. The 328/336 leaked processes are the test PROCESS dying without unwinding:
`runs.py:378` SIGKILLs only its direct child, through an `strace -f` that has no `--kill-on-exit`.
The reason CLIENT-29 gives for having no death signal ("no safe way, without `unsafe`") is false:
rustix 1.1.2, already a dependency with `process`, has a safe `set_parent_process_death_signal`.
**(3)** Several stated bounds are per-syscall, not per-reply, so a hostile peer can wedge where the
model allows only a crash-stop. `sockets.rs` bounds each `read()` by `replyMsMax`, not the reply,
so a trickling Host holds nd, and behind it the resident's serial `nd --stdio`, indefinitely.
keybroker's and nd-members' reads from their decider have no timeout at all. keybroker's
`UPSTREAM_TIMEOUT`, documented as "connect to last byte", is per read. Separately, `fsx`'s
"absent or complete-and-durable" claim is false for `create_once`, and an empty `rotation` file
from a crash at the wrong instant refuses every later command.

---

## 1. Law 2 on the stdio leg: the re-count (the brief's main question)

The criterion is IMPACT-E2 §1.2's: an accept, refuse, select or order decision, or a synthesized
reply, that is not a Lean definition, beyond byte transport, process lifecycle and key custody. For
each site the last column says whether it can change what the member or the resident SEES AS
SUCCESS (`CommandExit.ok`).

First the T0 check (READ). `Machine.lean:1051-1071` `settled`: on `result[0] = committed` it
answers `.done CommandExit.ok` only when `ownSettle X me w cb = some (.committed _ _)`. Here `cb` is
the call bytes step 3 put in the continuation and `w` is follow's current World. Anything else is
`attemptContradicted … "committed"`. `refused` is printed only on follow's own `refused`/`expired`.
`declined`, `open`, `contradicted`, `uncertain` and `badReply` map to non-ok exits whatever their
payload. So **R7 (`run.rs:292-314`) is a hint, as HOSTING-42's tcb row says.**

| # | site (READ) | kind | what Rust decides | can it make the member/resident see ok? |
|---|---|---|---|---|
| S1 | `stdio.rs:57-60` | refuse + synthesize | op ≠ COMMAND, or not a `Command`: `refused undecodable` | no (exit refused) |
| S2 | `stdio.rs:61-67` | refuse + synthesize | argv[0], decoded **lossy** UTF-8, not in `STDIO_VERBS`: `refused notOnSurface WORD` | no. The list is emitted; the RULE ("first word only", lossy decode) is Rust's. `Stdio.lean:7` states it as prose and no Lean definition exists |
| S3 | `stdio.rs:68-75` | order | connects follow.sock and then host.sock for EVERY verb before follow sees the command; either failure ends exit `client` | no |
| S4 | `stdio.rs:76-87` | synthesize | every `RunError` becomes exit `client` with `nd: {Display}` text (Debug-formatted custody names, `custody.rs:72`) | no |
| S5 | `stdio.rs:106-108` | select | a hang-up frame is skipped, but a request already forwarded for that connection still RUNS to completion (submits included) | no, but see F1: a resident that timed out and retries next tick has two commands in flight, serially |
| S6 | `run.rs:191-209` | order + synthesize | an armed rotation's attempt is driven before every command; `contradicted` → a Rust-built `Done(hostContradicted, "", "hostContradicted … (attempt DIR)")` (`:203-205`); every other unsettled end is swallowed (`:207 _ => {}`) | no (exit 55). Reachable from stdio only when another nd armed a rotation on the workspace |
| S7 | `run.rs:118-130` `hint` | select | status byte → `Seen`, a hand-written map; `closed` and any unnamed status → `Lost` | no (only steers `Attempt.next`) |
| S8 | `attempt.rs:51-65` `Receipt::read` | accept | follow's nested `receipt CALL` stdout is a verdict only if it is exactly three lines with the hand-typed prefixes `receipt `/`head `/`settle ` | no for the member. It does drive custody's key advance and the `settled` file (S11) |
| S9 | `attempt.rs:224-296` `drive` | select + order | the loop around `Attempt.next`: the latched receipt (`:245`), the fuel `3·sendsMax+1` ending `Uncertain` (`:242,:291`), each end's payload (`:259-268`), the hint bound (`:287`) | no |
| S10 | `run.rs:292-314` (R7) | synthesize follow's input | the end → step 4's result | **no since T0** (above) |
| S11 | `run.rs:295-297` | order | custody `settle(committed)` advances the KEYS on S8's parse BEFORE follow's step-4 `ownSettle` check runs | no for exit ok, but it is one fact decided in two places, in Rust's order (F9) |
| S12 | `run.rs:241-243, 281, 322-327` `nested` | refuse | a `receipt` inside an attempt that asks to rotate or submit is an error, mapped to `Lost` by `receipt()` | no |
| S13 | `run.rs:275-279` | select | a Host transport failure on a plain `host` step ends the command exit `client` and is never handed to follow as a result | no |
| S14 | `run.rs:240, 319` | refuse | `stepsPerCommandMax` exhausted → `StepsExhausted` → exit `client` | no |
| S15 | `sockets.rs:72-85` `step` | refuse | follow status ≠ ok → io error (`closed` named) → exit `client` | no |
| S16 | `nd-members.rs:499-520, 608-615` (R9) | order | the stdio pair starts only after the follower answers an empty command | no (the resident sees `.error`) |

Two sites look like decisions but are not live:
- `sockets.rs:94-99`, the `argvBytesMax` check, **cannot fire**. The generated `Command::encode`
  (`generated.rs`, `layout::Command::encode`) already returns `Err(PastBound)` whenever
  `out.len() > 132096 = ARGV_BYTES_MAX`, so every payload that reaches `:94` is within the bound.
  That is a dead check with a live-sounding refusal text (F18).
- `custody.rs:79-93` (`CustodyError` → emitted `CustodyRefusal`) is custody's own mapping, which
  law 2 allows.

**Count: 16, against IMPACT-E2's 9.** The difference is S3, S5, S11, S13, S14, S15 and the dead
`argvBytesMax` check. None of the new ones yields ok. **What the member or resident sees that Rust
chose:** the exits `client`, `refused` (S1, S2) and `hostContradicted` (S6); free text in stderr
built from Rust `Display`/`Debug` (S4, F14); and the key advance ordering (S11). The one Rust gap
that can produce TWO successes for one intent is not on this table, because it is an absence, not
a branch: F1.

---

## 2. Findings, ranked

### DEFECT

**F1. An open or uncertain ordinary attempt is never looked up again.** DEFECT. READ.
- `client/src/attempt.rs:18-21`: "Every other end (declined, open, contradicted, uncertain,
  badReply) leaves the attempt open on disk, so the next run looks it up again."
- The same promise is in `Protocol/Attempt.lean:38` ("the next run starts from 'sent, outcome
  lost' and looks up again"), `:90`, `:99`, CLIENT-25 ("the next run looks it up") and CLIENT-27
  ("Every other end is OPEN on disk").
- What the code does: `Attempt::load` has exactly one caller in `client/src`, `run.rs:195` inside
  `reconcile`. That caller loads only `attempts/<n>` for the `n` an ARMED ROTATION names
  (`run.rs:191-195`). Everything else in `command` only creates attempts: `fresh()` at
  `run.rs:353-365` computes max+1, and `Attempt::freeze` at `:283`.
- So for every non-rotation call, `attempts/<n>/` is a write-only record. The next `nd` (or
  `nd --stdio`) command freezes `attempts/<n+1>` with whatever NEW call follow plans on its
  current World.
- Why it is wrong: the Lean docstring says the open end exists because "running the command again
  would sign a NEW call that could land beside this one" (`Attempt.lean:21-23`). CLIENT-27's
  defect 2 says the same ("a re-run signs a NEW call, so both commit"). The client's restart-class
  exits (`uncertain` 2, `declined` 53, `open` 54) and the resident's `deliverP` ("any other exit →
  retry next tick", IMPACT-E2 §1.1 row 14) are exactly re-runs. Nothing ever settles the old
  attempt, and `nd cancel CALL` (090b164) needs the member to dig the hex out of
  `attempts/<n>/call` by hand.
- The input that shows it: a `transfer`/`write`/`invoke` whose submit reply is lost
  (`sockets.rs` timeout, or a `closed` from the mux). nd exits `uncertain`, and the member or
  resident runs it again. If any other Turn landed in between, the World moved and follow plans
  different bytes, so the old frozen call and the new one can both commit. INFERRED: what decides
  it is whether follow's re-plan is byte-identical on an unmoved World, so that the journal dedups.
  It cannot be identical on a moved one. The Bell is protected only by its own
  `rung: answered` guard (resident_bell Q3).
- Why the tests stay green:
  - `client/tests/attempt.rs:340-355` (`declined_leaves_the_attempt_open_and_the_next_run_looks_up`)
    and `:194-212` (`lost_reply_is_uncertain_and_only_looked_up`) perform the "next run" themselves
    with `Attempt::load(&d)` + `drive`.
  - No test runs `run::run` twice over one workspace with a non-rotation attempt open.
  - Deleting the (non-existent) resume path changes no test.
  This is the "plant that tests its own reconstruction" class.

**F2. No process we spawn dies with its parent. Teardown is `Drop`, and `Drop` did not run.**
DEFECT (harness and deployment). READ for the code, INFERRED for the exact kill.
- The parts:
  - The sandbox gives `--die-with-parent` to the CONFINED grandchild only (`sandbox/src/lib.rs:435`,
    Linux). macOS `sandbox-exec` has none (`:378-424`).
  - nd-supervise, nd-members, keybroker and grain-launch are started unconfined: by the tests
    (`devtools/src/lib.rs:222-245`, `launcher/tests/common/mod.rs:619-636, 866-875, 1124-1149`) and
    by nd-members (`nd-members.rs:666-672`, plain `Command::new(&conf.supervise)`).
  - None of them sets a parent-death signal, and none handles SIGTERM except nd-supervise. nd-members'
    orderly end (`nd-members.rs:272-281`: stop pairs, drain `stopping`, kill the decider) runs only
    when `serve` returns, which is only on the decider's end.
- The teardown is `Supervisor::drop` (`devtools/src/lib.rs:204-210`: SIGKILL by handle),
  `Members::drop` (`common/mod.rs:1101-1114`: SIGKILL nd-members, then every pid in PIDS),
  `Broker::drop` (`:666-672`), `Logged` (a `Supervisor`), `World::drop` (`:530-533`) and
  `Scratch`/`Short`/`Gone`. Inside one test process this is complete on Linux. I traced it for
  `resident_bell`: grain-launch's, keybroker's and nd-supervise's confined children all have
  `--die-with-parent` on parents that the drops SIGKILL. It is also complete on a test panic,
  because unwinding drops the locals.
- **Why it did not run:** `Drop` runs only if the test process unwinds.
  - `gates/runs.py:378` runs every row as `subprocess.run(argv, …, timeout=DEADLINE)` (600 s;
    a row past it is re-run once, `runs.py:66-67`). On timeout Python SIGKILLs only its DIRECT
    child.
  - When tracing is on, that child is `strace -f` (`gates/readset.py:83-86`, with no
    `--kill-on-exit`), so the tracees are detached, not killed. Without tracing the child is cargo,
    and the test binary is cargo's child.
  - Either way the test binary and its whole tree live on with closed pipes. The test binary dies
    later, without unwinding the test threads: libtest's next write to a closed stdout panics the
    main thread, which ends the process. Or it hangs forever.
  - Every nd-supervise, keybroker, nd-members and grain-launch it held is then orphaned, and each
    keeps its own confined child alive, because that child's parent did not die.
  - The same holds for `KILLED(load)` (earlyoom/cgroup SIGKILL of the test binary, `runs.py:74`)
    and for a Ctrl-C.
  - This matches cv 01a16b44's inventory: nd-supervise, host, keybroker, nd-members,
    hosting-broker and nd-bwrap under `~/.cache/nd-t`, 4–5 days old. A timed-out row re-runs once,
    so it leaks twice.
  - What would decide the exact path: the gate log of the leaking run (an `UNREAD(timeout` or
    `KILLED(load` verdict on a cargo row from `main/.git/nanodregg-gate-3` or `wt/client`).
- **The stated reason is false.** CLIENT-29's CRITIQUE (decisions/client.md, the "Shared fate"
  bullet) says "There is no safe way, without `unsafe`, to give them a parent-death signal".
  rustix 1.1.2, pinned (`Cargo.lock:523-524`) and enabled with `process` in client and launcher
  (`client/Cargo.toml:23`, `launcher/Cargo.toml:36`), exports
  `rustix::process::set_parent_process_death_signal(Option<Signal>) -> io::Result<()>` as a safe
  function (`~/.cargo/registry/src/…/rustix-1.1.2/src/process/prctl.rs:66`, READ). Each of OUR
  binaries can call it on itself in `main`, with the usual `getppid()` race check after the call.
  No `pre_exec` is needed.
- Caveat (INFERRED): PDEATHSIG fires on the death of the parent THREAD. For a test that spawns on
  one thread and keeps the child past it, that is a design point, not a blocker.

**F3. `sockets.rs` bounds each read, not the reply: a trickling Host or follow wedges nd.**
DEFECT (a wedge where the model allows a crash-stop). READ.
- `sockets.rs:28-29`: "One request, one reply, each bounded by `replyMsMax`". `connect`
  (`:45-50`) sets `SO_RCVTIMEO`/`SO_SNDTIMEO` to `REPLY_MS_MAX` (120 s), and `frame::read` →
  `fill` (`frame.rs:72-83`) loops `read()`. That bounds every SYSCALL at 120 s. A peer that sends
  one byte every 119 s keeps one frame (up to 262 144 bytes) alive for about a year.
- The mux knows the difference and enforces a whole-frame deadline (`mux.rs:337-352` `Deadline`,
  `FRAME_MS_MAX`). The client's reader of the HOST does not, and the Host is the party PROTOCOL-46
  says not to trust.
- `nd --stdio` serves requests strictly in order (`stdio.rs:92-117`). One wedged command blocks
  every later request of that resident. The mux closes the resident's own connection
  `replyTimeout`, but the child stays stuck.
- Mutation/input: a host.sock endpoint that answers a submit with a frame header and then one byte
  per 100 s. Today nd never returns. A deadline per reply would return `timeout` → `Lost` →
  `uncertain`.
- Scope (INFERRED): the deployed hosted host.sock is the local writer's nd-supervise, whose writes
  are whole and bounded (`mux.rs:171-175`). The exposure is the remote host.sock of CLIENT-12 and
  a buggy local follow.

**F4. The decider reads in keybroker and nd-members have no timeout. A silent decider wedges both
forever.** DEFECT (liveness; law 7 "every way it ends is a name"). READ.
- `launcher/src/residents.rs:13-21` (`ask`) does `read_frame(dout)` with no deadline.
- keybroker holds the decider `Mutex` across that read (`keybroker.rs:536-540`, and
  `ask_once` `:668-675`, `reply` `:723-729`). The tick and every resident's ask then block behind
  it.
- nd-members calls `ask` on its only thread (`nd-members.rs:335`).
- The `ENDING_TICKS` logic (`nd-members.rs:336-342`, `keybroker.rs:445-456`) runs only when `ask`
  RETURNS `None` (EOF, a wrong verdict). It never runs for a decider that is alive and silent:
  stuck on a Store read, SIGSTOPped, or one that wrote half a frame.
- Input: a stub decider that reads the `residents` frame and sleeps. Today keybroker never ends
  and never names it, and every `broker.sock` ask hangs. The existing plants
  (`broker.rs a_decider_that_never_ran_its_own_end_…`, `members.rs nd_members_ends_by_name`) use
  deciders that EXIT. QUESTION within it: what bound Lean's decider guarantees per answer. If it
  has one, it should be the emitted deadline.

**F5. `fsx` promises crash atomicity that `create_once` does not have. An empty `rotation` refuses
every later command.** DEFECT (crash-only; a wedge after a crash-stop). READ.
- `fsx.rs:1-3`: "a crash leaves it either absent or complete-and-durable". `write_new`
  (`:47-55`) is `open(O_CREAT|O_EXCL)` → `write_all` → `fsync`, in place, with no temp file and no
  rename.
- A process killed after `open` and before `write` (an OOM kill, the gate's SIGKILL, a power loss
  before `fsync`) leaves the file present and empty or short.
- For `custody.rs:530-536` `arm` → `ROTATION` (72 bytes): `armed()` (`:539-550`) reads it with
  `read_private(…, 72..=72)`. An empty file is `Refused::Length` → `CustodyError::File`, and
  `reconcile` (`run.rs:191`) runs FIRST in every `run`. So every later `nd` command, `nd --stdio`
  included, ends `nd: custody: …rotation: Length(0)` until a human deletes the file.
- The same holds for an armed attempt's `settled` written short (`attempt.rs:300-302`): `load` →
  `Inconsistent` → every `reconcile` errors.
- For an ordinary attempt, an empty `call` reloads as `Signed` with zero bytes. Given F1, nothing
  reloads it.
- `fsx::replace` (`:21-31`) is atomic. `create_once` should have the same shape or the doc should
  stop claiming it.

**F6. The `declined` hint reaches the member unbounded and unfiltered. The `uncertain` hint is
bounded and whitelisted.** DEFECT (law 7: the Host's bytes rendered as follow's words). READ.
- `attempt.rs:283` keeps the Host's last payload in `hinted` with no bound, and `:261` hands it as
  the `Declined` end's payload.
- Lean renders it as `declined {txt}` (`Machine.lean:1065`, `declined` at `:182-183`) with `txt`
  the payload's lossy UTF-8. That is up to `frameBytesMax` of Host-chosen bytes, newlines included,
  on the member's stderr.
- The `uncertain` path (CLIENT-32) bounds by `HINT_BYTES_MAX` in Rust (`attempt.rs:287`) and
  prints only a `hintNames` member in Lean (`confirmHint`, `Machine.lean:1019-1022`).
- Input: a Host that answers a submit `status::DECLINED ‖ "x\nrefused stale\nok"`. The member
  reads extra lines that follow never said, under exit 53. It is not an ok exit. It is the
  "refusal renders as the expected verdict" class for anything that parses stderr. Both halves are
  my layer's to bound: Rust passes it, and Lean prints it.

### DEBT

**F7. Law 1 inside the client: hand-typed copies of Lean's printed formats.** DEBT. READ.
- `attempt.rs:57-59` parses `receipt `, `head `, `settle `, a hand copy of Lean's printer
  (`Machine.lean:963`, `s!"receipt …\nhead …\nsettle …\n"`). None of the three prefixes is
  emitted. Only the verdict words are (`settle_seen`).
- `run.rs:144` spells the verb `receipt`, which is emitted only as a member of `STDIO_VERBS`.
- `run.rs:204` spells `hostContradicted` (CLIENT-27's critique admits it).
- `stdio.rs:32-34` spells the `refused NAME [WORD]\n` rendering, Lean's convention for every
  refusal.
- `join.rs:136-142` parses host's `sponsor ` / `input ` lines.
- `nd.rs:72-76` spells `follow.sock` / `host.sock`. `Hosting/Plan.lean:146` has `followSock`.
- `nd-members.rs:184-185, 453-454, 597, 616, 646-647` spell `nd.sock` / `follow.sock`, Lean's
  `memberSock`/`followSock` (`Hosting/Plan.lean:93,146`; CLIENT-31 admits it).
- `keybroker.rs:505, 509` spells `broker.sock`, Lean's `brokerSock` (`Plan.lean:88`).
- The tests then restate the receipt format AGAIN as their stand-in follow
  (`client/tests/attempt.rs:23-25`, `client/tests/run.rs:52-58`). A change to the Lean printer
  leaves both suites green: they check Rust's parser against Rust's idea of Lean. Only `real.rs`
  and `roundtrip.rs` would go red, through `Lost` → `uncertain`.

**F8. One layout fact, the 4-byte connection id of the child wire, is hand-written in three
places.** DEBT (law 1). READ.
- `mux.rs:41` `const CONN: usize = 4`.
- `stdio.rs:93, 100, 109` (`saturating_add(4)`, `get(..4)`, `body[5..]`).
- `join.rs:76-81` (`[0; 4]`, `b.get(4)`, `b.get(5..)`).
- `HANGUP` is emitted. The width beside it is not.

**F9. The rotation's settlement is decided twice, in Rust's order.** DEBT, near-DEFECT. READ.
- `run.rs:294-297`: custody `settle(committed)` (the keys advance: `custody.rs:554-564`) runs on
  S8's parse of the nested receipt BEFORE follow's step 4 runs `ownSettle` on the same call
  (`run.rs:317`).
- On reload, `Attempt::load` recomputes `committed` from the receipt's `seen`
  (`attempt.rs:202`, `final_of`). In-run, `settle` writes it from `end == Action::Committed`
  (`:246`). That is two derivations of one bit.
- They agree while `Attempt.next` and the receipt agree, and while follow's World does not move
  between the nested receipt and step 4. If follow then answers `hostContradicted` (call bytes
  that do not decode as follow's, a World that moved), custody has already advanced.
- What would decide it: a row where the nested receipt says committed and step 4's `ownSettle`
  disagrees. I found none.

**F10. `client/DESIGN.md` describes the old attempt store, the one CLIENT-27 deleted as a
lockout.** DEBT (a design doc that lies about the safety property). READ.
- `DESIGN.md:58`: "the Host's settlement is one file, `committed` or `not-committed`". `:59-60`:
  "Classification of a reply is the Host's status byte". The code refuses that layout by name
  (`attempt.rs:306-319`, `tests/attempt.rs:303`), and PROTOCOL-46 says the Host never settles.
- Other stale lines:
  - `:17` "spawns nothing" (`nd --join` spawns host, `join.rs:121-159`);
  - `:18` "6 ops" (5 host + 2 follow);
  - `:46` "five step tags" (seven);
  - `:51` "One 32-byte seed file" (three custody shapes);
  - `:77` "no refusal names" (`stdio.rs` renders them);
  - `:86` "the ceiling for client/src is 2,000 lines" (CLIENT-32: 2528);
  - `:7` "CLIENT-1..7".

**F11. CLIENT-29 no longer matches nd-members.** DEBT (law 10). READ.
- The decision gives the argv as `nd-members MEMBER MEMBERS FOLLOW PIDS …` and the follower Store
  as `MEMBERS/<name>/store` with `MEMBERS/<name>/follow`. The code takes STATE as its third
  argument (`nd-members.rs:1, 123-138`) and uses `STATE/<name>/store` and `STATE/<name>/follow`
  (`:442-448, 600`), which is HOSTING-32's layout.
- The decision still says `fdLimit … = 71`. It is 73 since CLIENT-30.
- The CRITIQUE bullet "The stdio child may write the follower's Store" is stale: STATE is now
  `--hide` for the stdio child (`:636`).
- The "no safe way … parent-death signal" sentence is false (F2).
- CLIENT-29 carries an "Amended (CLIENT-30)" line but no HOSTING-32 amendment.

**F12. nd-members' restart constants are hand copies, and their comment names a deleted unit.**
DEBT (law 2: "never hand-copied constants"). READ.
- `nd-members.rs:60-63`: "nd-member@'s RestartSec, StartLimitBurst and StartLimitIntervalSec" →
  `RESTART_AFTER = 2 s`, `STARTS_MAX = 5`, `STARTS_WINDOW = 120 s`. nd-member@ was deleted by
  CLIENT-29. The live values are Ops/Units.lean's rendering (`deploy/units/linux/*.service`
  `RestartSec=2`, `StartLimitBurst=5`, `StartLimitIntervalSec=120`, READ), not emitted into Rust.
- `TICK` (200 ms) is spelled separately in nd-members (`:55`) and keybroker (`keybroker.rs:80`).
- keybroker's other bounds are not emitted: `UPSTREAM_TIMEOUT`, `RESIDENT_IDLE`, `RESPONSE_MAX`,
  `KEYFILE_MAX`, `ANCHORS_MAX`, `PINS_MAX` (`:65-77`).
- IMPACT-E2 §1.2 recorded the first three. They are still there.

**F13. "A signal death is a code ≥ 128" is stated three times, twice without the platform rule.**
DEBT (law 1). READ.
- `sandbox/src/lib.rs:222-226` `killed_by_signal` is Linux-conditioned: on macOS a code ≥ 128 is
  NOT a signal.
- `launcher/src/residents.rs:36-44` (`c >= 128 → Signaled`) and `grain-launch.rs:387-395` and
  `:113-116` restate it unconditionally.
- nd-supervise uses the sandbox's (`nd-supervise.rs:156`). The launcher does not.

**F14. nd's own refusals print Rust `Debug`, not names.** DEBT (law 7). READ.
- `custody.rs:65-75`: `Display` falls back to `{e:?}` (`custody: NoPending`, `File(p, Dir(…))`
  → `custody: …: Dir(…)`).
- `join.rs:55, 47-50` prints `key file: {r:?}` and `{name}: {r:?}`.
- `sockets.rs:24-26` prints `{what}: {r:?}` for a layout refusal.
- The tests pin the Debug spelling: `tests/join.rs:192` `contains("key file: Dir(")`, `:241`
  `contains("invitation: Mode(")`, `:246` `contains("Dir(")`. Renaming a Rust enum variant reds a
  test, but no emitted name exists for these.

**F15. `fresh()` lists the whole `attempts/` directory on every submit, and `attempts/` has no
bound.** DEBT (law 4: a static bound on everything; law 5: no O(store) on the request path).
READ.
- `run.rs:353-365` reads every entry of `attempts/` to compute max+1, on the submit path.
- Nothing prunes `attempts/`. Given F1, nothing settles most of it either.
- A resident answering rings for a year accumulates one directory per call, and each submit is
  O(calls ever made). No `Bounds` entry names it.

**F16. Test comments that claim checks the tests do not make.** DEBT. READ.
- `client/tests/foreign.rs:352-354`: "once B's head advances to it, it checks (the first
  acceptance already stands: refused as a second acceptance, not as a receipt)". It is followed
  only by the head post (`bf.ok(["invoke", &h, "1", …])`). The accept of `r_later` is never
  re-run, so neither "it checks" nor "refused as a second acceptance" is asserted.
- `client/tests/foreign.rs:237-238`: `forge` documents "at 2, the low byte of the stated commit
  height", but the call is `forge(&r, 3)` (`:310`). Hex digit 3 is the low nibble of the height's low byte, and digit 2 its high nibble, so the same
  byte is forged either way. It is harmless, but the comment does not describe the call.
- `client/tests/pin.rs:1` cites CLIENT-33 (Test scratch) for `--pin`, which is CLIENT-35.

**F17. Weak refusal assertions.** DEBT. READ.
- `client/tests/foreign.rs:342` X1b ("one receipt, one acceptance") asserts only
  `!o.status.success()`. It stays green for `uncertain`, `client`, a transport failure, any
  refusal. It would catch an ADMIT, since exit ok is red. It would not catch "refused by the wrong
  rule".
- `stdio.rs:251` (`assert_ne!(rep.exit, OK)` for the canary install) is the same shape, but there
  the property is "the canary bytes never appear", which is asserted.
- X2, X2r, X2h, X3, X3b and X5 use `contains(NAME)` over stdout+stderr: a name, but a substring
  over both streams. A hint line carrying the name would satisfy them.
- Everything else I read asserts the exact name and exit. Examples: `stdio.rs:225-229`
  (`(REFUSED, "refused notOnSurface VERB\n")`), `join.rs:170, 184`, `pin.rs:143-170`, bell Q3
  (`(1, "refused lawDenied")` + the guard's hint).

**F18. Dead check: `sockets.rs:94-99` (`argv: pastBound argvBytesMax`).** DEBT ("a check that
cannot fail"). READ.
- See §1. The emitted encoder refuses first, with `malformed("argv", PastBound{…})`, a Debug
  string and not Lean's `argvPastBound`.
- Mutation: delete `:94-99`. No input changes behaviour and no test reds.

**F19. keybroker re-decides `keyMissing` after Lean has already charged.** DEBT (law 1/2). READ.
- `keybroker.rs:689-691` refuses `KeyMissing` when a `Grant`'s slot is not in the key file.
- The Grant carries `charged` (dropped by the `..` at `:680-688`). Lean was told the slots at
  start precisely "so Lean refuses `keyMissing` before it charges anything" (`:22-23`).
- If the Rust arm is ever reached, the allowance is charged for a call never made. If it is never
  reached, it is a twin.

**F20. `UPSTREAM_TIMEOUT` is documented as a whole-call bound and is a per-read bound.** DEBT (a
comment that lies, F3's class). READ.
- `keybroker.rs:70` "How long one upstream call may take, connect to last byte". `:791-793`
  connect timeout plus `set_read_timeout`/`set_write_timeout` per syscall.
  `read_to_end` (`:821-827`) can take `RESPONSE_MAX` × 120 s.
- The resident's socket is `busy` for all of it (`:622-625`). The upstream is pinned
  (HOSTING-28), so the exposure is a slow provider, not a stranger.

### QUESTION

**F21. The mux closes a pipelining peer `replyBacklog` by a scheduling race.** QUESTION. READ.
- `mux.rs:461-469`: a reply whose connection's `slot` is still set is a backlog close. The slot is
  cleared only when the writer thread RECEIVES the previous reply (`:323`).
- A peer with two requests in flight whose replies arrive back to back is closed `replyBacklog` if
  the writer has not been scheduled between them, even though the peer is reading.
- Every deployed peer is strictly request-reply per connection: nd, the resident's `Sockets.lean`
  (one connection per command), nd-attach (I did not read it). Then this is unreachable.
- What would decide it: whether PROTOCOL allows pipelining on a member or host socket. If it does,
  the backlog rule needs "more than one reply QUEUED", not "one not yet taken".

**F22. `GRACE` (90 s) vs the unit's `TimeoutStopSec=10`.** QUESTION. READ.
- `nd-members.rs:66-68` derives `GRACE = 3 · reply_write = 90 s` for a stopping supervisor.
- `deploy/units/linux/nd-members@.service` sets `TimeoutStopSec=10`. Under a unit stop, systemd
  SIGTERMs the whole control group (each nd-supervise names its closes itself, CLIENT-30) and
  SIGKILLs at 10 s.
- nd-members has no SIGTERM handler, so its own drain (`:273-279`) never runs there.
- Is 10 s the operator's deliberate bound (then CLIENT-30's "each within `reply_write`" does not
  hold at a unit stop), or an unpriced default?

**F23. `nd --stdio` runs a request whose connection already hung up.** QUESTION. READ.
- `stdio.rs:106-108` skips only the hang-up frame itself. A COMMAND the mux already forwarded runs
  to its end, submit included, after its resident gave up (`replyTimeout` at 120 s, `mux.rs:378`).
- The resident retries at its next tick, which is a second command for one intent, serialized
  behind the first. With F1 that is two calls.
- What would decide it: whether the child wire's hang-up was meant to CANCEL queued requests of
  that connection (PROTOCOL-23 names only "owed to the child as a hang-up").

**F24. The stdio surface rule is Rust's.** QUESTION (law 2). READ.
- `stdio.rs:61-67` decides "argv[0] only, lossy UTF-8, exact match against the emitted list". Lean
  has the list and the theorem `mem_stdioWords_iff`, but the SCREEN is not a Lean definition
  (`Stdio.lean:7` states it as prose).
- R1 in IMPACT-E2 makes the same point. It is unchanged at f9657bd. Not a success path (exit
  refused), so this is the brief's "hint" class. I list it because it is a refusal Rust both
  decides and renders.

---

## 3. The supervisor and the launcher's process model (the brief's second question)

Who starts whom (READ), and what stops each:

| process | started by | confined? | death tied to parent? | stopped by |
|---|---|---|---|---|
| nd-supervise | service manager / nd-members (`nd-members.rs:666`) / tests (`devtools/src/lib.rs:229`) | no | **no** | SIGTERM handler (`nd-supervise.rs:123-136`, CLIENT-30) or SIGKILL by handle |
| its child (`host`, `nd --stdio`) | nd-supervise via `sandbox::command` | yes | Linux: `--die-with-parent`; macOS: no (EOF on stdin ends a well-behaved Lean child) | nd-supervise's `child.kill()` |
| nd-members | systemd / tests (`Members::spawn`) | no | **no** | systemd's cgroup; tests: SIGKILL + PID files (`common/mod.rs:1101-1114`) |
| its decider | nd-members (`:250-257`) | yes | Linux: yes | `stop()` (`:285-291`) on a normal end only |
| keybroker | systemd / tests (`start_residents`) | no | **no** | systemd's cgroup; tests: SIGKILL by handle (`Broker::drop`) |
| hosting-broker | keybroker (`:392-399`) | yes | Linux: yes | keybroker's kill on its ends |
| grain-launch | systemd / tests (`Logged`) | no | **no** | systemd's cgroup; tests: SIGKILL by handle |
| controller, grains | grain-launch (`:431, :231`) | yes | Linux: yes | `stop_all` (`:287-293`) |

- PID files exist for every child (nd-members `PIDS/<name>.<role>.pid` and `decider.pid`;
  keybroker `PIDS/decider.pid`; grain-launch `PIDS/<grain>.pid`; tests `SOCK.pid`,
  `nd-members.pid`, `member-stdio.pid`).
- Two PID-file windows (READ):
  - nd-members writes the file AFTER spawn (`nd-members.rs:673-676`, `keybroker.rs:400`,
    grain-launch `:241`). A SIGKILL between spawn and write leaves a child no PID file names.
  - devtools writes `SOCK.pid` inside `Supervisor::hold`, after the spawn.
- The teardown and why it did not run are F2.
- In one sentence: a supervisor tree whose root is killed with SIGKILL leaks every unconfined
  level, and in tests the root is the test binary, which the gate kills without unwinding.

---

## 4. The tests: what each asserts, and whether it would stay green under an admit

READ for the files named. "Admit" means the mutation "the kernel admitted instead of refusing".

- **client/tests/stdio.rs**: exact `(exit, stderr)` for seven off-surface argvs and two
  undecodables. The served write is checked by reading back the object. The custody fence is
  checked by `contains("noRotation")` plus `keys` still 64 bytes (no pending minted). An admit is
  red everywhere.
- **client/tests/join.rs**: exact `refused inviteRefused pinMismatch\n` / `…notSponsor\n`,
  nothing written (`unwritten`), the joined World's origin/sponsor/input equal to the sponsor's,
  the kept files' mode, the joiner's write served, and `adopt`'s `notSponsor`/`notBehind` exact.
  The chain-rule refusals pin Rust Debug text (F14). An admit is red.
- **client/tests/foreign.rs**: X1 counts the acceptance rows (one). X2/X2r/X2h/X3/X3b/X5 use
  `contains(NAME)` (F17). X1b is exit-only (F17). An admit is red for each, because every check
  includes `!success()`. The "advances to it, it checks" step asserts nothing (F16).
- **client/tests/pin.rs**: exact `refused program\n` plus the method's name on stdout
  (`unread`, `grantDead`, `scan: refused grantDead`), and exact `refused badKey\n` /
  `refused unknownRelation\n`. An admit is red. This is a good file.
- **client/tests/attempt.rs**: the emitted `next` driven by scripted replies, with exact `State`
  values and request sequences. It cannot see a Lean/printer drift (F7). Its "next run" is the
  test's own (F1).
- **client/tests/run.rs** (read in part): a scripted follow and host, with exact exits, custody
  keys, and armed/unarmed state. A `T` table of test values (`:14-27`, "not the protocol's"). The
  receipt stand-in duplicates the printer (F7).
- **launcher/tests/resident_bell.rs**: Q1–Q7 and the mutations assert names
  (`(1, "refused lawDenied")` + `rung: answered`; `refused program`; `answerRefused program`,
  `answerRefused grantRight`; `bellShape notBell`; `argvNotPlan …` exact), counts of provider
  requests, and the rows read back. An admit is red at Q3, Q4 and both mutations.
  `PATIENCE = 2048` (`:84`) is a hand copy of the Bell's `(patience 2048)`. It is guarded, since a
  changed patience reds Q7's retire, but it is a twin.

**resident_bell's 218 s: how much is waiting vs measuring** (READ + MEASURED-by-others):
- 1eae61f's message reads "resident_bell GREEN 218.44s", with "Q7 adds about 135 s to the row"
  (its decisions/hosting.md text).
- Before Q7 the row was 71.08 s (CX-OPS.report.md:9, MEASURED on hbox by CX-OPS at 892647d).
- Q7's 135 s is **2048 sequential `nd write` commands** (`resident_bell.rs:589-592`), each a
  process spawn, a submit and a nested confirm, only to move the height past the Bell's patience.
  That is world-building, about 66 ms per write, and it measures nothing.
- The race section waits on the controller's crash-loop window: `RESTART_WINDOW_MS = 60000`
  (`launcher/src/generated.rs:6`). The row asserts `waited ≥ RESTART_WINDOW_S / 2` (`:873-877`)
  and waits until the grain starts on the window's passing (`:866-871`). So at least 30 s, and
  INFERRED about 60 s, is a timer.
- `next_window` (`:397`, common `:814-826`) waits up to one 3 s broker window.
- **Estimate (INFERRED from those numbers):** of 218 s, about 135 s is height padding, about 55-60
  s is the crash-loop timer, and about 20-25 s is everything Q1–Q6 and the mutations actually
  exercise. Roughly 90% of the wall clock is waiting or padding.
- What would turn it into measurement: a test-only patience, or a Bell instance with a small
  patience installed beside the shipped one. Both are LANG's to judge, because the shipped Bell is
  what the row is for. A window constant the test can lower is HOSTING's.

---

## 5. generated.rs, law 1, and hostile bytes

- **Is `client/src/generated.rs` ever hand-edited?** The header says "do not edit"
  (`generated.rs:1-3`). `gates/generated.tsv` pins it to `emit-rust --check`, as it does
  `launcher/src/generated.rs` and `broker_generated.rs`. The last 15 commits that touch it each
  also touch `Emit/`, `Protocol/` or `Host/`, the sources of its tables (MEASURED: `git log -15 --
  client/src/generated.rs` with `--stat`). I did NOT re-run the emitter: the local
  `.lake/build/bin/emit-rust` is from 10-16, so a check with it would be against a stale emitter.
- **Hand-written duplicates of emitted or Lean facts:** F7, F8, F12, F13, F18, F19, and
  `grain_name_ok`'s character class (`launcher/src/lib.rs:145-150`, "Lean's `labelOk`", restated;
  only `GRAIN_NAME_MAX` is emitted).
- `table.rs` is clean: every field comes from `generated` (`table.rs:11-41`).
- **`unwrap`/`expect` on a socket byte:** none. clippy denies `unwrap_used`, `expect_used` and
  `panic` in both crates (`client/Cargo.toml:37-39`, `launcher/Cargo.toml:68-70`), and every
  `unwrap_or*` I found has a total fallback. I checked every index:
  - `frame.rs:148` `body[0]` after `len ≥ 1`;
  - `mux.rs:455` `rest[0]` after `body.len() > CONN`;
  - `stdio.rs:109` `body[5..]` after `get(4)`;
  - `custody.rs:122, 235, 544-547` slices after exact-length reads;
  - `keybroker.rs:225` `pair[1]` after `hex.len() == 64`;
  - the generated `Cursor` uses `get`.
  The one `assert_eq!` (`frame.rs:134-138`) checks Rust's own arithmetic.
- **Crash-stop vs wedge:** no hostile byte crashes the client or the launcher. A hostile or slow
  peer WEDGES them in F3 (Host or follow trickle), F4 (decider silence) and F20 (upstream trickle),
  and a crash at the wrong instant wedges every later command in F5. The model allows a crash-stop.
  These are not that.

---

## 6. What I did not read, with sizes (lines)

client/tests (read in part or not at all):
- `run.rs` 929: read `:1-90`, `:640-690`, `:880-929` and the assertion lines;
- `supervise.rs` 605: read `:32-75`;
- `custody.rs` 404: not read;
- `mux.rs` 322: not read;
- `real.rs` 297: read `:160-185`;
- `roundtrip.rs` 235: not read;
- `frame.rs` 62: not read;
- `sockets.rs` 34: not read.

launcher/tests:
- `members.rs` 1149: read `:394-510` and the assertion lines;
- `broker.rs` 1024: not read;
- `fence.rs` 948: not read;
- `isolation.rs` 724: not read;
- `resident.rs` 563: not read;
- `sock.rs` 290: not read;
- `grain.rs` 237: not read;
- `common/mod.rs` 1173: read `:1-100`, `:420-680`, `:840-1173`.

launcher/src:
- `bin/probe.rs` 214: read `:1-60`;
- `generated.rs` 656 and `broker_generated.rs` 669: read the headers, `path_clean` and `Grant`.

Decisions and docs:
- `decisions/client.md` 1102: read CLIENT-24, 25, 27, 29, 30-34; titles only for the rest;
- `decisions/ops.md` 597: titles and grep only;
- `deploy/RUNBOOK.md` 781: grep plus `:400-432`.

Outside my layer but read to answer the brief: `Protocol/Command/Machine.lean:959-1071` and
`:182-183`; `Protocol/Attempt.lean:1-160`; `Protocol/Invite.lean:70-185`;
`Protocol/Command/Stdio.lean:1-30`; `Hosting/Plan.lean:85-146` (grep); `sandbox/src/lib.rs:216-234,
340-470`; `devtools/src/lib.rs:1-260`; `gates/runs.py:60-80, 360-400, 630-670`;
`gates/readset.py:82-87`; `redregg/work/promo/IMPACT-E2.md:1-90`; and the rustix 1.1.2 source
(`process/prctl.rs:66`).
