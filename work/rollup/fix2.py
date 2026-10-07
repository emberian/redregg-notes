import re
p="Kernel.lean"
s=open(p).read()
m=re.search(r"<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>> 061f0625[^\n]*\n", s, re.S)
head=m.group(1).split("\n")
theirs=m.group(2)
cc=[l for l in head if l.startswith("import Kernel.CertifiedClearing")]
assert len(cc)==1
s=s[:m.start()]+theirs+cc[0]+"\n"+s[m.end():]
open(p,"w").write(s)
p="Kernel/NativeHostReplay.lean"
s=open(p).read()
m=re.search(r"<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>> 061f0625[^\n]*\n", s, re.S)
head=m.group(1); theirs=m.group(2)
# theirs = activity row w/o 'some' tail, then the seat block; keep HEAD's activity row, then the seat block with one more none
i=theirs.index("  if let some ingress := SeatReceiver")
seat=theirs[i:]
seat=seat.replace(".seat accepted, none, none, none, none, none, none, none, none, none, none, none, none⟩",".seat accepted, none, none, none, none, none, none, none, none, none, none, none, none, none⟩")
s=s[:m.start()]+head+seat+s[m.end():]
open(p,"w").write(s)
