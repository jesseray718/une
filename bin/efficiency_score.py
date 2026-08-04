#!/data/data/com.termux/files/usr/bin/python3
"""OpenRoot Efficiency Score - Joules per Query metric."""
import json, os, sys

LEDGER_PATH = "/data/data/com.termux/files/home/une/logs/energy/stream.jsonl"
CACHE_PATH = "/data/data/com.termux/files/home/une/storage/joule_cache.json"
CONTEXT_PATH = "/data/data/com.termux/files/home/une/context_bridge/context.json"

def load_samples():
    samples = []
    if not os.path.exists(LEDGER_PATH):
        return samples
    with open(LEDGER_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    samples.append(json.loads(line))
                except:
                    pass
    return samples

def count_queries():
    """Count wisdom queries from context sessions."""
    try:
        with open(CONTEXT_PATH, "r") as f:
            ctx = json.load(f)
        return len(ctx.get("sessions", []))
    except:
        return 0

def main():
    samples = load_samples()
    cache = {}
    try:
        with open(CACHE_PATH, "r") as f:
            cache = json.load(f)
    except:
        pass

    total_joules = cache.get("total_joules", 0.0)
    query_count = count_queries()
    sample_count = len([s for s in samples if s.get("type") == "sample"])
    error_count = len([s for s in samples if s.get("type") == "error"])

    # Calculate average power from samples
    powers = [s.get("power_w", 0) for s in samples if s.get("type") == "sample"]
    avg_power = sum(powers) / len(powers) if powers else 0

    # Peak power (most negative = highest discharge)
    peak_discharge = min(powers) if powers else 0
    idle_power = max(powers) if powers else 0

    # Joules per query
    joules_per_query = abs(total_joules) / query_count if query_count > 0 else 0

    # Efficiency score: lower joules per query = higher efficiency
    # Scale: 100 = perfect, 0 = terrible. Based on joules_per_query.
    if joules_per_query > 0:
        efficiency = max(0, 100 - (joules_per_query * 10))
    else:
        efficiency = 100

    result = {
        "total_joules": round(total_joules, 4),
        "total_queries": query_count,
        "joules_per_query": round(joules_per_query, 4),
        "efficiency_score": round(efficiency, 1),
        "avg_power_mW": round(avg_power * 1000, 2),
        "peak_discharge_mW": round(peak_discharge * 1000, 2),
        "idle_power_mW": round(idle_power * 1000, 2),
        "samples_collected": sample_count,
        "errors": error_count,
        "rating": "EXCELLENT" if efficiency >= 80 else "GOOD" if efficiency >= 50 else "INEFFICIENT"
    }
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
