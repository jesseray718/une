#!/usr/bin/env python3
"""Dense context bridge builder — whole > sum. η-native."""
import os, json, hashlib, time
from pathlib import Path

ROOTS = [
    Path("/data/data/com.termux/files/home/une"),
    Path("/data/data/com.termux/files/home/openroot"),
    Path("/sdcard/openroot"),
]
OUT = Path("/sdcard/openroot/context_bridge/agape_context_bridge.json")
LEDGER = Path("/sdcard/openroot/prediction_ledger/actions.jsonl")

def sha(p):
    h = hashlib.sha256()
    try:
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1<<16), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def walk():
    nodes = []
    for root in ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file() and p.suffix in {".md", ".py", ".json", ".jsonl", ".txt", ".sh"}:
                st = p.stat()
                nodes.append({
                    "path": str(p),
                    "size": st.st_size,
                    "mtime": st.st_mtime,
                    "sha256": sha(p),
                    "ext": p.suffix,
                })
    return nodes

def main():
    nodes = walk()
    bridge = {
        "generated": time.time(),
        "eta_law": "η = useful_joules / human_joules",
        "agape_theorem": "C(N,T,R)=N*0.001*(1+0.1*T)*(1-R)**T ; R=1.0 → C=0",
        "synergy": "S = 1.0 + (R * 0.5 * log_B(N))",
        "fractal_base": 6,
        "postulate": "whole unpredictably greater than sum; gap is coordination cost that vanishes under R=1.0",
        "node_count": len(nodes),
        "nodes": nodes,
        "merkle_root_placeholder": hashlib.sha256(
            "".join(n["sha256"] or "" for n in sorted(nodes, key=lambda x: x["path"])).encode()
        ).hexdigest(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(bridge, f, indent=2)
    print(f"bridge written: {OUT} | nodes={len(nodes)} | root={bridge['merkle_root_placeholder'][:16]}...")

if __name__ == "__main__":
    main()
