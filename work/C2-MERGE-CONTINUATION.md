# C2-MERGE continuation (2026-10-17)

Read this first if you are taking over from C2-MERGE.

C2-MERGE was a lane working for INTEGRATOR-5 and then INTEGRATOR-6. It produced the batch-3
branch `lane/integrator-batch3-c2` = **95fcd260** (pushed to /srv/git/minidregg.git and GitHub).
INTEGRATOR-6 is gating that tip in /srv/lanes/integrator5 on burst5.

## What is on the branch, oldest first

- `69d19a2c` codec(materializer): bookStream carries the floors section. Parent: batch 3 e1d53913.
  Also pushed alone as lane/integrator-batch3-floorsfix.
- `995c2bdb` Merge lane/state-at-c2 f7c998b6 (C2 durable engine, WIP) into batch 3.
  - Loaded holds engine/view AND turn-log's track.
  - rebaseD / entriesOf_rebase are gone.
  - Loaded.prepare gained checkBounds.
  - prefixOwn is rebuilt on resumeEngine.
  - The duplicate replay_model/resume_model in Kernel.SnapRepresents was deleted;
    DurableEngine holds the only copy.
- `611d4e24` gates!(codec-shapes): two changes to scripts/codec-shapes-regen.py.
  - Prefix re-pin rule: a bare `prefix_*` identity re-pins only under an identity bumped in the
    same run, and only if it is never a whole frame. `--selftest` covers it.
  - The `codec-shapes-regen: frozen` marker, placed on Compiler/LegacyStoreCarry.lean and
    Kernel/PayCellLegacyV4.lean.
- `a83d0204` codec!(shapes): 48 identities bumped, pins re-emitted. The full list is in the
  commit message. Hand bumps:
  - RESOURCE/TRANSACTION 10→14 and 13→15;
  - ADMITTED-INPUT-CONTEXT 2→3;
  - ACTIVITY-CELL → /v2, so the framing is now +43;
  - DURABLE.SEED 2→3, with SeedEpoch.retired;
  - clockWireVersion 2→3.
- `e5023a3d` Merge main 92b6e19d (batch 2). It merged clean.
- `4d4ec4f6` cherry-pick of 774455c3 (scripts/pipeline/known-red-verdict).
- `95fcd260` gates(objective): 467 decision lines + pins (--pin, self-tests ON, 0 unadmitted).

Verified state:
- Umbrella + TokenCensus at e5023a3d: the only failure is Fixtures.NativeAcceptedFixture
  (known red, cv 01a146dd).
- TokenCensus is green.
- known-red-verdict says READY.

## Open items (none is done)

1. **Fixtures/NativeAcceptedFixtureData re-emit** (cv 01a146dd). The fixture was already red, and
   it is now staler: its seedHex has seed frame byte 2 (now 3), and its commands use
   RESOURCE/TRANSACTION ++[10] (now 14). Re-emit it with its own authority script
   (scripts/pipeline/check-fixture-authority.sh, fixture-authorities.txt). Then delete its row
   from scripts/pipeline/known-red-modules in the same commit; known-red-verdict refuses a stale
   row.
2. **native/mini-sdk/tests/fixtures/plan.json** has NO generator in the tree. It is a CAPTURED real
   Host `inspect plan` output (5c88af84, lane W2.H, 10-03), and it predates many bumps.
   - Do not hand-edit bytes into it; that would forge a capture.
   - A true re-emit needs a live flow: draft, Host op 7, finalize, then `inspect plan`.
   - The filtered test that reads it passes as is:
     `CARGO_TARGET_DIR=<lane>/cargo-target cargo test --locked --offline -p minidregg-mini-sdk --test golden`
     (4 passed). The explain path does not read the command's hex frame byte.
   - Decide between a capture from a journey row and an explicit "historical capture" label plus
     a cv task.
3. **PersistedCodecTags deletions in a83d0204.** INTEGRATOR-5 accepted these; they are recorded
   here so nobody "restores" them:
   - `durable_seed_byte_v1`: no codec spells the v1 seed frame any more. The `[version]` arm
     refuses it, and seedEpoch_v1_refusedFor is reproved.
   - `requestCodecVersion : Nat := 2`: no codec referenced it. It was reachable only because a Nat
     tag renders as its decimal string, and seedWireVersion/clockWireVersion also rendered "2".
   - Latent census weakness, NOT fixed: Nat identities collide by decimal string. Worth a cv task.
4. **The C2 WIP is still WIP.** state-at-c2's 3 WIP commits (engine, history newest first, C2)
   landed un-squashed with WIP messages. Bench numbers are in STATE-AT-LOG.md "PAUSED 10-15".
   Never claim a grow win: the instruction count moved -0.7%.
   NativeHostReplay extendExactReadback and JointControlBootstrapBundle still call the spec
   prepare (cold paths).
5. **known-red-modules accuracy.** INTEGRATOR-5 wanted it checked; known-red-verdict does that
   now (4d4ec4f6).

## Gotchas a successor must know

- The census is red after any codec-shape change. Use `scripts/codec-shapes-regen.py`.
  - On burst5-a, `/srv/pipeline/slots/with-lean-slot` is a stray copy missing lib.sh, and the
    script uses it if it exists. I ran the script through a wrapper that replaces its build()
    with `/srv/pipeline/scripts/slot.sh swarm-build lake build ...`:
    /srv/lanes/c2-merge/runregen.py.
  - The regen bumps literals only. It cannot handle `s!"...v{n}"` spellings (clock_v3) or
    version bytes; those are hand bumps.
  - It used to rewrite frozen legacy descriptors; the frozen marker now stops that.
- Objective: run `--draft FROM..TO` with OBJECTIVE_SELF_TESTS=0, put decision lines before
  `# ---- history:`, then `--pin` with self-tests ON. Each takes ~15-25 min on burst5.
  My reason generator is /srv/lanes/c2-merge/decide.py (a copy is in the Mac scratchpad).
- Floors removed/restated/redefined decisions are written as MEANING CHANGES (INTEGRATOR-5's
  rule).

## Lane /srv/lanes/c2-merge (burst5-a)

- **src/** is a git clone at 95fcd260 with a warm .lake. Throwaway once the batch lands.
- **Throwaway, mine:** logs/, cargo-target/, *.pid, *.py helpers (resolve, bytebump, actbump,
  seedbump, seed2, framing, reqver, frozen, peek, runregen, decide, mkfix), *msg.txt, *.block,
  fix.index, known-red-modules.mklane.
- **Keep until the gate is green:** logs/ub4.out (the umbrella + TokenCensus log the verdict
  read), logs/objpin.out.
- /tmp/objective-proofs.* dirs (OBJECTIVE_KEEP_TMP) are mine too.
