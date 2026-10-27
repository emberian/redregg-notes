## PROTOCOL-46 · PROPOSED · a settlement is the member's word, never the Host's: the attempt store settles a call only from a receipt its own follow built and checked; `absent` is final only once the call is dead (2026-10-18, PROTOCOL-10; cv 01a14dfa-1ffb, cv 01a14ade-0f69, PROTOCOL-45 alternative (b))

**The defect today (read, not assumed).**
- client/src/run.rs `settlement` classifies the Host's reply by its status byte alone. attempt.rs then writes `committed` / `not-committed` holding the Host's reply verbatim.
- `reconcile` hands that classification to custody (`custody.settle(committed)`). So a Host that says `ok` to the lookup of an unlanded rotation advances custody to a key the World never installed. A Host that says `refused` for a committed rotation keeps custody on a revoked key. Either way the member is locked out on the Host's word.
- `Attempt.next`'s terminal `absent` says "nothing committed; running the command again is safe". That is false while the call's window is live. The Host (any relay) holds the signed bytes and can submit them up to `validUntil`. A member that re-runs the command signs a NEW call, so both can commit: a double effect.
  - This needs no hostile Host. An honest relay that queued the bytes is enough.

**Decision (proposed).**
1. **Follow settles; the Host hints.** The Host's `submit` / `lookup` status still drives the LOOP (when to look up, when to resend the same bytes). It never ends an attempt as final. Every action that would end the attempt (committed, refused, absent) becomes `confirm`: nd asks follow `receipt CALL`.
   - The verb takes the CALL bytes instead of a TXID (still 19 verbs). It needs `notBefore` and `validUntil`, and the txId is derived from the call.
   - Follow catches up, builds the receipt from its own World (`Receipt.build`), and checks it against its own head (`Receipt.check E w.height (w.roots E) …`).
   - It prints `receipt HEX`, `head STEPS HEIGHT ROOTS` and one `settle NAME` line, decided by a new total function `Settle.ofReceipt (answer) (height) (validUntil)`:
     - `committed H TD`: final;
     - `refused CODE`: recorded; final (`submit_refused_never`);
     - `expired`: `absent` at a head whose height ≥ `validUntil`; final (`absent_final`; the window is the kernel's);
     - `open`: `absent` while the window is live. NOT final: the bytes may still land. The run ends with the attempt open, like `declined`;
     - `uncertain forgotten`: past `journalForgets`.
2. **The settlement file holds the receipt and the head it checked against**, never the Host's reply. It can be re-checked later and quoted (the phone's read).
3. **Custody settles only on a confirmed settlement.** `reconcile` passes `committed` / `not-committed` from the `settle` line. Anything else leaves the rotation armed.
4. **A contradiction is named.** If the Host said `ok` / `refused` and follow says otherwise, the run prints `hostContradicted HOSTSAID FOLLOWSAID` on stderr, the attempt stays open, and exit is `uncertain`. The client never picks a side; the member's fold wins by construction.
5. **`Attempt.table`**: Action gains `confirm`, and the terminal `absent` is deleted. "Sends exhausted, still absent" ends `open`. Flag day: the emitted table re-emits, and CLIENT re-implements from it as before.

**HOST half: none.** The lookup reply is unchanged. The cv's "Host's lookup answers carry a receipt" is DECLINED, argued:
- A Host-built receipt is at the writer's head: its exact step count, mid-batch.
- The member can check it only against a head it holds at THAT step count, so it must page to exactly there.
- Once it has paged there, it holds the World, and its own `Receipt.build` answers. The Host's receipt adds bytes and nothing the member does not already compute. A Host that withholds pages leaves the member at an older head either way, where `absent` is `open` (never final) under rule 1.

Trigger to revisit: a member that holds a head but NOT a World (the phone, cv 01a14d95-36b0). For that member the lookup reply carries the receipt plus the head record. That needs a chain-anchored receipt, which needs KERNEL's last head link (cv 01a14dfa-200a).

**CLIENT half (the need).**
- attempt.rs performs `confirm` by `follow.command(["receipt", CALLHEX])`, writes the settlement from the `settle` line plus the receipt and head bytes, and adds no classification of its own (the line's name comes from the generated table).
- run.rs `reconcile` settles custody from it.
- Tests with a lying Host stub, each mutation red:
  - `ok` for an absent call: open, `hostContradicted`;
  - `refused` for a committed call: committed;
  - `absent` with sends exhausted and a live window: open, not "safe to run again".

**PROTOCOL half (mine).**
- `Protocol/Settle.lean` `ofReceipt` and Attempt `confirm`; the verb re-cut; the Machine arm.
- Theorems:
  - `check_build`: completeness. On a canonical World, `check E w.height (w.roots E) tx nb (build E w tx) = .ok answer` unless forgotten. Needs KERNEL's refusals twin of `journal_prove_verifies` / `journal_prove_absent`.
  - `settle_committed`: `committed` → the World's journal holds the entry, or a collision (via `check_committed`).
  - `settle_final_never_admits`: `refused` or `expired` → no later World admits the call (`submit_refused_never`, `absent_final`).
  - `settle_open_not_final`: a witness World where an `open` call is later admitted. This is the theorem that makes deleting the old terminal `absent` mandatory, not taste.
- Row `settle` (27th) on the Loopback with a `lieLookup` Host fault:
  - a committed call whose lookup the Host answers `absent` / `refused` settles `committed`;
  - a live absent call with sends exhausted stays `open`, and after the `window` act settles `expired`.
  - Plant `trustLookup` (the store takes the status byte) is caught at the line reading the lie.

**What it costs / what breaks.**
- Every final settlement costs one follow catch-up.
- An absent call is final only after its window, at most `windowMax` heights. Before that the member sees `open`, which is the truth.
- `receipt TXID` → `receipt CALL` (the phone row re-cuts).
- The attempt table and generated.rs re-emit.
- The settlement file format changes. Old attempt dirs refuse to load: no attempt dirs exist outside tests.

**Alternatives.**
- (a) Host receipt in lookup: declined above.
- (b) Keep the terminal `absent` with a "may still land" hint: a no-op kept for comfort. Refused by doctrine.
- (c) A cancel call that burns the txId early: the kernel has no such step. A member that cannot wait a window could ask KERNEL for it. Recorded, not proposed.

**Asks.**
- KERNEL: refusals prove/verify completeness and soundness (the twins of `journal_prove_verifies`, `journal_prove_absent`, `journal_inclusion_sound`, `journal_exclusion_sound`), sent to KERNEL as item (5).
- CLIENT: the half above (CLIENT is not live: ROOT staffs).
