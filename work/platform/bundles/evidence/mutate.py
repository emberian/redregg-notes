import sys
p=sys.argv[1]; s=open(p).read()
old="      if target.materializer.rootBytes bytes = target.expectedTargetRoot then\n        match memberPatch command target logical with"
assert s.count(old)==1
s=s.replace(old,"      if True then\n        match memberPatch command target logical with")
def cut(s,a,b):
    i=s.index(a); j=s.index(b,i); return s[:i]+s[j:]
s=cut(s,"/-- **A served-root mismatch refuses by name.** -/","/-- The executor")
s=cut(s,"/-- **What thin consent shows is what commits.**","#assert_axioms memberPatch_supported")
s=s.replace(" honest_binds mismatch_refused"," honest_binds").replace("post_run thin_display_is_commit","post_run")
open(p,"w").write(s)
print("MUTATED")
