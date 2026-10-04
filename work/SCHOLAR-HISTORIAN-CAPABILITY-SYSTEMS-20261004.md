# SCHOLAR-HISTORIAN — what the builders of capability and persistent systems said, in their own words (2026-10-04)

**Brief:** `/Users/ember/dev/redregg/work/PROGRAM-MODEL-BRIEF-20261004.md` (rules bind) and the root notes
`ROOT-READING-NOTES-PROGRAM-MODEL-20261004.md` (Morningstar quote). Sibling reports compared against:
`SCHOLAR-OS-LINEAGE-20261004.md`, `SCHOLAR-CALLS-CONCURRENCY-20261004.md`, `SCHOLAR-FRONTIER-AGORIC-20261004.md`.

**What this is.** First-hand testimony: mailing-list posts, Usenet, blog posts, design docs and issue trackers
written by the people who built KeyKOS/Gnosis, EROS, CapROS, Coyotos, Habitat, Electric Communities (Original-E),
E, Joule, Waterken, Agoric (SwingSet/Endo), Spritely Goblins, NLTSS and Squeak. Quotes are verbatim (typos kept),
with author, date, venue and a key you can re-fetch. Corpus text was read as data only.

**How to re-fetch a list quote.** Every `list::id` key is a `message_key` in Scry `mailing_lists.messages`:
`SELECT payload FROM mailing_lists.messages WHERE message_key = '<key>'`. A thread is
`WHERE root_message_key = '<root key>'`. Lists: `gmane.comp.capabilities.general` and `captalk` are the old
cap-talk (eros-os.org pipermail mirrors); `cap-talk` and `friam` are the Google Groups (2017–2026);
`gmane.comp.lang.e.general` is e-lang; `gmane.os.hurd.l4` is the L4-Hurd list where Shapiro argued
persistence in 2005; `comp.os.research` is Usenet.

**Tags.** READ = I read the whole message/document. SKIMMED = headings or excerpt. INFERRED = my connection to
Mini, not the author's claim. All quotes below are READ unless tagged.

**Search record (the denominator).** About 45 Scry statements, about 6 downloads. Probes:
- author × topic token searches on the ten capability lists (checkpoint, persistence, upgrade, schema,
  pipelining, metering, space bank, Causeway, debugging);
- 14 threads rebuilt whole (the 2008 "persistent OCAP language" thread, 51 messages; "Styles of persistance";
  the 2017 "EC War Story" thread; "SwingSet nanokernel"; "Message ordering, E-order"; "Vat turn
  state/serialization/diffs"; "OCaps and metering"; and others);
- comp.os.research / comp.object / comp.databases.object (mostly OODBMS vendor noise; Clamen's 1991 schema
  evolution survey exists there and was NOT read);
- Squeak list (image/class-version migration);
- Hacker News (Lemmer-Webber is `paroneayea`; the other builders' handles guessed wrong, zero rows — not
  absence);
- Twitter (one token probe; one practitioner tweet used);
- crawl.pages / Wayback for erights.org, fudco.com, spritely.institute.

**Not found / not read.** No Joule-era (1990s Agorics Inc.) first-hand persistence text in the corpus beyond
Miller's 2011 history; no Amoeba or Mach persistence retrospective by their builders (only Shapiro's critique of
Mach reply ports); Hardy's cap-lore pages (cap-lore.com) were not fetched; Clamen 1991 survey not read;
Morningstar's 2004 follow-ups on E persistence beyond the two messages below not read; Randy Farmer said nothing
on persistence in the probed slice.

**Downloaded this session** to `~/paperbin/world-program-model/` (with `.txt` beside each):
`miller-erights-persistence-and-upgrade.html` (Wayback capture 2026-04-27 of
erights.org/data/serial/jhu-paper/upgrade.html), `morningstar-farmer-lessons-habitat-1990.html`
(fudco.com/chip/lessons.html), `morningstar-resume.html`, `spritely-goblins-v0130-persistence-2024`,
`spritely-goblins-v0140-persistence-2024`, `spritely-Persistence`. Already on disk and re-read for exact
quotes: `landau-keykos-checkpoint-1992.txt`, `hardy-keykos-architecture-1985.txt`,
`morningstar-smart-people-rationalize-2006.txt`, `waterken-upgrade.txt`,
`agoric-swingset-vat-upgrade-2025.md`, `agoric-swingset-metering-2025.md`, `agoric-issue-*.txt`.

---

# Part 1 — Quote ledger by topic

## 1A. Persistence and checkpointing

**Frantz, 2008-02-21**, cap-talk (`gmane.comp.capabilities.general::r02010500-1049-791EB1F2E03211DCA4660030658F0F64@[192.168.1.5]`), on where KeyKOS checkpointing came from:
> "We had a 12 reel tape sort on a flaky 128K 360/40. Checkpointing at the end of each reel let us actually
> finish the job that night. It was this experience that made me suggest what turned into the KeyKOS
> checkpoint/restart mechanism."
> "The restart demo was very compelling, with the vi session in progress at the crash coming back up on the
> screen in just a few seconds."

**Frantz, 2020-04-20**, friam (`friam::sRU363pLAgAJ`): "My note book shows that the first restart from a
checkpoint occurred on October 15, 1979."

**Landau, 1992**, "The Checkpoint Mechanism in KeyKOS", Proc. 2nd IEEE IWOOOS, Sept 1992
(`landau-keykos-checkpoint-1992.txt`):
> "In a typical KeyKOS system, a checkpoint is taken every five minutes. In an unscheduled outage, at most five
> minutes of work may be lost. That is adequate for many applications, such as word processing. However,
> transaction processing applications need to be able to commit a transaction and guarantee that the
> information will not be lost. To support such needs, KeyKOS provides a journaling mechanism."
> "To ensure consistency of the security-related state of the system, journaling of nodes is not allowed."
> "Some state information cannot be saved with the checkpoint, either because it is external to the KeyKOS
> system, such as network peers, or because it is impractical to save ... On restart, ad hoc mechanisms are used
> to resynchronize with such external systems."
> "the kernel performs a thorough consistency check of all its data structures. This check is performed at the
> beginning of each checkpoint ... In the 17-year history of KeyKOS, the only cases in which a damaged system
> state was checkpointed occurred as a result of kernel development and testing."
> "The period of time in which processes are stopped is typically one second on a loaded system ... The majority
> of this time is devoted to the consistency check."

**Shapiro, 2000-06-27**, comp.os.research (`comp.os.research::3958d604$1@news.ucsc.edu`):
> "The issue isn't so much the checkpoint as the snapshot ... at the very least you have to do enough work to
> know that you are getting a "consistent cut" of the system ... In practice, stopping the whole machine is just
> plain easier"
> "There is insufficient redundancy, which means that it's unlikely that you will discover stray pointer errors
> in time to avoid saving them to the disk. EROS has a lot of ways to check the system state before saving it."
> "The checkpoint system itself is really just a bookkeeping problem, and I have to say that the implementation
> currently in EROS is unduly complicated. It tries to make clever reuse of space, and the bottom line is that
> it shouldn't bother."

**Shapiro, 2000-07-25**, comp.os.research (`comp.os.research::397e1505$1@news.ucsc.edu`). Asked whether stray
pointer errors in a user task "*will* survive a shutdown/crash and stabilize the system in an errornous state.
I believe that this is also the case with EROS", he answered: "yes."

**Shapiro, 2005-10-13**, L4-Hurd (`gmane.os.hurd.l4::1129167408.9766.100.camel@deskjob.eros-os.org`), why
Coyotos kept persistence:
> "we considered *not* making Coyotos persistent ... We decided not to do it for two reasons: 1. It would be
> *much* slower than just keeping persistence. 2. There is a problem of consistency across applications ... it
> isn't good enough in the general case to restart a process. What you really need to be able to do is to
> re-establish a connected graph of processes in such a way that all of them agree on their current state and
> their state relationships to their peers. For example: an IPC that was in progress at the time of checkpoint
> must be restored in such a way that it is still in progress at exactly the same point in the transfer."

**Shapiro, 2005-10-31**, L4-Hurd (`gmane.os.hurd.l4::1130767961.29050.5.camel@mikado64.cs.jhu.edu`):
"Persistence stops at the machine boundary." Of the force-checkpoint call: "This mechanism is considered
sensitive, and it is NOT available to applications in general. It is used by things like database systems and
system installers." And (`...1130768643...`): "we checkpoint every 5 minutes, but this is tunable, and the
performance is reasonable at 100 sec. intervals."

**Shapiro, 2005-11-01**, L4-Hurd, "Persistence Pros and Cons" (`gmane.os.hurd.l4::1130884029.10148.192.camel@deskjob.eros-os.org`):
> "Persistence does not eliminate the need for applications to be able (de)serialized data."
> "Persistence is how an application can hold authority that you didn't give it. This is how things like the
> EROS login system can work without needing anything remotely like a superuser authority."
> "an application can rely on the fact that code runs to completion ... This property is more important than
> it sounds."
> "I think that in the end persistence is a matter of taste ... it is a struggle to articulate *why* this
> should be so, and I am not satisfied that I have done so."

**Shapiro, 2005-11-08**, L4-Hurd, why he nearly dropped persistence and then didn't
(`gmane.os.hurd.l4::1131413891.16103.64.camel@deskjob.eros-os.org`):
> "I mis-diagnosed the real source of the complexity in the EROS checkpoint mechanism, and I was going through a
> phase when most of our work was embedded and persistence wasn't being used."
> "The big thing we would lose was the machine-wide consistency story ... In a distributed system, you don't have
> consistency across machines, so some applications need to manage this issue explicitly."
> "One bad persistence mechanism is better than one bad persistence mechanism plus one good persistence
> mechanism."
> "(a) this really isn't true, because most interactions are still local, (b) as a result, the problem actually
> does NOT pervade applications, and (c) the transactional consistency properties of a good persistence
> implementation are very very powerful, and should not be abandoned."
> "all of the issues that were hiding here are going to exist in any object paging system, whether or not it is
> persistent. Given an object paging layer, the marginal logic for in-kernel persistence is just the snapshot
> and generation support"

**Shapiro, 2021-03-16**, L4-Hurd (`gmane.os.hurd.l4::CAAP=3QN1HbRbSH_H=+EFpOmTG+8KGNyOYFCToJo6+UKREmDtxw@mail.gmail.com`):
> "One the problem with orthogonal persistence is that it doesn't actually simplify much in networked systems.
> Two processes running on the same machine will be restored in a mutually consistent way, but processes
> running on *different* machines will not. This tends to mean that communications across the machine perimeter
> behave very differently, and a lot of processes need to know about it. The truth is that these two cases have
> *always* behaved differently, but UNIX and Windows go to extreme lengths to hide this from applications
> (unsuccessfully, because it can't be done in principle when messages cross failure domains)."
> "The other problem is that you sometimes *need* to violate orthogonality. For example, you don't want to lose a
> committed banking transaction if the system has to restart before the next checkpoint. KeyKOS, EROS, and
> Coyotos *all* have ways to bypass the checkpoint rules for this kind of situation."
> "The hard part is bounded rollback using local checkpoint ... The problem of independent failure domains isn't
> going to go away, and once you have to deal with it *anywhere* the incentive to expand individual failure
> domains is greatly reduced."
> "all of the "pointers" (the object references) point from the invoker to the invokee. That turns out to be
> essential if you want to implement transparent orthogonal persistence."
> "The hardest part of persistence in EROS was that the "node" object had so many possible interpretations"

**Shapiro, 2021-03-23**, L4-Hurd (`gmane.os.hurd.l4::CAAP=3QNYy=sFFyLO36OdYFTvYp9HPT9g90-OCKQd8p0fcRKqcA@mail.gmail.com`), on the bypass:
> "the database holds a specialized capability that allows it to flush a page (or pages) to disk and add the new
> content of the page to the previous checkpoint. This can only be done for data pages, and in 50 years we've
> never found a credible use case for it other than database transaction commits."

**Shapiro, 2026-03-06**, cap-talk, "Ageing, checkpoint, and OTEntry scans" (`cap-talk::JWWkx4plBgAJ`):
> "In KeyKOS, the checkpoint pass involved a synchronous pass to mark all the dirty objects immutable and
> invalidate mapping tables. This cost is linear with DRAM size ... In Coyotos all of that is incremental. Once you
> make it into the kernel, the snapshot step is about ten instructions to flip the generation number"
> "taking an in-memory snapshot doesn't mean that you have to write down a background checkpoint."

**Landau, 2009-10-12**, e-lang (`gmane.comp.lang.e.general::4AD3A778.1020907@macslab.com`). Kevin Reid had said
"Due to E's requirements for consistency on revival, an entire vat *must* be persisted as a unit." Landau:
"That does not imply that the implementation must take time proportional to the size of the vat. KeyKOS and
CapROS only write out objects that were changed since the last checkpoint."

**Karp, 2019-11-19**, friam (`friam::jVntUujaCAAJ`), on Waterken's output commit:
> "Tyler Close took a different approach in waterken. He delayed releasing messages until the checkpoint at the
> end of the turn finished. The result is that the most recent checkpoint of every node is part of the globally
> consistent state ... The downside is increased message latency"

**Miller, 2019-11-20**, friam (`friam::wtFOmZzUBAAJ`): if a restored vat "is now in a state prior to the one in
which it decided to send 5, and might compute forward from there in a way that does not decide to again send 5,
then that's hangover inconsistency. My overall answer to that is: don't do it."

**Miller, 2019-12-02**, friam (`friam::B0gHxWqXBgAJ`), Agoric's original plan:
> "Using lexical closures for encapsulation is fundamental to our ocap patterns. Yes, we plan to implement
> orthogonal persistence for full SES heap state. Our POC does currently implement orthogonal persistence in an
> unreasonably expensive manner: by replaying the entire history of incoming messages. The same determinism that
> enables deterministic replication enables recovery by replay."

**Morningstar, 2020-12-17**, cap-talk, "SwingSet nanokernel" (`cap-talk::q-hZQafWAwAJ`):
> "If you mean "what do you do if a vat fails?", the answer is: we kill the vat. Since vats are deterministic,
> if it fails once it will always fail and so there's no point to trying to recover"
> "given that our principal target environment is blockchain, we need to have the snapshot be part of the
> consensus state, which requires much more careful specification and implementation than if all you needed to
> do was something more like a heap dump."
> "we let the vat run to quiescence, at which point it no longer has agency and control returns to the kernel."
> "we can't capture idiosyncratic memory state inside the vats (consider, for example, closed over variables)
> without the complicity of the underlying JavaScript engine"

**Lemmer-Webber, 2020-12-02**, cap-talk, "Vat turn state/serialization/diffs" (`cap-talk::gPxrbwM3BAAJ`): lists
"Replay all messages on top of some initial conditions (Examples: Waterken, Agoric currently)", "Runtime-level
snapshotting (but requires deep cooperation from the runtime)", "Safe Serialization Under Mutual Suspicion ...
'ask the objects to give a sealed representation, but they can only claim the authority they have'", and
"Hybrid: take periodic snapshot, then only play messages in-between". On dirty-tracking: "Bob is not asked for a
depiction because Bob was not seen to be called on this turn!"

**Miller, 2026-03-05**, cap-talk, "Comparing capability systems" (`cap-talk::xBsfBdwbBgAJ`), the current
position:
> "Agoric's use of Endo starts with orthogonal persistence just to ensure that all honest validators produce the
> same deterministic computation, independent of whether they crashed and started or they just continued. This
> leaves upgrade as a separate problem. Agoric does both state-based upgrade (via Exos) and relay based
> "Manchurian" upgrade (via async-flow) ... we do not expect non-consensus use of Endo to support orthogonal
> persistence. Rather, the durable state of state-based upgrade will also provide persistence."

**Morningstar, résumé** (fudco.com/chip/resume.html, fetched 2026-10-04), on his Agoric kernel work:
> "Much my kernel work consisted of building out the data persistence machinery for the isolated computation
> containers (which we call "vats"), to present the illusion of continuous execution, where memory state
> transparently survives shutdowns and system failures. Further elaboration of these mechanisms allow support
> for data persistence in the face of code upgrade"

INFERRED: the man who wrote that EC's orthogonal persistence was "the blind alley" (2006) later built Agoric's
transparent crash persistence. The two positions agree once the roles are split: transparent persistence for
crash and consensus, declared durable state for upgrade.

## 1B. Schema and version migration of persistent objects

**Morningstar, ~2006-12-21**, Habitat Chronicles, "Smart people can rationalize anything"
(`morningstar-smart-people-rationalize-2006.txt` l.211–215; first comment dated 2006-12-22):
> "it cost months and months of development time, and it introduced a number of subtle new problems, any one of
> which would have a made a good PhD dissertation topic."
> "for most kinds of objects, the amount of state you actually need to save persistently is a small fraction of
> the full run-time state of the object. But in an orthogonal scheme you save it all, indiscriminately. The
> problem is not so much that it's bulky, though it is, but that the volume of semantic meaning that you are now
> committed to maintain in near-perpetuity is vastly increased ... The problem of schema migration as new
> versions of objects were developed (due to bug fixes or feature enhancements) proved effectively intractable.
> Ultimately we fell back on a scheme that compelled programmers to be much more deliberate about what state
> was checkpointed, and when. That proved more practical, but in the meanwhile we lost literally years of
> development resources to the blind alley."

**Miller, "Persistence and Upgrade"**, erights.org/data/serial/jhu-paper/upgrade.html (undated; part of the
Safe Serialization Under Mutual Suspicion material, early 2000s — date INFERRED; Miller pointed to it in 2017 as
the write-up of the EC war story). Section headed "Lessons of Persistence and Upgrade (*** To be written)".
Saved `miller-erights-persistence-and-upgrade.txt`:
> "if one uses transparent orthogonal persistence instead of manual persistence, then the entire runtime
> representation becomes the schema that needs to evolve. This amplifies the difficulty of the upgrade problem,
> often to a fatal extent."
> "Do you, Programmer, take this Object to be part of the persistent state of your application, to have and to
> hold, through maintenance and iterations, for past and future versions, as long as the application shall
> live? --Arturo Bejar"
> "Runtime representations emphasize the operational, whereas schema emphasize the declarative."
> "Smalltalk, with its easy support for live upgrade, is not a counter-example. This support cannot be made
> reliable, and is instead designed for programmers-as-customers who know how to recover from inconsistencies."
> "it more closely resembles building an upgrade-robot that will reliably perform this maintenance on any
> possible state such a machine may be in ... This kind of persistence indeed provides a process with easy
> immortality, but only as a living fossil."
> "The old machine is scrapped and a new machine is freshly built around these arguments."
> "The first step in dealing with the schema evolution problem is to mostly avoid the problem by saving vastly
> smaller schema."
> "A system may well use both: transparent orthogonal persistence to mask crashes efficiently [KeyKOS, EROS], and
> largely manual persistence only when upgrading ... Each post-crash revival is then a degenerate zero-delta
> upgrade"
> "What to save/restore vs. what to reconstruct vs. what to reconnect." "Does such a state include messages in
> flight?"

**Miller, 2017-10-20**, cap-talk, "My EC War Story: The disaster of orthogonal-only persistence"
(`cap-talk::YWqBWHwiAQAJ`; root `cap-talk::tBn53HohAQAJ`):
> "It is at the core of a knot of issues that I continue to wrestle with, and have reversed course on several
> times. Since this was written, Waterken and Ethereum have both adopted orthogonal persistence and used it
> well."
> "Starting from Ken-like distributed orthogonal persistence, there are two related problems we must face:
> a) Upgrade ... b) Coping with distributed failure. Both of these can built as a layer on top of Ken-like
> orthogonal persistence."
> "Tezos is an extreme lesson in the issues of managing upgrade under mutual suspicion, making it into mostly a
> governance issue."

**Garnock-Jones, 2017-10-27**, same thread (`cap-talk::oumC1_ecAgAJ`): "Each Erlang/OTP process state value is
more or less a defunctionalized, closure-converted continuation, expressed in a domain-specific way. Upgrade of
process state then becomes schema (datatype) evolution".

**Stiegler, 2008-07-17**, cap-talk, "How desirable / feasible is a persistent OCAP language?"
(`captalk::gVLX--LlvvYJ`; root `captalk::Ipp6VUIfoWAJ`):
> "I seem to be on the bleeding edge of using persistence in OCAP languages, having written persistent code with
> both E and Waterken. My observation from the field is, new insights are sorely needed ... E's persistence is
> just plain hard to use."
> "Waterken's orthogonal persistence runs quite behind the scenes and is utterly unstoppable -- your stuff gets
> persisted, and revives exactly where it left off, it is like a bulldozer ... Or perhaps like a Terminator. On a
> normal day this is really cool. But on a bad day -- and bad days occur too often to just write them off as
> anomalies -- this can be a serious problem. Recovering from an error can be so difficult that you have to
> throw away the whole universe -- not just one computer's worth, but a whole distributed network's worth. One
> of the specific circumstances that is most dreadworthy is the software upgrade, which in a waterken world is
> necessarily a live system upgrade. Alan Karp and I recently started a pilot program with half a dozen users
> using a waterken application we have under development. I have not added a single significant feature since,
> and am terrified of the need to do so."
> "Upgrading the software in a distributed system when there is any persistent state is just hard."
> "All the garbage in a waterken system gets persisted too"
> "the schema is a clean compact representation of the core of the upgrade problem ... You can write a separate
> program just to massage the dbms into shape for the next launch ... You can even tinker manually if you screw
> it up badly. The ability to tinker in the event of a screwup substantially reduces the fear factor"

**Shapiro, 2008-07-17**, same thread (`captalk::zOyagVcrRXkJ`):
> "Equally important, it constitutes an alleged type system that informally encapsulates many of the essential
> internal semantic relationships of the data set, and the transactional capabilities of a DBMS mean that you
> can do an all-or-nothing upgrade procedure on it. EROS/KeyKOS have a similarly generic low-level
> representation, but they don't have anything analogous to a schema, and I have come to see this as a failing.
> All of the stories I have heard for upgrading such systems are just that: stories."

**Karp, 2008-07-29**, same thread (`captalk::mNqmB4_vmOoJ`):
> "While it's persistence model has saved us untold lines of code, we have made changes incompatible with the
> serialized objects, which forced us to throw away the saved state and start over. That's OK for a research
> prototype, but not for the real world."
> "Orthogonal persistence (OP) captures the entire reference graph so that it is available on restart. The ZBAC
> approach is to capture only enough of the permission state to allow rebuilding of the desired part of the
> reference graph after a restart."

**Ihab Awad, 2008-03-16**, cap-talk (`gmane.comp.capabilities.general::8694afb80803160855l183ca54bld900d94edc4e1101@mail.gmail.com`):
"By providing orthogonal persistence, you limit the times when you have to worry about representation to when
upgrade is necessary. At that point, there is a semantic issue -- do you store the date of birth of the Person
object or the age? -- that the programmer *must* deal with."

**Shapiro, 2008-03-31**, cap-talk (`gmane.comp.capabilities.general::1206983813.3331.14.camel@shaptop.om-md.eros-os.com`):
> "Orthogonal persistence does not eliminate the need for object serialization ... In most cases, the best way to
> upgrade an object is to serialize its state, instantiate the new version, and have the new version read in the
> old state (possibly using an intermediate, transient format converter to separate out the conversion logic).
> To the extent that this is true, the only objects requiring a complex upgrade protocol are objects that
> require on-line update."

**Donnelley (NLTSS), 2008-03-16**, cap-talk (`gmane.comp.capabilities.general::200803180553.m2I5rGlg019934@www.eros-os.com`):
"all our service processes were designed to be restartable without loss of objects and their capabilities ...
the persistence of the objects and capabilities was the responsibility of the service processes - even across
restarts and most certainly across upgrades ... There was often a bit of a tricky transition when a service code
was upgraded to a new object header form (translate the old into the new) ... Such changes didn't happen very
often." On persisting process stacks across code upgrade: "If so that sounds pretty ambitious to me."

**Stiegler, 2004-08-29/30**, e-lang, "Persistence In E: Usability Issues and Proposals"
(`gmane.comp.lang.e.general::001e01c48e1b$ede89380$0201a8c0@hpl.hp.com`, `...001f01c48e1c...`, `...000501c48e26...`):
> "I found the persistence system in E to be, uh, slightly challenging (i.e., it was intractably unusable)."
> "persistence is the only core requirement for which E is, in my opinion, not yet usable."
> "In a program constructed without consideration of persistence, the answer is, "nope, nobody knows how to
> construct you"."
> "Of the six methods in the mint interface, two are for actual operations, and four exist for the sole purpose of
> supporting persistence."
> "persisting a sealer/unsealer pair is, without leaping through enormous hoops, apparently impossible."

**Morningstar, 2004-08-30**, e-lang (`gmane.comp.lang.e.general::200408300744.i7U7iGZ02106@abulafia.fudco.com`,
`...200408300748.i7U7mi302116...`):
> "Mark's approach to things ... is just too ascetic, too "eat your vegetables", for people like me to be happy
> using it directly."
> "Having that stuff be a method named "__optUncall" has all the aesthetic appeal of listening to a dead fish
> smack onto wet concrete."
> "I agree with MarcS that the solution is to suck persistence into the language syntax as a first-class concept
> in its own right"

**Close, 2008-01-20**, cap-talk, "Handling upgrade with the Waterken Server"
(`gmane.comp.capabilities.general::5691356f0801201522v4379a47jc62a5b79aeb45c26@mail.gmail.com`):
> "a common theme across many design patterns for handling upgrade will be to dodge the problem as much as
> possible. For example, one approach is to design a set of classes whose sole purpose is to hold your
> long-lived state. These objects are kept as simple and generic as possible. The application's behaviour and
> user interface is then implemented in a separate set of classes. Designing these classes to survive multiple
> upgrades is just too hard, so we don't and instead plan to fail here. Failure to upgrade is handled gracefully
> by ensuring each user has a capability that can later be used to create a new application facade on top of
> the existing long-lived state."
> "my feeling right now is that it's a manageable problem"

**Close, Waterken "upgrade: Live fast, die young and leave a good-looking corpse"** (waterken.sourceforge.net/upgrade/,
c. 2008–10; `waterken-upgrade.txt`):
> "At the end of every event loop turn, before any externally visible I/O is done, the Waterken server persists
> all application objects that are reachable from previously persisted objects."
> "An effective strategy for dealing with the challenges of persistent state is avoiding it."
> "This design reduces the upgrade challenge to the design of the application's model. Constraining the scope of
> the upgrade challenge in this way is the most important step to take in the design of an application's
> persistence strategy."
> touch.jar "runs as a normal vat transaction and so will either commit with all objects upgraded, or abort"
> Amputation: "only refer to objects in that part of the graph using eventual references. Once bit rot takes
> hold in that part of the object graph, change the application code to no longer access it."
> Offload: "it may be best to start over with a new design, bootstrapping new vats with application data pulled
> in from the old model ... the application model should support a query interface that can generate documents
> describing the current application state."

**Freudenberg, 2013-05-13**, squeak-dev (`gmane.comp.lang.smalltalk.squeak.general::6BA3EEB1-DF27-4D9D-A11C-A2F6E170D174@freudenbergs.de`):
"Classes in Squeak are versioned precisely for that reason (see implementers of #classVersion). A newer class is
supposed to be able to read instances of its older versions. It provides data migration methods ... when
exporting a changeset that affected class layout, the system used to warn you that you should better add an
migration method". And: "you could plan ahead and build in support for migration."

**Lemmer-Webber, 2024-04-23**, "Spritely Goblins v0.13.0: Object Persistence and Easier IO!"
(`spritely-goblins-v0130-persistence-2024.txt`):
> "Goblins' persistence system does not use "orthogonal persistence" ... orthogonal persistence suffers from
> generally saving much more than the programmer may need and tends to result in difficult to upgrade systems."
> "Every persisted object is also tagged with a version (defaulting to 0 if none is provided) permitting the user
> to perform an upgrade at restoration time"
> "Objects cannot describe themselves with more power than they actually have access to."
> "The original version of Aurie was cumbersome to use"

**Tallon, 2024-09-19**, "Goblins v0.14.0" (`spritely-goblins-v0140-persistence-2024.txt`): "any far reference is
restored as a promise that resolves when the object on the other vat becomes available. In other words, all far
references start out as promises." Of the migrations macro: "you only have to focus on migrating from one
version to the next".

**Practitioner, 2023-03-14**, Twitter @anvil_ic (tweet 1635723399875166211): "Orthogonal persistence in
canisters works great if you know what you are doing from the start. Startups usually don't. They are just
adding stuff to memory and only later do they figure out what to do with it".

## 1C. Upgrade of running code

**Landau, 1992**, §8.2 "Upgrading software":
> "The new kernel can simply restart using the data checkpointed by the old kernel. The other side of this coin is
> that user software upgrades must be managed more carefully in KeyKOS than in less reliable architectures.
> Non-kernel software does not stop running when the system is rebooted. It requires explicit action to stop
> such software. Furthermore, the convenience of storing permanent object data in virtual memory structures or
> even process registers must be weighed against the need to separate the program from its data when it is
> desired to upgrade the program while preserving the data. In the applications where KeyKOS has been used, we
> have found fairly simple upgrade strategies to be adequate, but they must be planned in advance."

**Frantz, 2008-03-16**, cap-talk (`gmane.comp.capabilities.general::r02010500-1049-3BC18040F32711DCB7FC0030658F0F64@[192.168.1.5]`):
> "these systems offer a choice between easy persistence and easy upgrade. Given that this dichotomy is real,
> when programming for KeyKOS style persistence systems, the programmer must pay the same kind of attention to
> upgrade as a Unix programmer pays to persistence."

**Frantz, 2008-04-05**, cap-talk, "Styles of persistance"
(`gmane.comp.capabilities.general::r02010500-1049-20CFFA0E02B211DD98ED0030658F0F64@[192.168.1.5]`) — the
single most complete first-hand account of KeyKOS upgrade practice:
> "In order of decreasing desirability:
> 1. Avoid long-lived objects. For example, instead of keeping an instance of a reusable compiler, build a new
> instance of a use-once compiler for each compile ...
> 2. Build long-lived objects that can serialize their state, load a new version, and have that new version
> reload the serialized state ...
> 2a. Build the new version in a new object and discard the old version. All capabilities to the old version
> become invalid, and users must be rebound to the new version (somehow). This approach is desirable because it
> assumes the least about the relationship between the internal structure of the two versions.
> 2b. Build the new version on the ashes of the old version so old capabilities remain valid.
> 3. Design, from the beginning, for the object to be able to upgrade itself. This approach seems to be the only
> viable one for the space bank."
> "We can avoid having to upgrade that data by only checking for upgrades when it is no longer needed. So we
> check for upgrades when the stack is (nearly) empty."
> "For the data which must be upgraded, the long-term state, we should first isolate it in a separate segment
> from the code, stack, transient heap etc."
> "For short-lived objects we didn't have a problem. For long-lived objects, like the space bank, we tried to
> avoid the need for upgrade. The first technique we used was to keep the specifications for these objects
> simple ... I don't think we ever had to upgrade the space bank."
> "The one long-lived object we actually upgraded was the clock object ... Since the original clock object was
> not designed to assist in upgrade, the process ended up being a bit like open-heart surgery."
> "To upgrade the clock, we used the read-write capability to the code segment to patch the running program ...
> (If the whole segment had been in use we would have been SOL.) ... But the whole process was ugly beyond
> belief."

**Frantz, 2008-07-28**, cap-talk (`captalk::1J5jrVudr-4J`): "when the long-term state is kept in a well defined
format, upgrade becomes easy. Examples include the KeyKOS kernel (but not the objects it implements)".

**Miller, 2019-11-20**, friam (`friam::wtFOmZzUBAAJ`): "Agoric is mostly following the Waterken philosophy, but
will likely adapt the E failure model to deal with upgrade. This means that the analogue of an E live reference is
one that survives partition exactly in a Waterken-like way, but then severs all such live-like references across
an upgrade. This also help manage version skew between messages sent and messages expected."

**Agoric SwingSet, "Vat Upgrade"** (packages/SwingSet/docs/vat-upgrade.md; `agoric-swingset-vat-upgrade-2025.md`):
> "Vat upgrade is not transparent: other vats will notice something has happened. The vat upgrade philosophy is
> to preserve long-term state, but abandon any work that was in-progress."
> "Each export represents an obligation."
> "Promises do not cross the upgrade boundary ... we haven't thought of a good way for v2 to assume
> responsibility for resolving a v1 promise"
> "To enable upgrade, the v1 code must stash important data in durable storage ... It needs to do this from the
> very beginning: if v1 fails to retain something, v2 cannot get access to it"
> "any lazy migration must be prepared to handle arbitrary messages despite the migration not being complete."

**Connolly, 2023-09-21**, cap-talk, "vat upgrade in production" (`cap-talk::4WuGp5mVAAAJ`): "#49 Upgrade Smart
Wallet to support NFTs just completed, in block 11731339 on the Agoric production mainnet chain. The Persistence
and Upgrade problem has been a thorny one for quite some time" [quotes Bejar] "The SwingSet vat-upgrade solution
preserves capability security through the upgrade."

**Hibbert, 2024-03-08**, friam (`friam::aOjUXlQHBAAJ`): "We've recently added tools that provide for durable
handling of promises, which means it's possible to write long-lived services that rely on other long-lived
services, and expect to survive a restart or upgrade of either the code you're writing or code you're depending
on."

**Agoric issue #12315**, 2026-01-07 (github.com/Agoric/agoric-sdk/issues/12315; author not in saved copy):
> "Currently if a flow fails replay, it is marked as panicked in the hope that future upgrade can handle the
> situation. This can often be wishful thinking because the incompatible flow can now have new activations,
> resulting in replay logs of both incompatible behaviors. A contract should be able to chose failing its upgrade
> if flows fail to replay."

**Agoric issue #12138**, 2025-10-20: "Chain halted due to missing durable kind definition for tag `asyncFlow`" …
"CONSENSUS FAILURE!!!".

**Agoric issue #8955**, 2024-02-20: "if we're restarting vats to switch to a new xsnap, we have no way to return to
the old version: that old heap snapshot and transcript are unusable without the old xsnap to run them." "this
restart-all-vats plan might be practical for now, when we have 87 vats on chain, but not when we have a
thousand."

**Miranda, 2015-05-04**, squeak-dev (`gmane.comp.lang.smalltalk.squeak.general::CAC20JE1udSPERdYTLo0Zd3RiS3ZzvYXDo1arUSRqoF8Lp+9kvQ@mail.gmail.com`):
"This breaks my image, dumping it into the emergency evaluator ... So for those of you using Spur please *don't*
update until I've fixed the bootstrap."

**Shapiro, 2021-03-16** (key above), on interfaces: "it is possible for the API or interface of the object to
change dynamically ... The capacity to "morph" its operation set was part of the specification of the original
behavior of the object."

## 1D. Promise pipelining and eventual send in practice

**Miller, 2011-06-11**, e-lang, "Re: Question about E's history"
(`gmane.comp.lang.e.general::BANLkTim=fxknXGfWaAeZp-cG-RK6O-r1xg@mail.gmail.com`):
> "In 1989, Dean, I, and others independently came up with a promise pipelining model similar to Liskov and
> Shrira's promises as part of the Xanadu (aka Udanax Gold) work ... we found out about their 1988 paper ... and
> so have consistently given them credit for inventing the idea first"
> "AFAIK, Joule is the first language to combine Actor-like pervasively concurrent futures/promises with
> Liskov-like promise pipelining."
> "Original-E's unique achievement ... was the first to invent non-blocking promises, via "when", in the context
> of concurrency added to a locally sequential-imperative language."
> "Doug Barnes first created Original-E, by shoehorning Joule-inspired concurrency onto a Java base in an intense
> two week efforts driven by a business panic, after a contractual dispute between Agorics ... and Electric
> Communities"

**Stiegler, 2004-11-27**, e-lang, "Events as Bad Ideas"
(`gmane.comp.lang.e.general::BCD023E7727C0A4C93574C4D6C7FE31208D26A@cacexc12.americas.cpqcorp.net`):
> "E promise pipelining has as goals, high performance when latency is the limiting factor, and an interface to
> the human programmer that improves the programmer's chances of coming out alive."
> "if you care about performance more than everything else in the world, we do not have anything to offer."
> "E once again has a mechanism that was not foreseen by the authors, the broken promise."

**Stiegler, 2015-10-14 and -15**, cap-talk (quoted inside Miller's reply
`gmane.comp.capabilities.general::CABHxS9gZ7_Kguabb6vGpn15CuvLruv4CrH5PAyPY5pKVS6_QsQ@mail.gmail.com`):
> "pipelining promises is anything but automagical. Capper, my open source nodejs server that uses promises and
> semi-transparent checkpointing and webkeys ... does not include pipelining for the promises. The pipelining is
> far more work to implement than are the promises themselves."
> "you want to use waterken, which builds the reliability into the promises along with the pipelining, by
> retrying relentlessly until it gets a resolution ... It is magnificent to use. One suspects at this point that
> we will not see anything comparable again in our lifetimes, sorta like KeyKos or Xanadu."
Miller in reply: "I know Waterken had the enabling mechanism for promise pipelining. But I don't remember if it
was completed and made the default mode of operation."

**Miller, 2017-10-20** (key above): "E live refs break under partition and all messages in flight are dropped. By
contrast, Ken's "all refs are sturdy refs" ... can only be implemented with an unbounded obligation to keep trying
to send all unacknowledged messages forever ... From this I conclude that the E failure model is ultimately what I
want, but with timeouts more like 20 years rather than 20 seconds."

**Miller, 2019-11-19**, friam (`friam::iwW-xcfdCAAJ`): "A message is retransmitted until an ack is received. A
duplicate incoming message is dropped by the receiver but redundantly acked. Under the assumption that things
eventually come back on line, every message ever sent is eventually delivered in order exactly once."

**Miller, 2026-03-05**, cap-talk (`cap-talk::6dTLUpEgBgAJ`): "Waterken masks partition and crash/revival. A
network partition is, to the Waterken programmer, just a slow network. Every crashed machine is just a slow
machine ... Agoric's use of Endo following the Waterken failure model." "distributed error model is entangled both
with persistence and upgrade model and with the distributed deallocation model ... Also entangled with message
ordering, such as FIFO vs E-Order."

**Frantz, 2011-02-05**, friam, "Waterken issues discussed today" (`friam::VoLGM1QDksgJ`): Karp's scenario — in
one turn `get(x); get(y); setxy(a,b)`; if the response to the second GET "gets lost and later replayed, VatA might
receive the new value of y". Fix discussed: "record the GET requests for a future checkpoint ... the recorded note
doesn't need to be committed to disk until the POST". And: a server with a non-empty input queue "can delay
writing the checkpoint to disk and returning the results until the end of the next turn ... For a heavily loaded
server this technique may be a useful way of load shedding."

**Shapiro, 2013-05-01**, cap-talk, on CapIDL vs Cap'n Proto
(`gmane.comp.capabilities.general::CAAP=3QOy-5Xu7ppVnyfQGRoEdmsVJi1hTK8J_LOUfd7PmoSCbA@mail.gmail.com`):
> "the type of the resulting promise must be a union type of the form (value|exception). Note that *all* CapIDL
> return values are [open] unions, because any CapIDL operation can produce an exception."
> "the original CapIDL design provided for exception structures, I later came to feel that this was a huge
> mistake, because it makes the size of the return payload unknowable. In practice, exceptional results can
> invariably be encoded by an exception code and a single augmenting information word."

**Shapiro, 2021-03-16** (key above): "The ability to transfer the authority to *reply* is fairly essential. This
was a pretty fundamental design mistake in Mach IPC."

**Hibbert, 2024-03-08**, friam (`friam::aOjUXlQHBAAJ`): "MarkM has convinced us at Agoric that this form is
usually a bad idea ... the caller can't be sure whether the code will return synchronously or not ... the correct
rule is that a non-top-level await (i.e. await in a loop or conditional) can't be the first await in a function".

**Agoric issue #9608**, 2024-06-28: vows for "Retry idempotent eventual sends with reliable durable result vows
that mask upgrade trauma."

## 1E. Capability administration and governance

**Hardy, 2006-06-21**, cap-talk, "Capability accounting"
(`gmane.comp.capabilities.general::A116C1E6-F4B4-4493-A244-66868D217399@cap-lore.com`):
> "Keykos has highly developed accounting hooks ... It was written for a Timesharing company that charged for
> resources ... This was within the confines of one machine and indeed guaranteeing resources for a distributed
> application is much more difficult."
> "In practice there was one user who created new user accounts. That user would create the sub-bank and sub meter
> for each new account. He would retain the service keys to both the bank and meter. A directory of users mapped
> user names to nodes with these keys which allowed intervention in the user's world."

**Hardy, 2017-02-11**, friam, "Synergy for the record" (`friam::i5qwCjjVDwAJ`):
> "When X asks Y for a zot to serve X's purpose, X delivers a space bank B to Y so that X pays for the space that
> Y uses to serve X ... To support these two goals Y asks the bank creator, known to both X and Y, "Is B a bank" ...
> Now Y can call B with assurance that it will promptly get either "Space is unavailable." or "Here is a cap to
> the space you asked for."."

**Hardy, 2012-01-08**, cap-talk (`captalk::ho2ApsfLQGEJ`):
> "Keykos does not signal unreachability ... it was often necessary to delete objects despite existing references
> to them. Such bloody stumps are efficiently guarded against by code using them, but the cost of surviving a
> missing limb may still be large, or impossible ... Disappearance of 'exogenous' objects must generally be
> explicitly tolerated."

**Frantz, 2008-04-05** (key above) on the KeyKOS factory: it "tightly controls the out-bound channels of
communication available to the objects it creates. However, it doesn't attempt to control the in-bound
communication" — which is exactly what made the clock patch possible.

**Agoric vat-upgrade doc**: "The ability to upgrade a vat is also the ability to control its behavior, and any
users who expect some particular vat behavior (e.g. when auditing some contract code) must take into account the
possibility of upgrade, which means they'll care about who exactly can cause an upgrade to occur."

**Miller, 2017-10-20** (key above): "Tezos is an extreme lesson in the issues of managing upgrade under mutual
suspicion, making it into mostly a governance issue."

**Morningstar & Farmer, 1990**, "The Lessons of Lucasfilm's Habitat" (in Benedikt (ed.), *Cyberspace: First
Steps*, MIT Press 1991; `morningstar-farmer-lessons-habitat-1990.txt`):
> "Detailed central planning is impossible; don't even try."
> "It is important that there not be "leakage" between these two levels [infrastructure and experiential]."
> "Work within the system."
> "All new region generation and feature implementation had to go through us, since there were no means for
> players to create new parts of the world on their own."
> The money-supply bug: "We only discovered this the next morning when our daily database status report said that
> the money supply had quintupled overnight." (A pricing error, legal under the rules, not a code bug.)
> The operator who threatened to cancel a player's account to recover a gun: "Their world model had been
> painfully violated." The authors instead ransomed it in-character.
> On decentralising: "The most significant of these is the prevention of cheating. Obviously, the owner of the
> network node that implements some part of the world has an incentive to tilt things in his favor."

**Rob Meijer, 2008-04-05**, cap-talk (`gmane.comp.capabilities.general::12156.82.95.100.23.1207381457.squirrel@webmail.xs4all.nl`):
"Where possible, avoid using capabilities that should survive transactions."

**Frantz, 2008-07-28 / Karp** (`captalk::1J5jrVudr-4J`, `captalk::spcoaOIk-F0J`): Karp's point that "the most
important thing that needs to be persisted in a capability system is changes in the long-term capability
relationships"; Frantz: "the changing access relations of a capability system are an important part of the things
that should be persistable." Miller (`captalk::bFaRG-uoJt0J`): "the holder of a cap to resource R generally
doesn't have permission to add itself to R's ACL."

**Shapiro, 2005-11-08** (key above), the KeyKOS kernel rule: "the kernel should never rely on the correct behavior
of application code in order to ensure the correct behavior of kernel code. Not even application code from the
system TCB. If the space bank got something wrong, the kernel should not contribute to further error".

## 1F. Metering and accounting

**Hardy, 1985**, "KeyKOS Architecture" (`hardy-keykos-architecture-1985.txt`): "For a domain to run, its meter slot
must hold a meter key to a valid superior meter ... There must be a chain of meters leading to the primitive meter.
As a domain runs, the chain of meters rooted in the domain's meter slot all record the resources used ... A
meter's keeper slot key is called when a resource counter in the meter reaches zero."

**Frantz, 2019-07-30**, cap-talk, "Questions about KeyKOS" (`cap-talk::zGTI49fRCAAJ`): "KeyKOS only metered CPU
time, although the plan was to use the same logic as the Tymshare modified VM system ... The meter was designed to
measure main memory occupancy (number of pages times time) and transfers to and from disk to that memory. Making
these measures reproducible was one of the neat tricks in the algorithm."

**Frantz, 2018-04-08**, friam, "What are Actors?" (`friam::zPqK1GpEAgAJ`):
> "KeyKOS never built a scheduler using the meters. We were able to get by using the internal kernel level
> scheduler which implemented the kernel's contract, which boiled down to, "The kernel will run ready domains when
> it wants to.""
> "The question of how to run the ready domains was one that almost brought the team to blows ... all the more
> intelligent options could be gamed to get more CPU for yourself ... preference to domains which had other domains
> waiting on them ... could be gamed by ensuring there was a domain waiting on your domain, even if you had to
> build it yourself. We never settled these issues"

**Hardy, 2012-01-31**, cap-talk, "Passing data in segments"
(`gmane.comp.capabilities.general::AF777178-7A7C-41CA-9585-610119451FAA@cap-lore.com`):
> "Such code runs under a meter that is paid for by the agency that 'owns' the lock and its data ... If the caller
> is terminated the transaction is unperturbed, as it is running under a meter owned by whoever is responsible for
> lock integrity."
> "If the meter of the code that owns the lock, is subject to delay, then any client of that code will likewise be
> delayed. I think this is an inherent problem."
> "I agree that there are no universal answers."

**Hardy, 2006-06-25**, cap-talk (`gmane.comp.capabilities.general::F1C0A5C9-C65E-4F71-984F-067F93ABBC04@cap-lore.com`):
"One danger is of 10,000 undifferentiated anonymous deamons sucking CPU and RAM in my computer. Most of them are
not supporting anything I value." "I have not seen useful designs for agents that make security decisions."

**Miller, 2025-08-25**, cap-talk, "OCaps and metering" (`cap-talk::Qb6liTZmAAAJ`): "Normally ocaps are about access
control. Metering is about excess control."

**Shapiro, 2025-08-26**, same thread (`cap-talk::BoLlJ3FzAAAJ`, `cap-talk::iSs4AF6BAAAJ`):
> "One of the conclusions in EROS was that the meter tree was inconsistent with hard or soft real-time scheduling."
> "The KeyKOS meter abstraction tacitly assumes that (a) scheduler time is arbitrarily subdivisible, and (b) in
> practice, scheduler time is non-monotonic ... The first assumption, in practice, is not correct"
> "Meters do not provide a contract about when (in a rate-periodic sense) you get scheduled. Then there's a
> question about what happens when an inter-process communication passes from a source on schedule A to a
> recipient on [unrelated] scheduler B. Most solutions yield both bounded scheduler inversion and a variation of
> confused deputies in the time domain."
> "Coyotos was headed in a direction based on BVT, abandoning meters entirely."

**Agoric "Metering CPU Usage"** (`agoric-swingset-metering-2025.md`): "if any crank causes the Meter's remaining
value to drop below zero, the vat is terminated"; computrons do "*not* depend upon ... wall-clock time, or type of
CPU"; and they are "likely to change if/when the JS engine is upgraded. SwingSet kernels that participate in a
consensus machine must be careful to synchronize upgrades".

**Agoric storage**, issue #8400 (closed 2023-09-28): "about 60% of our kvstore entries are the result of a bug in
the price feed contracts" — a safety feature (the ERTP Recovery Set) retained dropped quote Payments. #8401:
cross-vat cycles, "about 50k instances ... 310MB". #8928 (2024): terminating the bloated vats "would perform an
unacceptably large amount of work, and trigger some O(N^2) performance bugs in the kernel GC handling code, which
would probably crash the chain."

**Hibbert, 2020-06-07**, friam (`friam::fmsTrzCCAQAJ`): "The benefits come from the shared visibility of the
assurance that the "computer" did the right thing. Those benefits are valuable enough that the cost of replicated
computation are worth it."

## 1G. Debugging live systems

**Miller, 2004-12-10**, e-lang, "Causeway is ready for trial use!"
(`gmane.comp.lang.e.general::41B9B6B1.8060201@cs.jhu.edu`): "a "message-oriented" distributed debugger. Its main
follow-the-conversation view ... shows events organized by their causal relationship, as messages emitted by one
event cause "child" events ... As each event is selected, the lower left pane shows the stack at the moment the
message was sent that caused this event." "Causeway is primarily the work of Terry Stanley, based on an idea by E.
Dean Tribble".

**Kevin Reid, 2007-10-02**, e-lang (`gmane.comp.lang.e.general::F012C60C-0ACC-4179-BD16-985F9FE380F5@mac.com`):
> "Causeway is a post-mortem debugger (operating on logs produced by the program) displaying which turns caused
> which other turns."
> "Virtualization ... is the intended full interactive debugging mechanism for E ... The unique property of
> debugging access is that it allows the vat to be suspended and examined in the middle of a turn ... This hasn't
> been done yet because it requires what I'll call a "full VM" implementation of E: there must be no immediate
> callbacks from primitive code to E objects"

**Terry Stanley, 2008-02-18**, e-lang (`gmane.comp.lang.e.general::3047277a0802171844g59768e4md2ea4fdffdc41267@mail.gmail.com`):
"Trying to write the Related Works section has been pretty frustrating. Can anyone point me at debuggers built for
the communicating event loops concurrency model?"

**Tribble, 2003-12-24**, e-lang, "Re: Three problems with exceptions"
(`gmane.comp.lang.e.general::6.0.0.22.0.20031222094525.048d7e40@postoffice.pacbell.net`), on Miller's proposed
`abort()` that would kill the vat incarnation and restore the last checkpoint:
> "I expect that this is a bad idea. The function needs to exist, but should not be generically available ... it
> then includes total failure in the partial-correctness subset of E"
> "It also introduces a primitive that behaves significantly differently between persistent and non-persistent
> vats."
> "Joule's model ... is that an exception can be signalled to the caller; if the caller does not handle it, it goes
> to the Vat's keeper ... Fundamental VM errors (e.g., divide by 0, out of memory) were signalled to the keeper
> first so that it could intervene if appropriate before the user program notices the error."

**Hardy, 2007-08-11**, cap-talk (`gmane.comp.capabilities.general::11CC3E7E-5A3F-4CC8-9E85-EF005DE63438@cap-lore.com`,
SKIMMED): the KeyKOS logging membrane ANNALYST — "I used it to examine some of the software tools and found and
fixed some performance problems therein."

**Morningstar résumé** (Agoric): "creating tooling to allow developers (of both contracts and of the Agoric system
itself) to simulate the operation of the chain in service of debugging, testing, and performance measurement."

## 1H. Why each system did or did not succeed

**Landau, 2008-02-23**, cap-talk, "What sparked interest in capabilities - Charlie"
(`gmane.comp.capabilities.general::p06230909c3e2ba8c9145@[192.168.0.35]`):
> "Working on a project without any deadline is a wonderful luxury, and the Gnosis project took advantage of it,
> choosing always to do things the "right way"."
> "after McDonnell-Douglas Corp purchased Tymshare in 1984, Gnosis was no longer a priority ... Key Logic ... At
> that time, timesharing was becoming obsolete, the personal computer was ascendant, and the web hadn't yet
> happened; as a result, security did not sell, and Key Logic closed its doors in 1991."
> On Palm: "the preexisting Palm API was not capability-oriented, so none of these features showed through to the
> application programmer."
> "After 40 years, I'm still hoping to create a system that is reliable and secure enough that I can trust it to
> run the home automation software in my own home."

**Frantz, 2008-02-21** (key above): "When the PC killed the commercial timesharing business, Key Logic was formed
... After KeyKOS was retired to a locked filing cabinet, making me a strong fan of open source".

**Miller, 2012-12-05** (quoted in Hardy, `gmane.comp.capabilities.general::5F0456D5-2A97-48D3-B078-6578B2663776@cap-lore.com`):
> "We've generally pursued capabilities bottom up because we've been implicitly assuming we're supply limited
> rather than demand limited ... *That* is what we've been doing for 40 years and losing. The problem is, no one
> knows that they want what we've got ... The KeyKOS family is the single most perfect OS design ever conceived.
> Didn't take."
Hardy's reply: "We ran X11 on the Motorola 88K without even recompiling ... The Unix features it needed were there
in costume. It is true that many applications would need rewrite to run naturally and efficiently in Keykos ... As
Markm says, "It didn't take.". The pressure is higher now and growing."

**Landau, 2022-11-20**, cap-talk, "CapROS status" (`cap-talk::18pUqAQnAQAJ`), a letter to Miller:
> "Do any of these systems use checkpoint/restart? If not, how do they solve the problem of preserving
> relationships that are represented in capabilities? Does this no longer matter in a world where every device has
> a battery?"
> "Do these systems support tight control of resources such as storage space and CPU time, as KeyKOS did with space
> banks and meters? Or is it fair to consider resources unlimited nowadays?"
> "My work on CapROS stopped in 2013 when I had to take a full-time job. The last running CapROS system stopped in
> 2015 when lightning struck the hardware ... it no longer builds on currently-supported compilers ... There is
> virtually no documentation, and the EROS documentation has been lost."
> "I believe there are some useful ideas in the system, but so far no one seems to have known or cared about them."

**Shapiro, 2005-11-08** (key above): "why did L3/Eumel/L4 and Gnosis/KeyKOS/EROS survive for 25 years when the other
microkernels died? ... both systems were based firmly and uncompromisingly on principle driven design."

**Shapiro, 2025-08-26**, friam, "Opinions sought: Capabilty OS Book" (`friam::hHzrD1hFAAAJ`): "A log-structured
checkpoint system was designed, but never implemented." Coyotos changes: "The persistence architecture was reworked
to allow more than two object types. This greatly simplified the rest of the architecture." "Processes became first
class, retiring the "three nodes make a process" pun". 2025-12-14 (`cap-talk::WaD46YwWCQAJ`): migrating Coyotos to
Rust.

**Morningstar résumé**, Communities.com 1995–2001: "important parts of this technology were released as open source
software, principally in the form of the secure distributed capability programming language E"; second-generation
server "yielding significant technology licensing revenues even while CEO was bankrupting company trying to create a
media portal."

**Miller, 2015-10-15** (key above): "seL4 -- it has both L4 and EROS as direct parents. IMO the architecture is more
KeyKOS-family-like than L4-like." "Sometimes it is hard to notice when we win, if the victory is dressed in different
clothing."

**James A. Donald, 2008-07-18**, cap-talk (`captalk::I8XBZIZEJiQJ`), the dissent: "Persistent state hurts.
Persistent distributed state hurts a lot. Don't do that! Anything truly persistent must live at one authoritative
source". Shapiro in the same thread (`captalk::gNQZmJPUl5oJ`): "designing to avoid rollback cascade involves
accepting either (1) a very loose definition of "consistency" within the distributed application, or (2) a
qualitatively harder data schema and associated applications that cope with partial consistency by making it
explicit ... real programmers simply bet that failures are unlikely enough to be ignorable."

