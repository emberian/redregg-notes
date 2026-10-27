# SPEC-DOCS — the README for a verification researcher, the Objective Bend specification, and two references (real 2026-10-27)

Brief: Ember (real 2026-10-27), "update the README … target audience Max von Hippel … docs that have specs and technical references too … maintain the writing quality of e.g. the WebAssembly specification."
Tree restated: nanodregg `main` `276ded8` (one later commit, `48232e7b`, touched only the offer library, which the documents do not describe).

## Landings

| hash | contents |
|---|---|
| `e63da167` | README retargeted at a verification researcher: what Objective Bend is, why its meaning is contextual and its surface extensible; one complete program (law, three methods, a hole with a cell-supported candidate, a generator) in core text, read section by section; the Spec claims one sentence each; reading map. `Lang/Journey/Readme.lean` runs the README's literal text through `Receive.submit`/`Lang.program` (rows RM1–RM14, lang-journey GREEN on hbox after rebase). `docs/OBJECTS.md`: stale Claims and Effects rows corrected. |
| `3bd3cbd1` | `docs/spec/` README (ToC), 0 Conventions, 1 Introduction, 2 Structure |
| `c17d2561` | 3 Validation: HasType rule by rule, the checker theorem, type-error table, install check, holes, claims |
| `b0737858` | 4 Execution: machine rules, tick cost, runs/extraction, install/load, method run, calls/grades/edits/held value, laws per act, nested calls and pool, guards, contextual semantics (selection steps, resolution, demand, repair), refusal texts |
| `74341946` | 5 Binary format (tree codec, tags, data, package v10, worked vectors, version history), 6 Appendix (theorems, not-proved, bounds, rule and refusal indexes) |
| `992ec055` | `docs/reference/kernel.md`, `docs/reference/protocol.md` (written by two subagents to my brief, name-checked by grep, findings sections moved here); README reading map starts with the spec; MEMBER `revoke`→`retire`; OVERVIEW duplicate sentence |


## What could not be stated because the tree does not decide it (findings)

### Language (mine)

1. The authoring surface `Lang/Surface.lean` has no syntax for holes; a contextual package can be written only in core text, so the README's program is core text with seven type names abbreviated on the page (the journey holds the literal). `Lang.Read.grammar` omits the `(effects …)`, `(claims …)` and `(holes …)` sections and the hole term; `Lang.Surface.grammar` omits `(claim keeps INV LAW)` and the `install`/`createOf` call kinds. A `lang:` landing adding `(hole …)` declarations to the surface would let the README show one surface text.
2. `ob (check P)` cannot check a contextual package: it runs `Package.checkWith`, which refuses `illTyped noHole …` (the closed type check runs before `contextualSignature`). No tool outside a World runs the contextual install check; I verified the README program with a scratch Lean file and the journey.
3. `Lang/Claim.lean` module docstring is stale: it says `Package` carries no claims field and install does not call the checker (contradicted by LANG-93, `276ded8`).
4. Laws and guards do not draw on the call's tick pool or the member's meter: each runs under its own `lawTicks` = 100000. Judging work per call is bounded (laws × guards × lawTicks) but unmetered. The spec states this as fact (§4.8.3); whether it is intended is not recorded in a decision I found.
5. An unpinned ROM row support is refused `holeDerivationMoved` (the "moved" name), not an unpinned refusal: a client cannot tell "not pinned" from "moved" for row supports by name; the coordinate is given.
6. A selection refusal lists only the failing step's coordinates; the `selectHole` docstring's "learns its whole missing read set in one refusal" overstates (CRIT-CTX said the same). Stated in §4.10.2 and §6.1.
7. No top claim covers the contextual layer at history level (DESIGN-CTX §2.4): stated as in flight in README, §1.6, §4.10.6, §6.1.
8. Only methods edit rows, so a hole's selection row needs a package method to write it; the README program has a `choose` method for that reason.

### Kernel (from the kernel reference's author)


1. `Kernel/World.lean` `chainNext`: the docstring says `rd` is the roots digest of the cells', journal's and refusals' roots; `rootsOf` digests four roots, the rows' included.
2. `Kernel/World.lean` `World.refusals`: the field's docstring names refused ids and per-member counts; the trie also holds the World's totals (KERNEL-55) and the meter (KERNEL-68).
3. `Kernel/World.lean` `refusalCount`, `refusalTotal`: the docstrings say "in the window of height `H`"; neither takes `H`, both read `w.height`.
4. `Kernel/Turn.lean` header and `Kernel/World.lean` `bornId`: they say a born id is a content id, a keyed account id, or derived from `txId` and the index; a member's id is `memberId`, the digest of its join consent.
5. `Kernel/Receive/Call.lean` `Body.retire`: the docstring cites `World.credit`; the definition is `Nanodregg.Kernel.credit`.
6. `Kernel/Receive/Call.lean` `Refusal.lawDenied`: the docstring says the law "refused the write"; it is raised for every occasion.
7. `Kernel/Receive/Call.lean` `Right.observe`: the docstring says "read the cell"; no receiver reads `observe`, and the kernel uses it only on the World target (`mayFollow`).
8. `overBound event` names two bounds: `Bounds.eventBytesMax` and, for a cancel signature, `Bounds.cancelBytesMax` (`checkRefusedBounds`); `Bound` has no constructor for the second.
9. `missingCell`, `rangeTooLong` and `duplicateRow` are names in both tables, so `Verdict.name` gives one string for two verdicts; only the code distinguishes them.
10. A root grant on a cell the issuer does not own is admitted; it confers nothing (`ownerAuthority` compares the root issuer with the owner). `account asset owner` does not check that `asset` names a well. The tree decides both; neither is stated as intended in a decision entry I found.
11. `decisions/kernel.md` KERNEL-54 AS BUILT names a receive refusal `staleRecorded` and a function `auditRefusal`; neither exists in the tree.
12. `decisions/kernel.md` KERNEL-66 cites `Kernel/Proofs/Audit.lean`; the file does not exist; the theorems it names are in `Kernel/Proofs/Rederive.lean` and `Kernel/Proofs/StaleOnly.lean`.
13. `decisions/kernel.md` has two entries headed KERNEL-76 and none headed KERNEL-72 or KERNEL-74.
14. `docs/MEMBER.md` lists a verb `revoke`; `Protocol/Command/Verb.lean` has `retire` (KERNEL-70).
15. `docs/OVERVIEW.md` states "The operator can read every byte in a World." twice in one paragraph.
16. `Sim.nameOf` is `Gen.nameOf`, the constructor name taken from `Repr`; the wire names are `Refusal.name` and `Reject.name`.

### Protocol (from the protocol reference's author)


Each finding is a fact read at `276ded8`.
None was run.

**F1. Two client decisions are Rust's.**
Which open attempt an argv resumes, and whether a resumed attempt that ends `refused` is planned again, are decided in `client/src/run.rs` `run` (CLIENT-37), not in the Lean.
`docs/MEMBER.md` says "nd decides nothing".
At-most-once per intent is not a claim of `Spec` (`Spec/README.md`, C(v)).

**F2. The operation table's receivers are not the declarations the writer runs.**
`Op.receiver` names `Nanodregg.Kernel.World.lookup` for `lookup`; no declaration of that name exists.
It names `Receive.receive` for `submit`; the writer decides with `Receive.judge` (`Host/Serve.lean` `handle`).
It names `Host.Page.build` for `log`; the deployed writer pages with `Host.Page.kept` (`Host/Deployed.lean` `pager`).
The table's header says a gate resolves each name; no Lean declaration other than `Op.receiver_injective` reads `Op.receiver`.

**F3. `Consent.signShapes` covers `step`, not `start`.**
`start` offers custody `whoami` and the first envelope of every catch-up.
The envelope is one of the six shapes; `whoami` is not.
`Protocol/Proofs/Domains.lean` lists seven member shapes.
`Spec/README.md` names the join shape "a possession proof"; `Spec/Proofs/Sign.lean` and PROTOCOL-79 name it a join consent.

**F4. `Spec/Proofs/Fork.lean`'s header says "SUNDR's fork consistency at the deployed act".**
PROTOCOL-82 and `Spec/README.md` state that no claim is SUNDR's fork consistency.
PROTOCOL-82 decision 6 renames the claim; the rename is not on `main`.

**F5. Three comparison paths have no claim.**
`ForkConsistent.sync` covers `sync --to` and not `sync --check`.
No claim covers `forkedCertified`, on a page or behind follow's position.
No claim covers `behindOr`'s comparison of posts at or behind follow's position; `System` has no field for it.

**F6. `cancel CALL` can exceed `Bounds.stepsPerCommandMax`.**
`Bounds.pages_fit_steps` budgets one catch-up: `2 · 28 + 5 ≤ 64`.
`cancel` runs two catch-ups, and `cancelCatchUp` starts the second with a page count of 0.
A cancel whose two catch-ups each read many pages can take more than 64 steps; the client then ends `StepsExhausted` after the cancel was sent.
The table's docstring for `Bounds.pagesPerCommandMax` says "at most four other steps"; the theorem budgets five.

**F7. A page is absorbed onto follow's current World, not the World it was asked for.**
`host follow` interleaves frames of several commands over one World (`Host/Follow.lean` `loop`).
A command asks for a page from the step count its continuation recorded (`start` in `acc`), and absorbs it onto follow's World at the time of the reply (C-Page).
`step` does not compare the two.
When another command moved follow's World between, the events re-derive on a World that already holds them, and the command ends `eventMismatch`, `replayed`, `refusedFinal` or `chainMismatch`: names that say the writer's log is wrong.
I did not check whether a row exercises interleaved commands.

**F8. `sync` does not print the step count that `sync --to` takes.**
`parse`'s comment says `STEPS:CHAIN` is "a step count and the chain's hex, as `sync` prints them".
`syncLines` prints `height`, `chain` and `roots`.
The step count is printed by the `head` line of `receipt CALL` and `receipt --health`.

**F9. Docstrings that disagree with the code.**
* `CommandExit.behind`: "printed `behind HEIGHT TIP`"; `behind` prints two step counts.
* `custodyPhase`: lists phases 1, 2 (`init`), 3, 5, 6, 8; the code also counts 9 and 11.
* `Protocol/Command/Machine.lean` header: "`init` needs no World"; `init` signs a join to follow's World's origin (PROTOCOL-79).
* `Protocol/Command/Machine.lean` header cites `resume_rederives`; no declaration of that name exists.
* `Protocol/Head.lean`, the "Certified heads" section: "No deployed path PRODUCES a certificate yet … and none consumes one yet"; `adopt` consumes one (`certifiesWorld`), every `log` page carries one (`pageCertified`), and `host serve --certify` produces one.
* `Kernel/Receive/Follow.lean` `Authority.none`: "a certificate under it is `unlisted` whoever signs it"; `certified` refuses `noAuthority` before it reads a signer (PROTOCOL-77.1).
* `Verb.receipt`: "`head STEPS HEIGHT ROOTS`"; the printed line ends with the chain.
* `Verb.adopt` and `docs/MEMBER.md` cite `Invite.accept`; `adopt` uses `Invite.acceptStart`, which also takes a carried start.
* `Host/Follow.lean` header: `wrongSocket` for "submit, lookup, read, log"; `cancel` is refused the same way.

**F10. Stale statements in `docs/`.**
* `docs/OVERVIEW.md` states "The operator can read every byte in a World." twice in succession.
* `docs/MEMBER.md`: "A resumed plan is re-derived; changed signed bytes are planMoved."
  A resumed attempt resumes at phase 4 with its frozen call and is not planned again (§3.18); `planMoved` arises at phase 3 within one run (P-Submit).
* `docs/MEMBER.md`: "nd decides nothing" (F1).

**F11. What the tree does not decide.**
* Which head a party without a World should trust for a foreign receipt: `HeadOf` is a premise with no discharge (§7.3).
* A validity source for a certified head: a certificate gives attribution, not validity (§5.3); `Spec/README.md` lists §9's validity source as owed.
* Comparison at unequal positions: a post past the page's end, a position below the Store's oldest kept file, and a position below a thin member's base are compared by nobody (§6.3).
* Health receipts have no `Spec` claim (§7.2).

Housekeeping: the protocol agent left `/tmp/claude-501/toks.txt` (outside the scratchpad; not deleted, per the disk rule). My hbox worktree `~/nd-land/spec-docs` (1.5G, its own copied `.lake`) and `~/nd-land/spec-docs-scratch` remain; the worktree is registered on the `/tank/dregg-build/nanodregg/main` repo.


LANG-SURFACE (2026-10-27): findings Language 1 and 2 are fixed by `57111733` (LANG-104, LANG-105). The surface text has holes. The README's program is now surface text, which the journey reads from README.md (RM0–RM16). `ob (check P)` runs the contextual install check, and `(check P (view …))` resolves holes on a stated view. `Read.grammar` gained the sections and the hole term. Still open: `(createOf T)` in the surface (finding 1's second half). Report: `LANG-SURFACE.report.md`.
