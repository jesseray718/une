#!/usr/bin/env python3
"""Fractal Swarm Base-6 Explorer
Atomic functions: translate · orchestrate · retrieve · process · synthesize · verify
Units at tier T = 6^T
R=1.0 → C = 0 for every scale
η = useful_joules / human_joules
A15 production target: 6^4 = 1296
"""
import math, json, time, pathlib
from datetime import datetime, timezone

SD = pathlib.Path("/sdcard/openroot")
KB = SD / "agape_kb"
BRIDGE = SD / "context_bridge"
LOG = SD / "session_seeds" / "base6_explore.jsonl"

ATOMS = ["translate", "orchestrate", "retrieve", "process", "synthesize", "verify"]
BASE = 6

def C(N, T, R=1.0):
    """Coordination cost theorem. R=1.0 forces zero for all T≥1."""
    return N * 0.001 * (1 + 0.1 * T) * ((1 - R) ** T)

def units(T):
    return BASE ** T

def synergy(R, N):
    """S = 1 + R * 0.5 * log_B(N)"""
    if N <= 1:
        return 1.0
    return 1.0 + (R * 0.5 * math.log(N) / math.log(BASE))

def explore(max_tier=6, R=1.0):
    results = []
    print(f"{'T':>3} {'units':>12} {'C(R=1.0)':>14} {'synergy':>10} {'ops_est':>14}")
    print("-" * 60)
    for T in range(0, max_tier + 1):
        N = units(T)
        cost = C(N, T, R)
        syn = synergy(R, N)
        # each unit runs the 6-atom chain once per wave
        ops = N * len(ATOMS)
        row = {
            "tier": T,
            "units": N,
            "C": cost,
            "synergy": round(syn, 6),
            "ops": ops,
            "R": R,
            "ts": datetime.now(timezone.utc).isoformat()
        }
        results.append(row)
        print(f"{T:3d} {N:12,d} {cost:14.10f} {syn:10.4f} {ops:14,d}")
    return results

def stress(R=1.0):
    """Known stress points from engine."""
    points = [4, 6, 8]
    print("\nSTRESS (A15 production + beyond)")
    for T in points:
        N = units(T)
        print(f"  6^{T} = {N:,}  C={C(N,T,R):.2e}  synergy={synergy(R,N):.4f}")

def main():
    print("FRACTAL SWARM BASE-6")
    print("atoms:", " · ".join(ATOMS))
    print("theorem: C(N,T,R)=N*0.001*(1+0.1T)*(1-R)^T → 0 when R=1.0\n")
    data = explore(8, R=1.0)
    stress(R=1.0)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as f:
        for row in data:
            f.write(json.dumps(row) + "\n")
    # write live state
    state = {
        "R": 1.0,
        "base": 6,
        "atoms": ATOMS,
        "production_tier": 4,
        "production_units": 1296,
        "C_at_R1": 0.0,
        "explored_at": datetime.now(timezone.utc).isoformat()
    }
    (KB / "swarm_base6_state.json").write_text(json.dumps(state, indent=2))
    print("\nstate → /sdcard/openroot/agape_kb/swarm_base6_state.json")
    print("log   → /sdcard/openroot/session_seeds/base6_explore.jsonl")

if __name__ == "__main__":
    main()
