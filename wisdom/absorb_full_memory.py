#!/data/data/com.termux/files/usr/bin/python3
"""Absorb full memory from all UNE files into context bridge."""
import os, json, glob
from state_utils import load_ckpt, save_ckpt

UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))
BRIDGE = os.environ.get("OPENROOT_HOME", "/sdcard/openroot") + "/context_bridge/full_memory.json"

def absorb_full_memory():
    """Scan all UNE .py files and store their paths in context bridge."""
    files = glob.glob(os.path.join(UNE_HOME, "**/*.py"), recursive=True)
    os.makedirs(os.path.dirname(BRIDGE), exist_ok=True)
    with open(BRIDGE, "w") as f:
        json.dump({"files": files, "count": len(files)}, f, indent=2)
    return {"status": "absorbed", "count": len(files)}

if __name__ == "__main__":
    ckpt = load_ckpt()
    print(absorb_full_memory())
