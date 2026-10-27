import pathlib
p = pathlib.Path("/home/hbox/nd-land/glm-l/testground/teach.js")
s = p.read_text()

old = """    if (c.kind === 'object') return openInspector(m, hex);
    if (c.kind === 'package') return openPackage(m, hex);
    if (c.kind === 'grant') return openGrant(m, hex);
    return null;"""
new = """    if (c.kind === 'object') return openInspector(m, hex);
    if (c.kind === 'package') return openPackage(m, hex);
    if (c.kind === 'grant') return openGrant(m, hex);
    if (c.kind === 'member') return openMember(m, hex);
    return null;"""
assert s.count(old) == 1, "openId not found"
s = s.replace(old, new)

old = """    const n = nameOf(hex);
    if (n) return $('span', { title: `member ${hex}` }, n);
    if (hex === 'anyone') return 'anyone';
    const c = cellOf(m, hex);
    if (!['object', 'package', 'grant'].includes(c.kind)) return $('span', { class: 'dim', title: `${hex} (${c.kind === 'none' ? 'not a cell' : c.kind})` }, short(hex));"""
new = """    const n = nameOf(hex);
    if (n) return $('a', { class: 'cmd', title: `member ${hex}`, onclick: () => openMember(m, hex) }, n);
    if (hex === 'anyone') return 'anyone';
    const c = cellOf(m, hex);
    if (!['object', 'package', 'grant', 'member'].includes(c.kind)) return $('span', { class: 'dim', title: `${hex} (${c.kind === 'none' ? 'not a cell' : c.kind})` }, short(hex));"""
assert s.count(old) == 1, "idLink not found"
s = s.replace(old, new)

old = """  // ---------------------------------------------------------------- the session's cells
  function openInventory(m, ids) {"""
new = """  // ---------------------------------------------------------------- a member
  function openMember(m, id) {
    const c = cellOf(m, id);
    const body = $('div', { class: 'inspector' },
      kv([['member', id], ['key', c.key ?? '-'], ['next', c.next ?? '-'], ['sponsor', c.sponsor === '-' || !c.sponsor ? '-' : idLink(m, c.sponsor)]]),
      $('p', { class: 'dim' }, 'A member is a cell. key is the public key that signs its calls; rotate replaces it, and a call signed with the old one is refused (unknownKey). next is the digest of the precommitted next key: the rotate that installs it must be signed by that key (notPrecommitted otherwise).'));
    openWindow({ id: `member-${id}`, title: `Member ${short(id)}`, w: 520, body });
  }

  // ---------------------------------------------------------------- the session's cells
  function openInventory(m, ids) {"""
assert s.count(old) == 1, "openInventory anchor not found"
s = s.replace(old, new)

old = "return { openLesson, openId, openPackage, openGrant, openInventory, cellOf, idLink, openInspector, openEditor, openRepl, openGrammar, openTurn, openTutorial, remember, idOfText, reset, steps, templates, parseLine };"
new = "return { openLesson, openId, openPackage, openGrant, openMember, openInventory, cellOf, idLink, openInspector, openEditor, openRepl, openGrammar, openTurn, openTutorial, remember, idOfText, reset, steps, templates, parseLine };"
assert s.count(old) == 1, "export list not found"
s = s.replace(old, new)

p.write_text(s)
print("teach.js edited")
