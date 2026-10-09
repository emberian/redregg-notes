# kern-pole — the OB totality pole runner (R0 part (c), train `kern`)

You are a Codex worker (gpt-6.1-sol) on the Mini repo, lane at 546c1c88. Deputy: DEPUTY-KERNEL (Claude).
A sibling astra worker `kern-r0` is, in its own lane, (a) pinning a deployed `History` as
`DeployedHistory.history` (new file Kernel/DeployedHistory.lean) and (b) adding a `Turn.absent` guard kind
so `Turn.ofIntent` stops refusing `guardOnAbsent`. You build the EXECUTABLE pole that measures whether
every recorded Objective Bend (OB) intent derives a kernel turn.

## The check (from kern-r0, verbatim)
For each recorded OB commit, BEFORE it is applied, on the durable state it was admitted against:
`Kernel.HostRefinesWorld.Turn.ofLoaded DeployedBridge.bridge DeployedHistory.history opened.durable verdict.intent`
must be `.ok _`. Print one line per intent: `<row> <idx> ok` or `<row> <idx> refusal <Refusal>`; then per-row
counts and a final `TOTAL n ok k refused m`. Rows: `activity`, `objectrecord`, `call`, `send`, `seats`,
`domain`, `upgrade` (docs/OBJECTIVE-BEND.md:529-537; scripts under scripts/pipeline/, journey-rows).
Every row must report a NONZERO intent count, or the run fails (an empty run must never read as green).
Exit code: 0 iff every intent ok and every row nonzero.

## FIRST: read, then paste the real signatures into WORKLOG.md
`Turn.ofLoaded` (Kernel/HostRefinesWorld.lean:410), `TurnOfIntent.Refusal` (Kernel/TurnOfIntent.lean ~:540),
`DeployedBridge.bridge`, the OB receiver's `Verdict`/`Prepared.intent` (Kernel/ObjectiveActivityReceiver.lean
~:1255), `NativeHostReplay.NativeAdmission` (Kernel/NativeHostReplay.lean ~:1095) and the replay/advance entry
that re-admits recorded commits, and how the journey scripts record their run (durable log / store files).
Then decide HOW to get the intents: preferred = replay the durable log a journey leaves behind through the
Host's own replay (NativeHostReplay), calling the check at each OB admission; acceptable = re-run the
journey's commands through the receiver in-process. Say which in WORKLOG with the reason, before coding.

## Shape
- `Kernel/ObjectiveTurnTotalityRunner.lean` (+ a `lean_exe` entry in lakefile.lean, exe entry ONLY), generic
  over `H : History …` in its core function; `main` instantiates `DeployedHistory.history`. Until kern-r0's
  file exists in your lane, write `main` against a clearly named local `abbrev` you will replace; NEVER use a
  history whose `legBytes`/`imageBytes` are `fun _ => 0` in the final. The deputy will merge kern-r0's lane
  into yours when DeployedHistory lands (you'll get a message); then switch `main` to it.
- A driver script under `scripts/kern/` (new dir; NOT scripts/pipeline, which another train owns — read it,
  never edit it) that runs the journeys' recorded artifacts (or produces them with the journey scripts as
  they are, invoked read-only) and then the exe. Run it with `request_journey`; `{bin}`/`{manifest}` expand
  to the prebuilt base artifacts; if you changed Host, request_build it and pass your own path.
- At the base (no `absent`), the expected result is RED on `objectrecord` wherever a `create` has no seed
  (`Refusal.guardOnAbsent`), and on `domain` if any member is stateless. Record that red output verbatim in
  WORKLOG — it is the plant evidence. If a row shows NO seedless create / stateless member, say so plainly.

## Rules
- Files you may edit: Kernel/ObjectiveTurnTotalityRunner.lean, lakefile.lean (one lean_exe entry),
  scripts/kern/*. Need another? ask_deputy.
- No `| tail`, no `|| true`, no `pkill -f`, no fixed /tmp paths (use a per-run dir under the lane).
- Builds/runs ONLY via request_build / request_journey; end your turn after each request; never poll.
- Submit with the umbrella green. In the note: the method, the per-row counts, the red output at base.
