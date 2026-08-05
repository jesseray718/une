#!/data/data/com.termux/files/usr/bin/python3
"""
try:
    from paths import OPENROOT
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

Batch Absorber: Processes a specific range of chunks (e.g., 1-20).
Translates paths to Universical Primes and ranks by Alignment.
"""
import sys
import json
import os
import glob
sys.path.insert(0, '/data/data/com.termux/files/home/une')
from universical_primes import interpret_prime
from red_words_translator import translate_to_primes, calculate_alignment_score

DUMP_DIR = os.path.join(OPENROOT, "dump/chunks")
START_TASK = 1
END_TASK = 20

def load_chunk(task_id):
    path = os.path.join(DUMP_DIR, f"chunk_{task_id}.json")
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return None

def analyze_chunk(task_id, data):
    files = data.get("files", [])
    if not files:
        return None

    # Sample first 5 files for speed
    sample = files[:5]
    total_score = 0
    count = 0
    keywords = []

    for f in sample:
        path = f.get("path", "")
        primes = translate_to_primes(path)
        score = calculate_alignment_score(primes)
        total_score += score
        count += 1
        
        # Extract high-value primes
        for p in primes:
            if p["prime"] in ["AGZ", "ZNZ", "ATZ", "NAN", "SXY", "DGZ", "EYZ"]:
                keywords.append(p["word"])
            elif p["prime"] == "PAR":
                keywords.append(f"PAR:{p['word']}")

    avg = total_score / count if count else 0
    
    return {
        "task_id": task_id,
        "file_count": len(files),
        "score": round(avg, 4),
        "keywords": list(set(keywords))[:5],
        "sample": files[0]["path"] if files else ""
    }

print(f"=== BATCH ABSORBER: Tasks {START_TASK} to {END_TASK} ===")
results = []

for i in range(START_TASK, END_TASK + 1):
    data = load_chunk(i)
    if data:
        res = analyze_chunk(i, data)
        if res:
            results.append(res)
            print(f"Task {i}: Score {res['score']:.4f} | Files: {res['file_count']}")

# Sort by score descending
results.sort(key=lambda x: x['score'], reverse=True)

print("\n--- RANKED LIST (Highest Alignment First) ---")
for i, r in enumerate(results):
    print(f"{i+1}. Task {r['task_id']:3d} | Score: {r['score']:.4f}")
    print(f"   Keywords: {', '.join(r['keywords'])}")
    print(f"   Sample: {r['sample'][:60]}...")
    print()

# Save to file
with open(os.path.join(OPENROOT, "tasks/batch_1_20_ranked.json"), "w") as f:
    json.dump(results, f, indent=2)
print("Saved to: /sdcard/openroot/tasks/batch_1_20_ranked.json")
