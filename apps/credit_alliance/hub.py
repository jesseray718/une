from une.une_atomic_library import cooperation_efficiency, unified_effective_power

class CreditAllianceHub:
    def __init__(self, hub_id: str, target_size: int = 50):
        self.hub_id = hub_id
        self.target_size = target_size
        self.nodes = {}
        self.total_pool = 0.0

    def add_contribution(self, node_id: str, volume: float, consistency: float = 1.0, help_given: float = 0.0, work_type: str = "general"):
        if node_id not in self.nodes:
            self.nodes[node_id] = {
                "contribution": 0, 
                "consistency": 1.0, 
                "help_given": 0.0,
                "work_history": []
            }
        self.nodes[node_id]["contribution"] += volume
        self.nodes[node_id]["consistency"] = max(0.5, min(1.0, consistency))
        self.nodes[node_id]["help_given"] += help_given
        self.nodes[node_id]["work_history"].append({"type": work_type, "volume": volume})
        self.total_pool += volume

    def calculate_node_score(self, node_id: str) -> float:
        data = self.nodes.get(node_id)
        if not data: return 0
        base = data["contribution"] * data["consistency"] * (1 + data["help_given"] * 0.5)
        return base * cooperation_efficiency(len(self.nodes) or 1)

    def calculate_payout(self, node_id: str, total_available: float) -> float:
        """Fair distribution based on contribution + cooperation multiplier"""
        score = self.calculate_node_score(node_id)
        total_score = sum(self.calculate_node_score(n) for n in self.nodes)
        if total_score == 0: return 0
        share = (score / total_score) * total_available
        return round(share, 2)

    def assign_role(self, node_id: str) -> str:
        score = self.calculate_node_score(node_id)
        if score > 180: return "high_value_node"
        elif score > 100: return "core_contributor"
        else: return "support_node"

    def get_tier(self, node_id: str) -> str:
        score = self.calculate_node_score(node_id)
        if score > 220: return "Platinum"
        elif score > 140: return "Gold"
        elif score > 70: return "Silver"
        else: return "Bronze"

    def get_hub_summary(self) -> dict:
        return {
            "total_nodes": len(self.nodes),
            "total_contribution": round(self.total_pool, 2),
            "average_score": round(sum(self.calculate_node_score(n) for n in self.nodes) / max(len(self.nodes), 1), 2)
        }

    def get_game_theory_insight(self, node_id: str = None) -> dict:
        from .game_theory import stable_coalition_check, suggest_coalition_strategy, cooperate_vs_defect_payoff
        
        return {
            "coalition_stable": stable_coalition_check(self),
            "strategy_recommendation": suggest_coalition_strategy(self),
            "cooperate_payoff_example": cooperate_vs_defect_payoff(self, list(self.nodes.keys())[0]) if self.nodes else 0
        }
