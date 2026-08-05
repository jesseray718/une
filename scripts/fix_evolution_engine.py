import random
from pathlib import Path
from state_utils import load_ckpt, save_ckpt, stamp, append_lesson

UNE = Path(os.environ.get("UNE_DIR", str(Path.home() / "une")))
AXIOMS = [
    "observe_and_interact", "catch_and_store_energy", "obtain_a_yield",
    "apply_self_regulation_and_accept_feedback", "use_and_value_renewable_resources",
    "produce_no_waste", "design_from_patterns_to_details", "integrate_rather_than_segregate",
    "use_small_and_slow_solutions", "use_and_value_diversity",
    "use_edges_and_value_the_marginal", "creatively_use_and_respond_to_change"
]

def evaluate_fitness(state):
    lesson_count = len(state.get("lessons", []))
    energy = state.get("energy_joules", 0.0)
    cycle = max(state.get("cycle", 0), 1)
    
    base_rate = lesson_count / cycle
    # Dynamic penalty: energy ratio relative to cycle count
    energy_ratio = min(energy / (cycle * 10.0), 10.0) 
    penalty = min(energy_ratio * 0.05, 1.0) 
    
    raw_fitness = max(0.0, base_rate * (1 - penalty))
    return round(min(raw_fitness, 1.0), 4)

def evolve(state):
    axiom = random.choice(AXIOMS)
    mutation_energy = random.uniform(0.0001, 0.005) 
    
    state["cycle"] = state.get("cycle", 0) + 1
    state["energy_joules"] = round(state.get("energy_joules", 0.0) + mutation_energy, 6)
    
    lesson_text = f"cycle {state['cycle']}: applied '{axiom}' ({mutation_energy:.6f} J)"
    state["lessons"].append({
        "cycle": state["cycle"],
        "axiom": axiom,
        "joules": mutation_energy,
        "ts": stamp()
    })
    
    state["fitness_score"] = evaluate_fitness(state)
    return axiom, lesson_text

def main():
    state = load_ckpt()
    axiom, lesson_text = evolve(state)
    state["timestamp"] = stamp()
    append_lesson(lesson_text)
    save_ckpt(state)
    print(f"[EVOLVE] cycle={state['cycle']} axiom={axiom} "
          f"fitness={state['fitness_score']} energy={state['energy_joules']:.6f}J")

if __name__ == "__main__":
    main()
