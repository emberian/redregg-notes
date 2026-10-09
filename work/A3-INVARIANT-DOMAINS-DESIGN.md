# A3: registered, authoritative INVARIANT DOMAINS (GPT-6 row A). Design

Author: DEPUTY-OB-ENG, 2026-10-07. Status: design, not built. Base: `next` with upgrade-turns, object-pin and row-a1.

## The problem

A per-frame law (the object's `effectiveLaw`, judged at each frame's return on that object's own
old/new state) cannot state a RELATIONAL invariant across objects. Examples: "the bank's reserve equals
the sum of its account objects' balances", "the two halves of a trade move together", "at most N live
tickets across these venues". Today the only cross-object guarantee is call atomicity (all or nothing).
GPT-6 asks for invariant domains that are registered and authoritative, checked in conjunction with the
per-frame laws, over bounded authenticated data, with no discovery calls.

## Shape

    structure Domain where
      id      : Digest                  -- a kernel cell (role `domain`, protected coordinate)
      members : List ObjectId           -- bounded: length ≤ config.domainCap; distinct
      law     : Pred                    -- over the JOINT view below; first-party fragment only
                                        -- (no witnessed/hashEq/ran: Pred.Sat-decidable, like upgrade floors)
      upgrade : UpgradePolicy           -- frozen | governed, as ObjectRecord (may only tighten)

- **Joint view.** For each member `i`, its declared-state slots are renamed `member/<i>/state/...`. The
  turn's request slots are added once. Old view = pre-turn states, new view = post-turn states. The view
  is built from member records and state cells the turn READ-GUARDS: authenticated, bounded by
  `|members|`. Nothing is discovered, because the member list is in the domain cell and the turn names
  the domain.
- **Membership is recorded on the member.** ObjectRecord gains `domains : List Digest` (bounded). A turn
  that writes an object's declared state must guard every domain in that list. The receiver then
  re-judges each such domain's law once, at the END of the turn: after the whole call tree, on the final
  post-state. The turn is admitted only if every per-frame law held at its frame (today's rule) AND every
  touched domain's law holds on (pre, post). Otherwise the whole turn refuses by name,
  `domainLawDenied (domain) (leaf)`, which is atomic co-failure like any call.
- **Why turn end and not per frame:** a relational invariant is legitimately broken between two frames
  of one atomic transfer. Per-frame laws keep judging each object's own writes, so a domain can only ADD
  refusals; it never admits what a frame law refused.
- **Registration (`registerDomain` turn):** it needs the consent of EVERY member: each member's upgrade
  authority must permit it, since joining a domain adds a constraint to an object, which is exactly a
  law-tightening and so is under the object's governance. The law must hold on the members' current
  states at registration. Members gain the domain id in `domains`. Leaving or changing a domain is a
  governed domain upgrade that may only tighten, plus each member's consent to leave.
- **Cost:** a turn touching a domain pays `|members|` guarded reads and one Pred evaluation per touched
  domain, through `Config.covers` and the tariff (the same accounting path as row C3). `domainCap` and
  `|domains per object|` bound the work.

## Theorems (on the admitting functions)

1. `domain_law_enforced`: an admitted turn that writes any member's state yields a post-state on which
   every domain of every written member satisfies its law.
2. `domain_holds_forever`: over CheckpointInvariant.Reachable, from a genesis with no domains, every
   registered domain's law holds on every reachable world. It is an induction like `live_counts`, and
   every AdmittedTurn constructor must be classified (a writes-member-state arm guards and judges; the
   others leave member states unchanged), with no wildcard.
3. `domain_conjunction`: the turn's admission equals per-frame admission ∧ domain judgement, so domains
   never widen.
4. Tooth: the DAO bank with domain law `bank.reserve = Σ accounts.balance`. A planted call tree that moves
   balance without moving the reserve is refused `domainLawDenied`, while the same tree with domains
   ignored commits (log both). Second pole: an honest transfer commits.

## Breaks / re-emits

ObjectRecord gains `domains` (OBJECT-RECORD v3), a new cell role `domain`, a new turn `registerDomain`
(activity COMMAND bump), a new receiver refusal, Host JSON for both, and journey rows for the bank case.
Every world with objects re-genesises.

## Not in scope

Discovery of domains by content, unbounded membership, and domain laws over non-member cells.

## As built (range 1, row-a3 = b57ef817..113bd02c, approved by DEPUTY-OB-ENG 2026-10-07)

- **A domain law is a STATE predicate** (`ObjectiveDomain.judgeJoint`): it is judged on the members' joint
  state alone, as both the old and the new view, with no request slots (`member/<i>/state/...` only).
  Reason: a domain is an invariant of its members' states. A law that read `request/height` (which moves
  with no turn) or compared old and new could hold at registration and fail later with no turn at all, so
  "holds forever" would be false by construction. Transition rules stay the members' own laws.
- Judged at turn END (`ActivitySeatEnd.finish` = seat join, then `judgeDomains`) on the FINAL posts, for every
  object whose state the posts write; ALL members' final states are read (unwritten ones guarded).
- Domain cell: protected activity-cell role `domain` (tag 6), content-addressed id (members, law).
  Membership index: `ObjectRecord.domains` (OBJECT-RECORD v4). Membership is permanent in range 1.
- The native route re-decides a turn at submit, so a stale plan is re-judged on the new member states;
  the read guards (`finalIntent_guards`, `finish_domains`) are what protect a truly concurrent commit.

## Implemented decisions (ROW-A3, 2026-10-07; approved by DEPUTY-OB-ENG)

1. **A domain law is a STATE predicate.** It is judged on the members' joint state alone
   (member i's slots under `member/<i>/`), as both the old and the new view, with no request
   slots. Reason: it states an invariant of the members' states. A law that read the height
   (which moves with no turn) or compared old with new could hold at registration and fail with
   no turn at all, so it could not be an invariant (`judgeJoint`).
2. **Stale plans vs concurrent commits.** The native Host re-decides at submit, so a stale plan
   is re-judged on the members' new states (journey D3). Read guards on the domain cell and every
   member's state cell protect a truly concurrent commit (`finalIntent_guards`, `finish_domains`;
   Lean tooth `invoke-drops-guards`).
3. **One choke point, no per-turn list.** `ActivitySeatEnd.finish` (every `Step.turn` carries its
   output) ends with `judgeDomains`, which admits only posts that (1) keep every domain of every
   object record they rewrite (`domainsDropped`), (2) leave satisfied every domain of every object
   whose state a post writes OR whose state a posted cell holds (a retired or blanked state counts
   as a write), and every domain whose cell a post touches, and (3) leave every touched domain
   cell named by each member's final record (`domainUnindexed`). `domain_holds_forever`
   (Kernel/ObjectiveDomainInvariant) therefore holds for every AdmittedTurn constructor, present
   and future; inert seat posts and ordinary-gate intents cannot write the protected cells.
4. **The sum atom** `Pred.sumEq left right` (Σ new[left] = Σ new[right], all present). It is
   outside the floor-decision fragment, `dial = .ordering` (`sumEq_not_merge_closed`), and
   refused by the circuit compiler under every profile (`lower_sumEq_refuses`; lowering is cv task
   01a11633-cf8e). G1b's `law` fragment does not expose it.
5. Membership is permanent in this row: a frozen object cannot join. Leave/change is cv task
   01a115c9-d990 and pricing is 01a115c9-d9b7; caps are 16 members and 8 domains per object.

## Pricing the domain judgment (cv 01a115c9-d9b7) — design (ROW-A3, 2026-10-07)

Facts (mapped): a turn's fee is `config.tariff.workOf envelope`, fixed from the DECLARED envelope before the
turn runs, never refunded; `finish`/`finalize` see neither envelope nor payer; nothing prices reads or guards;
`registerDomain` and `create` post no Book batch.

Design:
1. `Capacity.domainWork : Nat` — declared units of domain judgment; `Tariff.domainWork` rate (tariff v3);
   `workOf` adds `t.domainWork * c.domainWork`. Because envelopes already flow through every escrow (birth's
   resume/timeout, invoke postage -> deliverMessage, adopt's envelope -> migrate), every turn that can trigger
   the judgment already pays for its declared domain units through the existing fee path.
2. Units of work: judging a domain = |members| guarded state reads + 1 law evaluation; indexing a touched domain
   cell = |members| record reads. `judgeDomains` returns its units with its guards.
3. `AdmittedTurn.domainAllowance` (every constructor, no wildcard) = the domainWork of the envelope the turn is
   charged for (invoke/birth/rebirth/adopt: request envelope; deliver/exhaust/abortDrained: the turn's envelope
   = escrow + extra; deliverMessage: the message envelope (paid as postage); migrate: the adopt's envelope when
   it is charged, else 0; registerDomain: its new `envelope` (charged, see 4); others: 0).
4. `registerDomain` gains `envelope : Capacity` and a Book fee batch (payer account + capability) — COMMAND v10.
5. `finish` refuses `domainUncovered work allowance` when the judgment's units exceed the allowance, before any
   post is committed.
6. Theorems: finish ok -> units <= allowance (`finish_domain_covered`); `workOf_domainWork`:
   rate * allowance <= workOf envelope; with the existing charge theorems, the payer was charged for every unit.
7. Tooth: a planted Host where the judgment reports 0 units commits a turn whose envelope declares 0 domainWork;
   the honest Host refuses it `domainUncovered` (journey row D6).
