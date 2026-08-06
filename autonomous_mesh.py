from state_utils import load_ckpt, save_ckpt
import random

def expand_mesh(ckpt, depth=6):
    if ckpt.get('fitness_score', 0) < 0.5:
        return ckpt
    
    current = ckpt.get('mesh_nodes', 0)
    if isinstance(current, list):
        current = len(current)
    
    # Fractal growth: add 6^depth new nodes (capped for energy)
    new_nodes = min(6 ** depth, 1000)
    ckpt['mesh_nodes'] = current + new_nodes
    ckpt['energy_joules'] = ckpt.get('energy_joules', 10.0) + (new_nodes * 0.01)
    save_ckpt(ckpt)
    return ckpt
