#!/data/data/com.termux/files/usr/bin/python3
"""
Divine Resonance Node Growth Calculator.
Updates mesh_nodes and fitness_score based on synergy and health.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state_utils import load_ckpt, save_ckpt

def calculate_dr_growth(current_nodes, synergy_mult, health_score):
    """
    DR = synergy_mult (from swarm) * (health/100)
    New Nodes = current_nodes * (DR ^ 1.5)
    Fitness = DR
    """
    if not synergy_mult: synergy_mult = 1.0
    if not health_score: health_score = 50
    
    # Health factor: 0.5 to 1.5
    health_factor = 0.5 + (health_score / 100.0)
    
    # Divine Resonance Score
    dr = synergy_mult * health_factor
    
    # Exponential growth based on DR
    # If DR > 1.0 -> Growth. If DR < 1.0 -> Decay/Stagnation.
    growth_factor = dr ** 1.5
    
    new_nodes = int(current_nodes * growth_factor)
    
    # Floor: 6^8 = 1,679,616
    floor = 1679616
    if new_nodes < floor:
        new_nodes = floor
        
    return {
        "dr": round(dr, 4),
        "growth_factor": round(growth_factor, 4),
        "new_nodes": new_nodes
    }

if __name__ == "__main__":
    ckpt = load_ckpt()
    current = ckpt.get('mesh_nodes', 1679616)
    health = ckpt.get('health_score', 65)
    
    # Get synergy from last cycle result if available, else default 1.0
    # For now, we simulate synergy based on health (perfect health = high synergy)
    # In a real run, this would come from the swarm result
    synergy = 1.0 + (health / 100.0) # Example: Health 65 -> Synergy 1.65
    
    result = calculate_dr_growth(current, synergy, health)
    
    print(f"Current Nodes: {current}")
    print(f"Synergy: {synergy:.2f}, Health: {health}")
    print(f"Divine Resonance (DR): {result['dr']:.4f}")
    print(f"Growth Factor: {result['growth_factor']:.4f}")
    print(f"New Nodes: {result['new_nodes']}")
    
    # Update checkpoint
    ckpt['mesh_nodes'] = result['new_nodes']
    ckpt['fitness_score'] = result['dr'] # Fitness IS the DR
    save_ckpt(ckpt)
    
    print(f"✅ Checkpoint updated: Fitness={result['dr']:.4f}, Nodes={result['new_nodes']}")
