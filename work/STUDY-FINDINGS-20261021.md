# WHAT NANO HAS SHOWN — findings of the nanodregg study (SCHOLAR-STUDY, 2026-10-21)

For mini, for breadstuffs, for the next robigalia. Read-only; nothing built, nothing run beyond `grep`,
`sed`, `git log`, `git show`. One document written (this one).

**Frame (Ember, 10-21).** nanodregg is an OBJECT OF STUDY beside breadstuffs (where the whole system we
built lives, waiting to be resumed or composted into the next robigalia) and minidregg (the previous side
exploration, finish-only). Nano demonstrates where mini could be better where that is cheap in the
smaller system. This is the findings paper, not a demo list: each finding is a claim, its evidence, what
the two bigger systems do instead today, what adopting it would cost in PREMISES and in what REFUSES
(a re-genesis is not a cost), and a verdict.

**Sources and the commit each was read at.**

| tag | tree | read at |
|---|---|---|
| N: | hbox `/tank/dregg-build/nanodregg/main` (ssh, read-only) | `cdd9d84` (577 commits; git author dates 2026-10-16 18:30 → 2026-10-19 17:19 −0400) |
| M: | `~/dev/minidregg` main, after today's fast-forward | `334316df` |
| B: | `~/dev/breadstuffs` main, working tree | `22fad151e` |
| W: | `~/dev/redregg/work/` (decision cards, lane logs, STALL-WATCH) | as of 10-21 ~21:45Z |

**Tags on every claim.** MEASURED = I ran the command or read the file:line myself this session. READ = a
number or claim as a decision, commit message or lane log states it (its own measurement, not re-run here).
ASSUMED = my inference, unverified.

**A note on dates.** hbox git author dates on nano's main run 10-16..10-19; the decisions, the lane logs
and STALL-WATCH label the same commits 10-17..10-21 (e.g. `e86f237` is `2026-10-19` in git and "10-21
evening" in the logs). I cite each as its source has it. ASSUMED: one history, two clocks; the logs' clock
runs ahead (ROOT corrected a fast log clock once already, memory 10-17).

**Scope guard.** Three candidate items the brief named are NOT on main at `cdd9d84` and are reported as
in flight from lane logs: HOST-64 (the checkpoint mechanism, HOST-20's worktree, compiles whole, seeds
pass), the HOSTING-15 fence refutations (R1/R3/R4, landing was waiting on GATES-10's runner rule), and
GATES-20h (the fluid landing rule, measured 0 % skip, held). Everything else cited is a landed commit.

---

## 0. The verdict table

| # | finding | verdict | for |
|---|---|---|---|
| F1 | Stale pins final by structure (versioned pins) and by theorem | **TAKE** | mini |
| F2 | Refusals recorded, final within a window, bounded per member and world-wide | TAKE-WITH-CHANGE | mini |
| F3 | The World size bound is derived from the charge rule and the codec, not a literal | **TAKE** | mini, bread |
| F4 | A turn's inserts are one batch on a dirty overlay, sealed once | TAKE-WITH-CHANGE | mini |
| F5 | The draw-independent per-required instrument, pinned, only falls | **TAKE** | mini, bread |
| F6 | A key encoding is injective by itself, never by a World invariant standing in for it | TAKE-WITH-CHANGE | mini |
| F7 | The judge: traced read-sets, a landing queue, the silent-revert guard, the judge's code is main's | **TAKE** | mini, bread |
| F8 | `CollidesAmong` over an explicit list replaces `∨ Collision` | **TAKE** | mini (8 sites), bread (audit 14) |
| F9 | A package's law proved against the kernel's own admission (escrow pays once) | TAKE-WITH-CHANGE | mini |
| F10 | The resident's tick is an effect tree; durability over a crash RELATION | TAKE-WITH-CHANGE | mini, bread |
| F11 | A crash-loop window passes by the launcher's tick, as a theorem | TAKE-WITH-CHANGE | mini |
| F12 | A tick walks at most one word (the byte primitives are charged per 32 bytes) | TAKE-WITH-CHANGE | mini, bread |
| F13 | The package wire carries a version byte; the old shape refuses to load | **TAKE** | mini |
| F14 | A member's connection is one fd with every close named; the bound bounds | **TAKE** | mini |
| F15 | The two-uid fence refuted three times on its first real run (ACL, setgid-on-chmod, UMask) | **TAKE** | mini |
| F16 | Checkpointing with a trust premise bound to the Store's recorded origin (IN FLIGHT) | TAKE-WITH-CHANGE | bread, mini |
| F17 | Relations as rows in the one trie, commuting inserts, path compression, one printer | TAKE-WITH-CHANGE | mini |
| F18 | "A refusal renders as the expected verdict" is a class; hints beside names | **TAKE** | mini, bread |
| F19 | Adoption judges the state (`adopt` occasion, `law_judged`) | NANO-ONLY | — |

**TAKE: 9. TAKE-WITH-CHANGE: 9. NANO-ONLY: 1.** Then §20, what nano has shown about the METHOD (eight
rules, each with its incident).

---

## F1 · A stale pin is final by structure, and the finality is a theorem

**(i) Claim.** If a pin names a monotone per-cell VERSION instead of a content digest, a pin the fold has
passed can never match again, so a stale refusal needs no record, no budget and no hashes to be final, and
"a call refused stale BEHIND is never admitted later" is a theorem of the kernel plus the protocol.

**(ii) Evidence.**
- Design and measurement before ruling: N:`decisions/kernel.md:2539-2593` (KERNEL-54 PROPOSED + STEP 1
  MEASURED): the defect (READ: concurrent writers refused `stale` on 0.75–4.25 % of writes, N=400, 3
  actors; at N=1000 an honest member reached `declined refusalBudget`), three options, and the premise
  spread over 356 statements: a per-cell counter N adds **0** premises; last-write height H′ adds 3; pure H
  ≥5 and breaks `admit_comm` and the sim gate `rows-two-rains:both`. ROOT's prior (the height) lost on the
  measurement: `kernel.md:2594-2600` (RULED).
- As built (MEASURED file:line): `Kernel/Proofs/Versions.lean:240 stale_behind_forever`, `:1124
  pinOf_old_recurs` (the tooth: the content pin recurs never-born → born → retired; the entry pin does
  not), `:1373 stale_behind_forever_sep`; `Kernel/Proofs/StaleOnly.lean:268 admit_stale_pin` (`.stale`
  is built at exactly three places); `Protocol/Proofs/Behind.lean:219 staleBehind_final`, `:336
  staleBehind_final_sep`. Commits `b48c10f` (kernel!, KERNEL-54) and `6f28e4a` (PROTOCOL-57), MEASURED in
  `git log`.
- What it saved (READ, `kernel.md:2592`): each stale no longer recorded saves 527.2 B, 11.41 hashes, one
  step and one budget unit. The `refuse record-bytes-per-refusal` row is 529.217 after KERNEL-54
  (MEASURED `gates/waste.tsv`).
- The proofs found two FALSE phase-1 statements (`row_stale_behind_forever` under an unlawful `Ord`;
  `rowsPrefix` at rel ≥ 256) and the vacuous `∨ Collision` (F8): `kernel.md:2627-2633` (READ).
- The split BEHIND (final) / AHEAD (open): `decisions/protocol.md:1665-1685` (PROTOCOL-52): settled from
  the member's OWN fold, never recorded; AHEAD stays `open`.

**(iii) What mini does.** Content-digest pins: M:`Kernel/World.lean:531-539` (`pinCheck`, "the one
staleness refusal": refuses when `H.cellDigest (w.cells p.1) ≠ p.2`), theorem `admit_pin_refused`
`:2114-2121` (MEASURED). A refused intent is unrecorded: M:`Kernel/DurableCommitProtocol.lean:474-476`
("an unrecorded intent whose guard fails leaves the durable snapshot untouched"); a later `lookup` is
`.absent` (M:`Host/Main.lean:1300,1367`). So mini has the A→B→A class nano's KERNEL-44 names: a write
A→B→A restores the digest and the same signed call admits after its attempt store ended it refused
(ASSUMED: I read the pin check and the absence of a record; I did not construct the sequence in mini).
No finality theorem for a refused pin exists in mini (MEASURED: no `stale_*final|behind` in M:Kernel).
**What breadstuffs does.** A per-AGENT nonce: B:`turn/src/turn.rs:470` (`nonce: u64`, hashed into the
signing message `:619`); refusal code 5 "the turn's nonce does not match the agent's next nonce (replay or
stale turn)" B:`turn/src/admission_reason.rs:36,111` (MEASURED). That is version discipline on the SIGNER
(serial per agent), which makes replay final by structure but says nothing about a read of another cell;
whether breadstuffs turns pin other cells' state at all I did not find (ASSUMED: no cross-cell read pins).

**(iv) Cost.** Premises: nano measured 0 on landed cell readers (one statement's hypothesis STRENGTHENED,
`live_inclusion_sound`; `kernel.md:2625`). Mini must measure its own spread the same way (the 27-statement
list method, `kernel.md:2560`); ASSUMED similar, since mini's pins are also a list on the Turn. Shape: an
`Entry.live` version (varint), row leaves a version, heads a floor; the pin reads the ENTRY so absent, tomb
and live are three pins. Refuses: a passed pin is `declined stale` (unrecorded, not final from the Host; final
from the member's fold); a version past the counter limit refuses by name. Flag day: the pin wire, every
vector embedding a pin, every Store (free).

**(v) Verdict: TAKE (mini).** The cheapest finality nano has: a field, not a record. For breadstuffs, only
if it adds cross-cell read pins; its agent nonce already has the structure for its own class.

---

## F2 · Refusals are recorded, final within the window, bounded per member and world-wide

**(i) Claim.** An authenticated in-window refusal is a step of the log in a third trie instance; `submit`
of a recorded txId answers the recorded name without re-deriving (`refusedFinal`); the record is bounded
per member per window (16) and world-wide per window (16,384), and the bound is a theorem of the fold.

**(ii) Evidence.** KERNEL-44 proposed N:`decisions/kernel.md:1769-1798`; KERNEL-47 as built `:1986-2029`
(ONE fold over `Step = turn | refusal`, a step counter, seven amendments: in-window only, a tag byte in
one chain domain, `refusedFinal` as a check of `World.admit`); commit `38d94e1` (MEASURED). Bounds
(MEASURED): `Kernel/Bounds.lean:63 refusalsPerWindow := 16`, `:73 refusalsPerWindowMax := 16384`;
`Kernel/World.lean:93 refusedFinal`. The world-wide cap R1 and its theorem: `kernel.md:2824-2864`
(KERNEL-55 part 2), `Kernel/Proofs/RefusalsBound.lean:157 refusals_bounded`, `:296
refusals_bounded_of_counted`; three windows coexist and three is tight (`refusal_window_three`, READ).
Price as premises (READ, `kernel.md:2020-2027`): `World.fold` renamed on 149 lines in 35 files, NONE
gaining a premise; one premise REPLACED (`follower.height = host.height` → `steps`); one landed helper
(`refuse_sumN`) forced a premise at R1 (`kernel.md:2856`). The R1 price ROOT accepted, named: ~1,024
members at their own budget stall everyone's refusal finality for a window; admission unaffected
(`kernel.md:2863`).

**(iii) Mini.** No record (F1 (iii): `DurableCommitProtocol.lean:474`, `Host/Main.lean:1300` `.absent`).
Mini's journal is one entry per ADMITTED turn (ASSUMED from `.absent` on an unjournaled txId). The client
cannot tell a final refusal from a lost reply. **Breadstuffs.** `TurnError` is returned (B:`turn/src/error.rs:52`),
not recorded; no `RefusalRecord` type in `turn/src` or `chain/src` (MEASURED grep, 0 hits). The nonce makes a
RE-submission of the same turn fail by structure, but a refused turn did not spend the nonce, so "was it
refused or lost" has no answer there either (ASSUMED).

**(iv) Cost.** Premises: in nano 0 added, 1 replaced, 1 forced. For mini: every `fold`-over-turns theorem is
restated over steps (statement churn, not premises, if mini's fold is generic in the transition as nano's
`Rooted` was). What refuses: `refusedFinal`, `refusalBudget` (declined, not final: the one honest cliff
KERNEL-54 removed for `stale`), `refusalsFull` (R1), a base whose window has records but no total
(`kernel/refusals-counted`). Flag day: refusals key wire, chain tag byte, every World with a record.

**(v) Verdict: TAKE-WITH-CHANGE (mini).** Take the record and `refusedFinal` only AFTER F1, so the record
holds no `stale` (nano built them in the other order and then took stale out). Take R1 only with its
liveness price written where mini's operators read, or with a per-member shape that rests on a membership
bound mini can prove (nano could not: `kernel.md:2819` Q2).

---

## F3 · The World size bound is derived, exactly, and the writer never reaches it

**(i) Claim.** `worldBytesMax` is a definition built from named constants through a potential theorem
(145·weight + 84·allowance) and an exact codec size equality, equal to 91,914,346 bytes by `decide`; every
World an admitted fold reaches encodes within it with no premise on the reached World.

**(ii) Evidence (MEASURED file:line).** `Host/Proofs/Size.lean:116 worldBytesDerived_eq : worldBytesDerived =
91914346 := by decide`; `:155 reached_size_le`; `Codec/Proofs/WorldSize.lean:123 world_size_eq` (exact:
`size + 8·(live+rows) = weight + worldFixed + journalBytes + refusalsBytes + 3·(live+tomb) + 2·spent +
versionBytes`, only a 32-byte-digest premise). Decisions: N:`decisions/host.md:2624-2653` (HOST-57),
`codec.md:1565-1598` (CODEC-39, slack 54/49 with the tooth `world_size_slack_tight`), `kernel.md:2645-2660`
(KERNEL-55: the old `2^28` literal was never reached by any fold; two docstrings stated ratios the code did not
have), `:2818-2822` (the potential, Φ = 145·weight + 84·allowance, tight at a pinless declare 84/61). The
derived bound is 34 % of the literal it replaced (READ). Premises: none on landed theorems except
`refuse_sumN` (F2).

**(iii) Mini.** M:`Kernel/Bounds.lean:96-97`: `/-- A Store's state bytes this epoch (creates refused past it, HP-3).
ASSUMED 64 MiB. -/ def stateBytesMax : Nat := 67108864` — a literal whose own docstring says ASSUMED
(MEASURED). Mirrored into Rust by name (M:`native/resource-client/src/bounds.rs:28`). **Breadstuffs.** No
analogue found in `turn/` or `chain/` (MEASURED grep for `worldBytesMax|stateBytesMax`: 0 hits; ASSUMED none).

**(iv) Cost.** Premises: the potential theorem is over the CHARGE rule (`growth_le_logWeight`); mini has a
charge rule ("storage lane = patch bytes", M:`Kernel/World.lean:539-541`), so the theorem has a home. The
codec equality needs every byte to have a term, which is the CODEC-39 discipline (a def-module of measures,
`entrySlack` and a tight witness). What refuses: `baseTooLarge`, `allowancePastBound` /
`potentialPastBound` at genesis, join and import (HOST-56); `worldTooLarge` stays as the encode twin that no
honest fold reaches. No wire moves; the base frame max moves (HOST-57 flag day).

**(v) Verdict: TAKE (mini, and the method for breadstuffs).** The finding is less the number than the
rule: a bound that a theorem does not reach is a literal, and a literal grows prose ratios around it.

---

## F4 · A turn's inserts are one batch on a dirty overlay, sealed once

**(i) Claim.** Rebuilding a trie path per key hashes shared nodes once per key; writing the turn's keys onto
an unhashed overlay and sealing once hashes each written node once, and the batch IS the sequential trie
by a premise-free theorem.

**(ii) Evidence.** Commit `258c273` (MEASURED `git show`): seeds 0-63 admission trie hashes 61851 → 60448,
refuse 37119 → 29613; `admit trie-hashes-per-turn` 14.074 → 13.754; `Kernel/Proofs/Trie.lean:737
insertAll_eq_foldl` (MEASURED), "no premise, not even WF"; `T` stays the only authenticated shape
("nothing reads, proves, lists or encodes a `U`"). Commit `5e33878` (rows and heads on the overlay): rows
probe 6912 → 4416, stem probe 28672 → 24576, worstcut 32.938 → 32.217; `rowsRun_eq` with no premise;
ONE `rowStepOn` body over a store, the trie its instance by rfl. Every `hashes-per-required` row stays
1.000 exact (MEASURED `gates/waste.tsv`: `admit hashes-per-required`, `refuse hashes-per-required`,
`row-insert-*`, `row-retract-*`, `bar trie-hashes-per-required` all 1.000).

**(iii) Mini.** M:`Theory/AuthTrie.lean` is a per-key authenticated trie (`NodeIn`, `climb`, `Reports`);
M:`docs/DURABLE-STORE.md:73-74`: "The served world root is a cached tree, so one write rehashes one path
per written slot" — per SLOT, so a turn writing k slots under a shared prefix rehashes the shared nodes k
times (ASSUMED from the sentence; not measured in mini). **Breadstuffs.** Not measured here (ASSUMED: no
hashes-per-required instrument exists in B:, see F5).

**(iv) Cost.** Premises: 0 in nano (`seal_insU` holds without WF). Code: a second, unauthenticated trie
shape beside `T` — nano accepts it because nothing authenticated reads it. What refuses: nothing new; no wire
moves (the sealed digests are identical).

**(v) Verdict: TAKE-WITH-CHANGE (mini).** Change: the instrument first (F5). Without `hashes-per-required`
pinned, the gain is invisible and the second shape is a twin risk; with it, the overlay is a 2.3 % win on
admission and a 20–36 % win on rows that the ratchet keeps.

---

## F5 · The per-required instrument: counted on the real compiled code, draw-independent, only falls

**(i) Claim.** Count the trie-domain hash calls of the REAL compiled `World.admit` and divide by what the
design requires (`Required.batchReq`: one hash per node on some batch key's path, each once); pin the ratio;
ceilings only fall. A ratio of 1.000 is exact and does not depend on the random draw.

**(ii) Evidence.** `gates/waste.tsv` header "ceilings only fall; see gates/waste.py" and the rows
(MEASURED); commit `16f3b9f` (MEASURED): `World.roots` re-hashed the empty digest per root on every read;
one `rootsOf` thunk shared; `bar trie-hashes-per-required` 1.096 → 1.000 "measured 1.000 exact in three
runs" (379/379, 395/395, 395/395; was 393/366 .. 433/406); `Kernel/Proofs/Admit.lean:101 World.roots_eq`
(MEASURED) makes it a no-flag-day change (the old per-root digest equals the shared read for every E and w).
The tooth: the plant `hash-count:empty-per-root` reads 1.161 against the old read. The whole table: 18 rows,
every `*-per-required` at 1.000, the ABSOLUTE companions (`trie-hashes-per-turn` 13.754, `proof
bytes-per-inclusion` 257.797) pinned beside them (MEASURED).

**(iii) Mini.** No waste ratchet found: M:`scripts/pipeline/instruments.tsv` exists (MEASURED `ls`); what it
pins I did not read (ASSUMED: a list of instruments, not a falling ceiling). Mini's CHARTER-era rule "no
wall-clock benching, deterministic counts only" was Ember's for nano (memory 10-17). **Breadstuffs.** B:`perf/`
exists (MEASURED `ls`); ASSUMED wall-clock, no per-required ratio.

**(iv) Cost.** Premises: none; it is a counting environment (`Sim.countingEnv`) and a definition of
required. Code: a `Required` module per operation shape. What refuses: a landing whose ratio rises
(`gates/waste.py`). The trap it closes: a plant that counts a stat the design never defined (F20 §5).

**(v) Verdict: TAKE (mini and breadstuffs).** Of everything in this paper, this is the cheapest and the
one every other performance claim rests on.

---

## F6 · A key encoding is injective by itself, never by a World invariant standing in for it

**(i) Claim.** A rows key that wrote the relation, the key length, the width and the prefix length as one
wrapping byte (`byte8`) made relation 0 and relation 256 one key and the empty key's bytes followed by 256
zeros equal to the 256-byte key's; LEB128 (`natBytes`) at all four sites is injective and prefix-free over
all of Nat, so the rows trie becomes the fourth `HeadSound` instance and a phone reads rows against a head.

**(ii) Evidence.** Commit `7c09186` (kernel!, MEASURED `git show`): "`rowFits` bounded `rel < 256` and `|k| <=
128` inside the World, a World invariant standing in for a property the encoding must have by itself";
`Kernel/Turn.lean:144,154 natBytesFuel/natBytes`, `Kernel/Proofs/RowsSep.lean:97 rowKeyBytes_injective`
(MEASURED); teeth `rowKeyBytes_rel_wrap_ne`, `rowKeyBytes_len_wrap_ne`, `rows_rel_wrap_read` (decide
+kernel on a toy Env: the relation-0 head's proof does not verify at relation 256). Premises REMOVED from
nine statements (`width < 256`, `rel < 256`); ONE premise ADDED, on a tooth (`declare_growth_tight` needs
`rel < 128`). 23 tags moved; 242 vectors re-emitted over 55 sites; `rowDepth` 1304 → 1320. The meta-critique
in the commit: "(b) is also the option that touches the fewest other layers, which is a reason to distrust
the choice; it survives because it is the only single mechanism."

**(iii) Mini.** Mini has no relation rows in its kernel (W:`NANO-VS-MINI-20261017.md` §2; LANG-44 `lang.md:1203`
reads delvetalk's relations as the prior art, not mini's). Mini's trie keys are `NodeIn.leaf (k : K) (v : V)`
with K a type parameter (M:`Theory/AuthTrie.lean:30-34`); where K is instantiated by an ENCODING of several
fields I did not check for wrap sites (ASSUMED unknown). **Breadstuffs.** Not checked (ASSUMED).

**(iv) Cost.** Premises: net negative in nano (nine removed, one added on a tooth). What refuses: a relation
or width at or past 256 by NAME on the wire (`kernel/row-key`, `kernel/range-pin`), where a one-byte field
wrapped it to 0. Flag day: rows keys with a field ≥ 128 change bytes; every Store.

**(v) Verdict: TAKE-WITH-CHANGE.** The code is nano-only (mini has no rows trie). The RULE transfers to any
composite key either system hashes: an admission bound (`rowFits`-style) is not an injectivity proof, and the
census question is "which `byte8`-shaped fields are hash preimages".

---

## F7 · The judge: traced read-sets, a landing queue, the silent-revert guard, and the judge's code is main's

**(i) Claim.** A landing is judged by main's own gate code on a candidate merged from what the lander
RECORDED (never the working tree), selected and re-used by a traced read-set keyed on content, queued by
readiness with an age bound, and refused `stale path` when it would silently revert a recent commit. Built
this way it found four fail-opens in its own predecessor within a week.

**(ii) Evidence (all READ from N:`decisions/gates.md`, commits MEASURED in `git log`).**
- The measured problem (GATES-19, `gates.md:432-465`, commit `1a6163b`): over 36 h, 216 landings took 306 full
  judges; 90 GREEN judges were lost to the compare-and-swap; HOST-52 took six runs. Static reuse as built:
  10.4 % (the design's 42.9 % was a replay of an unsound key). First day under the queue: 6 of 13 landers
  reached the age bound.
- Fail-open 1 — **selection by import closure only** (GATES-19 item 0, `gates.md:437`): a re-emitted
  `world/resident/Bell` selected no row; a `lang!` that broke it landed GREEN; standing went RED after.
- Fail-open 2 — **a run selected by its own exe only** (GATES-20a, `gates.md:467-486`, `6527d9f`): `store-plants`
  runs `{host}`, `rows` runs `lake exe lang-journey`; "ten landings carried a pre-push GREEN without the run".
- Fail-open 3 — **the silent revert** (GATES-20b, `gates.md:487-512`, `8c2c5fd`): a re-based attempt re-read a
  file from the working tree while CLIENT-31 had added 70 lines to it on main; the candidate was `git add -A`.
  Verified with a stub pre-push that could land nothing. Now: snapshot at the first attempt (BASE, OURS to the
  object store), a 3-way `merge-file` per path, `stale path: P` refused unless `--reverts C` names the commit
  and its owner. Replayed over 150 landings: 14 (9.3 %) would have been flagged, every one a deliberate
  deletion. Its own meta-critique: "GATES-19 trusted HEAD as 'the copy the lander edited' and its plants never
  moved HEAD. The defect lived in what the plants held fixed."
- Fail-open 4 — **a judge table invisible to a trace** (GATES-20e, `gates.md:608-630`, `c8ebb06`): PERF-4's
  `41e041f` re-pinned worstcut ceilings in `gates/waste.tsv`; attempts 2–6 printed `NOT RUN (standing-only; its
  inputs are unchanged)` because the bench never READS the table the judge compares it against. Now every
  read-set carries W, the waste rows the row measured.
- The self-judging runner (GATES-20, `gates.md:527,557`): "GATES-19 and GATES-20a both changed gates/runs.py
  and were judged by their own runner"; plant `g20-evil-runner` (a candidate runs.py printing `runs: ok`) now
  reads RED. Traced reuse 41.8 % (803 of 1922) vs 10.4 % static; 804 re-runs sit on the binary-closure floor.
- GATES-20d (`gates.md:580-606`, `be8ee18`): the first real standing under tracing read RED on 13 of 14 cargo
  rows because a warm cargo reads fewer paths than a cold one; a compile's reads become C, compared only
  against a compile; an escaped name (`O\222\17\333\5`, strace reading a string while a thread rewrote it)
  invalidates the whole trace. Meta-critique: "The plant held the cache order fixed, the way GATES-19's plants
  held HEAD fixed: the same blind spot, a week apart."
- The gate that reads red first (GATES-15, `gates.md:355-379`): under the old judge a `runs.py` that raised at
  entry read `runs: ok ()` / `PRE-PUSH GREEN`; now every cargo row runs a `nobin RED` control FIRST and every
  Lean exe a `--harness-control`.

**(iii) Mini.** M:`scripts/pipeline/known-red-verdict:1-10`: ONE known-red rule (the failure set must EQUAL
the listed set; an unlisted red refuses, a listed module that now builds refuses) with a `--selftest` that
plants both; `landing.sh:14` is load-gated (`PIPELINE_GATE_MAX_LOAD` 20); `lane-staleness-selftest` exists
(MEASURED `ls`). No judged 3-way merge, no read-set, no snapshot-at-first-attempt (MEASURED grep: `merge|rebase|
3-way|behind` in `landing.sh` → only the load line; `strace|read-set` in `scripts/` → 0). **Breadstuffs.**
B:`scripts/local-gates.sh:1-12`: "The bar is not 'GitHub is green'": of the last 60 ci.yml runs 37 cancelled,
21 failed, 0 succeeded, median commit gap 92 s vs ~87 min to a verdict (READ); `check-gates-executed.py`,
`gates-executed.tsv` (MEASURED `ls`); main is not branch-protected (memory `minted-fail-open-gate-class`).

**(iv) Cost.** No premises; this is tooling. Operational price nano states: 9.3 % of landings pay one flag
(`--reverts`); the first judge after each key version re-runs every row once; strace keeps bench rows near the
600 s deadline on a loaded box (STALL-WATCH 17:36Z 10-21: "a gate effectively off on busy days"). What
refuses: a candidate behind main with a conflict (by name, with hunks); a stale path; a forged reuse record
(`stale verdict`); a run with no verdict line (`NO VERDICT`); a runner whose known-red control passes.

**(v) Verdict: TAKE (mini and breadstuffs).** In this order: GATES-15 (prove the reader can read red) →
20b (snapshot + `stale path`) → 19 (queue) → 20/20a/20d/20e (traced selection). The one sentence to carry:
the candidate never runs its own judge.

---

## F8 · `CollidesAmong hash S` over an explicit list replaces `∨ Collision`

**(i) Claim.** `Collision hash := ∃ dom a b, a ≠ b ∧ hash dom a = hash dom b` is provable from a lawful
digest by pigeonhole (a fixed-size digest is a finite type; byte strings are not), so every theorem concluding
`… ∨ Collision` was true whatever the fold did. The sound escape names the finite list S of (domain, bytes)
inputs the theorem's OWN objects hashed; a hash that separates S refutes the disjunct.

**(ii) Evidence.** N:`decisions/kernel.md:2637-2643` (KERNEL-56): 61 statements, found "because a proof lane
tried to close a sorry honestly and noticed it could close it in one line"; "Green builds, census, and two
earlier vacuity reads all passed these 61 statements". Commit `482aecc` (MEASURED): `Collision`, `Trie.Coll`,
`HashColl` deleted; "No definition a node runs changes value, no wire, no hash input, no vector: nothing
re-geneses, nothing re-emits". `Kernel/Proofs/Fold.lean:30 def CollidesAmong` (MEASURED); 144 lines across
the Lean layers name it (MEASURED grep). Premises added: none; three refutation theorems whose conclusion WAS
the escape got teeth stating the binding fact directly. Memory: `minted-a-disjunct-provable-from-the-premises-is-vacuous`.

**(iii) Mini.** The SAME shape, live: M:`Theory/AuthTrie.lean:81 def Collision : Prop := ∃ a b : NodeIn K V D, a ≠
b ∧ dig a = dig b` with `NodeIn` holding `leaf (k : K) (v : V)` (`:30-34`), so for any infinite K and finite D
it is provable by pigeonhole (MEASURED the definition; the finiteness of each instance's D is ASSUMED — the
deployed digest is 32 bytes). Eight consumer sites conclude `… ∨ Collision` (MEASURED grep):
`Theory/AuthTrie.lean:135,166,265`, `Theory/AuthTrieRange.lean:114,182`, `Pred/HashEqDigest.lean:275`,
`Pred/HashEq.lean:197,209`, `Theory/ObjectiveBendDigest.lean:195,205`. Whether each is vacuous depends on its
`K`/`D` instantiation; the audit is one lane-hour. **Breadstuffs.** 14 lines in 4 files conclude `∨
Collision|Coll|HashColl` (MEASURED): `metatheory/Dregg2/Verify/FreeConclusionRatchet.lean`,
`Dregg2/Circuit/FirstDivergence.lean`, `Dregg2/Shielded/RealCrypto.lean`, plus import comments in
`Dregg2.lean`. One of them is ALREADY the sound form: `Circuit/FirstDivergence.lean:75 def Coll (h) (p : π × π)`
is over an explicit pair. The others are the audit.

**(iv) Cost.** Premises: none. Statement size: every escape carries its S list, threaded through the trie
helpers. What refuses: a theorem whose proof cannot name its colliding pair does not compile (the cheapest
audit the kernel has had). Nothing re-emits.

**(v) Verdict: TAKE (mini: 8 sites; breadstuffs: 14 lines).** And the reader rule with it (§20.1).

---

## F9 · A package's law proved against the kernel's own admission

**(i) Claim.** "The escrow pays out at most once" is a theorem over a HISTORY of admitted kernel turns
around one object, interleaved with any other turns, at the node's deployed context with only the history as
premise — not over a spec model of the escrow — and a KERNEL-CHECKED witness run meets the premises.

**(ii) Evidence (MEASURED file:line; commits in `git log`).** `Ledger/Proofs/EscrowRun.lean:385
escrow_runs_one_payout` (LEDGER-14, `ebe9d81`); `Ledger/Proofs/EscrowInvokes.lean:90
escrow_invokes_one_payout` (LEDGER-15, `e86f237`); `Ledger/Proofs/EscrowWitness.lean:187
escrow_runs_witness` ("evaluated by `decide +kernel`; no `native_decide`, no allow or tcb row"; ~10 s, 2.7 GB,
READ `ledger.md:735`); the kernel's link `Kernel/Proofs/InvokeNext.lean:444 invoke_next_slots` (`5807a47`,
kernel!: "the next run of an object is handed what this run returned") and its joint-satisfiability witness
`Kernel/Proofs/InvokeWitness.lean:332 invoke_next_slots_witnessed` (`628a8b9`). Decisions
N:`decisions/ledger.md:629-818`. What the second-agent reads found and the owner fixed: `Runs` chained the
written LIST (a real `invoke` may order slots differently) → key-wise equality; the first `Invokes` allowed only
consecutive invokes → the `other` step; "nothing showed `receive` + `World.admit` ever accept an invoke of a
programmed object" → the witness. Deleted: the spec chain (`escrow_one_payout`, `spends`, `callAt`,
`spendCount`), because it counted `methodResult` over states the SPEC chose. Named gaps (READ): a nested invoke
is not a step (`ececba1` later closed the kernel half); an admitted ESCROW release witness waits on KERNEL-28.
The OOM lesson (`ledger.md:731-739`): a `decide +kernel` probe that "gets stuck" was earlyoom (exit 143); the
kernel does not unfold mutual WF recursion; route through the equation lemma.

**(iii) Mini.** M:`Kernel/CanonicalEscrowMarket.lean:1-8` and its theorems `:115-328` (`State.opened_valid`,
`afterFill_valid`, `conserves`, `retry_replays`, `installed_rekey_nullifier_not_fresh`) are over a `State`/`Deposit`
model with "one accepted transfer into an escrow account" (MEASURED the header and theorem names; ASSUMED:
none takes a receiver run as premise — no `runMeasured`/`admit` in their statements that I saw).
**Breadstuffs.** B:`metatheory/Dregg2/Proof/WP.lean` (partial correctness over a state transition, W:`COMPARE-20261021.md`
§4) and B:`metatheory/Market/Clearing.lean:108,321` ("escrow-in-aggregate", `EscrowWitness.fund`): the law is of
the model, the kernel link is what breadstuffs' `vcg_run_sound` took as a START-state premise (COMPARE §1.2).

**(iv) Cost.** Premises: none added to landed theorems in nano; the new theorems' premises are the history
(each step a `receive`/`World.admit` fact). What it needs from the kernel: the next-run link (`invoke_next_slots`)
and `admit_frame`; mini has activities that outlive a turn (ADOPT's drain, M:`Kernel/ObjectiveActivityUpgrade.lean:1-14`),
so its link is per activity step, not per turn (ASSUMED). Kernel evaluation budget: ~3 GB per witness.

**(v) Verdict: TAKE-WITH-CHANGE (mini).** The change is the subject: prove one mini package's law over mini's
receiver with its own run link, and delete the spec twin that replaces the run with chosen states.

---

## F10 · The resident's tick is a tree of effects; durability is over a crash RELATION

**(i) Claim.** Write the resident's tick as a `Prog` tree whose every node is one effect and whose continuation
takes that effect's result; prove the order over EVERY path and every result (`tick_order`), prove the
interpreter performs exactly a path at a recording handler, and prove keep/forget durable and atomic under a
POSIX contract modelled as a crash RELATION (each entry returns to ANY value it held since the last directory
sync; an unsynced file returns ANY contents or unreadable).

**(ii) Evidence.** N:`decisions/hosting.md:1999-2081` (HOSTING-36/37) and `:2082-2139` (HOSTING-39);
`Hosting/Proofs/ResidentRun.lean:273 tick_order`, `Hosting/Proofs/ResidentVolume.lean:184 keep_atomic`, `:409
resume_durable` (MEASURED). Teeth: `keep_without_sync_tears`, `keep_without_syncDir_reverts`,
`in_place_loses_both`, `interpTwice_no_path`, `unresumed_keep_reverts`. Plants by hand (READ): `.sync` removed →
RED; a cmd node performed twice → RED; the intent keep removed → the proof RED and row Q6 RED. The first model
was NOT ACCEPTED by the vacuity reader (six holes: a deterministic crash made one lemma hold "only by that";
Stable/Fresh unestablished; torn merged with absent; a tooth tested `Runs` not the interpreter). Meta-critique
(`hosting.md:2024`): "The short proof was short because it said less." The trust boundary is NAMED: `ioHandler`'s
five fields ARE the five calls; `interp_runs` at one handler; the filesystem meets `Vol.apply` (operator);
single writer of `kept-*`.

**(iii) Mini.** The Hermes resident/controller is Rust: M:`native/resource-client/src/main.rs`,
`native/grain-runtime/src/main.rs`, `native/hermes-test-provider/src/main.rs` (MEASURED grep `hermes`); M:`Host/`
holds only `ResidentContextInspection.lean`; no theorem over the tick's effect order or its durability
(ASSUMED from the absence of a Lean controller). **Breadstuffs.** `deos-hermes/`, `dreggnet-hermes/` (MEASURED
`ls`), Rust; ASSUMED the same.

**(iv) Cost.** Premises: a `Handler`/`Prog` structure and continuation-style code where do-notation was
(nano names the readability cost). The crash model is the author's and must be a RELATION over every outcome
the platform may produce; a model that is a function makes every theorem vacuous about the disk. What refuses:
a keep or forget that fails part way ends the process `volume` and the restart RESUMES a whole keep of what
the volume holds before its first tick (HOSTING-39, every start costs one keep).

**(v) Verdict: TAKE-WITH-CHANGE (mini, breadstuffs).** Change: the pattern (tree + handler + recorder +
relation), applied to whichever loop in the bigger system answers a provider exactly once per ring. The
resident is the smallest loop that has all three hazards (order, double-send, torn file), which is why nano
could afford to prove it.

---

## F11 · A crash-loop window passes by the launcher's tick, as a theorem

**(i) Claim.** A controller whose clock is the latest launcher report never re-decides a crash-looped grain on
a quiet World (its window never passes); a `tick atMs` report every `tickMs` from the launcher's own clock makes
"the window passes" a theorem (`lifts_eventually`) while the decider reads no clock and stays pure.

**(ii) Evidence.** N:`decisions/hosting.md:2140-2204` (HOSTING-38), commit `d846c2d` (MEASURED);
`Hosting/Proofs/Loop.lean:626 lifts_eventually` (MEASURED); teeth `step_quiet`, `tick_ignored`, `lifted_length`;
option (A) the World's height REFUSED ("a window in Turns is a function of strangers' traffic"). The bell plant
measured (READ): the grain starts by itself at 59 s and 60 s after its crash loop with NO owner act. The G18
"replay" line was DELETED because it could never go red (determinism is a fact of `step`'s type).

**(iii) Mini.** M:`native/spk-host/src/grain.rs:1260`: "reported and never retried (exit 3; the template does
not restart on it)"; restarts are systemd's (`Restart=on-failure`, M:`deploy/candidate/INTERFACES.md:452`)
(MEASURED). So mini's window is the unit's `RestartSec`, outside any theorem; whether a crash-looped grain
needs the owner's stop/start in mini is ASSUMED unknown. **Breadstuffs.** Not checked (ASSUMED).

**(iv) Cost.** Premises: none on landed theorems (statements re-proved over `Report.grain?`). A report wire
case (`tick`) — both ends emit from one tree. Idle traffic: one frame per second per launcher. What refuses: a
controller without the case refuses a tick `badReport`.

**(v) Verdict: TAKE-WITH-CHANGE (mini).** Applies only where mini's controller, not systemd, decides
restarts; where systemd does, the finding reduces to "the window is a unit parameter nobody proved".

---

## F12 · A tick walks at most one word

**(i) Claim.** A tick that is "one step" lets `cat` copy 64 KiB and `beq` compare two 64 KiB operands for one
tick, so one law run under 100,000 ticks could do ~6.5 GB of work inside admission. Charging the byte primitives
one tick per 32 operand bytes, PAID BEFORE they walk, bounds a run to 32 B per charged tick (`walked_le`) with
every shipped program's required steps unchanged.

**(ii) Evidence.** N:`decisions/lang.md:2677-2740` (LANG-64), commit `5325ab5` (MEASURED);
`Lang/Proofs/Cost.lean:161 walked_le`, `:139 walked_le_paid` (MEASURED); `law_walks_le` 3,200,000 B per law run
(READ). The control: a tree with `wordBytes = 2^30` reproduces main's journey and rows output byte for byte
(READ). The unit was read off the COMPILED machine (`ByteArray.ext_iff` copies both operands). Plants:
`cat64_price` (2053 ticks, refused under 2052), `cat64_walks` (walks exactly 65,536 so `walked` is not 0 by
construction), `cat64_flat` (the old step prices it at 6 ticks: `walked_le` false for it). The reader's first
pass found the byte MEASURE vacuous (it copied the step's guard, so the flat machine read 0).

**(iii) Mini.** M:`Compiler/ObjectiveBendC4.lean:8-10`: "Every fuel is derived from the size of the input it
walks" — C4's linearizer already charges by walked size (MEASURED, the comment). Whether Objective Bend's
evaluator charges `cat`/`beq`-class primitives per byte I did not find (ASSUMED unknown; Bend values are not
bytes). **Breadstuffs.** `dregg-dsl-runtime/` fuel (MEASURED `ls`; ASSUMED per-step).

**(iv) Cost.** Premises: none (the reference derivation charges the same price, so `derives_lt_used`,
`bigStep_run` keep their statements). Deployed: a `deq` of two 32-byte digests costs 2 ticks where it cost 1
(stated, not measured). What refuses: a primitive whose budget runs out while paying has walked nothing.

**(v) Verdict: TAKE-WITH-CHANGE (mini, breadstuffs).** The change is the audit: list every primitive whose
work is not O(1) per tick in the deployed evaluator, read its cost off the compiled code, and run the
`wordBytes = 2^30` control before pinning.

---

## F13 · The package wire carries a version byte; the old shape refuses to load

**(i) Claim.** A format change that re-reads old bytes as a different value is a reinterpretation; one
version byte first on the wire, bumped by every `lang!`, refuses every earlier package by NAME before a tree is
read, and the refine's census label is derived from the constant so the two cannot drift.

**(ii) Evidence.** N:`decisions/lang.md:2505-2552` (LANG-60): under LANG-59 an older package's bytes DECODED as a
different package (big-endian literals); `Lang/Bounds.lean:65 packageWireVersion : UInt8 := 3`,
`Lang/Proofs/Wire.lean:670 unversioned_package_refused` (MEASURED); `packageCodec_label` ties the literal
`lang/package/3` to the constant ("bump one without the other and the build is red"). Measured cost (READ):
the Bell 21,780 → 21,960 bytes (+1 version, +175 doc, +4 framing); every package re-ids; a re-genesis for any
World holding package cells.

**(iii) Mini.** Per-structure version fields exist where a structure thought of them
(M:`Kernel/HyperdocumentTwoParentWitness.lean:251 schemaVersionMonotone`, MEASURED); a wire-level version on
compiled packages I did not find (MEASURED grep `wireVersion|packageVersion` in M:Kernel/Compiler/Host → only
`schemaVersion` hits; ASSUMED absent). **Breadstuffs.** `CANONICAL_STATE_SCHEMA_EPOCH` and `PersistentStore`'s
re-genesis gate (B:`CLAUDE.md`, READ): the same rule at the STORE level, not per content-addressed package.

**(iv) Cost.** Premises: none (`readPackage_package` holds with no new premise). What refuses:
`lang/package-version` for any other first byte; every pre-LANG-60 package (first byte 0, and no version may
be 0). Flag day: every package id.

**(v) Verdict: TAKE (mini).** Every content-addressed format with a decoder that could reinterpret.

---

## F14 · A member's connection is one fd with every close named, and the bound bounds

**(i) Claim.** A supervisor whose per-connection writer kept the only sender and the stream's clone leaked
two fds and a thread per departed peer, and its "bound" counted the routing map, not fds; one fd per connection
owned by `Conn`, counted until its `Drop`, a static `fds_max` (8 + 64 + 1 = 73), refusal at launch below
`RLIMIT_NOFILE`, and SIGTERM ending every peer by a NAMED close.

**(ii) Evidence.** N:`decisions/client.md:798-830` (CLIENT-28) and `:933-975` (CLIENT-30);
`client/src/mux.rs:63 fds_max` (MEASURED). Measured before/after (READ): (6, 2) → (70, 130) with 64 open under a
bound of 71; the 65th is `full`; (6, 2) after all end; old code at (410, 204). Mutations each red (M1–M5,
S1–S4). CLIENT-30: a SIGTERM to the unit made peers read a bare EOF (against CLIENT-28's law 7); now every
peer reads `closed unreachable`; nd-members stops a removed resident with a `GRACE` = 3·`reply_write` (90 s)
and SIGKILLs at the deadline (`memberStopForced`), live + stopping ≤ 2·RESIDENTS_MAX. Two TCB rows named
(`signal-hook`, `signal-hook-registry`).

**(iii) Mini.** M:`native/grain-runtime/src/main.rs:13590,17447,19779`: `signal_group(pgid, libc::SIGTERM)` —
the group is signalled (MEASURED); what a connected peer then reads is ASSUMED a bare EOF (no named close found).
No `RLIMIT_NOFILE`/`fds_max` check (MEASURED grep in M:native → 0). **Breadstuffs.** No `RLIMIT_NOFILE` in
`chain/` or `turn/` (MEASURED grep → 0).

**(iv) Cost.** Premises: none (Rust). What refuses: `refusedAtLaunch` when the soft limit is below `fds_max`;
`full` at the bound by Lean's existing name; a rebirth of a name still stopping (`memberStopping`).

**(v) Verdict: TAKE (mini's supervisors).** The two measurements (fd/thread counts before/after 200
connections; a peer's read on SIGTERM) take an hour each and either passes or finds this.

---

## F15 · The two-uid fence was refuted three times on its first real run

**(i) Claim.** A custody fence designed and planted on one uid (HOSTING-17, ratified twice) could not START a
confined process on two real uids, dropped its own setgid bit, and made its socket directories 02700 — three
refutations, each invisible on one uid, each found within the first hour of a real second uid on hbox.

**(ii) Evidence (READ: W:`HOSTING-LOG.md:1060-1120`, W:`resume/STALL-WATCH-20261007.md:1019-1022`;
not on main at `cdd9d84`, landing waited on GATES-10's `cargo-untraced` row kind).**
- R1: `/usr/local/libexec/nd-bwrap` is `root:<operator-group> 0750` by HOSTING-17's own install line, unexecutable
  by both `nd` and `nd-hosted`; every confined child goes through it. Ruled: a POSIX ACL for exactly the two
  uids.
- R3: `create_dir` then `chmod 02710` DROPS S_ISGID (Linux clears it on a chmod by a caller outside the file's
  group without CAP_FSETID; `nd ∉ nd-hosted` by §1); keybroker's own check then refuses 0710; nd-members has
  the same class. Ruled: `mkdir` with mode 0o710 inheriting setgid and group from the parent; no chmod, no
  umask window (ROOT refused the process-wide umask version).
- R4: under the units' `UMask=0077`, `mkdir(0o710)` gives 02700 (`Mode(1472)`); both `nd-keybroker.service` and
  `nd-members@.service` said 0077. Ruled: `UMask=0027` on exactly those two units (OPS-6).
- Checks 1 and 2 HOLD under the real uids (keybroker: `nd-hosted` → `NoAllowance` past the peer check; `nd`,
  a third uid with the group, `nd-hosted` with gid nd → `PeerRefused`; no group → `PermissionDenied` at the
  02710 dir); four plants RED (peer check `true`; `ConnectOwner` `true`; create-then-chmod reverted; umask
  0077). hbox `logs/hosting15-fence-r3.log` (READ, not opened).
- The decision had said so in advance: N:`decisions/hosting.md:1089-1090` "On one uid (every test on hbox)
  the owner/0600 branch runs and the cross-uid branch … cannot be produced"; the addendum `:2205-2243`
  "Never run. hbox has one uid … A real two-uid box is the first thing a deployment buys."

**(iii) Mini.** Mini hit R1's class FIRST: W:`STALL-WATCH:147-161` (10-15): m6grain on hbox failed at app-uid
exec (`165536 r-x on mini-grain-bwrap`) → "ROOT granted the narrow ACL"; M:`deploy/spk-host/install-user-world:29`
(`profiled_bwrap=/usr/local/libexec/mini-grain-bwrap`, per-app-uid ACLs, MEASURED). Mini's units say
`UMask=0077` (M:`deploy/spk-host/mini-spk-broker@.service:9`, M:`deploy/candidate/run.sh:264`, MEASURED) — the
R4 class if spk-host serves group sockets to app uids through a setgid directory (ASSUMED: I did not read
spk-host's socket-dir creation). **Breadstuffs.** Not checked (ASSUMED; `grain-jail/`, `sandstorm-serve/` exist).

**(iv) Cost.** No premises. An ACL line in the install, a `make_dir` helper, two unit hunks, a `cargo-untraced`
row kind (strace cannot run sudo). What refuses: `sockDir` by name when the unit's UMask is stricter than the
dir needs.

**(v) Verdict: TAKE (mini).** Concretely: read spk-host's and the broker's directory creation for
create-then-chmod, and the two units' UMask against the modes their sockets need. The finding behind the
finding (§20.8): a plant on one uid is a plant that holds fixed what the defect lives in.

---

## F16 · Checkpointing with a trust premise bound to the Store's recorded origin — IN FLIGHT

**(i) Claim.** Retain N sealed bases (floor 2); each kept segment opens with a MAC'd header binding the origin
chain, start offset, steps, chain and index count; a follower that opens from a base it did not seal does so
under a NAMED premise `CheckpointTrusted o w` over the Store's recorded ORIGIN (which already commits the
start: genesis = hash of the founder inputs, carry = hash of name/nonce/exported origin/roots/allowance/height/
journal), with `start_unique`; a page before the retained range is refused `checkpointed`, a flipped header
`checkpointCorrupt`, another origin `foreignOrigin`.

**(ii) Evidence (READ only; not on main).** W:`HOST-LOG.md:1384-1420` (HOST-20: compiles WHOLE, Host 192 jobs;
seeds 1–3 ALL PASS with the teeth; the second-agent read found `CheckpointTrusted` WEAK twice — first a budget
fact a received base discharges locally, then an ∃ over a carried preimage — and ROOT's "add a start-digest
field" was REFUTED by HOST-20 because `World.origin` already commits the start: STALL-WATCH 21:08Z, 21:18Z 10-21).
W:`DECISIONS-20261021.md` CARD 1 (the pause item, the options, the conflation: "replay too damn high" names a
NEW follower's cold audit, which dropping segments does not fix). Prior art read by HOST-19 (STALL-WATCH
19:16Z): breadstuffs' `CheckpointAttested` premise "is UNUSED in every proof"; delvetalk2's segmented journal;
"minidregg keeps every checkpoint despite its doc".

**(iii) Breadstuffs.** B:`metatheory/Dregg2/Distributed/CheckpointPrune.lean:62,166`: `CheckpointAttested` is
"the named crypto portal … NEVER `:= True`"; MEASURED: 11 mentions in the file, 0 in any `theorem` line. A
premise that yields no conclusion is the lesson HOST-19 took. **Mini.** `checkpointEvery` default 64
(M:`Host/SourceAgreementReader.lean:59,89`), every accepted record past it "seals a checkpoint"
(M:`docs/DURABLE-STORE.md:72-74`); retention: none (READ HOST-19; ASSUMED from the doc).

**(iv) Cost.** Premises (READ, CARD 1): `fold_reaches_host` unchanged; the `deployed_*` reached-World theorems
gain "a base World is reached", discharged on the writer and NOT for a received base → `CheckpointTrusted`;
backup theorems restated over the file sequence; `historyClean` = "clean from the oldest checkpoint". What
refuses: `checkpointed H` (exit 61), `checkpointCorrupt` (62), `foreignOrigin`, `foreignSegment`,
`segmentShort`, a missing `seg.<o>.log`. LOST: a fresh party re-deriving the dropped prefix from THIS Store
(an archive role keeps it).

**(v) Verdict: TAKE-WITH-CHANGE (breadstuffs, mini), pending the landing.** For breadstuffs the change is
the test HOST-19 applied: `CheckpointAttested` must appear in the statement that opens from a received
checkpoint, or be deleted. For mini: retention is a real design choice; the premise is the part to copy.

---

## F17 · Relations as rows in the one trie, commuting inserts, path compression, one printer

**(i) Claim.** Keyed, bounded rows under an object live in a third instance of the one trie; two inserts at
distinct keys commute because their footprints are disjoint (`admit_comm`, both orders admitting), never
because a pin is relaxed; a relation head counts and sums and is never pinned; a range read is pinned by its
listing; and every object prints through ONE printer (`read OBJ ?`, `read OBJ REL K`).

**(ii) Evidence.** N:`decisions/lang.md:1203-…` (LANG-44, the delvetalk comparison: delvetalk's commutation is
`#guard`ed, not proved), commit `42c261b` (kernel!, the rows day, MEASURED); measured ports (READ, memory 10-18):
CappedTally tally 630 like Mini; CoAuthor 64K → 37K chars on four relations, then 2,464 with the authoring
surface (LANG-50, `87dff6e`) vs Mini's 7,896. The cost it exposed and fixed: ~564 hashes per row insert from
an uncompressed trie over a 280-bit shared prefix (KERNEL-49 PROPOSED, N:`decisions/kernel.md` "## KERNEL-49";
ruled: path compression with the branching depth IN the hash, "without it … an exclusion proof then forges";
~9 hashes after, READ memory). The printer: `decisions/protocol.md:1206` (PROTOCOL-44, "objects describe
themselves … through the one printer; refusals print what to do next"), `:1622` (PROTOCOL-51 range read),
`:1515` (PROTOCOL-48 a programmed object's state value). The key injectivity is F6.

**(iii) Mini.** No kernel relations (W:`NANO-VS-MINI` §2 lists invariant domains, hyperdocument event logs,
but no keyed rows; M:`Kernel/HyperdocumentEventLog.lean`, `HyperdocumentMerge.lean` are the nearest shape,
MEASURED `grep Relation`). Mini's CoAuthor surface is 7,896 chars (READ). **Breadstuffs.** delvetalk2 (a
sibling, not breadstuffs) had relations; breadstuffs' cell model is slots (ASSUMED).

**(iv) Cost.** Premises: nano's rows day added instance premises (`[Std.TransOrd D] [Std.LawfulEqOrd D]`) only
on NEW statements (`kernel.md:2629`); the floor on a head (F1) was needed so retracts do not break commutation.
A fourth trie instance in every `roots` digest (flag day). What refuses: 13 named rows refusals (`keyTaken`,
`relationFull`, `missingRow`, `orphanRow`, `rowParentUnpinned`, `rangeUnpinned`, …).

**(v) Verdict: TAKE-WITH-CHANGE (mini).** Change: mini's relation need is measured by its own documents and
CoAuthor; take the trie-instance shape and the commutation theorem, and the one printer with it (mini's
`read` surface is many printers, ASSUMED).

---

## F18 · "A refusal renders as the expected verdict" is a class, and hints sit beside names

**(i) Claim.** A refusal that a consumer maps onto one of its ordinary outcomes (`lost` → `uncertain`;
`absent`; a reader that matches green) is a class of defect, not an incident; the cure is a NAME on the wire
for every refusal (CHARTER law 7), a verdict reader that proves it can read red (GATES-15), and a HINT line on
stdout beside the name on stderr so the next step is printed without becoming the verdict.

**(ii) Evidence.** N:`decisions/protocol.md:1734-1760` (PROTOCOL-55): `rows bell` printed `uncertain` for an
install the writer had COMMITTED, because the confirm's receipt was `refused badResult` (an empty page short of
the tip: the install event, 31.5 KB, exceeded a GUESSED page budget 16384), `drive` read the refused confirm as
`lost`, and `Attempt.next` mapped (confirm, lost) → `uncertain`. Fix: the budget DERIVED (`eventBytesMax + 5`),
with the theorem that a walk that served nothing serves the first step; the guessed bound "broke twice" (4096,
16384) and the deployed 65536 was ALSO short by 5. CHARTER law 7 (N:`CHARTER.md`, MEASURED): "a parse failure is
never rendered as a verdict; 'uncertain' is a real outcome". Hints: `protocol.md:1206` (PROTOCOL-44: `stale
CELL` → read it and run again; `lawDenied LAWHEX` → the law's own words; "every other refusal prints no hint";
hints are client-side text decided from the refusal VALUE, not carried in the wire name — its meta-critique:
"I first wrote that a hint in the wire frame was the better design, deferred for cost. That was the pricing
move CLAUDE.md names"), `:1720` (PROTOCOL-54: a method's refusal reaches the member in its own words, `hint
program: answer: refused notResident`; REASON bounded by `reasonMax`, newlines folded, "a hint, never a
verdict"), `cdd9d84` (PROTOCOL-59: `rangeUnpinned` with its hint; `beforeLog` reported "with its remedy and
never acted on"), `decisions/host.md:2712` (HOST-61 `beforeLog` by name). The same class at the gate: GATES-15
(`gates.md:357`): CLIENT-6's mutation harness "read every mutation green behind `cargo test -q`".

**(iii) Mini.** No `hint` in M:`protocol/` or M:`Host/` (MEASURED grep → 0). The memory
`minted-refusal-renders-as-the-expected-verdict` records the class in the mini/bread lineage (a parse failure
rendering as `"1"`, the same string as `ConstraintViolated`; a wire disagreement refusing every turn under a
false diagnosis). **Breadstuffs.** `TurnError` has 1,341 `refus` mentions in `turn/src` (MEASURED count); whether
any consumer maps a refusal onto a success-shaped outcome is ASSUMED unaudited; `EffectsHashMismatch` — the
07-27 memory's "constructed zero times" — is now constructed at B:`turn/src/executor/execute.rs:1740-1746`
(MEASURED), so that one closed.

**(iv) Cost.** None in premises. A hint column per refusal value in the client; a `--harness-control` per
verdict exe; a `nobin RED` control per cargo row. What refuses: a runner whose control passes.

**(v) Verdict: TAKE (mini, breadstuffs).** Audit every place a refusal value meets a `match` whose other arms
are outcomes.

---

## F19 · Adoption judges the state

**(i) Claim.** A law holds from the turn that adds it; that turn runs the laws in force on `relaw laws'` (the
authority to change laws) and every ADDED law on `adopt laws'` over the UNCHANGED state, so a law that refuses
the state it is added over is refused by name and never installed; no `since` height.

**(ii) Evidence.** N:`decisions/kernel.md:687-696` (KERNEL-27: ROOT's `relaw` wording made `Frozen`
uninstallable; the `.birth` conflation refused), `:2874-2883` (KERNEL-57, commit `7862b65`);
`Kernel/Proofs/Authority.lean:193 law_judged`, `:221 law_adopt_refused` (MEASURED). W:`COMPARE-20261021.md` §1:
delvetalk's scar W8/F7 ("a rule added later does not reach existing state"); mini's ADOPT.

**(iii) Mini.** M:`Kernel/ObjectiveActivityUpgrade.lean:1-14`: ADOPT requires the next policy to only tighten
(`UpgradePolicy.permits`), the next law to ENTAIL every floor with an unsat certificate (`adopt_floors_entailed`),
and the current state to migrate and pass the next record's judgment — stronger than nano's, with a drain
window because activities outlive a turn (MEASURED the header; COMPARE §1.2 for the theorem lines).
**Breadstuffs.** No law change at all; a cell's program is fixed (COMPARE §1.2, READ).

**(iv) Cost.** For mini: nothing to take; it already judges adoption more strongly and proves it as a
reachable-world invariant (COMPARE §1.2). The one small transfer would be a KERNEL-side theorem naming what the
receiver's two judges decide (`law_judged`'s shape) if mini's is only in the upgrade module.

**(v) Verdict: NANO-ONLY.** Nano confirmed delvetalk's scar and converged on what mini already had; the
finding is for the next robigalia's spec, not for mini.

---

## 20 · What nano has shown ABOUT THE METHOD

Each rule with the incident that minted it. Tags as above.

**20.1 The disjunct check.** Read each disjunct of a conclusion on its own: is it provable from the premises
alone, or from the instance? Incident: KERNEL-56 (F8), 61 landed theorems with `∨ Collision`, green through
builds, census and two vacuity reads, found when a proof lane noticed a sorry closed in one line
(`kernel.md:2642`, READ). Since then every second-agent read is "with the disjunct check" (MEASURED: 20+
decision entries say so, e.g. `host.md:2534,2586,2606`, `lang.md:2552,2594,2637`, `hosting.md:2019`), and it
keeps finding: LANG-64's byte measure vacuous on the flat machine (`lang.md:2730`), LEDGER-14's list-chained
`Runs`, HOSTING-36's label grammar that "proved the brief's order while admitting an ask about any ring".

**20.2 Price premises, not cost.** A design's price is every premise it puts on a LANDED theorem; a rebuild is
free. Incidents: KERNEL-49 (memory `minted-price-premises-not-only-cost`: a journal-in-the-trie design approved on
hash counts would have put a `Canon` premise on ~150 cell theorems); KERNEL-54 STEP 1 (`kernel.md:2574-2592`):
356 statements measured BEFORE ruling, N = 0 premises, H′ = 3, H ≥ 5 and two broken theorems — the
measurement overturned ROOT's prior. The counter-incident, named by the same decision: "the measurement that
priced the day counted premises on landed theorems but could not see a missing premise on a new one"
(`kernel.md:2633`): phase 1's two false statements.

**20.3 A plant that cannot go red is not a plant.** Incidents: GATES-14 (`gates.md:313-350`): the toy run's
`carry-budget-plant:overflow` could not go red at a UInt64 digest (a cell weighs less than a retire charges),
so the ungated toy run was DELETED ("an ungated run with a vacuous plant is worse than no run: it reads as
coverage"); GATES-15 (`gates.md:368`): a `runs.py` raising at entry read `PRE-PUSH GREEN` under the old judge
— the runner had never proved it could read red; HOSTING-38 (`hosting.md:2178,2194`): a G18 "replay" line
drafted and DELETED because determinism is a fact of `step`'s type. The standing rule: every verdict exe
carries a known-red control that runs FIRST.

**20.4 The two table rules.** Every landing that moves a codec tag: (1) each refine site has a lawfulness +
canonicity theorem and vectors with a boundary pair; (2) a row under an unchanged tag is immutable (regenerate
the tsv from an EMPTY file; `--write` keeps rows already under a tag). Incident: CODEC-28 / GATES-13 (W:`STALL-WATCH:570-583`,
10-17): "a hand edit relabelling a vector's meaning passed `--check`, a decode check not byte equality" → row
immutability checked against the parent, plants edited/removed/added rows red. Text: W:`CODEC-LOG.md:879-883`;
decision N:`decisions/codec.md:754` (READ). LANG-60's corollary: a refine's Shape carries its NAME, so the label
is DERIVED from the version constant (`packageCodec_label`).

**20.5 A stat is a proxy.** A key that records a stat by MODE lets a changed file carry a verdict; cargo's
fingerprint compares mtime and size, so a stat is a read of the bytes and is keyed by CONTENT. Incident:
GATES-20 (`gates.md:518,575`): "The design's two soundness claims both failed when built: a mode-only stat, and
a re-trace check keyed on the fresh read-set. Each would have been a quiet false reuse." Found by building and
running, not by reading the design; the design's 53.4 % reuse was the flattering number, 41.8 % as built.

**20.6 One write per line.** A diagnostic line written in pieces (`eprintln!` = three `write(2)`s) lets
another process's whole line land inside it; one `write_all` per line, one writer for every binary. Incident:
`2e84396` (MEASURED `git show`): 31/4000 red before, 0/4000 after, twice; strace confirmed; the test's match
tightened from a substring to a whole line; the same class as HOSTING-9's keybroker end line; three copies of
the rule made one (`nanodregg_launcher::say`).

**20.7 `cv adopt` after a prune, before respawning.** A pruned session's lanes are dead ids with live worktrees;
adopting the transcript keeps the context, respawning loses it. Incident: W:`STALL-WATCH:1009` (10-21 19:11Z):
OPS-6 adopted whole; "seven successors were already driving their worktrees so their predecessors stay dead";
rule W:`LANE-RULES-NANODREGG.md:15` (`cv lanes --recent N --unfinished` then `cv adopt`; spawn fresh only past
~400K). Memory 10-17: after a compaction, re-read the back-and-forths with `cv show --kind prompt,answer`.

**20.8 The plant holds fixed what the defect lives in.** Three incidents a week apart, each named by its own
decision: GATES-19's plants never moved HEAD (the silent revert, `gates.md:512`); GATES-20d's plants held the
cargo cache order (the warm/cold re-trace red, `gates.md:605`); HOSTING-17's plants ran on one uid (F15,
`hosting.md:1089`). The test of a plant is the variable it does not vary.

**20.9 Measure findings, not landings (Ember, 10-21).** The judge queue's first day showed the swarm's goodput
was low with 6–8 landers tying at the age bound (GATES-19 measured first day, `gates.md:465`); the fluid rule
measured 0 % skip over 61 re-judges because one row walks the whole tree (STALL-WATCH 19:58Z 10-21). This
paper is the form that ruling asked for: what was SHOWN, with its number, over what LANDED.

---

## 21 · Residue: what this study could not settle, and the one question for the next robigalia

- Three candidate items are in flight (F16, F15, GATES-20h); their evidence is a compile, a sim and lane logs,
  not a landed judge. Re-read them at the landing hash.
- Every mini and breadstuffs "what it does today" is a grep and a header read, not a construction of the failing
  sequence; where I say ASSUMED, a lane's first task is the sequence.
- The date discrepancy between git and the logs is unexplained by me (ASSUMED one history).
- Counts worth carrying: nano `cdd9d84` has 4,966 theorems, 0 `#guard`, 0 `sorry`, 0 deployed `partial`, 41
  runs rows, 18 waste rows every ratio at its ceiling (MEASURED `SIZE.md`, grep, `gates/*.tsv`); mini
  `334316df` has 4,284 `#guard` occurrences and 0 `sorry` terms (MEASURED grep, `.lake` excluded); breadstuffs
  `22fad151e` has 17,095 `#guard` and 1 `sorry` in `metatheory/` (MEASURED; memory's 14,399 was an earlier
  count) with `metatheory/docs/GUARD-DISCIPLINE.md` and `scripts/check-guard-discipline.py` already written.
- The question the nine TAKEs put to the next robigalia: which of them are laws of the SPEC (F1, F3, F8, F13,
  F18 read as "the format refuses, the bound is derived, the escape names its inputs, the refusal is a name")
  and which are laws of the SHOP (F5, F7, F14, F15, §20). Nano's charter wrote both into one file; the next
  system should know which is which before it writes line one.
