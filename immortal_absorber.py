#!/data/data/com.termux/files/usr/bin/python3
"""
try:
    from paths import OPENROOT
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

Immortal Absorber v1.0
Purpose: Scan ALL files, assign Universical Primes, and update the Immortal Context Bridge.
Output: os.environ.get("OPENROOT_BASE", "/sdcard/openroot") + "/"context_bridge/immortal_context.json
"""
import sys
import json
import os
import glob
sys.path.insert(0, 'os.path.expanduser("~") + "/"une')
from universical_primes import interpret_prime
from red_words_translator import translate_to_primes, calculate_alignment_score

# Paths
DUMP_DIR = os.path.join(OPENROOT, "dump/chunks")
CONTEXT_BRIDGE = os.path.join(OPENROOT, "context_bridge/context.json")
IMMORTAL_CONTEXT = os.path.join(OPENROOT, "context_bridge/immortal_context.json")
MASTER_INDEX = os.path.join(OPENROOT, "tasks/master_index.json")

def load_master_index():
    """Load all files from all chunks."""
    print("Loading Master Index...")
    pattern = os.path.join(DUMP_DIR, "chunk_*.json")
    files = sorted(glob.glob(pattern))
    
    all_files = []
    for f in files:
        try:
            with open(f, 'r') as fp:
                data = json.load(fp)
                all_files.extend(data.get("files", []))
        except Exception as e:
            print(f"Error loading {f}: {e}")
            
    print(f"Total files loaded: {len(all_files)}")
    return all_files

def enrich_file(file_entry):
    """Add Prime metadata to a single file entry."""
    path = file_entry.get("path", "")
    size = file_entry.get("size", 0)
    
    # Translate path to primes
    primes = translate_to_primes(path)
    
    # Calculate alignment
    alignment = calculate_alignment_score(primes)
    
    # Extract top keyword
    top_keywords = [p["word"] for p in primes if p["prime"] in ["AGZ", "ZNZ", "ATZ", "NAN", "SXY", "DGZ"]]
    top_parasitic = [p["word"] for p in primes if p["prime"] == "PAR"]
    
    # Determine category
    if alignment >= 0.8:
        category = "KINGDOM_CORE"
    elif alignment >= 0.5:
        category = "ALIGNMENT_BUILD"
    elif alignment >= 0.2:
        category = "NEUTRAL_NOISE"
    else:
        category = "PARASITIC_WASTE"
        
    # Get essence chain (first 3 primes)
    essence_chain = " → ".join([p.get("reading", "Unknown") for p in primes[:3]])
    
    # Create enriched entry
    enriched = {
        "path": path,
        "size": size,
        "prime_sequence": [p["prime"] for p in primes],
        "alignment_score": round(alignment, 4),
        "category": category,
        "keywords": list(set(top_keywords))[:5],
        "parasitic_flags": list(set(top_parasitic))[:3],
        "essence_chain": essence_chain
    }
    
    return enriched

def main():
    print("=== IMMORTAL ABSORBER v1.0 ===")
    print("Step 1: Loading Master Index...")
    all_files = load_master_index()
    
    if not all_files:
        print("ERROR: No files found in chunks.")
        return

    print(f"Step 2: Enriching {len(all_files)} files with Universical Primes...")
    enriched_data = []
    
    for i, f in enumerate(all_files):
        enriched = enrich_file(f)
        enriched_data.append(enriched)
        
        if (i + 1) % 1000 == 0:
            print(f"   Processed {i+1}/{len(all_files)} files...")

    print("Step 3: Building Immortal Context...")
    
    # Load existing context if it exists
    existing_context = {}
    if os.path.exists(CONTEXT_BRIDGE):
        try:
            with open(CONTEXT_BRIDGE, 'r') as f:
                existing_context = json.load(f)
        except:
            pass

    # Construct new immortal context
    immortal_context = {
        "meta": {
            "name": "OpenRoot Immortal Context",
            "version": "2.0",
            "created": "2026-07-24",
            "total_files_indexed": len(enriched_data),
            "universical_primes_version": "1.0",
            "cooperation_formula": "η_coop = Σ(useful_output) / (effort × (1 + extraction))",
            "axiom": "AGAPE (A) is the source of all power. Power multiplies when distributed."
        },
        "statistics": {
            "kingdom_core": len([x for x in enriched_data if x["category"] == "KINGDOM_CORE"]),
            "alignment_build": len([x for x in enriched_data if x["category"] == "ALIGNMENT_BUILD"]),
            "neutral_noise": len([x for x in enriched_data if x["category"] == "NEUTRAL_NOISE"]),
            "parasitic_waste": len([x for x in enriched_data if x["category"] == "PARASITIC_WASTE"])
        },
        "file_index": enriched_data,
        "wisdom_corpus_ref": os.path.join(OPENROOT, "wisdom/wisdom_corpus.json"),
        "encyclopedia_ref": os.path.join(OPENROOT, "universical/encyclopedia.json")
    }

    # Save
    print(f"Step 4: Saving to {IMMORTAL_CONTEXT}...")
    with open(IMMORTAL_CONTEXT, 'w') as f:
        json.dump(immortal_context, f, indent=2)

    print("\n=== IMMORTAL CONTEXT CREATED ===")
    print(f"Total Files: {len(enriched_data)}")
    print(f"Kingdom Core: {immortal_context['statistics']['kingdom_core']}")
    print(f"Alignment Build: {immortal_context['statistics']['alignment_build']}")
    print(f"Neutral Noise: {immortal_context['statistics']['neutral_noise']}")
    print(f"Parasitic Waste: {immortal_context['statistics']['parasitic_waste']}")
    print(f"\nSaved: {IMMORTAL_CONTEXT}")
    print("\nNext Step: Use this file for Nomic Embedding and Vector Mapping.")

if __name__ == "__main__":
    main()
