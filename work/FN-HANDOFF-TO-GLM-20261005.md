# fn: handoff to GLM (2026-10-05)

A self-contained guide for an agent that hasn't been in this session. Read §1–§3 once; each task card in §5 is independent.

---

## 1. What fn is, in one screen

- **fn** is an NNTP news server whose every decision is an ACL2 function with checked theorems (`books/`). A thin SBCL host layer (`host/`, `host/native/*.lisp`) does I/O and calls those functions, and is saved into images. Tests are Python (`tests/test_*.py`), raw SBCL harnesses (`tests/*_raw*.lisp`) and ACL2 test books (`tests/acl2/*-tests.lisp`).
- **Repo:** `~/dev/fn`. `origin` is **public GitHub**, so run `python3 tools/secrets_check.py` before every push. The trunk is **`dev`**, not main. Today's integration branch is `integrate/20261004`.
- **Current state:**
  - dev = `319aee828`, the release `fn 6.6.1-pre (90393a5c0)`.
  - The redeploy packet is green and waits only on ember's go (`build/coordinator/REDEPLOY-PACKET.md`). **Never touch the live nodes:** the Mini root session executes node steps on ember's word.
- **Sibling project:** "Mini" (`~/dev/minidregg`, Lean) consumes fn: its wire grammar, M1 durability and the identity command. Mini is run by a separate Claude session; you don't need to talk to it.

## 2. The rules (binding; they are why the project looks the way it does)

1. **ACL2 decides.** The host may not decide anything a theorem should cover. A new decision is an ACL2 function plus a **keystone** theorem stated about the function the host actually calls.
2. **Statement first, with teeth.** Write the theorem statement before the proof. Every keystone ships `defteeth`: a positive (satisfiable) witness, and one removal witness per hypothesis showing the conclusion fails without it. A vacuous or tautological statement is a defect.
3. **Never weaken a statement, and never revert.** Fix forward. If you can't prove something, file a named **proof-owed** item (`planning/repair/repair.py`) instead of weakening or deleting it.
4. **Representations (D27):** octet lists are for the logical model only. The runtime uses stobj byte arrays, strings and vectors, with a correspondence theorem at each host boundary. No per-octet ACL2 calls or locks in host loops, and no quadratic list operations (`nth`/`append`/`length` in loops). `tools/list_codec_check.py` and `tools/loop_call_check.py` ratchet these.
5. **Limits come from the store profile, not constants** (D27). Exceeding one is refused *by name*.
6. **Accepted, refused and uncertain stay distinct.** Never report uncertain as refused, or anything as accepted unless it's durable.
7. **Git hygiene:**
   - commit named files only (never `git add -A`);
   - never `git stash`;
   - write prose messages to a file and use `git commit -F` (zsh eats backticks);
   - work in a lane worktree under `~/dev/fn/build/lanes/<name>` on branch `lane/<name>`;
   - don't push `dev` or `integrate/*` yourself; leave the branch for the integrator (see §4).
8. **Disk is ember's call.** persvati is at 94% and hbox `/tank` at 81%. Never delete anything outside your own worktree or scratch. If a disk is low, stop writing and say so.

## 3. Machines

| box | use | rules |
|---|---|---|
| **hbox** (`ssh hbox`, 24c / 123G, ZFS `/tank`) | certify, image builds, native tests | Wrap heavy commands in `swarm-build <cmd>`. **One heavy job at a time.** It's shared with Mini: before an *image build* (heavy /tank IO), check whether one is already running (`ps -eo pid,etime,args \| grep -E 'certs.py\|hbox_native\|run.sh'`). The ZFS ARC makes `free` look full; check `/proc/spl/kstat/zfs/arcstats` and process RSS instead. |
| **persvati** | small narrow certifies only | 94% disk: **no image builds**. Check `df -h /` first; you need more than 150G free. |
| **the laptop** | Python, git, editing | **No ACL2 or SBCL builds here** (it's ember's machine). |
| rented boxes (lat1, cloud1, cloud2) | gone | They were torn down on 10-05; commands naming them will fail. |

The key tools, all in the fn repo:
- `tools/proof_repl.py --host hbox` — an ACL2 REPL on a box, for iterating on proofs. Load a book to its end before certifying.
- `tools/farm.py submit hbox --lane --affected-by books/x.lisp` (or `tools/boxq.py submit --kind certify-lane --box hbox --wait -- --lane --affected-by …`) — narrow certify. **A cache-only certify vouches for nothing:** use `--recertify` for your changed books.
- `tools/hbox_native.sh --image-set <published-sha> --overlay <your-sha> tests.test_native_x` — a native verdict for a **host-only** change without building an image (~minutes). It refuses layout and book changes by name; those need an image build.
- `tools/hbox_native.sh attach <label>` — harvest a running or finished native run.
- `tools/host_check.py --load` — every host file loads.
- `make check-fast` — fast static gates (the verdict cache makes unchanged steps instant).
- `planning/repair/repair.py` — the repair ledger: `show/claim/verify/set`. Read `planning/repair/README.md` once.
- `build/coordinator/workq.py claim ID --worker <you> --files a,b` — the cross-agent file lock. **Forbidden-zone files** (`host/native/owner.lisp`, `io.lisp`, `mux.lisp`, `books/definterface.lisp`) must be claimed before you edit them.

Published image sets live on hbox under `/tank/fn/images/<sha>/`. The newest gated set is the release's: `3e53d7bc5dbd72de73042b46e6174d316ef7a63d`.

## 4. How work lands

1. Work on `lane/<name>`, push it, and write `build/coordinator/lanedumps/<name>.md`: what landed with shas, test before → after, certify run ids, and **the exact continuation** for whoever comes next.
2. Add a row to `build/coordinator/HARDEN.md`: branch @ sha, certified (run id), host-ld, natives, what needs judgment.
3. An integrator (Claude) merges hardened branches into `integrate/…`, builds one image, runs the gates and pushes dev. You don't merge into dev.
4. A **red-before / green-after witness** is required for any fix: a test that fails on the old code and passes on the new.

## 5. Task cards (each is independent; take any)

Every card's own **continuation file is the brief**. Read it first; it holds more detail than this card.

### A. Finish the perf batch (span borrow): **good first task**
- **Brief:** `build/coordinator/PERF-REGRESSION-20261005.md` (the diagnosis plus a ranked table) and `lanedumps/span-borrow.md`.
- **State:** `lane/span-borrow` (pushed). Done so far:
  - the span borrow with its theorems (no more per-octet ACL2 calls on the window read path);
  - the 16 KiB ARTICLE quantum with an immediate yield-resume;
  - compressed-window spans;
  - the scaling gate `tests/test_native_scaling.py`;
  - the `loop_call_check` ratchet.
- **Left:**
  - the end-of-batch evaluation: 1 MiB ARTICLE (time to the 220 line and total), OVER over 10k, 1000 POSTs and a catch-up, dev versus the branch, plus an `sb-sprof` profile of a live owner;
  - more hunting from the ranked table.
- **Known overlap:** `serve-next` has uncommitted work in the same files (`page-window-read.lisp`, `page-window-executor-host.lisp`, `extent.lisp`). Note the conflicts for the merger; don't resolve them by deleting.

### B. Verified streaming (the real fix for the quadratic read): Opus-grade proof work
- **Problem:** each window re-hashes the whole protected prefix, so the read is quadratic in article size.
- **Fix:** keep BLAKE3 subtree chaining values at window granularity, so each window hashes only itself.
- **First step:** state and prove the BLAKE3 tree-decomposition theorem (the digest of the whole equals the tree composition of the windows' chaining values).
- **Context:** `PERF-REGRESSION-20261005.md`, `lanedumps/serve-next.md` (the ruling: option (c)).

### C. A2 recovery, head side (RL-01)
- **Brief:** `lanedumps/m1-durable.md`, the "m1-durable-5" section.
- **State:** `lane/m1-durable-5@05dd73a37`.
  - Done: the copy-and-swap recovery and "the open never drops segments", both certified. RL-01 is reproduced on real disk on the base.
  - Left: build the head image (`lane/m1-durable-5-image@587e407ea`), then run the `tools/power_loss.py rl01` head leg plus the eio-only and kill-only controls and the log, recovery, log_compaction and crash_model natives. Also the open-time cost measurement.
- The dm-flakey native needs sudo on a box; persvati has it but is short on disk, so keep scratch under 5G and clean up only your own files.

### D. Extracted core (ship without the ACL2 image)
- **Problem:** since 09-29 the release tarball shipped an extracted bare-SBCL core that dies at load ("Selected ACL2 table metadata is unavailable for FN-CARRIED"). This redeploy ships the ACL2 image instead.
- **Fix:** decide raw-dispatch verdicts in the ACL2 world at export time, each with a digest of the row it judged; the core checks the digests and refuses by name on a mismatch. Then qualify it on smoke, core and peer, with the same pass/fail set as the ACL2 image.
- **Briefs:** `OVERNIGHT.md` ("Added to the queue"), `lanedumps/extract-2.md` / `extract-writable.md` / `extract-gate.md` (another session may have progressed; read them first).

### E. RL-02 (a stuck checkpoint slot)
- **Brief:** `lanedumps/rl02.md`; ruling D52 in `planning/decisions.md`.
- **Gist:** an early-failing checkpoint publication must release its slot; ACL2 classifies the failure (blocked with an alarm / retry on completion / bounded backoff); settlement is keyed to the publication's identity; safety and liveness theorems are kept separate.

### F. Live-reclaim opt-in
- **Brief:** `lanedumps/reclaim-optin.md`; ruling D53.
- **State:** written and REPL-checked on `lane/reclaim-optin@346912687`.
- **Left:** the 60-book narrow certify; natives `reclaim_walk` with `reclaim_live` on and off; the small-preset heap figure must stay at 1068 MB with it off.

### G. Teeth gate
- **Briefs:** `lanedumps/teeth-gate.md` and `teeth-gate-owed.md`.
- **State:** findings went from 160 to 70.
- **Left:**
  - certify `lane/teeth-21` (which includes teeth-62);
  - the stobj and multiple-value witness classes (58 keystones), which need a `books/defkeystone.lisp` change and therefore a world recertify — coordinate before doing it;
  - the remaining mechanical `defteeth`.

### H. Serving reds (next after the redeploy)
- **Brief:** `lanedumps/serve-next.md`.
- **Items:**
  - NATIVE-R2-OVER-PINS-LARGE-ARTICLE: overlaps A and B;
  - r71-F13: with the owner stalled, 29 sockets are accepted against a bound of 4. The accept path should stop at the bound, decided in ACL2, with the public_exposure and tls_handshake_budget natives kept green.
  - Also FILL-PEER-LOGIN-REFUSAL-REASON: the `needs-send` wording.

### I. Catch-up throughput (peering)
- **Problem:** catch-up imports about 35 articles a second, limited by one IHAVE in flight times the commit fsync.
- **Fix:** allow several records in flight before their verdicts, so the committer batches them (exactly-once over a window: design plus proof).
- **Brief:** `lanedumps/feed-pace.md`, the "Next" item.

### J. Smaller items, Sonnet-friendly
- **w-bp:** the remaining `bp_node_native` reds, plus BP-FORGED-SESSION-SENDER-EXIT6 (`lanedumps/w-bp.md`).
- **w-window:** the decoded-window cache web red, with four ranked hypotheses (`lanedumps/w-window.md`).
- **zmq-2:** req/rep plus the `opaque-reply` kind (`lanedumps/zmq.md`).
- **tariff:** the remaining families (`lanedumps/tariff4.md`; the ratchet is `tools/cost_obligations.py`).
- **The repair ledger** has open items by area: `python3 build/coordinator/workq.py next --area <store|serve|owner|bp|peer|reclaim|web|misc>`.

## 6. Where the history lives
- **Decisions:** `planning/decisions.md` (D27 representations, D49 the 6.6.0 goal, D51–D60 coordinator rulings).
- **Tonight's coordination:** `build/coordinator/OVERNIGHT.md`, `HARDEN.md`, `ROLLUP.md`, `REDEPLOY-PACKET.md`, `REDEPLOY-GATES-ANSWER.md`, `PERF-REGRESSION-20261005.md`.
- **Outside review and decision records:** `~/dev/redregg/work/FN-OPEN-DECISIONS-20261004.md`, `FN-GPT6-REVIEW-20261004.md`, `FN-WAITING-ON-EMBER-20261004.md`, `FN-CLOUD-TAKEAWAYS-20261004.md`.
- **Per-lane history:** `build/coordinator/lanedumps/*.md`.

## 7. Traps that cost real time
- A **global rewrite rule** in a widely included book can make unrelated proofs blow up (the may-seal hang: `fn-wg-consp-when-len-positive`). Helper lemmas about `len`/`consp`/`nth` stay `local` or `defthmd`.
- `planning/interfaces.json` is **generated**. Never commit a hand-edit; the image build refuses a stale one, so regenerate it on a run branch.
- The overlay refuses struct and stobj layout changes, new definterfaces and build-time definitions. Those need an image build.
- `test_native_state_checkpoint`'s running-owner compaction case races on re-saved (overlay) cores. An overlay red there is not evidence.
- Never `pkill -f` a pattern that appears in your own ssh command line; it matches itself.
- A background watcher can wake an agent after it hands off. Cancel your waits before you stop.
