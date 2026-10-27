import Kernel.Receive.Submit
open Nanodregg.Kernel.Receive
/- GLM-B: enumerate the verdict wire-name tables; report duplicates across and within. -/
#eval s!"refusalNames.length = {refusalNames.length}, rejectNames.length = {rejectNames.length}"
#eval s!"shared names (refusal ∩ reject): {(refusalNames.filter (rejectNames.contains ·)).toString}"
#eval s!"every duplicate (across and within): {(((refusalNames ++ rejectNames).filter (fun n => (refusalNames ++ rejectNames).count n > 1)).eraseDups).toString}"
#eval s!"all names distinct: {(refusalNames ++ rejectNames).eraseDups.length == (refusalNames ++ rejectNames).length}"
