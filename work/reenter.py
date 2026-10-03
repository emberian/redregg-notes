#!/usr/bin/env python3
"""Read-only re-entry aid. Extraction/inventory is NOT evidence of agent reading."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

BASE = Path(__file__).resolve().parent

def main():
    manifest = json.loads((BASE / "reentry-manifest.json").read_text())
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--hook", action="store_true")
    group.add_argument("--inventory", action="store_true")
    group.add_argument("--dialogue", metavar="START..END")
    ap.add_argument("--session", default=manifest["session"])
    args = ap.parse_args()
    if args.hook:
        event = json.load(sys.stdin)
        if (event.get("hook_event_name") != "SessionStart" or
            event.get("source") not in ("compact", "resume") or
            event.get("session_id") != manifest["session"]):
            return
        context = (
            "Ember requested this thread's post-compaction re-entry ritual. "
            "Before new architecture/status decisions, read " + str(BASE / "REENTRY.txt") +
            " and follow it: recover BOTH human prompts and assistant replies using cv; "
            "read the named core records in full and route-specific records before decisions; "
            "check actual live agents/build ownership. Summaries and reports are navigation, "
            "not current evidence. Record what was actually read and changed; extraction is not reading. "
            "Do not restart an active swarm or lower the destination to its first passing tranche. "
            "This reminder does not establish that any reading has happened.")
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}))
        return
    if args.inventory:
        groups = {"always": manifest["always"], **manifest["routes"]}
        for label, paths in groups.items():
            print("\n" + label)
            for name in paths:
                p = Path(name)
                if not p.is_file():
                    print("MISSING " + name)
                    continue
                data = p.read_bytes()
                print(f"{hashlib.sha256(data).hexdigest()} {len(data)} bytes {name}")
        return
    try:
        lo, hi = map(int, args.dialogue.split(".."))
        if lo < 0 or hi < lo:
            raise ValueError()
    except ValueError:
        ap.error("--dialogue needs nonnegative half-open START..END (END excluded)")
    result = subprocess.run(["cv", "show", args.session, "--range", f"{lo}..{hi}", "--json"], check=True, capture_output=True, text=True)
    session = json.loads(result.stdout)
    print(f"CV dialogue {args.session} [{lo}..{hi}) (END excluded). Full text blocks, no thinking/tool outputs.\n"
          "Origins are cv classifications; review machine envelopes/quotes before attributing them to Ember.\n"
          "Use cv show --around INDEX --context K whenever omitted tools/adjacent exchanges matter.")
    selected = 0
    for index, message in enumerate(session["messages"], lo):
        if message.get("kind") not in ("prompt", "reply") or message.get("origin") not in ("human", "model"):
            continue
        if message.get("role") not in ("user", "assistant"):
            continue
        text = "\n".join(b["text"] for b in message.get("content", []) if b.get("type") == "text")
        if not text:
            continue
        selected += 1
        print(f"\n[{index}] {message['role']} origin={message['origin']} {message.get('timestamp', '')}\n{text}")
    print(f"\nEND: {selected} dialogue messages emitted; no reading/comprehension claim.")

if __name__ == "__main__":
    main()
