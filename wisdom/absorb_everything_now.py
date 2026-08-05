#!/data/data/com.termux/files/usr/bin/python3
"""Absorb everything now — fast dump of all state."""
import os, json, glob, time

UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))
OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
OUT = OPENROOT + "/context_bridge/everything_now.json"

def absorb_everything_now():
    """Dump all .py, .sh, .md, .json file list with timestamps."""
    patterns = ["**/*.py", "**/*.sh", "**/*.md", "**/*.json"]
    files = []
    for pat in patterns:
        files.extend(glob.glob(os.path.join(UNE_HOME, pat), recursive=True))
    
    entries = [{"path": f, "mtime": os.path.getmtime(f)} for f in files if os.path.exists(f)]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump({"timestamp": time.time(), "entries": entries}, f, indent=2)
    return {"status": "absorbed", "count": len(entries)}

if __name__ == "__main__":
    print(absorb_everything_now())
