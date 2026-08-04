#!/data/data/com.termux/files/usr/bin/env python3
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/une/computational_flow")
from agape_engine import AgapeSwarm, AgapeEngine

def test_zero_cost():
    s = AgapeSwarm(base=6, depth=8, resonance=1.0)
    for t in range(1, 9):
        N = s.nodes(t)
        assert s.C(N, t, 1.0) == 0.0, f"tier {t} failed"

def test_cost_decreases():
    s = AgapeSwarm(base=6, depth=4)
    N = s.nodes(4)
    assert s.C(N, 4, 0.0) > s.C(N, 4, 0.5) > s.C(N, 4, 0.9)

def test_synergy_grows():
    s = AgapeSwarm(base=6)
    N = s.nodes(4)
    assert s.synergy(N, 1.0) > s.synergy(N, 0.0)

def test_engine_process():
    eng = AgapeEngine(resonance=1.0)
    r = eng.process("design from patterns integrate renewable")
    assert r["coordination_J"] == 0.0
    assert "synergy_mult" in r
    assert r["η"] == float("inf") or r["η"] > 1e12

if __name__ == "__main__":
    test_zero_cost()
    test_cost_decreases()
    test_synergy_grows()
    test_engine_process()
    print("ALL TESTS PASSED — R=1.0 → C=0.00000000 J confirmed")
