#!/usr/bin/env python3
"""SELF IMPROVE — Reads audit, applies safe fixes automatically."""
import json, os, sys, time
from pathlib import Path

AUDIT = Path("/sdcard/openroot/agape_kb/audit_report.json")
ROOT = Path("$(pwd)/une")
LOG = Path("/sdcard/openroot/agape_kb/self_improve_actions.jsonl")
SAFE = ["dead_file", "duplicate_content"]

def run(dry_run=False):
    if not AUDIT.exists():
        print("No audit found. Run meta_audit.py first.")
        return
    audit = json.loads(AUDIT.read_text())
    findings = audit.get("findings", [])
    taken = []
    skipped = []

    for f in findings:
        if f.get("issue") not in SAFE:
            skipped.append({"issue":f.get("issue",""),"reason":"not_auto_safe"})
            continue
        if f.get("issue") == "dead_file":
            target = ROOT / f["file"]
            if target.exists():
                if not dry_run:
                    target.unlink()
                taken.append({"action":"deleted_dead","file":f["file"],"dry_run":dry_run})
        elif f.get("issue") == "duplicate_content":
            files = f.get("files", [])
            for dup in files[1:]:
                target = ROOT / dup
                if target.exists():
                    if not dry_run:
                        target.unlink()
                    taken.append({"action":"deleted_dup","file":dup,"kept":files[0],"dry_run":dry_run})

    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as fh:
        fh.write(json.dumps({"timestamp":time.strftime("%Y-%m-%dT%H:%M:%S"),"taken":taken,"skipped":skipped,"dry_run":dry_run}) + "\n")

    mode = "DRY RUN" if dry_run else "LIVE"
    print("SELF IMPROVE [" + mode + "] | Taken:" + str(len(taken)) + " Skipped:" + str(len(skipped)))
    for a in taken:
        print("  " + a["action"] + ": " + a["file"])

if __name__ == "__main__":
    dry = len(sys.argv) > 1 and sys.argv[1] == "--dry"
    run(dry_run=dry)
