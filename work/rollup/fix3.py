import re
p="Kernel/ObjectiveActivityReceiver.lean"
s=open(p).read()
# conflict 1: drop everything (HEAD side empty); the seats side's defs move to ActivitySeatEnd
m=list(re.finditer(r"<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>> 6abc7401[^\n]*\n", s, re.S))
assert len(m)==3, len(m)
# conflict 3 (asserts): union
def sub(s, m, text):
    return s[:m.start()]+text+s[m.end():]
c3=m[2]; c2=m[1]; c1=m[0]
s=sub(s,c3,"#assert_axioms native_delivery_fields_bind_checkpoint\n#assert_axioms native_end_closes_held_seats\n")
# conflict 2: theirs, with Decided.finalIntent -> AdmittedTurn.finalIntent
t=c2.group(2).replace("Decided.finalIntent","ObjectiveActivity.AdmittedTurn.finalIntent")
s=sub(s,c2,t)
s=sub(s,c1,"")
open(p,"w").write(s)
