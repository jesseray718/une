from state_utils import load_ckpt
import json
from datetime import datetime, timezone

def generate_dossier(ckpt):
    mesh = ckpt.get('mesh_nodes', 0)
    node_count = mesh if isinstance(mesh, int) else len(mesh)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cycle": ckpt.get('cycle', 0),
        "fitness": ckpt.get('fitness_score', 0),
        "nodes": node_count,
        "energy": ckpt.get('energy_joules', 0),
        "health": ckpt.get('health_score', 0),
        "lessons": len(ckpt.get('lessons', []))
    }

if __name__ == "__main__":
    ckpt = load_ckpt()
    d = generate_dossier(ckpt)
    print(json.dumps(d, indent=2))
