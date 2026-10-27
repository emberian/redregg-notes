import re

t = open("Lang/Journey/Gen.lean").read()

# 1. the docstring row list: keep the faerie's GN25, add mine as GN26 after it
doc_head = """<<<<<<< HEAD
* GN25 (LANG-108) a creator WRITTEN IN SURFACE TEXT: a method with a `(createOf (rec (n nat)))` slot whose
  `done` returns `(createOf (pkg #bytes) (state (record (n 5))))`. B installs it, creates C, and makes: the
  ONE Turn bears B's object of the package id (owned by B) and then the package. The same text with an
  `install` slot is refused `callKind createOf` when it is read.
=======
* GN25 the same promise in the authoring text: a generator whose `generate` declares
  `(effect (moves 0) (produces …))` with `reset` in the interface is written in surface text, lowered
  and installed, and generate is refused `produces generate: lacks reset`, nothing born.
>>>>>>> b91bc1d2 (lang: a method's effect clause in the authoring text can name the interface it produces (LANG-103's surface form))
"""
doc_new = """* GN25 (LANG-108) a creator WRITTEN IN SURFACE TEXT: a method with a `(createOf (rec (n nat)))` slot whose
  `done` returns `(createOf (pkg #bytes) (state (record (n 5))))`. B installs it, creates C, and makes: the
  ONE Turn bears B's object of the package id (owned by B) and then the package. The same text with an
  `install` slot is refused `callKind createOf` when it is read.
* GN26 the same promise in the authoring text (LANG-103's surface clause): a generator whose `generate`
  declares `(effect (moves 0) (produces …))` with `reset` in the interface is written in surface text,
  lowered and installed, and generate is refused `produces generate: lacks reset`, nothing born.
"""
assert t.count(doc_head) == 1
t = t.replace(doc_head, doc_new)

# 2. the code: keep the faerie's GN25 whole, then my block as GN26 with fresh variable names
code_head = t[t.index("<<<<<<< HEAD\n  -- GN25 (LANG-108)"):]
code_head = code_head[:code_head.index(">>>>>>> b91bc1d2")] + ">>>>>>> b91bc1d2 (lang: a method's effect clause in the authoring text can name the interface it produces (LANG-103's surface form))\n"
faerie = code_head[len("<<<<<<< HEAD\n"):-len("=======\n")] if False else None

m = re.search(r"<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> [^\n]*\n", t, re.S)
blocks = re.findall(r"<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> [^\n]*\n", t, re.S)
assert len(blocks) == 1, len(blocks)
theirs, mine = blocks[0]

# theirs: the faerie's GN25 block, unchanged. mine: renumbered to GN26, fresh names.
mine26 = mine
mine26 = mine26.replace("-- GN25 the same promise written in surface text", "-- GN26 the same promise written in surface text")
mine26 = mine26.replace("text25?", "text26?")
mine26 = mine26.replace("text25", "text26")
mine26 = mine26.replace("p25", "p26")
mine26 = mine26.replace("r49, v49, g49?", "r51, v51, g51?")
mine26 = mine26.replace("gpkg49, G49", "gpkg51, G51")
mine26 = mine26.replace("r49", "r51").replace("v49", "v51").replace("g49?", "g51?")
mine26 = mine26.replace("r50, v50, t50", "r52, v52, t52")
mine26 = mine26.replace("r50", "r52").replace("v50", "v52").replace("t50", "t52")
mine26 = mine26.replace('note r "GN26 the declared interface has no text"', 'note r "GN26 the declared interface has no text"')
mine26 = mine26.replace('"GN26 {v51}"', '"GN26 {v51}"')
# every GN25 string inside my block becomes GN26
mine26 = mine26.replace("GN25", "GN26")

t = t.replace(m.group(0), theirs + "\n" + mine26 + "\n")
open("Lang/Journey/Gen.lean", "w").write(t)
print("gen resolved")
