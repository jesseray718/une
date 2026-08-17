#!/usr/bin/env python3
"""Safe seed extractor — absolute paths only, no tilde, no expansion."""
import json
import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone

HOME = Path(os.environ.get("HOME", "/data/data/com.termux/files/home"))
OPENROOT = Path("/sdcard/openroot")
SEED = OPENROOT / "session_seeds" / "current_seed.json"
UNE = HOME / "une"

def main():
    if not SEED.exists():
        print("NO SEED")
        return 1
    data = json.loads(SEED.read_text())
    print("SEED KEYS:", sorted(data.keys()))
    print("timestamp:", data.get("timestamp"))
    print("eta3:", data.get("eta3") or data.get("η³"))
    # optional git status from une root (absolute)
    try:
        r = subprocess.run(
            ["git", "status", "-sb"],
            capture_output=True, text=True, cwd=str(UNE), timeout=8
        )
        print("git:", r.stdout.strip()[:200] if r.returncode == 0 else "git fail")
    except Exception as e:
        print("git error:", e)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
