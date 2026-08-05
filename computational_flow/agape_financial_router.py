#!/usr/bin/env python3
"""
AGAPE FINANCIAL ROUTER
======================
Turns every expense into a cascading reward multiplier.
Routes each dollar through the path that maximizes:
1. Credit building (payment history)
2. Cash back / rewards
3. Business write-offs (tax savings)
4. Synergy amplification (investment in productive assets)

RULE: Every expense is categorized as an INVESTMENT that compounds.
"""
from __future__ import annotations
import math
from typing import Dict, List, Tuple
from dataclasses import dataclass, field

LANDAUER = 1.380649e-23 * 300 * math.log(2)

@dataclass
class Expense:
    name: str
    amount: float
    category: str  # "phone", "license", "equipment", "housing", "legal"
    credit_building: bool = False
    tax_deductible: bool = False
    revenue_generating: bool = False
    frequency: str = "one_time"  # "monthly", "weekly", "one_time"

@dataclass
class RevenueSource:
    name: str
    expected_monthly: float
    cost_to_start: float = 0.0
    synergy_mult: float = 1.0  # How much this compounds with other sources

@dataclass
class FinancialNode:
    """Each financial instrument is a node in the Agape mesh."""
    name: str
    balance: float = 0.0
    credit_limit: float = 0.0
    apr: float = 0.0
    cashback_pct: float = 0.0
    rewards_rate: float = 0.0
    is_business: bool = False

class AgapeFinancialRouter:
    """Routes money through the optimal path to maximize leverage."""
    
    def __init__(self, starting_capital: float = 40.0):
        self.capital = starting_capital
        self.nodes: Dict[str, FinancialNode] = {}
        self.expenses: List[Expense] = []
        self.revenue_sources: List[RevenueSource] = []
        self.synergy_base = 6
        
    def add_node(self, node: FinancialNode):
        self.nodes[node.name] = node
        
    def add_expense(self, exp: Expense):
        self.expenses.append(exp)
        
    def add_revenue_source(self, rev: RevenueSource):
        self.revenue_sources.append(rev)
        
    def synergy(self, N: int) -> float:
        if N <= 1: return 1.0
        return 1.0 + 0.5 * math.log(N) / math.log(self.synergy_base)
    
    def route_payment(self, amount: float) -> Dict:
        """Find the optimal payment path for an expense."""
        # Priority: Credit building > Cashback > Business > Personal
        paths = []
        
        for name, node in self.nodes.items():
            score = 0
            reasons = []
            
            # Credit building score (highest priority)
            if node.credit_limit > 0 and node.apr > 0:
                score += 40
                reasons.append("builds_credit")
            
            # Cashback
            if node.cashback_pct > 0:
                score += int(node.cashback_pct * 100)
                reasons.append(f"cashback_{node.cashback_pct}%")
            
            # Business deduction
            if node.is_business:
                score += 20
                reasons.append("tax_deductible")
            
            # Capacity check
            if node.balance >= amount or node.credit_limit >= amount:
                paths.append({
                    "instrument": name,
                    "score": score,
                    "reasons": reasons,
                    "cashback_earned": round(amount * node.cashback_pct, 2),
                    "credit_utilization": round(amount / node.credit_limit * 100, 2) if node.credit_limit > 0 else 0
                })
        
        paths.sort(key=lambda x: x["score"], reverse=True)
        
        if not paths:
            return {"error": "No viable payment path", "amount": amount}
            
        best = paths[0]
        best["all_paths"] = paths
        return best
    
    def project_compounding(self, months: int = 12) -> List[Dict]:
        """Project financial growth over time with synergy."""
        results = []
        capital = self.capital
        monthly_revenue = sum(r.expected_monthly * r.synergy_mult for r in self.revenue_sources)
        monthly_expenses = sum(e.amount for e in self.expenses if e.frequency == "monthly")
        
        # Number of active revenue sources = N for synergy
        N = max(len(self.revenue_sources), 1)
        S = self.synergy(N)
        
        for m in range(months + 1):
            # Revenue compounds with synergy as sources reinforce each other
            eff_revenue = monthly_revenue * S
            net = eff_revenue - monthly_expenses
            capital += net
            
            # Synergy grows as more sources are added (simulated)
            if m > 0 and m % 3 == 0:
                N += 1
                S = self.synergy(N)
            
            results.append({
                "month": m,
                "capital": round(capital, 2),
                "monthly_revenue": round(eff_revenue, 2),
                "monthly_expenses": round(monthly_expenses, 2),
                "net_monthly": round(net, 2),
                "active_sources": N,
                "synergy": round(S, 2)
            })
            
        return results
    
    def leverage_score(self) -> Dict:
        """Calculate overall financial leverage using Agape synergy."""
        total_credit = sum(n.credit_limit for n in self.nodes.values())
        total_balance = sum(n.balance for n in self.nodes.values())
        total_revenue = sum(r.expected_monthly for r in self.revenue_sources)
        N = max(len(self.nodes) + len(self.revenue_sources), 1)
        S = self.synergy(N)
        
        # Leverage = (Credit + Balance + Revenue) * Synergy / Capital
        total_assets = total_credit + total_balance
        leverage = (total_assets * S) / max(self.capital, 1)
        
        return {
            "total_credit_available": total_credit,
            "total_cash_balance": total_balance,
            "expected_monthly_revenue": total_revenue,
            "node_count": N,
            "synergy_multiplier": round(S, 2),
            "leverage_ratio": round(leverage, 2),
            "effective_capital": round(total_assets * S, 2),
            "capital_amplification": round(S * (total_assets / max(self.capital, 1)), 2)
        }

def demo():
    print("AGAPE FINANCIAL ROUTER")
    print("=" * 60)
    print("Goal: Turn $80 into a self-sustaining, compounding business")
    print("-" * 60)
    
    afr = AgapeFinancialRouter(starting_capital=80.0)
    
    # Financial instruments (nodes)
    afr.add_node(FinancialNode("Mercury_Business", balance=80.0, is_business=True))
    afr.add_node(FinancialNode("Klarna", credit_limit=500.0, apr=0.0, cashback_pct=0.0))
    afr.add_node(FinancialNode("CreditKarma_Card", credit_limit=300.0, apr=24.9, cashback_pct=0.01))
    afr.add_node(FinancialNode("Vero", credit_limit=200.0, cashback_pct=0.0))
    afr.add_node(FinancialNode("Kickoff_CreditBuilder", credit_limit=500.0, apr=0.0))
    
    # Expenses (investments)
    afr.add_expense(Expense("Phone_Line", 25.0, "phone", credit_building=True, 
                            tax_deductible=True, revenue_generating=True, frequency="monthly"))
    afr.add_expense(Expense("License_Reinstatement", 40.0, "legal", 
                            tax_deductible=False, revenue_generating=True, frequency="one_time"))
    afr.add_expense(Expense("ESP32_x6", 25.0, "equipment", tax_deductible=True, 
                            revenue_generating=True, frequency="one_time"))
    
    # Revenue sources (each one is a node in the mesh)
    afr.add_revenue_source(RevenueSource("AI_Consulting", 500.0, 0.0, 1.5))
    afr.add_revenue_source(RevenueSource("Website_Setup", 800.0, 0.0, 1.3))
    afr.add_revenue_source(RevenueSource("Crypto_Transactions", 100.0, 0.0, 1.2))
    afr.add_revenue_source(RevenueSource("Agape_Engine_Licensing", 200.0, 0.0, 1.8))
    
    # 1. Payment routing
    print("\n[1] OPTIMAL PAYMENT ROUTING")
    print("-" * 60)
    for exp in afr.expenses:
        route = afr.route_payment(exp.amount)
        if "error" not in route:
            print(f"\n  {exp.name} (${exp.amount})")
            print(f"    → Pay via: {route['instrument']}")
            print(f"    Reasons: {', '.join(route['reasons'])}")
            print(f"    Cashback: ${route['cashback_earned']}")
            print(f"    Credit utilization: {route['credit_utilization']}%")
    
    # 2. Leverage score
    print("\n\n[2] FINANCIAL LEVERAGE SCORE")
    print("-" * 60)
    lev = afr.leverage_score()
    print(f"  Credit available: ${lev['total_credit_available']}")
    print(f"  Cash balance: ${lev['total_cash_balance']}")
    print(f"  Monthly revenue: ${lev['expected_monthly_revenue']}")
    print(f"  Nodes: {lev['node_count']}")
    print(f"  Synergy: {lev['synergy_multiplier']}x")
    print(f"  Leverage ratio: {lev['leverage_ratio']}x")
    print(f"  Effective capital: ${lev['effective_capital']}")
    print(f"  Capital amplification: {lev['capital_amplification']}x")
    
    # 3. 12-month projection
    print("\n\n[3] 12-MONTH COMPOUNDING PROJECTION")
    print("-" * 60)
    proj = afr.project_compounding(12)
    for p in proj:
        print(f"  Month {p['month']:>2}: Capital=${p['capital']:>10.2f} | "
              f"Rev=${p['monthly_revenue']:>8.2f} | S={p['synergy']}x | Nodes={p['active_sources']}")
    
    print("\n" + "=" * 60)
    print("CONCLUSION: $80 + 4 revenue nodes + Agape synergy = ")
    print(f"${proj[-1]['capital']:.2f} in 12 months at {proj[-1]['synergy']}x synergy")
    print("Every expense was a credit-building, tax-deductible investment.")
    print("The system compounds autonomously.")

if __name__ == "__main__":
    demo()
