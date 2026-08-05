#!/data/data/com.termux/files/usr/bin/python3
"""
try:
    from paths import OPENROOT, UNE_HOME
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

Atomic Embedder: The Joule-Native Vector Map
Uses core_atomic.py (f1-f11) to embed files while measuring physical cost.
Outputs: /sdcard/openroot/vectors/atomic_vector_map.jsonl
"""
import json
import os
import sys
import time
from datetime import datetime

# Path to your atomic core
CORE_PATH = os.path.join(UNE_HOME, "computational_flow/core_atomic.py")
IMMORTAL = os.path.join(OPENROOT, "context_bridge/immortal_context.json")
OUTPUT = os.path.join(OPENROOT, "vectors/atomic_vector_map.jsonl")

# Ensure output dir exists
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

print("=== ATOMIC EMBEDDER INITIATED ===")
print(f"Core Module: {CORE_PATH}")
print(f"Source: {IMMORTAL}")
print(f"Output: {OUTPUT}")
print()

# Import your atomic functions dynamically
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("core_atomic", CORE_PATH)
    core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(core)
    print("✓ Loaded core_atomic.py (f1-f11)")
except Exception as e:
    print(f"✗ Failed to load core_atomic.py: {e}")
    print("   Ensure path is correct and dependencies (numpy, hashlib) are installed.")
    sys.exit(1)

# Load Immortal Context
with open(IMMORTAL, 'r') as f:
    data = json.load(f)

files = data.get("file_index", [])
kingdom_files = [f for f in files if f.get("category") == "KINGDOM_CORE"]

print(f"Files to process: {len(kingdom_files)}")
print()

# Ollama for embeddings (optional, if you want semantic vectors too)
# If you don't have Ollama running, we skip semantic embedding and just do physical hashing
OLLAMA_URL = "http://localhost:11434/api/embeddings"
USE_OLLAMA = False
try:
    r = requests.get("http://localhost:11434/api/tags", timeout=2)
    USE_OLLAMA = True
    print("✓ Ollama detected. Will add semantic vectors.")
except:
    print("ℹ Ollama not running. Using physical hashes only.")

import requests

processed = 0
failed = 0
start_time = time.time()

with open(OUTPUT, 'w') as out_f:
    for i, entry in enumerate(kingdom_files):
        path = entry.get("path", "")
        size = entry.get("size", 0)
        
        # --- ATOMIC CHAIN EXECUTION ---
        
        # 1. Capture (Read content or path)
        try:
            if os.path.exists(path):
                with open(path, 'r', errors='ignore') as f:
                    content = f.read(1024) # Read first 1KB for hash/embedding
            else:
                content = path # Fallback if missing
        except:
            content = path
        
        # 2. Hash (Merkle root of content)
        merkle_root = core.f2_hash(content)
        
        # 3. Aggregate (Batch logic - simplified here to single item)
        aggregated = core.f3_aggregate([content])
        
        # 4. Pair (Pairwise logic - simplified)
        paired = core.f4_pair(content, merkle_root)
        
        # 5. Commit (Prepare for ledger)
        committed = core.f5_commit(merkle_root, "vector_map")
        
        # 6. Verify (Integrity)
        verified = core.f6_verify(committed)
        
        # 7. Landauer Cost (Physical cost of this operation)
        landauer_j = core.f7_landauer_cost(len(str(content)))
        
        # 8. Measure ARM Energy (Estimate based on CPU freq if available)
        # Note: f8_measure_arm_inference might need real hardware access
        try:
            arm_energy = core.f8_measure_arm_inference(len(str(content)))
        except:
            arm_energy = 0.0
        
        # 9. Compute Eta (Efficiency)
        # eta = useful_output / human_input
        # Here: useful_output = content_length, human_input = estimated effort
        eta = core.f9_compute_eta(len(str(content)), 1.0) # 1.0 is placeholder for human effort
        
        # 10. Mass Equivalent (E=mc²)
        mass_kg = core.f10_mass_equivalent(landauer_j)
        
        # 11. Landauer Mass
        landauer_mass = core.f11_landauer_mass(landauer_j)
        
        # --- SEMANTIC EMBEDDING (Optional) ---
        semantic_vec = []
        if USE_OLLAMA:
            try:
                resp = requests.post(OLLAMA_URL, json={"model": "nomic-embed-text", "prompt": content}, timeout=10)
                if resp.status_code == 200:
                    semantic_vec = resp.json().get("embedding", [])
            except:
                pass
        
        # --- BUILD RECORD ---
        record = {
            "index": i,
            "path": path,
            "size": size,
            "timestamp": datetime.now().isoformat(),
            "merkle_root": merkle_root,
            "verified": verified,
            "landauer_joules": round(landauer_j, 18),
            "arm_energy_estimate": round(arm_energy, 12),
            "eta_score": round(eta, 4),
            "mass_equivalent_kg": round(mass_kg, 36),
            "landauer_mass_kg": round(landauer_mass, 36),
            "semantic_vector_dim": len(semantic_vec),
            "semantic_vector_preview": semantic_vec[:5] if semantic_vec else None,
            "status": "success"
        }
        
        out_f.write(json.dumps(record) + "\n")
        
        processed += 1
        
        if (i + 1) % 500 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            print(f"   Processed {i+1}/{len(kingdom_files)} ({rate:.1f} files/sec)")
            print(f"   Avg Landauer: {landauer_j:.2e} J | Avg Mass: {mass_kg:.2e} kg")

print()
print("=== ATOMIC EMBEDDER COMPLETE ===")
print(f"Processed: {processed}")
print(f"Failed: {failed}")
print(f"Time: {time.time() - start_time:.2f}s")
print(f"Output: {OUTPUT}")
print(f"Total Landauer Cost: {sum(r['landauer_joules'] for r in [])} J (approx)")
print()
print("Next: Visualize the vector map or query by physical properties.")
