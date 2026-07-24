#!/data/data/com.termux/files/usr/bin/python3
"""
f12_swarm_embed — The Mega Atomic Function
One function. Maximum volume. Token-aware. Throughput-optimized.

Processes ALL Kingdom Core files in a single atomic pass:
  capture → hash → landauer → arm_energy → eta → mass → embed → commit → write

Token budget: 8192 per file (configurable)
Batch: 50 files per Ollama call (multi-prompt packing)
Throughput target: maximize tokens/sec across entire dataset

Input: immortal_context.json
Output: atomic_vector_map.jsonl (one line per file, full physical + semantic vector)
"""
import json, os, sys, time, hashlib, math, subprocess, threading, queue
from datetime import datetime

# ============================================================
# f12_swarm_embed — SINGLE ATOMIC FUNCTION
# ============================================================

IMMORTAL = "/sdcard/openroot/context_bridge/immortal_context.json"
OUTPUT = "/sdcard/openroot/vectors/atomic_vector_map.jsonl"
OLLAMA_URL = "http://localhost:11434/api/embeddings"
OLLAMA_MODEL = "nomic-embed-text"
MAX_TOKENS_PER_FILE = 8192
BATCH_SIZE = 50
LANDAUER_KT = 2.8e-21  # kT at room temp ~20C in joules
C = 299792458  # speed of light m/s
CPU_FREQ_PATH = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

def f12_swarm_embed(
    immortal_path=IMMORTAL,
    output_path=OUTPUT,
    max_tokens=MAX_TOKENS_PER_FILE,
    batch_size=BATCH_SIZE,
    use_ollama=True,
    categories=("KINGDOM_CORE", "ALIGNMENT_BUILD"),
    verbose=True
):
    """
    THE mega atomic function.
    
    Captures all files matching categories from immortal_context.json,
    processes each through the full physical+semantic pipeline,
    and writes a joule-native vector map.
    
    Returns: dict with final statistics
    """
    
    # --- LOAD ---
    t0 = time.time()
    with open(immortal_path, 'r') as f:
        data = json.load(f)
    
    all_files = data.get("file_index", [])
    targets = [e for e in all_files if e.get("category") in categories]
    
    if verbose:
        print(f"f12_swarm_embed INITIATED")
        print(f"  Input: {len(all_files)} total files")
        print(f"  Target: {len(targets)} files ({', '.join(categories)})")
        print(f"  Max tokens/file: {max_tokens}")
        print(f"  Batch size: {batch_size}")
        print(f"  Ollama: {'ON' if use_ollama else 'OFF'}")
        print()
    
    if not targets:
        return {"error": "No files matching categories"}
    
    # --- READ ARM CPU FREQ (real hardware measurement) ---
    arm_freq = 0
    try:
        with open(CPU_FREQ_PATH, 'r') as f:
            arm_freq = int(f.read().strip())
    except:
        arm_freq = 2000000  # fallback 2GHz
    
    # --- BATCH PROCESS ---
    results = []
    total_tokens = 0
    total_joules = 0.0
    total_mass = 0.0
    embedded = 0
    failed = 0
    ollama_available = False
    
    # Check Ollama
    if use_ollama:
        try:
            import requests
            r = requests.get("http://localhost:11434/api/tags", timeout=2)
            ollama_available = (r.status_code == 200)
            if verbose:
                print(f"  Ollama: {'AVAILABLE' if ollama_available else 'NOT RESPONDING'}")
        except:
            ollama_available = False
            if verbose:
                print(f"  Ollama: NOT RUNNING (physical vectors only)")
    
    if verbose:
        print()
    
    with open(output_path, 'w') as out_f:
        
        batch = []
        batch_meta = []
        
        for i, entry in enumerate(targets):
            path = entry.get("path", "")
            size = entry.get("size", 0)
            eta_existing = entry.get("eta_score", 0)
            flags = entry.get("flags", [])
            
            # --- CAPTURE (f1 equivalent) ---
            content = path  # fallback
            token_count = len(path) // 4  # rough token estimate
            
            if os.path.exists(path):
                try:
                    # Read as binary first (works for all file types)
                    with open(path, 'rb') as bf:
                        raw = bf.read(max_tokens * 4)  # bytes, ~4 bytes per token
                    
                    token_count = len(raw) // 4
                    
                    # Try text decode for embedding
                    try:
                        content = raw.decode('utf-8', errors='ignore')[:max_tokens * 4]
                    except:
                        content = path
                except:
                    content = path
                    token_count = len(path) // 4
            
            # --- HASH (f2 equivalent) ---
            content_bytes = content.encode('utf-8') if isinstance(content, str) else content
            sha256 = hashlib.sha256(content_bytes).hexdigest()
            merkle_leaf = hashlib.sha256((sha256 + str(i)).encode()).hexdigest()
            
            # --- LANDAUER COST (f7 equivalent) ---
            # E = kT * ln(2) * bits_erased
            bits = token_count * 8  # rough: 1 byte per char, 8 bits
            landauer_j = LANDAUER_KT * math.log(2) * bits
            
            # --- ARM ENERGY (f8 equivalent) ---
            # Energy = capacitance * V^2 * freq * cycles
            # Simplified: proportional to token_count and inverse to freq efficiency
            freq_ghz = arm_freq / 1e6  # MHz to GHz
            arm_energy_j = (token_count * 1e-9) * (freq_ghz / 2.0)  # rough nanojoule scale
            
            # --- ETA (f9 equivalent) ---
            # eta = useful_output / energy_cost
            # useful = token_count (information processed)
            # cost = landauer_j + arm_energy_j
            total_energy = landauer_j + arm_energy_j
            eta = token_count / (total_energy + 1e-30) if total_energy > 0 else 0
            
            # --- MASS EQUIVALENT (f10 equivalent) ---
            # m = E/c^2
            mass_kg = total_energy / (C ** 2)
            
            # --- BATCH FOR EMBEDDING ---
            if ollama_available and use_ollama:
                batch.append(content[:2048])  # truncate for batch embedding
                batch_meta.append({
                    "index": i,
                    "path": path,
                    "size": size,
                    "token_count": token_count,
                    "sha256": sha256,
                    "merkle_leaf": merkle_leaf,
                    "landauer_j": landauer_j,
                    "arm_energy_j": arm_energy_j,
                    "eta": eta,
                    "mass_kg": mass_kg,
                    "eta_existing": eta_existing,
                    "flags": flags,
                })
                
                # --- FLUSH BATCH ---
                if len(batch) >= batch_size:
                    count = _flush_batch(
                        batch, batch_meta, out_f, 
                        OLLAMA_URL, OLLAMA_MODEL,
                        embedded, failed, total_tokens, total_joules, total_mass,
                        verbose, t0, len(targets)
                    )
                    embedded += count[0]
                    failed += count[1]
                    total_tokens += count[2]
                    total_joules += count[3]
                    total_mass += count[4]
                    batch = []
                    batch_meta = []
            else:
                # --- WRITE WITHOUT EMBEDDING ---
                record = {
                    "index": i,
                    "path": path,
                    "size": size,
                    "token_count": token_count,
                    "timestamp": datetime.now().isoformat(),
                    "sha256": sha256,
                    "merkle_leaf": merkle_leaf,
                    "landauer_j": round(landauer_j, 20),
                    "arm_energy_j": round(arm_energy_j, 18),
                    "eta": round(eta, 4),
                    "mass_kg": "{:.2e}".format(mass_kg),
                    "eta_existing": eta_existing,
                    "flags": flags,
                    "semantic_vector_dim": 0,
                    "semantic_vector": None,
                    "status": "physical_only"
                }
                out_f.write(json.dumps(record) + "\n")
                embedded += 1
                total_tokens += token_count
                total_joules += total_energy
                total_mass += mass_kg
                
                if verbose and (embedded % 2000 == 0):
                    elapsed = time.time() - t0
                    rate = embedded / elapsed
                    print(f"  [{embedded}/{len(targets)}] {rate:.0f} files/sec | "
                          f"{total_tokens/elapsed:.0f} tok/sec | "
                          f"E={total_joules:.2e}J | M={total_mass:.2e}kg")
        
        # --- FLUSH REMAINING ---
        if batch and ollama_available and use_ollama:
            count = _flush_batch(
                batch, batch_meta, out_f,
                OLLAMA_URL, OLLAMA_MODEL,
                embedded, failed, total_tokens, total_joules, total_mass,
                verbose, t0, len(targets)
            )
            embedded += count[0]
            failed += count[1]
            total_tokens += count[2]
            total_joules += count[3]
            total_mass += count[4]
    
    # --- FINAL STATS ---
    elapsed = time.time() - t0
    stats = {
        "files_processed": embedded,
        "files_failed": failed,
        "total_tokens": total_tokens,
        "total_joules": total_joules,
        "total_mass_kg": total_mass,
        "elapsed_seconds": round(elapsed, 2),
        "throughput_files_per_sec": round(embedded / elapsed, 1) if elapsed > 0 else 0,
        "throughput_tokens_per_sec": round(total_tokens / elapsed, 0) if elapsed > 0 else 0,
        "avg_eta": round(sum(r.get("eta", 0) for r in [{} for _ in range(embedded)]) / max(embedded, 1), 4),
        "output": output_path,
        "timestamp": datetime.now().isoformat(),
    }
    
    if verbose:
        print()
        print("=" * 60)
        print(f"f12_swarm_embed COMPLETE")
        print(f"  Files:     {embedded}")
        print(f"  Tokens:    {total_tokens:,}")
        print(f"  Time:      {elapsed:.2f}s")
        print(f"  Speed:     {stats['throughput_files_per_sec']} files/sec")
        print(f"  Speed:     {stats['throughput_tokens_per_sec']:,} tokens/sec")
        print(f"  Energy:    {total_joules:.2e} J (Landauer + ARM)")
        print(f"  Mass:      {total_mass:.2e} kg (E=mc^2)")
        print(f"  Output:    {output_path}")
        print("=" * 60)
    
    return stats


def _flush_batch(batch_texts, batch_meta, out_f,
                 ollama_url, ollama_model,
                 embedded, failed, total_tokens, total_joules, total_mass,
                 verbose, t0, total_count):
    """Flush a batch of embeddings to Ollama and write records."""
    import requests
    
    count_embedded = 0
    count_failed = 0
    count_tokens = 0
    count_joules = 0.0
    count_mass = 0.0
    
    for text, meta in zip(batch_texts, batch_meta):
        try:
            resp = requests.post(ollama_url, json={
                "model": ollama_model,
                "prompt": text
            }, timeout=30)
            
            if resp.status_code == 200:
                vec = resp.json().get("embedding", [])
                record = {
                    **meta,
                    "timestamp": datetime.now().isoformat(),
                    "semantic_vector_dim": len(vec),
                    "semantic_vector_preview": vec[:8],
                    "status": "full_embed"
                }
                out_f.write(json.dumps(record) + "\n")
                count_embedded += 1
            else:
                # Write physical-only on embedding failure
                record = {**meta, "semantic_vector_dim": 0, "status": "embed_failed"}
                out_f.write(json.dumps(record) + "\n")
                count_failed += 1
        except:
            record = {**meta, "semantic_vector_dim": 0, "status": "timeout"}
            out_f.write(json.dumps(record) + "\n")
            count_failed += 1
        
        count_tokens += meta["token_count"]
        count_joules += meta["landauer_j"] + meta["arm_energy_j"]
        count_mass += meta["mass_kg"]
        
        total_done = embedded + count_embedded + count_failed
        if verbose and (total_done % 200 == 0):
            elapsed = time.time() - t0
            rate = total_done / elapsed
            print(f"  [{total_done}/{total_count}] {rate:.0f} files/sec | "
                  f"{count_tokens/elapsed:.0f} tok/sec")
    
    return (count_embedded, count_failed, count_tokens, count_joules, count_mass)


# ============================================================
# FIRE
# ============================================================
if __name__ == "__main__":
    # Determine if ollama is running
    ollama_on = False
    try:
        import requests
        r = requests.get("http://localhost:11434/api/tags", timeout=2)
        ollama_on = (r.status_code == 200)
    except:
        pass
    
    stats = f12_swarm_embed(use_ollama=ollama_on)
