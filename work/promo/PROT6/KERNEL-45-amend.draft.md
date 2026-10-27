
### KERNEL-45 item 3 FIRED as two runs of one term (LANG-75.11, PROT-6, 2026-10-23; CX-PROMO-6; RELEASE R-0050 under grant R-0049). Decision text; kernel lines changed: 0

Item 3's trigger fired. The trigger was "the first row whose invariant spans two objects changed in one turn", and that row is Std.offer's fuse: two offer rows, under two objects, consumed in one Turn (`Lang/StdOffer.lean`). It fired at the price item 3 named, "a separate judge (as LANG-44's row guards are)", in this shape:
- A matcher object's `fuse` returns two invokes of `take`, one to each party. Both carry ONE byte string, the deal.
- Each `take` runs as its own object. It decodes those bytes, reads its own offer and its peer's (the declared peer read, LANG-75.11), evaluates the generated term `offerJoint` on the two pinned offers, and retracts only its own offer (law 4, `rowParent`).
- Both retracts sit in one Draft, and that Draft is sealed once. The tree commits or fails whole.

**What it is not.** It is not a joint law, and it is not one judge. Nothing in the Turn observes both offer rows, or both session rows, together. Two runs evaluate one term. They agree on θ because they decode one byte string, and that is the matcher's guarantee (`fuse_calls`), not the takes'. An owner may root-invoke its own `take` with no matcher at all, so one session row is not a fuse. `Program.judge`, `deriveTurn` and the 85 / 86 / 59 / 51 / 21 law theorems are untouched.

**K stays deferred.** K is a kernel judge over the sealed Draft. Its trigger: the first row whose invariant spans objects of two packages, or methods no generator wrote, or the owner-root `take` named as a defect by a row's owner.
