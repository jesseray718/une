#!/data/data/com.termux/files/usr/bin/env python3
"""Append a progress stamp to the context bridge. State accumulates, never replays."""
import json, time
from pathlib import Path

BRIDGE = Path("/sdcard/openroot/context_bridge/agape_context_bridge.json")
PROGRESS = Path("/sdcard/openroot/context_bridge/progress_log.jsonl")

def stamp(action, detail, metrics=None):
    entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "action": action,
        "detail": detail,
        "metrics": metrics or {}
    }
    # Append to linear log
    PROGRESS.parent.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS, "a") as f:
        f.write(json.dumps(entry) + "\n")
    
    # Update bridge pointer
    data = json.loads(BRIDGE.read_text()) if BRIDGE.exists() else {}
    data["last_progress"] = entry
    data["progress_log_path"] = str(PROGRESS)
    data.setdefault("progress_count", 0)
    data["progress_count"] += 1
    BRIDGE.parent.mkdir(parents=True, exist_ok=True)
    BRIDGE.write_text(json.dumps(data, indent=2))
    print(f"Stamped: {action} ({data['progress_count']} total)")

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        action = sys.argv[1]
        detail = sys.argv[2]
        stamp(action, detail)
    else:
        print("Usage: python3 stamp_context.py <action> <detail>")
