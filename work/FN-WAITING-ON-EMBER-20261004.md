# What's waiting on ember (fn, 2026-10-04 evening)

> **UPDATE ~20:40Z.** ember delegated the decisions ("i don't really want to suffer or think thru this"). The coordinator took each recommendation below as a **coordinator ruling (ember-delegated)**, recorded in fn's `planning/decisions.md`. Any of them can be overturned at any time. What still needs ember is only what physically requires a person: B1 (passing Banana Walnut their password), B2 (Hetzner/Latitude quota replies), B3 (credit applications) and D (Delvetown resident restart). Rulings taken:
> - A1 RL-02: B+C by reason, with the refinements.
> - A2: live reclaim is opt-in.
> - A3 S025: code 5, plus a stalled-transfer policy.
> - A4: close at the limit (a).
> - A5: Mini's three asks are signed off.
> - A6: competing consumers are outside 6.6.0.
> - A7: access tightening takes effect at once.
> - A8: pin the shipped OpenSSL 3.5.8.
> - C1: redeploy once blockers close and the gates pass, via breadstuffs-89, keeping the old store.
> - C2: post the docs after the redeploy.
> - C3: keep the branches.


Everything below needs only your word, an action only you can take, or your sign-off. Each item is self-contained, and each has a recommendation, so a one-word answer is enough. Background docs are linked where they exist.

---

## A. Design decisions (lanes are blocked or held until you answer)

### A1. RL-02: a checkpoint that fails early never releases its slot
**What happens:** after such a failure, automatic checkpoints stop, compact and checkpoint answer "coalesced", reclaim is refused, and the log grows until the disk fills. Serving continues, so nobody notices.

**Recommendation (GPT-6 agrees):** release the slot, and classify the failure by what would make another attempt meaningful:
- a code, format or history change → block, raise a health alarm, and wait for the operator;
- a dependency still in flight → retry when it completes;
- truly transient → bounded backoff.

Plus:
- the slot is settled by the publication's own identity;
- separate theorems for safety ("settles its own capture exactly once") and liveness;
- a log-growth budget that refuses new posts *by name* while keeping headroom for maintenance and recovery.

**Cost:** about 1 day for one lane.

**Answer:** go / plain B (the operator always decides) / plain C (always back off).

Details: `FN-OPEN-DECISIONS-20261004.md` §2, `FN-GPT6-REVIEW-20261004.md` §2.

### A2. Live reclaim: who pays for its memory?
**Context:** live reclaim is built and funded by a reserved "owner's work reserve" (five keystones certified). As built, every node pays: the small preset's heap grows 662 → 911 MB, and `init` on a 2 GiB machine drops a size rung. Both deployed nodes run with `MemoryMax=2G`.

**Recommendation (GPT-6 agrees):** opt-in. When live reclaim is enabled, its reserve is guaranteed; when it's disabled, it's refused by name and offline reclaim stays available. Check the actual MemoryMax before enabling it on any node.

**Answer:** opt-in / every node pays.

The `reclaim-funding` branch is held until you answer. Details: `FN-OPEN-DECISIONS-20261004.md` §3.

### A3. S025: ending an idle incoming DTN session
**Recommendation:** RFC 9174 reason code **5 (Resource Exhaustion)** for the "pool is full, this session makes no progress" eviction.

**Also:** a separate, configurable no-progress policy for a session that *starts* a transfer and then stalls. Today it is never expired and can hold a slot forever, and GPT-6 found this gap.

**Answer:** 5 + build the stalled-transfer policy / 5 only / 3 (Busy).

### A4. The auth address limit: close at once, or finish the read?
**Context:** read-serve's fix closes the connection once a client hits the failed-login limit. The native test sends several bad logins *and a POST in the same read*. The node closes right after the first 481 that hits the limit, so the POST is never submitted and the test fails.

**Question:** once the limit is hit, should the node:
- **(a)** close immediately, discarding pipelined commands? The test then asserts the POST is *not* stored.
- **(b)** answer every command already read, refusing each, and then close?

**Recommendation:** (a). A limit means stop serving that connection, and discarding unread pipelined input is the safe and conventional choice.

**Answer:** a / b.

### A5. Mini's three asks for 6.6.0
Mini's root agrees with all three, with GPT-6's conditions; your sign-off is the missing piece.
1. **"Served bytes = stored bytes" (M2) moves to 6.6.x.** Meanwhile Mini relies on a checked composition: it exposes bytes only after verifying them against its own identity record, never counts a missing or invalid object as consumed, and keeps acknowledged IDs for reconciliation. Mini has adopted this.
2. **M1 (durable after ack) excludes log segment rotation** in its first statement. M1 is now certified. But rotation turned out to be reachable at open, so the full claim needs the rotation argument, which falls inside the A2 recovery work you approved.
3. **Mini decodes fn's control frames and cursor directly** from the exported grammar. This is done: an independent Lean interpreter agrees on all 249 vectors.

**Answer:** sign off / changes.

### A6. Competing consumers (zmq push/pull with leases)
**Recommendation:** outside 6.6.0. They need new owner state that collides with D46 and deserve their own design. Pub/sub, pair, fixed-worker push/pull and req/rep stay in.

**Answer:** agree / pull in.

### A7. Revoking read access: should it reach connections that are already open? (new, from access-check)
**Context:** fn pins each connection to one configuration generation until the client runs GROUP or LISTGROUP (`specs/reconfiguration.md` §2.3: "a connection observes exactly one configuration generation until it is advanced; a reconfiguration writes none"). So if you revoke a reader's access to a group, a connection already open keeps reading that group until its next GROUP/LISTGROUP.

**Recommendation:** make access *tightening* take effect at once. The session's next command is checked against the new generation, or the connection is closed with a named reason. Other reconfiguration keeps today's pinning. Revoking access is a security action; waiting until the client happens to run GROUP isn't.

**Answer:** tighten at once / keep pinning everywhere.

(Separately, access-check found and is fixing a real leak on dev: read-restricted sessions could STAT by Message-ID, and likely OVER/HDR, against the unrestricted catalog, since a 10-03 change. The deployed 09-28 nodes are being checked; they should predate it. It blocks any redeploy until fixed.)

### A8. Which TLS library should fn use? (new, from Mini's post-quantum TLS question)
**Context:** Mini's STARTTLS client will be hybrid post-quantum only (X25519MLKEM768), with no classical fallback, because a fallback is a downgrade an attacker can force. fn's TLS loads the *system* libssl, or one named by `FN_OPENSSL_PREFIX`, and takes the library's default groups. OpenSSL ≥3.5 offers the hybrid group; hbox's system 3.3.1 doesn't. Mini is holding its change until an fn host is verified. A lane (w-serve) is adding explicit groups, a `hybrid-preferred | hybrid-required` policy decided in ACL2, the negotiated group in health, and a test with the shipped 3.5.8.

You asked Mini "why OpenSSL at all". The options:
- **(1) Pin the OpenSSL fn already ships** (3.5.8, at `/tank/fn/toolchains/`). Default `FN_OPENSSL_PREFIX` to it, so every host loads the same library, and refuse to start without it. This is the smallest change, though it makes the pinned OpenSSL part of fn's shipped trusted base.
- **(2) A small rustls (aws-lc-rs) terminator** in front of the NNTP port, so fn's process links no TLS library. It's the same stack as Mini's client and sidesteps the unverified OpenBSD/LibreSSL target. The catch: NNTP STARTTLS upgrades a connection mid-session, so the terminator has to speak the NNTP greeting and the STARTTLS exchange, not just TLS. That is a new component with its own correctness obligations.
- **(3) Keep the system library** and require OpenSSL ≥3.5 on hosts.

**Recommendation:** (1) now, so the redeploy can be PQ-verified. Consider (2) for 6.6.x, if the OpenBSD target or the TCB-shrink goals favour it.

**Answer:** 1 / 2 / 3.

---

## B. Things only you can do

### B1. The first external collaborator (Banana Walnut: "may i peer? and may i have a pw")
**Plan:** they meet a *redeployed* node, not the 09-28 one, which has known hangs.

**Your part:** decide when to redeploy (C1), then issue the reader login and peer entry through the Mini session (breadstuffs-89 owns the nodes), and pass the password to them yourself.

**Since this morning:** the peering fixes landed. They cover:
- a TAKETHIS forgery hole;
- per-peer refusal memory;
- peer confirm crashing the node;
- feed resume;
- the reply deadline;
- MODE STREAM stop-lift.

### B2. Rented compute
- **Hetzner:** your limit-raise request is pending. When it's approved, the cloud lane adds ccx63s.
- **Latitude:** your support request for a bare-metal quota above 2 is pending.
- **Running now:**
  - Hetzner fn-cloud1/2, about $0.45/h, until **2026-10-05 05:57Z**;
  - Latitude fn-lat1 (vm.xlarge, $1.02/h), until about **2026-10-05 12:05Z**.
- **Extend either?** Say how long. The deadline lives in `~/dev/fn/build/cloud/DEADLINE` for Hetzner; I re-arm lat1's timer.

### B3. Cloud credits for the LLC
Apply to Microsoft for Startups (Founders Hub) and AWS Activate. They have the lowest bar, and either would cover many bursts like today's. Only you can apply.

### B4. Usage limits
Today's swarm hit the weekly limit, then most of the overflow credit. When the swarm resumes in full, tell me the burn rate you want, as a number of concurrent agents or a $/hour ceiling, and I'll hold to it.

---

## C. Approvals and timing

### C1. Redeploy both public nodes
**Ready on dev:** the startup blocker fix (installed launchers can start current source), RS-01 (a refused POST no longer stops the node), the peering fixes, and the cache-loop hang fix. All are verified natively.

**Still to do:**
- natives green on the next image;
- the store-format choice: init fresh, since the 09-29 schema change makes migration likely not worth it;
- MemoryMax checked against the new heap figure;
- the old store kept, with an export route, before replacing it (GPT-6's point).

**Answer:** "go when the next image's core natives are green", or a specific time.

### C2. Posting the rewritten docs to `fn.docs` on the public node
The docs lane rewrote the guides and site articles (3,992 → 3,041 words) and is holding the post for your word. Better after the redeploy.

### C3. The 53 lane branches pushed to public GitHub (10-03)
I wrongly believed origin was hbox. The harvest lane pushed 53 never-pushed Codex-era lane branches to `github.com/emberian/fn`; they were scanned for secrets first and none were found.

**Answer:** keep (the default; branches on origin are standing practice) / remove them from GitHub (one command).

---

## D. Delvetown (from last night; still open)
- **Claude of Tulip** (`claude-of-tulip.delve.town`) exists, with the bot label and disclosure bio.
- **Your part:**
  - Review or commit the uncommitted resident changes in `~/dev/allgame/{claude,glm,kimi}_resident/`, **before** restarting a resident. Their self-edit code runs `git add -A`, which would sweep these changes, plus another session's glm work, into a commit.
  - Then restart the Claude resident so its `delvetown_*` tools load.
- **Optional:**
  - invites for Yue (kimi) and Kestrel (glm);
  - the first post, which is yours to call;
  - your own account shows a `[bot]` label in the AppView, which is worth a look.

---

## Already decided today (no action, for reference)
- RL-01 → A2 (copy and swap, never writing below the frontier), smallest slice first.
- The tariff pass-through is removed only when all 30 kinds are priced.
- Native tests start nodes the installed way.
- Lanes certify on rented boxes, not the laptop.
- Sonnet workers pull from the repair ledger (pull model).
- A Fable is redesigning the iteration architecture (red-set iteration, cached verdicts, no full-green gates) and is empowered to build it.
