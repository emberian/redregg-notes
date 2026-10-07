# Quest ACTIVITY-RETENTION-PAYERS (range 2 of metering/disposal) — proposed by SCHOLAR-HISTORIAN (consultant a58aefb7622368c6a)
Base: lane/metering-disposal 4015fd72 (on lane/resume-view 46b9d4fd, on activity-native) — queued in MERGE-QUEUE.md.
Native-route WIP for exhaust/abandon: lane/activity-metering-wip 1d720ef2 (persvati lane activity-metering), built on b31d8be8; rebase onto the native-route range when it lands.
Scope:
- Book `deregisterAccount` as a third Batch field with a conservation theorem (follow the activity-native consultant's design, agent a749680e0cb5834fe); update every <registrations, operations> construction site (~15 files reference Batch).
- A payer recorded on the package cell at publish.
- A storage deposit per checkpoint, re-priced at each yield.
- A `retention_cells_have_payer` census theorem.
- A real retire path through the World model's existing `retires`, replacing tombstones (today a reclaimed cell keeps an empty-body tombstone because the store's write law only accepts live cells and the bridge refuses retired ones).
Known pre-existing failure: the committed acceptance script leaves the sponsor at 51962, short of the 63001 the growth section needs (bookRefused) — fix the funding in the script.
