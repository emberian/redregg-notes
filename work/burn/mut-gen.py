#!/usr/bin/env python3
"""mut-gen.py SRC OUT.jsonl  -- enumerate mutation sites in admit/refuse defs of the Kernel files.
One JSON line per mutant: id, file, line, kind, old (full line), new (full line).
Only single-line edits; a mutant is applied by replacing line `line` of `file`.
Only code inside def/abbrev/instance (not theorem/lemma/structure, not `: Prop` defs)."""
import re, sys, json, os
src, out = sys.argv[1], sys.argv[2]
FILES = """ObjectiveActivity ObjectiveActivityCell ObjectiveActivityGate ObjectiveActivityGateRoute ObjectiveActivityReceiver
ObjectiveActivityUpgrade ObjectiveActivityWire ObjectiveCall ObjectiveCallReference ObjectiveSend ObjectiveDomain
ObjectiveDomainInvariant AnswerSlot Inbox ReceivingLaw ResourceBirthController PayEnrolReceiver SeatStore NativeHostContext""".split()
DECL = re.compile(r'^(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|noncomputable|partial|unsafe|nonrec)\s+)*(def|abbrev|instance|theorem|lemma|structure|inductive|class|example|macro|syntax|opaque|axiom|namespace|end|section|open|variable|set_option|local|scoped|attribute|notation|#\w+|mutual|termination_by|decreasing_by|universe|import|elab|deriving|initialize|builtin_initialize)\b')
REFUSE = re.compile(r'error|throw|refus|fail|none|drain|reject|deny|denied|false|Except|invalid|stale|absent|missing|exceed', re.I)
def split_code(line):
    i = line.find('--')
    return (line[:i], line[i:]) if i >= 0 else (line, '')
def operand_left(s, i):
    """start index of left operand of operator at s[i:]; None if nothing on this line"""
    depth = 0; j = i
    while j > 0:
        c = s[j-1]
        if c in ')]}⟩': depth += 1
        elif c in '([{⟨':
            if depth == 0: break
            depth -= 1
        elif depth == 0:
            if s[:j].endswith(('&& ', '|| ', '∧ ', '∨ ', ':= ', '=> ', ', ')) or s[:j].rstrip().endswith(('then','else','if','unless','do','guard','&&','||','∧','∨',':=','=>')): break
        j -= 1
    st = j
    t = s[st:i]
    if not t.strip(): return None
    return st
def operand_right(s, i):
    depth = 0; j = i
    while j < len(s):
        c = s[j]
        if c in '([{⟨': depth += 1
        elif c in ')]}⟩':
            if depth == 0: break
            depth -= 1
        elif depth == 0:
            rest = s[j:]
            if re.match(r' (&&|\|\||∧|∨|then|else|do|:=|=>)( |$)', rest): break
        j += 1
    if not s[i:j].strip(): return None
    return j
muts = []
for f in FILES:
    path = os.path.join(src, 'Kernel', f + '.lean')
    if not os.path.exists(path): print('missing', path, file=sys.stderr); continue
    lines = open(path, encoding='utf-8').read().split('\n')
    kind = None; isprop = False; blk = False
    for n, ln in enumerate(lines, 1):
        if blk:
            if '-/' in ln: blk = False
            continue
        code, com = split_code(ln)
        st = code.lstrip()
        if st.startswith('/-'):
            if '-/' not in st: blk = True
            continue
        m = DECL.match(ln)
        if m:
            kind = m.group(1)
            isprop = False
            # header up to :=
            hdr = ln
            k = n
            while ':=' not in hdr and k < len(lines) and k < n + 8:
                hdr += ' ' + lines[k]; k += 1
            h = hdr.split(':=')[0]
            if re.search(r':\s*Prop\b', h): isprop = True
        if kind not in ('def', 'abbrev', 'instance') or isprop: continue
        if not st or st.startswith('--'): continue
        def emit(k2, new_code):
            new = new_code + com
            if new != ln: muts.append(dict(file=f'Kernel/{f}.lean', line=n, kind=k2, old=ln, new=new, refusal=bool(REFUSE.search(code))))
        # if-conditions (non-dependent)
        for mi in re.finditer(r'\bif\s+(?!let\b)(?!\w[\w\'.]*\s*:[^=])(.+?)\s+then\b', code):
            cond = mi.group(1)
            if cond.count('(') != cond.count(')'): continue
            a, b = mi.start(1), mi.end(1)
            emit('negate-if', code[:a] + '¬(' + cond + ')' + code[b:])
            if REFUSE.search(code[mi.end():]) or True:
                emit('fallthrough-if(cond:=False)', code[:a] + 'False' + code[b:])
        # conjunct -> true
        for mi in re.finditer(r' (&&|∧) ', code):
            op = mi.group(1); tr = 'true' if op == '&&' else 'True'
            l = operand_left(code, mi.start()); r = operand_right(code, mi.end())
            if r is not None:
                emit(f'conjunct-{op}-right:=true', code[:mi.end()] + tr + code[r:])
            if l is not None:
                emit(f'conjunct-{op}-left:=true', code[:l] + tr + code[mi.start():])
        for mi in re.finditer(r' (\|\||∨) ', code):
            op = mi.group(1); fl = 'false' if op == '||' else 'False'
            r = operand_right(code, mi.end()); l = operand_left(code, mi.start())
            if r is not None: emit(f'disjunct-{op}-right:=false', code[:mi.end()] + fl + code[r:])
            if l is not None: emit(f'disjunct-{op}-left:=false', code[:l] + fl + code[mi.start():])
        # unless / guard
        if re.match(r'\s*unless\b', code):
            mm = re.match(r'(\s*unless\s+)(.+?)(\s+do\b.*)$', code)
            if mm:
                emit('negate-unless', mm.group(1) + '¬(' + mm.group(2) + ')' + mm.group(3))
                emit('fallthrough-unless(cond:=True)', mm.group(1) + 'True' + mm.group(3))
        mm = re.match(r'(\s*)guard\s+(.+)$', code)
        if mm: emit('fallthrough-guard', mm.group(1) + 'guard True')
        # off-by-one: strictness flip, only on condition-ish lines
        if re.search(r'\bif\b| && | ∧ | \|\| |\bunless\b|^\s*(&&|∧|\|\|)', code):
            for sym, rep in ((' ≤ ', ' < '), (' < ', ' ≤ '), (' ≥ ', ' > '), (' > ', ' ≥ ')):
                for mi in re.finditer(re.escape(sym), code):
                    if sym == ' > ' and code[mi.start()-1:mi.start()] in '-=': continue
                    emit(f'offbyone({sym.strip()}->{rep.strip()})', code[:mi.start()] + rep + code[mi.end():])
seen = set(); res = []
for m in muts:
    k = (m['file'], m['line'], m['new'])
    if k in seen: continue
    seen.add(k); res.append(m)
for i, m in enumerate(res): m['id'] = f'm{i:04d}'
with open(out, 'w') as o:
    for m in res: o.write(json.dumps(m, ensure_ascii=False) + '\n')
from collections import Counter
print(len(res), 'mutants'); print(Counter(m['file'] for m in res)); print(Counter(m['kind'].split('(')[0].split('-')[0] + ':' + m['kind'] for m in res).most_common(30))
