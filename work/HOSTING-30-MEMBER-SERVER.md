# HOSTING-30 PROPOSED — one per-World member server binds each resident's member socket from the World (HOSTING-9, 2026-10-19)

Status: **design only.** ROOT approved it in principle (10-19). It needs a CLIENT half (CLIENT-8), described in §4, and an OPS half (OPS-5).
Until it lands, RUNBOOK §2a's "start nd-member@ID before the birth" stands.

## 1. The gap

A resident's launch resolves `MEMBER/<dirOf id>/nd.sock`. If that socket is missing, the launch is refused `pathMissing` and the controller counts the exit, so a resident started early can reach `crashLoop` (HOSTING-25 CRITIQUE).

Today the socket comes from `nd-member@ID.service`, which needs two things:
- a per-resident environment file, `/etc/nd/hosted/member-ID.env`, holding ND_MEMBER_WS, ND_FOLLOW_SOCK, ND_GID and ND_PEER;
- an operator who starts the unit BEFORE the grain is born.

keybroker had the same ordering fault for broker sockets, and HOSTING-26 closed it: keybroker asks its Lean decider which resident grains the World holds, at start and every 200 ms, and binds and unbinds to match. This proposal applies the same mechanism to member sockets.

## 2. Decision (proposed)

- **One long-lived process per World, `nd-members`, run as `nd`.** For every resident grain the World holds, it serves that resident's member socket: `nd --stdio` over the resident's own member workspace, under the same confinement nd-member@ gives today.
- **Who is served is the World's, learned exactly as keybroker learns it.** A Lean decider follows the World (HOST's tail, read-only) and answers `residents` with the socket names of the born, unremoved resident grains (`Controller.residentOf`, `Controller.dirOf`). keybroker's decider (`BrokerCli`) already speaks this, with `Track.update` and the theorems `launch_served` and `residents_mem`.
  - The decider here is a new HOSTING lean_exe, `hosting-residents STORE`. It answers only the `residents` request (BrokerWire request 2 → verdict 3: the same frames, codec and bound `residentsMax`), and holds no allowance reader, key slot or clock.
  - It shares `BrokerCli.Follow`, `refresh` and `absorbTurns`. The refactor moves them to a module both exes import, so there is no copy.
  - DeciderExit's codes and names are reused.
- **Bind at birth, remove at removal.** A name newly answered gets `MEMBER/<name>/` (02710, MEMBER's group) and a socket bound by an `nd --stdio` child under nd-supervise's confinement. A name no longer answered has its child stopped (by the child's own handle) and its socket and directory removed.
  - A name whose member workspace `MEMBERS/<name>` does not exist, or fails custody, is not bound. It is reported once per tick change on stderr as `memberMissing <name>`. It is never a fatal end, because one unprovisioned resident must not stop the others.
- **Custody is unchanged.**
  - Each child writes only its own member workspace.
  - Each child hides `/etc/nd` and `/home` (the operator's custody), as nd-member@ does.
  - Each child connects only to `host.sock` and that resident's follow socket.
  - Each socket admits only PEER in GID (`--group --peer`, the same check). The surface is STDIO_VERBS, and custody refuses rotation.
  - One socket per resident; the server holds no seed itself; one resident's child never sees another's workspace (sandbox deny-default, plus the plan's own hiding of `worlds/<l>/members`).
- **Deleted when it lands:**
  - `nd-member@.service`;
  - `/etc/nd/hosted/member-*.env`;
  - RUNBOOK §2a's ordering procedure ("start nd-member@ID before the birth");
  - the race that procedure works around: from then on a resident started before the server binds its socket is refused `pathMissing` exactly as with keybroker (HOSTING-26's race, named and planted). Option (B), retrying `pathMissing`, stays the controller's open option.
- **What stays the operator's** (provisioning, out of scope here): making a resident's member (`nd --init-hosted` in `MEMBERS/<dirOf id>`, `init`, the operator's `enroll`, `grant world … observe`) and its follower (see the open question in §4). The server binds a socket for a provisioned member at the grain's birth. Provisioning must precede the birth, and that is a fact about the World's data, not about a unit's start order.

## 3. What HOSTING ships (when CLIENT-8 is ready)

- **`Hosting/ResidentsCli.lean`**: the `hosting-residents STORE` exe, with root `Hosting/ResidentsMain.lean` (C7). The shared follower lives in `Hosting/Follow.lean`, taken out of BrokerCli.
- **Theorems:**
  - `residents` answers exactly `residentOf` over the followed World (`residents_mem` is restated for the new exe);
  - every launch's member socket name is in the answered set (`launch_member_served`, mirroring `launch_served`).
- **Ops/Units.lean** (OPS-5):
  - a `nd-members@L.service` (User=nd, per World L) replaces `nd-member@`;
  - `RestartPreventExitStatus` comes from the new exe's fatal codes and nd-members' own table;
  - `deploy/units/linux/tmpfiles/nd-member.conf` stays, because MEMBER is still the operator's 02710 root.
- **Rows:**
  - `cargo:launcher:resident` drives the server. The test no longer hand-starts `nd-supervise … nd --stdio`.
  - A resident grain born while the server runs gets its member socket (no restart, no env file).
  - A removed one's socket and directory go, and an `nd` command on a connection still open to it fails (the child is gone).
  - A resident whose workspace is missing is `memberMissing` while the others are served.
  - Plants: never unbind; ask only once; serve an app grain; serve a removed grain.

## 4. The CLIENT need (for CLIENT-8), precisely

**A new binary, `nd-members`, in the client crate** (std only, `sandbox::command`, the mux code nd-supervise uses: no copy).

    nd-members MEMBER MEMBERS FOLLOW HOST_SOCK GID PEER STORE -- /ABS/DECIDER [ARG]…

| arg | meaning |
|---|---|
| MEMBER | the member root (`/run/nd-member`): nd's, group GID, 02710, checked by `custody::check_shared_dir` at start (`memberRoot` fatal otherwise) |
| MEMBERS | the World's member workspaces (`/srv/nd-hosted/worlds/L/members`); `MEMBERS/<name>` is resident `<name>`'s workspace |
| FOLLOW | the root holding each member's follow socket, `FOLLOW/<name>/follow.sock` (§ open question) |
| HOST_SOCK | the writer's `host.sock` (alone in its directory, HOSTING-25) |
| GID, PEER | the hosted group and uid: each socket 0660 group GID admitting only PEER (0600 when PEER is nd's own uid, the one-uid shape: HOSTING-21) |
| STORE | the World's Store, the decider's only readable path |
| DECIDER | `hosting-residents`, started confined (read = STORE, exec = itself) with STORE as its argument |

**What it reads:**
- the decider's `residents` verdicts: `broker_generated::wire::{Request::Residents, Verdict::Residents}` (the emitted codec), at start and every 200 ms;
- `MEMBERS/<name>` (exists, and passes `custody::check_private_dir`);
- `FOLLOW/<name>/follow.sock` (exists).
Nothing else. No env file. No operator list.

**What it does per name:**
- A name that is newly answered and provisioned:
  1. Make `MEMBER/<name>/` at 02710 (as keybroker makes `SOCKDIR/<r>/`).
  2. Bind `MEMBER/<name>/nd.sock` ONLY ONCE THE CHILD EXISTS (CLIENT-28's law: no bare EOF).
  3. Start `nd --stdio MEMBERS/<name> FOLLOW/<name>/follow.sock HOST_SOCK`, confined: write = `MEMBERS/<name>`, exec = nd, connect = [HOST_SOCK, FOLLOW/<name>/follow.sock], hide = `/etc/nd`, `/home`.
  4. Mux that socket's connections onto the child's stdio, exactly as nd-supervise does for its one socket.
- A child that exits is restarted with backoff, never more often than nd-member@'s StartLimit (5 per 120 s), after which that name is `memberCrashLoop` on stderr and left unbound until the next answer change.
- A name no longer answered: stop its child (by its own `Child` handle), unlink the socket, remove its directory.
- Ends by name (an emitted exit table, `Protocol.Exit`-style):
  - fatal: `memberRoot`, `deciderRefused`, `deciderEnded <code>` (passed through like keybroker's), `deciderMechanism`;
  - restart: `deciderSignaled`.

**The Lean plan it renders from:** `Ops.Units` (the unit's argv, in the order above, and the exit table), and `Hosting.memberSock` / `Controller.dirOf` (the socket name, via the decider's answer).
- nd-members never computes a socket name. It binds exactly the names answered, under `<name>/nd.sock` (`Plan.memberSock`, emitted).
- `grain_name_ok` (launcher) refuses any other name `memberRoot`, as keybroker refuses `sockDir`.

**The open question for CLIENT-8 (it decides the FOLLOW argument).**
- Does `nd --stdio` need a follower of ITS OWN member (`host follow STORE MEMBER GRANT`, one per resident, as World::member runs it today)? Or can every resident's nd share the World's one follower?
- If one each: nd-members also supervises one `host follow` per resident. That takes MEMBER_HEX and GRANT_HEX per resident, which must come from the member workspace, not from an env file: a file `MEMBERS/<name>/follow` holding `MEMBER GRANT`, written by the provisioning step, would be the one new datum.
- If shared: FOLLOW is one socket, and the per-resident follower disappears.
- I lean toward shared if follow admits any member's commands. That is CLIENT/HOST's call.

## 5. Critique

- **One process for every resident's socket** is a shared fate: nd-members crashing drops every resident's World access until the restart. nd-member@ per resident isolated that. The children survive a parent crash only if they are re-parented, and then the sockets are orphans that bind nothing new. Restarting the pair is the honest answer, and it is measured in seconds.
- **A second decider following the same Store** costs one tail read per tick. keybroker's decider could answer both, but it holds a key-adjacent position: it is keybroker's child, with the key file hidden. Mixing the member server into keybroker's process tree would put member custody beside key custody. Refused.
- **Provisioning stays manual.** The ordering fault moves from "start a unit before the birth" to "provision a member before the birth". The second is World data the operator writes once, and the server tolerates its absence by name (`memberMissing`) rather than crash-looping the launch.

## 6. Meta-critique

I reached for the keybroker mechanism because it is mine and proven. The pull to resist is building a supervisor of supervisors in CLIENT's crate before the follow question is answered. If followers are per member, nd-members becomes a process manager for 2N children, and the right answer might instead be systemd templates instantiated by a generator from the World. I kept the proposal to the socket-binding mechanism ROOT approved and put the follow question first for CLIENT-8.
