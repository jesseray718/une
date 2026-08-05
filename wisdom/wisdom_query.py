#!/data/data/com.termux/files/usr/bin/python3
"""Query the wisdom corpus for permaculture, theology, and strategy insights."""
import os, json

UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))
CORPUS = os.path.join(UNE_HOME, "wisdom", "wisdom_corpus.json")

def load_corpus():
    """Load the wisdom corpus from disk."""
    if not os.path.exists(CORPUS):
        return {}
    with open(CORPUS) as f:
        return json.load(f)

def list_elements():
    """List all elements in the taxonomy."""
    corpus = load_corpus()
    return list(corpus.get("elements", {}).keys()) if isinstance(corpus, dict) else []

def list_traditions():
    """List all wisdom traditions."""
    corpus = load_corpus()
    return list(corpus.get("traditions", {}).keys()) if isinstance(corpus, dict) else []

def query_problem(problem):
    """Query the wisdom database for a problem."""
    corpus = load_corpus()
    results = []
    if isinstance(corpus, dict):
        for key, val in corpus.items():
            if isinstance(val, str) and problem.lower() in val.lower():
                results.append({"source": key, "text": val})
            elif isinstance(val, dict):
                for k2, v2 in val.items():
                    if isinstance(v2, str) and problem.lower() in v2.lower():
                        results.append({"source": f"{key}.{k2}", "text": v2})
    return results

def add_lesson(lesson, source="unknown"):
    """Add a lesson to the context bridge."""
    bridge = os.environ.get("OPENROOT_HOME", "/sdcard/openroot") + "/context_bridge/lessons.jsonl"
    os.makedirs(os.path.dirname(bridge), exist_ok=True)
    import time
    entry = {"lesson": lesson, "source": source, "timestamp": time.time()}
    with open(bridge, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry

def main():
    """Main entry point for wisdom query."""
    import sys
    if len(sys.argv) > 1:
        results = query_problem(sys.argv[1])
        for r in results:
            print(f"[{r['source']}] {r['text'][:100]}...")
        return results
    else:
        print("Usage: python3 wisdom_query.py <problem>")
        print(f"Elements: {list_elements()}")
        print(f"Traditions: {list_traditions()}")
        return {}

if __name__ == "__main__":
    main()
