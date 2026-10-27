import sys
p=sys.argv[1]; s=open(p).read()
old="  Term.renameVar (fun n => embedding.getD n n) filling\n"
new="  Term.renameVar (fun n => if n = 1 && embedding.getD 1 1 != 1 then 0 else embedding.getD n n) filling\n"
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
