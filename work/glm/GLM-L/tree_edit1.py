import pathlib

# demos.js — the one load line (an import and the assignment; a side-effect import would run this
# module before `demos` exists: the cycle is real, so the merge is two lines, the smallest that works).
p = pathlib.Path("/home/hbox/nd-land/glm-l/testground/demos.js")
s = p.read_text()
old = """/** Run a lie scene: `act` is the page's (or the harness's) runner for each kind of step. */"""
new = """// ROTATE (GLM-L, CLIENT-54; the rotate row JROT/JROTL, Protocol/Rows.lean, and Kernel/Sim's rotate
// lines): a member's key rotation. The demo here is the subset a plain runner drives; the full scene
// (a thief's forged calls with the saved old key, custody's advance, the member cell's key slots) is
// scenes-rotate.js, run by scenes-rotate-run.mjs in the gate. Two lines, not one: a side-effect
// import of scenes-rotate.js would evaluate it before `demos` is initialized (the module cycle).
import { rotateDemo } from './scenes-rotate.js';
demos.rotate = rotateDemo;

/** Run a lie scene: `act` is the page's (or the harness's) runner for each kind of step. */"""
assert s.count(old) == 1, "demos.js anchor not found"
s = s.replace(old, new)
p.write_text(s)

# gate.sh — run the rotation scene after the axes, and its control in the harness-control block.
p = pathlib.Path("/home/hbox/nd-land/glm-l/testground/build/gate.sh")
s = p.read_text()
old = """node axes-run.mjs || { echo "FAIL an axis demo did not answer as scripted (axes-run.mjs)"; exit 1; }"""
new = """node axes-run.mjs || { echo "FAIL an axis demo did not answer as scripted (axes-run.mjs)"; exit 1; }
node scenes-rotate-run.mjs || { echo "FAIL the rotation scene did not answer as the rows expect (scenes-rotate-run.mjs)"; exit 1; }"""
assert s.count(old) == 1, "gate.sh axes line not found"
s = s.replace(old, new)
old = """  if node axes-run.mjs --harness-control; then echo "FAIL harness: axes-run.mjs --harness-control passed"; exit 0; fi"""
new = """  if node axes-run.mjs --harness-control; then echo "FAIL harness: axes-run.mjs --harness-control passed"; exit 0; fi
  if node scenes-rotate-run.mjs --harness-control; then echo "FAIL harness: scenes-rotate-run.mjs --harness-control passed"; exit 0; fi"""
assert s.count(old) == 1, "gate.sh control line not found"
s = s.replace(old, new)
# the header's list of what the gate runs gains the scene
old = """then each axis's
# demo (axes-run.mjs: the generator, the creator, the meter to ticksBudget, the time-lock, the document), the tutorial's"""
new = """then each axis's
# demo (axes-run.mjs: the generator, the creator, the meter to ticksBudget, the time-lock, the document), the key-rotation
# scene (scenes-rotate-run.mjs: rotate, the old key refused by name, the thief's rotate refused
# notPrecommitted, custody advanced, the member cell's key slots), the tutorial's"""
assert s.count(old) == 1, "gate.sh header not found"
s = s.replace(old, new)
p.write_text(s)

# docs/MEMBER.md — the "Your key" section, before "What nd does and does not do".
p = pathlib.Path("/home/hbox/nd-land/glm-l/docs/MEMBER.md")
s = p.read_text()
old = "## What nd does and does not do"
new = """## Your key

Your member cell holds the digest of your next key, precommitted when you were enrolled. Every call names the member and the key it signs with; a key that is not the member's current one is refused `unknownKey`. `rotate` is the one call that does not sign with the current key: it is signed by the NEXT key, whose digest must be the precommitted one, or it is refused `notPrecommitted` (KERNEL-6). A stolen current key cannot rotate.

What a member's custody holds:

| File | What it is |
|---|---|
| `ND_WORKSPACE/seed` | the current secret key. It signs every call. |
| `ND_WORKSPACE/next.pub` | the next key's public half. The World holds only its digest. |
| `ND_HOLDING/next` | the next key's secret, on removable media or under another account. Needed only to rotate. |
| `ND_HOLDING/pending` | the key after next, minted fresh at precommit. |
| `ND_WORKSPACE/rotation` | the armed rotation's record. Present only mid-rotation. |

The next secret is never in the workspace ([custody.rs](../client/src/custody.rs); `client/tests/custody.rs` asserts it). A hosted resident is different: one record `ND_WORKSPACE/keys = current ‖ next [‖ pending]`, so a thief of that one file holds both keys, and for it the rotate holds only against a leak of the current key alone. The writer's certify key made the opposite trade: keybroker's `KEYS` refuses a `certify.next` line, because nothing commits to a next certify key yet (HOSTING-60).

Back up both places: the workspace (the current key) and the holding (the next secret, and the pending one mid-rotation). A backup of the workspace alone cannot rotate.

`nd rotate` runs the whole cycle: catch-up; a fresh pending key minted into the holding; the rotation planned to your next key and signed by the NEXT key; the rotation armed durably before the call is sent; settlement only on your own follow's receipt — committed advances custody (`current := next`, `next := pending`), a definitive refusal drops the pending key. A crash anywhere in between is finished by the next run. A rotation whose reply is lost is found by lookup; one that never reached the writer ends `open` and leaves custody on the old key, which still signs (the rotate row, [Rows](../Protocol/Rows.lean)).

If the current key is stolen, rotate at once. The thief cannot: they hold no next secret. Until the rotation lands they can sign calls as you. After it lands, their calls are refused `unknownKey`, and the calls they already signed die with the rotation: a rotate writes your member cell, so every pin on that cell goes stale (KERNEL-60, `rotate_stales_outstanding`). Each rotation precommits the next key, so you can rotate again whenever you want.

If the key is lost, the design has one answer: a backup. Restore the workspace and the holding and you are the member again. Without the current seed nothing can sign — custody opens only with the current seed present, so even an intact holding cannot rotate you back in (the next key could in principle sign the rotate alone; the client does not start). The member cell stays: a member is not retirable (KERNEL-70 — a member's end would leave its grants unrevocable and its objects ownerless), so its cells stay owned by it, nobody can act for it, and its objects cannot change owner. What a World offers instead is a new member: a sponsor spends one enrolment to enrol a fresh key (`enroll`, with the new key's join consent), and the person starts again with none of the old member's cells. A member's departure — handing on or sweeping what it roots — is open work.

## What nd does and does not do"""
assert s.count(old) == 1, "MEMBER.md anchor not found"
s = s.replace(old, new)
p.write_text(s)
print("demos.js, gate.sh, MEMBER.md edited")
