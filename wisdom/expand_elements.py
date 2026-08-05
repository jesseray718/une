#!/data/data/com.termux/files/usr/bin/python3
"""Expand elements from wisdom corpus into individual files."""
import os, json

UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))
CORPUS = os.path.join(UNE_HOME, "wisdom", "wisdom_corpus.json")

def expand_elements():
    """Read corpus and write each element to its own file."""
    if not os.path.exists(CORPUS):
        return {"status": "no corpus"}
    with open(CORPUS) as f:
        data = json.load(f)
    
    out_dir = os.path.join(UNE_HOME, "wisdom", "expanded")
    os.makedirs(out_dir, exist_ok=True)
    
    count = 0
    elements = data.get("elements", data) if isinstance(data, dict) else data
    if isinstance(elements, dict):
        for key, val in elements.items():
            with open(os.path.join(out_dir, f"{key}.json"), "w") as f:
                json.dump(val, f, indent=2)
            count += 1
    
    return {"status": "expanded", "count": count}

if __name__ == "__main__":
    print(expand_elements())
