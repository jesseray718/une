from state_utils import load_ckpt, save_ckpt
import random

AXIOMS = [
    'observe_and_interact',
    'catch_and_store_energy',
    'obtain_a_yield',
    'apply_self_regulation_and_accept_feedback',
    'use_and_value_renewable_resources',
    'produce_no_waste',
    'design_from_patterns_to_details',
    'integrate_rather_than_segregate',
    'use_small_and_slow_solutions',
    'use_and_value_diversity',
    'use_edges_and_value_the_marginal',
    'creatively_use_and_respond_to_change'
]

def mutate_strategy(strategy):
    if random.random() < 0.3:
        strategy['efficiency'] = strategy.get('efficiency', 1.0) * random.uniform(0.9, 1.1)
        strategy['axioms'] = strategy.get('axioms', [])
        strategy['axioms'].append(random.choice(AXIOMS))
    return strategy

def evolve_cycle(ckpt):
    ckpt['cycle'] = ckpt.get('cycle', 0) + 1
    
    current_fitness = ckpt.get('fitness_score', 0.0)
    delta = random.uniform(-0.02, 0.05)
    ckpt['fitness_score'] = max(0, min(1, current_fitness + delta))
    
    # Log the lesson
    axiom = random.choice(AXIOMS)
    joules = round(random.uniform(0.001, 0.04), 9)
    ckpt.setdefault('lessons', []).append({
        'cycle': ckpt['cycle'],
        'axiom': axiom,
        'joules': joules,
        'ts': __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()
    })
    
    # Small energy cost per cycle
    ckpt['energy_joules'] = ckpt.get('energy_joules', 10.0) + round(joules, 6)
    
    save_ckpt(ckpt)
    return ckpt
