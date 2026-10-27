p = "testground/teach.js"
s = open(p).read()

def rep(a, b, label):
    global s
    n = s.count(a)
    assert n == 1, f"{label}: found {n}"
    s = s.replace(a, b)
    print(f"patched {label}")

# 1. idLink: an account opens its window too
rep("    if (!['object', 'package', 'grant'].includes(c.kind))",
    "    if (!['object', 'package', 'grant', 'account'].includes(c.kind))",
    "idLink kinds")

# 2. openId: route an account to the inspector (which renders its value)
rep("""    if (c.kind === 'object') return openInspector(m, hex);
    if (c.kind === 'package') return openPackage(m, hex);""",
    """    if (c.kind === 'object' || c.kind === 'account') return openInspector(m, hex);
    if (c.kind === 'package') return openPackage(m, hex);""",
    "openId route")

# 3. the account panel (Kernel.Value.ofCell through tg_cell), and the branch at the top of openInspector
rep("""  async function openInspector(m, id) {
    const w = openWindow({ id: `obj-${id}`, title: `Object ${short(id)}`, w: 640, body: $('div', {}, 'reading…') });""",
    """  // an account is not an object (read ? refuses it): its window is its value, read through tg_cell
  // (Kernel.Value.ofCell) off the member's own follow, so it stays current after every command
  function accountPanel(m, id, c) {
    return $('div', { class: 'inspector' },
      kv([['account', id], ['owner', idLink(m, c.owner)], ['asset', $('code', {}, c.asset ?? '-')],
        ['balance', `${c.balance ?? 0} of ${c.asset ? short(c.asset) : 'the asset'}`],
        ['floor', c.floor ?? '-'],
        ['viewed by', `${m.name}'s follow, updated after each command`]]),
      $('p', { class: 'dim' }, 'An account is a cell. transfer moves value between accounts. The balance is the value it holds now.'));
  }
  async function openInspector(m, id) {
    const c0 = cellOf(m, id);
    if (c0.kind === 'account') {
      const w = openWindow({ id: `obj-${id}`, title: `Account ${short(id)}`, w: 560, body: $('div', {}, 'reading…') });
      w.refresh = async () => w.setBody(accountPanel(m, id, cellOf(m, id)));
      await w.refresh();
      return w;
    }
    const w = openWindow({ id: `obj-${id}`, title: `Object ${short(id)}`, w: 640, body: $('div', {}, 'reading…') });""",
    "account panel")

# 4. the grades and held fields, read beside the package source
rep("""      const shown = src?.surface ?? src?.core ?? '';""",
    """      const shown = src?.surface ?? src?.core ?? '';
      // the package's grades (LANG-89) and held fields (LANG-90), read off the member's follow:
      // read OBJ ? prints neither
      const iface = pkg ? answer((m.K ?? K()).iface(m.index, pkg)) : null;
      const grade = {}, held = {};
      if (iface?.ok) for (const l of iface.text.trim().split('\\n').filter(Boolean)) {
        const x = l.split(' ');
        if (x[0] === 'grade') grade[x[1]] = x[3];
        else if (x[0] === 'holds') held[x[1]] = x[2];
      }""",
    "iface read")

# 5. the Methods table gains the grade column
rep("""        methods.length ? [h('Methods'), $('table', { class: 'props sunken methods' },
          $('tr', {}, $('td', {}, 'index'), $('td', {}, 'name'), $('td', {}, 'argument type'), $('td', {}, 'calls it may make'), $('td', {}, '')),
          methods.map((x) => $('tr', {}, $('td', {}, x.i), $('td', {}, $('b', {}, x.label)), $('td', {}, $('code', {}, x.ty)),
            $('td', {}, calls.filter((c) => c.i === x.i).map((c) => $('div', {}, $('code', {}, c.ty)))),
            $('td', {}, $('a', { class: 'cmd', title: 'put a call with an example argument in the terminal', onclick: () => prefill(m, `invoke ${id} ${x.i} ${quoteArg(example(m, x.ty))}`) }, `call ${x.label}…`)))))] : '',""",
    """        methods.length ? [h('Methods'), $('table', { class: 'props sunken methods' },
          $('tr', {}, $('td', {}, 'index'), $('td', {}, 'name'), $('td', {}, 'argument type'), $('td', {}, 'calls it may make'), $('td', {}, 'grade (moves)'), $('td', {}, '')),
          methods.map((x) => $('tr', {}, $('td', {}, x.i), $('td', {}, $('b', {}, x.label)), $('td', {}, $('code', {}, x.ty)),
            $('td', {}, calls.filter((c) => c.i === x.i).map((c) => $('div', {}, $('code', {}, c.ty)))),
            $('td', {}, grade[x.label] ? `≤ ${grade[x.label]}` : ''),
            $('td', {}, $('a', { class: 'cmd', title: 'put a call with an example argument in the terminal', onclick: () => prefill(m, `invoke ${id} ${x.i} ${quoteArg(example(m, x.ty))}`) }, `call ${x.label}…`)))))] : '',""",
    "grade column")

# 6. the Relations pass their held field
rep("""        rels.length ? [h('Relations'), rels.map((r) => relPanel(m, id, r))] : '',""",
    """        rels.length ? [h('Relations'), rels.map((r) => relPanel(m, id, r, held))] : '',""",
    "rels pass held")

# 7. relPanel renders the holds field
rep("""  function relPanel(m, obj, r) {
    const name = (r.match(/^\\((\\S+)/) || [])[1] ?? r;
    const out = $('div', {});
    const list = async () => {
      const x = await (m.nd ?? ctx.nd()).run(m, ['read', obj, name, '16']);
      out.replaceChildren(pre((x.exit === 'ok' ? x.stdout : x.stderr).trim() || '(no rows)'));
    };
    return $('div', {}, $('code', {}, r), ' ', $('button', { class: 'btn', onclick: list }, 'list rows'), out);
  }""",
    """  function relPanel(m, obj, r, held = {}) {
    const name = (r.match(/^\\((\\S+)/) || [])[1] ?? r;
    const out = $('div', {});
    const list = async () => {
      const x = await (m.nd ?? ctx.nd()).run(m, ['read', obj, name, '16']);
      out.replaceChildren(pre((x.exit === 'ok' ? x.stdout : x.stderr).trim() || '(no rows)'));
    };
    return $('div', {}, $('code', {}, r),
      held[name] ? $('span', {}, ` every row's ${held[name]} is value the object holds for it`) : '',
      ' ', $('button', { class: 'btn', onclick: list }, 'list rows'), out);
  }""",
    "holds line")

# 8. the glossary gains the two words
rep("""          ['core', 'The package as the kernel reads it: the source lowered to plain terms (lam, record, case, …).'],""",
    """          ['grade', 'The most one run of the method may move: the sum over the transfers and credits it returns. A run past it is refused and nothing moves.'],
          ['holds', 'A relation whose rows name value the object holds. A run that writes such a row must move that value in; one that retracts it must move it out.'],
          ['core', 'The package as the kernel reads it: the source lowered to plain terms (lam, record, case, …).'],""",
    "glossary")

open(p, "w").write(s)
print("teach.js patched")
