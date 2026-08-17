"""swarm_query.py: Routes queries through the mesh based on current state."""
import json, os, sys, math
from pathlib import Path
from state_utils import load_ckpt, save_ckpt, stamp

UNE = Path(os.environ.get("UNE_DIR", str(Path.home() / "une")))
BASE_DEGREE = 6
MAX_DEPTH = 6

def route(query_text="default"):
    """Calculate routing cost (hops) based on mesh depth."""
    state = load_ckpt()
    nodes = max(state.get("mesh_nodes", 1), 1)
    
    # Cap depth at MAX_DEPTH
    depth = min(int(math.log(nodes, BASE_DEGREE)) if nodes >= BASE_DEGREE else 0, MAX_DEPTH)
    
    # Simulate query processing
    hops = depth + 1
    energy_cost = 0.0001 * hops
    
    state["energy_joules"] = round(state.get("energy_joules", 0.0) + energy_cost, 6)
    save_ckpt(state)
    
    return {
        "query": query_text[:50],
        "hops": hops,
        "nodes_traversed": nodes,
        "energy_cost": energy_cost
    }

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "status_check"
    result = route(query)
    print(f"[SWARM] Query: '{result['query']}' -> {result['hops']} hops, "
          f"{result['energy_cost']:.6f}J")

if __name__ == "__main__":
    main()
