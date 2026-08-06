#!/usr/bin/env python3
"""
import os
try:
    from paths import OPENROOT, UNE_HOME
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

ATOMIC SCAN: Rule-based Fractal Swarm Analysis
Uses 20 Elements to detect patterns without LLM.
"""
import os, sys, json, re
from datetime import datetime
from state_utils import load_ckpt, save_ckpt

REPO_PATHS = [
    "os.path.expanduser("~") + "/"une",
    os.path.join(OPENROOT, "github_clone_temp/une"),
    os.path.join(OPENROOT, "github_clone_temp/openroot")
]
CORPUS = os.path.join(UNE_HOME, "wisdom/wisdom_corpus.json")
LOG = os.path.join(OPENROOT, "session_seeds/atomic_scan_log.jsonl")

# Define patterns for the 20 Elements (Simplified for Atomic Scan)
ELEMENT_PATTERNS = {
    "E-01_OBSERVATION": r"(print|logging\.info|logger\.debug|monitor|sensor)",
    "E-02_STORAGE": r"(cache|save|write|persist|backup|snapshot)",
    "E-03_YIELD": r"(return|yield|output|result|profit|gain)",
    "E-04_FEEDBACK": r"(if.*else|try.*except|loop|while|retry|adjust)",
    "E-05_RENEWAL": r"(refresh|reload|reset|update|renew|clean)",
    "E-06_ZERO_WASTE": r"(del |remove|cleanup|gc.collect|unused)",
    "E-07_PATTERN_FIRST": r"(class|def|struct|interface|schema|template)",
    "E-08_INTEGRATION": r"(import|include|require|link|connect|merge)",
    "E-09_INCREMENTALISM": r"(step|iter|batch|chunk|partial|progressive)",
    "E-10_DIVERSITY": r"(random|shuffle|multi|alt|fallback|redundant)",
    "E-11_EDGE_VALUE": r"(edge|boundary|limit|exception|corner|near_miss)",
    "E-12_ADAPTATION": r"(adapt|pivot|scale|resize|dynamic|config)",
    "E-13_ENTROPY": r"(TODO|FIXME|HACK|TEMP|deprecated|orphan|dead_code)",
    "E-14_EMERGENCE": r"(agent|swarm|collective|network|distributed|emergent)",
    "E-15_RECIPROCITY": r"(request|response|callback|hook|event|emit)",
    "E-16_RESONANCE": r"(sync|match|align|frequency|harmonic|tune)",
    "E-17_SURRENDER": r"(yield|passive|wait|idle|sleep|release)",
    "E-18_VOID": r"(empty|null|None|skip|void|placeholder)",
    "E-19_SCALE_INVARIANCE": r"(recursive|self_similar|fractal|scale|level)",
    "E-20_INTENTION": r"(goal|objective|purpose|aim|target|intent)"
}

def scan_file(filepath):
    try:
        with open(filepath, 'r', errors='ignore') as f:
            content = f.read()
        
        findings = {}
        for elem, pattern in ELEMENT_PATTERNS.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                findings[elem] = len(matches)
        
        return {"file": filepath, "findings": findings, "size": len(content)}
    except:
        return None

def main():
    print("="*60)
    print("ATOMIC FRACTAL SWARM SCAN (Rule-Based)")
    print("="*60)
    
    total_files = 0
    total_findings = 0
    all_results = []
    
    # Scan all repo paths
    for base_path in REPO_PATHS:
        if not os.path.exists(base_path):
            print(f"Skipping missing path: {base_path}")
            continue
        
        print(f">>> Scanning {base_path}...")
        for root, dirs, files in os.walk(base_path):
            # Skip hidden and large dirs
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file.endswith(('.py', '.sh', '.md', '.json', '.txt')):
                    fp = os.path.join(root, file)
                    res = scan_file(fp)
                    if res and res["findings"]:
                        all_results.append(res)
                        total_files += 1
                        total_findings += sum(res["findings"].values())
                        
                        if len(all_results) % 10 == 0:
                            print(f"   Processed {len(all_results)} files...")
    
    # Save results
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Update Wisdom Corpus
    if os.path.exists(CORPUS):
        try:
            with open(CORPUS) as f: data = json.load(f)
            if "entries" not in data: data["entries"] = []
            
            # Aggregate top findings
            element_counts = {}
            for r in all_results:
                for elem, count in r["findings"].items():
                    element_counts[elem] = element_counts.get(elem, 0) + count
            
            entry = {
                "ts": datetime.utcnow().isoformat()+"Z",
                "source": "Atomic_Scan",
                "type": "pattern_analysis",
                "total_files": total_files,
                "total_matches": total_findings,
                "top_elements": sorted(element_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            }
            data["entries"].append(entry)
            with open(CORPUS, 'w') as f: json.dump(data, f, indent=2)
            print(f"\n✅ Updated Wisdom Corpus with {len(element_counts)} element types.")
        except Exception as e:
            print(f"⚠️ Could not update corpus: {e}")
    
    print("\n" + "="*60)
    print("SCAN COMPLETE")
    print(f"Files Analyzed: {total_files}")
    print(f"Pattern Matches: {total_findings}")
    print(f"Log Saved: {LOG}")
    print("="*60)

if __name__ == "__main__": main()
