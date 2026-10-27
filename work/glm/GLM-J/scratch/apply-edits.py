#!/usr/bin/env python3
"""Apply GLM-J's edits to shared files in the nanodregg worktree. Each edit asserts its anchor
appears exactly once (or that the edit is already in), so a re-run fails loudly, never duplicates."""
import sys
from pathlib import Path

root = Path(sys.argv[1])

def edit(rel, old, new, count=1):
    p = root / rel
    t = p.read_text()
    if new in t and old not in t:
        print(f"  {rel}: already applied")
        return
    n = t.count(old)
    assert n == count, f"{rel}: anchor appears {n} times, expected {count}: {old[:60]!r}"
    p.write_text(t.replace(old, new, count))
    print(f"  {rel}: edited")

# --- docs/MEMBER.md: the retire row in the command table ---
edit(
    "docs/MEMBER.md",
    "| Cancel: nd cancel CALL | Follow checks the member's own signed call can be cancelled, requests a cancel signature and sends it. A second catch-up must show the recorded cancellation before success. |",
    "| Cancel: nd cancel CALL | Follow checks the member's own signed call can be cancelled, requests a cancel signature and sends it. A second catch-up must show the recorded cancellation before success. |\n"
    "| Retire: nd retire CELL | The owner retires an object it owns or an empty account; the issuer of a grant retires the grant (revocation). Every law in force judges the occasion over the object's last state. An object holding rows is refused rowsRemain; once empty the retirement admits, the storage returns to the World, and the id stays a tombstone. Reads and calls under it are refused missingCell, and every grant over it is dead. |",
)

# --- client/tests/foreign.rs: the stale claim that nd has no verb that retires an object ---
edit(
    "client/tests/foreign.rs",
    "here (`nd` has no verb that retires an object or signs a call it does not send); they are the",
    "here (`nd` signs no call it does not send; an object's retirement is `retire.rs`'s); they are the",
)

# --- Web/Sim/Testground.lean: the meter answers the World's allowance ---
edit(
    "Web/Sim/Testground.lean",
    "`refusals R`, `total T`, `height H`, `health HEX`, `checked ok` (or `checked NAME`). Nothing here asks the\nwriter. -/",
    "`refusals R`, `total T`, `height H`, `health HEX`, `checked ok` (or `checked NAME`), `allowance A` (the\nWorld's storage budget left; a retirement returns an entry's weight to it, KERNEL-70). Nothing\nhere asks the writer. -/",
)
edit(
    "Web/Sim/Testground.lean",
    '      s!"height {w.height}\\nhealth {Text.toHex b}\\nchecked {verdict}\\n").toUTF8',
    '      s!"height {w.height}\\nhealth {Text.toHex b}\\nchecked {verdict}\\n" ++\n      s!"allowance {w.allowance}\\n").toUTF8',
)

# --- testground/demos.js: load the retirement scene (the one line) ---
edit(
    "testground/demos.js",
    "// demos.js — each demo is the nd command sequence a member types, nothing more: the same argv the",
    "import { scenes as retireScenes } from './scenes-retire.js';\n\n"
    "// demos.js — each demo is the nd command sequence a member types, nothing more: the same argv the",
)
edit(
    "testground/demos.js",
    "};\n\n// META (DESIGN-META, journey §GN):",
    "};\nObject.assign(demos, retireScenes);   // scenes-retire.js: the retirement scene (KERNEL-70, journey §RT)\n\n// META (DESIGN-META, journey §GN):",
)

# --- testground/testground.js: the tour step, and the allowance in the meter line ---
edit(
    "testground/testground.js",
    "answers.', demo: 'inbox' },",
    "answers.', demo: 'inbox' },\n"
    "  { say: 'Retire: the owner ends an object. A member who does not own it is refused (notOwner); a row under the object blocks the end (rowsRemain); once the object is empty its retirement admits, the storage it held returns to the World, and the id stays a tombstone. Reads under it are refused (missingCell).', demo: 'retire' },",
)
edit(
    "testground/testground.js",
    "  return `ticks ${(+kv.ticks).toLocaleString()} / ${(+kv.budget).toLocaleString()} this window · ${kv.refusals} refusals · ${checked}`;",
    "  return `ticks ${(+kv.ticks).toLocaleString()} / ${(+kv.budget).toLocaleString()} this window · ${kv.refusals} refusals · ${checked}`\n"
    "    + (kv.allowance != null ? ` · ${(+kv.allowance).toLocaleString()} bytes of storage left` : '');",
)

# --- testground/axes-run.mjs: the retire demo in the gate, with its measured checks ---
edit(
    "testground/axes-run.mjs",
    "import { demos, runDemo } from './demos.js';",
    "import { demos, runDemo } from './demos.js';\nimport { retireChecks } from './scenes-retire.js';",
)
edit(
    "testground/axes-run.mjs",
    "const axes = control ? ['harness-control'] : only ? [only] : ['generator', 'creator', 'meter', 'timelock', 'document', 'inbox'];",
    "const axes = control ? ['harness-control'] : only ? [only] : ['generator', 'creator', 'meter', 'timelock', 'document', 'inbox', 'retire'];",
)
edit(
    "testground/axes-run.mjs",
    "    console.log(`${ok ? '    ' : 'FAIL'} bob's health receipt (${(kv.health ?? '').length / 2} bytes, checked ${kv.checked}): ticks ${kv.ticks} of ${kv.budget} · refusals ${kv.refusals} · total ${kv.total} · height ${kv.height}`);",
    "    console.log(`${ok ? '    ' : 'FAIL'} bob's health receipt (${(kv.health ?? '').length / 2} bytes, checked ${kv.checked}): ticks ${kv.ticks} of ${kv.budget} · refusals ${kv.refusals} · total ${kv.total} · height ${kv.height}`);\n"
    "  }\n"
    "  if (name === 'retire' && r.ok) {\n"
    "    // the retirement's own numbers (scenes-retire.js): the inspector reads the tombstone, and a\n"
    "    // retirement gives the entry's weight back to the World's allowance (journey §RT2)\n"
    "    const c = await retireChecks(members, r.v);\n"
    "    const ok = c.tombstone && c.retired && c.unreadable && c.back > 0;\n"
    "    if (!ok) bad++;\n"
    "    console.log(`${ok ? '    ' : 'FAIL'} the retired board reads kind retired; a full cell's retirement returned ${c.back} bytes (allowance ${c.before} -> ${c.after})`);",
)

print("all edits applied")
