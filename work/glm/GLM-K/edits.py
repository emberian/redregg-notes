#!/usr/bin/env python3
# the market scene's wiring: one line in demos.js, carol beside alice and bob, one tour step
import pathlib

root = pathlib.Path.home() / 'nd-land/glm-k'
def edit(path, old, new, count=1):
    p = root / path
    t = p.read_text()
    assert t.count(old) == count, f'{path}: {t.count(old)} hits for {old[:60]!r}'
    p.write_text(t.replace(old, new, count))
    print(f'edited {path}')

# one line in demos.js: the market scene's own file, registered on the demos list
edit('testground/demos.js',
     "  return { ok: true, r: last, v, outcome: last && outcomeOf(last) };\n}",
     "  return { ok: true, r: last, v, outcome: last && outcomeOf(last) };\n}\n"
     "\n"
     "// the market (DESIGN-CTX §2.5b): the escrow offer as a book, in its own file\n"
     "import { scenes as marketScenes } from './scenes-market.js'; Object.assign(demos, marketScenes);\n")

# the harnesses' Worlds gain carol (the market's would-be taker)
edit('testground/axes-run.mjs',
     "const g = genesis(K, 'testground', ['alice', 'bob']);",
     "const g = genesis(K, 'testground', ['alice', 'bob', 'carol']);")
edit('testground/axes-run.mjs',
     "const axes = control ? ['harness-control'] : only ? [only] : ['generator', 'creator', 'meter', 'timelock', 'document', 'inbox'];",
     "const axes = control ? ['harness-control'] : only ? [only] : ['generator', 'creator', 'meter', 'market', 'timelock', 'document', 'inbox'];")
edit('testground/demo-run.mjs',
     "const g = genesis(K, 'testground', ['alice', 'bob']);",
     "const g = genesis(K, 'testground', ['alice', 'bob', 'carol']);")

# the page: three founders, carol's icon, the tour's count, one tour step
edit('testground/testground.js',
     "  world = genesis(K, 'testground', ['alice', 'bob']);",
     "  world = genesis(K, 'testground', ['alice', 'bob', 'carol']);")
edit('testground/testground.js',
     "icon('b', 'bob', () => world.members[1] && openTerm(world.members[1]), 'icon-m1');",
     "icon('b', 'bob', () => world.members[1] && openTerm(world.members[1]), 'icon-m1');\n"
     "icon('c', 'carol', () => world.members[2] && openTerm(world.members[2]));")
edit('testground/testground.js',
     "'One World, two members (alice, bob), all in this tab.",
     "'One World, three members (alice, bob, carol), all in this tab.")
edit('testground/testground.js',
     "  { say: 'A claim: a package says what it keeps (total <= 100), and install checks that its own law enforces it. A package whose law skips the test on a write is refused (claimUnproved).', demo: 'claims' },",
     "  { say: 'A claim: a package says what it keeps (total <= 100), and install checks that its own law enforces it. A package whose law skips the test on a write is refused (claimUnproved).', demo: 'claims' },\n"
     "  { say: 'A market: two offers hold their legs in two books. carol\\'s own take is refused (notFuser); a fuse naming a thin offer is refused (unfairLegs); bob\\'s fuse pays both legs in one turn.', demo: 'market' },")

edit('Web/Sim/Testground.lean',
     "the journey's offer (§LF), the tutorial's last step. -/",
     "the journey's offer (§LF), the tutorial's last step, and its escrow twin (§LE), the market's book. -/")

# the kernel's text menu: the escrow offer beside the offer (the same match, the same printer)
edit('Web/Sim/Testground.lean',
     "import Lang.StdOffer\n",
     "import Lang.StdOffer\nimport Lang.StdOfferEscrow\n")
edit('Web/Sim/Testground.lean',
     """   -- the journey's offer (§LF, `Lang.Journey.Offer`): one term `price`, roles buyer and seller
   ("offer", match Lang.Std.offerPackage ["price"] ["buyer", "seller"] with
     | .ok p => packageText p
     | .error _ => "")]""",
     """   -- the journey's offer (§LF, `Lang.Journey.Offer`): one term `price`, roles buyer and seller
   ("offer", match Lang.Std.offerPackage ["price"] ["buyer", "seller"] with
     | .ok p => packageText p
     | .error _ => ""),
   -- the journey's escrow offer (§LE, `Lang.Journey.OfferEscrow`): the same offer holding a value
   -- leg, the market's book (a post moves its leg in, a fuse pays both legs out in one Turn)
   ("offerEscrow", match Lang.Std.offerEscrowPackage ["price"] ["buyer", "seller"] with
     | .ok p => packageText p
     | .error _ => "")]""")

print('all edits in')
