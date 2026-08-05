#!/data/data/com.termux/files/usr/bin/python3
"""
try:
    from paths import OPENROOT
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

Task Optimizer: Reorders your 472 tasks based on Semantic Alignment.
Goal: Prioritize files that align with "Love/Give" and deprioritize "Parasitic" patterns.
"""
import json
import os
import sys
sys.path.insert(0, 'os.path.expanduser("~") + "/"une')
from prime_mapper import SemanticPrimeEngine

TASK_DIR = os.path.join(OPENROOT, "tasks")
DUMP_DIR = os.path.join(OPENROOT, "dump/chunks")
STATE_FILE = f"{TASK_DIR}/engine_state.json"
INDEX_FILE = f"{TASK_DIR}/.file_index"
OUTPUT_QUEUE = f"{TASK_DIR}/optimized_queue.json"

def load_chunks():
    chunks = []
    for i in range(1, 473): # 472 tasks
        path = f"{DUMP_DIR}/chunk_{i}.json"
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    chunks.append({"task_id": i, "data": data})
            except:
                pass
    return chunks

def main():
    print("Loading Semantic Prime Engine...")
    engine = SemanticPrimeEngine()
    
    print("Loading 472 task chunks...")
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks.")
    
    scored_tasks = []
    
    print("Analyzing alignment for each task...")
    for chunk in chunks:
        tid = chunk["task_id"]
        files = chunk["data"].get("files", [])
        
        if not files:
            continue
            
        # Sample first 5 files in chunk to estimate alignment
        sample_files = files[:5]
        total_score = 0
        count = 0
        
        for f in sample_files:
            path = f.get("path", "")
            # We don't have content yet, so we score based on PATH semantics
            # (In v2, we will read content. For now, path hints like "src", "doc", "test" vs "cache", "tmp")
            vec = engine.vectorize_concept(path)
            score = engine.calculate_alignment(vec)
            total_score += score
            count += 1
            
        avg_score = total_score / count if count > 0 else 0
        scored_tasks.append({
            "task_id": tid,
            "alignment_score": avg_score,
            "file_count": len(files),
            "recommendation": "PRIORITIZE" if avg_score > 0.5 else "REVIEW" if avg_score > 0.2 else "DEEP_SCAN_NEEDED"
        })
    
    # Sort: Highest alignment first
    scored_tasks.sort(key=lambda x: x["alignment_score"], reverse=True)
    
    # Save optimized queue
    with open(OUTPUT_QUEUE, 'w') as f:
        json.dump(scored_tasks, f, indent=2)
        
    print("\n=== OPTIMIZED TASK QUEUE GENERATED ===")
    print(f"Top Priority Tasks (High Alignment):")
    for t in scored_tasks[:5]:
        print(f"  Task {t['task_id']}: Score {t['alignment_score']:.4f} ({t['recommendation']})")
        
    print(f"\nBottom Priority Tasks (Low/Negative Alignment):")
    for t in scored_tasks[-3:]:
        print(f"  Task {t['task_id']}: Score {t['alignment_score']:.4f} ({t['recommendation']})")
        
    print(f"\nQueue saved to: {OUTPUT_QUEUE}")
    print("Next step: Run tasks in order of the optimized queue.")

if __name__ == "__main__":
    main()
