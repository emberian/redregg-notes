import sys
p=sys.argv[1]; s=open(p).read()
old="""  let present := h.guardPin.all (supportLive digestOf look rv self)
"""
new="""  if h.guardPin.any (supportLive digestOf look rv self) then throw (.guardBlocked h.name)
  let present := h.guardPin.all (supportLive digestOf look rv self)
"""
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
