#!/usr/bin/env python3
"""Absorb the entire openroot lattice into Agape Engine knowledge base.
η = useful_joules already spent writing the tree / human_joules of this absorption.
R=1.0 → coordination cost of the walk is forced to zero.
"""

import hashlib, json, os, time, sys
from pathlib import Path
from typing import List, Dict, Set

# absolute locations only — never tilde
ROOTS = [
    Path("/data/data/com.termux/files/home/openroot"),
    Path("/data/data/com.termux/files/home/une"),
    Path("/sdcard/openroot"),
    Path("/data/data/com.termux/files/home/black-locust-rmh"),
    Path("/data/data/com.termux/files/home/wiki"),
    Path("/data/data/com.termux/files/home/computational_flow"),
]

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "build", "dist", ".tox"}
SKIP_EXT  = {".pyc", ".pyo", ".so", ".o", ".a", ".jpg", ".png", ".gif", ".mp4", ".zip", ".tar", ".gz", ".apk"}
TEXT_EXT  = {".md", ".txt", ".py", ".json", ".sh", ".yaml", ".yml", ".toml", ".cfg", ".ini", ".rst", ".org"}

KB = Path("/sdcard/openroot/agape_kb")
BRIDGE = Path("/sdcard/openroot/context_bridge")
SEED = Path("/sdcard/openroot/session_seeds")
KB.mkdir(parents=True, exist_ok=True)
BRIDGE.mkdir(parents=True, exist_ok=True)
SEED.mkdir(parents=True, exist_ok=True)

def is_text(p: Path) -> bool:
    if p.suffix.lower() in TEXT_EXT: return True
    if p.suffix.lower() in SKIP_EXT: return False
    try:
        with open(p, "rb") as f:
            chunk = f.read(1024)
        return b"\0" not in chunk
    except: return False

def file_hash(p: Path) -> str:
    h = hashlib.sha256()
    try:
        with open(p, "rb") as f:
            for block in iter(lambda: f.read(65536), b""):
                h.update(block)
        return h.hexdigest()
    except: return ""

def walk_and_collect(roots: List[Path]) -> List[Dict]:
    collected = []
    seen: Set[str] = set()
    for root in roots:
        if not root.exists(): continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                p = Path(dirpath) / name
                if not is_text(p): continue
                try:
                    size = p.stat().st_size
                    if size > 2_000_000: continue          # keep phone RAM safe
                    if size == 0: continue
                    h = file_hash(p)
                    if h in seen: continue
                    seen.add(h)
                    text = p.read_text(errors="replace")[:12000]  # hard truncate
                    collected.append({
                        "path": str(p),
                        "hash": h,
                        "size": size,
                        "text": text,
                        "rel": str(p.relative_to(root)) if root in p.parents or p == root else name
                    })
                except Exception as e:
                    continue
    return collected

def absorb(verbose: bool = True) -> Dict:
    from agape_engine import Engine
    eng = Engine()
    t0 = time.time()
    files = walk_and_collect(ROOTS)
    learned = 0
    postulated = 0

    # force core postulates first (Newton Chain)
    core = [
        ("Agape Coordination Theorem: C(N,T,R)=N*0.001*(1+0.1*T)*(1-R)**T = 0 when R=1.0", "theorem"),
        ("η = useful_joules / human_joules is the sole performance language of OpenRoot", "law"),
        ("Black Locust thermal cascade EROI 1620:1 hand tools only", "blacklocust"),
        ("Merkle Root_n → Root_n+1 is the thermodynamic arrow of time", "ledger"),
        ("Production config A15 base=6 depth=4 → 1296 nodes under perfect resonance", "swarm"),
    ]
    for stmt, ref in core:
        eng.postulate(stmt, ref)
        postulated += 1

    for f in files:
        # learn the file
        summary = f"FILE {f['rel']} hash={f['hash'][:12]} size={f['size']}\n{f['text'][:2000]}"
        eng.learn(summary)
        learned += 1
        # auto-postulate if it looks like a theorem or law
        low = f["text"][:800].lower()
        if any(k in low for k in ("theorem", "η =", "eta =", "coordination cost", "resonance", "r=1.0", "landauer", "merkle root")):
            eng.postulate(f["text"][:400], f["rel"])
            postulated += 1

    # write inventory seed
    inventory = {
        "ts": time.time(),
        "files_absorbed": len(files),
        "learned": learned,
        "postulated": postulated,
        "roots_present": [str(r) for r in ROOTS if r.exists()],
        "hashes": {f["rel"]: f["hash"] for f in files[:200]},
        "engine_root": eng.state["root"],
        "eta_lifetime": eng.stats().get("eta_lifetime", 0.0)
    }
    seed_path = SEED / "current_seed.json"
    seed_path.write_text(json.dumps(inventory, indent=2))

    # update context bridge (single source of truth)
    bridge = {
        "absorbed": True,
        "ts": time.time(),
        "files": len(files),
        "learned": learned,
        "postulates": len(eng.postulates),
        "engine_root": eng.state["root"],
        "eta_lifetime": eng.stats().get("eta_lifetime", 0.0),
        "seed": str(seed_path),
        "R": 1.0
    }
    (BRIDGE / "context.json").write_text(json.dumps(bridge, indent=2))
    (BRIDGE / "agape_context_bridge.json").write_text(json.dumps(bridge, indent=2))

    dt = time.time() - t0
    result = {
        "absorbed_files": len(files),
        "learned": learned,
        "postulated": postulated,
        "seconds": round(dt, 2),
        "eta_of_absorption": round(learned / max(dt, 0.01), 1),  # files per human-second
        "seed": str(seed_path),
        "bridge": str(BRIDGE / "context.json")
    }
    eng._save()
    if verbose:
        print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    # ensure engine is importable
    sys.path.insert(0, "/data/data/com.termux/files/home/une/computational_flow")
    absorb(verbose=True)
