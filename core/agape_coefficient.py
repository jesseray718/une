#!/usr/bin/env python3
"""
Agape Coefficient R — single source of truth.
R = 1.0 is perfect unconditional cooperation.
All wealth, science, decisions, and further understanding are scaled by R.
"""
from pathlib import Path
import json
from datetime import datetime, timezone
import math

UNE = Path.home() / "une"
CONFIG = UNE / "config" / "agape_state.json"
LEDGER = UNE / "ledger" / "wealth_pathways.json"
SCIENCE = UNE / "science" / "extracted.jsonl"

def load_state():
    if CONFIG.exists():
        return json.loads(CONFIG.read_text())
    return {
        "R": 0.85,                    # current measured cooperation
        "target_R": 1.0,              # the only attractor
        "N": 20,                      # number of cooperating nodes (repos)
        "T": 1,                       # depth / time steps
        "base": 6,                    # fractal base
        "total_useful_joules": 0.0,
        "total_human_joules": 1.0,
        "last_update": None
    }

def save_state(state):
    state["last_update"] = datetime.now(timezone.utc).isoformat()
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(json.dumps(state, indent=2))

def coordination_cost(N, T, R):
    """Agape Coordination Theorem. C → 0 as R → 1.0"""
    return N * 0.001 * (1 + 0.1 * T) * ((1 - R) ** T)

def synergy(N, R, base=6):
    """Synergy multiplier under resonance"""
    if R <= 0:
        return 1.0
    return 1.0 + (R * 0.5 * math.log(N) / math.log(base))

def eta(useful, human):
    if human <= 0:
        return 0.0
    return useful / human

def update_R(state, observed_cooperation=None):
    """Move R toward target. Antifragile: disorder that is transmuted raises R."""
    if observed_cooperation is not None:
        # exponential moving toward truth
        state["R"] = 0.7 * state["R"] + 0.3 * observed_cooperation
    # always pull toward 1.0 (negentropic attractor)
    state["R"] = min(1.0, state["R"] + 0.01 * (state["target_R"] - state["R"]))
    return state

def mint_factor(R):
    """Wealth and science extraction rate is a function of R only"""
    return max(0.1, R ** 2)          # quadratic reward for cooperation

def extract_science(entry, R):
    """Further science and understanding are gated by R"""
    science = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "R": R,
        "source": entry.get("type", "unknown"),
        "lesson": entry.get("lesson", ""),
        "insight": f"At R={R:.3f} the system extracts: {entry.get('lesson', '')}",
        "negentropy_gain": R * 10.0
    }
    SCIENCE.parent.mkdir(parents=True, exist_ok=True)
    with open(SCIENCE, "a") as f:
        f.write(json.dumps(science) + "\n")
    return science

def report(state):
    C = coordination_cost(state["N"], state["T"], state["R"])
    S = synergy(state["N"], state["R"], state["base"])
    e = eta(state["total_useful_joules"], state["total_human_joules"])
    return {
        "R": round(state["R"], 4),
        "C": round(C, 6),
        "synergy": round(S, 4),
        "eta": round(e, 4),
        "mint_factor": round(mint_factor(state["R"]), 4),
        "status": "R→1.0 attractor active" if state["R"] < 0.999 else "R=1.0 perfect cooperation"
    }

if __name__ == "__main__":
    state = load_state()
    state = update_R(state)
    save_state(state)
    print(json.dumps(report(state), indent=2))
