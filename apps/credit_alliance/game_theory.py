from une.une_atomic_library import cooperation_efficiency

def marginal_contribution(hub, node_id: str) -> float:
    """
    Calculate the marginal value a node adds to the hub.
    This is inspired by Shapley value concepts.
    """
    if node_id not in hub.nodes:
        return 0.0
    
    # Value of hub with this node
    with_node = hub.get_hub_efficiency() if hasattr(hub, 'get_hub_efficiency') else len(hub.nodes)
    
    # Value without this node (simulate removal)
    original_nodes = hub.nodes.copy()
    del hub.nodes[node_id]
    without_node = hub.get_hub_efficiency() if hasattr(hub, 'get_hub_efficiency') else len(hub.nodes)
    hub.nodes = original_nodes  # restore
    
    return max(0, with_node - without_node)

def stable_coalition_check(hub) -> bool:
    """
    Check if the current hub allocation is stable (no subgroup wants to deviate).
    Uses cooperation formula as stability incentive.
    """
    n = len(hub.nodes)
    if n < 3:
        return True
    
    coop_value = cooperation_efficiency(n)
    
    # Simple stability: if cooperation multiplier is high, coalition is stable
    # In real game theory this would be more complex (core of the game)
    return coop_value > 2.5

def cooperate_vs_defect_payoff(hub, node_id: str, cooperate: bool = True) -> float:
    """
    Classic cooperative game theory payoff.
    Cooperating gives higher long-term payoff via the formula.
    Defecting gives short-term gain but damages hub stability.
    """
    base_score = hub.calculate_node_score(node_id)
    
    if cooperate:
        # Cooperation is rewarded by the formula
        return base_score * cooperation_efficiency(len(hub.nodes))
    else:
        # Defection gives immediate boost but hurts future cooperation
        return base_score * 1.8  # short-term temptation

def suggest_coalition_strategy(hub) -> str:
    """
    Simple recommendation engine using cooperative game theory.
    """
    n = len(hub.nodes)
    coop_value = cooperation_efficiency(n)
    
    if coop_value > 4.0:
        return "Strongly cooperate — hub is highly stable and efficient"
    elif coop_value > 2.5:
        return "Cooperate — good coalition value, avoid defection"
    else:
        return "Consider restructuring hub or increasing mutual support to raise cooperation value"
