#!/data/data/com.termux/files/usr/bin/env python3
"""
MERKLE JOULE ROOT — Civilization 2.0 Foundation
η = useful_joules / human_joules
Every irreversible bit costs ≥ kT ln(2). Every bit has mass via E=mc².
ACRE claims are minted only from measured useful joules.
"""

import hashlib
import json
import os
import time
from pathlib import Path

kB = 1.380649e-23          # J/K
T  = 300.0                 # K (room)
LANDAUER = kB * T * 0.693147  # ≈ 2.870e-21 J/bit
c2 = 8.9875517923e16       # c² (m²/s²)
MASS_PER_BIT = LANDAUER / c2  # kg

LEDGER = Path("/sdcard/openroot/joule_ledger/root.jsonl")
POSTULATES = Path("/sdcard/openroot/agape_kb/postulates.json")
STATE = Path("/sdcard/openroot/joule_ledger/state.json")

def landauer_cost(bits: int) -> float:
    return bits * LANDAUER

def mass_of_information(bits: int) -> float:
    return bits * MASS_PER_BIT

def merkle_leaf(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def merkle_parent(left: str, right: str) -> str:
    return hashlib.sha256((left + right).encode()).hexdigest()

def append_claim(useful_j: float, human_j: float, source: str, meta: dict = None):
    """Only measured useful joules may mint. Human joules are the denominator of η."""
    eta = useful_j / (human_j + 1e-30)
    bits_erased = int(useful_j / LANDAUER) if useful_j > 0 else 0
    claim = {
        "ts": time.time(),
        "useful_j": useful_j,
        "human_j": human_j,
        "eta": eta,
        "landauer_bits": bits_erased,
        "mass_kg": mass_of_information(bits_erased),
        "source": source,
        "meta": meta or {},
        "leaf": None
    }
    claim["leaf"] = merkle_leaf(json.dumps(claim, sort_keys=True))
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER, "a") as f:
        f.write(json.dumps(claim) + "\n")
    return claim

def current_root() -> str:
    if not LEDGER.exists():
        return "0" * 64
    leaves = []
    with open(LEDGER) as f:
        for line in f:
            leaves.append(json.loads(line)["leaf"])
    if not leaves:
        return "0" * 64
    # Simple binary Merkle reduction
    while len(leaves) > 1:
        next_level = []
        for i in range(0, len(leaves), 2):
            left = leaves[i]
            right = leaves[i+1] if i+1 < len(leaves) else left
            next_level.append(merkle_parent(left, right))
        leaves = next_level
    return leaves[0]

def acre_mint(useful_j: float, human_j: float, physical_work: str):
    """Mint ACRE claim only from measured useful work."""
    claim = append_claim(useful_j, human_j, "ACRE", {"physical_work": physical_work})
    root = current_root()
    return {
        "claim_id": claim["leaf"][:16],
        "merkle_root": root,
        "eta": claim["eta"],
        "mass_kg": claim["mass_kg"],
        "status": "minted"
    }

def status():
    root = current_root()
    total_useful = total_human = 0.0
    n = 0
    if LEDGER.exists():
        with open(LEDGER) as f:
            for line in f:
                c = json.loads(line)
                total_useful += c["useful_j"]
                total_human += c["human_j"]
                n += 1
    eta = total_useful / (total_human + 1e-30)
    return {
        "merkle_root": root,
        "claims": n,
        "total_useful_j": total_useful,
        "total_human_j": total_human,
        "system_eta": eta,
        "landauer_j_per_bit": LANDAUER,
        "mass_per_bit_kg": MASS_PER_BIT
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        print(json.dumps(status(), indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "mint":
        # example: python3 merkle_joule_root.py mint 420000 1800 "black_locust_coppice_0.4ha"
        u = float(sys.argv[2])
        h = float(sys.argv[3])
        work = sys.argv[4] if len(sys.argv) > 4 else "manual"
        print(json.dumps(acre_mint(u, h, work), indent=2))
    else:
        print("Usage:")
        print("  python3 merkle_joule_root.py status")
        print("  python3 merkle_joule_root.py mint <useful_j> <human_j> <physical_work>")
