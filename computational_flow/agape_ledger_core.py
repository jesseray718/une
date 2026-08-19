#!/data/data/com.termux/files/usr/bin/env python3
"""
Agape Ledger Core v1.0 — pure
Only measured joules. η = useful_joules / human_joules
Append-only. Links to resonance and Newton Chain.
"""

import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

KB_DIR = Path("/sdcard/openroot/agape_kb")
LEDGER_DIR = KB_DIR / "ledger"
JOURNAL = LEDGER_DIR / "joule_journal.jsonl"
STATE = LEDGER_DIR / "ledger_state.json"
POSTULATES = KB_DIR / "postulates.json"
ENGINE_STATE = KB_DIR / "engine_state.json"

LEDGER_DIR.mkdir(parents=True, exist_ok=True)

def _now() -> str:
    return datetime.now().isoformat()

def _hash_entry(entry: dict) -> str:
    raw = json.dumps(entry, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {
        "version": "1.0.0",
        "entries": 0,
        "total_useful_j": 0.0,
        "total_human_j": 0.0,
        "last_η": None,
        "last_active": None,
        "resonance": 1.0
    }

def save_state(state: dict):
    state["last_active"] = _now()
    STATE.write_text(json.dumps(state, indent=2))

def get_resonance() -> float:
    if ENGINE_STATE.exists():
        try:
            return float(json.loads(ENGINE_STATE.read_text()).get("resonance", 1.0))
        except Exception:
            pass
    return 1.0

def record(useful: float, human: float, event: str = "work",
           postulate: Optional[str] = None, note: str = "",
           measured: bool = True) -> dict:
    """
    Only measured joules are accepted.
    human_joules must be > 0.
    """
    if not measured:
        raise ValueError("Ledger refuses theoretical joules. measured=True required.")
    if human <= 0:
        raise ValueError("human_joules must be > 0")
    if useful < 0:
        raise ValueError("useful_joules cannot be negative")

    η = useful / human
    R = get_resonance()

    entry = {
        "ts": _now(),
        "event": event,
        "useful_j": round(useful, 6),
        "human_j": round(human, 6),
        "η": round(η, 6),
        "resonance": R,
        "postulate": postulate,
        "note": note,
        "measured": True
    }
    entry["hash"] = _hash_entry(entry)

    with JOURNAL.open("a") as f:
        f.write(json.dumps(entry) + "\n")

    state = load_state()
    state["entries"] = state.get("entries", 0) + 1
    state["total_useful_j"] = state.get("total_useful_j", 0.0) + useful
    state["total_human_j"] = state.get("total_human_j", 0.0) + human
    state["last_η"] = η
    state["resonance"] = R
    save_state(state)

    return entry

def summary() -> dict:
    state = load_state()
    total_u = state.get("total_useful_j", 0.0)
    total_h = state.get("total_human_j", 0.0)
    η = (total_u / total_h) if total_h > 0 else None
    return {
        "entries": state.get("entries", 0),
        "total_useful_j": round(total_u, 6),
        "total_human_j": round(total_h, 6),
        "η": round(η, 6) if η is not None else None,
        "last_η": state.get("last_η"),
        "resonance": state.get("resonance", 1.0),
        "last_active": state.get("last_active")
    }

def tail(n: int = 8):
    if not JOURNAL.exists():
        print("Journal empty.")
        return
    lines = JOURNAL.read_text().strip().splitlines()
    for line in lines[-n:]:
        e = json.loads(line)
        print(f"{e['ts'][:19]}  η={e['η']:8.4f}  U={e['useful_j']:10.4f}  H={e['human_j']:10.4f}  {e['event']}  {e.get('note','')[:40]}")

def cmd_status():
    s = summary()
    print("Agape Ledger Core v1.0 — pure")
    print(f"  Entries        : {s['entries']}")
    print(f"  Total useful J : {s['total_useful_j']}")
    print(f"  Total human J  : {s['total_human_j']}")
    print(f"  Cumulative η   : {s['η']}")
    print(f"  Last η         : {s['last_η']}")
    print(f"  Resonance      : {s['resonance']}")
    print(f"  Last active    : {s['last_active']}")
    print()
    print("Only measured joules accepted. Theoretical entries rejected.")

def cmd_record(args):
    """record <useful> <human> [event] [note...]"""
    if len(args) < 2:
        print("Usage: record <useful_j> <human_j> [event] [note]")
        return
    useful = float(args[0])
    human = float(args[1])
    event = args[2] if len(args) > 2 else "work"
    note = " ".join(args[3:]) if len(args) > 3 else ""
    entry = record(useful, human, event=event, note=note)
    print(f"Recorded  η={entry['η']:.6f}  hash={entry['hash']}")

def cmd_prove(args):
    """Minimal PoPW-style proof line for later ACRE wiring."""
    if len(args) < 2:
        print("Usage: prove <useful_j> <human_j> [note]")
        return
    useful = float(args[0])
    human = float(args[1])
    note = " ".join(args[2:]) if len(args) > 2 else "physical_work"
    entry = record(useful, human, event="popw_prove", note=note, measured=True)
    print("PROOF")
    print(f"  hash     : {entry['hash']}")
    print(f"  η        : {entry['η']:.6f}")
    print(f"  resonance: {entry['resonance']}")
    print(f"  ts       : {entry['ts']}")
    print("Ready for later ACRE claim wiring.")

def interactive():
    print("Agape Ledger Core v1.0 — interactive")
    print("Commands: status | record <u> <h> [event] [note] | prove <u> <h> [note] | tail [n] | quit")
    while True:
        try:
            line = input("ledger> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line in ("quit", "exit", "q"):
            break
        parts = line.split()
        cmd = parts[0]
        args = parts[1:]
        if cmd == "status":
            cmd_status()
        elif cmd == "record":
            cmd_record(args)
        elif cmd == "prove":
            cmd_prove(args)
        elif cmd == "tail":
            n = int(args[0]) if args else 8
            tail(n)
        else:
            print("Unknown. status | record | prove | tail | quit")

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "interactive":
            interactive()
        elif arg == "status":
            cmd_status()
        elif arg == "record":
            cmd_record(sys.argv[2:])
        elif arg == "prove":
            cmd_prove(sys.argv[2:])
        elif arg == "tail":
            n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
            tail(n)
        elif arg == "summary":
            print(json.dumps(summary(), indent=2))
        else:
            print("Usage:")
            print("  python3 agape_ledger_core.py interactive")
            print("  python3 agape_ledger_core.py status")
            print("  python3 agape_ledger_core.py record <useful> <human> [event] [note]")
            print("  python3 agape_ledger_core.py prove <useful> <human> [note]")
            print("  python3 agape_ledger_core.py tail [n]")
    else:
        cmd_status()

if __name__ == "__main__":
    main()
