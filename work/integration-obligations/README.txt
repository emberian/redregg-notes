INTEGRATION OBLIGATIONS — private operational extension of existing cluster boards
Each lieutenant owns ONE JSON file (runtime.json/product.json/protocol.json),
not a second product issue tracker. Link existing project task IDs when known.
Track unfinished capability joins, not one row per file or every trivial edit.

Format: {"updated_at":"UTC timestamp", "obligations":[{...}]}
Each row needs id, outcome, owner, consumer, coordinator, state, next_action,
acceptance and progress_evidence (all nonempty). Agent names use exact short tool
names. States: building, waiting, ready, receiving, integrated. A completed agent
turn does not change the obligation state.
Optional waits_for array has owner, deliverable, next_action, ready(bool), evidence
(required when ready). A waiting dependency must have a real builder, not a queue
or unassigned concept. Distinguish authored/compiled/executed/integrated evidence.
Closing integrated requires receiving_evidence and consumer_ack:{owner,evidence}.
The consumer must actually acknowledge use; compiler PASS/source publication alone
cannot close an obligation that promises a native effect or user journey.

On producer completion, update readiness and immediately followup_task the stopped
consumer/owner with exact artifact + next action. When an owner finishes a turn,
retain its unfinished rows and named producer callbacks. Each lieutenant sweeps
on substantive producer events and root's periodic44minute check. Reentry reads
this audit alongside current live tools. Do not make sweeps a new approval queue.

Run sweep.py --inactive NAME (repeat for agents confirmed inactive by a CURRENT
collaboration.list_agents call). It reports stranded ready work, sleeping needed
producers, incomplete records and unsupported closures. It neither polls processes
nor calls collaboration tools; the coordinating agent must act on its output.
A recorded job PID/log/lock is not liveness. Check the process/tool handle now;
use a unique attempt ID/log/status and distinguish accepted, running and terminal.
No automatic work spawning, builds, destructive action or completion claims.
