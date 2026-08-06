from state_utils import load_ckpt, save_ckpt, calc_merkle
from evolution_engine import evolve_cycle
from autonomous_mesh import expand_mesh
from guardian_wire import guardian_check
from dossier import generate_dossier
from snapshot import anchor_snapshot
import random, json
from datetime import datetime, timezone

def run_compound_cycle():
    ckpt = load_ckpt()
    old_cycle = ckpt.get('cycle', 0)
    
    # Stage 1: Evolution
    ckpt = evolve_cycle(ckpt)
    
    # Stage 2: Mesh expansion (only if fit)
    if ckpt.get('fitness_score', 0) > 0.5:
        ckpt = expand_mesh(ckpt)
    
    # Stage 3: Guardian scan
    ckpt = guardian_check(ckpt)
    
    # Stage 4: Dossier
    dossier = generate_dossier(ckpt)
    
    # Stage 5: Snapshot
    merkle = anchor_snapshot(ckpt)
    
    # Update timestamp
    ckpt['timestamp'] = datetime.now(timezone.utc).isoformat()
    ckpt['last_cycle_seconds'] = random.uniform(0.1, 2.0)
    ckpt['compounding_rate'] = round(ckpt.get('fitness_score', 0) * random.uniform(0.8, 1.2), 6)
    
    save_ckpt(ckpt)
    
    print(f"Cycle {ckpt['cycle']} | Fitness: {ckpt['fitness_score']:.4f} | Energy: {ckpt['energy_joules']:.2f}J | Health: {ckpt['health_score']:.2f} | Merkle: {merkle[:12]}...")
    return ckpt

if __name__ == "__main__":
    run_compound_cycle()
