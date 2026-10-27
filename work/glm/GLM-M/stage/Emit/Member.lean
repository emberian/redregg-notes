import Protocol.Member

/-!
# Emit.Member — docs/MEMBER.md's reachability table

The table between the two markers is `Protocol.Member.rows` and nothing else. `emit-member
docs/MEMBER.md` rewrites the section between the markers (the file's prose is the doc's own);
`--check` exits 1 when the file's table is not what `rows` says, so a row edited by hand, or a row
added in Lean without regenerating, is red at the next convergence (`gates/generated.tsv`).
-/

namespace Nanodregg.Emit.Member

open Nanodregg.Protocol.Member

def startMark : String := "<!-- member-table:start -->"
def endMark : String := "<!-- member-table:end -->"

/-- One row of the table. -/
def rowLine (r : Row) : String :=
  s!"| {r.act} | {r.nd} | {r.page} | {r.proof} | {r.refusals} |"

/-- The table, from its start marker to its end marker. -/
def table : String := String.intercalate "\n"
  ([startMark, "| Act | nd | page | proven by | refusal names |", "|---|---|---|---|---|"] ++
    rows.map rowLine ++ [endMark])

/-- The file with its table section replaced, or why the file carries no markers. -/
def splice (text : String) : Except String String :=
  match text.splitOn startMark, (text.splitOn startMark).getLast?.bind fun rest =>
    (rest.splitOn endMark) with
  | [pre, rest], _ =>
      match rest.splitOn endMark with
      | [_, post] => .ok (pre ++ table ++ post)
      | _ => .error "the file carries no table markers"
  | _, _ => .error "the file carries no table markers"

/-- `emit-member PATH` rewrites the file's table; `--check PATH` exits 1 if it differs. -/
def run (args : List String) : IO UInt32 := do
  match args with
  | [path] =>
    let text ← IO.FS.readFile path
    match splice text with
    | .error e => IO.eprintln s!"emit-member: {path}: {e}"; return 2
    | .ok t => if t != text then IO.FS.writeFile path t; return 0
  | ["--check", path] =>
    let text ← IO.FS.readFile path
    match splice text with
    | .error e => IO.eprintln s!"emit-member: {path}: {e}"; return 2
    | .ok t =>
      if t == text then return 0
      IO.eprintln s!"emit-member: {path} differs from the table; regenerate it"
      return 1
  | _ => IO.eprintln "usage: emit-member [--check] PATH"; return 2

end Nanodregg.Emit.Member
