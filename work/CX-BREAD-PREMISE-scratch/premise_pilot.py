#!/usr/bin/env python3
"""Read-only, explicitly scoped journal adapter. Run: python3 -I premise_pilot.py.

This is a dry run: it never authorizes or rewrites a Lean theorem. The historical
14-line sample is a lexical sample, not fourteen verified repair obligations.
"""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path('/Users/ember/dev/breadstuffs')
SCRATCH = Path(__file__).resolve().parent
FILES = {
    'F': 'metatheory/Dregg2/Circuit/FirstDivergence.lean',
    'R': 'metatheory/Dregg2/Shielded/RealCrypto.lean',
    'G': 'metatheory/Dregg2/Verify/FreeConclusionRatchet.lean',
}
# Re-inventoried at breadstuffs 22fad151e. A lexical sample, including controls.
SITES = [
    ('F', 139, 'globalBreak_free', 'free-witness'),
    ('F', 149, 'indexedBreak_not_free', 'negative-control'),
    ('F', 171, 'leafPair_binds_or_coll', 'indexed-theorem'),
    ('F', 230, 'zipFirst_binds_or_coll', 'indexed-theorem'),
    ('F', 311, 'foldLast_binds_or_coll', 'indexed-theorem'),
    ('F', 399, 'resolve', 'indexed-consumer'),
    ('F', 431, 'Site.sound', 'structure-field'),
    ('R', 380, 'Poseidon2Tree.root_binds_or_collides', 'indexed-theorem'),
    ('R', 417, 'forged_set_is_honest_or_collides', 'indexed-theorem'),
    ('R', 519, 'deployed_forged_set_is_honest_or_collides', 'indexed-theorem'),
    ('G', 89, 'free-shape-example', 'comment'),
    ('G', 90, 'indexed-shape-example', 'comment'),
    ('G', 897, 'repair-example', 'string-literal'),
    ('G', 911, 'quantifier-warning', 'string-literal'),
]
AUDITS = [
    'docs/audit/META-REVIEW-STATEMENTS.md',
    'docs/audit/NON-VACUITY-MANIFEST.md',
    'metatheory/docs/AXIOM-HYGIENE.md',
    'metatheory/docs/SOUNDNESS-RESIDUAL-CENSUS.md',
]
ARCHIVE = ROOT / 'docs/artifacts/floor-census-v2-2026-07-26/floor-census-v2.tsv'
CURRENT = SCRATCH / 'floor-census-current.tsv'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def load_census(path):
    rows = []
    if not path.is_file():
        return rows
    with path.open(newline='') as stream:
        for parts in csv.reader(stream, delimiter='\t'):
            if parts and parts[0] in ('CARRIER', 'UCARRIER'):
                # v2/v3 expose floor carriers, not general constant consumers.
                rows.append(parts)
    return rows


def audit_hits(token):
    out = []
    for rel in AUDITS:
        for n, line in enumerate((ROOT / rel).read_text().splitlines(), 1):
            if token in line:
                out.append({'path': rel, 'line': n})
    return out


def source_mentions(token):
    """Lexical leads, never a checked dependency or proof-term consumer list."""
    out = []
    for rel in FILES.values():
        for n, line in enumerate((ROOT / rel).read_text().splitlines(), 1):
            if token in line and not line.lstrip().startswith(('--', '/-', '*')):
                out.append(f'{rel}:{n}')
    return out[:12]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--census', type=Path, default=CURRENT if CURRENT.exists() else ARCHIVE)
    ap.add_argument('--summary', action='store_true', help='print the auditable 14-row projection')
    args = ap.parse_args()
    census = load_census(args.census)
    result = []
    for key, line, name, kind in SITES:
        rel = FILES[key]
        p = ROOT / rel
        lines = p.read_text().splitlines()
        if line > len(lines):
            raise SystemExit(f'stale inventory: {rel}:{line} absent')
        text = lines[line - 1].strip()
        if not ('∨' in text or 'OrBreak' in text or 'Coll' in text):
            raise SystemExit(f'stale inventory: {rel}:{line}: {text}')
        leaf = name.split('.')[-1]
        # The TSV's CARRIER rows tell us about refuted floor hypotheses only.
        # Matching a row to the declaration is evidence about that surface;
        # absence says nothing about ordinary theorem or definition supports.
        exact = [r for r in census if r[1].endswith('.' + name) or r[1] == name]
        result.append({
            'id': f'bread-premise/{key}{line}',
            'subject': name,
            'source': f'{rel}:{line}',
            'source_sha16': sha(p),
            'line': text,
            'classification': kind,
            'logical_status': 'unassessed' if kind.endswith('theorem') or kind == 'structure-field' else 'out-of-scope',
            'supports': {'elaborated_constants': 'UNEXPORTED', 'axioms': 'UNEXPORTED'},
            'census_floor_carrier_rows': [r for r in exact],
            'census_consumers': 'NOT_EMITTED_BY_FLOOR_CENSUS',
            'lexical_mentions_in_three_files': source_mentions(leaf) if kind not in ('comment', 'string-literal') else [],
            'audit_hits': audit_hits(leaf) if kind not in ('comment', 'string-literal') else [],
            'blockers': ['scope/semantic-review-needed'] if kind == 'free-witness' else [],
            'event': {'kind': 'dry-run-discover', 'withdrawn': False, 'repair': None},
        })
    if args.summary:
        print(f'mode=DRY_RUN_ONLY  census={args.census.name}  coverage=14 lexical lines')
        for row in result:
            short = row['id'].rsplit('/', 1)[-1]
            print(f"{short:<4} {row['subject']:<44} {row['classification']:<17} {len(row['census_floor_carrier_rows'])}")
        print('supports.elaborated_constants=UNEXPORTED  supports.axioms=UNEXPORTED')
        print('census_consumers=NOT_EMITTED_BY_FLOOR_CENSUS')
        print('not_an_obligation_count=true')
        return
    print(json.dumps({
        'mode': 'DRY_RUN_ONLY', 'source_commit': '22fad151e9f118e3aa001a823e075918ffa139e8',
        'census': str(args.census), 'census_sha16': sha(args.census) if args.census.exists() else None,
        'census_carrier_rows': len(census), 'coverage': 'historical 14 lexical lines in three files',
        'not_an_obligation_count': True, 'obligations': result,
    }, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
