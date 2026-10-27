import sys
p=sys.argv[1]; s=open(p).read()
old="""      else if Term.usesVar pi.2 c.body then .error (.supportMoved h.name pi.2)
      else .ok (removed ++ [pi.2])) []"""
new="""      else if Term.usesVar pi.2 c.body then .error (.supportMoved h.name pi.2)
      else match pin with
        | .cell _ => .ok removed
        | _ => .ok (removed ++ [pi.2])) []"""
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
