import os, math
from pathlib import Path
from state_utils import load_ckpt, save_ckpt, stamp

UNE = Path(os.environ.get("UNE_DIR", str(Path.home() / "une")))
BASE_DEGREE = 6
# REMOVED HARD CAP: Allow fractal scaling based on fitness
# MAX_DEPTH = 6  # Deleted

def expand_mesh(state):
    fitness = state.get("fitness_score", 0.0)
    current_nodes = state.get("mesh_nodes", 1)
    
    # Fractal growth: expand if fitness > 0.5, no hard cap
    if fitness < 0.5:
        return f"HOLDING at {current_nodes} nodes (fitness={fitness:.2f} < 0.5)"
    
    # Calculate next depth dynamically
    current_depth = int(math.log(current_nodes, BASE_DEGREE)) if current_nodes >= BASE_DEGREE else 0
    new_nodes = BASE_DEGREE ** (current_depth + 1)
    
    # Safety: stop if nodes exceed device RAM estimate (approx 100M nodes on mobile)
    if new_nodes > 100_000_000:
        return f"CAP REACHED (RAM limit) at {current_nodes} nodes"
        
    energy_cost = 0.0001 * (new_nodes - current_nodes)
    state["mesh_nodes"] = new_nodes
    state["energy_joules"] = round(state.get("energy_joules", 0.0) + energy_cost, 6)
    return f"EXPANDED to {new_nodes} nodes (depth {current_depth + 1})"

def route_query(state, query="default"):
    nodes = max(state.get("mesh_nodes", 1), 1)
    depth = max(int(math.log(nodes, BASE_DEGREE)), 1) if nodes >= BASE_DEGREE else 1
    return depth

def main():
    state = load_ckpt()
    expansion = expand_mesh(state)
    hops = route_query(state)
    state["timestamp"] = stamp()
    save_ckpt(state)
    print(f"[MESH] {expansion}")
    print(f"[MESH] query routing cost: {hops} hops")

if __name__ == "__main__":
    main()
