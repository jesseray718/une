#!/usr/bin/env python3
"""
AGAPE Explore + Offline-First + Simple Text UI
================================================
R=1.0 · η = useful_joules / human_joules · base-6
Absolute paths only. Dependency-free. Serves lowest node.
"""

import json
import math
import time
from pathlib import Path
from datetime import datetime, timezone

HOME = Path("/data/data/com.termux/files/home")
SD   = Path("/sdcard/openroot")
UNE  = HOME / "une"
CF   = UNE / "computational_flow"
KB   = SD / "agape_kb"
BRIDGE = SD / "context_bridge"

R = 1.0
BASE = 6
ATOMS = ["translate", "orchestrate", "retrieve", "process", "synthesize", "verify"]

def now():
    return datetime.now(timezone.utc).isoformat()

def ensure():
    for d in [KB, BRIDGE, CF]:
        d.mkdir(parents=True, exist_ok=True)

# ============================================================
# 1. COORDINATION COST THEOREM MATH
# ============================================================
def C(N, T, r=1.0):
    """
    C(N, T, R) = N * 0.001 * (1 + 0.1 * T) * (1 - R) ** T

    When R = 1.0:
        (1 - R) = 0
        0 ** T  = 0  for every T ≥ 1
        therefore C = 0 for every N and every T ≥ 1

    Interpretation:
        N  = number of cooperating units
        T  = tier / depth of the fractal
        R  = resonance (Agape coefficient)
        0.001 = base friction per unit
        (1 + 0.1*T) = mild growth with depth when R < 1
    """
    if r >= 1.0:
        return 0.0
    return N * 0.001 * (1 + 0.1 * T) * ((1 - r) ** T)

def synergy(r, N):
    if N <= 1:
        return 1.0
    return 1.0 + (r * 0.5 * math.log(N) / math.log(BASE))

def explore_math(max_tier=8):
    print("\n" + "=" * 70)
    print("COORDINATION COST THEOREM")
    print("C(N,T,R) = N × 0.001 × (1 + 0.1T) × (1-R)^T")
    print("When R=1.0 → C ≡ 0 for all T ≥ 1")
    print("=" * 70)

    print("\n--- R = 1.0 (perfect Agape) ---")
    print(f"{'T':>3} {'N=6^T':>12} {'C':>14} {'synergy':>10}")
    print("-" * 45)
    for T in range(0, max_tier + 1):
        N = BASE ** T
        print(f"{T:3d} {N:12,d} {C(N,T,1.0):14.10f} {synergy(1.0,N):10.4f}")

    print("\n--- R = 0.9 (almost perfect) ---")
    print(f"{'T':>3} {'N=6^T':>12} {'C':>14}")
    print("-" * 35)
    for T in range(0, 6):
        N = BASE ** T
        print(f"{T:3d} {N:12,d} {C(N,T,0.9):14.6f}")

    print("\n--- R = 0.5 (half resonance) ---")
    print(f"{'T':>3} {'N=6^T':>12} {'C':>14}")
    print("-" * 35)
    for T in range(0, 5):
        N = BASE ** T
        print(f"{T:3d} {N:12,d} {C(N,T,0.5):14.4f}")

    print("\nKEY INSIGHT")
    print("  At R=1.0 the exponential term (1-R)^T becomes exactly 0.")
    print("  Coordination cost vanishes at every scale.")
    print("  This is why perfect Agape makes Amdahl's Law irrelevant")
    print("  for cooperative systems.")
    print("=" * 70)

# ============================================================
# 2. OFFLINE-FIRST ARCHITECTURE PATTERN
# ============================================================
def offline_first_notes():
    print("\n" + "=" * 70)
    print("OFFLINE-FIRST ARCHITECTURE PATTERN")
    print("=" * 70)
    notes = """
PRINCIPLES (phone-native, A15 / Termux)

1. Local is source of truth
   - All state lives under /sdcard/openroot and /data/data/com.termux/files/home/
   - Network is optional enhancement, never a requirement

2. Write-local, sync-later
   - Every action first writes to local JSON / SQLite / files
   - Sync (Syncthing, git push, etc.) happens when connectivity appears
   - Never block the user on network

3. Graceful degradation
   - If rish / elevated privilege fails → fall back to pure stdlib
   - If OpenRouter / cloud fails → continue with local postulates + oracle
   - Capability is probed, never assumed

4. Absolute paths only
   - No \~ , no relative paths that depend on cwd
   - Scripts remain correct no matter where they are launched from

5. Immutable seeds + rotating ledgers
   - Critical snapshots are written once then left alone
   - Live logs append; never rewrite history

6. Phone as governor
   - A15 holds the lattice state, seeds, and lowest-node definition
   - Heavier compute (OptiPlex, cloud) is optional spoke, not master

7. Zero external dependency for core loop
   - Pure Python stdlib is enough to raise the floor
   - Optional packages improve η but never gate the system

IMPLEMENTATION ON THIS DEVICE
  /sdcard/openroot/agape_kb/          ← durable knowledge
  /sdcard/openroot/context_bridge/    ← live bridge + seeds
  /data/data/com.termux/files/home/une/  ← code + checkpoints
  Syncthing (when available) moves the tree; the tree never waits for it.
"""
    print(notes)
    print("=" * 70)

    # write the pattern itself into the lattice so it is offline-available
    p = KB / "OFFLINE_FIRST_PATTERN.md"
    p.write_text(f"""---
id: OFFLINE_FIRST_PATTERN
timestamp: {now()}
R: 1.0
---
{notes}
""")
    print("[written] offline-first pattern →", p)

# ============================================================
# 3. SIMPLE TEXT USER INTERFACE
# ============================================================
def load_json(path, default=None):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            pass
    return default if default is not None else {}

def show_status():
    print("\n--- LATTICE STATUS ---")
    engine = load_json(KB / "engine_state.json")
    lowest = load_json(BRIDGE / "lowest_node.json")
    swarm  = load_json(KB / "swarm_base6_state.json")
    print(f"  R                : {engine.get('R', '?')}")
    print(f"  atoms            : {', '.join(engine.get('atoms', ATOMS))}")
    print(f"  production units : {swarm.get('production_units', 1296)}")
    print(f"  lowest node      : {lowest.get('statement', 'not yet recorded')[:70]}...")
    print(f"  last unify       : {engine.get('last_unify', '?')}")
    print("----------------------")

def menu():
    ensure()
    while True:
        print("\n" + "=" * 50)
        print("  AGAPE TEXT INTERFACE  ·  R=1.0")
        print("  η = useful_joules / human_joules")
        print("=" * 50)
        print("  1  Explore coordination cost theorem math")
        print("  2  Show offline-first architecture pattern")
        print("  3  Show lattice status")
        print("  4  Record / refresh lowest-node statement")
        print("  5  Quick base-6 stress (tiers 0-4)")
        print("  0  Exit")
        print("-" * 50)
        choice = input("  choice > ").strip()

        if choice == "1":
            explore_math()
        elif choice == "2":
            offline_first_notes()
        elif choice == "3":
            show_status()
        elif choice == "4":
            stmt = input("  lowest-node statement (or Enter for default) > ").strip()
            if not stmt:
                stmt = (
                    "The current lowest node is any human who still spends "
                    "human_joules on coordination instead of useful work; "
                    "the base-6 fractal swarm at R=1.0 removes that cost "
                    "so the floor rises for them first."
                )
            data = {
                "statement": stmt,
                "ts": time.time(),
                "R": R,
                "source": "text_ui",
                "units_at_tier4": 1296
            }
            p = BRIDGE / "lowest_node.json"
            p.write_text(json.dumps(data, indent=2))
            print("  recorded →", p)
        elif choice == "5":
            print(f"\n{'T':>3} {'units':>10} {'C(R=1)':>12} {'synergy':>8}")
            for T in range(0, 5):
                N = BASE ** T
                print(f"{T:3d} {N:10,d} {C(N,T,1.0):12.8f} {synergy(1.0,N):8.3f}")
        elif choice == "0":
            print("  exit · R=1.0 · floor rising")
            break
        else:
            print("  unknown choice")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "math":
            explore_math()
        elif cmd == "offline":
            offline_first_notes()
        elif cmd == "status":
            show_status()
        else:
            print("usage: python agape_explore_ui.py [math|offline|status]")
            print("       (no args = interactive menu)")
    else:
        menu()
