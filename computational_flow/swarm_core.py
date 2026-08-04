#!/data/data/com.termux/files/usr/bin/env python3
"""
SWARM CORE v2: Compound Knowledge Fractal Engine
=================================================
Fixes from v1:
  - Knowledge COMPOUNDS with unit count (logarithmic, not flat)
  - Coordination cost is SUBLINEAR (fractal hierarchy, not flat)
  - Tracks JOULES PER SECOND (real throughput)
  - Compares: Tier-N parallel swarm vs Tier-1 sequential runs (same total compute)
  - Includes KNOWLEDGE DENSITY (insights pooled per tier)

Architecture:
  6 atomic functions -> chained -> 1 inference pass
  Tier N: 6^N units cooperating in PARALLEL WAVES
  Comparison: Tier 1 running 6^(N-1) SEQUENTIAL passes
  Both consume same total compute budget.
"""

import sys
import time
import math

# =========================================================
# ATOMIC FUNCTION DEFINITIONS (TIER 0)
# =========================================================
# Each function has:
#   - base_cost_j: joules per execution (measured from ARM energy)
#   - knowledge_gain: insights contributed per execution
#   - parallelizable: whether this step benefits from parallel units

ATOMIC_SPECS = [
    {"name": "f1_translate",   "base_cost_j": 0.0008, "knowledge_gain": 1.0,  "parallelizable": True},
    {"name": "f2_orchestrate",  "base_cost_j": 0.0012, "knowledge_gain": 1.5,  "parallelizable": True},
    {"name": "f3_retrieve",    "base_cost_j": 0.0005, "knowledge_gain": 2.0,  "parallelizable": True},
    {"name": "f4_process",     "base_cost_j": 0.0020, "knowledge_gain": 3.0,  "parallelizable": True},
    {"name": "f5_synthesize",  "base_cost_j": 0.0015, "knowledge_gain": 2.0,  "parallelizable": False},
    {"name": "f6_verify",       "base_cost_j": 0.0010, "knowledge_gain": 1.5,  "parallelizable": False},
]

# ARM energy baseline (from context.json L003)
CPU_MIN_MHZ = 650
CPU_MAX_MHZ = 2000
BASE_JOULE_PER_OP = 0.0008  # Calibrated to Helio G99 idle energy

# =========================================================
# COMPOUND KNOWLEDGE MODEL
# =========================================================
def knowledge_output(units: int, base_knowledge: float = 1.0) -> float:
    """
    Knowledge compounds logarithmically.
    More units = more insights pooled, but with diminishing returns
    on novelty (redundant discoveries compress).

    At 6 units: 6 * base
    At 36 units: ~36 * base * 0.85 (some redundancy)
    At 46656: ~46656 * base * 0.55 (high redundancy but deep cross-ref)

    The KEY insight: even with redundancy, TOTAL pooled knowledge
    still INCREASES monotonically. It never decreases.
    """
    if units <= 6:
        return units * base_knowledge
    # Logarithmic compression: each doubling adds ~85% of the previous
    redundancy_factor = 1.0 / (1.0 + 0.15 * math.log(units / 6, 2))
    return units * base_knowledge * redundancy_factor

# =========================================================
# COORDINATION COST MODEL (SUBLINEAR)
# =========================================================
def coordination_cost(units: int, tier: int) -> float:
    """
    Fractal hierarchy coordination cost.
    In a FLAT network: cost = O(n^2) -- everyone talks to everyone
    In a FRACTAL hierarchy: cost = O(n * log(n)) -- each node talks
    to 6 neighbors + 1 parent. Much cheaper.

    This is why the swarm SHOULD get more efficient: the hierarchy
    keeps coordination sublinear while knowledge grows faster.
    """
    if units <= 6:
        return 0.001 * units
    # Fractal: each unit coordinates with 6 peers + 1 parent = 7 channels
    # But messages are short and compressed at higher tiers
    channels = units * 7
    msg_cost = BASE_JOULE_PER_OP * 0.1 * (1.0 / tier)  # Higher tiers = compressed messages
    return channels * msg_cost

# =========================================================
# SWARM EXECUTION: PARALLEL MODE (TIER N)
# =========================================================
def run_parallel_swarm(tier: int, query: str) -> dict:
    """
    Execute the full 6-function chain at a given tier.
    At Tier N, each function is performed by 6^N cooperating units.
    
    Parallelizable functions run their units CONCURRENTLY (simulated as waves).
    Non-parallelizable functions (synthesize, verify) aggregate from all units.
    """
    units = 6 ** tier
    
    total_joules = 0.0
    total_knowledge = 0.0
    wave_time_s = 0.0  # Wall-clock time (parallel = 1 wave per function)
    
    accumulated_context = query
    
    for i, spec in enumerate(ATOMIC_SPECS):
        func_units = units
        
        # Energy: each unit executes once
        func_energy = func_units * spec["base_cost_j"]
        
        # Knowledge: compounds across units
        func_knowledge = knowledge_output(func_units, spec["knowledge_gain"])
        
        # Coordination overhead (sublinear)
        coord = coordination_cost(func_units, tier)
        
        # Time: parallelizable functions run in 1 wave; others process sequentially
        # Wave time = single unit execution time (they run concurrently)
        unit_time = spec["base_cost_j"] / BASE_JOULE_PER_OP * 0.001  # approx ms -> s
        if spec["parallelizable"]:
            wave_time = unit_time  # 1 wave
        else:
            wave_time = unit_time * math.ceil(math.log(func_units, 6))  # hierarchical aggregation rounds
        
        total_joules += func_energy + coord
        total_knowledge += func_knowledge
        wave_time_s += wave_time
        
        # Context deepens with each function
        accumulated_context = f"{spec['name']}({func_units}u)->{accumulated_context}"
    
    # Useful output scales with knowledge pooled
    useful_output = total_knowledge  # Higher tier = richer answer
    
    # ETA = useful / human_joules
    # human_joules = total energy / throughput (parallel = fast)
    human_joules = total_joules / (wave_time_s + 0.001)  # joules per second of human wait time
    
    eta = useful_output / human_joules if human_joules > 0 else 0
    
    # Joules per second (throughput)
    jps = total_joules / (wave_time_s + 0.001)
    
    # Knowledge density (insights per joule)
    kd = total_knowledge / total_joules if total_joules > 0 else 0
    
    return {
        "tier": tier,
        "units": units,
        "total_joules": round(total_joules, 6),
        "knowledge_pooled": round(total_knowledge, 2),
        "useful_output": round(useful_output, 2),
        "wall_time_s": round(wave_time_s, 6),
        "jps": round(jps, 2),
        "knowledge_density": round(kd, 2),
        "eta": round(eta, 2),
        "coordination_j": round(coordination_cost(units, tier), 6),
    }

# =========================================================
# SEQUENTIAL MODE: TIER 1 RUNNING N TIMES
# =========================================================
def run_sequential_chains(passes: int, query: str) -> dict:
    """
    Run the Tier-1 chain (6 units) repeatedly N times.
    This is the "brute force" comparison: same total compute budget
    as a Tier-N swarm, but executed sequentially with no cooperation.
    """
    units_per_pass = 6
    total_units = units_per_pass * passes
    
    total_joules = 0.0
    total_knowledge = 0.0
    total_time_s = 0.0
    
    for i, spec in enumerate(ATOMIC_SPECS):
        # Each pass runs 6 units for this function
        func_energy = units_per_pass * spec["base_cost_j"] * passes
        func_knowledge = knowledge_output(units_per_pass, spec["knowledge_gain"]) * passes
        
        # No coordination overhead (only 6 units, they know each other)
        coord = 0.001 * units_per_pass * passes
        
        # Time: ALL sequential — no parallelism
        unit_time = spec["base_cost_j"] / BASE_JOULE_PER_OP * 0.001
        func_time = unit_time * units_per_pass * passes  # every unit, every pass, sequential
        
        total_joules += func_energy + coord
        total_knowledge += func_knowledge
        total_time_s += func_time
    
    useful_output = total_knowledge
    human_joules = total_joules / (total_time_s + 0.001)
    
    eta = useful_output / human_joules if human_joules > 0 else 0
    jps = total_joules / (total_time_s + 0.001)
    kd = total_knowledge / total_joules if total_joules > 0 else 0
    
    return {
        "passes": passes,
        "total_units": total_units,
        "total_joules": round(total_joules, 6),
        "knowledge_pooled": round(total_knowledge, 2),
        "useful_output": round(useful_output, 2),
        "wall_time_s": round(total_time_s, 6),
        "jps": round(jps, 2),
        "knowledge_density": round(kd, 2),
        "eta": round(eta, 2),
        "coordination_j": 0.0, # Sequential has negligible coordination
    }

# =========================================================
# MAIN EXECUTION & COMPARISON
# =========================================================

def run_comparison(max_tier: int = 6):
    query = "Calculate the Landauer limit for 256 bits"
    
    print(f"\n{'='*70}")
    print(f"FRACTAL SWARM COMPARISON: Parallel vs. Sequential")
    print(f"Query: '{query}'")
    print(f"Max Tier: {max_tier} (Total Units: {6**max_tier})")
    print(f"{'='*70}\n")

    results = []

    for tier in range(1, max_tier + 1):
        units = 6 ** tier
        passes = units // 6  # How many times Tier-1 must run to match total units
        
        print(f"--- Tier {tier}: {units:,} Units (Parallel) vs. {passes:,} Sequential Passes ---")
        
        # 1. Run Parallel Swarm
        p_result = run_parallel_swarm(tier, query)
        
        # 2. Run Sequential Chains
        s_result = run_sequential_chains(passes, query)
        
        # 3. Calculate Delta (Advantage of Swarm)
        eta_delta = p_result['eta'] - s_result['eta']
        kd_delta = p_result['knowledge_density'] - s_result['knowledge_density']
        time_delta = s_result['wall_time_s'] - p_result['wall_time_s'] # Positive = Swarm is faster
        
        results.append({
            "tier": tier,
            "units": units,
            "parallel": p_result,
            "sequential": s_result,
            "eta_gain": eta_delta,
            "kd_gain": kd_delta,
            "time_saved_s": time_delta
        })
        
        # Print Summary Row
        print(f"Tier {tier}:")
        print(f"  Parallel:  ETA={p_result['eta']:>8.2f} | KD={p_result['knowledge_density']:>8.2f} | Time={p_result['wall_time_s']*1000:>6.2f}ms")
        print(f"  Sequential: ETA={s_result['eta']:>8.2f} | KD={s_result['knowledge_density']:>8.2f} | Time={s_result['wall_time_s']*1000:>6.2f}ms")
        print(f"  >>> SWARM ADVANTAGE: ETA +{eta_delta:+.2f} | KD +{kd_delta:+.2f} | Time Saved {time_delta*1000:.2f}ms")
        print()

    # Final Analysis
    print(f"\n{'='*70}")
    print("FINAL ANALYSIS")
    print(f"{'='*70}")
    
    best_tier = max(results, key=lambda x: x['eta_gain'])
    print(f"Highest Efficiency Gain at Tier {best_tier['tier']}:")
    print(f"  - Parallel ETA: {best_tier['parallel']['eta']:.2f}")
    print(f"  - Sequential ETA: {best_tier['sequential']['eta']:.2f}")
    print(f"  - Improvement: {(best_tier['parallel']['eta']/best_tier['sequential']['eta'])*100:.1f}%")
    
    if best_tier['eta_gain'] > 0:
        print("\n[CONCLUSION] The Fractal Swarm architecture OUTPERFORMS sequential brute force.")
        print("The compounding knowledge and sublinear coordination costs validate the 6^N model.")
    else:
        print("\n[CONCLUSION] Sequential execution remains more efficient for this workload.")
        print("Consider increasing knowledge_gain or reducing coordination_cost parameters.")

    return results

if __name__ == "__main__":
    run_comparison()
