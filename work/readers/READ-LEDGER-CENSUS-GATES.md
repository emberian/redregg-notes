# READ — LEDGER + CENSUS + GATES (nanodregg origin/main f9657bd, 2026-10-24)

Reader: one whole-file reader (Claude Opus 5.5) under `redregg/work/readers/BRIEF.md`. Nothing edited in
nanodregg. Two scratch measurements (below, MEASURED) ran in this session's scratchpad only: a copy of
`Census/Statements.lean` compiled alone with the v4.30.0 toolchain, and `gates/decls.py`'s own `judge`
driven over hand-made export rows the way `gates/decls_plants.py --synthetic` drives it.

## Verdict

I read whole: Census/Statements.lean, Census/Axioms.lean, Census/Certificate.lean,
Census/CertificateData.lean, Census/Refines.lean; Ledger/Escrow.lean, Ledger/EscrowSpec.lean,
Ledger/Proofs/GrantCap.lean, Ledger/Proofs/EscrowInvokes.lean, and the statements of Ledger/Proofs/Escrow.lean;
gates/census.py, statement_plants.py, decls.py, decls_plants.py, certificate.py, certificate_plants.py,
tcb.py, tcb.tsv, waste.py, waste.tsv, refusals.py, fast.py; most of scripts/pre-push and the verdict half of
scripts/bar.sh; the entries GATES-23, 20q, 20s, 20t, 20u, LEDGER-14, 15, 18, 19 and PERF-13. I read the rest
in part (headers, declaration lists, the functions the gates call); the list is at the end.

The gates are better than most I have read. Each one has a known-red control that goes through its own
comparator, and the plants check that their mutation happened before they read a verdict. The Ledger
theorems say what their decisions say. The gate question still has a bad answer in three places:

1. **The declaration diff (GATES-20t) cannot see a change of meaning made through a definition, and it accepts
   any change it can see once the change is named.** Check 1 compares theorem and axiom statement digests
   only. A digest names each constant and does not include its body. So `MovesThrough := … ∧ False` changes
   no digest and needs no map line: MEASURED `decls: ok … 0 map line(s)`. A theorem restated to `True` passes
   with one `RESTATES-MEANING:` line: MEASURED `decls: ok … 1 declared change(s) of meaning`. That is the
   truck. Nothing checks that the new statement is not weaker, or that law 6's second reader saw it. Outside
   the certificate's one theorem, and outside the one level of vocabulary the certificate pins, no gate pins
   a meaning.
2. **The default landing (GATES-22 FAST) runs none of the censuses or plant rows.** It skips the axiom census,
   the statement census, the refine census, the certificate pin, `statement_plants`, `certificate_plants`,
   `decls_plants --synthetic`, ledger-sim and the waste measurements. They run only at the 3-hour
   convergence. No source gate refuses `native_decide`, so a `native_decide` theorem with no allow row lands
   green and is seen hours later. GATES-20s, GATES-20u and PERF-13 all say their rows run "on every judge";
   in the default mode, they do not.
3. **The statement census's known miss is still in the code, and MEASURED there are more.** The `.size ∈`
   projection miss (cv 01a1654c-543c) still reads ok, and its planned fourth plant (`forgotten`) is not in
   `statement_plants.py`. These also read ok: `¬ Function.Injective h`, a Bool collision
   `(h a == h b) = true`, and `¬ h a ≠ h b`. A disjunction under a `∀` nested inside an `∃` produces no row
   at all. No landed theorem has any of these shapes today: there is no `.size ∈` / `.length ∈` in the
   tree's source, by git grep.

The answer to each of the brief's specific questions is in the findings: D1/D2 (RESTATES-MEANING), D3 (the
census miss), D6 (the certificate's four pins), D7 (tcb.tsv), B4 (waste's 1/1/0), and L1–L3 (the Ledger's cap
and LEDGER-15's history).

---

## DEFECTS

### D1. The declaration diff cannot see a change of meaning made through a definition
- **Where.** gates/decls.py:470-500 (READ). The check-1 loop judges a parent row only when `c is None` (a
  deletion) or when `p.kind in STATEMENT_KINDS and p.stmt != c.stmt` (STATEMENT_KINDS =
  {theorem, axiom}, decls.py:184).
- **Why the definition is invisible.** A definition whose value changed is never named. The statement digest
  of a theorem that names it does not move either: `digest_row` hashes the statement's DAG plus the constant
  NAMES (`sha(ts, cs(tc))`, decls.py:212-213), never the named constants' bodies.
- **Mutation.** GATES-20u's own P3 (`MovesThrough … ∧ False` plus a re-proof) MEASURED against decls.py's
  `judge`, with the export replaced by rows the way decls_plants.py's synthetic mode does it. The parent has
  `Demo.A.MovesThrough` (definition, value V1) and `Demo.B.grant_moves_le_cap` naming it. The candidate
  changes only MovesThrough's value. Result: `def-body-weakened exit 0 decls: ok — 2 module(s) exported, 2
  parent declaration(s) in the reach, 0 map line(s), 0 declared change(s) of meaning`.
- **What else covers it.** Only the certificate (D6), for one theorem and one level, and only at convergence
  (D4). Every other theorem's meaning can move through any definition it names.
- **The gap in the record.** GATES-20t's decision text says check 2 "is what catches a reverted definition
  body". That is true only for a STALE copy (a lack that `rebase.py stale` forwards). A forward edit is
  never judged. GATES-20u says the same of 20t ("on a forward edit it compares only theorem and axiom
  statements"), so the gap is recorded there. It has no entry of its own, no cv task named in 20t, and no
  synthetic plant that pins it as a known miss.
- **Severity.** DEFECT. The gate claims to judge "every theorem whose statement it changes", and meaning
  lives in definitions.

### D2. RESTATES-MEANING: a declared change of meaning is accepted on the declaration alone
- **Where.** gates/decls.py:461-464 (READ). For RESTATES-MEANING, the only check is that the statement DIFFERS
  (`elif same(p, c): … unused map line`). Nothing compares the strength of the old and new statements,
  names a reader, or keeps a set of protected statements.
- **Mutation.** MEASURED the same way: `grant_moves_le_cap`'s row replaced by a statement with no constants
  (`TRUE`), message `RESTATES-MEANING: Demo.B.grant_moves_le_cap` → `theorem-to-True-declared exit 0 decls:
  ok … 1 map line(s), 1 declared change(s) of meaning`. The synthetic plants pin this as GREEN on purpose
  (decls_plants.py:286, the `restated-meaning` case).
- **A second door.** A two-name line on a DEFINITION, `RESTATES-MEANING: Foo → Bar`, adds `Bar → Foo` to the
  inverse rename map (decls.py:386-387, 404). Every candidate statement that names `Bar` is then digested
  as if it named `Foo`. So one line moves the meaning of every theorem over Foo, and none of them is named.
  It is the same hole as D1, reached by a line instead of by an edit. INFERRED from decls.py:386-407.
- **Is it a truck?** Yes. The line is findable (`git log --grep RESTATES-MEANING:`), which is all
  GATES-20t claims. It is not a check. Law 6 ("every theorem statement is read by a second agent before it
  lands") has no gate. The only thing standing between a landing and a weakened theorem is the lander's own
  message.
- **Severity.** DEFECT. The decision is honest that this is the design. But the design means any statement
  can be weakened if it is named, which is what the brief asked.

### D3. The statement census reads several vacuous shapes as ok; the cv 01a1654c-543c miss is still in the code
- **Where.** Census/Statements.lean:52-61 (`leftFreeRounds`: a membership bounds every chosen variable the
  element term CONTAINS, `m.appArg!.containsFVar`); :104-109 (an escape is only an `Eq` whose two sides
  share an app head); :88-114 and :123-146 (the walks enter only `∃`, `∧`, `∨`, `↔`, and up to four unfoldings
  of the roots' OWN definitions; any other head, `∀` included, ends the walk). READ.
- **MEASURED.** I compiled a byte copy of Census/Statements.lean alone (it imports only Lean), then a module
  `P.T` of six theorems over `h : List Nat → Fin 4`, each proved by `.inl trivial`, and ran
  `#statement_census "out.tsv" P` (scratch `sc/`):
  - `forgotten : True ∨ ∃ a b, a.length ∈ [5] ∧ b.length ∈ [5] ∧ a ≠ b ∧ h a = h b` → **ok**. This is the
    named next tooth of GATES-20s (cv 01a1654c-543c), unchanged. The plant does not hold it:
    statement_plants.py:31 `VACUOUS` still has three names.
  - `notinj : True ∨ ¬ Function.Injective h` → **ok**. `Function.Injective` is core, so `unfoldOwn` refuses
    to unfold it (Statements.lean:72-73).
  - `beq : True ∨ ∃ a b, a ≠ b ∧ (h a == h b) = true` → **ok**. The right side of the `Eq` is the constant
    `true`, not an app.
  - `notne : True ∨ ∃ a b, a ≠ b ∧ ¬ h a ≠ h b` → **ok**. `Not` is not walked.
  - `hidden : ∃ n, ∀ m, m = n → (True ∨ ∃ a b, a ≠ b ∧ h a = h b)` → **no row at all**. The `∀` under the `∃`
    ends `disjunctions`, so this escape is never even listed for a human reader.
  - control `ctl : True ∨ ∃ a b, a ≠ b ∧ h a = h b` → RED, as it should be.
- **Present on main today?** Not as a landed theorem: `git grep -nE '\.(size|length|…)\s*∈'` over `*.lean`
  matches nothing, and no landed disjunct uses `Injective`, `==` or `¬ … ≠` around a digest. That is from
  the source text only. Through unfolding, a membership on a projection can still arise from a definition,
  which this grep cannot see.
- **The fixtures.** Only the classifier's two-sides test is mutated (statement_plants.py:140-141). Nothing
  mutates `leftFreeRounds` to over-bound (for example, `containsFVar` replaced by "any membership bounds
  everything"). Fixture 3 would catch that one. Narrower over-bounds, like the projection rule above, are
  invisible to every fixture.
- **Severity.** DEFECT, for the census's claim "the rule reads structure, never a name". It reads one
  structure, an equation with one head, and four others pass. No landed instance was found.

### D4. The default landing judges none of this layer's verdicts; `native_decide` lands unrefused
- **What a fast landing runs.** gates/fast.py:46-52 (READ): a landing is FULL only for a `!:` subject or a
  change to gates/*.py or scripts/. scripts/pre-push:319-370 (READ), fast mode: gates, the build of reached
  targets, `decls_judge`, cargo check/fmt, then `PRE-PUSH FAST GREEN … (the census, rows, benches, waste,
  generated files and clippy judge it at the next convergence)`.
- **So, per landing,** none of these run:
  - census.py: the axiom census (sorryAx, `Lean.ofReduceBool`, new axioms), the refine census and the
    statement census;
  - the four script rows (certificate.py, certificate_plants.py, statement_plants.py, decls_plants.py);
  - ledger-sim and waste.py `--measured`.
- **What the source gates refuse.** gates/refusals.py:26-40 (READ) refuses `sorry`, `axiom`, `partial`,
  `unsafe`, `@[extern]`, and other commands and options. It does not refuse `native_decide` or
  `decide +native`. No other source gate does: `git grep native_decide gates/*.py` finds only tcb.py's
  table-consistency checks.
- **Mutation.** A theorem `:= by native_decide`, with no row in gates/axioms-allow.tsv, in a LEDGER commit
  lands FAST and green (lakefile warningAsError does not fire on native_decide). The axiom census reds it at
  the next convergence, and the revert rule acts a convergence after that (scripts/converge:13-15).
  INFERRED from those three files; I did not land anything.
- **The same applies to:**
  - a vacuous disjunct (D3's ok shapes aside, even the RED ones);
  - a re-pinned or broken certificate (D6);
  - a planted Statements.lean weakening. Census/*.lean is a Lean module, not gates/*.py, so changing the
    census's own Lean is a FAST landing judged by nothing in this layer until convergence.
- **The prose says otherwise.**
  - GATES-20s: the statement plant is "selected on every judge, run after the build".
  - GATES-20u: "every judge runs it after the build, 9.5 s".
  - PERF-13 (d): "the forced-stale comparator is in --harness-control, which runs.tsv runs on every judge".
  - CHARTER law 6: "No `sorry` ever lands". The build's warningAsError does hold that one.
- **Severity.** DEFECT. The gates are post-landing detectors under the default mode, and three decision
  entries describe them as landing gates. Ember's GATES-22 ruling chose this, so the shape is not the
  defect. The defect is that `native_decide` has no source refusal, and that the entries were not re-read
  against 20t's and 22's mode split.

### D5. The refine census accepts a vacuous lawfulness theorem
- **Where.** Census/Refines.lean:56-73 (READ). `lawfulHead?` takes the conclusion after `forallTelescope`, so
  premises are dropped unread. It refuses `LawfulOn P c` only when `P` is syntactically
  `fun _ => False` (`constFalse`).
- **What it accepts.** `theorem t (h : 1 = 0) : Lawful (c …)`, `LawfulOn (fun b => False ∧ True) c`, and
  `LawfulOn (fun b => b.size > 2^70) c` each count as "has a lawfulness theorem". The site is then pinned by
  nothing that bites (CODEC-28's whole point).
- **Severity.** DEFECT (INFERRED from the code; not measured. The command hard-codes the
  `Nanodregg.Codec.Stream.*` names, so a scratch test needs that namespace stood up). Same class as D3: a
  name check where a satisfiability check is claimed.

### D6. The certificate's four pins: what they still miss
- **Where.** gates/certificate.py, Census/Certificate.lean, Census/CertificateData.lean,
  gates/certificate-grant.json (READ). Vocabulary (48 constants, listed from the pin) is one level:
  `CellsCanon`, `LedgerContiguous`, `GrantStep`, `MovesThrough`, `audit`, `ledgerLeft`, `World.live`, `Chain`
  and the core constants. A body two levels down is unpinned.
- **Edits it still misses, beyond 20u's own critique (a) (`Dispatched`):**
  - **(i) A vacuous premise one step under LedgerContiguous.** `LedgerContiguous` is pinned, but its body
    names `GrantContiguous` (Kernel/Proofs/LedgerNext.lean:48-55), which is not. `GrantContiguous cell :=
    … ∧ False` makes `hlc` unsatisfiable at every World holding a live grant, and `hl` demands one. So
    `grant_moves_le_cap` holds of nothing. The pin stays GREEN: the statement, the axioms, the 67 supports'
    TYPES and LedgerContiguous's payload are all unchanged.
  - **What the edit costs.** The proofs that construct contiguity (`genesis_ledgerContiguous`) break and
    must be restated or deleted with one map line each. D2 accepts those lines.
  - **(ii) Two levels under `audit`.** `audit`'s payload is pinned, but it names `auditStep` → `auditTurn` →
    `rederive`/`receive` and `World.admit`. A change to `auditTurn` (say, accept without `rederive`)
    changes which histories the theorem is about and is GREEN. This is the "meaning cone" 20u priced at
    2,444 declarations and declined. It should be stated as a miss the plant set records, not left
    implicit.
  - **(iii) `countOf` / `ledgerSpendsMax` under `ledgerLeft`.** These define what `left` reads, and both
    are unpinned.
  - **(iv) The twin.** `grant_credits_le_cap` (GrantCap.lean:273) is not pinned at all (20u (f)), though it
    is the same scheme over another base.
  - **(v) The pin file is data.** gates/certificate-grant.json is `gates/` data. Editing it is a FAST landing
    (D4), and owners.py lets any layer touch it with a `CROSS-LAYER: GATES …` line (owners.py:50-57). So
    "`--emit-pin` is the only writer" (20u) is a convention. A landing that weakens GrantCap's vocabulary
    and re-pins the JSON in the same commit is GREEN at its landing and GREEN at convergence (live = new
    pin).
- **The plants exercise the right object.** C0 asserts that the copy's pin equals the real environment's
  pin (certificate_plants.py:159-162), and the mutants share the gate's `differences`. They prove the
  comparator per section, and that P3 is caught at one level. They do not prove (i)–(v).
- **Severity.** DEFECT for (i) and (v): a vacuity and a re-pin that the pin is advertised to stop
  ("vacuity: `MovesThrough … ∧ False`" is the reason given for the fourth pin). (ii)–(iv) are QUESTION-level
  scope notes.

### D7. tcb.tsv: unrowed unsafe holders; pins nobody compares; a row that trusts Rust for an ordering decision
- **MEASURED: unrowed unsafe holders.** `tcb.check('.')` returns `[]` (green). Of Cargo.lock's crates, these
  are unmatched and rowless: `rustix`, `libc`, `linux-raw-sys`, `errno` (the syscall layer), `generic-array`,
  `num-bigint`, `nom`, `base64`, `data-encoding`, `time`, the serde family and others. `rustix =1.1.2` is a
  DIRECT dependency of client/, sandbox/ and launcher/ (their Cargo.toml lines 23/13/36/62, READ). It is
  where those forbid-unsafe crates' fs/process/net syscalls go, which is exactly what tcb.py's own docstring
  defines as an UNSAFE_HOLDER ("the unsafe a forbid-unsafe crate delegates", tcb.py:9). `UNSAFE_HOLDERS`
  lists only signal-hook (tcb.py:41).
- **READ: pins that are text.** The rows for `cc (hbox)` (a gcc sha256), `nd-bwrap (hbox)`, `nd-bwrap
  AppArmor profile`, `sandbox-exec (macOS)` and `nd-bwrap (burst5)` (whose pin reads "pin NOT measured")
  carry pins that tcb.py never compares. It compares only Cargo.lock crypto crates, the lean4 toolchain,
  native_decide rows, extern rows and lake packages (tcb.py:115-153). GATES-12's "pinned to what is actually
  used" holds only for those kinds. A wrong sha256 in the cc row is green.
- **"Trusted for" is never read.** tcb.py checks only that the field is non-empty (tcb.py:100). Most rows'
  sentences are about bytes: a primitive, a parser, a syscall wrapper. The exceptions are decisions:
  - **`stdio-leg`** (tcb.tsv:54): trusts client/src Rust that "the resident's member commands are served,
    in the order it sent them, by ONE follower … an ok reply … is that follower's Lean done". That is an
    ORDER-and-SELECT claim made by Rust. Law 2 says Lean decides it ("every accept/refuse/select/order …").
  - **`rustls-webpki`** (:30) and **`webpki-root-certs`** (:33): accept/refuse decisions about certificate
    chains, taken in Rust, and "keybroker trusts any of its CAs".
  - **`ed25519-dalek`** (:10): "accepted … only as observed by the journey rows (vectors, no theorem)" is
    bytes, honestly labelled.
- **Severity.** DEFECT for the unrowed rustix/libc (the table is gated as complete for the holder class,
  and is not) and for the uncompared pins. The stdio-leg row is a QUESTION: either it is a decision, so law
  2 wants it in Lean, or it is transport and the sentence overclaims.

### D8. THE BAR's clock limits cannot go red in any run that happens
- **Where.** scripts/bar.sh:625-648 (READ). In `--standing` (the only runs.tsv row,
  `script:scripts/bar.sh --records 60 --standing`), the verdict is `PASS` whenever the driver is not RED.
  `$over`, the write-p99 and reopen limits from gates/bar.tsv, is consulted only to prove the control
  fires. In full mode the verdict is `UNJUDGED` when load1 ≥ 2. PERF-13 measured that floor itself on hbox:
  "Full mode still judges nothing on hbox. The box's load floor is now above 2".
- **So** the charter's spec (write ≤ 5 s, cold reopen ≤ 60 s) has a comparator that is planted
  (`--harness-control` requires `over` to be non-empty) and a verdict path that is never taken.
- **Severity.** DEFECT. A gate whose red is proved but never consumed: "red as steady state" turned into
  "never judged as steady state".

---

## DEBT

### B1. Three expression-DAG serializers of one fact (law 1); a whole journal subsystem with no consumer
- **The three.**
  - `Census/JournalExpr.lean` (exact structural interchange, `N`/`L`/… inductives) with
    `Census/Journal.lean`'s `expressionEdges`;
  - `Census/CertificateData.lean:24-58` (`encodeExpr`, reprStr rows, ExprStructEq sharing);
  - the Lean string inside `gates/decls.py:63-118` (`go`, hash-consed tokens).
- **They do not agree.** They serialize the same kernel `Expr` for the same purpose (a pinned digest of a
  statement or value), and they disagree on purpose: binder names are kept in the certificate and erased in
  decls (20u (b) records the disagreement).
- **The journal subsystem.** Census/Journal*.lean (465 lines) and gates/journal*.py (≈1,100 lines) landed in
  3070fac "the consolidation's S0 impact and declaration-digest work is the intended consumer". That
  consumer landed as decls.py's own exporter instead. `git grep` finds no runs.tsv row, no pre-push or
  converge step, and no decisions/gates.md entry naming the journal. It is dead code with live-sounding
  names ("finite receipt authorization").
- **Severity.** DEBT, and the largest in the layer.

### B2. decls.py's Lean is `partial def go` (law 4), and no gate can see it
- **Where.** gates/decls.py:91 (READ). GATES-20s removed four `partial def`s from Census/Statements.lean
  because `size.py` counted them against a ceiling of 0. The same construct, in the exporter that judges
  every landing, is a Python string literal. refusals.py and size.py read only `.lean` modules, so this one
  is unseen.
- **Severity.** DEBT (a law applied where the gate looks).

### B3. decisions/ledger.md LEDGER-15 describes a definition the code deleted
- **The entry.** LEDGER-15 (ledger.md:775-819) states `escrow_invokes_one_payout` over `Invokes X obj pkg
  escrow w invs`, with `other` steps that "neither touch nor create obj". Its critique (2) says a nested
  invoke of `obj` "is not a step".
- **The code.** Ledger/Proofs/EscrowInvokes.lean:70-75 (READ) is over `ObjectHistory X obj w w' tr`, plus
  `hpkg`. Its header says the hand-rolled `Invokes` "is deleted" and that nested invokes ARE covered
  (`ObjectStep.nested`). The change is recorded only in decisions/kernel.md:2913 (KERNEL-59, commit 4442b43).
- **Why it matters.** LEDGER-18 later says the theorems "keep their statements", true relative to its own
  date. No ledger.md entry supersedes LEDGER-15. A reader of the ledger's own file gets the old premise and
  the old hole.
- **Severity.** DEBT (a decision the code no longer matches).

### B4. waste.tsv's forced-stale rows: a ceiling where the fact is an equality; measured only at full judges and convergence
- **The rows.** waste.tsv:57-59 pins `bar stale-writes 1 1`, `stale-reruns 1 1`, `stale-after-sync 0 0`.
  waste.py holds them as CEILINGS (`seen > ceil`, waste.py:50). A run whose forced contention did not
  happen (0/0/0) is green to waste.py.
- **What actually holds the fact.** bar.sh:576-583 requires exactly (1, 1, 0). That is two statements of one
  fact, and the waste one cannot fail in the direction that matters. Lowering stale-writes' ceiling to 0, a
  legal ratchet move, would contradict bar.sh's exact 1.
- **When it is measured.** The bar row runs at a full landing (script rows are always selected,
  runs.py:286-294) and at convergence. A FAST landing never measures it (D4). waste.py's non-`--measured`
  mode compares the table's own hand-typed `measured` column to its ceiling (waste.py:66-68), which is two
  numbers in one file, not a measurement.
- **Severity.** DEBT.

### B5. Decision prose that overclaims what the gates run or catch
- **The claims.**
  - GATES-20s, 20u and PERF-13 (d): "every judge" (D4).
  - GATES-20t (3): check 2 "is what catches a reverted definition body". Only a stale one; forward edits
    are D1.
  - The statement census header (Statements.lean:14): "The rule reads structure, never a name" (D3's
    `Function.Injective` is a name the walk will not open).
  - size.py:135's metric is named "partial defs (deployed)" and counts every module, proofs and tooling
    included (stricter than the name, but the name lies).
- **Severity.** DEBT.

### B6. `grant_moves_le_cap`: the name says cap, the object is `left`, and only transfers that name `g`
- **The object.** Ledger/Proofs/GrantCap.lean:256-264 (READ). The bound is `left`, which `ledgerLeft
  transferBase g cell` reads at the START World `w`. That is the cap only for an untouched grant. LEDGER-19
  (3) and the docstring say so; the theorem's name does not.
- **What is counted.** Only transfers whose `via = some g` (`MovesThrough`). Value moved under g's
  authority through a child grant carved from g (`checkParent`'s `spendAt`, Kernel/Receive/Derive.lean:301)
  is not counted. It is bounded only by composing each child's own theorem, and that composition is not
  stated (LEDGER-19 critique (1) says carves "only tighten the bound", which is true of g's sum, not of
  g's delegation tree).
- **"At most one per step" is sound.** It is backed by `effectsPinned`'s `duplicateEffect`
  (Kernel/Receive/Call.lean:483-488, READ): two spends of `g` in one turn would be two effects on one cell.
  That backing is not mentioned in GrantCap or LEDGER-19.
- **Severity.** DEBT (a name stronger than the statement) plus the QUESTION in L1.

---

## QUESTIONS

### L1. What the cap bounds over a delegation tree
- **Asking.** Should "a grant moves at most its cap" mean transfers through `g` (as now), or everything
  rooted at `g`?
- **What decides it.** A theorem `Σ (transfers via any descendant of g) ≤ left g`. It needs a read-back of
  `checkParent`'s carve; KERNEL-30 offered one (LEDGER-19 (1)).
- **The mutation that tells the difference.** A grant g with 10 left carves a child g' of 10, then g'
  transfers 10. The current theorem counts 0 for g (true) and 10 for g' (true), and nothing states the
  10 + 0 ≤ 10 composition.

### L2. LEDGER-15's "at most one payout": over which history
- **Today's history** (READ, EscrowInvokes.lean:65-75): any `ObjectHistory X obj w w' tr`.
  - It starts at an arbitrary World `w`, not at the object's birth.
  - Every judged step must read its package as `escrow` (`hpkg`).
  - `payoutCalls` counts the run's RETURNED grantless transfers (EscrowSpec.lean:81-87), not what
    committed.
- **The suffix bound is sound.** Settled is absorbing (`escrow_absorbing`, `escrow_judge_settled`), so a
  suffix starting after a payout pays 0. A whole-life bound follows by composition, and it is not stated.
- **Still open.** Whether a history in which the escrow's law is CHANGED to a non-escrow package can occur
  is excluded by `hpkg`, not proved impossible. `escrow_frozen` refuses `relaw` through the law, and KERNEL
  refuses it for programmed objects (the Escrow.lean:32 comment).
- **What decides it.** A theorem from `create … escrow` through every audited log, with no `hpkg` premise,
  where `hpkg` is derived from the ROM package cell plus the frozen law.

### Q3. `PRE-EXISTING` in full landings
- **The mechanism.** A row red on the parent passes its candidate as PRE-EXISTING (scripts/pre-push:260-300).
  The keys are `run EXE ARGS` plus each `    red <line>` line (pre-push:248-249), so a new red LINE in an
  already-red row is new. That is right for rows whose red lines name the failure.
- **The doubt.** certificate.py prints one red line holding every section (`certificate-pin: RED a | b`,
  certificate.py:65). A second, unrelated difference changes that line, so it is new: fine. But a change
  that REPLACES one difference with another of the same text would hide. I could not construct one.
- **What decides it.** Run a full judge on a parent red in `axioms` with a candidate that adds a
  `vocabulary` difference, and read the keys.

### Q4. census.py executes the CANDIDATE's own census code
- **Where.** scripts/pre-push:385 runs `python3 "$G/tree/gates/census.py"` from the candidate tree, against
  the candidate's Census/*.lean. GATES-20 ("the judge's code is main's, the candidate supplies only its
  table") is applied to runs.py and decls.py ($J), not to the census.
- **Partial defence.** A change to gates/census.py forces FULL mode, and the parent's check.py runs too. But
  the census itself is not run by main's copy.
- **What decides it.** Is the census a judge, so it runs main's copy, or data? The current split makes a
  weakened Census/Statements.lean judge itself at convergence, where only its own fixtures and the plant row
  stand against it.

---

## What I checked and found sound (so it is not re-read)

- **census.py's verdict.** It requires returncode 0 AND each of `AXIOM-CENSUS ok`, `REFINE-CENSUS ok` and
  `STATEMENT-CENSUS ok` (census.py:42). The wrapper does not answer for the work. Exe root modules are
  excluded from the census, and closure C7 (closure.py:16, 89) holds them to `main` only.
- **The statement census's fixtures.** They are judged before the tree, and a misread fixture is an
  error (Statements.lean:169-177). The plant's `--harness-control` reds on the same `RED (n)` comparison
  as the real run (statement_plants.py:204-207). The mutant compiles a scratch Statements with the
  two-sides test disabled, and the fixtures refuse it. The LEAN_PATH `:` hazard is refused by name.
- **certificate_plants.** These are plants of the REAL GrantCap.lean:
  - every site count is asserted (`site moved`);
  - C0 equals the real pin;
  - P2's probe proves the mutation happened;
  - each section's mutant (M-supports, M-vocabulary) escapes;
  - the control requires P2 RED, which nothing meets.
- **decls_plants --synthetic.** It runs decls.py's real `judge`, with only the Lean export replaced. It
  does NOT exercise the exporter (`#decl_export`, `go`): an exporter that serialized every statement alike
  would leave the synthetic row GREEN. The historical plants (H1–H4, R1–R3, C0) do exercise it, but they
  are run by hand (decls_plants.py:9-11) and are not a runs.tsv row. Recorded here as a gap of the standing
  plant rather than a separate finding.
- **runs.py's verdict.** It needs `rc == 0` and the exact last line (runs.py:314-324), and a control must
  read RED and contain `harness-control` (runs.py:594-604).
- **The axiom census's allow rows.** A row that matches nothing is red (Axioms.lean:80-82). tcb.py ties each
  native_decide allow row to a `native_decide:` tcb row at the toolchain pin.
- **Ledger, no defect found:**
  - `grant_moves_le_cap` is about the deployed `audit` (Kernel/Receive/Audit.lean:68), not a proof-side
    twin;
  - `move_weight`'s premise is the audited call itself;
  - `GrantCapTooth` refutes the bound exactly at `¬ LedgerContiguous`, through the real `receive` and
    `World.admit` (decide +kernel);
  - the escrow's law, methods and docstring agree (Escrow.lean:17-36 against :113-130, `escrow_verdicts`).

## Files not read whole (sizes in lines)

- **Read in part.**
  - Ledger: Ledger/Proofs/EscrowRun.lean 630 (header + declaration list), Ledger/Proofs/Escrow.lean 388
    (statements, not every proof), Ledger/Proofs/GrantCapTooth.lean 169 (header + statement).
  - gates: gates/runs.py 1070 (verdict, control, selection), gates/rebase.py 680 (header + function list),
    gates/size.py 303 (first 140), gates/converge.py 399 (header), gates/check.py 126 (the results table).
  - scripts: scripts/bar.sh 657 (header + verdict half), scripts/pre-push 428 (most), scripts/converge 135
    (header).
  - Census/Journal.lean 204 and Census/JournalExpr.lean 136 (heads).
  - decisions/gates.md 1046, ledger.md 1003 and perf.md 873: the entries cited above only.
- **Not read.**
  - Ledger: Ledger/Proofs/EscrowWitness.lean 265, Ledger/Proofs/EscrowAdmitted.lean 398,
    Ledger/Sim/Journey.lean 344 (plants grepped), Ledger/Sim/Main.lean 3.
  - Census: Census/JournalRun.lean 125.
  - gates: readset.py 656, journal_pilot.py 460, journal.py 283, tree.py 297, land.py 204,
    journal_finish.py 150, journal_coverage_plants.py 127, closure.py 112 (C7 grepped), size_limit.py 105,
    size_limit_plants.py 82, owners.py 65 (rule grepped), journal_plants.py 54, vectors.py 53,
    journal_compose.py 50; the tables decls-plants.tsv 227, codec-vectors.tsv 264, runs.tsv 59 (read);
    ceilings.tsv, bar.tsv, size-allow.tsv.
  - scripts: scripts/commit 313 (mode selection grepped).

## Scratch artifacts (this session only)
- `/private/tmp/claude-501/-Users-ember-dev-breadstuffs/01a167c9-1142-7bc2-a1e6-b2cf23dfde66/scratchpad/sc/`
  holds the Statements copy, `P/T.lean` with the six theorems, `Run.lean` and `out.tsv` (D3).
- `/private/tmp/claude-501/-Users-ember-dev-breadstuffs/01a167c9-1142-7bc2-a1e6-b2cf23dfde66/scratchpad/dp/`
  holds the two decls judge cases (D1, D2).
