# RETIRE — continuation (real 2026-10-26, written by RETIRE-1 at its context park)

Read RETIRE.report.md first (the dated log). This file is the state and the recipe; the brief is
the one in the report's header (Ember's two decisions: cv 01a16d3e-5358 retirement, cv 01a16d3e-5382
the join bound to the World).

## The patches (durable copies in /Users/ember/dev/redregg/work/codex/retire/)
- `retire-join.diff`: JOIN (PROTOCOL-79) against nanodregg 5a0a7e4. Self-contained.
- `retire-only.diff`: the RETIRE kernel half, ON TOP of retire-join.diff.
- `retire-full.diff`: join + retire together (= `git diff HEAD` of the second tree).
- `retire-base-for-lang.diff`: an OLDER join+retire snapshot handed to the LANG helper (its enroll still
  compared `origin = c.unsigned.world` inside the receiver; superseded, only the helper's base).
- The LANG helper (an Opus subagent of RETIRE-1) writes its delta to
  `/private/tmp/claude-501/-Users-ember-dev-breadstuffs/01a179c1-8fda-7533-bba2-b7eab03493e4/scratchpad/retire-lang.diff`
  (Lang/ only + law texts + journey rows). If RETIRE-1 is gone when it returns, its report is in the
  parent's task notification; its diff applies on top of retire-full.diff (Lang files only; check it).

Local editing trees (macOS, scratchpad, shared scratchpad dir — other lanes have `nd/` there: never touch it):
- `.../scratchpad/retire-nd`  = 5a0a7e4 + JOIN (working tree; `git diff HEAD` is the join diff).
- `.../scratchpad/retire-nd2` = 5a0a7e4 + JOIN STAGED in the index (`git apply --cached retire-join.diff`)
  + RETIRE unstaged. So `git diff` = retire only, `git diff HEAD` = both. After any JOIN fix: edit BOTH
  trees, regenerate retire-join.diff from retire-nd, then in retire-nd2 `git reset -q && git apply --cached
  ../retire-join.diff`. NEVER `git add` in retire-nd2 (it mixes the halves). Plain `git commit` is refused
  by the repo hooks; landings go through `scripts/commit` on hbox only.
hbox: `/tank/dregg-build/nanodregg/wt/retire` (warm .lake copied from wt/fable-trust at 202f8f4), holds the
JOIN patch applied; build `/tmp/retire-lane/build.sh [targets]` (SWARM_MEM_MAX=6G, 2 threads, log
`/tmp/retire-lane/build.log`, PID `/tmp/retire-lane/build.pid`; wait with
`timeout 590 tail --pid=$(cat /tmp/retire-lane/build.pid) -f /dev/null`). Ship a patch:
`scp diff hbox:/tmp/retire-lane/ && ssh hbox 'cd …/wt/retire && git checkout -q -- . && git apply /tmp/retire-lane/X.diff'`.
KNOWN: every build so far ends with a link error of `codec-vectors` (`undefined symbol
initialize_nanodregg_Emit_Vectors`): `.lake/build/ir/Emit/Vectors.c.o.export` is 736 bytes for a 3 MB
`Vectors.c` (a truncated object, probably from the copied cache or a cgroup kill). It is in this
worktree's own .lake: delete `Vectors.c.o.export*` there and rebuild `codec-vectors`; if it recurs, it is
not ours (check main's build of 5a0a7e4).

## JOIN (PROTOCOL-79) — design as built
- `Body.enroll key next origin join via` (codec tag 0 gains a digest; the wire moves). The joiner signs
  `joinMessage X origin sponsor next key = domJoin ‖ origin ‖ sponsor ‖ next ‖ key` (`domJoin =
  "nanodregg/kernel/join/v1"`, replacing `tagPossession`/`possession/v1`). Refusals: `badJoin` (the old
  `badPossession`) and `otherWorld` (new); the receive refusal table moves (Submit.refusalNames).
- WHERE the World is compared: in `receive` and in `signedBy`, right after the signature
  (`req (c.unsigned.body.joinOrigin.all (· = w.origin)) .otherWorld`), NOT in the enroll receiver: the
  derivation (`receiveWith`, `deriveTurn`) stays blind to the World's name (KERNEL-40,
  `receiveWith_world`/`deriveTurn_world` unchanged). Placed after the signature and before the key so that
  `receive_signed` (receive = signedBy; deriveTurn, law 1) and `receive_checkSignature` stay true;
  `receive` now spells checkSignature; join; keyRule; deriveTurn instead of calling `receiveWith`.
- The member is born at `memberId X origin sponsor next key = H(domMemberId, joinMessage …)`
  (content-addressed): the same consent enrolled again, in the same World or in a carried World whose
  trie holds the first enrolment, is `World.admit`'s `idTaken` (the reader's "again in A" half).
- `init` signs over follow's own World origin (`w.origin` in `Machine.step`): `nd --join`'s one-shot
  follower is on the joined Store, so a carried join signs the carried origin. The join token is
  `key ‖ next ‖ origin ‖ join` (Verb.Join).
- Possession: NOT a separate datum. Possession of a key is shown by any signature of it and needs no
  World; the join's signature is that proof. A second, World-free possession signature by the same key
  would refuse nothing the join does not (a no-op the charter forbids). The category error the reader's
  proposal made (and Ember named): binding the POSSESSION proof to a World turns a fact about a key into
  a contextual datum; the defect was that the old message was a JOIN consent (it named the sponsor)
  mislabelled as possession, and named no World. Write this in PROTOCOL-79's critique.
- Premise price (statements restated; name each in the landing message as RESTATES-MEANING):
  `enroll_authorized` (possession conjunct → join conjunct over origin), `enroll_join_bound` (new),
  `receive_join_world` (new), `receive_named` / `receive_reorigin` / `carry_receive` (+1 hypothesis:
  `c.unsigned.body.joinOrigin.all (· = o) = true`), `carry_receive_world` (+1: `joinOrigin = none`: an
  enrolment's join is World-bound, a carried World's join is a new join). Domains.lean: every
  `*_possession_*` theorem renamed `*_join_*` (RENAMES lines).
- kernel-sim `probeJoinCarried` (after probeCarry): arms `join-carried:possession` (the A-consent still
  verifies under its key in B), `join-carried:otherWorld`, `join-new:ok`, `join-again:idTaken`; registered
  in the required-arms list.
- DONE for JOIN (MEASURED ~21:50Z): whole tree green (790 jobs), kernel-sim --seeds 64 ALL PASS. STILL TO DO: rows
  (Protocol rows run `enroll`/`init` through `join`: confirm ALL PASS); lang-journey (it enrols: confirm);
  `cargo test --test join` and `--test foreign` (client) filtered; codec vectors re-drawn
  (`gates/codec-vectors.tsv`, `lake exe codec-vectors` — find its write flag); generated Rust
  (`client/src/generated.rs`: refusal names/codes? `lake exe emit-rust`), decisions: PROTOCOL-79 in
  decisions/protocol.md (mid-file under its number), the dated correction of decisions/ops.md OPS-1's
  "not carried: … possession proofs" sentence (possession is a fact of a key, never carried or not; what
  is World-bound is a JOIN; a carried World's join is a new join; members already in the export are
  carried as members, KERNEL-40), deploy/RUNBOOK if it names possession. Land `kernel!:` (full judge)
  with RESTATES/RENAMES lines, SIZE and CROSS-LAYER lines as the gates ask (TRUST: Kernel/Receive,
  Protocol/Command; CODEC: Codec/Kernel; CLIENT: generated.rs), "every Store re-geneses (none
  deployed)". Then close cv 01a16d3e-5382 with the hash (`cv task resolve … --from ember`? no: the task is
  Ember's decision, resolved by Ember's 10-26 note; add a note with the hash and close as done).

## RETIRE (KERNEL-70) — design as built (kernel half in retire-only.diff)
- ONE act: `Body.retire cell` replaces `Body.revoke` (codec tag 8 unchanged in bytes). `retireCheck`
  by the pinned cell's kind: grant → its issuer (`notIssuer`); object → its owner (`notOwner`) and every
  law in force judging `Occasion.retire` over its last state (old = new; `X.program.judge look pkg laws`);
  account → its owner, balance 0 and floor 0 (`valueRemains`) — so a retirement moves no value and a
  well (floor = cap) is never retired while it bounds a supply; member / package / authority →
  `notRetirable`. Not callable (an object's method cannot retire yet: cv to open — object-owned
  accounts and object-issued grants need it; it needs a `retire` call kind in Lang's callTy).
- Members are NOT retirable, by design: a member roots authority (owner of cells, issuer of grants) that
  no cell lists; retiring it would leave its grants unrevocable and its objects ownerless (the dangling-
  grant bias the brief names). Its storage is bounded by enrolment counts (KERNEL-16), unlike objects'
  and accounts'. A member's departure needs an index of what it roots: a design, cv task to open.
- Rebirth: tombs are terminal (`checkCreates` idTaken). An id is a digest of its birth's inputs; a keyed
  account's id is (owner, asset), so reopening a retired account is `idTaken`: retirement is final for
  the pair. Merit argument: anyone may open anyone's account (Ledger.account), so a reusable id would
  let any third party re-spend the storage the owner gave back; terminal makes the owner's retirement
  durable. Price: that owner never holds that asset at that id again. Objects' ids are (tx, index): never
  reborn anyway. Members (if ever): their id is the consent's digest, so terminal = the consent spent.
- The kernel already credited a retirement (KERNEL-19: `counterWeight + cell.weight`) and drops a retired
  parent's heads (KERNEL-63 dropHeadsU) and refuses a parent holding rows (`rowsRemain`): those now RUN on
  derived logs. Theorem cases made reachable: `row_stale_behind_forever`'s and
  `range_stale_behind_forever`'s "or the parent is retired (a tombstone)" disjunct (Versions.lean),
  `rowPin_old_floor_recurs`'s situation, `rowStep_dead`/`admit_dead` (orphanRow), checkRowsRemain,
  dropHeads(U)'s retire arm, `admit_retire` (Weight.lean: the credit). Name them in KERNEL-70.
- Theorem `retire_frees_credit`: NOT written yet. Honest form: a derived retire of `x` admitted from `w`
  to `w'` gives `w'.allowance + t.charge = w.allowance + Entry.weight (w.entry x) + (heads' weight)` and
  `w'.entry x = some .tomb` — `admit_retire` (Kernel/Proofs/Weight.lean) states the keep-and-retire turn's
  identity already; the receive-level statement composes it with `retire`'s Draft (one effect). The
  kernel-sim arm `retire-object:ok` measures the same identity.
- The premise price, being paid in retire-only.diff (DONE in source, NOT yet built):
  InvokeTree.lean `dispatch_other`/`dispatched_effects(_step)` (+ hypothesis `∀ x, b ≠ .retire x`),
  `effect_at_object` (+ disjunct `body = .retire e.1 ∧ e.2 = .retire`), `effect_at_grant` (retire case),
  `object_turn_cases` (+ `body ≠ .retire obj` in the keep case, + disjunct `body = .retire obj`), tooth
  `effect_at_object_needs_kind` REPLACED by `effect_at_object_needs_owner`; ObjectHead.lean
  `turn_object_head`/`submit_object_head`/`step_object_head`/`honest_object_head`/`fold_package_fixed`
  (+ disjunct `w'.entry X.env obj = some .tomb`); Versions.lean `admit_retire_tomb` made public +
  `fold_tomb_stays` (new). The other kernel proofs' revoke cases renamed (Rooted, Ledger, LedgerNext,
  AuthorityOf).
- STILL TO DO for RETIRE (in order): build retire-full.diff; fix the cascade's consumers:
  Kernel/Proofs/Logic/History.lean (`ObjectStep`: the `keep` constructor needs `body ≠ .retire obj`; a new
  `retire` constructor (a JUDGED step: laws, `reqOf … .retire`, state, state, []) and an `ObjectHistory`
  ending at a tombstone; `object_history_of_honest`, `object_history_chain` (a retire step lifts like a
  relaw: old = new), `object_step_none`); Protocol/Proofs/FollowHead.lean `absorbStep_packageAt` (uses
  submit_object_head: + the tomb case, so the package claim is "or retired") → Hosting/Proofs/SocketStrong
  `reach_packageAt` (AGENT's column: report line first); Spec/Proofs/Deployed.lean `top_integrity_law`
  (ROOT's Spec: `Integrity.law` says the object's package is fixed — with retirement it is "fixed while it
  lives"; the Spec statement in Spec/System.lean must say so: write it in the report as a change of
  ROOT's top-level claim, not a weakening of a check: the object can now actually end); Host/Proofs/Refine
  (docs only). Then merge the LANG helper's diff; kernel-sim (`probeRetire`, 8 arms: retire-member:
  notRetirable, retire-object:notOwner, retire-object:ok (+ the allowance identity), retire-read:stale,
  retire-frozen:lawDenied, retire-well:valueRemains, retire-account:ok, account-reborn:idTaken); the sim's
  `frozenAct` refuses `.retire`; lang-journey rows from the helper (rowsRemain → clear → retire admitted,
  heads dropped, stale / orphanRow / noRelation by name); verb `retire CELL` (Verb/Machine/Stdio/Rows;
  client tests pin.rs, doc.rs use it; re-emit client/src/generated.rs); KERNEL-70 decision (critique +
  meta-critique: the bias is a retire that leaves dangling grants: answered for grants TARGETING a retired
  object (they fail closed: missingCell; their issuers can still retire them and get their storage back),
  for members (not built, why), for programmed objects that issued grants or own accounts (the package's
  law decides, as it decides every act of its object; the Std laws' retire arms are conservative)); land
  `kernel!:` (full judge). Close cv 01a16d3e-5358 with the hash.

## Ownership lines written (FABLE-OWNERSHIP.md): KERNEL-70, PROTOCOL-79 claimed. Hunks in other columns
are listed in RETIRE.report.md's header; add any new one (Spec/ = ROOT, Hosting/Proofs = AGENT) there
before touching. RELAND-CTX's K1 (`Req.caller`: `reqOf` gains a caller arg; Kernel/Receive gains fields)
was in the full judge at 21:00Z: rebase onto it; `retireCheck`'s `reqOf c.unsigned x a.actor .retire`
needs its caller (`none` at the signed top, like derive's).
