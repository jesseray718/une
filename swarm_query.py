#!/data/data/com.termux/files/usr/bin/python3
"""
import os
try:
    from paths import OPENROOT
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

Swarm Query Interface
=====================
Searches the atomic vector map by:
  1. Semantic proximity (meaning)
  2. Physical properties (energy, mass, eta)
  3. Swarm consensus (multi-model verification via aiq providers)

Routes complex queries through Groq -> Cerebras -> local
just like the epi epistemology swarm.

Usage:
  python3 swarm_query.py "thermal cascade efficiency"
  python3 swarm_query.py --physical --min-eta 0.7 --min-energy 1e-15
  python3 swarm_query.py --swarm "Is fractal recursion necessary for cooperation scaling?"
  python3 swarm_query.py --chart eta
  python3 swarm_query.py --chart energy
"""
import json, os, sys, math, time, argparse, subprocess
from datetime import datetime

VECTOR_MAP = os.path.join(OPENROOT, "vectors/atomic_vector_map.jsonl")
SWARM_CFG = "os.path.expanduser("~") + "/".governor/swarm-config.json"
OUTPUT_DIR = os.path.join(OPENROOT, "vectors")

# ============================================================
# FIXED ETA CALCULATION (normalized, no saturation)
# ============================================================

def calc_eta(token_count, landauer_j, arm_energy_j):
    """
    Normalized efficiency score (UNCAPPED).
    eta > 1.0 = efficient
    eta < 1.0 = inefficient
    NO CAPS: Let the numbers breathe!
    """
    total_j = landauer_j + arm_energy_j
    if total_j == 0 or token_count == 0:
        return 0.0
    
    # Benchmark: 1 microjoule per token (adjust if needed)
    benchmark = token_count * 1e-6
    
    # Ratio: Expected Cost / Actual Cost
    # If actual cost is tiny, eta is HUGE (very efficient)
    eta = benchmark / total_j
    
    return round(eta, 4)

def load_vectors():
    """Load the full vector map into memory."""
    records = []
    if not os.path.exists(VECTOR_MAP):
        print(f"[!] Vector map not found: {VECTOR_MAP}")
        print("    Run f12_swarm_embed.py first.")
        sys.exit(1)
    
    with open(VECTOR_MAP, 'r') as f:
        for line in f:
            try:
                records.append(json.loads(line.strip()))
            except:
                pass
    
    return records

# ============================================================
# PHYSICAL SEARCH (by energy, mass, eta)
# ============================================================

def physical_search(records, min_eta=None, max_eta=None,
                   min_energy=None, max_energy=None,
                   min_mass=None, max_mass=None,
                   min_tokens=None, max_tokens=None,
                   limit=50):
    """Search by physical properties."""
    results = []
    
    for r in records:
        eta = calc_eta(r.get("token_count", 0), r.get("landauer_j", 0), r.get("arm_energy_j", 0))
        energy = r.get("landauer_j", 0) + r.get("arm_energy_j", 0)
        mass = float(r.get("mass_kg", "0").replace("e", "e") if isinstance(r.get("mass_kg"), str) else r.get("mass_kg", 0))
        tokens = r.get("token_count", 0)
        
        if min_eta is not None and eta < min_eta:
            continue
        if max_eta is not None and eta > max_eta:
            continue
        if min_energy is not None and energy < min_energy:
            continue
        if max_energy is not None and energy > max_energy:
            continue
        if min_tokens is not None and tokens < min_tokens:
            continue
        if max_tokens is not None and tokens > max_tokens:
            continue
        
        results.append({
            "path": r.get("path", ""),
            "eta": round(eta, 4),
            "energy_j": round(energy, 20),
            "mass_kg": mass,
            "tokens": tokens,
            "sha256": r.get("sha256", "")[:16],
            "status": r.get("status", ""),
        })
    
    return results[:limit]

# ============================================================
# SEMANTIC SEARCH (keyword / text similarity)
# ============================================================

def semantic_search(records, query, limit=20):
    """Simple keyword-based semantic search (no Ollama needed)."""
    query_lower = query.lower()
    query_terms = query_lower.split()
    
    scored = []
    for r in records:
        path = r.get("path", "").lower()
        tokens = r.get("token_count", 0)
        
        # Score by how many query terms appear in the path
        score = sum(1 for term in query_terms if term in path)
        
        # Boost for exact phrase match
        if query_lower in path:
            score += 5
        
        # Boost for higher eta (more valuable files)
        eta = calc_eta(r.get("token_count", 0), r.get("landauer_j", 0), r.get("arm_energy_j", 0))
        score += eta * 0.1
        
        if score > 0:
            scored.append({
                "path": r.get("path", ""),
                "score": round(score, 2),
                "eta": round(eta, 4),
                "tokens": tokens,
                "energy_j": round(r.get("landauer_j", 0) + r.get("arm_energy_j", 0), 18),
                "mass_kg": r.get("mass_kg", "0"),
                "sha256": r.get("sha256", "")[:16],
                "status": r.get("status", ""),
            })
    
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:limit]

# ============================================================
# SWARM CONSENSUS (multi-model via aiq)
# ============================================================

def swarm_consensus(query, records, limit=10):
    """
    Route query through the swarm:
      1. SCOUT: Find relevant files via semantic search
      2. ARCHITECT: Build context from top results
      3. SKEPTIC: Send to multiple providers for verification
      4. SCRIBE: Consolidate and format
      5. GOVERNOR: Display final answer
    """
    print("=" * 60)
    print("SWARM CONSENSUS INITIATED")
    print(f"Query: {query}")
    print("=" * 60)
    
    # --- 1. SCOUT: Find relevant files ---
    print("\n[SCOUT] Searching vector map...")
    relevant = semantic_search(records, query, limit=limit)
    
    if not relevant:
        print("[SCOUT] No relevant files found.")
        return
    
    print(f"[SCOUT] Found {len(relevant)} relevant files:")
    for i, r in enumerate(relevant[:5]):
        print(f"  {i+1}. {r['path'][:80]}")
        print(f"     eta={r['eta']} tokens={r['tokens']} score={r['score']}")
    
    # --- 2. ARCHITECT: Build context ---
    print("\n[ARCHITECT] Building context from top files...")
    context_parts = []
    for r in relevant[:5]:
        path = r["path"]
        if os.path.exists(path):
            try:
                with open(path, 'r', errors='ignore') as f:
                    content = f.read(500)
                context_parts.append(f"--- {path} ---\n{content}")
            except:
                context_parts.append(f"--- {path} ---\n[unable to read]")
        else:
            context_parts.append(f"--- {path} ---\n[file not found on disk]")
    
    context = "\n\n".join(context_parts)
    
    # --- 3. SKEPTIC: Multi-model verification ---
    print("\n[SKEPTIC] Querying swarm providers...")
    
    # Load swarm config
    providers = []
    try:
        with open(SWARM_CFG, 'r') as f:
            cfg = json.load(f)
        providers = cfg.get("provider_order", ["groq"])
    except:
        providers = ["groq"]
    
    # Build the prompt
    full_prompt = f"""You are analyzing a knowledge base. Based on the following files and their content, answer this question:

QUESTION: {query}

CONTEXT FROM KNOWLEDGE BASE:
{context[:3000]}

Provide a concise, accurate answer. If the context is insufficient, say so.
Cite which file(s) support your answer."""
    
    results = []
    for provider in providers:
        if provider == "local":
            continue  # Skip local for now (no Ollama chat model loaded)
        
        print(f"  [{provider}] querying...")
        
        # Use aiq to query
        try:
            cmd = ["aiq", "-p", full_prompt[:4000]]
            
            # Add provider-specific model
            if provider == "groq":
                cmd = ["aiq", "llama-3.3-70b-versatile", "-p", full_prompt[:4000]]
            elif provider == "cerebras":
                cmd = ["aiq", "llama3.1-70b", "-p", full_prompt[:4000], "--provider", "cerebras"]
            
            result = subprocess.run(
                cmd,
                capture_output=True, text=True, timeout=45,
                env={**os.environ}
            )
            
            output = result.stdout.strip()
            if output and len(output) > 10:
                results.append({
                    "provider": provider,
                    "response": output,
                    "status": "success"
                })
                print(f"  [{provider}] ✓ {len(output)} chars")
            else:
                stderr = result.stderr.strip()
                if stderr:
                    print(f"  [{provider}] ✗ {stderr[:80]}")
                else:
                    print(f"  [{provider}] ✗ empty response")
                results.append({
                    "provider": provider,
                    "response": "",
                    "status": "failed"
                })
        except subprocess.TimeoutExpired:
            print(f"  [{provider}] ✗ timeout")
            results.append({"provider": provider, "response": "", "status": "timeout"})
        except Exception as e:
            print(f"  [{provider}] ✗ {str(e)[:80]}")
            results.append({"provider": provider, "response": "", "status": "error"})
    
    # --- 4. SCRIBE: Consolidate ---
    print("\n[SCRIBE] Consolidating results...")
    
    successful = [r for r in results if r["status"] == "success"]
    
    if not successful:
        print("[SCRIBE] No providers responded. Showing physical search results only.")
        print("\n=== PHYSICAL RESULTS ===")
        for r in relevant:
            print(f"  {r['path']}")
            print(f"    eta={r['eta']} tokens={r['tokens']} energy={r['energy_j']:.2e}J")
        return
    
    # Show each provider's response
    for r in successful:
        print(f"\n{'='*60}")
        print(f"[{r['provider'].upper()}]")
        print(f"{'='*60}")
        print(r["response"][:2000])
    
    # --- 5. GOVERNOR: Consensus ---
    if len(successful) >= 2:
        print(f"\n{'='*60}")
        print("[GOVERNOR] CONSENSUS CHECK")
        print(f"{'='*60}")
        
        # Simple consensus: do the responses share key terms?
        responses = [r["response"].lower() for r in successful]
        
        # Extract key terms (words > 4 chars that appear in multiple responses)
        all_words = set()
        for resp in responses:
            words = set(w for w in resp.split() if len(w) > 4)
            all_words.update(words)
        
        shared = []
        for word in all_words:
            if sum(1 for resp in responses if word in resp) >= 2:
                shared.append(word)
        
        agreement = len(shared)
        
        if len(successful) >= 2:
            print(f"Providers responded: {len(successful)}/{len(results)}")
            print(f"Shared key terms: {agreement}")
            if agreement > 10:
                print("CONSENSUS: STRONG (high term overlap)")
            elif agreement > 5:
                print("CONSENSUS: MODERATE (some term overlap)")
            else:
                print("CONSENSUS: WEAK (responses diverge)")
        
        print(f"\nSupporting files:")
        for r in relevant[:5]:
            print(f"  {r['path'][:80]}")
            print(f"    eta={r['eta']} | tokens={r['tokens']} | energy={r['energy_j']:.2e}J | mass={r.get('mass_kg', '?')}")
    
    # Save query result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = f"{OUTPUT_DIR}/swarm_query_{timestamp}.json"
    with open(result_file, 'w') as f:
        json.dump({
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "relevant_files": relevant,
            "provider_responses": results,
            "consensus_shared_terms": shared if len(successful) >= 2 else [],
        }, f, indent=2)
    
    print(f"\n[GOVERNOR] Result saved: {result_file}")

# ============================================================
# VISUALIZATION (ASCII charts)
# ============================================================

def chart_distribution(records, metric="eta"):
    """Print ASCII distribution chart of a metric."""
    print(f"\n=== DISTRIBUTION: {metric.upper()} ===\n")
    
    # Collect values
    values = []
    for r in records:
        if metric == "eta":
            v = calc_eta(r.get("token_count", 0), r.get("landauer_j", 0), r.get("arm_energy_j", 0))
        elif metric == "energy":
            v = r.get("landauer_j", 0) + r.get("arm_energy_j", 0)
        elif metric == "mass":
            mv = r.get("mass_kg", 0)
            if isinstance(mv, str):
                v = float(mv)
            else:
                v = mv
        elif metric == "tokens":
            v = r.get("token_count", 0)
        else:
            continue
        
        if v > 0:
            values.append((r.get("path", ""), v))
    
    if not values:
        print(f"No {metric} values found.")
        return
    
    # Sort and get range
    values.sort(key=lambda x: x[1], reverse=True)
    max_val = values[0][1]
    min_val = values[-1][1]
    
    # Create buckets
    num_buckets = 20
    bucket_range = (max_val - min_val) / num_buckets if max_val > min_val else 1
    buckets = [0] * num_buckets
    
    for _, v in values:
        idx = min(int((v - min_val) / bucket_range), num_buckets - 1)
        buckets[idx] += 1
    
    max_count = max(buckets) if buckets else 1
    
    # Print chart
    print(f"Range: {min_val:.2e} to {max_val:.2e}")
    print(f"Files: {len(values)}")
    print()
    
    bar_width = 40
    for i, count in enumerate(buckets):
        lo = min_val + i * bucket_range
        hi = lo + bucket_range
        bar_len = int(count / max_count * bar_width) if max_count > 0 else 0
        bar = "█" * bar_len
        print(f"  {lo:.2e} - {hi:.2e} | {bar} {count}")
    
    # Top 10
    print(f"\nTop 10 by {metric}:")
    for path, v in values[:10]:
        print(f"  {v:.2e}  {path[:70]}")
    
    # Bottom 10
    print(f"\nBottom 10 by {metric}:")
    for path, v in values[-10:]:
        print(f"  {v:.2e}  {path[:70]}")

# ============================================================
# SUMMARY STATS
# ============================================================

def print_summary(records):
    """Print summary statistics of the vector map."""
    total = len(records)
    if total == 0:
        print("No records found.")
        return
    
    etas = [calc_eta(r.get("token_count", 0), r.get("landauer_j", 0), r.get("arm_energy_j", 0)) for r in records]
    energies = [r.get("landauer_j", 0) + r.get("arm_energy_j", 0) for r in records]
    tokens = [r.get("token_count", 0) for r in records]
    
    masses = []
    for r in records:
        mv = r.get("mass_kg", 0)
        if isinstance(mv, str):
            try:
                masses.append(float(mv))
            except:
                pass
        else:
            masses.append(mv)
    
    embedded = sum(1 for r in records if r.get("semantic_vector_dim", 0) > 0)
    physical_only = sum(1 for r in records if r.get("status") == "physical_only")
    
    print("=" * 60)
    print("ATOMIC VECTOR MAP SUMMARY")
    print("=" * 60)
    print(f"Total records:       {total}")
    print(f"Fully embedded:      {embedded}")
    print(f"Physical only:       {physical_only}")
    print()
    print(f"Total tokens:        {sum(tokens):,}")
    print(f"Avg tokens/file:     {sum(tokens)//total:,}")
    print(f"Max tokens:          {max(tokens):,}")
    print(f"Min tokens:          {min(tokens):,}")
    print()
    print(f"Avg eta:             {sum(etas)/total:.4f}")
    print(f"Max eta:             {max(etas):.4f}")
    print(f"Min eta:             {min(etas):.4f}")
    print()
    print(f"Total energy:        {sum(energies):.2e} J")
    print(f"Avg energy/file:     {sum(energies)/total:.2e} J")
    print()
    if masses:
        print(f"Total mass:          {sum(masses):.2e} kg")
        print(f"Avg mass/file:       {sum(masses)/total:.2e} kg")
    print("=" * 60)

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Swarm Query Interface")
    parser.add_argument("query", nargs="?", help="Semantic search query")
    parser.add_argument("--physical", action="store_true", help="Physical property search")
    parser.add_argument("--min-eta", type=float, default=None)
    parser.add_argument("--max-eta", type=float, default=None)
    parser.add_argument("--min-energy", type=float, default=None)
    parser.add_argument("--max-energy", type=float, default=None)
    parser.add_argument("--min-tokens", type=int, default=None)
    parser.add_argument("--max-tokens", type=int, default=None)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--swarm", action="store_true", help="Route through multi-model swarm")
    parser.add_argument("--chart", choices=["eta", "energy", "mass", "tokens"], help="Show distribution chart")
    parser.add_argument("--summary", action="store_true", help="Show summary statistics")
    
    args = parser.parse_args()
    
    records = load_vectors()
    
    if args.summary:
        print_summary(records)
    elif args.chart:
        chart_distribution(records, args.chart)
    elif args.physical:
        results = physical_search(
            records,
            min_eta=args.min_eta, max_eta=args.max_eta,
            min_energy=args.min_energy, max_energy=args.max_energy,
            min_tokens=args.min_tokens, max_tokens=args.max_tokens,
            limit=args.limit
        )
        print(f"\n=== PHYSICAL SEARCH RESULTS ({len(results)} files) ===\n")
        for r in results:
            print(f"  {r['path'][:80]}")
            print(f"    eta={r['eta']} energy={r['energy_j']:.2e}J tokens={r['tokens']} mass={r.get('mass_kg','?')}")
    elif args.swarm and args.query:
        swarm_consensus(args.query, records, limit=args.limit)
    elif args.query:
        results = semantic_search(records, args.query, limit=args.limit)
        print(f"\n=== SEMANTIC SEARCH: '{args.query}' ({len(results)} results) ===\n")
        for i, r in enumerate(results):
            print(f"  {i+1}. {r['path'][:80]}")
            print(f"     score={r['score']} eta={r['eta']} tokens={r['tokens']}")
            print(f"     energy={r['energy_j']:.2e}J mass={r.get('mass_kg','?')}")
    else:
        print("Usage:")
        print("  python3 swarm_query.py 'thermal cascade'")
        print("  python3 swarm_query.py --swarm 'Is fractal recursion necessary?'")
        print("  python3 swarm_query.py --physical --min-eta 0.7")
        print("  python3 swarm_query.py --chart eta")
        print("  python3 swarm_query.py --summary")
