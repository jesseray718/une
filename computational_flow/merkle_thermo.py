#!/data/data/com.termux/files/usr/bin/python3
"""
import os
try:
    from paths import OPENROOT
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

merkle_thermo.py — Merkle tree + thermodynamic accounting
Pure Python 3. Zero dependencies.
Leaves can carry joules / E=mc² equivalents.
"""

import json
import hashlib
import time
from pathlib import Path

BASE = Path(os.path.join(OPENROOT, "context_bridge"))
TREE_LOG = BASE / "merkle_tree.jsonl"
C = 299_792_458          # m/s
C2 = C * C

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def leaf_hash(entry: dict) -> str:
    """Hash a single ledger / dividend / response entry."""
    raw = json.dumps(entry, sort_keys=True, ensure_ascii=False).encode()
    return sha256(raw)

def build_merkle(leaves: list[str]) -> list[list[str]]:
    """Build full Merkle tree from list of leaf hashes. Returns levels."""
    if not leaves:
        return []
    levels = [leaves]
    while len(levels[-1]) > 1:
        current = levels[-1]
        next_level = []
        for i in range(0, len(current), 2):
            left = current[i]
            right = current[i+1] if i+1 < len(current) else left
            combined = sha256((left + right).encode())
            next_level.append(combined)
        levels.append(next_level)
    return levels

def root_from_leaves(leaves: list[str]) -> str:
    tree = build_merkle(leaves)
    return tree[-1][0] if tree else ""

def joules_to_mass_kg(joules: float) -> float:
    """E = mc² → m = E / c²"""
    return joules / C2

def append_leaf(entry: dict, joules: float = 0.0):
    """Add a new leaf with optional thermodynamic data and update the tree log."""
    entry = dict(entry)  # copy
    entry["leaf_hash"] = leaf_hash(entry)
    entry["joules"] = joules
    entry["mass_kg_equivalent"] = joules_to_mass_kg(joules)
    entry["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")

    # Load existing leaves
    leaves = []
    if TREE_LOG.exists():
        with open(TREE_LOG) as f:
            for line in f:
                try:
                    leaves.append(json.loads(line)["leaf_hash"])
                except:
                    pass

    leaves.append(entry["leaf_hash"])
    root = root_from_leaves(leaves)

    entry["merkle_root"] = root
    entry["leaf_index"] = len(leaves) - 1

    with open(TREE_LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Leaf {entry['leaf_index']} added")
    print(f"Hash     : {entry['leaf_hash']}")
    print(f"Root     : {root}")
    print(f"Joules   : {joules}")
    print(f"Mass eq  : {entry['mass_kg_equivalent']:.3e} kg")
    return entry

def current_root() -> str:
    if not TREE_LOG.exists():
        return ""
    leaves = []
    with open(TREE_LOG) as f:
        for line in f:
            try:
                leaves.append(json.loads(line)["leaf_hash"])
            except:
                pass
    return root_from_leaves(leaves)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "root":
        print("Current Merkle root:", current_root())
    else:
        print("Usage:")
        print("  from merkle_thermo import append_leaf, current_root")
        print("  append_leaf({\"type\": \"measurement\", \"note\": \"...\"}, joules=184000)")
        print("  python3 merkle_thermo.py root")
