#!/usr/bin/env python3
"""Read-only integration handoff audit; does not infer live processes or send messages."""
import argparse
import json
from pathlib import Path

STATES = {'building', 'waiting', 'ready', 'receiving', 'integrated', 'checkpointed'}
REQUIRED = ('id', 'outcome', 'owner', 'consumer', 'coordinator', 'state',
            'next_action', 'acceptance', 'progress_evidence')


def audit(records, inactive, known_agents=None):
    findings = []
    if not records:
        findings.append(('<registry>', 'INVALID', 'no obligations loaded; this is not a clean integration audit'))
    seen = set()
    for item in records:
        key = item.get('id', '<missing id>')
        for field in REQUIRED:
            if not item.get(field):
                findings.append((key, 'INVALID', f'missing {field}'))
        if known_agents is not None:
            for field in ('owner', 'consumer', 'coordinator'):
                if item.get(field) and item[field] not in known_agents:
                    findings.append((key, 'UNKNOWN_AGENT', f'{field}: {item[field]}'))
        if key in seen:
            findings.append((key, 'INVALID', 'duplicate obligation id'))
        seen.add(key)
        state = item.get('state')
        if state not in STATES:
            findings.append((key, 'INVALID', f'unknown state {state!r}'))
        waits = item.get('waits_for', [])
        for dep in waits:
            if known_agents is not None and dep.get('owner') and dep['owner'] not in known_agents:
                findings.append((key, 'UNKNOWN_AGENT', f"dependency owner: {dep['owner']}"))
            if not all(dep.get(k) for k in ('owner', 'deliverable', 'next_action')):
                findings.append((key, 'INVALID', 'dependency lacks owner/deliverable/action'))
            if dep.get('ready') is True and not dep.get('evidence'):
                findings.append((key, 'INVALID', 'ready dependency lacks evidence'))
            if state != 'checkpointed' and dep.get('ready') is not True and dep.get('owner') in inactive:
                findings.append((key, 'WAKE_PRODUCER',
                    f"{dep['owner']}: {dep.get('next_action', '')}"))
        if state == 'checkpointed':
            # Deliberately inactive is neither complete nor accidentally stranded.
            # Retain the source/evidence and explicit reactivation decision.
            for field in ('checkpoint_ref', 'restart_condition', 'unresolved_work'):
                if not item.get(field):
                    findings.append((key, 'INVALID_CHECKPOINT', f'missing {field}'))
            continue
        if state == 'integrated':
            ack = item.get('consumer_ack', {})
            if not item.get('receiving_evidence') or ack.get('owner') != item.get('consumer') or not ack.get('evidence'):
                findings.append((key, 'INVALID_CLOSE', 'receiving evidence and named consumer acknowledgement required'))
            if any(dep.get('ready') is not True for dep in waits):
                findings.append((key, 'INVALID_CLOSE', 'unresolved dependency'))
            continue
        ready = all(dep.get('ready') is True for dep in waits)
        if state == 'waiting' and ready:
            findings.append((key, 'READY_NOT_DISPATCHED', item.get('next_action', '')))
        if ready and item.get('owner') in inactive:
            findings.append((key, 'WAKE_OWNER',
                f"{item['owner']}: {item.get('next_action', '')}"))
        elif not ready and state == 'ready':
            findings.append((key, 'CONTRADICTION', 'claims ready with unmet dependency'))
        # A consumer can exercise a qualified part while later producers build.
        # Full integration above still requires every dependency and actual use.
        if state == 'receiving' and item.get('consumer') in inactive:
            findings.append((key, 'INACTIVE_CONSUMER',
                f"{item['consumer']}: verify next runnable receiving step or record its actual wait"))
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='*', type=Path)
    parser.add_argument('--inactive', action='append', default=[],
                        help='Agent observed completed/stopped in a FRESH collaboration.list_agents call; repeat as needed.')
    parser.add_argument('--agent', action='append', default=None,
                        help='Exact short agent name from the full live tree, including completed agents and root; repeat to supply a complete roster.')
    args = parser.parse_args()
    files = args.files or sorted(Path(__file__).parent.glob('*.json'))
    records = []
    for path in files:
        data = json.loads(path.read_text())
        records.extend(data['obligations'])
    findings = audit(records, set(args.inactive), None if args.agent is None else set(args.agent))
    if not args.files:
        for name in ('runtime.json', 'product.json', 'protocol.json'):
            if not (Path(__file__).parent / name).is_file():
                findings.append(('<registry>', 'MISSING_CLUSTER', name))
    print(json.dumps({'obligations': len(records), 'findings': findings,
        'limitation': 'Record validation only. Verify receiving evidence and actual job/agent state separately. Use followup_task for an inactive owner; send_message does not wake it.'}, indent=2))
    return 1 if findings else 0


if __name__ == '__main__':
    raise SystemExit(main())
