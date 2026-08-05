"""kernel_init.py: Initializes the UNE system."""
import os, sys, subprocess
from pathlib import Path
from state_utils import load_ckpt, save_ckpt, stamp

UNE = Path(os.environ.get("UNE_DIR", str(Path.home() / "une")))

def init():
    """Create directories and initial state."""
    dirs = ["logs", "lessons", "bin", "relay", "storage", "aec", "snapshots", "meta_hub"]
    for d in dirs:
        (UNE / d).mkdir(parents=True, exist_ok=True)
    
    state = load_ckpt()
    if state["cycle"] == 0:
        state["timestamp"] = stamp()
        state["merkle_root"] = "init"
        save_ckpt(state)
        print("[KERNEL] System initialized")
    else:
        print(f"[KERNEL] System active at cycle {state['cycle']}")

def main():
    init()

if __name__ == "__main__":
    main()
