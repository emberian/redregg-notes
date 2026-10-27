import Lean
import Minidregg
import Assurance
import Host
import Selvage
import Verify
import SimplexQualification
import ObjectiveProofs
import Deployed
import AxiomCensus
import AxiomCensusResearch
import TokenCensus
open Lean Meta Elab Command

namespace Census

def repoRoots : List String :=
  ["Minidregg","Theory","Kernel","Pred","Effects","Compiler","Selvage","Assurance","Host",
   "Verify","SimplexQualification","ObjectiveProofs","Deployed","AxiomCensus","AxiomCensusResearch","TokenCensus"]

def lastStr : Name → String
  | .str _ s => s
  | .num p _ => lastStr p
  | .anonymous => ""

def has (s : String) (pats : List String) : Bool :=
  let l := s.toLower
  pats.any fun p => (l.splitOn p).length > 1

def lastNum (s : String) : Bool := s.all Char.isDigit && !s.isEmpty

/-- generated / auxiliary declaration: excluded from the census. -/
def isGenerated (n : Name) : Bool :=
  n.isInternal || n.anyS (fun s => s.startsWith "proof_" || s.startsWith "match_" || s.startsWith "_")
  || (let l := lastStr n
      l == "injEq" || l == "inj" || l == "sizeOf_spec" || l == "eq_def" || l == "ext_iff"
      || l == "congr_simp" || l.startsWith "eq_" && lastNum (l.drop 3).toString || l.startsWith "_eq_"
      || l == "noConfusion" || l == "noConfusionType")

-- ---- rule tables (printed in the report) ----
def temporalNamePats := ["eventually","liveness","eventual","fairness","coind","terminates","_halts","halts_","productive"]
def temporalConstExact := ["Eventually","Terminates","Terminating","Halts","Fair","Fairness","Stream","Stream'","Colist","LazyList","WellFounded","Acc"]
def stepConstExact := ["Step","Steps","Run","Exec","Star","Reachable","StepStar","Iterate","iterate"]
def reachConstPats := ["reachable","reachab","refltransgen","transgen","stepstar"]
def reachWeakPats := ["trace"]  -- only outside Compiler/Selvage (there they are algebraic traces / folding chains)
def reachConstExact := ["Step","Steps","Run","Exec","Star"]
def refineNamePats := ["simulat","refine","refin","agrees","agree_","_agree","correspond","bisim","equivalen","differential","conform","faithful","adequa"]
def refineConstPats := ["simulat","refines","refinement","agree","bisim","correspond"]  -- "agreement" excluded (coding theory)
/-- predicates that unfold to a universal quantifier: a statement headed by one is NOT closed -/
def quantDefs : List Name := [``Function.Injective, ``Function.Surjective, ``Function.Bijective, ``Set.InjOn, ``Set.SurjOn,
  ``Set.BijOn, ``Monotone, ``Antitone, ``StrictMono, ``StrictAnti, ``Function.LeftInverse, ``Function.RightInverse,
  ``Function.Involutive, ``Function.Commute, ``Set.MapsTo, ``Function.Semiconj]
def evalWords := ["eval","exec","run","interp","denot","sem","check","verify","apply","decode"]

structure Info where
  nData : Nat := 0
  nProp : Nat := 0
  nInst : Nat := 0
  innerQ : Nat := 0
  consts : Array Name := #[]
  body : Expr := .bvar 0
  typeIsEqIff : Bool := false

partial def collectConsts (e : Expr) : Array Name :=
  e.foldConsts #[] fun n acc => acc.push n

def headConst? (e : Expr) : Option Name :=
  match e.getAppFn with
  | .const n _ => some n
  | _ => none

/-- count inner quantifiers over data (forall with non-Prop closed domain, or Exists). -/
def innerQuant (e : Expr) : MetaM Nat := do
  let mut n := 0
  let mut stack := #[e]
  let mut seen : Std.HashSet UInt64 := {}
  while stack.size > 0 do
    let t := stack.back!
    stack := stack.pop
    let hsh := hash t
    if seen.contains hsh then continue
    seen := seen.insert hsh
    match t with
    | .forallE _ d b _ =>
      if !d.hasLooseBVars then
        let isP ← try isProp d catch _ => pure true
        if !isP then n := n + 1
      stack := stack.push d |>.push b
    | .app f a => stack := stack.push f |>.push a
    | .lam _ d b _ => stack := stack.push d |>.push b
    | .mdata _ b => stack := stack.push b
    | .letE _ d v b _ => stack := stack.push d |>.push v |>.push b
    | .proj _ _ b => stack := stack.push b
    | _ => pure ()
    if t.isAppOf ``Exists then n := n + 1
  return n

def analyze (type : Expr) : MetaM Info := do
  forallTelescope type fun xs body => do
    let mut i : Info := { body := body }
    for x in xs do
      let d ← x.fvarId!.getDecl
      if d.binderInfo.isInstImplicit then i := { i with nInst := i.nInst + 1 }
      else
        let isP ← try isProp d.type catch _ => pure false
        if isP then i := { i with nProp := i.nProp + 1 }
        else i := { i with nData := i.nData + 1 }
    let iq ← innerQuant body
    let cs := collectConsts type
    let bc := body.getAppFn.constName?
    return { i with innerQ := iq, consts := cs,
                    typeIsEqIff := (bc == some ``Eq || bc == some ``Iff) }

/-- constant whose type ends in `Prop` (a predicate family), not a data type like an enum. -/
def isPropFam (env : Environment) (c : Name) : Bool :=
  match env.find? c with
  | some ci => (ci.type.getForallBody).isProp
  | none => false

def natFuelExists (e : Expr) : Bool :=
  (e.find? fun x => x.isAppOf ``Exists && (x.getArg! 0).isConstOf ``Nat &&
     (match x.getArg! 1 with
      | .lam n _ _ _ => ["n","k","m","fuel","steps","ticks","t","N","budget"].contains n.toString
      | _ => false)).isSome

/-- user (repo) constant? -/
def isRepoConst (env : Environment) (repo : Std.HashSet Name) (n : Name) : Bool :=
  match env.getModuleIdxFor? n with
  | some idx => repo.contains env.header.moduleNames[idx.toNat]!
  | none => true  -- declared in the current file (none here)

def classify (env : Environment) (repo : Std.HashSet Name) (n : Name) (type : Expr) (i : Info) :
    String × String := Id.run do
  let nm := lastStr n
  let consts := i.consts
  let cls := consts.map lastStr
  -- TEMPORAL
  if has nm temporalNamePats then return ("TEMPORAL", "name")
  if cls.any (fun c => temporalConstExact.contains c) then return ("TEMPORAL", "const:" ++ (cls.find? (fun c => temporalConstExact.contains c)).get!)
  if consts.any (fun c => isPropFam env c && has (lastStr c) ["eventually","terminates","liveness"]) then return ("TEMPORAL", "prop-const-pat")
  -- ∃ n, steps: Exists over Nat together with a step-like const
  let hasExN := natFuelExists type
  if hasExN && cls.any (fun c => stepConstExact.contains c || has c ["steps","fuel","iterate"]) then
    return ("TEMPORAL", "exists-nat-steps")
  -- REFINEMENT
  if has nm refineNamePats && !has nm ["agreement"] then return ("REFINEMENT", "name:" ++ nm)
  if cls.any (fun c => has c refineConstPats && !has c ["agreement"]) then return ("REFINEMENT", "const-pat")
  if i.typeIsEqIff then
    let b := i.body
    let lhs? := (b.getArg? (if b.isAppOf ``Eq then 1 else 0)).bind headConst?
    let rhs? := (b.getArg? (if b.isAppOf ``Eq then 2 else 1)).bind headConst?
    match lhs?, rhs? with
    | some l, some r =>
      if l != r && isRepoConst env repo l && isRepoConst env repo r
         && has (lastStr l) evalWords && has (lastStr r) evalWords then
        return ("REFINEMENT", "two-evaluators:" ++ lastStr l ++ "~" ++ lastStr r)
    | _, _ => pure ()
  -- REACHABLE
  if consts.any (fun c => (isPropFam env c && reachConstExact.contains (lastStr c)) || has (lastStr c) reachConstPats) then
    return ("REACHABLE-INVARIANT", "const:" ++ (consts.find? (fun c => (isPropFam env c && reachConstExact.contains (lastStr c)) || has (lastStr c) reachConstPats)).get!.toString)
  if consts.any (fun c => let q := c.toString
        !(q.startsWith "Minidregg.Compiler." || q.startsWith "Minidregg.Selvage.") &&
        has (lastStr c) reachWeakPats && (isPropFam env c || true)) then
    return ("REACHABLE-INVARIANT", "weak-const")
  if has nm ["reachable"] then return ("REACHABLE-INVARIANT", "name")
  -- CLOSED: no data binder, no inner data quantifier
  let disguised := (match i.body.getAppFn with
    | .const c _ => quantDefs.contains c
    | _ => false)
  if i.nData == 0 && i.innerQ == 0 && !disguised then
    -- does it reference repo constants at all?
    return ("CLOSED-INSTANCE", s!"props={i.nProp}")
  -- OTHER: no repo constant in statement (generic library-style lemma)
  if !(consts.any (isRepoConst env repo)) then return ("OTHER", "no-repo-const")
  return ("PER-FUNCTION", s!"data={i.nData},innerQ={i.innerQ}")

def procFlags (v : Expr) : String :=
  let cs := collectConsts v
  let nat := cs.contains ``Lean.ofReduceBool || cs.any (fun c => (c.toString.splitOn "native_decide").length > 1)
  let dec := cs.contains ``of_decide_eq_true || cs.contains ``Decidable.decide
  let rfl := cs.contains ``Eq.refl || cs.contains ``rfl
  let l := (if nat then ["native"] else []) ++ (if dec then ["decide"] else []) ++ (if rfl then ["rfl"] else [])
  ",".intercalate l

end Census

open Census in
#eval show CommandElabM Unit from do
  let env ← getEnv
  let mods := env.header.moduleNames
  let repo : Std.HashSet Name := mods.foldl (init := {}) fun s m =>
    if repoRoots.contains (m.getRoot.toString) then s.insert m else s
  let out := (← IO.getEnv "CENSUS_OUT").getD "/tmp/census.tsv"
  let mut lines : Array String := #["name\tmodule\ttop\tbucket\treason\tnData\tnProp\tnInst\tinnerQ\tproof\tsize"]
  let mut gen := 0
  for (n, ci) in env.constants.map₁.toList do
    match ci with
    | .thmInfo tv =>
      match env.getModuleIdxFor? n with
      | none => pure ()
      | some idx =>
        let m := env.header.moduleNames[idx.toNat]!
        unless repo.contains m do continue
        if isGenerated n then gen := gen + 1; continue
        let r ← liftCoreM ((analyze tv.type).run')
        let (b, why) := classify env repo n tv.type r
        let fl := procFlags tv.value
        lines := lines.push s!"{n}\t{m}\t{m.getRoot}\t{b}\t{why}\t{r.nData}\t{r.nProp}\t{r.nInst}\t{r.innerQ}\t{fl}\t{tv.type.approxDepth}"
    | _ => pure ()
  IO.FS.writeFile out ("\n".intercalate lines.toList ++ "\n")
  logInfo m!"theorems: {lines.size - 1}; generated excluded: {gen}; out {out}"
