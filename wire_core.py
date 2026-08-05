"""wire_core.py: Central hub that integrates all modules via state_utils."""
import json, os, sys
from pathlib import Path
from state_utils import load_ckpt, save_ckpt, stamp, append_lesson

UNE = Path(os.environ.get("UNE_DIR", str(Path.home() / "une")))

def connect_modules():
    """Verify all core modules exist and are importable."""
    modules = [
        "evolution_engine", "autonomous_mesh", "snapshot", 
        "dossier", "guardian_wire", "compound"
    ]
    missing = []
    for mod in modules:
        try:
            __import__(mod)
        except ImportError as e:
            missing.append(mod)
            append_lesson(f"Module missing: {mod} — {str(e)[:50]}", "warning")
    
    if not missing:
        append_lesson("All core modules connected successfully", "info")
        return True
    return False

def sync_state():
    """Ensure checkpoint is consistent."""
    state = load_ckpt()
    # Validate structure
    required_keys = ["cycle", "fitness_score", "mesh_nodes", "energy_joules", "lessons"]
    for key in required_keys:
        if key not in state:
            state[key] = 0 if key != "lessons" else []
    save_ckpt(state)
    return state

def main():
    print("[WIRE_CORE] Connecting modules...")
    connected = connect_modules()
    state = sync_state()
    
    print(f"[WIRE_CORE] State synced: cycle={state['cycle']} "
          f"fitness={state['fitness_score']} mesh={state['mesh_nodes']}")
    if connected:
        print("[WIRE_CORE] ✅ All modules online")
    else:
        print("[WIRE_CORE] ⚠️ Some modules missing")

if __name__ == "__main__":
    main()
