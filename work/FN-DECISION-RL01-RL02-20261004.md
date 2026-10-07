# Decision brief: recovery after a failed barrier (RL-01) and the stuck checkpoint slot (RL-02)

fn, 2026-10-04. Found by the `read-life` reader lane by mental execution of `host/native/io.lisp` / `owner.lisp` at dev `65389a90e`; neither is reproduced natively yet. Ledger items `planning/repair/items/RL-01.json`, `RL-02.json` on `lane/read-life@8c6d9d0c2`.

---

## RL-01 — after a failed log barrier, recovery trusts bytes that may never reach the disk

### What happens

1. A POST batch is appended to the active log segment and its barrier (`fdatasync`) fails — EIO, or a transient device error.
2. fn does the right first thing: `fnn-log-fence` (`io.lisp:7797-7826`) fences the store and the node exits 3. Nothing in that batch was acknowledged.
3. systemd restarts the node. The open's recovery, `fnn-log-recover` (`io.lisp:7553-7590`), reads the active segment through `read(2)` and validates it.
4. **The trap.** On Linux, when writeback fails, the kernel marks the failed pages *clean* and keeps them cached; the error is reported once and then forgotten (the 2018 "fsyncgate" behaviour that PostgreSQL also had to redesign around). So recovery reads the failed batch from the page cache, finds valid records, and treats them as committed history. The pages are clean, so no later barrier ever writes them; recovery itself writes only the zero tail beyond the frontier before its own `fdatasync`.
5. The node serves those articles, appends new batches after them, and **acknowledges** those new batches with good barriers.
6. On power loss, the disk holds zeros or garbage where the failed batch "was", and valid acknowledged entries after it. The next open refuses `log-damaged`, and the only repair on offer, `--repair truncate`, cuts at the hole — **dropping every acknowledged entry after it.**

That is acknowledged data lost — the one thing fn's whole design exists to prevent (AGENTS.md: "durable acceptance comes only from persisted state"). Mini's M1, durable-after-ack, depends on this case being closed: it's the "indeterminate completion" outcome FLR-002 already names.

The same class appears in two neighbours:
- **Peer feed journals (FNFD):** `fnn-owner-feed-append-locked` fences on a failed fsync, but the restart's `fnn-owner-feed-open` scans frames from cache, and its fsync covers only dirty pages.
- **Checkpoint read-back verification (S045):** `fnn-state-checkpoint-verify` reads the staged checkpoint back from the page cache, so it verifies the encoder, not the disk.

### Exposure

Conditional on a device write error followed by an automatic restart, then a power loss. Rare on healthy hardware, but it is exactly the case the barrier exists for. It is not reproduced; it's Linux-documented behaviour applied to our code path. ZFS (hbox) and OpenBSD (a release target) have different cache semantics, so the fix should not depend on Linux-specific cache control.

### Options

| | what | for | against |
|---|---|---|---|
| **A. Rewrite on recovery** | Recovery rewrites the bytes it validated below the frontier, the same octets it just read, in place, then `fdatasync`. The pages become dirty, so the barrier writes them; if the device is still failing, the barrier fails again and the node fences again (correct). | Filesystem- and OS-agnostic. Provable: a keystone that after recovery every octet below the frontier was written by this run's program before its barrier. One rule closes the log case. | One extra write of the active segment per open, bounded by rotation (the segment is at most K/2). Changes `fn-lg-recover-program`'s byte program — the write is the identity on the byte model, but it must be a step of it. |
| **A′. Rewrite only after an unclean stop** | As A, but only when the previous run ended without a clean shutdown. | Saves the write on clean restarts. | Needs a reliable "previous run fenced" signal, and writing that marker is itself a disk write that can fail in the same way. More states to prove. |
| **B. Read with O_DIRECT** | Recovery reads the segment bypassing the page cache, so it sees what is actually on disk. | No extra write; exact. | Platform-specific: not on ZFS before 2.3 (hbox), not on OpenBSD; alignment rules. A fallback is still needed, so it is A plus complexity. |
| **C. Drop the cache before recovery** (`posix_fadvise(DONTNEED)`) | Evict the file's clean pages so the re-read goes to disk. | Cheap. | Advisory and filesystem-dependent (ZFS's ARC ignores it); not on OpenBSD; a hint, not a guarantee — not something a keystone can stand on. |
| **D. Do nothing; document** | Treat a device error as requiring operator restore. | No work. | Leaves acknowledged-data loss after an automatic restart. Contradicts AGENTS.md and blocks Mini's M1. |

### Recommendation

**A, applied on every open, for the log; and the same rule for FNFD feed journals.** It is the only option that is portable, provable and closes the case without trusting cache behaviour. The cost is bounded and paid once per open. For checkpoint read-back (S045), the honest fix is to **relabel** the verification as an encoder check and move "on disk" verification to the next open, where rule A's re-read-then-rewrite already applies. Don't pretend a cached read verifies the disk.

Statement first (m1-durable's lane holds the context and should own it): after `log-recovered`, every octet below the frontier was written by this process's recovery program before its barrier; with the fence-on-failure rule, an acknowledged record is in the recovered store after any crash cut, including after a failed barrier and restart.

### Decisions for ember
1. **A vs A′ vs B-with-A-fallback.** My recommendation: A.
2. **The cost.** One extra write of the active segment per open. Acceptable? If K is large on some profiles, the lane reports the worst-case open-time increase before landing.
3. **Checkpoint read-back.** Relabel S045's verification honestly (encoder check) and rely on next-open recovery for the disk? Recommendation: yes.

---

## RL-02 — a checkpoint publication that fails early never releases its slot

### What happens

A checkpoint publication captures (sets `fn-owner-sco-inflight` to the capture count, `owner-host.lisp:904`) and then fails before producing its result. The failure is either an `:unencodable` history verdict (`owner-host.lisp:997-998`) or a history image row refused by name (`io.lisp:3683/3713`, e.g. `fn-his-row-begin :refused :pending-suffix`). The "done" step that clears the marker runs only `(when next …)` (`owner.lisp:7224-7228`), so the marker stays set for the rest of the run:
- no automatic checkpoint;
- every `store compact` / `store checkpoint` answers "coalesced";
- a reclaim pass is refused as in-flight;
- the record log grows without bound;
- the next open replays the whole suffix — and may meet the same refusal.

Serving continues and the log line says "CHECKPOINT auto failed", so it is silent in practice until the disk fills.

### Options

| | what | for | against |
|---|---|---|---|
| **A. Just release the slot** | Clear the marker on any early failure. | Trivial. | The due rule re-arms on every count change, so every later POST triggers a full history walk plus log rotation and the same refusal: a work storm. |
| **B. Release + blocked deferral** | Release the slot and record the named refusal as a deferral that blocks automatic publication until the operator asks (a new `:refused` deferral kind, shown in health). | No storm; visible; the operator decides. | An unattended node stops checkpointing until someone acts, while the log grows. |
| **C. Release + bounded backoff** | Release and retry after an exponentially growing number of commits or time, capped. | Self-heals transient refusals. | A permanent refusal retries forever (bounded, but forever), and health must show it. |
| **B + C by reason** | Classify the refusal: transient reasons (e.g. `:pending-suffix`, a suffix still in flight) get C; permanent ones (e.g. `:unencodable`) get B and a health alarm. | Matches the two kinds of failure. | Needs the classification decided in ACL2 (it is a decision, so it belongs there anyway). |

### Recommendation

**B + C by reason**, with the classification an ACL2 decision. Add a keystone for the liveness half the code lacks today — every captured publication releases its slot — plus a health line that names the deferral and its reason. A permanent refusal is a bug signal (history fn can't encode), so it should be loud. The fix is local (disposition LOCAL), roughly a day for one lane.

### Decision for ember
4. **B + C by reason** (recommended), or plain B (operator always decides), or plain C.

---

## Also found, no decision needed

**Retire abandons its final checkpoint** (RET-RETIRE-CHECKPOINT-ABANDONED): a drained retire starts its final checkpoint and then immediately starts shutdown, which abandons it on any store that isn't tiny. The retire lane has confirmed it and filed it; `lane/retire@911c51cad` now asserts that the checkpoint actually completes.

## Who does it
- RL-01: the `m1-durable` lane (Fable), which is proving durable-after-ack over the log kernel and needs this case closed for its theorem — design, keystone, implementation, a native with an injected barrier failure + restart + simulated power loss (`tools/power_loss.py`'s rig can host it).
- RL-02: one Opus lane, or the `read-life` reader's successor from its continuation file `build/coordinator/lanedumps/read-life.md`.
