# Mutation survivors (Mini cfdaf64d)

mutants run: 467  build verdicts: {'BUILD-RED': 204, 'BUILD-GREEN': 214, 'DOWNSTREAM-RED': 49}  journey verdicts (of BUILD-GREEN): {'PENDING': 214}

A survivor changed NO verdict: lake build of the module, the umbrella + ObjectiveProofs, and (JOURNEY-GREEN) the journey rows that exercise the file all stayed green. PENDING = journeys not yet run.


## Kernel/AnswerSlot.lean  (1)

### m0402  line 198  offbyone(<->≤)  [PENDING]
```lean
- else if slot.deadline < height then .error (.pastDeadline slot.deadline height)
+ else if slot.deadline ≤ height then .error (.pastDeadline slot.deadline height)
```


## Kernel/NativeHostContext.lean  (9)

### m0508  line 213  negate-if  [PENDING]
```lean
- if own = some .joint then pure () else
+ if ¬(own = some .joint) then pure () else
```

### m0509  line 213  fallthrough-if(cond:=False)  [PENDING]
```lean
- if own = some .joint then pure () else
+ if False then pure () else
```

### m0510  line 220  negate-if  [PENDING]
```lean
- if own = some .activity then pure () else
+ if ¬(own = some .activity) then pure () else
```

### m0511  line 220  fallthrough-if(cond:=False)  [PENDING]
```lean
- if own = some .activity then pure () else
+ if False then pure () else
```

### m0512  line 304  negate-if  [PENDING]
```lean
- if config.jointConsensus.isSome then
+ if ¬(config.jointConsensus.isSome) then
```

### m0513  line 304  fallthrough-if(cond:=False)  [PENDING]
```lean
- if config.jointConsensus.isSome then
+ if False then
```

### m0515  line 367  conjunct-∧-left:=true  [PENDING]
```lean
- source.record.version = head.version ∧ source.record.semantics = config.profile.semantics)
+ True ∧ source.record.semantics = config.profile.semantics)
```

### m0516  line 420  negate-if  [PENDING]
```lean
- if condition then .ok () else .error detail
+ if ¬(condition) then .ok () else .error detail
```

### m0518  line 438  negate-if  [PENDING]
```lean
- if config.grainBirthTariff.isSome then
+ if ¬(config.grainBirthTariff.isSome) then
```


## Kernel/ObjectiveActivity.lean  (88)

### m0006  line 592  conjunct-&&-right:=true  [PENDING]
```lean
- decide (envelope.sourceTicks ≤ config.maxTicks) && decide (config.limits.heap ≤ envelope.heap) &&
+ decide (envelope.sourceTicks ≤ config.maxTicks) && true &&
```

### m0009  line 592  offbyone(≤-><)  [PENDING]
```lean
- decide (envelope.sourceTicks ≤ config.maxTicks) && decide (config.limits.heap ≤ envelope.heap) &&
+ decide (envelope.sourceTicks ≤ config.maxTicks) && decide (config.limits.heap < envelope.heap) &&
```

### m0031  line 1084  fallthrough-if(cond:=False)  [PENDING]
```lean
- if ObjectiveBendSourceArtifact.identity artifact = pin then .ok artifact.laws else .error .packageIdentity
+ if False then .ok artifact.laws else .error .packageIdentity
```

### m0032  line 1279  negate-if  [PENDING]
```lean
- if (typeData program.assumptions config.typeFuel outcome.data outcomeType).isNone then
+ if ¬((typeData program.assumptions config.typeFuel outcome.data outcomeType).isNone) then
```

### m0033  line 1279  fallthrough-if(cond:=False)  [PENDING]
```lean
- if (typeData program.assumptions config.typeFuel outcome.data outcomeType).isNone then
+ if False then
```

### m0035  line 1396  fallthrough-if(cond:=False)  [PENDING]
```lean
- | .exhausted => if config.maxTicks ≤ envelope then some s!"no yield within the turn cap {config.maxTicks}" else none
+ | .exhausted => if False then some s!"no yield within the turn cap {config.maxTicks}" else none
```

### m0055  line 1556  conjunct-&&-right:=true  [PENDING]
```lean
- else if before && !after then object.release pin activity
+ else if before && true then object.release pin activity
```

### m0065  line 1660  negate-if  [PENDING]
```lean
- if (fields.map Prod.fst).Nodup then fields.mapM fun field => do pure (field.1, ← decodeEdit field.2)
+ if ¬((fields.map Prod.fst).Nodup) then fields.mapM fun field => do pure (field.1, ← decodeEdit field.2)
```

### m0066  line 1660  fallthrough-if(cond:=False)  [PENDING]
```lean
- if (fields.map Prod.fst).Nodup then fields.mapM fun field => do pure (field.1, ← decodeEdit field.2)
+ if False then fields.mapM fun field => do pure (field.1, ← decodeEdit field.2)
```

### m0067  line 1690  negate-if  [PENDING]
```lean
- if edits.all (fun edit => edit.2.isKeep) then .ok none else
+ if ¬(edits.all (fun edit => edit.2.isKeep)) then .ok none else
```

### m0068  line 1690  fallthrough-if(cond:=False)  [PENDING]
```lean
- if edits.all (fun edit => edit.2.isKeep) then .ok none else
+ if False then .ok none else
```

### m0069  line 1698  negate-if  [PENDING]
```lean
- if edits.all (fun edit => fields.any (fun field => field.1 == edit.1)) then
+ if ¬(edits.all (fun edit => fields.any (fun field => field.1 == edit.1))) then
```

### m0070  line 1698  fallthrough-if(cond:=False)  [PENDING]
```lean
- if edits.all (fun edit => fields.any (fun field => field.1 == edit.1)) then
+ if False then
```

### m0073  line 1731  conjunct-&&-right:=true  [PENDING]
```lean
- if !viewed && current.isSome && edits.any (fun edit => edit.2.isSet) then throw .blindWrite
+ if !viewed && true && edits.any (fun edit => edit.2.isSet) then throw .blindWrite
```

### m0074  line 1731  conjunct-&&-left:=true  [PENDING]
```lean
- if !viewed && current.isSome && edits.any (fun edit => edit.2.isSet) then throw .blindWrite
+ if true && current.isSome && edits.any (fun edit => edit.2.isSet) then throw .blindWrite
```

### m0075  line 1731  conjunct-&&-right:=true  [PENDING]
```lean
- if !viewed && current.isSome && edits.any (fun edit => edit.2.isSet) then throw .blindWrite
+ if !viewed && current.isSome && true then throw .blindWrite
```

### m0076  line 1734  negate-if  [PENDING]
```lean
- if current.isNone then throw (.writeShape "the first yield must create the declared state")
+ if ¬(current.isNone) then throw (.writeShape "the first yield must create the declared state")
```

### m0088  line 1812  offbyone(<->≤)  [PENDING]
```lean
- if height + plan.patience < due then .error (.plan "a height await is due after its deadline") else
+ if height + plan.patience ≤ due then .error (.plan "a height await is due after its deadline") else
```

### m0089  line 2013  negate-if  [PENDING]
```lean
- if 0 < book.balance held asset then some (.transfer held account asset (book.balance held asset).toNat) else none
+ if ¬(0 < book.balance held asset) then some (.transfer held account asset (book.balance held asset).toNat) else none
```

### m0090  line 2013  fallthrough-if(cond:=False)  [PENDING]
```lean
- if 0 < book.balance held asset then some (.transfer held account asset (book.balance held asset).toNat) else none
+ if False then some (.transfer held account asset (book.balance held asset).toNat) else none
```

### m0091  line 2013  offbyone(<->≤)  [PENDING]
```lean
- if 0 < book.balance held asset then some (.transfer held account asset (book.balance held asset).toNat) else none
+ if 0 ≤ book.balance held asset then some (.transfer held account asset (book.balance held asset).toNat) else none
```

### m0097  line 2060  negate-if  [PENDING]
```lean
- if artifact.outputCodec ≠ codecId then throw (.packageType "not an activity artifact")
+ if ¬(artifact.outputCodec ≠ codecId) then throw (.packageType "not an activity artifact")
```

### m0098  line 2060  fallthrough-if(cond:=False)  [PENDING]
```lean
- if artifact.outputCodec ≠ codecId then throw (.packageType "not an activity artifact")
+ if False then throw (.packageType "not an activity artifact")
```

### m0099  line 2065  negate-if  [PENDING]
```lean
- if stored.payer = config.asset ∨ stored.payer = config.collector then throw .payerInvalid
+ if ¬(stored.payer = config.asset ∨ stored.payer = config.collector) then throw .payerInvalid
```

### m0100  line 2065  fallthrough-if(cond:=False)  [PENDING]
```lean
- if stored.payer = config.asset ∨ stored.payer = config.collector then throw .payerInvalid
+ if False then throw .payerInvalid
```

### m0101  line 2065  disjunct-∨-right:=false  [PENDING]
```lean
- if stored.payer = config.asset ∨ stored.payer = config.collector then throw .payerInvalid
+ if stored.payer = config.asset ∨ False then throw .payerInvalid
```

### m0102  line 2065  disjunct-∨-left:=false  [PENDING]
```lean
- if stored.payer = config.asset ∨ stored.payer = config.collector then throw .payerInvalid
+ if False ∨ stored.payer = config.collector then throw .payerInvalid
```

### m0104  line 2202  negate-if  [PENDING]
```lean
- | some _, .draining next _ => if next.migration.isSome then config.tariff.workOf next.envelope else 0
+ | some _, .draining next _ => if ¬(next.migration.isSome) then config.tariff.workOf next.envelope else 0
```

### m0105  line 2202  fallthrough-if(cond:=False)  [PENDING]
```lean
- | some _, .draining next _ => if next.migration.isSome then config.tariff.workOf next.envelope else 0
+ | some _, .draining next _ => if False then config.tariff.workOf next.envelope else 0
```

### m0106  line 2251  negate-if  [PENDING]
```lean
- (if request.deposit = 0 then [] else [.transfer request.account held config.asset request.deposit])
+ (if ¬(request.deposit = 0) then [] else [.transfer request.account held config.asset request.deposit])
```

### m0107  line 2251  fallthrough-if(cond:=False)  [PENDING]
```lean
- (if request.deposit = 0 then [] else [.transfer request.account held config.asset request.deposit])
+ (if False then [] else [.transfer request.account held config.asset request.deposit])
```

### m0108  line 2270  negate-if  [PENDING]
```lean
- if request.predecessor.isSome then 9 else 1
+ if ¬(request.predecessor.isSome) then 9 else 1
```

### m0109  line 2270  fallthrough-if(cond:=False)  [PENDING]
```lean
- if request.predecessor.isSome then 9 else 1
+ if False then 9 else 1
```

### m0114  line 2369  negate-if  [PENDING]
```lean
- if !config.covers request.resume then throw (.uncovered request.resume)
+ if ¬(!config.covers request.resume) then throw (.uncovered request.resume)
```

### m0115  line 2369  fallthrough-if(cond:=False)  [PENDING]
```lean
- if !config.covers request.resume then throw (.uncovered request.resume)
+ if False then throw (.uncovered request.resume)
```

### m0116  line 2370  negate-if  [PENDING]
```lean
- if !config.covers request.timeout then throw (.uncovered request.timeout)
+ if ¬(!config.covers request.timeout) then throw (.uncovered request.timeout)
```

### m0117  line 2370  fallthrough-if(cond:=False)  [PENDING]
```lean
- if !config.covers request.timeout then throw (.uncovered request.timeout)
+ if False then throw (.uncovered request.timeout)
```

### m0119  line 2374  negate-if  [PENDING]
```lean
- if request.resume.extractTicks < config.planBudget.ticks then
+ if ¬(request.resume.extractTicks < config.planBudget.ticks) then
```

### m0120  line 2374  fallthrough-if(cond:=False)  [PENDING]
```lean
- if request.resume.extractTicks < config.planBudget.ticks then
+ if False then
```

### m0121  line 2374  offbyone(<->≤)  [PENDING]
```lean
- if request.resume.extractTicks < config.planBudget.ticks then
+ if request.resume.extractTicks ≤ config.planBudget.ticks then
```

### m0123  line 2376  fallthrough-if(cond:=False)  [PENDING]
```lean
- if request.timeout.extractTicks < config.planBudget.ticks then
+ if False then
```

### m0125  line 2389  negate-if  [PENDING]
```lean
- if isRetired (snapshot.canonicalBytes cell) then throw .recordRetired
+ if ¬(isRetired (snapshot.canonicalBytes cell)) then throw .recordRetired
```

### m0126  line 2389  fallthrough-if(cond:=False)  [PENDING]
```lean
- if isRetired (snapshot.canonicalBytes cell) then throw .recordRetired
+ if False then throw .recordRetired
```

### m0127  line 2394  negate-if  [PENDING]
```lean
- if request.account = config.asset ∨ request.account = config.collector ∨ request.account = held then
+ if ¬(request.account = config.asset ∨ request.account = config.collector ∨ request.account = held) then
```

### m0128  line 2394  fallthrough-if(cond:=False)  [PENDING]
```lean
- if request.account = config.asset ∨ request.account = config.collector ∨ request.account = held then
+ if False then
```

### m0129  line 2394  disjunct-∨-right:=false  [PENDING]
```lean
- if request.account = config.asset ∨ request.account = config.collector ∨ request.account = held then
+ if request.account = config.asset ∨ False ∨ request.account = held then
```

### m0130  line 2394  disjunct-∨-left:=false  [PENDING]
```lean
- if request.account = config.asset ∨ request.account = config.collector ∨ request.account = held then
+ if False ∨ request.account = config.collector ∨ request.account = held then
```

### m0131  line 2394  disjunct-∨-right:=false  [PENDING]
```lean
- if request.account = config.asset ∨ request.account = config.collector ∨ request.account = held then
+ if request.account = config.asset ∨ request.account = config.collector ∨ False then
```

### m0132  line 2399  negate-if  [PENDING]
```lean
- if held ∈ (logicalBook book.logical).accounts then throw .purseTaken
+ if ¬(held ∈ (logicalBook book.logical).accounts) then throw .purseTaken
```

### m0133  line 2399  fallthrough-if(cond:=False)  [PENDING]
```lean
- if held ∈ (logicalBook book.logical).accounts then throw .purseTaken
+ if False then throw .purseTaken
```

### m0137  line 2544  negate-if  [PENDING]
```lean
- if named ≠ slot then throw .slotMismatch
+ if ¬(named ≠ slot) then throw .slotMismatch
```

### m0139  line 2614  negate-if  [PENDING]
```lean
- if slot.name ≠ slotName ∨ slot.activity ≠ cell then .error .slotMismatch else
+ if ¬(slot.name ≠ slotName ∨ slot.activity ≠ cell) then .error .slotMismatch else
```

### m0140  line 2614  fallthrough-if(cond:=False)  [PENDING]
```lean
- if slot.name ≠ slotName ∨ slot.activity ≠ cell then .error .slotMismatch else
+ if False then .error .slotMismatch else
```

### m0141  line 2614  disjunct-∨-right:=false  [PENDING]
```lean
- if slot.name ≠ slotName ∨ slot.activity ≠ cell then .error .slotMismatch else
+ if slot.name ≠ slotName ∨ False then .error .slotMismatch else
```

### m0142  line 2614  disjunct-∨-left:=false  [PENDING]
```lean
- if slot.name ≠ slotName ∨ slot.activity ≠ cell then .error .slotMismatch else
+ if False ∨ slot.activity ≠ cell then .error .slotMismatch else
```

### m0143  line 2618  negate-if  [PENDING]
```lean
- pure ⟨if decision = .expired then .timedOut else .resumed, outcome,
+ pure ⟨if ¬(decision = .expired) then .timedOut else .resumed, outcome,
```

### m0144  line 2618  fallthrough-if(cond:=False)  [PENDING]
```lean
- pure ⟨if decision = .expired then .timedOut else .resumed, outcome,
+ pure ⟨if False then .timedOut else .resumed, outcome,
```

### m0145  line 2626  negate-if  [PENDING]
```lean
- if await.deadline < height then .ok ⟨.timedOut, .timedOut, [], [], []⟩
+ if ¬(await.deadline < height) then .ok ⟨.timedOut, .timedOut, [], [], []⟩
```

### m0146  line 2626  fallthrough-if(cond:=False)  [PENDING]
```lean
- if await.deadline < height then .ok ⟨.timedOut, .timedOut, [], [], []⟩
+ if False then .ok ⟨.timedOut, .timedOut, [], [], []⟩
```

### m0148  line 2627  negate-if  [PENDING]
```lean
- else if due ≤ height then .ok ⟨.resumed, .reply (.record [("at", .natural height)]), [], [], []⟩
+ else if ¬(due ≤ height) then .ok ⟨.resumed, .reply (.record [("at", .natural height)]), [], [], []⟩
```

### m0149  line 2627  fallthrough-if(cond:=False)  [PENDING]
```lean
- else if due ≤ height then .ok ⟨.resumed, .reply (.record [("at", .natural height)]), [], [], []⟩
+ else if False then .ok ⟨.resumed, .reply (.record [("at", .natural height)]), [], [], []⟩
```

### m0150  line 2627  offbyone(≤-><)  [PENDING]
```lean
- else if due ≤ height then .ok ⟨.resumed, .reply (.record [("at", .natural height)]), [], [], []⟩
+ else if due < height then .ok ⟨.resumed, .reply (.record [("at", .natural height)]), [], [], []⟩
```

### m0152  line 2644  fallthrough-if(cond:=False)  [PENDING]
```lean
- (if request.extra = zeroCapacity then []
+ (if False then []
```

### m0153  line 2646  negate-if  [PENDING]
```lean
- (if migration = 0 then [] else [.fee (heldAccount cell) config.collector config.asset migration]), []⟩
+ (if ¬(migration = 0) then [] else [.fee (heldAccount cell) config.collector config.asset migration]), []⟩
```

### m0154  line 2646  fallthrough-if(cond:=False)  [PENDING]
```lean
- (if migration = 0 then [] else [.fee (heldAccount cell) config.collector config.asset migration]), []⟩
+ (if False then [] else [.fee (heldAccount cell) config.collector config.asset migration]), []⟩
```

### m0155  line 2757  negate-if  [PENDING]
```lean
- if head.await.id = awaitId' then
+ if ¬(head.await.id = awaitId') then
```

### m0156  line 2757  fallthrough-if(cond:=False)  [PENDING]
```lean
- if head.await.id = awaitId' then
+ if False then
```

### m0159  line 2865  negate-if  [PENDING]
```lean
- if 0 < record.tried ∧ envelope.sourceTicks ≤ record.tried then .error (.alreadyExhausted record.tried envelope.sourceTicks) else
+ if ¬(0 < record.tried ∧ envelope.sourceTicks ≤ record.tried) then .error (.alreadyExhausted record.tried envelope.sourceTicks) else
```

### m0160  line 2865  fallthrough-if(cond:=False)  [PENDING]
```lean
- if 0 < record.tried ∧ envelope.sourceTicks ≤ record.tried then .error (.alreadyExhausted record.tried envelope.sourceTicks) else
+ if False then .error (.alreadyExhausted record.tried envelope.sourceTicks) else
```

### m0161  line 2865  conjunct-∧-right:=true  [PENDING]
```lean
- if 0 < record.tried ∧ envelope.sourceTicks ≤ record.tried then .error (.alreadyExhausted record.tried envelope.sourceTicks) else
+ if 0 < record.tried ∧ True then .error (.alreadyExhausted record.tried envelope.sourceTicks) else
```

### m0162  line 2865  conjunct-∧-left:=true  [PENDING]
```lean
- if 0 < record.tried ∧ envelope.sourceTicks ≤ record.tried then .error (.alreadyExhausted record.tried envelope.sourceTicks) else
+ if True ∧ envelope.sourceTicks ≤ record.tried then .error (.alreadyExhausted record.tried envelope.sourceTicks) else
```

### m0163  line 2865  offbyone(≤-><)  [PENDING]
```lean
- if 0 < record.tried ∧ envelope.sourceTicks ≤ record.tried then .error (.alreadyExhausted record.tried envelope.sourceTicks) else
+ if 0 < record.tried ∧ envelope.sourceTicks < record.tried then .error (.alreadyExhausted record.tried envelope.sourceTicks) else
```

### m0164  line 2865  offbyone(<->≤)  [PENDING]
```lean
- if 0 < record.tried ∧ envelope.sourceTicks ≤ record.tried then .error (.alreadyExhausted record.tried envelope.sourceTicks) else
+ if 0 ≤ record.tried ∧ envelope.sourceTicks ≤ record.tried then .error (.alreadyExhausted record.tried envelope.sourceTicks) else
```

### m0165  line 2955  negate-if  [PENDING]
```lean
- (if record.tried = 0 then record.escrow.used path else 0) +
+ (if ¬(record.tried = 0) then record.escrow.used path else 0) +
```

### m0166  line 2955  fallthrough-if(cond:=False)  [PENDING]
```lean
- (if record.tried = 0 then record.escrow.used path else 0) +
+ (if False then record.escrow.used path else 0) +
```

### m0167  line 2956  negate-if  [PENDING]
```lean
- (if request.extra = zeroCapacity then 0 else config.tariff.workOf request.extra)
+ (if ¬(request.extra = zeroCapacity) then 0 else config.tariff.workOf request.extra)
```

### m0168  line 2956  fallthrough-if(cond:=False)  [PENDING]
```lean
- (if request.extra = zeroCapacity then 0 else config.tariff.workOf request.extra)
+ (if False then 0 else config.tariff.workOf request.extra)
```

### m0177  line 3124  negate-if  [PENDING]
```lean
- if fee = 0 then [] else [.fee (heldAccount cell) config.collector config.asset fee]
+ if ¬(fee = 0) then [] else [.fee (heldAccount cell) config.collector config.asset fee]
```

### m0178  line 3124  fallthrough-if(cond:=False)  [PENDING]
```lean
- if fee = 0 then [] else [.fee (heldAccount cell) config.collector config.asset fee]
+ if False then [] else [.fee (heldAccount cell) config.collector config.asset fee]
```

### m0180  line 3235  negate-if  [PENDING]
```lean
- if request.amount = 0 then .error .zeroAmount else
+ if ¬(request.amount = 0) then .error .zeroAmount else
```

### m0181  line 3235  fallthrough-if(cond:=False)  [PENDING]
```lean
- if request.amount = 0 then .error .zeroAmount else
+ if False then .error .zeroAmount else
```

### m0182  line 3236  negate-if  [PENDING]
```lean
- if request.account = config.asset ∨ request.account = heldAccount request.record then .error .payerInvalid else
+ if ¬(request.account = config.asset ∨ request.account = heldAccount request.record) then .error .payerInvalid else
```

### m0183  line 3236  fallthrough-if(cond:=False)  [PENDING]
```lean
- if request.account = config.asset ∨ request.account = heldAccount request.record then .error .payerInvalid else
+ if False then .error .payerInvalid else
```

### m0184  line 3236  disjunct-∨-right:=false  [PENDING]
```lean
- if request.account = config.asset ∨ request.account = heldAccount request.record then .error .payerInvalid else
+ if request.account = config.asset ∨ False then .error .payerInvalid else
```

### m0186  line 3291  negate-if  [PENDING]
```lean
- if request.account = config.asset ∨ request.account = config.collector then .error .payerInvalid else
+ if ¬(request.account = config.asset ∨ request.account = config.collector) then .error .payerInvalid else
```

### m0187  line 3291  fallthrough-if(cond:=False)  [PENDING]
```lean
- if request.account = config.asset ∨ request.account = config.collector then .error .payerInvalid else
+ if False then .error .payerInvalid else
```

### m0188  line 3291  disjunct-∨-right:=false  [PENDING]
```lean
- if request.account = config.asset ∨ request.account = config.collector then .error .payerInvalid else
+ if request.account = config.asset ∨ False then .error .payerInvalid else
```

### m0189  line 3291  disjunct-∨-left:=false  [PENDING]
```lean
- if request.account = config.asset ∨ request.account = config.collector then .error .payerInvalid else
+ if False ∨ request.account = config.collector then .error .payerInvalid else
```


## Kernel/ObjectiveActivityReceiver.lean  (25)

### m0192  line 566  negate-if  [PENDING]
```lean
- if delivery.await.id ≠ await then throw .staleAwait
+ if ¬(delivery.await.id ≠ await) then throw .staleAwait
```

### m0193  line 566  fallthrough-if(cond:=False)  [PENDING]
```lean
- if delivery.await.id ≠ await then throw .staleAwait
+ if False then throw .staleAwait
```

### m0194  line 574  negate-if  [PENDING]
```lean
- if exhausted.await.id ≠ await then throw .staleAwait
+ if ¬(exhausted.await.id ≠ await) then throw .staleAwait
```

### m0195  line 574  fallthrough-if(cond:=False)  [PENDING]
```lean
- if exhausted.await.id ≠ await then throw .staleAwait
+ if False then throw .staleAwait
```

### m0196  line 579  negate-if  [PENDING]
```lean
- if abandoned.await.id ≠ await then throw .staleAwait
+ if ¬(abandoned.await.id ≠ await) then throw .staleAwait
```

### m0197  line 579  fallthrough-if(cond:=False)  [PENDING]
```lean
- if abandoned.await.id ≠ await then throw .staleAwait
+ if False then throw .staleAwait
```

### m0198  line 602  negate-if  [PENDING]
```lean
- if aborted.await.id ≠ await then throw .staleAwait
+ if ¬(aborted.await.id ≠ await) then throw .staleAwait
```

### m0199  line 602  fallthrough-if(cond:=False)  [PENDING]
```lean
- if aborted.await.id ≠ await then throw .staleAwait
+ if False then throw .staleAwait
```

### m0200  line 607  negate-if  [PENDING]
```lean
- if reborn.await.id ≠ await then throw .staleAwait
+ if ¬(reborn.await.id ≠ await) then throw .staleAwait
```

### m0201  line 607  fallthrough-if(cond:=False)  [PENDING]
```lean
- if reborn.await.id ≠ await then throw .staleAwait
+ if False then throw .staleAwait
```

### m0203  line 737  fallthrough-if(cond:=False)  [PENDING]
```lean
- if objectHolder snapshot semantics ambient command o c preRoot outcome then .ok () else .error .notObjectHolder
+ if False then .ok () else .error .notObjectHolder
```

### m0205  line 739  fallthrough-if(cond:=False)  [PENDING]
```lean
- if accountHolder snapshot semantics ambient command a c preRoot outcome then .ok () else .error .notAccountOwner
+ if False then .ok () else .error .notAccountOwner
```

### m0206  line 744  negate-if  [PENDING]
```lean
- | .abortDrained _ _ extra a ac => if extra = zeroCapacity then .ok () else account a ac
+ | .abortDrained _ _ extra a ac => if ¬(extra = zeroCapacity) then .ok () else account a ac
```

### m0207  line 744  fallthrough-if(cond:=False)  [PENDING]
```lean
- | .abortDrained _ _ extra a ac => if extra = zeroCapacity then .ok () else account a ac
+ | .abortDrained _ _ extra a ac => if False then .ok () else account a ac
```

### m0208  line 749  negate-if  [PENDING]
```lean
- if extra = zeroCapacity then .ok () else account a ac
+ if ¬(extra = zeroCapacity) then .ok () else account a ac
```

### m0209  line 749  fallthrough-if(cond:=False)  [PENDING]
```lean
- if extra = zeroCapacity then .ok () else account a ac
+ if False then .ok () else account a ac
```

### m0210  line 790  negate-if  [PENDING]
```lean
- if (price : Int) ≤ available then .ok () else .error (.kernel (.unfunded available price))
+ if ¬((price : Int) ≤ available) then .ok () else .error (.kernel (.unfunded available price))
```

### m0211  line 790  fallthrough-if(cond:=False)  [PENDING]
```lean
- if (price : Int) ≤ available then .ok () else .error (.kernel (.unfunded available price))
+ if False then .ok () else .error (.kernel (.unfunded available price))
```

### m0214  line 814  fallthrough-if(cond:=False)  [PENDING]
```lean
- if command.expectedAuthorityRoot ≠ snapshot.cell.root then throw .staleAuthority
+ if False then throw .staleAuthority
```

### m0223  line 1455  conjunct-&&-right:=true  [PENDING]
```lean
- { snapshot with spent := fun n => n != claimed && snapshot.spent n }
+ { snapshot with spent := fun n => n != claimed && true}
```

### m0224  line 1455  conjunct-&&-left:=true  [PENDING]
```lean
- { snapshot with spent := fun n => n != claimed && snapshot.spent n }
+ { snapshot with spent := fun n => true && snapshot.spent n }
```

### m0225  line 1553  negate-if  [PENDING]
```lean
- if chargedCause reason && (failureRequest deployment.domain profile.semantics command).isSome then
+ if ¬(chargedCause reason && (failureRequest deployment.domain profile.semantics command).isSome) then
```

### m0226  line 1553  fallthrough-if(cond:=False)  [PENDING]
```lean
- if chargedCause reason && (failureRequest deployment.domain profile.semantics command).isSome then
+ if False then
```

### m0227  line 1553  conjunct-&&-right:=true  [PENDING]
```lean
- if chargedCause reason && (failureRequest deployment.domain profile.semantics command).isSome then
+ if chargedCause reason && true then
```

### m0228  line 1553  conjunct-&&-left:=true  [PENDING]
```lean
- if chargedCause reason && (failureRequest deployment.domain profile.semantics command).isSome then
+ if true && (failureRequest deployment.domain profile.semantics command).isSome then
```


## Kernel/ObjectiveActivityUpgrade.lean  (10)

### m0230  line 114  fallthrough-if(cond:=False)  [PENDING]
```lean
- | index, floor :: rest => if floorEntailed law floor then firstUnentailed law (index + 1) rest else some index
+ | index, floor :: rest => if False then firstUnentailed law (index + 1) rest else some index
```

### m0231  line 148  negate-if  [PENDING]
```lean
- | .get (.bound index) name => if index = depth then [name] else []
+ | .get (.bound index) name => if ¬(index = depth) then [name] else []
```

### m0232  line 148  fallthrough-if(cond:=False)  [PENDING]
```lean
- | .get (.bound index) name => if index = depth then [name] else []
+ | .get (.bound index) name => if False then [name] else []
```

### m0233  line 186  conjunct-&&-right:=true  [PENDING]
```lean
- (topFields oldType).filter (fun field => !(reads.contains field) && !(dropped.contains field))
+ (topFields oldType).filter (fun field => !(reads.contains field) && true)
```

### m0234  line 186  conjunct-&&-left:=true  [PENDING]
```lean
- (topFields oldType).filter (fun field => !(reads.contains field) && !(dropped.contains field))
+ (topFields oldType).filter (fun field => true && !(dropped.contains field))
```

### m0239  line 264  negate-if  [PENDING]
```lean
- | none => if stateSubtype record.stateType next.stateType then .ok () else .error .notSubtype
+ | none => if ¬(stateSubtype record.stateType next.stateType) then .ok () else .error .notSubtype
```

### m0240  line 264  fallthrough-if(cond:=False)  [PENDING]
```lean
- | none => if stateSubtype record.stateType next.stateType then .ok () else .error .notSubtype
+ | none => if False then .ok () else .error .notSubtype
```

### m0252  line 468  negate-if  [PENDING]
```lean
- if next.migration.isSome then config.tariff.workOf next.envelope else 0
+ if ¬(next.migration.isSome) then config.tariff.workOf next.envelope else 0
```

### m0253  line 468  fallthrough-if(cond:=False)  [PENDING]
```lean
- if next.migration.isSome then config.tariff.workOf next.envelope else 0
+ if False then config.tariff.workOf next.envelope else 0
```

### m0255  line 471  fallthrough-if(cond:=False)  [PENDING]
```lean
- ⟨[], if migrateFee config next = 0 then [] else
+ ⟨[], if False then [] else
```


## Kernel/ObjectiveActivityWire.lean  (1)

### m0266  line 188  conjunct-&&-left:=true  [PENDING]
```lean
- if rest.isEmpty && dataBytes data == bytes then some data else none
+ if true && dataBytes data == bytes then some data else none
```


## Kernel/ObjectiveCall.lean  (23)

### m0267  line 296  conjunct-&&-right:=true  [PENDING]
```lean
- | some labels => !labels.isEmpty && labels.all (fun label => allowed.contains label)
+ | some labels => !labels.isEmpty && true
```

### m0268  line 296  conjunct-&&-left:=true  [PENDING]
```lean
- | some labels => !labels.isEmpty && labels.all (fun label => allowed.contains label)
+ | some labels => true && labels.all (fun label => allowed.contains label)
```

### m0293  line 1049  negate-if  [PENDING]
```lean
- else if callDepth ≤ stack.length then .error (.depth callDepth, journal.meter)
+ else if ¬(callDepth ≤ stack.length) then .error (.depth callDepth, journal.meter)
```

### m0295  line 1049  offbyone(≤-><)  [PENDING]
```lean
- else if callDepth ≤ stack.length then .error (.depth callDepth, journal.meter)
+ else if callDepth < stack.length then .error (.depth callDepth, journal.meter)
```

### m0299  line 1225  conjunct-&&-left:=true  [PENDING]
```lean
- | some held => .ok (held, mail.inboxes.filter (fun other => !(other.sender == sender && other.target == target)))
+ | some held => .ok (held, mail.inboxes.filter (fun other => !(true && other.target == target)))
```

### m0300  line 1244  disjunct-||-right:=false  [PENDING]
```lean
- if taken : (payloadOf bytes).isSome || isRetired bytes || mail.slots.any (fun held => held.name == name) then
+ if taken : (payloadOf bytes).isSome || false || mail.slots.any (fun held => held.name == name) then
```

### m0302  line 1244  disjunct-||-right:=false  [PENDING]
```lean
- if taken : (payloadOf bytes).isSome || isRetired bytes || mail.slots.any (fun held => held.name == name) then
+ if taken : (payloadOf bytes).isSome || isRetired bytes || false then
```

### m0303  line 1283  negate-if  [PENDING]
```lean
- if message.continues then ["call", "send"] else ["call"]
+ if ¬(message.continues) then ["call", "send"] else ["call"]
```

### m0304  line 1283  fallthrough-if(cond:=False)  [PENDING]
```lean
- if message.continues then ["call", "send"] else ["call"]
+ if False then ["call", "send"] else ["call"]
```

### m0305  line 1339  negate-if  [PENDING]
```lean
- else if !labelsWithin method.applied.assumptions method.planType ["call", "send"] then
+ else if ¬(!labelsWithin method.applied.assumptions method.planType ["call", "send"]) then
```

### m0306  line 1339  fallthrough-if(cond:=False)  [PENDING]
```lean
- else if !labelsWithin method.applied.assumptions method.planType ["call", "send"] then
+ else if False then
```

### m0307  line 1342  negate-if  [PENDING]
```lean
- else if Inbox.continuationDepth ≤ message.depth then .error (.continuationDepth Inbox.continuationDepth, meterAfter)
+ else if ¬(Inbox.continuationDepth ≤ message.depth) then .error (.continuationDepth Inbox.continuationDepth, meterAfter)
```

### m0308  line 1342  fallthrough-if(cond:=False)  [PENDING]
```lean
- else if Inbox.continuationDepth ≤ message.depth then .error (.continuationDepth Inbox.continuationDepth, meterAfter)
+ else if False then .error (.continuationDepth Inbox.continuationDepth, meterAfter)
```

### m0309  line 1342  offbyone(≤-><)  [PENDING]
```lean
- else if Inbox.continuationDepth ≤ message.depth then .error (.continuationDepth Inbox.continuationDepth, meterAfter)
+ else if Inbox.continuationDepth < message.depth then .error (.continuationDepth Inbox.continuationDepth, meterAfter)
```

### m0310  line 1411  negate-if  [PENDING]
```lean
- if !held.now.watched then .error (.notPipelinable name.value, mail.frontEnd) else
+ if ¬(!held.now.watched) then .error (.notPipelinable name.value, mail.frontEnd) else
```

### m0311  line 1411  fallthrough-if(cond:=False)  [PENDING]
```lean
- if !held.now.watched then .error (.notPipelinable name.value, mail.frontEnd) else
+ if False then .error (.notPipelinable name.value, mail.frontEnd) else
```

### m0312  line 1412  negate-if  [PENDING]
```lean
- if held.now.queued.length < Inbox.bound then
+ if ¬(held.now.queued.length < Inbox.bound) then
```

### m0313  line 1412  fallthrough-if(cond:=False)  [PENDING]
```lean
- if held.now.queued.length < Inbox.bound then
+ if False then
```

### m0314  line 1412  offbyone(<->≤)  [PENDING]
```lean
- if held.now.queued.length < Inbox.bound then
+ if held.now.queued.length ≤ Inbox.bound then
```

### m0317  line 1481  negate-if  [PENDING]
```lean
- if mail.closed.any (fun closed => closed.name == name) then .ok .gone else
+ if ¬(mail.closed.any (fun closed => closed.name == name)) then .ok .gone else
```

### m0318  line 1481  fallthrough-if(cond:=False)  [PENDING]
```lean
- if mail.closed.any (fun closed => closed.name == name) then .ok .gone else
+ if False then .ok .gone else
```

### m0319  line 1488  negate-if  [PENDING]
```lean
- if isRetired (snapshot.canonicalBytes (AnswerSlot.cell config.domain name)) then .ok .gone else
+ if ¬(isRetired (snapshot.canonicalBytes (AnswerSlot.cell config.domain name))) then .ok .gone else
```

### m0320  line 1488  fallthrough-if(cond:=False)  [PENDING]
```lean
- if isRetired (snapshot.canonicalBytes (AnswerSlot.cell config.domain name)) then .ok .gone else
+ if False then .ok .gone else
```


## Kernel/ObjectiveDomain.lean  (3)

### m0385  line 692  negate-if  [PENDING]
```lean
- if record.domains.length < domainsPerObject then .ok () else .error (.memberDomainsFull member.value)
+ if ¬(record.domains.length < domainsPerObject) then .ok () else .error (.memberDomainsFull member.value)
```

### m0386  line 692  fallthrough-if(cond:=False)  [PENDING]
```lean
- if record.domains.length < domainsPerObject then .ok () else .error (.memberDomainsFull member.value)
+ if False then .ok () else .error (.memberDomainsFull member.value)
```

### m0387  line 692  offbyone(<->≤)  [PENDING]
```lean
- if record.domains.length < domainsPerObject then .ok () else .error (.memberDomainsFull member.value)
+ if record.domains.length ≤ domainsPerObject then .ok () else .error (.memberDomainsFull member.value)
```


## Kernel/ObjectiveSend.lean  (5)

### m0343  line 109  conjunct-&&-left:=true  [PENDING]
```lean
- if journal.controls.isEmpty && journal.drained then .replied result journal
+ if true && journal.drained then .replied result journal
```

### m0344  line 110  negate-if  [PENDING]
```lean
- else .failed (if !journal.controls.isEmpty then
+ else .failed (if ¬(!journal.controls.isEmpty) then
```

### m0345  line 110  fallthrough-if(cond:=False)  [PENDING]
```lean
- else .failed (if !journal.controls.isEmpty then
+ else .failed (if False then
```

### m0351  line 146  offbyone(<->≤)  [PENDING]
```lean
- else if Inbox.fanOut < outs.length then some (.fanOut Inbox.fanOut)
+ else if Inbox.fanOut ≤ outs.length then some (.fanOut Inbox.fanOut)
```

### m0354  line 147  offbyone(<->≤)  [PENDING]
```lean
- else if message.allowance < onwardEscrow config message outs then
+ else if message.allowance ≤ onwardEscrow config message outs then
```


## Kernel/PayEnrolReceiver.lean  (2)

### m0445  line 875  negate-if  [PENDING]
```lean
- if command.expectedAuthorityRoot = snapshot.cell.root then
+ if ¬(command.expectedAuthorityRoot = snapshot.cell.root) then
```

### m0446  line 875  fallthrough-if(cond:=False)  [PENDING]
```lean
- if command.expectedAuthorityRoot = snapshot.cell.root then
+ if False then
```


## Kernel/SeatStore.lean  (47)

### m0448  line 192  negate-if  [PENDING]
```lean
- if payload.role = role then some payload.body else none
+ if ¬(payload.role = role) then some payload.body else none
```

### m0449  line 192  fallthrough-if(cond:=False)  [PENDING]
```lean
- if payload.role = role then some payload.body else none
+ if False then some payload.body else none
```

### m0450  line 214  negate-if  [PENDING]
```lean
- if payload.role = .seat then
+ if ¬(payload.role = .seat) then
```

### m0451  line 214  fallthrough-if(cond:=False)  [PENDING]
```lean
- if payload.role = .seat then
+ if False then
```

### m0452  line 216  negate-if  [PENDING]
```lean
- if body.seat.account = account then some body else none
+ if ¬(body.seat.account = account) then some body else none
```

### m0453  line 216  fallthrough-if(cond:=False)  [PENDING]
```lean
- if body.seat.account = account then some body else none
+ if False then some body else none
```

### m0454  line 416  negate-if  [PENDING]
```lean
- if !config.covers envelope then throw (.uncovered envelope)
+ if ¬(!config.covers envelope) then throw (.uncovered envelope)
```

### m0455  line 416  fallthrough-if(cond:=False)  [PENDING]
```lean
- if !config.covers envelope then throw (.uncovered envelope)
+ if False then throw (.uncovered envelope)
```

### m0456  line 417  negate-if  [PENDING]
```lean
- if envelope.extractTicks < config.planBudget.ticks then
+ if ¬(envelope.extractTicks < config.planBudget.ticks) then
```

### m0458  line 417  offbyone(<->≤)  [PENDING]
```lean
- if envelope.extractTicks < config.planBudget.ticks then
+ if envelope.extractTicks ≤ config.planBudget.ticks then
```

### m0460  line 459  disjunct-||-left:=false  [PENDING]
```lean
- base.filter (fun account => !loaded.contains account || next.any fun seat => seat.account == account) ++
+ base.filter (fun account => false || next.any fun seat => seat.account == account) ++
```

### m0461  line 460  conjunct-&&-right:=true  [PENDING]
```lean
- ((next.filter fun seat => seat.inst == inst && !(base.contains seat.account)).map Seat.account)
+ ((next.filter fun seat => seat.inst == inst && true).map Seat.account)
```

### m0462  line 460  conjunct-&&-left:=true  [PENDING]
```lean
- ((next.filter fun seat => seat.inst == inst && !(base.contains seat.account)).map Seat.account)
+ ((next.filter fun seat => true && !(base.contains seat.account)).map Seat.account)
```

### m0463  line 464  negate-if  [PENDING]
```lean
- if bytes = snapshot.canonicalBytes cell then none else some (postAt snapshot cell bytes)
+ if ¬(bytes = snapshot.canonicalBytes cell) then none else some (postAt snapshot cell bytes)
```

### m0464  line 464  fallthrough-if(cond:=False)  [PENDING]
```lean
- if bytes = snapshot.canonicalBytes cell then none else some (postAt snapshot cell bytes)
+ if False then none else some (postAt snapshot cell bytes)
```

### m0465  line 487  negate-if  [PENDING]
```lean
- if loaded.seats.any (fun body => body.seat.account == seat.account) then none
+ if ¬(loaded.seats.any (fun body => body.seat.account == seat.account)) then none
```

### m0466  line 487  fallthrough-if(cond:=False)  [PENDING]
```lean
- if loaded.seats.any (fun body => body.seat.account == seat.account) then none
+ if False then none
```

### m0467  line 493  negate-if  [PENDING]
```lean
- if next.registry.spent.contains body.invitation.id then some { body with spent := true } else none
+ if ¬(next.registry.spent.contains body.invitation.id) then some { body with spent := true } else none
```

### m0468  line 493  fallthrough-if(cond:=False)  [PENDING]
```lean
- if next.registry.spent.contains body.invitation.id then some { body with spent := true } else none
+ if False then some { body with spent := true } else none
```

### m0469  line 675  negate-if  [PENDING]
```lean
- if batch = noPostings then []
+ if ¬(batch = noPostings) then []
```

### m0470  line 675  fallthrough-if(cond:=False)  [PENDING]
```lean
- if batch = noPostings then []
+ if False then []
```

### m0471  line 786  negate-if  [PENDING]
```lean
- if present snapshot (instanceCell domain inst) then
+ if ¬(present snapshot (instanceCell domain inst)) then
```

### m0472  line 786  fallthrough-if(cond:=False)  [PENDING]
```lean
- if present snapshot (instanceCell domain inst) then
+ if False then
```

### m0473  line 788  negate-if  [PENDING]
```lean
- | some body => if body.inst.id = inst then .ok (some body) else .error (.cellUndecodable (instanceCell domain inst).value)
+ | some body => if ¬(body.inst.id = inst) then .ok (some body) else .error (.cellUndecodable (instanceCell domain inst).value)
```

### m0474  line 788  fallthrough-if(cond:=False)  [PENDING]
```lean
- | some body => if body.inst.id = inst then .ok (some body) else .error (.cellUndecodable (instanceCell domain inst).value)
+ | some body => if False then .ok (some body) else .error (.cellUndecodable (instanceCell domain inst).value)
```

### m0475  line 794  negate-if  [PENDING]
```lean
- if present snapshot (invitationCell domain id) then
+ if ¬(present snapshot (invitationCell domain id)) then
```

### m0476  line 794  fallthrough-if(cond:=False)  [PENDING]
```lean
- if present snapshot (invitationCell domain id) then
+ if False then
```

### m0477  line 796  negate-if  [PENDING]
```lean
- | some body => if body.invitation.id = id then .ok (some body)
+ | some body => if ¬(body.invitation.id = id) then .ok (some body)
```

### m0478  line 796  fallthrough-if(cond:=False)  [PENDING]
```lean
- | some body => if body.invitation.id = id then .ok (some body)
+ | some body => if False then .ok (some body)
```

### m0479  line 803  negate-if  [PENDING]
```lean
- if present snapshot (seatCell account) then
+ if ¬(present snapshot (seatCell account)) then
```

### m0480  line 803  fallthrough-if(cond:=False)  [PENDING]
```lean
- if present snapshot (seatCell account) then
+ if False then
```

### m0485  line 880  negate-if  [PENDING]
```lean
- if artifact.outputCodec ≠ contractCodecId then throw (.notAContract "the artifact is not a contract package")
+ if ¬(artifact.outputCodec ≠ contractCodecId) then throw (.notAContract "the artifact is not a contract package")
```

### m0486  line 880  fallthrough-if(cond:=False)  [PENDING]
```lean
- if artifact.outputCodec ≠ contractCodecId then throw (.notAContract "the artifact is not a contract package")
+ if False then throw (.notAContract "the artifact is not a contract package")
```

### m0487  line 883  negate-if  [PENDING]
```lean
- if present snapshot cell then throw .packageExists
+ if ¬(present snapshot cell) then throw .packageExists
```

### m0488  line 883  fallthrough-if(cond:=False)  [PENDING]
```lean
- if present snapshot cell then throw .packageExists
+ if False then throw .packageExists
```

### m0490  line 884  disjunct-∨-left:=false  [PENDING]
```lean
- if stored.payer = config.asset ∨ stored.payer = config.collector ∨ reservedBase ≤ stored.payer ∨
+ if False ∨ stored.payer = config.collector ∨ reservedBase ≤ stored.payer ∨
```

### m0491  line 884  disjunct-∨-right:=false  [PENDING]
```lean
- if stored.payer = config.asset ∨ stored.payer = config.collector ∨ reservedBase ≤ stored.payer ∨
+ if stored.payer = config.asset ∨ stored.payer = config.collector ∨ False ∨
```

### m0492  line 884  offbyone(≤-><)  [PENDING]
```lean
- if stored.payer = config.asset ∨ stored.payer = config.collector ∨ reservedBase ≤ stored.payer ∨
+ if stored.payer = config.asset ∨ stored.payer = config.collector ∨ reservedBase < stored.payer ∨
```

### m0493  line 896  negate-if  [PENDING]
```lean
- if !present snapshot (packageCell domain pin) then throw .packageMissing
+ if ¬(!present snapshot (packageCell domain pin)) then throw .packageMissing
```

### m0494  line 896  fallthrough-if(cond:=False)  [PENDING]
```lean
- if !present snapshot (packageCell domain pin) then throw .packageMissing
+ if False then throw .packageMissing
```

### m0495  line 921  negate-if  [PENDING]
```lean
- if body.retired then throw (.instanceMissing inst)
+ if ¬(body.retired) then throw (.instanceMissing inst)
```

### m0496  line 921  fallthrough-if(cond:=False)  [PENDING]
```lean
- if body.retired then throw (.instanceMissing inst)
+ if False then throw (.instanceMissing inst)
```

### m0498  line 922  fallthrough-if(cond:=False)  [PENDING]
```lean
- if reservedBase ≤ account ∨ account = config.collector ∨ account = config.asset then throw (.payerInvalid account)
+ if False then throw (.payerInvalid account)
```

### m0499  line 922  disjunct-∨-right:=false  [PENDING]
```lean
- if reservedBase ≤ account ∨ account = config.collector ∨ account = config.asset then throw (.payerInvalid account)
+ if reservedBase ≤ account ∨ False ∨ account = config.asset then throw (.payerInvalid account)
```

### m0500  line 922  disjunct-∨-left:=false  [PENDING]
```lean
- if reservedBase ≤ account ∨ account = config.collector ∨ account = config.asset then throw (.payerInvalid account)
+ if False ∨ account = config.collector ∨ account = config.asset then throw (.payerInvalid account)
```

### m0501  line 922  disjunct-∨-right:=false  [PENDING]
```lean
- if reservedBase ≤ account ∨ account = config.collector ∨ account = config.asset then throw (.payerInvalid account)
+ if reservedBase ≤ account ∨ account = config.collector ∨ False then throw (.payerInvalid account)
```

### m0502  line 922  offbyone(≤-><)  [PENDING]
```lean
- if reservedBase ≤ account ∨ account = config.collector ∨ account = config.asset then throw (.payerInvalid account)
+ if reservedBase < account ∨ account = config.collector ∨ account = config.asset then throw (.payerInvalid account)
```


NOT RUN (phase 1): 53 mutants (shards 6-8 on burst2-a still in progress at wind-down).
Owner routing: Kernel/Pay*, ResourceBirth*, NativeHostContext = DEPUTY-KERNEL; Kernel/Seat*, Objective*, Inbox, AnswerSlot, ReceivingLaw = DEPUTY-OB-ENG.
Journey phase (mut-journey.sh) had only just been launched on mut-w1 (burst2-b); expect all survivors to read PENDING.
