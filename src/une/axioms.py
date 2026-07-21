"""
Executable axioms / postulates for the UNE foundation.
Every calculation result must obey these.
"""


def axiom_efficiency_non_negative(useful: float, human: float) -> bool:
    """η must be ≥ 0"""
    from une.core_equations import efficiency
    return efficiency(useful, human) >= 0.0


def axiom_substitution_preserves_output(human_before, human_after, non_human,
                                        useful_before, useful_after) -> bool:
    """Substitution is only valid if useful output does not fall"""
    from une.core_equations import substitution_valid
    return substitution_valid(human_before, human_after, non_human,
                              useful_before, useful_after)


def axiom_composition_increases_eta(eta_a, eta_b, eta_ab) -> bool:
    """Combining modules is only beneficial if η rises"""
    from une.core_equations import composition_beneficial
    return composition_beneficial(eta_a, eta_b, eta_ab)


def axiom_labor_intensity_positive(person_hours: float, volume: float) -> bool:
    """Labor intensity is never negative"""
    from une.foundation_calc import labor_intensity
    return labor_intensity(person_hours, volume) >= 0.0


def check_all_axioms(**kwargs) -> list[str]:
    """Return list of violated axiom names (empty = all passed)"""
    violations = []
    if "useful" in kwargs and "human" in kwargs:
        if not axiom_efficiency_non_negative(kwargs["useful"], kwargs["human"]):
            violations.append("efficiency_non_negative")
    if "person_hours" in kwargs and "volume" in kwargs:
        if not axiom_labor_intensity_positive(kwargs["person_hours"], kwargs["volume"]):
            violations.append("labor_intensity_positive")
    return violations
