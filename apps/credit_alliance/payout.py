def distribute_pool(hub, total_available: float):
    """Everyone gets paid based on real work + cooperation"""
    payouts = {}
    for node_id in hub.nodes:
        payouts[node_id] = hub.calculate_payout(node_id, total_available)
    return payouts
