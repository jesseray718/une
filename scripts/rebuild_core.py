import os
from pathlib import Path

UNE = Path(os.environ.get("UNE_DIR", str(Path.home() / "une")))

files = {
    "wire_core.py": """
import json, os, sys
from pathlib import Path
from state_utils import load_ckpt, save_ckpt, stamp, append_lesson

UNE = Path(os.environ.get("UNE_DIR", str(Path.home() / "une")))

def connect_modules():
    modules = ["evolution_engine", "autonomous_mesh", "snapshot", "dossier", "guardian_wire", "compound"]
    missing = []
    for mod in modules:
        try:
            __import__(mod)
        except ImportError as e:
            missing.append(mod)
            append_lesson(f"Module missing: {mod}", "warning")
    if not missing:
        append_lesson("All core modules connected", "info")
    return not missing

def sync_state():
    state = load_ckpt()
    required = ["cycle", "fitness_score", "mesh_nodes", "energy_joules", "lessons"]
    for k in required:
        if k not in state:
            state[k] = 0 if k != "lessons" else []
    save_ckpt(state)
    return state

def main():
    print("[WIRE_CORE] Connecting modules...")
    connected = connect_modules()
    state = sync_state()
    print(f"[WIRE_CORE] State: cycle={state['cycle']} fitness={state['fitness_score']}")
    print("[WIRE_CORE] ✅ Online" if connected else "[WIRE_CORE] ⚠️ Missing modules")

if __name__ == "__main__":
    main()
""",
    "swarm_query.py": """
import math, sys
from pathlib import Path
from state_utils import load_ckpt, save_ckpt

UNE = Path(os.environ.get("UNE_DIR", str(Path.home() / "une")))
BASE_DEGREE = 6

def route(query="default"):
    state = load_ckpt()
    nodes = max(state.get("mesh_nodes", 1), 1)
    depth = int(math.log(nodes, BASE_DEGREE)) if nodes >= BASE_DEGREE else 0
    hops = depth + 1
    energy_cost = 0.0001 * hops
    state["energy_joules"] = round(state.get("energy_joules", 0.0) + energy_cost, 6)
    save_ckpt(state)
    return {"query": query[:50], "hops": hops, "energy": energy_cost}

def main():
    q = sys.argv[1] if len(sys.argv) > 1 else "status"
    r = route(q)
    print(f"[SWARM] {r['query']} -> {r['hops']} hops, {r['energy']:.6f}J")

if __name__ == "__main__":
    main()
""",
    # Add other core files similarly...
}

for fname, content in files.items():
    (UNE / fname).write_text(content)
    print(f"[REBUILD] {fname}")
