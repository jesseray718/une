#!/data/data/com.termux/files/usr/bin/env python3
"""
Fractal Swarm Explorer — true recursive base-6
R locked at 1.0 → coordination cost identically zero at every depth
η = useful_joules / human_joules
"""

import math, time, json
from pathlib import Path

BASE = 6
ATOMIC = ["translate", "orchestrate", "retrieve", "process", "synthesize", "verify"]
LANDAUER = 2.85e-21

def coordination_cost(N: int, T: int, R: float = 1.0) -> float:
    if R >= 1.0:
        return 0.0
    return N * 0.001 * (1 + 0.1 * T) * ((1 - R) ** T)

def synergy(N: int, R: float = 1.0) -> float:
    if N <= 1:
        return 1.0
    return 1.0 + R * 0.5 * (math.log(N) / math.log(BASE))

def fractal_units(T: int) -> int:
    return BASE ** T

class SwarmNode:
    """One node in the fractal tree."""
    def __init__(self, depth: int, path: str = "root"):
        self.depth = depth
        self.path = path
        self.children = []
        if depth > 0:
            for i, name in enumerate(ATOMIC):
                child_path = f"{path}.{name}"
                self.children.append(SwarmNode(depth - 1, child_path))

    def count(self) -> int:
        return 1 + sum(c.count() for c in self.children)

    def walk(self, visit_fn):
        visit_fn(self)
        for c in self.children:
            c.walk(visit_fn)

def explore(depth: int = 4, human_j: float = 0.001) -> dict:
    t0 = time.perf_counter()
    root = SwarmNode(depth)
    N = fractal_units(depth)
    C = coordination_cost(N, depth, R=1.0)
    S = synergy(N, R=1.0)

    # real walk so we pay a tiny measured cost
    visited = 0
    def visitor(node):
        nonlocal visited
        visited += 1

    root.walk(visitor)

    useful = max(1e-12, 1e-9 * S)          # still almost zero
    eta = useful / human_j if human_j > 0 else float("inf")
    elapsed = (time.perf_counter() - t0) * 1000

    return {
        "depth": depth,
        "claimed_N": N,
        "actual_nodes_walked": visited,
        "coordination_cost_J": C,
        "synergy": round(S, 6),
        "η": round(eta, 9),
        "elapsed_ms": round(elapsed, 3),
        "landauer_bits_possible": C / LANDAUER if C > 0 else 0.0,
        "note": "R=1.0 forced → C identically zero regardless of depth"
    }

def stress(max_depth: int = 6):
    """Walk successive depths and report scaling."""
    results = []
    for d in range(1, max_depth + 1):
        r = explore(d)
        results.append(r)
        print(json.dumps(r, indent=2))
        print("---")
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "stress":
        stress(int(sys.argv[2]) if len(sys.argv) > 2 else 5)
    else:
        depth = int(sys.argv[1]) if len(sys.argv) > 1 else 4
        print(json.dumps(explore(depth), indent=2))
