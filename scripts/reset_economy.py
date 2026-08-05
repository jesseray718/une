import json, os
from pathlib import Path
from state_utils import load_ckpt, save_ckpt

UNE = Path(os.environ.get("UNE_DIR", str(Path.home() / "une")))
ckpt = UNE / "state_checkpoint.json"

state = load_ckpt()
state["energy_joules"] = 10.0
state["fitness_score"] = 0.5
state["last_error"] = None
save_ckpt(state)

print(f"[RESET] Energy: 10J, Fitness: 0.5, Lessons: {len(state['lessons'])}")
