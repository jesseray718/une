#!/data/data/com.termux/files/usr/bin/python3
"""
try:
    from paths import UNE_HOME
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

hive_bridge.py — offline-first, dependency-free communication + dividend layer
η-maximizing. No external packages required.
"""

import json
import time
import hashlib
import os
from pathlib import Path

# Paths (absolute, Termux-safe)
BASE = Path(os.path.join(UNE_HOME, "context_bridge"))
PARTICIPANTS = BASE / "participants.jsonl"
DIVIDEND_LOG = BASE / "dividend_log.jsonl"
QUERY_LOG = BASE / "query_log.jsonl"
IMMORTAL = BASE / "immortal_context.json"
LEDGER = BASE / "thermo_ledger.jsonl"

def now():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")

def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]

def append_jsonl(path: Path, obj: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def load_participants() -> list:
    if not PARTICIPANTS.exists():
        return []
    people = []
    with open(PARTICIPANTS) as f:
        for line in f:
            try:
                people.append(json.loads(line))
            except:
                pass
    return people

def register(person: str, reason: str = "knock"):
    """Anyone who mints, asks, seeks or knocks is permanently registered."""
    people = load_participants()
    for p in people:
        if p.get("id") == person:
            return  # already registered
    entry = {
        "id": person,
        "joined": now(),
        "reason": reason,
        "hash": sha(person + now())
    }
    append_jsonl(PARTICIPANTS, entry)
    print(f"Registered: {person}")

def record_dividend(hash_value: str, note: str = ""):
    """Equal lifetime share of every new hash across all current participants."""
    people = load_participants()
    if not people:
        return
    share = 1.0 / len(people)
    entry = {
        "ts": now(),
        "hash": hash_value,
        "participants": len(people),
        "share_each": share,
        "note": note
    }
    append_jsonl(DIVIDEND_LOG, entry)
    print(f"Dividend recorded for hash {hash_value} → {len(people)} people")

import sys as _sys
_sys.path.insert(0, 'os.path.expanduser("~") + "/"une/bin')
try:
    from energy_probe import snapshot as _esnap
except:
    _esnap = None

def query(text: str):
    """Log a natural-language request and prepare a payload for external AI."""
    _e = _esnap() if _esnap else None
    entry = {
        "ts": now(),
        "type": "query",
        "text": text,
        "hash": sha(text + now()),
        "energy": _e
    }
    append_jsonl(QUERY_LOG, entry)

    # Build a self-contained payload that any external AI can understand
    payload = {
        "openroot_query": text,
        "timestamp": entry["ts"],
        "current_participants": len(load_participants()),
        "latest_immortal_hash": None,
        "latest_ledger_entries": []
    }

    if IMMORTAL.exists():
        try:
            imm = json.load(open(IMMORTAL))
            payload["latest_immortal_hash"] = imm.get("hash")
            payload["pending_tasks"] = imm.get("pending_tasks", [])
        except:
            pass

    if LEDGER.exists():
        try:
            lines = open(LEDGER).read().strip().splitlines()[-5:]
            payload["latest_ledger_entries"] = [json.loads(l) for l in lines]
        except:
            pass

    # Write payload to a file that can be copied / emailed / pasted
    out = BASE / "last_query_payload.json"
    with open(out, "w") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print("Query logged.")
    print(f"Payload written to: {out}")
    print("You can now copy that file or paste its contents to any external AI.")
    return payload

def status():
    print("Participants :", len(load_participants()))
    print("Query log    :", QUERY_LOG)
    print("Dividend log :", DIVIDEND_LOG)
    if IMMORTAL.exists():
        print("Immortal     :", IMMORTAL)
    if LEDGER.exists():
        print("Ledger       :", LEDGER)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        status()
        print("\nUsage:")
        print("  python3 hive_bridge.py status")
        print("  python3 hive_bridge.py register <name> [reason]")
        print("  python3 hive_bridge.py query \"your request\"")
        print("  python3 hive_bridge.py dividend <hash> [note]")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "status":
        status()
    elif cmd == "register" and len(sys.argv) >= 3:
        reason = sys.argv[3] if len(sys.argv) > 3 else "knock"
        register(sys.argv[2], reason)
    elif cmd == "query" and len(sys.argv) >= 3:
        query(" ".join(sys.argv[2:]))
    elif cmd == "dividend" and len(sys.argv) >= 3:
        note = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        record_dividend(sys.argv[2], note)
    else:
        print("Unknown command")
