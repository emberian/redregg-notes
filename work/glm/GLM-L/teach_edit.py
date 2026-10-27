import pathlib
p = pathlib.Path("/home/hbox/nd-land/glm-l/Web/Sim/Teach.lean")
s = p.read_text()

old_doc = """/-- `tg_cell I ID`: what ID names on member I's follow World, so the page opens the right window:
`kind WORD` (`none`: no cell has this id, a hash that is not a cell's), `retired` for a tombstone,
and for a grant its fields (`target`, `grantee` (or `anyone`), `issuer`, `parent`, `rights`). -/"""
new_doc = """/-- `tg_cell I ID`: what ID names on member I's follow World, so the page opens the right window:
`kind WORD` (`none`: no cell has this id, a hash that is not a cell's), `retired` for a tombstone,
for a grant its fields (`target`, `grantee` (or `anyone`), `issuer`, `parent`, `rights`), and for a
member its key slots (`key`, `next`, `sponsor`: the current key, the digest of the precommitted next
one, the sponsor), so a rotation is visible on the cell it changed. -/"""
assert s.count(old_doc) == 1, "docstring not found"
s = s.replace(old_doc, new_doc)

old_obj = """        else if c.kind = kindObject then
          [s!"owner {slotHex c slotOwner}"] ++ ((c.slots.get slotPackage).map fun p => [s!"package {Text.toHex p}"]).getD []
        else []"""
new_obj = """        else if c.kind = kindObject then
          [s!"owner {slotHex c slotOwner}"] ++ ((c.slots.get slotPackage).map fun p => [s!"package {Text.toHex p}"]).getD []
        else if c.kind = kindMember then
          [s!"key {slotHex c slotKey}",
           s!"next {slotHex c slotNext}",
           s!"sponsor {slotHex c slotSponsor}"]
        else []"""
assert s.count(old_obj) == 1, "object branch not found"
s = s.replace(old_obj, new_obj)

p.write_text(s)
print("edited:", p)
