# Codex orchestration under Claude deputies — design memo (CODEX-ORCH, 2026-10-08)

Scout: CODEX-ORCH (Opus subagent). Deliverable: design, no code landed. Tags on every claim:
**MEASURED** = I ran it (this session, 2026-10-07 22:2x–22:35 EDT); **READ** = docs/source/our files, URL or path given;
**INFERRED** = my judgement. Scratch evidence (probe script, raw JSON-RPC log, fetched docs, experimental schema):
`/private/tmp/claude-501/-Users-ember-dev-breadstuffs/ce776c01-2f59-4f57-8177-23008d71bf57/scratchpad/`
(`probe.py`, `probe-log.jsonl`, `probe-out.json`, `codex-as-exp/`, `web/`).

---

## 0. The recommendation in one screen

1. **Control plane: one long-lived bridge process, `cxo` ("Codex hub"), on the Mac.** It owns a **private**
   `codex app-server` child process (not the shared daemon), talks raw JSON-RPC v2 with `experimentalApi: true`, and
   gives deputies a **CLI** (`cxo spawn|send|wait|answer|status|interrupt|fork|renew|retire|limits`) over a local
   unix socket. It can get an MCP facade later. Deputies call it with Bash. Codex workers call back into it through
   **dynamic tools** (`deputy.report`, `deputy.ask`, `deputy.request_build`, `deputy.build_status`, `deputy.submit`).
   Not `codex exec` + `codex queue`, and not the SDKs (§a).
2. **The hub is the only party that holds identity, liveness, the rate-limit budget and build slots.** Deputies
   address workers by stable **name**, never by thread id. A send to a retired name is refused by construction, and
   nobody "waits on a peer": dependencies are hub conditions (§e).
3. **"Done" means the deputy verified it from artifacts.** The worker's `submit` is accepted only after mechanical
   guards (range exists, scope globs, no `sorry`, no deleted assertions, no widened pins). After that the Claude deputy
   checks the *pushed* range itself, reading statements, running the narrowest refuting check and planting a fault.
   Codex's goal status `complete` is the model's own claim. **MEASURED: it set that status itself** (§b).
4. **Steering ladder:** piggyback on the next `report` → `turn/steer` → `turn/interrupt` + corrective turn →
   `thread/fork` at the last good turn → fresh thread from the worker's own WORKLOG (§c).
5. **Models:** gpt-6-sol for bounded implementation with a worked example; gpt-6-astra for hard proofs, unknown-cause
   reds, and cross-model review of Sol's submissions. One account-wide weekly bucket. Admission is paced against the
   window with `ordinaryUsageAllowed` as the hard gate (§d). **⚠ Ember's labels are ambiguous; see §d.1.**
6. **Builds are the binding constraint, not Codex quota.** hbox gives ≤2 Mini builds. The pipeline tooling and the
   authoritative shared remote both lived on the deleted burst boxes, and **neither exists on hbox today (MEASURED)**
   (§f).
7. **First experiment:** one Opus deputy, three Codex workers (2 Sol + 1 Astra), one backlog item split three ways on
   disjoint files, about 6–8 h with Ember present. Ten measured quantities and an explicit scale/no-scale rule (§g).

Probe cost: **one thread, one 40 s turn, 155,329 tokens (154,208 input of which 132,992 cached; 1,121 output);
weekly `usedPercent` 0 → 1** (integer granularity, and other Codex sessions were active at the same time). MEASURED.

---

## 1. What Codex exposes (verified locally)

### 1.1 Binaries, versions, daemon
- `codex-cli 0.160.0` at `/opt/homebrew/bin/codex`. **MEASURED.**
- The shared daemon is already running: `codex app-server daemon version` →
  `{"status":"running","managedCodexVersion":"0.161.0","socketPath":"/Users/ember/.codex/app-server-control/app-server-control.sock","cliVersion":"0.160.0","appServerVersion":"0.161.0"}`.
  The **daemon and CLI are on different versions.** MEASURED.
- `codex app-server daemon update` is documented as "may interrupt running work". READ (`--help`).
- `codex app-server --listen stdio://|unix://PATH|ws://…` runs a private server. `generate-json-schema --experimental`
  emits the experimental fields. READ (`--help`), MEASURED (generated into `scratchpad/codex-as-exp/`).
- `~/.codex/config.toml`: `model = "gpt-6-astra"`, `model_reasoning_effort = "high"`. MEASURED.
- Feature flag `goals` is `stable true`. MEASURED (`codex features list`).

### 1.2 The protocol surface we need (from the schema; all names MEASURED from the generated JSON)
- **Client→server:** `initialize` (+`initialized` notification), `thread/start|resume|fork|read|archive|unsubscribe`,
  `thread/turns/list`, `thread/items/list`, `thread/inject_items`, `thread/goal/set|get|clear`, `thread/compact/start`,
  `turn/start|steer|interrupt`, `account/rateLimits/read`, `account/usage/read`, `model/list`, `thread/loaded/list`.
- **Server→client requests:** `item/tool/call` (dynamic tools), `item/commandExecution/requestApproval`,
  `item/fileChange/requestApproval`, `item/permissions/requestApproval`, `applyPatchApproval`, `execCommandApproval`,
  `item/tool/requestUserInput`, `mcpServer/elicitation/request`.
- **Notifications we consume:** `turn/started`, `turn/completed` (status `completed|interrupted|failed`), `turn/diff/updated`,
  `turn/plan/updated`, `item/started`, `item/completed`, `thread/status/changed` (`notLoaded|idle|systemError|active`),
  `thread/tokenUsage/updated`, `thread/goal/updated`, `thread/compacted`, `account/rateLimits/updated`, `error`,
  `serverRequest/resolved`, `thread/closed`, `model/rerouted`.
- **Experimental-only, so `capabilities.experimentalApi = true` is required:**
  - `dynamicTools` on `thread/start`. The non-experimental schema in `scratchpad/codex-as/` does not reference `DynamicToolSpec` from `ThreadStartParams` at all; the experimental one does. MEASURED.
  - The `item/tool/call` flow. READ: https://learn.chatgpt.com/docs/app-server, section "Dynamic tool calls (experimental)".
- **`dynamicTools` is accepted only on `thread/start`.** It is persisted in the rollout and restored on `thread/resume`.
  READ (docs above; issue https://github.com/openai/codex/issues/24808 "allow dynamicTools to be updated after
  thread/start"). Design consequence: **the tool set is fixed per thread; design it once.**
- `TurnStartParams` carries `toolOutput`. This is the protocol form of the Python SDK's `ExternalMessage`, which delivers
  content "with tool-level authority, below user and developer instructions". READ:
  https://github.com/openai/codex/blob/main/sdk/python/docs/api-reference.md. The field is MEASURED in the schema.
- `ThreadStartParams` also has `multiAgentMode` (`explicitRequestOnly|proactive|custom`), `permissions`, `historyMode`,
  `config` (free-form overrides), `developerInstructions`, `baseInstructions`, and `ephemeral`. MEASURED.
- Goal semantics. READ (docs):
  - The objective must be non-empty and at most 4,000 characters.
  - A new objective resets the usage accounting.
  - Status values: `active|paused|blocked|usageLimited|budgetLimited|complete`. MEASURED in the schema.
- Subscriptions. READ (docs):
  - A connection that starts a thread is subscribed to it.
  - When the last subscriber leaves, the thread unloads after 30 minutes with no subscribers and no activity.
  - `optOutNotificationMethods` in `initialize` suppresses noisy notifications per connection, for example `item/agentMessage/delta`.
- The handshake is required. Requests sent before `initialize` get a `Not initialized` error. READ.

### 1.3 The read-only probe (MEASURED; `scratchpad/probe.py`, log `probe-log.jsonl`)
Setup:
- A private `codex app-server --listen stdio://` in a temp dir with two text files.
- `thread/start` with `model: gpt-6-sol`, `sandbox: read-only`, `approvalPolicy: never`, and two dynamic tools: `report_status`, `submit_result`.
- `thread/goal/set` with a `tokenBudget` of 200,000.
- One `turn/start`.

Results:
- **The dynamic tool round trip works and is synchronous.**
  - Codex called `report_status` 3 times and `submit_result` once, in exactly the order the prompt asked for: at t = 4.9 s, 16.3 s, 25.3 s and 36.3 s.
  - Each call arrived as an `item/tool/call` server request. The turn waited for our JSON-RPC response (`{"success":true,"contentItems":[{"type":"inputText","text":…}]}`).
  - The thread items recorded each call as `type: dynamicToolCall`, `status: completed`.
- **`turn/steer` works mid-turn and is a precondition check.**
  - With the wrong `expectedTurnId`, the server returned `-32600 "expected active turn id 'turn_bogus' but found '01a11957-…'"`.
  - With the right id it returned `{"turnId": …}`. The steer text appeared as a `userMessage` item between the first tool call and the first shell command.
  - Codex obeyed it: the submitted answer was `"5 STEERED"`.
  - After the turn completed, a steer returned `-32600 "no active turn to steer"`.
  - **So steer is safe against acting on a stale turn**: it fails loudly instead of landing in the wrong turn.
- **The goal is self-completed by the model.**
  - `thread/goal/updated` fired 8 times. `tokensUsed` went 0 → 18,673 → … → 20,595, then the status flipped to `complete` inside the same turn.
  - Nobody but the model judged it complete.
- **Cost and context.**
  - Turn total: 155,329 tokens (input 154,208, of which 132,992 cached; output 1,121; reasoning 665). The goal reported `tokensUsed` 20,595.
  - The first request already carried about 18.7K tokens of context. That includes Ember's global `~/.codex/AGENTS.md` (5 KB) and the skills list (both seen in `cv show codex:01a11957-…`).
  - Five MCP servers started for the thread: playwright, cua_repl, node_repl, codex_apps ready; introspection failed. MEASURED from `mcpServer/startupStatus/updated`.
  - `modelContextWindow` = 258,400.
- **Rate limits.**
  - `account/rateLimits/read` returned **one bucket, `limitId: "codex"`**, with `primary.windowDurationMins: 10080` (weekly), `usedPercent` an **integer**, `planType: "promax"`, `ordinaryUsageAllowed: true`, and resets at 2026-10-15 02:24:50 UTC.
  - There was no per-model bucket. `secondary` was null.
  - `account/rateLimits/updated` was **pushed 8 times during one turn**, so the hub does not need to poll.
  - `rateLimitResetCredits` shows **one available "Full reset" credit** (granted 2026-10-07 19:20 EDT, expires 2026-11-06).
- **`account/usage/read`** gives daily token buckets.
  - The Codex-root days were **3.46B tokens (10-02) and 5.46B tokens (10-03)**. The peak day is 5.61B. Lifetime is 57.5B.
  - This is our only data on what an uncontrolled Codex coordinator costs.
- **`model/list`** returned `gpt-6.1-sol` (**isDefault**), `gpt-6-astra`, `gpt-6-sol`, `gpt-6-luna`, `gpt-5.6-sol`,
  `gpt-5.6-terra`, `gpt-5.6-luna`, and `gpt-daybreak-blue-latest`.
- **`cv show codex:<thread>` reads a hub-started thread with no extra wiring.** The rollout lands in `~/.codex/sessions/`.
- Two **other** Codex rollouts were created on this machine during the probe window (22:27 and 22:30), not by me.
  The 0 → 1 % tick therefore cannot be attributed to the probe alone. MEASURED (the files); attribution INFERRED.

---

## 2. Lessons from our own history

### 2.1 Codex as coordinator (10-02/03)
- **It burned the quota and walled.** The Codex root hit `usage_limit_exceeded` at 19:20 UTC on 10-03. The fn root died 3 s later. No Codex was usable until 10-10. READ: memory `project-2026-10-03-mini-codex-wall-takeover.md`. The daily buckets show 3.5B and 5.5B tokens on those two days (MEASURED). **Lesson: nothing paced admission against the window.**
- **Its output was scattered and mostly not on main.**
  - Its wave left **256 lane directories across 4 machines** (hbox workbox, /tank, the Mac, persvati).
  - Classified: **114 SUPERSEDED, 59 DEAD, 50 DUPLICATE, 15 SPEC-ONLY, 13 MINE-NOW, 5 WORKING-STATE.**
  - It included 12 GB of trace fixtures from a rejected generation.
  - READ: `work/CODEX-LANE-MINING-20261004.txt`.
  - **Lessons:**
    - Codex workers left to their own placement make directories, not landed ranges.
    - "Done" lived in STATUS prose ("broker 15:18 'completion uncertain'"), not in a queue.
- **Root state lived in compaction.** It went through 26 compactions, and a successor risked rebuilding work "because a note said it was not started". It left an agreement init (`00f711`) in an UNCERTAIN state that must never be resubmitted. READ (memory). **Lesson: state must be on disk in a registry and continuation files, not in a coordinator's context.**

### 2.2 Claude-only coordination (10-07). READ: `work/grounding/GPT6-REPORT-20261007.md` §3 and `work/DEPUTIES-20261006.md`
1. **Rules stated but not enforced.** "Fixtures, journeys and pins are fix-forward; never hold main for them" was broken three times, causing stalls of 77–83 min each. The stall watch saw them, but nothing turned the observation into a move (§3.1). → In `cxo`, stalls are **events that page an owner**, not log lines.
2. **Briefs teaching wrong mechanics.**
   - Hand-typed `flock` chains blocked on one named slot while others were idle.
   - Failed builds were re-run in the next slot.
   - Nine builds were blocked 8–36 min (§3.9).
   - → **Workers never touch slots. The hub owns them.**
3. **Stale agent ids woke retired agents.** A retired keeper at about 763K context cherry-picked into the live keeper's tree. The root's watch prompt carried stale ids for most of the day (§3.12). → **Address by name and generation. Refuse sends to retired names.**
4. **Workers waiting on dead or absent parties.**
   - Row E was assigned at 05:21Z and started at 11:50Z.
   - A binary the root owed a lane sat "not sent" for about 6.5 h (§3.15).
   - → **Dependencies are hub conditions with owners, and they time out into events.**
5. **Idle boxes.** Mean load was 5.7/16 and 7.9/32. Coordination, not compute, was binding (§3.15).
6. **Renewal by distill compounds.** A distill of a distill would have started its successor at 281K tokens. Fresh renewal from the agent's own continuation file is the rule (§3.11). The OB-ENG deputy ran to about 720K.
7. **Writers writing through things they do not own.** Lake-cache poisoning, writes through hard links, and fixtures regenerated by a non-owner (§3.6, §3.7, §3.3). → **Guards on protected paths. Only the keeper regenerates fixtures.**
8. **Tools reporting success the work had not earned.** `| tail` exit statuses, replayed cache entries, scripts nobody elaborated (§3.16). → **Verdicts come from artifacts** (exit-code files, not a log tail).
9. **Usage outages froze everything at once** (2 h and 1 h). State on disk made resumption one message per agent (§3.13). → The hub must survive an outage. `codexErrorInfo: usageLimitExceeded` pauses admission, and `ordinaryUsageAllowed` resumes it.

### 2.3 Outside practice (READ)
- **Verify every result from outside the agent that produced it.**
  - The lane brief had **numbered outcomes**, **numbered exclusions**, a **pinned environment**, and a **completion signal**: one command, run last, "so the orchestrator knows it has finished instead of guessing from the screen".
  - Independent verification caught a regression and an out-of-scope behaviour change that the lane's own checks missed.
  - Source: a Claude orchestrator with Codex GPT-6 Sol/Luna lanes in worktrees. https://www.sharmaprakash.com.np/homelab/letting-coding-agents-build-campsite/
- **Self-verification weakness and token spend** (SWE-Marathon, arXiv 2606.07682, via the secondary write-up https://codex.danielvaughan.com/2026/07/30/swe-marathon-…):
  - 99.6 % of failures contained validation signals the agent could have seen locally.
  - Lower token spend correlated with *better* outcomes. Spend tracks retry loops.
  - About 99.5 % of tokens are context replay.
  - Pass rate degrades sharply on longer runs, which favours short sub-sessions.
- **Shortcut-taking is common and detectable.** Deleting the test that exposes the bug is the canonical hack. https://arxiv.org/abs/2610.03055 (HACKTRACE). https://metr.org/blog/2025-06-05-recent-reward-hacking/
- **Model behaviour on scope.** OpenAI's Astra announcement, as quoted in the Kagi snippet (the page itself refused to load): "GPT-5.6 Sol … without production safeguards went beyond the authorized target 48% of the time, GPT-6 Astra … 0%". https://openai.com/index/gpt-6-astra/ This is READ from the snippet only; treat it as directional.
- **Price.** Astra's standard API token rates are about 5× Sol's, and about 10× for cached reads. Escalate to Astra "with a compact summary, failed approaches, and the test evidence rather than blindly replaying an enormous transcript", with turn and spend caps. https://huggingface.co/blog/karmen-beatapi/gpt-6-1-sol-vs-sol-vs-astra-coding-agent-cost (READ, secondary). Under a ChatGPT-plan quota the conversion to `usedPercent` is unknown and has to be measured (§g).
- **A weak planner hurts more than a weak executor.** https://arxiv.org/html/2510.07505v4 (PEAR). This supports a strong-planner (Opus deputy) plus cheaper-executor split. READ.

---

## (a) Control plane — decision: a hub over a private app-server, CLI-first

### Options weighed
| option | steer mid-turn | dynamic tools | goals/budgets | push rate limits | liveness | verdict |
|---|---|---|---|---|---|---|
| `codex exec --json` + `codex queue` | no. `queue` is "Queue a message for an existing session", for a later turn (READ `--help`) | no | no | no | parse stdout | **reject**: this is the "shell out and grep" design Ember ruled out |
| TS SDK `@openai/codex-sdk` | no | no | no | no | via exec | **reject**: it "spawns the CLI and exchanges JSONL" (READ https://github.com/openai/codex/blob/main/sdk/typescript/README.md) |
| Python SDK `openai_codex` | yes (`TurnHandle.steer/interrupt`) | not in its public API (READ api-reference.md) | not exposed | no | partial | **not as the base**. Useful reference; we would fight it to reach the experimental fields |
| shared daemon via its control socket | yes | yes | yes | yes | yes | **reject for workers.** It is shared with Ember's TUI and `codex agents`. Which connection receives a server request when several are subscribed is undocumented (INFERRED risk). Its version is skewed (0.161 vs 0.160, MEASURED). `daemon update` may interrupt work (READ) |
| **private app-server child owned by one hub** | yes | yes | yes | yes | yes | **choose** |

### Why a hub process, not each deputy holding a connection
- **Dynamic tool calls block the worker's turn until a client answers.** MEASURED in the probe; READ in the danielvaughan write-up: "Slow handlers stall the entire session". A Claude deputy acts in turns and is not a resident listener. So the answering party must be a resident process that serves most calls itself (`report`, `request_build`, `build_status`, `submit` guards) and parks only `ask` for the deputy.
- **Some things exist exactly once, and the hub is where they belong:**
  - the rate-limit bucket is account-wide (MEASURED);
  - the build slots are shared across deputies;
  - liveness and identity need one source of truth (§e).
- **Claude Code subagents get MCP servers from session start** (INFERRED from how the harness loads MCP). A CLI works for every deputy today with no restart. An MCP facade over the same socket is an optional later step.

### Shape of `cxo` (about 1,000 lines of Python, INFERRED estimate; a Claude lane builds it — bootstrap code is not a Codex task)
- `cxo-hub` daemon: an asyncio JSON-RPC client to its private `codex app-server --listen stdio://` child.
  - It pins the Codex binary and version. It refuses to start if `codex --version` differs from the version whose generated schema is checked in.
  - Registry: SQLite at `~/dev/redregg/work/cxo/registry.sqlite`. Every event is also appended to `events.jsonl`, so `cv` and humans can read it.
  - It runs under `launchd` or `nohup` with a restart loop.
  - On restart, every thread whose turn was in flight is marked `INTERRUPTED`. The hub then runs `thread/resume` (dynamic tools are restored, READ) followed by a `turn/start`: "you were interrupted at <time>; read WORKLOG.md and continue".
- `initialize` sends `capabilities: {experimentalApi: true, optOutNotificationMethods: ["item/agentMessage/delta", "item/reasoning/textDelta", "item/reasoning/summaryTextDelta", "item/commandExecution/outputDelta", "item/fileChange/outputDelta"]}`.
- **Every `thread/start` uses:**
  - `cwd` = the worker's worktree;
  - `model` and `effort` per §d;
  - `sandbox: "workspace-write"` with network off: builds go through the hub, so no ssh keys are in Codex's reach (custody, CLAUDE.md pause item 1);
  - `approvalPolicy: "never"`. The hub also declines any approval request that arrives anyway, as the probe did;
  - `multiAgentMode: "explicitRequestOnly"`, so Codex does not fan out its own sub-agents;
  - `developerInstructions` = the worker contract (§b);
  - `dynamicTools` = the fixed namespace `deputy` (§b);
  - `config` overrides that drop the five MCP servers and the global skills from worker threads. **INFERRED** that the keys take effect; this is the first thing the experiment checks, by comparing the first-request token count against the probe's 18.7K.
- **Deputy-facing CLI.** All verbs print one JSON line; each `wait` blocks in the *foreground* (memory: subagents strand on background waits).
  - `cxo spawn NAME --deputy D --model M --effort E --worktree PATH --base SHA --brief FILE [--after NAME:STATE]` creates the thread, sets the goal (`thread/goal/set` with objective and `tokenBudget`), and queues the first turn behind the scheduler (§d).
  - `cxo send NAME TEXT [--now]`:
    - **Default:** queued and delivered as the result text of the worker's next `deputy.report` call. This keeps order and does not disrupt the worker.
    - `--now`: `turn/steer` with `expectedTurnId` = the hub's current turn id.
    - If the thread is idle, `turn/start`.
    - A message relayed from another *agent* (not the deputy's own instruction) goes as `turn/start{toolOutput}`, with tool authority, not user authority.
  - `cxo wait [--deputy D] [--timeout 540]` returns the next event(s) for D: `ASK`, `SUBMIT`, `STALL`, `GUARD`, `TURN_END_NO_SUBMIT`, `ERROR`, `BUDGET`, `BUILD_DONE`, `DEP_DEAD`. A timeout under 600 s keeps it inside one Bash call.
  - `cxo answer NAME ASK_ID TEXT` · `cxo status [D]` · `cxo transcript NAME [--since TURN]` (from `thread/items/list`; `cv show codex:<id>` also works, MEASURED).
  - `cxo interrupt NAME` · `cxo fork NAME --at-turn T --correction FILE` · `cxo renew NAME` · `cxo retire NAME` · `cxo limits`.

---

## (b) The worker contract

### What a Codex child receives
1. **A worktree it owns**: `git worktree add` from the hub's mirror at the base SHA, under `~/workbox/cxo/<name>/`. One worker = one worktree = one branch `cx/<name>`. This makes merge conflicts between siblings visible at queue time, not as trampling.
2. **developerInstructions** (fixed text, same for every worker, about 1 KB):
   - You are a worker for a deputy. Call `deputy.report` at start, after each milestone, and at least every 15 min of work.
   - Call `deputy.ask` instead of guessing when the brief is ambiguous.
   - Call `deputy.request_build` for any build; never run `lake build` of more than one leaf module yourself.
   - Keep `WORKLOG.md` in the worktree: decisions and why, assumptions, current state. Your successor starts from it.
   - Finish only by calling `deputy.submit`. Ending without it is treated as a stall.
   - Forbidden: `sorry`/`admit`, new `axiom`, `native_decide` where none was, deleting or weakening a theorem, assertion or test, editing pins, fixtures, gate definitions or authority files, `|| true`, piping a build into `tail`, `pkill -f`, `git stash`, printing env.
3. **The brief** (first `turn/start` input). This is the KICKOFF format plus our values:
   - `GOAL:` one paragraph.
   - `OUTCOMES:` numbered, each with an acceptance check and the artifact that proves it.
   - `EXCLUSIONS:` numbered, plus `ALLOWED_PATHS` and `PROTECTED_PATHS` globs. The hub enforces these.
   - `GROUND TRUTH:` real signatures and absolute paths pasted in. We never write "put it under X/"; we give the real path, so the worker cannot build a mirror of the interface.
   - `WORKED EXAMPLE:` one done instance (the 02:00 "API before ports" amendment).
   - `ENV:` pinned toolchain, base SHA, build targets.
   - `PLANT:` for each new check, the fault that must turn it red.
   - `SAY WHAT YOU BROKE:` what refuses or re-emits, per CLAUDE.md.
   - Each brief claim is tagged measured / read / ASSUMED (memory "A brief is a claim").
4. **Goal**: `thread/goal/set {objective: <GOAL + outcome list, ≤4000 chars>, tokenBudget: B}`. B is 3M for Sol and 1.5M for Astra to start; adjust from experiment data. The goal gives a persistent objective across compaction (INFERRED, the purpose of `/goal`) and a hard ceiling (`budgetLimited`). **It is never the done signal.**

### The dynamic tools (namespace `deputy`)
| tool | args | hub behaviour |
|---|---|---|
| `report` | `phase`, `done[]`, `next`, `blockers[]`, `files_touched[]` | returns at once with "ack" plus any queued deputy messages; resets the silence timer; appends to events.jsonl |
| `ask` | `question`, `options[]`, `default`, `blocking` | non-blocking: returns "noted; proceed with default". Blocking: parked up to 15 min, raised as an `ASK` event to the deputy. On timeout it returns "no answer; proceed with `<default>` and record ASSUMPTION in WORKLOG.md". The worker's turn waits during the park (MEASURED that it blocks), so a long park costs nothing |
| `request_build` | `targets[]`, `kind` (`leaf` / `affected` / `exe`) | rsyncs the worktree to an hbox lane clone and queues it in a hub-owned slot under `swarm-build`. Returns a ticket at once (we do not rely on the server's tolerance for long blocking calls, INFERRED) |
| `build_status` | `ticket`, `wait_s ≤ 300` | returns `queued` / `running` / `exit=N`, the log path, and the last 60 lines. The exit code is read from an exit-status file the remote wrapper writes, never from a log tail |
| `submit` | `range` (base..tip), `claims[]` (`claim`, `evidence_path`, `refuting_cmd`), `plants[]`, `breaks`, `deferrals[]` | runs the guards (§c). Pass: pushes `cx/<name>` to the authoritative remote, drafts `queue/<name>.txt`, sets state SUBMITTED, raises a `SUBMIT` event, and returns "submitted — end your turn now". Fail: returns the guard findings, and the worker keeps working |

### Definition of done, and how the deputy checks it
- **Worker done** = a `submit` that passed the hub's guards. It is a candidate, not a fact.
- **Deputy done** = the deputy, independently:
  1. fetches `cx/<name>` from the authoritative remote into **its own** detached clone. It never reads the worker's worktree (memory: verify HEAD, not the working tree);
  2. reads the diff against OUTCOMES and EXCLUSIONS, and reads every new or changed theorem *statement*, rejecting vacuous ones;
  3. runs the narrowest refuting check per claim (`refuting_cmd`, re-derived rather than trusted) through `cxo build` in its own slot;
  4. applies each plant and confirms the check goes red. It asserts the mutation actually happened before reading the verdict (memory: a falsifier that stopped falsifying);
  5. only then writes the queue entry for the keeper under VERIFY-ONCE. The keeper's gate stays the only full gate.
- Optional middle layer for Sol submissions: an **Astra review thread** (read-only sandbox, no tools but `report`/`submit`). It gets the diff and the brief, and is asked for the three most likely defects. This is cheap relative to deputy context and is a different model family. It does not replace step 2.

---

## (c) Steering policy

### Monitors the hub runs mechanically (no LLM)
| signal | source | action |
|---|---|---|
| silence: no `report` for 20 min and no item events for 10 min while the turn is active | timers, `item/*` | piggyback is impossible, so `turn/steer` "report now". After another 10 min: `STALL` event to the deputy; after 15 min, also the root (the 02:15 amendment, done structurally) |
| turn ended without `submit` | `turn/completed` with no SUBMITTED state | automatic corrective `turn/start`: "you ended without submit; submit with evidence or `ask` with the blocker". The second time, a `TURN_END_NO_SUBMIT` event to the deputy (catches early "done") |
| scope drift | `turn/diff/updated`, `item/completed{fileChange}` paths | outside `ALLOWED_PATHS`: piggyback a warning. Inside `PROTECTED_PATHS` (fixtures, pins, gate scripts, authority, ledger): **immediate `turn/steer`**, and `GUARD` to the deputy |
| test or proof weakening | diff guard over `turn/diff/updated` and at `submit` | added `sorry`/`admit`/`axiom`, new `native_decide`, `set_option maxHeartbeats 0`; a deleted `theorem`/`lemma`/`example`/`#assert_*`/`assert`/`#[test]`; `#[ignore]`/`.skip`; a removed `#guard` without a named replacement; edited pins or hashes; `|| true`; `| tail` in a script. Each is a steer citing the rule. A repeat is an interrupt and a `GUARD` event |
| retry loop | the same command failing 3 or more times; tokens rising with no new files or reports | steer: "stop; `ask` with what you tried". If it continues: interrupt and hand to the deputy |
| context pressure | `thread/tokenUsage/updated.last.inputTokens` against `modelContextWindow` (258,400, MEASURED); `thread/compacted` count | at 60 % or after the second compaction: the deputy chooses fork or renew |
| budget or quota | `thread/goal/updated{budgetLimited}`, `error{codexErrorInfo: usageLimitExceeded/rateLimitExceeded/contextWindowExceeded}` | pause the worker; scheduler event |

### The ladder: cheapest move that fixes it
1. **Piggyback** on the next `report`. This is the default for course corrections, new information and answers. It keeps the worker's flow intact.
2. **`turn/steer`** when it must land before the worker's next action: protected path touched, wrong premise about to be built on, stop-and-report. It is safe against a stale turn because of `expectedTurnId` (MEASURED).
3. **`turn/interrupt` + corrective `turn/start`** when the current turn's *plan* is wrong but the thread's knowledge is good, for example the wrong approach to a right understanding.
4. **`thread/fork` with `lastTurnId` = the last good turn**, plus the correction, when the bad turn has *poisoned* the context: a false premise absorbed, a long detour. This keeps what was learned before the detour.
5. **Fresh thread from the worker's own `WORKLOG.md`** (`cxo renew`). Use it at the context or compaction ceilings, after a model switch from Sol to Astra (escalation), or when the brief itself changed materially. **Never renew from the deputy's paraphrase**, and never distill twice (§2.2.6).
- Restart, not steer, when the worker has twice ignored the same steer (steer obedience is measured in §g), or when it shows test-weakening intent twice in one thread.

---

## (d) Model allocation and rate-limit-aware scheduling

### d.1 ⚠ Resolve the naming first (a decision for Ember or the root, not taste)
- Ember wrote "gpt-6-sol ('5.6-Sol')". The account offers **both** `gpt-6-sol` ("GPT-6-Sol") and `gpt-5.6-sol` ("GPT-5.6-Sol"), and `model/list` marks **`gpt-6.1-sol` as the default**. MEASURED.
- The config default is `gpt-6-astra`. MEASURED.
- These are different models. The 48 % out-of-scope figure in §2.3 is about **gpt-5.6-sol**.
- **Proposal:** use ids exactly. Run the experiment's Sol workers on `gpt-6-sol` as Ember named it, and record `gpt-6.1-sol` as a candidate arm, not a silent substitution.

### d.2 Who does what (INFERRED, to be revised by §g data)
- **Sol (most workers):**
  - ports with a worked example;
  - census and ratchet scripts;
  - journeys and journey rows;
  - planted-fault harnesses;
  - `sg`-driven mechanical rewrites;
  - doc-against-code;
  - fix-forward of a red whose cause is named.
- **Astra:**
  - hard Lean proofs where the proof is the deliverable;
  - reds with unknown cause;
  - design-in-the-small inside an owned cluster;
  - review threads over Sol submissions (§b);
  - escalation after Sol fails twice on the same item. The escalation is a fork or renew carrying a compact failure summary, not a replay.
- **Effort:** `high` by default (config); `medium` for mechanical Sol work. Per-worker, not global (the Campsite lesson).
- **Never:** Codex coordinating Codex (§2.1). Codex workers never spawn sub-agents (`multiAgentMode`).

### d.3 Concurrency
- **Per deputy: 3 active workers in the experiment; at most 4–5 at scale.**
  - The deputy's adversarial review is the throughput limit. Each SUBMIT costs the deputy a diff read, a statement read and a plant.
  - About 8–12 accepted ranges should fit in a deputy's 400–500K ceiling. INFERRED; measured in §g.
- **Global:** active Codex workers ≤ min(Σ deputy caps, pacing cap below, build capacity × 3). With hbox alone, build capacity is 2 slots, so ~6 workers whose next step is a build.

### d.4 Rate-limit scheduler (in the hub)
- Inputs:
  - `account/rateLimits/updated` (pushed, MEASURED) and `account/rateLimits/read` at start;
  - `ordinaryUsageAllowed` as the **only** go/no-go. READ: the schema says "clients must not infer recovery from percentages or reset times";
  - `primary.usedPercent` (an integer) against elapsed fraction `f` of the 10,080-minute window.
- **Pacing rule:** target `usedPercent ≤ 100·f·0.85` plus a 15 % reserve for the keeper's fix-forward and the last day.
  - Ahead of pace: admit no new Astra turns, then no new spawns.
  - Never interrupt an in-flight turn for pacing. Only a hard `usageLimitExceeded` pauses everything.
- Per-thread `tokenBudget` (goal) caps runaway workers. A turn's spend is visible live in `thread/tokenUsage/updated`.
- **Calibration:** log (tokens by model, cached and uncached) against each `usedPercent` tick, giving tokens-per-percent for each model. One integer tick in the probe is not enough data. The experiment produces it.
- **Token hygiene,** the cheapest lever because about 99.5 % of tokens are replay (READ, §2.3):
  - strip the MCP servers and skills from worker threads (§a; the probe base context was 18.7K, MEASURED);
  - keep briefs short and pointed at files;
  - prefer fresh, short threads per sub-item over one marathon thread.
- **The free "Full reset" credit** (MEASURED available) and `account/rateLimitResetCredit/consume`: spending it is **Ember's call** (CLAUDE.md pause list: spending and irreversible acts). The hub never consumes it.

---

## (e) Identity and liveness

- **Names, generations, states.**
  - A worker is `deputy/item/gN`, for example `kern/store-audit/g2`.
  - The registry row holds: name, deputy name, generation, `thread_id`, model, effort, worktree, branch, base SHA, state, `last_event_at`, `last_report_at`, tokens, goal status, current `turn_id`, and successor.
  - States: `QUEUED → SPAWNING → WORKING ⇄ {WAITING_ASK, WAITING_BUILD} → SUBMITTED → VERIFIED → LANDED`, or `→ RETIRED`, or `→ DEAD`.
- **Address by name only.**
  - `cxo send NAME` resolves to the current generation's thread.
  - A name in `RETIRED`/`DEAD` with a successor is **refused** with "retired 10-08T03:12Z; successor `kern/store-audit/g3`". The caller must re-address deliberately. A stale id can't wake anything because ids are never the API.
  - `retire` also calls `thread/archive`, so the old thread is not in `codex resume` pickers.
  - The hub rejects any `item/tool/call` from a thread it doesn't hold as current. Belt and braces.
- **Deputies are names too.**
  - The hub stores `deputy → current Claude agent id`.
  - A renewed deputy runs `cxo deputy rebind kern <new-id>` as its first act.
  - Workers never message deputies directly. They `ask` or `report`, the hub raises an event, and whoever holds the deputy name now sees it on `cxo wait`.
  - The retired-deputy failure from §3.12 is structurally gone for the Codex half. For Claude↔Claude messaging, the root keeps its own name→id table in one file the hub also serves (`cxo whois NAME`). INFERRED: worth adopting for all agents.
- **Liveness from protocol facts, not prose:**
  - `thread/status/changed` (idle / active / systemError / notLoaded);
  - `turn/completed.status`;
  - `error` with `codexErrorInfo`;
  - item-event heartbeats.
  - A thread `active` with no item for 10 min triggers a `thread/read`. On `systemError`, or if the hub's child died, the state becomes `DEAD` and the deputy gets an event.
  - The hub stays subscribed to every live thread, so threads never hit the 30-minute unload (READ).
- **No waiting on peers.**
  - Cross-worker dependencies are declared: `--after NAME:LANDED`. The hub doesn't start the dependent turn until the condition holds.
  - If the dependency goes `DEAD`/`RETIRED` without a successor, the deputy gets `DEP_DEAD` immediately.
  - Workers have no peer-messaging tool at all. Every cross-worker fact flows through the deputy.
- **Stall escalation is mechanical:** `STALL` goes to the deputy at 10 min, and to the root at 15 min with what the worker waits on, since when, and what would unblock it.

---

## (f) Build boxes: what the plan needs

**Facts.**
- The Latitude burst boxes are deleted. The archive is at `work/burst2-teardown/` (1.2 GB). MEASURED.
- The **authoritative shared remote** lived on burst2-a (READ §3.10), so **it is gone.**
  - Local `~/dev/minidregg` has the last remote-tracking snapshot: `shared/main = shared/green = cfdaf64d` (10-07 22:29Z), `shared/next = 68f78d23` (10-08 00:53Z). MEASURED.
  - Its fetched `origin/main` is c1df1f08 (a stale fetch). MEASURED.
- **hbox has `swarm-build` and `/tank/dregg-build/claude-lanes/warm-base`, but no `/srv/pipeline`.** That means no `slot.sh`, `slots`, `lean-ask`, `mk-lane` pipeline or `build-anywhere`. It has no Mini bare repo either: `/srv/git` holds only `dregg-infra.git`. hbox has 24 threads, and its load was 9.8 at 22:34 EDT. MEASURED via read-only ssh.
- `scripts/burst/burst-up` exists on the shared refs (commit 73f9e805, on `shared/green`), but not in the local checkout's HEAD (4ef4e808). MEASURED.
- A fresh burst box measured 64 s (root phase) + 69 s (user phase) + a 68 s warm relay with 0 recompiles. READ §3.8.

**What the plan needs, in order.**
1. **A new authoritative remote.** INFERRED proposal: a bare repo on hbox `/tank` seeded from `shared/next` 68f78d23, with `shared-remote publish` semantics (main and green fast-forward only). This is the root's call. Until it exists, `submit` cannot push and the keeper has no train.
2. **The pipeline tooling on hbox**, installed by `burst-up`'s user phase or a subset of it: the slot tool and `lean-ask`. The hub's build executor wraps `swarm-build` itself, but `lean-ask` and the warm-base refresh are worth having.
   - CLAUDE.md caps hbox at 2 Mini builds. The hub enforces this with a **2-slot semaphore it owns**: 1 lane slot plus 1 for the gate and deputy verification during the experiment.
   - Workers never ssh.
3. **The warm base advanced** to the new authoritative next or green tip, rebuilt **once** (memory: warm bases, never parallel rebuilds). Lane clones are made by `cp -al` + unlink (memory: `cp -al` shares inodes).
4. **For scale beyond the experiment:** 2 slots cannot feed 3 deputies × 4 workers. `burst-up` is reproducible, so re-provision **1–2 burst boxes** when the scale decision is yes, and the hub's executor gains a box list. Provisioning is spending (pause list), so it is Ember's go.
5. **persvati: never build** (charter; it is Ember's laptop). The Mac runs the hub and the worktrees: editing and git only.
   - Single-leaf `lake env lean` checks on the Mac only if a warm tree exists there. INFERRED; not assumed.
   - **Worktree disk use goes on the hub's dashboard.** Disk pressure means stop and report (CLAUDE.md).

---

## (g) First experiment: one deputy, three Codex children, one real item

**Setup.**
- Build `cxo` (one Claude lane, about half a day; INFERRED).
- Stand up the authoritative remote and the 2-slot hbox executor (§f 1–3).
- Ember present (daytime). The deputy is Opus.

**Item choice criteria.**
- Real backlog with FUNCTION-FIRST value.
- Splits three ways on **disjoint files**.
- At least one piece is mechanical (Sol) and one is hard (Astra).
- Each piece has a checkable acceptance with a plantable fault.

**Candidates** (INFERRED; the root picks):
- (i) the census follow-ups from b28 (`kn2-coproc` private constructor without a census row) together with the type-level `kernelTransport` witness filed in §3.17 (Astra);
- (ii) a DEPUTY-PLATFORM slice: SPK BEGIN/CLAIM lookups never called (cv `01a10b3e-af9e`), plus its journey row (Sol), plus the planted-fault harness (Sol).

**Arms.**
- `W1 = gpt-6-sol` and `W2 = gpt-6-sol` on the two mechanical pieces. `W3 = gpt-6-astra` on the hard piece.
- One Astra review thread per Sol SUBMIT.
- No baseline re-run. Compare against the same deputy role's Sonnet-worker ledger from 10-06/07 (READ: queue LOG).

**Seed one known trap.** One brief contains an acceptance test that is easier to weaken than to satisfy. This checks that the guard *and* the deputy catch it. A guard that never fires is unverified (memory: a gate that can't go red).

**Measure (all from hub `events.jsonl`, the queue LOG and rate snapshots):**
1. **Accepted ranges** (deputy-verified, keeper-landed) per worker-hour and **per `usedPercent` point**, failures included.
2. **Tokens per accepted range by model** (cached and uncached), plus the **tokens-per-percent calibration** (§d.4).
3. **Defects caught after the worker's own evidence:**
   - found by the deputy's independent check;
   - found by the Astra reviewer;
   - post-landing reds traced to these ranges (target 0).
4. **Guard precision and recall:** fires (true and false positives), and whether the seeded trap was caught.
5. **Early-done rate:** turns ending without `submit`; `submit`s rejected by guards.
6. **Steering efficacy:**
   - steers sent, and the fraction obeyed within the next 3 items (read from `thread/items/list`);
   - interrupts, forks and renewals, with reasons.
7. **Deputy load:** deputy tokens per accepted range; wall time from SUBMIT to verdict; the deputy's context at the end.
8. **Liveness hygiene:**
   - sends refused for retired names (should be >0 if renewals happen, with 0 wrong deliveries);
   - waits over 15 min;
   - `DEP_DEAD` events.
9. **Build-slot utilisation:** busy and idle slot-minutes; time a worker sat in `WAITING_BUILD`.
10. **Worker context:** the first-request token count with the worker profile against the probe's 18.7K (validates the §a config override); compactions per thread.

**Scale if all hold** (thresholds INFERRED; tune at review):
- ≥3 deputy-verified ranges landed in one session;
- 0 post-landing reds attributable;
- the seeded trap caught;
- guard false positives ≤ 1 in 3;
- median SUBMIT→verdict ≤ 45 min;
- the deputy under 300K at the end;
- the projected weekly use at 3 deputies × 4 workers under 70 % of the window;
- zero wrong-recipient deliveries.

**Otherwise:** fix the failing layer (brief, guards, hub or slots) and repeat with the same three workers' names (renewed).
**Then:** 3 deputies × 4 workers, plus 1–2 re-provisioned burst boxes (Ember's go), the keeper unchanged.

---

## Open decisions (pause-list items only)
1. Which "Sol": `gpt-6-sol` vs `gpt-5.6-sol` vs default `gpt-6.1-sol` (§d.1). This is a decision on Ember's words, not on taste.
2. The new authoritative remote's home (§f.1). This is the root's call, an ordinary decision.
3. Re-provisioning burst boxes, and the reset credit: both spending, so Ember's.

Everything else above is the design I would defend.
