# omega.py FILE... — append ` (Ω := [])` to every complete call of the checker that omits Ω (S9, condition 3).
import re, sys
ARITY = {"inferE": 3, "inferFields": 3, "inferArms": 4, "inferSubst": 4, "checkE": 3, "infer": 3, "check": 3}
NAMES = sys.argv[1].split(",")
STOP = {"with", "then", "else", "do", "fun", "at", "by", "|", "=>", ":=", "=", "∧", "∨", "→", "↔", ",", "<|>", "<$>", ">>=", "|>"}
def args(s, i):
    """parse arguments from s[i:]; return list of (start,end)."""
    out = []
    n = len(s)
    while True:
        j = i
        while j < n and s[j] in " \t": j += 1
        if j >= n or s[j] == "\n": return out, i
        c = s[j]
        if c in "([{⟨":
            close = {"(": ")", "[": "]", "{": "}", "⟨": "⟩"}[c]
            depth = 0; k = j
            while k < n:
                if s[k] in "([{⟨": depth += 1
                elif s[k] in ")]}⟩":
                    depth -= 1
                    if depth == 0: break
                k += 1
            if s[j:j+2] == "(Ω" or s[j:k+1].startswith("(Ω :="): return None, None
            k += 1
            while k < n and s[k] == "." and k + 1 < n and (s[k+1].isalnum() or s[k+1] == "_"):
                k += 1
                while k < n and (s[k].isalnum() or s[k] in "_'?!."): k += 1
            out.append((j, k)); i = k
        else:
            m = re.match(r"[^\s()\[\]{}⟨⟩,]+", s[j:])
            if not m: return out, i
            tok = m.group(0)
            if tok in STOP or tok.startswith("|") or tok in (")", "]"): return out, i
            if re.match(r"^[+\-*/<>≤≥≠∘^%]+$", tok): return out, i
            out.append((j, j + len(tok))); i = j + len(tok)
for path in sys.argv[2:]:
    s = open(path, encoding="utf-8").read()
    edits = []
    for name in NAMES:
        for m in re.finditer(r"(?<![\w.'])" + re.escape(name) + r"(?![\w'?!])", s):
            line_start = s.rfind("\n", 0, m.start()) + 1
            line = s[line_start:m.start()]
            if re.match(r"\s*(private )?def\s+" + re.escape(name) + r"\b", line + name): continue
            if re.search(r"(/-|--|^\s*\*|`)", line) and not re.search(r"(theorem|lemma|def|:=|=>|\(h)", line): continue
            if "--" in line: continue
            a, end = args(s, m.end())
            if a is None: continue
            if len(a) == ARITY[name]:
                edits.append((end, end, " (Ω := [])"))
            elif len(a) == ARITY[name] + 1:
                x, y = a[-1]
                edits.append((x, y, "(Ω := " + s[x:y] + ")"))
    for x, y, t in sorted(set(edits), reverse=True):
        s = s[:x] + t + s[y:]
    open(path, "w", encoding="utf-8").write(s)
    print(path, len(set(edits)))
