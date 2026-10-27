#!/usr/bin/env bash
# GLM-B: rename the three Reject wire names that collide with Refusal names.
# Content-addressed; refuses to run twice or on a tree that drifted.
set -euo pipefail
cd "$(dirname "$0")"
fail() { echo "PRECHECK FAIL: $*" >&2; exit 1; }
pre() { local n; n=$(grep -c -- "$2" "$1" || true); [ "$n" = "$3" ] || fail "$1: '$2' found $n times, expected $3"; }
pre Kernel/World.lean '| missingCell (cell : D)' 1
pre Kernel/World.lean '| rangeTooLong (parent : D)' 1
pre Kernel/World.lean '| duplicateRow (parent : D)' 1
pre Kernel/World.lean '| \.missingCell _ => "missingCell"' 1
pre Kernel/World.lean '| \.rangeTooLong _ => "rangeTooLong"' 1
pre Kernel/World.lean '| \.duplicateRow _ => "duplicateRow"' 1
pre Kernel/World.lean '\.error (\.missingCell x\.cell)' 2
pre Kernel/World.lean '\.error (\.rangeTooLong q\.parent)' 1
pre Kernel/World.lean '\.error (\.duplicateRow (match' 1
pre Kernel/World.lean '(`rangeTooLong`: refused, never' 1
pre Kernel/World.lean 'slots distinct (`duplicateRow`)' 1
pre Kernel/World.lean '(`rangeTooLong`, never truncated)' 1
pre Kernel/World.lean '`noRelation`, `rangeTooLong`)' 1
pre Kernel/Receive/Submit.lean '"bornTouched", "missingCell",' 1
pre Kernel/Receive/Submit.lean '"declareLate", "rangeTooLong", "duplicateRow",' 1
pre Kernel/Proofs/Admit.lean '\.error (\.duplicateRow (match x\.slot' 1
pre Kernel/Proofs/Rows.lean '(`duplicateRow`), so the one touch' 1
pre Kernel/Proofs/InvokeTree.lean '\.error (\.missingCell [a-z])' 1
pre Kernel/Turn.lean 'refused `rangeTooLong` past `most`' 1
pre Kernel/Sim/Gen.lean '(\.rejected (\.missingCell o))' 1
rep() { perl -pi -e "s/\Q$2\E/$3/g" "$1"; echo "replaced in $1: $2"; }
rep Kernel/World.lean '| missingCell (cell : D)' '| absentCell (cell : D)'
rep Kernel/World.lean '| rangeTooLong (parent : D)' '| rangeOverMost (parent : D)'
rep Kernel/World.lean '| duplicateRow (parent : D)' '| duplicateRowSlot (parent : D)'
rep Kernel/World.lean '| .missingCell _ => "missingCell"' '| .absentCell _ => "absentCell"'
rep Kernel/World.lean '| .rangeTooLong _ => "rangeTooLong"' '| .rangeOverMost _ => "rangeOverMost"'
rep Kernel/World.lean '| .duplicateRow _ => "duplicateRow"' '| .duplicateRowSlot _ => "duplicateRowSlot"'
rep Kernel/World.lean '.error (.missingCell x.cell)' '.error (.absentCell x.cell)'
rep Kernel/World.lean '.error (.rangeTooLong q.parent)' '.error (.rangeOverMost q.parent)'
rep Kernel/World.lean '.error (.duplicateRow (match' '.error (.duplicateRowSlot (match'
rep Kernel/World.lean '(`rangeTooLong`: refused, never' '(`rangeOverMost`: refused, never'
rep Kernel/World.lean 'slots distinct (`duplicateRow`)' 'slots distinct (`duplicateRowSlot`)'
rep Kernel/World.lean '(`rangeTooLong`, never truncated)' '(`rangeOverMost`, never truncated)'
rep Kernel/World.lean '`noRelation`, `rangeTooLong`)' '`noRelation`, `rangeOverMost`)'
rep Kernel/Receive/Submit.lean '"bornTouched", "missingCell",' '"bornTouched", "absentCell",'
rep Kernel/Receive/Submit.lean '"declareLate", "rangeTooLong", "duplicateRow",' '"declareLate", "rangeOverMost", "duplicateRowSlot",'
rep Kernel/Proofs/Admit.lean '.error (.duplicateRow (match x.slot' '.error (.duplicateRowSlot (match x.slot'
rep Kernel/Proofs/Rows.lean '(`duplicateRow`), so the one touch' '(`duplicateRowSlot`), so the one touch'
perl -pi -e 's/\.error \(\.missingCell ([a-z])\)/.error \(.absentCell $1\)/' Kernel/Proofs/InvokeTree.lean && echo 'replaced in Kernel/Proofs/InvokeTree.lean: missingCell raise (regex)'
rep Kernel/Turn.lean 'refused `rangeTooLong` past `most`' 'refused `rangeOverMost` past `most`'
rep Kernel/Sim/Gen.lean '(.rejected (.missingCell o))' '(.rejected (.absentCell o))'
echo "=== post-check: old reject-side spellings left in the two tables (expect none):"
grep -n 'missingCell\|rangeTooLong\|duplicateRow' Kernel/World.lean Kernel/Receive/Submit.lean | grep -v 'absentCell\|rangeOverMost\|duplicateRowSlot' || echo "(clean)"
check1() { local c; c=$(grep -c -- "$1" Kernel/Receive/Submit.lean || true); [ "$c" = "1" ] || echo "POSTCHECK FAIL: $1 count=$c (want 1)"; }
check1 '"rangeTooLong", "rowParent"'
check1 '"missingCell", "wrongKind"'
check1 '"rowParent", "duplicateRow"'
