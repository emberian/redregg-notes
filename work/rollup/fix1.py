import re
p="Kernel/ObjectiveActivityCell.lean"
s=open(p).read()
m=re.search(r"<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>> 5a3b7e7d[^\n]*\n", s, re.S)
theirs=m.group(2)
old="""resource birth may install one, and no other receiver selects it, so these
coordinates are protected: only the activity receiver writes them.
"""
new="""resource birth may install one, and every other source facet's intents are refused
by name if they write any coordinate at or above `reservedBase`
(`Kernel.ObjectiveActivityGate.ordinaryGate`, `protectedWrite`): only the kernel
activity's own typed turns write them (`Kernel.ObjectiveActivityReceiver` under
`ControlFacet.objectiveActivity`).
"""
assert old in theirs
theirs=theirs.replace(old,new)
s=s[:m.start()]+theirs+s[m.end():]
open(p,"w").write(s)
