#!/data/data/com.termux/files/usr/bin/python3
"""Absorb wisdom corpus into context bridge."""
import os, json
from state_utils import load_ckpt, save_ckpt

CORPUS = os.environ.get("UNE_HOME", os.path.expanduser("~/une")) + "/wisdom/wisdom_corpus.json"
BRIDGE = os.environ.get("OPENROOT_HOME", "/sdcard/openroot") + "/context_bridge/context.json"

def absorb():
    """Load corpus and inject into context bridge."""
    if not os.path.exists(CORPUS):
        return {"status": "no corpus"}
    with open(CORPUS) as f:
        data = json.load(f)
    os.makedirs(os.path.dirname(BRIDGE), exist_ok=True)
    with open(BRIDGE, "w") as f:
        json.dump({"corpus": data}, f, indent=2)
    return {"status": "absorbed", "entries": len(data) if isinstance(data, list) else len(data.keys())}

if __name__ == "__main__":
    ckpt = load_ckpt()
    print(absorb())
