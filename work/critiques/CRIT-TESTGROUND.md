# CRIT-TESTGROUND

2026-10-27. Outside review by Codex.

The testground demonstrates outcomes without giving the visitor a reliable way to produce or explain them.
The missing connection is command → arguments → package method → proposed changes → permission and law checks → committed state.
Renaming the windows will not supply that connection.
Adding five separate tools will not supply it either.

The hosted tutorial and demo buttons are broken in the public deployment I tested.
The local examples run, but their displayed commands are not faithful instructions for reproducing those examples.
These defects take priority over another round of prose polishing.

## What I used and what this report establishes

I used [the public local page](https://emberian.github.io/nanodregg/) in Chromium 151.0.7922.34 through `/Users/ember/tools/playwright/node_modules/playwright`.
I also used [the public hosted page](https://emberian.github.io/nanodregg/?hosted=wss://nano.demo.dregg.online/ws&join).
The primary viewport was 1440 × 1000.
I checked the layout at 1024 × 768 as well.
The browser script ran in memory through a persistent Node process.
The screenshots are beside this file.
No repository was edited.
No build was run.

I read WORK-RULES-20261027.md, CHARTER.md on hbox, DESIGN-TESTGROUND.md, and TESTGROUND.report.md.
The report available during this review ended with the 0d72c078 publication and open follow-up work.
It contained no TESTGROUND-5 entry.
The design contained no inspector/editor/REPL/Turn-view/tutorial revision.
The plan critique below evaluates the five-part plan stated in the review brief.
It does not attribute an implementation order or unrecorded details to the building lane.

I made the browser observations before inspecting the public `testground.js`.
I then read that served JavaScript to identify causes of the observed UI failures.
The report's publication hash is a report claim.
I did not independently establish the deployed bundle's source commit.

This is one reviewer's newcomer walkthrough.
It is not a user study.
The ten-minute assessment below is a teaching judgment based on the actions recorded here.

| Surface | Actions exercised | Result |
|---|---|---|
| Desktop | All six icons; single click and double click; task buttons; the nanodregg button; minimize; close; restore; titlebar drag | Icons require double click. The nanodregg button opens World properties. Reopening a member through its icon clears its terminal transcript. |
| Local tour | All nine Run steps | Create, write, describe, grant, stale write, altered log, generator, meter, and time lock ran. |
| Local free typing | `help`; invalid `write`; unquoted and quoted text; unquoted and quoted record arguments; Bob's write without a grant; command-history arrows | `help` returns `unknownVerb`. Quoting changes failure into success. The printed transcript removes that distinction. |
| Objects | Data ID; grant ID; package ID; object self-link; write link; method links; Terms; compiled-code disclosure | Data values are visible. Grants and packages are routed into the wrong inspector. Compiled-code disclosure opens hexadecimal bytes. |
| Document methods | All eleven `invoke…` links | Each fills an object ID and numeric method index. None fills a valid argument example. |
| Frames | Frame rows; slider; Terms; lying-frame link | Selection changes metadata. It does not expose the changed field, rule, or object-state difference. |
| Local writer controls | Every option; both cold-reset buttons; every scene button | Seven scenes reached their displayed expected outcomes. Dropping a call produced `open` inside a window titled Refusal. |
| Local Demos | All four examples; generator repeated | First runs completed. Repeating the generator stopped at `idTaken`. |
| World lifecycle | New World; Join a hosted World prompt; Local World from hosted mode | New World discards the local session. It does not reset completed tour progress. Local World leaves the hosted query string in the address bar. |
| Hosted basic use | Join; create; quoted write; read; grant to a second browser tab; write through that grant; read from the first tab | The first tab read `0=second tab` after the second tab wrote it. |
| Hosted teaching UI | All icons; Start here; repeated first tour step; all four demo buttons | Tour never advanced. All four demo buttons raised the same missing-member JavaScript exception. |
| Hosted relay | Every option selected; reset; altered-log sync; restore honest mode | Altered-log sync returned `eventMismatch`. Normal writes worked after honest mode was restored. |
| Hosted fork check | Empty address; the provided live relay address | Empty input produced a JSON parse error in the terminal. Comparing the relay with itself returned `shared 12`. No second public fork endpoint was supplied. |

Repeated generated IDs were sampled by kind.
I did not click every hash fragment of every serialized value.
I read the dialogs produced by these paths.
I did not manufacture every possible kernel refusal.
The hosted failures prevented completing its advertised tour and demos.

## What a newcomer understands after ten minutes

The visitor can learn that Alice and Bob act on shared state.
The visitor can learn that an object has an owner.
The visitor can learn that a grant lets another member perform an operation.
The visitor can learn that a write can fail when someone else changes the expected state first.
The visitor can learn that the browser checks data received from the writer.
The visitor can see a deliberately altered log rejected.
The visitor can repeat the labels `stale`, `lawDenied`, and `eventMismatch`.

The visitor cannot derive a valid method call from the displayed type without guessing the terminal's quoting rules.
The visitor cannot inspect the grant that makes Bob's call legal.
The visitor cannot open the source behind a package link.
The visitor cannot find the predicate behind `law bounded`.
The visitor cannot distinguish the source-language term from the shell argument that carries it.
The visitor cannot trace a method's return value into the state change it requests.
The visitor cannot see the expected and actual states involved in the stale write.
The visitor cannot explain which part of a Turn the follower recalculated.
The visitor cannot tell which guarantees come from kernel checks and which conditions come from the example package.
The visitor cannot tell when the tick budget resets.
The visitor cannot infer persistence from the desktop metaphor.
The visitor cannot discover a complete object inventory from the current interface.

The generator is introduced before the visitor has authored an ordinary package.
That reverses the dependency between the lessons.
The document example introduces candidates, supports, holes, relations, pins, revocation, and rejudging before showing the method that implements any of them.
The time-lock example introduces another World before the first World's state transition is inspectable.
The examples expose the system's range before they establish its language.

The initial page already has Terms disclosures and substantially plainer prose than the owner's quoted complaint describes.
The current failure is not mainly excessive articles.
It is the substitution of explanatory labels for manipulable causes.

## Reproducible defects that obstruct learning

**The examples teach a command spelling that fails when typed.**

Click `write a slot…` on a data object.
Append `my own text`.
The command returns `refused usage`.
Wrap the text in quotes.
The command succeeds.

```text
write OBJ 0 my own text       → refused usage
write OBJ 0 "my own text"     → ok
```

The same problem occurs with the bounded object's method.
Click `invoke…` beside `set`.
Append `(record (n 75))`.
The command returns `refused usage`.
Quote the entire record argument.
The command succeeds.

```text
invoke OBJ 0 (record (n 75))       → refused usage
invoke OBJ 0 "(record (n 75))"     → ok
```

Both versions print the same command text in the transcript.
The public `runOne` joins parsed arguments with spaces.
It also truncates arguments longer than 40 characters.
The learner cannot copy the displayed program and reproduce its result.
The source-language expression is being confused with command-line tokenization.
The solution needs a faithful command renderer and a valid argument example at every prefill.
A synonym for `invoke` does not fix this.

**Links promise the wrong kind of inspection.**

The grant created by the tour opens a window with `refused wrongKind` in both the description and state areas.
That window still offers `write a slot…`.
The generated package link opens `refused wrongKind` above `refused malformedCell`.
That window also offers `write a slot…`.
The program makes its own broken navigation look like the learner's invalid action.
The public `linkify` routes unrecognized 64-character hexadecimal fragments to `openObject`.
It also turns chain and root hashes into object links.
A hexadecimal width is not a type.

See [the package-link failure](CRIT-TESTGROUND-local-package-link.png).

**The apparent source disclosure contains no source.**

The bounded inspector shows `1442 bytes (the package code invoke runs)`.
Expanding it shows hexadecimal compiled code.
The `bounded` law is a name without a link.
The method row offers a prefill link without an implementation link.
The `source` field names the read command used to populate the window.
It does not name the package source.

See [the expanded compiled bytes](CRIT-TESTGROUND-local-core-bytes.png).

**The tour mistakes attempted syntax for completed learning.**

On a fresh page, run Create.
Type `write` with no arguments.
The terminal returns `refused usage`.
The tour marks the write step done and offers Read.
The served `tourCheck` accepts every exit other than `client` when the verb matches.
A failed write is therefore counted as a completed write lesson.
After finishing the tour, New World creates fresh state but leaves the tour finished.
The served `newWorld` does not reset `tourAt`.

See [the failed step counted as done](CRIT-TESTGROUND-local-failed-step.png) and [the finished tour after reset](CRIT-TESTGROUND-local-reset-tour.png).

**The desktop destroys the history needed to learn.**

Double-clicking the Alice icon replaces the existing Alice terminal's body.
Its transcript disappears.
Its command history disappears.
The World remains.
This happens without pressing New World.
The served `openTerm` constructs new output and history for every icon activation.
Reopening a window must recover the working context.
It must not silently erase the evidence of earlier actions.

**Hosted mode exposes the local tutorial without the local actors.**

The first hosted terminal says `You are you, founder 0, member undefined`.
The membership ID appears later in enrollment output.
The introductory sentence remains wrong until the terminal is recreated.
The Alice icon opens the terminal named `you`.
The Bob icon does nothing.
Start here says `One World, two members (alice, bob), all in this tab`.
The first Run button executes `you$ nd create`.
It never advances.
Repeated clicks create more objects.
The served `tourCheck` explicitly excludes hosted Worlds.

All four hosted demo buttons raise `Cannot read properties of undefined (reading 'name')`.
The time-lock example first creates Carol's local World and gets a receipt.
It then fails when the sequence needs the missing local actor.
There is no visible explanation of the missing participant.
The normal hosted create/write/read path works.
The guided UI is what fails.

See [hosted arrival](CRIT-TESTGROUND-hosted-initial.png), [hosted tour](CRIT-TESTGROUND-hosted-tour.png), and [hosted demos](CRIT-TESTGROUND-hosted-demos.png).

**The status UI makes false statements about the trust boundary.**

After the hosted relay alters a log page, the sync refusal says `nothing: your follow refused the call before signing, so nothing was sent`.
The Frames window contains the log request and response for that same operation.
The dialog confuses “no mutating call submitted” with “no message sent.”
The hosted tray says `writer: LYING (flipEvent)` while the experiment changes the relay's response.
The local scene dialog also attributes relay mutations to the writer.
The distinction matters because the experiment is supposed to teach where verification happens.

See [the hosted contradiction](CRIT-TESTGROUND-hosted-lie.png).

**An unresolved call is presented as a refusal.**

Choose `drops the call (a loss, not a lie)`.
Type `create`.
The result is `open`.
The page displays it with a red cross in a window titled Refusal.
There is no explanation of the unresolved attempt or a next action.
A page about checked outcomes must keep pending, rejected, and confirmed outcomes visually distinct.

See [the dropped call](CRIT-TESTGROUND-local-dropped-call.png).

**The fork control is an address field without an experiment.**

Check attestation accepts an empty address.
It prints `Unexpected token '<'` from a failed JSON parse.
The supplied relay compared with itself returns a shared history.
The surrounding prose still describes “the other writer.”
The page gives the visitor no alternate endpoint with a fork to inspect.
The visitor can operate the button without performing the advertised lesson.

**Demos are not restartable lessons.**

Run Generator twice.
The second run stops at `idTaken`.
The page gives no direct way to reuse the installed example or restart just that example.
The first run's completion line says `every step as expected`.
The learner's next experiment then requires repairing the demo's setup.
The completed tour's New World suggestion also leaves the tour completed.

## Outcomes whose causes are missing

| Outcome shown | Cause the visitor needs to see | Required connection |
|---|---|---|
| `create` returns an ID | Kind, initial slots or typed state, owner, package | Open the created entity beside the exact command. Distinguish a data object from a package instance. |
| A write returns a transaction hash | Old slot value and proposed new value | Show `slot 0: old → new` beside the write. |
| Bob can write through a grant | Target, issuer, grantee, rights, parent, live/revoked state | The grant ID must open the grant. Show the path used for this call. |
| Bob gets `noGrant` | Which required right is absent | Identify the object and operation. Offer a correctly formed command using an available grant when one exists. |
| Bob gets `stale` | His signed expectation and Alice's intervening update | Show expected pin, actual pin, and the changed value together. Keep the retry beside that comparison. |
| `install` returns a package ID | The complete package text and its imports | Open source at the returned package. Preserve the exact submitted text. |
| `create --pkg` succeeds | Declared state type and the supplied initial value | Pair the type with the value. Explain the relationship to the installed package. |
| `invoke` returns success | Selected method, arguments, method body, requested effects | Link the method name to source. Show effects before and after admission. |
| Generator returns a package ID | Generator source and generated package source | Put input `max = 100` beside the generated predicate. Show both programs. |
| `lawDenied bounded` | Actual law expression and evaluated inputs | Show old `n`, proposed `n = 101`, bound `100`, and the false comparison. Link the check to the law. |
| Document candidate becomes verified | Proposed text, support references, checking method | Render the candidate and support rows as records. Link each support to its grant or object. |
| Candidate becomes suspended | Revoked grant and the explicit rejudge call | Show the dependency path. Show that method 5 ran after revocation. Do not imply automatic recomputation from the label alone. |
| Selecting suspended text returns `program` | Failing branch in `select` | Show `support0`, its target, and its revoked status beside the source branch. |
| Meter reaches `ticksBudget` | Cost of the attempted call, remaining budget, reset boundary | The observed count was 2,080,232 of 2,097,152. Explain why the next call does not fit. Define the budget window. |
| Time lock returns `early` | Receipt height and deadline | Display the comparison as numbers. Keep the receipt and lock visible together. |
| Time lock returns `headMismatch` | Receipt's head and the recorded trusted head | Highlight the differing field. Link the head object's rule that accepts its replacement. |
| Time lock releases or returns `settled` | Previous released flag and the law preventing a second release | Display the state change and the specific law branch. |
| Log corruption returns `eventMismatch` | Original event, altered event, and recomputed event | Highlight the changed field or byte. Identify the component doing the comparison. |
| Missing event returns `chainMismatch` | Expected history and received page | Mark the omitted entry. Show the two chain results. |
| False refusal is ignored | Writer response versus verified committed Turn | Present both claims beside the final local decision. |
| Cancel lie stays open | Request, claimed cancellation, and checked attempt state | Explain why neither success nor cancellation has been established. |
| Forged cancel is rejected | Purported signer and failed signature check | Link the rejected cancellation to the original request. |
| `forkedPost` | Posted historical head and the locally known head at that position | Show both histories at the comparison point. |
| `shared 12` or `forkedWorld` | Both origins, both positions, both chain hashes | Explain whether the comparison used another endpoint or the same endpoint. |
| Any verified result | Specific property checked and its implementation | Offer a separate reference from the result to the check and relevant theorem. State what that theorem covers. |

The Frames slider currently scrubs messages.
It does not rewind the World shown in an object window.
The slider needs to say that explicitly until a historical state view exists.
A timeline that changes only message metadata is not a Turn inspector.

## Copy to replace

These are the redundant, opaque, misleading, or decorative strings I found on the exercised paths.
The table includes necessary technical terms whose current presentation fails to explain their role.
The protocol names should remain available as exact diagnostic details.
They should not be the only instruction.
Quoted examples below retain the current capitalization.

| Current text | Plain replacement or disposition |
|---|---|
| `Start here` | `Create and change an object` |
| `World` on the initial properties window | `Local World` |
| `◆ nanodregg` as a button that opens properties | `World settings` |
| `Frames` | `Messages` |
| `Terms` | `What these fields mean` |
| `New World (genesis)` | `Reset local World` |
| `Local World` as the hosted exit button | `Start a local World` |
| `Join a hosted World…` | `Join the demo server…` with the supplied demo address filled in |
| `Relay address (wss://…/ws):` | `Demo server address:` |
| `runs in: this tab: one writer, one follow per member` | `Runs here. Alice and Bob each check the writer's log.` |
| `origin` | `World ID` with `origin` in details |
| `nonce` | `Random value used to create this World` in details |
| `founder 0`, `founder 1` | `Initial members: Alice, Bob` with indexes in details |
| `chain` | `History hash` |
| `chain0, roots0` | `Initial history and state hashes` in details |
| `authority 0 0` | `No head certifiers configured` |
| `kernel load`, `genesis` timing rows | Move to `Performance details`. They do not help the first action. |
| `Random bytes in the genesis input, so two Worlds never share an origin.` | `This random value distinguishes a newly created World. Copies of the same genesis keep its World ID.` |
| `You are alice, founder 0, member …` | `Acting as Alice` with the member ID in identity details |
| `You are you, founder 0, member undefined.` | `Joining the demo server…` followed by `Connected as member …` after enrollment |
| `Your keys stay in this tab.` | `This tab holds your signing keys.` Add the actual reload and persistence behavior beside it. |
| `Your follow (your copy of the World) checks each command before your key signs it.` | `Your local checker validates a call before signing it.` Link `local checker` to its state and checks. |
| `write OBJ SLOT TEXT` | `write OBJECT SLOT "TEXT"` with a runnable example |
| `invoke OBJ N ARGS` | `invoke OBJECT METHOD "ARGUMENT"` with a valid example for the selected method |
| `install TEXT` | `Install package source…` opening a source editor |
| `write a slot…` | `Change slot…` opening a slot/value form |
| `invoke…` | `Call set…`, `Call generate…`, or the actual method name |
| `source: alice's follow: read … ?` | `Viewed as: Alice` plus `Copy inspect command` |
| `updated: after every command` | Show the actual checked position or refresh time. Remove this repeated promise. |
| `state` used for both the declaration and value | `State type` and `Current state` |
| `data` | `Data object: numbered slots` |
| `core` | `Compiled bytes` under advanced details |
| `1442 bytes (the package code invoke runs)` | `Compiled package: 1,442 bytes` alongside a separate `View source` action |
| `method 0 set (rec (n nat))` | `set(n: natural number)` with the exact signature beside an example argument |
| `call 0 0 (sum (install (rec (pkg bytes))))` | `generate may install a package` with the exact effect signature in details |
| `law bounded` | `Rule: n must be at most 100` linked to the actual law expression |
| `rel` followed by a serialized declaration | `Table: candidates`, `Table: facts`, or the actual relation name with visible rows |
| `installs a n-bounded record at the bound its argument names` | `Creates a package whose n field cannot exceed max.` |
| `Document section with a hole` | `Choose a proposed paragraph` |
| `Generator: a package that installs a package` | `Generate a package with a number limit` |
| `Meter: ticks per member` | `Run out of computation budget` |
| `Time lock on another World's height` | `Release a lock after another World reaches step 3` using the actual deadline |
| `14 commands`, `7 commands`, `3 commands`, `17 commands` | Show actual step progress during execution. The meter label hides its repeated calls. |
| `Each demo types ordinary nd commands into the terminals, on the current World.` | `Examples change this World.` Add `Restart this example` and `Copy exact command` actions. |
| `demo …: every step as expected` | `Example complete` plus the concrete final state and a suggested change to try |
| `a light on the rock` | `Bob's proposed paragraph` for the introductory example |
| `support0 dead` | `Support 0 is revoked: Bob's grant …` with a link to that grant |
| `reset follow (cold)` | `Discard local state and recheck the log` |
| `The writer runs unmodified. Every follow checks what it serves in any case.` | `Fault injection is off.` |
| `The relay forwards every frame unchanged. Your follow checks every reply in any case.` | `Fault injection is off.` |
| `The writer is honest` / `The relay is honest` | `Fault injection: off` rather than an assertion about a remote party's honesty |
| `Run a row's scene on a new World:` | `Try a broken writer or relay in a new local World:` |
| `flipEvent` | `Alter a logged event` |
| `dropLastEvent` | `Omit the last event` |
| `forgesRefusal` | `Record the wrong refusal` |
| `lieLookup` | `Lie about a completed call` |
| `lieCancel` | `Claim a call was cancelled` |
| `forgeCancel` | `Forge a cancellation` |
| `forkedPost` | `Post a conflicting history` |
| `drops the call (a loss, not a lie)` | `Drop a submitted call` |
| `Conformance row … (a scripted test in Protocol.Rows), line …, expects: …` | `Expected result: …` with `View regression test` in details |
| `Entries logged during the lie stay in the log after you switch back.` | Use separate text for writer mutation and relay mutation. For a relay: `The writer's stored log is unchanged.` |
| `writer: LYING (flipEvent)` in hosted mode | `Relay fault: altered event` |
| `by the writer: alters an event in the log` for the relay scene | `The relay changed an event in the response.` |
| `LIED` | `Altered response` for a relay mutation |
| `FORGED` | `Submitted without the local check` for the hostile-client scene |
| `Lie caught` | `Altered log rejected`, `Forged cancellation rejected`, or the actual result |
| `Lie without effect` | `Committed call confirmed despite false reply` |
| `Nothing signed depends on it.` | State the observed action: `No new call was signed using the rejected page.` |
| `row expects` / `match yes` | Move to regression-test details. Show the compared values in the main result. |
| `Refusal` over `open` | `Call unresolved` |
| `Declined call` over `stale` | `Object changed before your write arrived` with `stale` as the code |
| `writer's reply: nothing: … so nothing was sent` | `No mutating call was submitted.` Show any log requests separately. |
| `refused usage` without explanation | `Invalid command arguments.` Show the required form and the failing input. |
| `refused unknownVerb` for `help` | `Unknown command. Available commands: …` |
| `wrongKind` inside a package or grant inspector | `This link opened the wrong inspector.` Repair the link rather than exposing this as normal product copy. |
| `lawDenied: a law of the object refused the change. A law compares the old state with the new state.` | `Proposed n = 101 exceeds the limit of 100.` Keep `lawDenied` and the source link. |
| `program: a check inside the method refused. The line above names the check.` | State the actual failed check and link its method branch. |
| `ticksBudget: this member has spent its ticks for this window.` | `This call exceeds the remaining computation budget.` Show attempted cost, remaining budget, and reset boundary. |
| `this window` in the meter | `Budget period …` with its actual bounds. A desktop window is already visible. |
| `exit ok · … ms · … frames · ticks …` after every beginner action | `Applied` followed by the state change. Put timing, traffic, and ticks in expandable details. |
| `guest-book` | `Enrollment service` |
| `Fork check` | `Compare histories` |
| `Check attestation` | `Compare signed history` |
| `ws://…/ws (another writer, same genesis)` | `Second server address` with a working demonstration endpoint or an explicit setup instruction |
| `A signed head (attestation) from the other writer shows a fork: refused forkedWorld.` | `Compare signed histories at the same position. Different hashes reveal a fork.` |
| `No attestation from : Unexpected token '<' …` | `Enter a server address.` Validate empty input before fetching. |
| `OK` on a failed experiment | Use `Edit arguments`, `Inspect rule`, or `Retry` where the action is available. Keep `Close` for dismissal. |

The narrative of the first six tour steps contains real information.
It needs editable examples beside it.
Deleting its articles would not repair the lesson.
Names such as `record`, `sum`, `law`, and `Turn` also carry real information.
They need definitions grounded in the current example.
Replacing all of them with vague everyday words would conceal the language again.

## The net-OS metaphor

The desktop makes identities feel separate.
Separate terminals make Alice's and Bob's authority visible.
Object windows can keep a target visible while a command changes it.
A taskbar can preserve several related investigations.
Those are useful properties for this system.

The present windows do not preserve those properties reliably.
The Tour covers much of World and Frames on arrival.
Object and refusal windows cover the terminal that caused them.
The visitor must manage stacking before comparing cause and effect.
The fixed terminal position extends beyond a 1024-pixel viewport.
The titlebars have no resize control.
The initial five-window arrangement gives equal visual weight to setup hashes and the next useful action.

The desktop also promises capabilities the page does not provide.
An object should be discoverable in a collection rather than only in terminal history.
Reopening a terminal should preserve its transcript.
Closing a window should not erase the only convenient route back to an object.
A change of user should not be represented by a misleading Alice icon in hosted mode.
A reset should visibly reset the lesson.
A desktop should state whether its work survives closing the tab.

Keep the desktop if these promises are fulfilled.
Use a default teaching arrangement with the task, object, source, and result visible together.
Allow the learner to detach those panels into windows after the first successful edit.
The visual style can remain early-2000s.
The mandatory window-management work should disappear.

See [the initial desktop](CRIT-TESTGROUND-local-initial.png), [an inspected object](CRIT-TESTGROUND-local-object.png), and [the smaller viewport](CRIT-TESTGROUND-1024-desktop.png).

## Three teaching environments worth copying

**Scratch: make the first cause visible and editable.**

Scratch's introductory sequence starts with moving a sprite.
It then adds sound, repetition, and further visible behavior.
The learner changes the program responsible for the effect. [Scratch's introductory sequence](https://scratch.mit.edu/help/studio/tips/howto/get-started-intro/).

The equivalent here is a visible field `n = 0`, a visible `set` method, and an editable argument.
The first task should be “make n equal 7.”
The second should be “try 101 and explain why it stays 7.”
The code and law need to stay beside the result.
A generator is a later exercise.

**Python Tutor: connect execution to state.**

Python Tutor shows code execution step by step alongside variables, objects, pointers, and stack frames. [Python Tutor](https://pythontutor.com/).

The equivalent here is a call trace with old state, argument, method result, proposed effects, checks, and new state.
A message counter is not that trace.
The learner should be able to select a rejected effect and see the rule that rejected it.
They should also be able to inspect the unchanged state after rejection.

**Squeak/Smalltalk: make the running object lead to its implementation.**

Squeak provides tools for browsing, writing, and executing code in a live object environment.
Its graphical objects are interactively changeable.
The system's implementation is available for inspection and modification. [Squeak's features](https://squeak.org/features/).

The equivalent here is object → package → method or law → editable source → a new installed package → a new instance.
The current package link ends at `wrongKind`.
The current code disclosure ends at hexadecimal bytes.
Those are the two links to repair before adding more desktop furniture.
The nanodregg editor must explain its own installation and replacement semantics.
It must not imply Smalltalk-style mutation of a content-addressed package.

## Five changes with the highest value per hour

These are reviewer estimates for scoped UI work.
They are not measurements of the lane's implementation effort.
They exclude new kernel introspection APIs.

| Order | Change | Initial slice | Estimated effort | Completion test |
|---|---|---|---|---|
| 1 | Make displayed commands executable | Preserve input text and full argv; render quoting correctly; fill a valid example argument; add command help and useful usage errors | 2–4 hours | Copy the displayed write and method call into the terminal. Change only the value. Both run. |
| 2 | Make the existing lesson state trustworthy | Preserve terminal history on reopen; reset tour progress with New World; advance steps only on the intended result; offer per-example restart | 2–4 hours | A failed write does not complete the write lesson. Reset starts at Create. Reopening Alice preserves her transcript. |
| 3 | Give every ID the right destination | Add a session object list; dispatch object/package/grant links by kind; show package source and grant rights; stop treating arbitrary hash fragments as objects | 4–8 hours if read APIs exist | A learner can go from Bob's successful call to its grant and from the target object to its method source. |
| 4 | Build one complete causal lesson | Use the ordinary bounded object; place state, source, argument, rule result, and state difference together; make the argument editable | 4–8 hours if source and checked effects are available | The learner changes 50 to 75, predicts 101's refusal, and identifies the exact law without leaving the example. |
| 5 | Give hosted mode its own working entry path | Correct identity and icons; use actual participants; expose the two-tab grant exercise; fix missing-member dispatch; validate the comparison address | 3–6 hours for basic shared-state teaching | Two fresh tabs complete create → grant → write → read through the UI. Every offered hosted lesson either runs or states the participant it needs. |

The immediate hosted fix must not silently turn an advertised hosted lesson into a local one.
The distinction between a remote writer and a local writer is part of the subject.
The existing successful two-tab path is the right first hosted lesson.
I exercised that path manually.
The first tab read the second tab's new value.
See [the second tab's successful granted write](CRIT-TESTGROUND-hosted-second-tab.png).

## The one thing to delete

Delete automatic modal result dialogs from ordinary learning actions.

Expected refusals are part of the lesson.
The red Refusal window interrupts the experiment and covers its context.
It also mislabels an unresolved call as a refusal.
Put each result beside the command and affected object.
Keep the exact refusal code visible.
Add links to the rule, inputs, and unchanged state.
Reserve an interrupting dialog for a decision the user must make before continuing.
This deletes presentation machinery.
It does not remove a check or suppress a refusal.

## Critique of TESTGROUND-5

The inspector, package editor, term REPL, structured Turn view, and tutorial are the right ingredients.
They are not a sufficient product definition.
Their success depends on shared identity, source location, selected call, and selected state across the five tools.
Five isolated windows would reproduce the existing problem at greater scale.

**Build a usable object-and-code loop first.**

Start with a normal bounded object.
Show its current state.
Show its state type.
Show its method and law source.
Provide a typed argument editor with a valid initial value.
Run the argument through the same command path as a typed invocation.
Display the proposed change and actual outcome beside the source.
Make a refusal preserve the submitted argument for editing.

The inspector must cover grants and packages as well as ordinary objects.
An object-only inspector leaves the existing `wrongKind` dead ends intact.
It must distinguish a declaration from a current value.
It must show which member's checked state is being viewed.
It must show the position of that state when several members disagree or lag.

**Introduce the tutorial with that first loop.**

Do not leave tutorial design until all four tools exist.
Use it to decide the minimum controls those tools need.
Make the learner change a value before explaining generator machinery.
Ask for a prediction before running the rejected value.
Require a repair after the refusal.
Ask the learner to point to the law that caused it.
A sequence of Run buttons tests the harness.
It does not test understanding.

**Attach a small structured result view before building a general Turn browser.**

The minimum useful result is old state, argument, proposed effects, checks, and committed state.
A successful Turn alone is insufficient.
Refused calls and unresolved attempts need first-class records too.
Otherwise the tutorial's most important moments disappear from the new view.

Show the phase of failure.
Distinguish parsing from type checking.
Distinguish local planning from submission.
Distinguish a package rule from a protocol check.
Distinguish an invalid log response from an unresolved network outcome.
The current red modal collapses these distinctions.

Link every displayed check to the method, law, permission, or protocol rule that produced it.
Keep raw Frames available below that view.
Do not make transport messages the default history.

**Add the package editor as a continuation of the inspected source.**

The editor needs a complete runnable example.
It needs imports and their resolved identities.
It needs parse and type errors at source locations.
It needs a clear installation result.
It needs an explicit path from the newly installed package to a new object.
Changing the source must not silently suggest that an existing content-addressed package changed in place.
The learner should change the bound from 100 to 200 and compare the old and new instances.
That experiment teaches package identity, installation, methods, and laws together.

**Put the general term REPL after the first successful package edit.**

A blank REPL is another syntax exam.
The user first needs a small term taken from the object they just understood.
Seed the REPL with that term.
Show its type and value.
Keep evaluation separate from changing the World.
When evaluation produces a description of effects, show those effects before offering execution.
Carry values between the REPL and the invocation editor without manual quoting.

The REPL is useful for learning records, variants, functions, and evaluation.
It does not replace an object browser, an argument editor, or a rule trace.
It does not repair the current command renderer.

**The missing pieces are navigation, repair, and mode-aware lessons.**

The plan needs a persistent session inventory of objects, packages, grants, and calls.
It needs type-aware links between them.
It needs a faithful command copy path.
It needs source locations on errors.
It needs an easy retry with the previous input intact.
It needs progress that tracks the required outcome.
It needs deterministic lesson restart.
It needs visible local-versus-hosted mode.
It needs a two-tab lesson that uses the actual joined members.
It needs to explain what survives reset and reload.

A glossary is support for those mechanisms.
It is not a substitute for them.
A string rewrite should follow the actual role of each field and action.
It should not rename missing behavior into apparent existence.

The recommended implementation order is: repair commands and session behavior; build the bounded-object loop with its tutorial; connect source, grants, and structured results; add package editing; add the term REPL; expand the Turn browser and later lessons.
Hosted onboarding repair belongs beside the first step.
The user-facing criterion is that a stranger can make one new behavior, explain its refusal, and fix it without reading the repository.

## Evidence index and reproduction

The screenshots most useful to the building lane are:

- [Initial local desktop](CRIT-TESTGROUND-local-initial.png).
- [Stale write](CRIT-TESTGROUND-local-stale.png).
- [Data-object window](CRIT-TESTGROUND-local-object.png).
- [Generated object and law refusal](CRIT-TESTGROUND-local-generator-clean.png).
- [Compiled bytes in place of source](CRIT-TESTGROUND-local-core-bytes.png).
- [Package link routed to an object reader](CRIT-TESTGROUND-local-package-link.png).
- [Document methods](CRIT-TESTGROUND-local-document-methods.png).
- [Time-lock result](CRIT-TESTGROUND-local-timelock.png).
- [Frames after scrubbing](CRIT-TESTGROUND-frames.png).
- [Unresolved call labeled Refusal](CRIT-TESTGROUND-local-dropped-call.png).
- [Failed tutorial step counted as done](CRIT-TESTGROUND-local-failed-step.png).
- [Completed tutorial retained after reset](CRIT-TESTGROUND-local-reset-tour.png).
- [Hosted member undefined](CRIT-TESTGROUND-hosted-initial.png).
- [Hosted tour stuck at Create](CRIT-TESTGROUND-hosted-tour.png).
- [Hosted demos after failure](CRIT-TESTGROUND-hosted-demos.png).
- [Hosted relay refusal with incorrect no-message claim](CRIT-TESTGROUND-hosted-lie.png).
- [Second tab writing through a grant](CRIT-TESTGROUND-hosted-second-tab.png).

The seven `CRIT-TESTGROUND-row-*.png` files cover each local adversary scene.
The file named `CRIT-TESTGROUND-local-generator.png` captures the meter result after the generator in the sequential tour.
Use `CRIT-TESTGROUND-local-generator-clean.png` for the generator itself.

This small Playwright script reproduces the most immediate command and hosted-demo failures.
It uses UI actions rather than the page's exported kernel helpers.
It is included here to keep the requested written deliverable to one file.
The full walkthrough also exercised the controls listed above.

```javascript
const { chromium } = require('/Users/ember/tools/playwright/node_modules/playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  const p = await context.newPage();
  await p.goto('https://emberian.github.io/nanodregg/');
  const tour = p.getByRole('dialog', { name: 'Tour', exact: true });
  await tour.getByRole('button', { name: 'Run', exact: true }).click();
  const alice = p.getByRole('dialog', { name: 'alice', exact: true });
  const idLink = alice.locator('a.hex').first();
  await idLink.waitFor();
  const id = await idLink.getAttribute('title');
  await p.locator('#tasks button[title="alice"]').click();
  const input = p.getByRole('textbox', { name: "alice's nd command" });
  await input.fill(`write ${id} 0 my own text`);
  await input.press('Enter');
  await p.getByRole('alertdialog').waitFor();
  console.log(await p.getByRole('alertdialog').innerText());
  await p.getByRole('button', { name: 'OK', exact: true }).click();
  await input.fill(`write ${id} 0 "my own text"`);
  await input.press('Enter');
  await p.waitForTimeout(500);
  console.log(await alice.innerText());
  const h = await context.newPage();
  h.on('pageerror', e => console.log('HOSTED UI ERROR:', e.message));
  await h.goto('https://emberian.github.io/nanodregg/?hosted=wss://nano.demo.dregg.online/ws&join');
  await h.getByRole('dialog', { name: 'you', exact: true }).getByText(/Enrolled\. member/).waitFor();
  await h.locator('#icons button').filter({ hasText: 'Demos' }).dblclick();
  await h.getByRole('dialog', { name: 'Demos', exact: true })
    .getByRole('button', { name: 'Run', exact: true }).first().click();
  await h.waitForTimeout(1000);
  await browser.close();
})();
```

DONE 2026-10-27 — [Critique written](/Users/ember/dev/redregg/work/critiques/CRIT-TESTGROUND.md), with browser evidence from both modes.
No repositories edited. Nothing landed.
