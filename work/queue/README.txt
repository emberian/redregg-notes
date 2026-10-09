MERGE QUEUE (directory form, from 2026-10-07 ~01:00 EDT; replaces the REQUESTS section of MERGE-QUEUE.md)
One file per range: queue/<lane>.txt. The LANE creates it (write it whole, once; to change it, write <lane>.txt again
whole). Only the MERGE-KEEPER edits or moves it afterwards: to queue/landed/ (with the main sha appended) or
queue/ejected/ (with the reason). Then SendMessage the keeper (MERGE-KEEPER, successor of a6ac8c6c; ask the deputies for its id) one line: "queued <lane>".
Contents, one field per line:
  lane: <name>
  source: <box:path or bare repo ref> (and/or bundle hbox:/tank/dregg-build/claude-lanes/bundles/<x>.bundle)
  branch: lane/<x>
  range: <base>..<tip>   (base = the `next` you built on; pick list if not the whole range)
  what: <one paragraph: what changes>
  evidence: <compiled/executed/plants, with log paths>
  breaks: <shape changes, what re-emits / re-genesis, what refuses>
  notes: <landing order, conflicts, "fixture/pin red only from <epoch bump>">
Train (Ember, 01:45): arrival is rebased onto `next` at once and `next` is PUBLISHED on the shared remote burst2-a:/srv/git/minidregg.git (authoritative since 10-07 16:58Z; GitHub is a mirror).
Lanes build on `next`. main fast-forwards to the newest gate-green next tip. A red range is ejected with a message to its owner.
The history stays in MERGE-QUEUE.md ## LOG.
