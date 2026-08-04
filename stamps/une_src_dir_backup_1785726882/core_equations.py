"""
UNE Core Equations — executable, modular, non-proprietary.
All quantities in joules, seconds, kilograms.
Nothing else is accepted as a fundamental output.
"""

from typing import Dict

# ─── 1. Fundamental ratios ─────────────────────────────

def efficiency(useful_joules: float, human_joules: float) -> float:
    """η = J_useful / J_human"""
    if human_joules <= 0:
        return float("inf") if useful_joules > 0 else 0.0
    return useful_joules / human_joules


def substitution_valid(human_before: float, human_after: float,
                       non_human: float, useful_before: float,
                       useful_after: float) -> bool:
    """True only if human work decreases and useful output does not fall."""
    return (human_after + non_human < human_before) and (useful_after >= useful_before)


def composition_beneficial(eta_a: float, eta_b: float, eta_ab: float) -> bool:
    """True if combining A and B raises efficiency above either alone."""
    return eta_ab > max(eta_a, eta_b)


def surplus_retained(producer_controlled: bool) -> bool:
    """Hard rule: surplus must remain under producer control."""
    return producer_controlled


# ─── 2. Physical constants ────────────────────────────

kT_ln2 = 2.875e-21          # J per bit at 300 K (Landauer)
c_squared = 8.98755179e16   # c² in m²/s²


def mass_of_energy(joules: float) -> float:
    """E=mc² → m = E/c²"""
    return joules / c_squared


def landauer_cost(bits: int) -> float:
    """Minimum irreversible cost in joules for erasing N bits."""
    return bits * kT_ln2


def landauer_mass(bits: int) -> float:
    """Mass equivalent of the Landauer cost of erasing N bits."""
    return mass_of_energy(landauer_cost(bits))


# ─── 3. Generic process evaluator ─────────────────────

def evaluate_process(
    useful_joules: float,
    human_joules: float,
    non_human_joules: float = 0.0,
    producer_controls_surplus: bool = True,
) -> Dict[str, float | bool]:
    """Single call that returns only physical results."""
    eta = efficiency(useful_joules, human_joules)
    return {
        "eta": eta,
        "useful_joules": useful_joules,
        "human_joules": human_joules,
        "non_human_joules": non_human_joules,
        "landauer_cost_J": landauer_cost(256),
        "mass_equivalent_kg": mass_of_energy(human_joules),
        "surplus_retained": surplus_retained(producer_controls_surplus),
        "accepted": eta > 1.0 and producer_controls_surplus,
    }


print("=== UNE Core Equations loaded ===")
