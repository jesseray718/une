from une.une_atomic_library import cooperation_efficiency, unified_effective_power

def calculate_node_score(contribution_volume: float, consistency: float, help_given: float, N: int = 50):
    """Formula-driven node evaluation for hub allocation"""
    base = contribution_volume * consistency * (1 + help_given * 0.5)
    coop_boost = cooperation_efficiency(N)
    return base * coop_boost

def assign_role(node_score: float, hub_needs: list):
    """Simple role allocation based on formula output"""
    # Extend this with real logic later
    return "high_value_node" if node_score > 100 else "support_node"
