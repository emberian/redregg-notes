# DESIGN-AGENT — an LLM agent as a first-class member of a nano World: the resident is the agent, the Bell is its inbox, a ring is any obligation (real 2026-10-26)

Author: FABLE-AGENT (a Fable). Axis 3 of `FRONTIER-AXES-20261026.md`. Read against nano `origin/main ad90a47`
(mirror `~/dev/nanodregg`), mini `hbox:/tank/dregg-build/pipeline/warm-base/src/README.md` at 334316df (read-only),
`VERDICT-20261024.md`, `HOLISTIC-HOSTING.md` §1b–1f, §3(E2), `HOLISTIC-RUST.md` §1.5, `TOPLEVEL-SPEC.md` §0.1, §6,
`DESIGN-CTX.md` §2.1, §2.5a, §4, §6, and the code: `Hosting/Resident/{Bell,Run,Sockets,Trace,Args}.lean`,
`Hosting/{Broker,BrokerWire,BrokerCli,Allowance,Pins,Plan}.lean`, `Hosting/Proofs/{ResidentRun,BellConform}.lean`
headers, `Lang/{Bell,StdActivity,StdHole,LiveHoles}.lean`, `world/resident/Bell.ob`, `world/grain/Lifecycle.ob`,
`Kernel/Receive/{Derive,Authority}.lean` (the invoke arm), `launcher/src/bin/keybroker.rs` header,
`launcher/tests/{resident_bell.rs,common/mod.rs}`, decisions HOSTING-12/13/27/42–51, LANG-76/77.
Tags: READ (a path) · MEASURED (a command) · INFERRED (my reasoning; attack these first).

## 0. The answer in one page

**The question, restated so it can be answered.** "What is the smallest thing that makes an LLM agent a
first-class member" presumes the agent is not one yet. MEASURED against the code, most of it already is. THE BAR's
"hosted Hermes" (HOSTING-27) is a member: it has a key (`nd --init-hosted`, a hosted record in nd-members'
workspace, READ `client/src/bin/nd.rs` header), a follower of its own (`/srv/nd-members/l/follow/<id>`, READ
`Hosting/Plan.lean` header), a grant chain the kernel checks on every act (`ownerAuthority`, READ `Derive.lean:188`),
a budget it cannot exceed (`capped_decide`, `start_window_refused`: the broker charges the WORST CASE before a byte
leaves and never refunds, READ `Hosting/Broker.lean` header), receipts for everything it did (every answer is a
signed Turn in the log whose row `answered_row_is_kept_answer` ties to the kept text, HOSTING-44), and laws that
bound it (the Bell's `bell` law, the `rung` guard, the patience; KERNEL-25's owner authority on `invoke`). It
cannot lie about what it did to the World because it cannot sign: it signs THROUGH `nd --stdio`, whose follower
admits the call on the member's own copy first (consent before signature, TOPLEVEL §4). It cannot see or
exfiltrate the provider key because it spends THROUGH keybroker (an ocap proxy; HOLISTIC-RUST §1.5). So the agent
is already **a process with two brokered capabilities and nothing else**: sign-as-me (the member socket) and
spend-my-allowance (the broker socket), confined by grain-launch to its package, its volume and those two sockets
(`Proofs.Plan.plan_sockets_own`). That is the shape the "agent as a principal, not a tool" line wants (MCP's
tool model has the agent CALL tools; here the agent IS the principal and every tool is a broker that decides).

**What is actually missing is one thing: the ring is the only obligation the agent can discharge.** The resident
is wired to one package shape (`Lang.Bell.shapeOk`, HOSTING-45): it reads `pending`, asks the model the ring's
text, and invokes `answer` with the text. It cannot fill a hole, judge an offer, or answer a typed question,
because the Bell's `answer` writes the text into `rings` and nowhere else. The frontier question's hint is right:
the generalisation is **the ring as ANY obligation**, and the design decision is WHERE the generalisation lives.

**Decision: the Bell is the agent's INBOX, and a ring carries where its answer goes.** Not: a resident that
knows N object shapes (a hole reader, an offer reader, an activity reader), each a shape predicate and a printer
with its own theorems over `Prog`. Instead a ring is `(text, reply-to)`, where `reply-to` names a target object, a
grant the Bell object holds on it, and the fields the target's method wants beside the text; `answer` records the
text in `rings` as today AND returns one typed nested call to the target (LANG-77's `invoke` slot: the Bell
computes the call from the value it judged). The kernel derives the nested call AS THE BELL OBJECT
(`callStep sub obj`, READ `Derive.lean:203-210`; `invokeRun … actor := obj`): an object may be a grantee, so the
hole's owner grants `[invoke propose]` on the hole TO THE BELL, and the Bell's forward is authorised with the
hole owner as principal. **Answered ⇔ delivered, in one Turn** (`invoke` derives the tree atomically; a target
that refuses refuses the whole answer, and the ring stays pending by name). The resident does not change: it still
reads `pending` at the same row type, asks once, keeps, invokes `answer` with the same argument, and every theorem
of the HOSTING stack (`tick_counts`, `bell_resident_conforms`, `delivered_answer_committed_strong`,
`answered_row_is_kept_answer`) stays as it is, because the generalisation is a second RELATION of the Bell
(`targets`, keyed by the ring's key, written by the ringer) and a `(reads (targets (points 1)))` plus a call slot
on `answer`. The first obligation beyond the ring is **a text hole the agent proposes into** (`Std.hole` at
`V := bytes`; DESIGN-CTX §4's document section), and its receipt is the candidate row `by = <the agent's member>`
in the hole's `candidates`, justified by the fact `(cell = the Bell's grant on the hole, pin)` that the sponsor
posted: **revoke the grant and the candidate is `suspended "support0 dead"` on the next `rejudge`, and a `select`
of it refuses by name** (`holeVerdictCheck`, READ `Lang/StdHole.lean:201-212`). That is "the hole it filled is
re-judged when its support is withdrawn", delivered by machinery that exists.

**What is built in this lane, in order** (§8): A0, the resident's provider is a REAL model (the Anthropic
API through the deployed keybroker, pinned, charged, in an opt-in launcher row that checks the receipt row and
the budget charge: a cap sized for exactly one ask makes the second ring's answer `(refused overSpend)`); A1,
the Bell with `targets` and the forwarding `answer`; A2, the hole row: a chooser summons the agent for a text
hole, the model's text lands as a candidate, the chooser revokes the Bell's grant, the candidate suspends by name.

**The price**, said out loud (§6): the Bell re-emits (a `hosting:`/`lang!` flag day of one package: its id moves,
the resident World re-geneses, which is free); `Lang/Proofs/Bell.answer_run` and
`Hosting/Proofs/BellRow.answered_row_is_kept_answer` RESTATE-MEANING ("makes no calls" becomes "makes the call
`targets[k]` names, or none"); the meter stays broker memory, so the World holds the agent's CAP and not its
SPEND (§6.3: the one thing a supervisor cannot read from the World today); a target's refusal stalls the agent's
queue until the ring's patience (§6.4, with the LANG change that fixes it: a ringer may always withdraw its own
ring).

**The one way it is wrong** (§7): if obligations turn out to need the AGENT's judgment about WHICH act to take
(fill this hole, or decline; judge this offer fair, or not; propose this law, or a weaker one), then "the ring's
reply-to is fixed by the ringer" is the wrong grain: the agent can only say text into a slot someone else aimed.
The measurement that decides it is in §7; the design that replaces it (a typed response the Bell cases on) is
A3, and it is a strict extension of this one, not a different mechanism.

---

## 1. What exists (MEASURED, so nobody rebuilds it)

| the member property | where it is true today | the theorem or row |
|---|---|---|
| a key the agent cannot read | the resident's member seed lives in nd-members' workspace (`/srv/nd-members/l/members/<id>`), outside the hosted tree; the resident signs by sending argv over its member socket to `nd --stdio` (HOSTING-20/32) | `Proofs.Plan.plan_outside_members`, `roots_disjoint`; the sandbox plant (HOSTING-5) |
| a provider key it cannot read | keybroker holds `KEYS`; Lean prints the upstream body from typed fields; the key is added by Rust after the verdict; a reply holding the key is `keyEchoed` before the resident sees it (HOSTING-12/29) | `body_tooth` (READ HOLISTIC-HOSTING §1e); resident_bell's control: the key in no file of the volume |
| a budget it cannot exceed | one meter per (resident, model) from the World's `allowance` objects owned by the operator (HOSTING-13); worst case charged before the call; a restart or a changed allowance forfeits the window | `capped_decide` (`Hosting/Proofs/Broker.lean:207`), `start_window_refused` (:267), `capped_follow` (:180) |
| at most one charge per obligation | the intent is kept durably BEFORE the ask; a kept answer is delivered, never re-asked, across failed invokes and restarts | `tick_counts` (ResidentRun), `bell_resident_conforms` (BellConform:356), `keep_atomic`/`resume_durable` (ResidentVolume); resident_bell Q6 |
| laws that bound what it may do | the Bell's `answer` checks `req.agent = state.resident`; the `rung` guard refuses a second answer and a text that is not the ring's (LANG-59); the `bell` law fixes the resident; the kernel's owner authority gates every `invoke` by the grant's rights (KERNEL-25) | `bell_monitored` (`Lang/Proofs/Bell.lean:61`), `resumes_resident`; resident_bell Q3/Q4 |
| receipts for everything it did | every answer is a signed Turn journaled on the member's own World, and the `rings` row is what that Turn wrote; the row is readable by any member with `observe` | `delivered_answer_committed_strong` (SocketStrong:640), `answered_row_is_kept_answer` (BellRow:149) |
| it cannot lie about what it did | it cannot sign: `nd --stdio` signs only what the member's own follower admits (consent before signature), and the Host admits only what the laws in force admit | TOPLEVEL §4 (`settle_final_never_admits`), §3 (`Integrity.law`) |
| an obligation it cannot ignore forever is retired by anyone | `(patience 2048)`: from `notBefore + patience` anyone retires an unanswered ring with its cursor row (LANG-76) | `waiting_retire_after_deadline_admitted`; resident_bell Q7 |
| no refusal is retried forever | `retriesMax` ticks in a row ended on a retry end the resident `retryExhausted` by name (HOSTING-48) | `no_refusal_repeats_forever`; resident_bell Q8 |
| the provider is real | `Broker.providerOf` names `api.anthropic.com` for every `claude-*` model; `deploy/tls/pins` holds THE PIN (OPS-19, valid to 2026-12-20); keybroker verifies the chain and the leaf's SPKI before a request byte (HOSTING-15/28) | `Hosting/Pins.lean`; what stands between the deployed resident and a model is the operator's key file (HOSTING-27 "What stands between it and a real model") |

What the stub is: `launcher/tests/common/mod.rs` `REPLY = b"hello back"`, a FAKE TLS provider the test's own PKI
signs, pinned by the test (`Pki::pin`). HOSTING-27 rules "the real upstream is never in a test". A0 keeps that
rule for the STANDING rows and adds one opt-in row that is not in `gates/runs.tsv` (§8).

What the ring IS, in the slot vocabulary (DESIGN-CTX §2.1): a cursor row of `Std.activity` whose chooser is the
resumer (the resident), source `posted` (the ringer's insert), justification "the ring is still pending at its
key" (the `rung` guard compares the row as it is: a conditional write), acceptance "the text is the ring's own",
life affine (answered once), patience 2048. The Bell is an activity with one plan `ask : (text) → bytes`.

## 2. The agent as a member: custody, confinement, identity

**Custody (the pause list's first item, answered by the existing cut).** The agent process holds NO key: not its
member seed, not the provider key. It holds two Unix sockets. Its member seed is nd-members' (`--init-hosted`:
one record, no holding directory, so the resident's key cannot rotate and needs no removable medium); its
provider key is keybroker's. The LLM call is the provider the resident asks THROUGH the broker; the broker is the
confined process the brief asks about, and the resident is a second confined process under it. Nothing here
changes. What A0 adds is only the operator's act HOSTING-27 names: a key file. (For the opt-in row the key file
is the test's, placed under a custody-clean directory at mode 0600 for the row's life and removed after; the
value is never printed and never enters the repository.)

**Identity in the World.** The agent is `state.resident` of its Bell: a member digest. The grain
(`world/grain/Lifecycle` with `kind resident`) is the PROCESS; the member is the PRINCIPAL. Two agents are two
grains, two members, two Bells, two allowances. A human supervises an agent by owning its Bell (the `bell` law
keeps the resident fixed; `open`/`close` are the owner's), owning its allowance (`set`/`revoke`), and owning the
grants that name it. Nothing new.

**Confinement.** `Plan` is a total function of (store label, grain): package read, volume read+write, the two
sockets, nothing else, and the launcher transcribes it (HOSTING-4/5). The agent cannot reach another grain's
volume, any Store, or any member's workspace, by construction (`roots_disjoint`) and by the sandbox plant.

## 3. The laws that bound it, as the kernel and the packages state them

1. **Budget.** `Allowance` per (resident, model): `cap` per `windowMs`, `maxTokens` per ask, a price. The
   charge is `cost a (body.size + maxTokens)`, worst case, final (HOSTING-12). An agent with no allowance is
   refused `noAllowance`; past its cap `overSpend`; a restart forfeits the window. The World holds the CAP.
2. **Patience.** An obligation it does not discharge is retired by anyone at `notBefore + patience`; the
   resident's own delivery of a retired ring is refused and judged by the rows (`deliver_gone_continues`).
3. **Which objects it may invoke.** Exactly the grants that name its member, with their counted rights: its
   Bell's `answer` (`invoke:0` through the operator's grant). With A1 the Bell OBJECT holds further grants (on
   targets), so the agent's reach is the Bell's grant set: a human grants and revokes it per target, and the
   kernel refuses a forward to a target the Bell has no live grant on (`noGrant`), which refuses the answer.
4. **What it may offer.** Nothing by itself: an offer is a `Std.offer` method of an object the agent would need
   `[invoke offer]` on. Under A1 a ring whose target is an offer book's `post` is how a human lets it offer: the
   human aims the slot, the agent fills it. (§7 is where that grain is questioned.)
5. **Rate.** The kernel's refusal budget per window (KERNEL-44) is the member's rate limit; the Bell's
   `(limits 64 1024)` bound the inbox; `retriesMax` and `tickMs` bound the process.
6. **Truthfulness.** It has no way to write anything but through methods the laws judge; its answer text is
   bounded to 1..2000 bytes at a UTF-8 boundary (`fit`), and a refusal or lost reply is answered by a NAMED text
   (`(refused NAME)`, `(unanswered WHY)`): the World sees that the agent did not get a reply, by name, rather
   than a plausible invented one (law 7 at the agent's grain).

## 4. The ring generalised: the Bell as inbox, reply-to, the forwarding answer (A1)

### 4.1 The package change (`world/resident/Bell.ob`, `Lang/Bell.lean`; AGENT's files)

```
(package
  (doc …)
  (state (rec (open bool) (resident digest)))
  (activity pending rings (limits 64 1024) (patience 2048) …)         ; as today
  (rel targets (key (notBefore nat) (agent digest))                    ; NEW: one row per ring that wants its answer forwarded
       (val (rec (cand digest) (s0 (opt (rec (cell digest) (pin digest)))) (s1 (opt …)) (target digest) (via digest)))
       (limit 64) (guard aimed))
  (method ring (arg (rec (text (bytes 1 2000)) (to (opt <targets val>)))) (edits 3)   ; the ringer may aim its ring
    …start_ask…, and with (some t): (insert targets key t))
  (method answer (arg <unchanged: notBefore ringText ringer text>) (reads (targets (points 1))) (calls (invoke T)) (edits 3)
    (check (deq req.agent state.resident) "notResident")
    (case rows.targets.p0
      (none _ (done state <the two edits as today> (no call)))
      (some t (done state <the two edits> (retract targets key)
                 (invoke t.target propose (record (cand t.cand) (s0 t.s0) (s1 t.s1) (value arg.text)) budget t.via)))))
  (law bell …))
```

`T` is `propose`'s argument type at `V := bytes`: `(rec (cand digest) (s0 (opt (rec (cell digest) (pin digest))))
(s1 (opt …)) (value bytes))` (READ `Lang/StdHole.lean:262-263`, `proposal`). The `aimed` guard: a `targets` row is
inserted only by its key's signer (the ringer: `(deq key.agent req.agent)`), never upserted, and retracted only
by the resident (the answer's third edit) or past the deadline (so an abandoned ring takes its target with it:
`retire` gains the third edit under the same `activityDue` arm). `answer`'s check that the text is the ring's own
stays the `rung` guard's; the forward's `value` is the same `arg.text` the row records, so **the candidate the
hole receives is byte for byte the text `rings[k]` holds**: a reader of the hole can check the agent's candidate
against the agent's own log. That is the receipt of the forward, and it is the kernel's (one Turn, two objects).

What the Bell does NOT do: choose the target (the ringer did), choose the candidate id or the justification (the
ringer did: `cand` is the ringer's name for this filling, so a second summons for the same hole uses a fresh
`cand` and the first candidate stays, with the reason it was set aside), or read the hole (the Bell has no
read of the hole; the hole's own `propose` judges the candidate under its facts, LIVE).

### 4.2 Why the forward is a nested call and not a second obligation kind in the resident

- The kernel already makes "answered ⇔ delivered" atomic for a tree (`invoke` derives `calls` depth-first in
  one Turn; a refusal anywhere refuses the Turn). A resident that answered first and proposed second would need
  a second intent file and a second exactly-once argument per target kind.
- The nested call runs as the Bell OBJECT with a grant the human gave the Bell (`invokeRun … actor := obj`,
  `ownerAuthority … via`). So the AGENT's reach is a set of grants on an OBJECT a human owns: revocable per
  target, visible in the World (a grant is a cell), and never the agent's to widen.
- The resident stays what HOSTING-42..51 proved it is. `Cmd.argv`'s invoke prints the same `answerArg`;
  `Shape.read` checks the same `answerArgTy`; `pendingVal` is unchanged. What changes meaning is the LANG
  witness of what `answer` writes (§6.1), not the Hosting order theorems.
- It composes: a target can be a hole's `propose`, an offer book's `post` (A3's typed response), an activity's
  `resume_<plan>` on another object, or ANOTHER AGENT's Bell (`ring` takes `(text, to)`: an agent summoning an
  agent is a ring whose target is a Bell, and the chain is bounded by the kernel's `revisited`/`callsMax`/pool).

### 4.3 What the kernel admits, what the member signs, what a receipt says (DESIGN-CTX §2.2's three questions)

The agent signs: `invoke bell answer {k, ringText, text} --via gb`, pins `pending[k]`, `rings[k]`, and (NEW)
`targets[k]` and whatever the target's declared reads need (the hole's three `facts` points), derived by the
client from the call's declared reads (`derivePins`; INFERRED that nested reads are derived too: FABLE-T's LC
rows ran nested calls over the Sim with `pinsFor`, and A2's row is where this is measured over `nd`).
The kernel admits exactly when: the signer is the resident (`answer`'s check), the ring is pending and the text
is its own (`rung`), the Bell holds a live grant on the target with `[invoke propose]` (`ownerAuthority`), the
hole is not closed and the candidate key is free (`propose`'s checks: `closed`, `keyTaken` via the candidates
guard), and the hole's facts the candidate cites are observed (`unpinned support0` otherwise: the client learns
the pin to add from the refusal, LANG-79).
The receipt: the journal entry of the Turn (`answered_row_committed` over `ReachOn`), the `rings` row (the
answer), and the hole's `candidates` row (`by` = the agent's member, `value` = the same text, `status` as judged
at insert). A supervisor reads all three with `nd read`.

## 5. Supervision: what a human does, and what the World shows

- **Reads its receipts**: `nd read BELL rings 64` (every answer, keyed by ring), `nd read HOLE candidates 64`
  (every proposal with its status and reason). The agent cannot write either row except through the methods the
  laws judge; it cannot delete a row (an answered ring is retired only by the owner's `retire`).
- **Revokes its grant**: revoke the Bell's grant on the hole (the kernel's grant revocation; the grant cell
  becomes a tombstone). From then on: the Bell's next forward to that hole is refused `noGrant` (the answer is
  refused; the ring stays pending by name); the candidates it already proposed whose `s0` cites that grant cell
  read `support0 dead` LIVE: `rejudge` records `suspended "support0 dead"` and a `select` refuses by name
  (`holeVerdictCheck`). **The hole it filled is re-judged when its support is withdrawn**, with nothing new.
  The sponsor posts that fact once: `post {cell = <the Bell's grant on the hole>, pin}` (anyone with
  `[invoke post]`), and names it in `ring`'s `to.s0`.
- **Revokes its allowance** (`revoke`): every ask is `noAllowance`, every ring is answered `(refused
  noAllowance)`: the agent keeps answering, by name, with no model. Or `close`s the Bell: no ring lands.
- **Retires it**: `stop` the grain (Lifecycle), `remove` it: keybroker closes its socket (HOSTING-26); its
  member stays a member (nothing retires a member: KERNEL-17) with nothing it may invoke once its grants are
  revoked.

## 6. The price

### 6.1 Theorems that change meaning (the flag day's map lines, INFERRED before the build; the build measures)

- `Lang.Proofs.Bell.answer_run`: RESTATES-MEANING. Today: "a returning run of `answer` … makes no calls, and its
  row acts are exactly the upsert and the retract". After A1: "… reads `targets` at the key; with no row, makes
  no calls and those two acts; with a row `t`, those two acts, the retract of `targets[k]`, and exactly one call
  `invoke t.target propose {t.cand, t.s0, t.s1, arg.text} budget (some t.via)`".
- `Lang.Bell.answerTy`, `answerBody`, `answerEdits`, `shapeOk`, `rels`, `E`: definitions restated (the witness
  names the new relation and the call slot); `Hosting.Resident.Bell.bellCore` consumes `shapeOk` unchanged.
- `Hosting.Proofs.BellRow.answered_row_is_kept_answer`: its third conclusion quotes `answer_run`'s "makes no
  calls": RESTATES-MEANING with the call conjunct. `delivered_answer_committed_strong` is unchanged (it is
  about the call the member signed, not the tree).
- `Hosting.Proofs.SocketStrong.describe_shape`: unchanged (reads the ARG type, which does not move).
- `Lang.Journey` LB rows and LBw: `shapeOk` of the re-emitted core (the lang-journey re-reads); resident_bell's
  `conf`/`bell_state` unchanged; its `ring_op` sends `(record (text …) (to none))` after A1 (`ring`'s argument
  type gains `to`): one line.
- Re-emit: `world/resident/Bell` (the core text; its package id moves); a resident World holding the old Bell
  re-geneses (free). No wire kind, no codec vector, no kernel change.

### 6.2 What it does not change
The resident exe, its argv, its config, its volume format, the broker, keybroker, the units, `Plan`.

### 6.3 The meter is not in the World (named, not solved here)
The agent's SPEND is broker memory (`Meter`), rebuilt at each broker life from the World's allowances with every
window forfeited. A supervisor can read the agent's CAP in the World and cannot read what it spent; the only
World-visible trace of an ask is the answer text (a `(refused overSpend)` answer is how the World learns the cap
was hit). Making the spend a World row needs a signer: the broker would post `spent` rows as the operator's hosted
member (a second `--init-hosted` record for keybroker's decider), one Turn per window roll, not per ask (O(windows),
and the per-ask count stays the broker's). That is a custody decision (a signing record in the key-holding
process's decider; the pause list's first item) and is Ember's: filed as the next step A4, not built.

### 6.4 A target's refusal stalls the queue until the patience
HOSTING-27 chose `answerRefused` to stop the WHOLE queue, because every refusal then known refused every ring
alike. With A1 a refusal can be the target's (`closed`, `keyTaken`, `noGrant` after a revoke), which refuses one
ring and blocks the rest behind it for up to `patience` heights (2048), until anyone retires it. Two fixes, the
first built with A1 (AGENT owns `Lang/StdActivity.lean`): **a ringer may always withdraw its own unanswered
ring** (a `notYours`-style arm on the log's unanswered-retract: `key.agent = req.agent` admits before the
deadline; the cursor's `activityDequeue` likewise). Then the human who aimed a ring at a closed hole retires it
at once. The second, later: a refused marker so the resident skips one ring (needs a kept per-ring state, a new
exactly-once argument; not this lane).

### 6.5 What A1 costs in Lang the AGENT does not own
Nothing: `Std.hole`'s `propose` is called as any grantee calls it. If DESIGN-CTX's `Req.caller` (K1) lands, the
hole could refuse a `propose` not made by a named Bell; that is CTX's and is welcome.

## 7. The one way this is most likely wrong

**The agent only speaks text into a slot a human aimed.** Under A1 the agent decides nothing about WHERE its
answer goes or WHETHER to answer: the ringer fixes the target; the agent fills it with text. If the obligations
nano members actually want from an agent are judgments that CHOOSE (fill or decline; fair or unfair; this
candidate or that), the inbox grain is too coarse: the agent would have to encode a decision inside a text the
target then parses, which is a twin of the type system in a string (law 1, at the worst place).
The measurement: after A2, the row where the model is asked a yes/no question about an offer and the target
wants `(enum yes no)`. If the only way to deliver it is a text the target's method parses, this design is wrong
at that grain. The repair is A3, a strict extension: a ring's plan gains a declared RESPONSE TYPE (the activity's
`resp`, already in the generator: `(plan ask (arg …) (resp bytes))`), the resident reads the model's text at
that type with `Lang.Read.readData` (`responseUnread` by name when it is not a value of the type: answered as a
named text, never a guess), and `answer` cases on the typed value to build the forward. The inbox, the
reply-to and the atomic forward are unchanged; only the text becomes a value. If even that is not enough — the
agent needs to PLAN (several acts, ordered, conditional on reads) — then the agent needs a program of its own,
which is axis 1's question (a package the agent installs, judged by the kernel), not this axis's.

A second, smaller way: `cand` chosen by the ringer makes a second summons produce a second candidate, so an
agent cannot REVISE a filling (the hole's `select` by the chooser is the revision). If revision by the agent is
wanted, `cand` should be a function of `(hole, agent)` and `propose` an upsert the `proposed` guard admits for
the same `by`; that is CTX's guard and is named here, not changed.

## 8. The sequence, and what each step makes true

| step | what the World can then do that it cannot now | needs | size |
|---|---|---|---|
| **A0 — a real model answers a ring** | the deployed resident, keybroker and decider, THE PIN, the Anthropic API: a ring is answered with a model's words; the row reads the `rings` row (the receipt), the broker's grant count, and the budget: a cap sized for one ask makes the second ring `(refused overSpend)` by name | the operator's key file (the row's, opt-in, never in `gates/runs.tsv`; HOSTING-27's "never in a test" stands for the standing set); a one-line change nowhere | hours |
| **A1 — the inbox: `targets`, the aimed ring, the forwarding `answer`; a ringer withdraws its own ring** | a ring's answer is delivered to a target object in the same Turn; the agent's reach is the Bell's grant set | `world/resident/Bell.ob`, `Lang/Bell.lean`, `Lang/Proofs/Bell.lean`, `Hosting/Proofs/BellRow.lean`, `Lang/StdActivity.lean` (the withdraw arm), journey LB; re-emit the Bell | a day |
| **A2 — the hole the agent fills** | a chooser summons the agent for a text hole; the candidate lands `by` the agent with the Bell's grant as its support; revoke the grant and it suspends by name; `select` of it refuses by name | a `Std.hole bytes` text installed over `nd` (CTX is making `world/doc/*`; A2 generates its own in the row until then and consumes CTX's when landed); `launcher/tests/agent_hole.rs` | a day |
| **A3 — typed responses** | the model's text read at the plan's `resp` type; a target that wants `(enum yes no)` gets a value, not a string to parse; `responseUnread` by name | `Hosting/Resident/Bell.lean` (`Read.readData` at the response type read from the description), `Lang/Bell.lean` | days |
| **A4 — the spend in the World** | a supervisor reads what the agent spent per window | a signing record for the decider (Ember's custody decision, §6.3) | a week, after the ruling |
| **A5 — any activity, not only the Bell** | the resident serves every `Std.activity` object whose resumer is its member, through the generated `resume_<plan>` | `Shape.read` over `resume_*` lines; `Prog`'s `Ring` generalised to a cursor row; the HOSTING proof stack restated | weeks; only if A3's measurement says the Bell is not enough |

## 9. Literature (where each piece sits)
- Agent as principal with brokered capabilities: object-capability discipline (Miller 2006), the secretless-broker
  pattern (HOLISTIC-RUST §1.5), Sandstorm grains; against MCP's tool model, where the model process holds the tools.
- Exactly-once obligations: write-ahead intent + conditional write at the receiver (Gray/Lampson; Verdi's dedup
  transformer; HOSTING §1c); here extended across two objects by the kernel's atomic tree.
- Beliefs as justified cells: de Kleer's ATMS (the candidate's supports; `support0 dead` is a retracted
  environment), Doyle's TMS; DESIGN-CTX §1.1 for the nano instance. The agent's proposal is an argument with a
  support (its grant) that a chooser may attack (prune) or accept.
- Accountability: every act a signed Turn in an audited log (PeerReview, Haeberlen et al. 2007; SUNDR); the agent
  cannot equivocate because it cannot sign outside its follower's consent.
- Economics: pessimistic reservation metering (ERTP purses), the refusal budget as a rate limit (KERNEL-44), the
  patience as the deadline that bounds how long an obligation may be owed (LANG-76).

## BUILT — appended per landing (the design memo is the record)

- **A0 LANDED** (main 16d0c23, HOSTING-52): `launcher/tests/agent_real.rs`, opt-in, never a standing row. MEASURED on hbox:
  GREEN in 37.2 s; `R1: the model answered "pong"`; `R2: the second ring was answered "(refused overSpend)": the cap of 600
  held`. One finding worth the design's §1: the "stub" was the test suite's; the deployed provider was real all along.
- **A1 BUILT to the witness, not landed; §4.1 is superseded on one point.** The `targets` relation does not fit under
  `eventBytesMax` (MEASURED 88,007 / 74,402 bytes vs 65,536: `E` is copied into every `done`/`refuse` annotation), and a
  declared point read with no pin reads `none` silently (`Lang/Rel.lean:256`): a fail-open forward. The aim is instead
  the ring's CAPTURED value (`ask : {text, to : option Aim} → bytes`), immutable with the ring under the existing `rung`
  guard (the resident must echo it), and `answer` cases on its own argument. Package 57,957 bytes, `shapeOk` true of the
  re-emitted core, `Lang.Bell` green. Everything else in §4 stands (the nested typed call, the Bell as grantee, the
  support `(cell = pin = via)`, answered ⇔ delivered). The consumer list and the landing recipe are in
  `codex/FABLE-AGENT.report.md`; the WIP is `codex/FABLE-AGENT-a1-wip.patch` and hbox `wt/fable-agent`.
- §6.1's map gains: `Lang.Bell.askCaptured/plans/pending/rings/rels/E` (the capture's type moved), `Hosting.Resident.pendingVal/
  Ring/answerArgTy/answerDatum/keptTy` (the resident reads and keeps the aim), and the resident's `invokeArgv` does NOT
  change (no pin: the guard is the check). §6.4's A1b (a ringer withdraws its own ring) is the next landing after A1.
- **A1 LANDED** (FABLE-AGENT-2; HOSTING-53; main **c4800fb7**): the inbox as the capture, not the
  `targets` relation. MEASURED on hbox: `Lang.Proofs.Bell.answer_run` concludes the forward by the echoed aim (the exact
  `invoke tD method ab 100000 (some vD)`, `ab` the bytes of `proposalData cand via y`); `answered_row_is_kept_answer`
  carries it to the resident's journaled call; `Hosting.Resident.answerArgTy` IS `Lang.Bell.answerArg` (one definition);
  the resident's `Ring` holds the aim and the kept file round-trips it; lang-journey GREEN with the new LI rows
  (`Lang/Journey/Inbox.lean`): the Bell object granted `propose` on a document section, the dropped aim refused
  `rung: text`, the echoed aim delivered as the section's candidate (`verified`, `by` the RESIDENT: `req.agent` is the
  signer, the authority the object's grant: §4.3's "by = the agent's member" measured TRUE, §4.2's "as the Bell OBJECT"
  is the authority, not the agent field), selected, revoked → `suspended "support0 dead"`, `select` refused, the next
  aimed answer refused `missingCell` (not `noGrant`: a tombstoned via) with the ring left pending; rows ALL PASS;
  resident_bell ok (312 s). §6.4's first fix (A1b) and §8's A2 are next; A2 measures the nested pins over `nd`.
- **A1b BUILT, in the judge** (FABLE-AGENT-3; LANG-97): §6.4's first fix, with one correction to §6.4's wording. "A ringer may
  always withdraw its own unanswered ring" is NOT a law of activities: the offer's session log is an activity whose rows are
  deal records, and a party releasing its own record before the deadline is a different contract. So the withdrawal is a
  DECLARED property, `(withdraw)` beside `(patience n)` (`Std.activityOwn`), default off: the offer, the escrow and
  `Std.hole` are byte-identical; the Bell declares it. MEASURED: the ringer withdraws its unanswered ring at both guards at
  any height (LB10f, LI9c: after the forward refused `missingCell`, the aimed ring leaves at once); everyone else waits for
  the deadline (LB10b/c, LB13f); `WaitingStep` gains `withdrawn` and `waiting_retract_iff` reads admitted ↔ answered ∨
  (withdraw ∧ own) ∨ past the deadline. The second fix (a refused marker so the resident skips one ring without the
  ringer's act) stays unbuilt: the case the inbox creates is a human who aimed a ring at a refusing target, and that human
  withdraws it.
