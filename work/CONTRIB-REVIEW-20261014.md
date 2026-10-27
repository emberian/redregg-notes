# CONTRIB-REVIEW 2026-10-14 — akapug (pug, David Anderson) on emberian/minidregg

Reviewer: CONTRIB-REVIEW (Claude). Read diffs only, nothing built. main = 30a5009a.

Corrections to the brief (measured):
- Only #3 is a PR. **#1 and #2 are ISSUES** (`gh pr list --state all` shows only #3; `gh api .../issues/1|2` has no
  `pull_request`). There is no diff to `git apply --check`; the verdicts below are on the proposals.
- `lane/perf-client` is **not on GitHub**: `git ls-remote origin` (emberian/minidregg) has no `lane/*` refs. It exists only
  in hbox `/tank/dregg-build/claude-lanes/bundles/burst3-minidregg.git` (lane clone `.../claude-lanes/perf-client/src`,
  tip 7cc040d6; H = 22166640). Lane base = perf-fix a16e2f1b (descends from 7dea0626); 30a5009a is not in that repo.
- 7dea0626..30a5009a touches nothing under `native/resource-client` (diff --stat empty), so PR #3 (based on 7dea0626)
  still applies to main as-is.

---

## PR #3 — "resource-client: reuse one storeless codec loop per process"

pug: 1 commit 3b7b8a70 (`akapug <cto@minusculeventures.com>`), +53/-8, `client_consent.rs` only.
Ours: H 22166640, +88/-102 across `client_consent.rs` and `main.rs`.

### What each changes

| | PR #3 (pug) | H 22166640 (ours) |
|---|---|---|
| Process-wide child slot | `CODEC: Mutex<Option<(PathBuf,[u8;32],Session)>>` | `CODEC: Mutex<Option<Session>>` |
| Reuse key | settings **path** + `anchor_binding(executable, settings_bytes)` = image path **+ inode identity (dev, ino, size, mtime, ctime)** + SHA-256 of settings bytes | image **path** + settings **bytes** only |
| Replaced Host image at the same path | detected, new child | **not detected**, old child keeps serving the old image |
| Same bytes, different settings path | new child | reused |
| Failed frame (I/O) | slot dropped | slot dropped |
| Settings changed during the frame | slot dropped + Err | Err, slot kept (harmless: next call's byte compare replaces it, but implicit) |
| A refusal (255 frame) | `round_trip` errs "local consent refused before signing: <bytes>", slot dropped | same child decodes its own refusal (`inspect outcome`, frame 8), records `HostDecision::RefusedFrame`, error `host refused <verb>: <line>; encoded refusal: <hex>` (same as the session path), child kept |
| Unexpected answer byte (not op, not 255) | folded into the refusal message above | slot dropped, explicit "answered frame X to frame Y" |
| No-pins path (`process` -> pure verb without local consent pinned) | **unchanged**: still one-shot `local_process` per verb (pug's "plain" rows show no gain, as they say) | routed through the child too; `codec_process` no longer needs pins |
| One-shot exit-2 handling (`one_shot_refusal` + its 2 tests) | **kept** (still reachable on the no-pins path) | **deleted** (no pure verb reaches `local_process` any more) |
| Tests | `codec_loop_is_reused_only_for_the_same_image_and_settings`: 1 start for ops 7..11, restart on changed settings bytes, restart on image replaced by rename | `one_codec_child_serves_the_process_and_names_its_refusals`: 1 start for 3 frames, refusal named by the child's own decode, same child answers afterwards |

Windows/non-unix: moot for both. `client_consent.rs` already uses `std::os::unix` unconditionally (e.g. `anchor_binding`,
`read_anchor`), so the module does not build off unix today; H's `#[cfg(not(unix))]` Err in `codec_process` is never
compiled. pug's use of `anchor_binding` adds no new portability cost.

### Measurement

- pug: end-to-end, snoopy (AMD 32t), alternating base/fix runs, same tree, only `mini` differs; journey J0-J4 + G(10,50).
  Deployed-path write p50 1.75 s -> 1.36 s (-22%), no-pins path unchanged (expected for their scope); `strace -f -e execve`
  Host execs 284 -> 54, codec starts 277 -> 47. Plus a per-write cost breakdown (useful: their inferred "~145 ms mini
  start = per-process SHA-256 of the 173 MB Host image" is exactly what our G 764d6bb6 removed).
- ours: `strace` census N=4 M=4 K=4, Host execs 216 -> 61 with H (births 7.50 -> 1.00/op, updates 5.00 -> 2.00, reads
  4.38 -> 1.88, setup 5.67 -> 1.00); 45 with G+H+I+L. Covers the no-pins path, which pug's does not. No isolated
  wall-clock number for H alone (box was loaded; stepbench is for the combined lane).
  pug's wall-clock p50 is the better user-facing number for the deployed path; our census is broader.

### Textual conflict

Yes. Both rewrite the same body of `local_frame` (client_consent.rs ~L556-575) and both add a `static CODEC` of different
types. Their test hunk (~L419) does not overlap ours (~L528). They cannot both merge.

### Decision: land OURS (H), folding in pug's reuse key, explicit drop, and test. Close #3 as landed-with-credit.

Ours is more complete (no-pins path, refusal decoding parity with the session path, dead one-shot path deleted).
pug's has three things ours lacks, and all three are right:
1. **Key on file identity, not path.** A Host image replaced in place (a redeploy while a `mini` runs) must not keep being
   served by a child of the old image. `anchor_binding` is already the identity the consent anchor trusts; reusing it
   makes the codec child agree with it. Cost: one `stat` + SHA-256 of the settings bytes per frame.
2. **Settings path in the key**, and **explicit `*slot=None`** when settings change during a frame.
3. **Their test**, which pins the restart cases (changed settings, replaced image) that ours does not test at all.

Also found while comparing (ours only):
4. In H's refusal branch, the decode exchange's error is swallowed by `.ok()` and the child is kept. If that exchange
   fails at the I/O level the child is broken; drop the slot when it errs (the message still falls back to the
   undecoded form via `refused_frame_message(.., None)`).
5. **Test flake hazard once both tests exist**: `CODEC` is process-global and `cargo test` runs tests on parallel
   threads. Two tests driving `local_frame` with different stub executables will replace each other's child, and each
   asserts its own start count == 1. Serialize them with a test-only `static CODEC_TESTS: Mutex<()>` and reset
   `CODEC` at the end of each (pug's test already resets it).

### Integration steps (onto lane/perf-client, hbox lane clone; no force-push of existing commits)

```
cd /tank/dregg-build/claude-lanes/perf-client/src         # tip 7cc040d6
git fetch https://github.com/emberian/minidregg pull/3/head:refs/contrib/pr3   # 3b7b8a70
```
Do NOT cherry-pick 3b7b8a70 (conflicts with H on every hunk of `local_frame`). Write ONE new commit on top of 7cc040d6,
`native/resource-client/src/client_consent.rs` only:
- `static CODEC: Mutex<Option<(PathBuf,[u8;32],Session)>>`; in `local_frame` compute
  `let binding=anchor_binding(&executable,&settings_bytes)?;` and replace the child when
  `path!=&settings||bound!=&binding` (replaces H's `executable`/`settings_bytes` compare; binding subsumes both).
- On "settings changed during codec operation": `*slot=None;` before returning Err.
- In the refusal branch: if the `exchange(session,8,..)` decode returns Err, `*slot=None` (keep the undecoded message).
- Add pug's `codec_loop_is_reused_only_for_the_same_image_and_settings` verbatim (it uses `opcode_stub`/`opcodes`/
  `stub_dir`, all still present after H; `opcode_stub` answers op N with `[N]`, which H's `local_frame` returns as
  `vec![operation]`), and guard it and `one_codec_child_serves_the_process_and_names_its_refusals` with a shared
  test-only mutex; both reset `CODEC` at exit.
- Commit message: subject e.g. `perf(client): the codec child is keyed by the Host image's file identity and settings path`;
  body names PR #3 and its measured numbers (deployed write p50 1.75 -> 1.36 s, execs 284 -> 54, snoopy), what was taken
  (binding key, explicit drop, restart test) and what was not (the one-shot exit-2 path and the old refusal message:
  H supersedes both). Trailer: `Co-Authored-By: akapug <cto@minusculeventures.com>` plus our usual Claude trailer.
- Gate (narrow, per house rule): `cargo test -p minidregg-resource-client codec_` (the two codec tests + `codec_*`), and
  `cargo test -p minidregg-resource-client one_shot` must now match nothing. Control: rerun the N=4 strace census
  (`WLSRC=<wt> wl.sh ... strace` + `execs.py`) and require Host execs == 45 (unchanged from L; the key change must not
  add starts in a run where the image is not replaced).
- When lane/perf-client reaches main: close #3 with the reply below, linking the landed commit and H.

### DRAFT reply to pug (PR #3)

> Thanks, pug. This landed, folded into a change we had in flight for the same cost.
>
> Our lane had already made the same move (one codec child per `mini` process, commit 22166640 on lane/perf-client),
> so we did not merge #3 as-is: both rewrite the body of `local_frame` and they conflict. What landed is ours plus three
> pieces of yours, in <SHA>, with you as co-author:
> - the child is keyed by `anchor_binding` (image path and inode identity) and the settings path, so a Host image
>   replaced in place starts a new child; ours had keyed on path and settings bytes only, and would have kept serving
>   the old image;
> - the explicit drop when settings change during a frame;
> - your test `codec_loop_is_reused_only_for_the_same_image_and_settings`, unchanged, now serialized with our codec
>   test because both use the process-wide slot.
>
> What differs from your version:
> - Pure verbs go through the child on every path, not only when local consent is pinned. Your "plain" rows will move
>   too. The client's one-shot exit-2 handling of pure verbs is gone, because nothing reaches it any more.
> - A refusal keeps the child. The child decodes its own refusal, as the session path does, and the error now reads
>   `host refused <verb>: <reason>; encoded refusal: <hex>`. It used to read
>   `local consent refused before signing: ...`.
> - The same lane also removes the per-process SHA-256 of the Host image (764d6bb6). That is your inferred ~145 ms
>   per `mini` start. `mini` now names the workspace's pinned `hostSha256`. The file is checked when `serve` starts,
>   and on request with `mini --verify-host` or `MINI_VERIFY_HOST=1`.
>
> What your deployment needs to do:
> - If anything matches on the old refusal text, match `host refused <verb>:` instead.
> - If you relied on every `mini` invocation re-hashing the Host image, set `MINI_VERIFY_HOST=1` (or pass
>   `--verify-host`) where you want that check. Replacing the image under a running `serve` is refused at its next
>   start with a pin mismatch.
> - Nothing else changes. The frames, the replies and `deploy/candidate/run.sh`'s env stay as they are.
>
> Your measurements (1.75 s to 1.36 s write p50, 284 to 54 Host execs) are in the commit message. Your per-write
> breakdown is going into our performance notes.

---

## Issue #1 — floors for capped issuance / credit limits / commons recycling; external-effect settlement classes

What it is: a design proposal (no code) from pug's Simbi ClockDAG work, following up an answer Ember gave. It proposes
replacing `sourceSolvent := isIssuerMint ∨ amount ≤ balance` in `Theory/CanonicalResourceKernel.lean` admission with a
per-(account, asset) **floor** (`amount ≤ balance + floor`): 0 = today, L = credit limit, C = issuer-well cap. It also
proposes two theorems (`admitted_preserves_floors`, `outstanding_le_sum_floors`), a `sweep` posting for commons recycling
or destruction, with the decayed display as a view plus a materialization lemma, and, for external effects, a class
1/2/3 taxonomy (keyed-idempotent / readable-state / fire-and-forget). It also proposes the first
`ImplementationRefinement` instance for a keyed toy target, and a `reconcile` transition out of `quarantinedForward`.

Still applies: every cited file exists on 30a5009a, and none changed since the cited 1c7e46da (empty `git diff --stat
1c7e46da 30a5009a` on all five; 1c7e46da is an ancestor of main). `sourceSolvent` is still the Boolean-or shape, used by
CanonicalEscrowMarket, ProviderExecutionLease and PurseRefill. No floor, credit-limit or `reconcile` transition exists in
the kernel today. `ImplementationRefinement` appears only as structure fields in
Assurance/DreggNetProviderConsumer and HyperdocumentAgentOperation, not as a settled instance for
IrreversibleEffectSettlement. The issue's "none exists" claim holds on main.

Twin rule: not engaged. It is all Lean, in the kernel that is the implementation. Their Rust side lives in ClockDAG
(Simbi's repo), not ours.

**Verdict:** a good, correctly-grounded proposal. The floor generalization keeps postings and conservation untouched and
changes only admission, which is the right place for it. `outstanding_le_sum_floors` is the property a mutual-credit
user actually needs. The note on net vs gross issuance (a lifetime gross cap is a counter, not value) is accurate. The
external-effects part matches what the module already says and turns it into a concrete next instance.

**Integration lane would:** add a `floors` parameter to `CanonicalResourceKernel` admission, and prove the
all-zero-floors/unbounded-wells equivalence with today's `sourceSolvent`. Since this is greenfield, it would then
delete the Boolean form, not keep both, and re-check the three consumers. It would add the two theorems as named
theorems with `#assert_axioms`, not `#guard`, and the `sweep` posting plus a worked example book. Then the class-1
`ImplementationRefinement` instance and a `reconcile` transition, with the no-second-effect theorem.

**Needs Ember:** only the design call on whether the floor *replaces* `isIssuerMint`, which changes what an issuer well
means (cap C vs unbounded) for every existing mint site. It is a genuine design fork, not a compatibility worry.

## Issue #2 — "GenericSimplex port to Rust: licence + restart rebase"

What it asks:
1. May they port `Kernel/GenericSimplex.lean`'s rules into Simbi's ClockDAG, which is **Apache-2.0**, as Rust with no
   code copied, and run our Lean `step` as a test-only AGPL oracle?
2. Is rebasing a restarted node at its latest local commit sound in our model ("views ≤ v collapse to genesis =
   committed cut"), or is there a trap?

Facts: minidregg is **AGPL-3.0-or-later** (LICENSE, NOTICE). NOTICE notes earlier MIT-OR-Apache grants only for the two
Hyperdocument native crates. `GenericSimplex.lean` is an executable rendering of a published paper
(arXiv:2609.32985v1, Figs 1,3,4,5) plus our own deviation (doubling view-timeout backoff, `backoffCap`). Our Lean has
**no restart, rebase or recover notion at all** (`git grep -i 'restart|rebase|recover'` on the file is empty). So (2)
is not answered by any theorem we have.

Twin rule: the "Rust port of a Lean thing is a TWIN" law governs *our* trees, where Lean must be the implementation.
A port inside Simbi's repo is not a twin in ours. Two things are still worth telling them. Their Rust is an unverified
reimplementation that our proofs do not cover. A differential test against our `step` checks the cases they run, and
says nothing about the cases they do not run. If such a port were ever proposed *into* minidregg or breadstuffs, it
would be refused under the law.

On (2), our reasoning, not established by any theorem: committed-prefix rebase is safe for the *chain*. The trap is
**the replica's own messages**. A replica that forgets which views above v it already voted in, or sent CANDIDATE(⊥)
for, can sign a conflicting message after restart. That is equivocation, and it eats the f budget. Restart soundness
needs those views' sent-message records persisted before sending, or the restarted replica must stay silent until it
has entered a view beyond any it could have spoken in. It also has to deal with the "past views remain active" rule
the file states.

**Verdict:** a licence question that only Ember can answer, plus a fair protocol question our model does not yet
cover. Nothing to integrate.

**Integration lane would:** nothing for (1). For (2), optionally: model a crash/restart transition in GenericSimplex,
with persisted `voted`/sent state, and prove no-equivocation across it, or exhibit the counterexample when sent state
is not persisted. That would let Ember answer (2) with a theorem name, not prose.

**Needs Ember:** YES. (1) is a licence/relicensing permission: an Apache-2.0 derivative of AGPL work, "no code copied"
but rules read from our file, plus the AGPL oracle in their tests. NOTICE's mention of Dregg2 lineage may matter too.
That is Ember's decision; we should not answer it.

---

## cv issue #21 (emberian/cv, Ember's tool, no action)

pug asks that `cv rewind`/`port` make transcripts recorded through non-Anthropic models resumable on the Anthropic API.
That means sanitizing `tool_use.id`/`tool_use_id` (`[^A-Za-z0-9_-]` -> `_`, same mapping both ends) and dropping
foreign-signed `thinking`/`redacted_thinking` blocks when the source model is not Claude, by default or behind a flag
like `port --thinking`.

---

## Needs Ember (summary)
- **#2 licence**: whether to permit an Apache-2.0 Rust port of GenericSimplex's rules and an AGPL test-only oracle.
- **#1 design fork**: floors replacing `isIssuerMint` changes what an issuer well means (capped vs unbounded).
- Twin rule: not violated by anything here. Neither proposal puts Rust beside Lean in our trees.
- PR #3: no Ember decision needed. Our integration lane lands H plus pug's key/test, and we reply.
