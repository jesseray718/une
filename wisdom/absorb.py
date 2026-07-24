#!/usr/bin/env python3
"""
Universal absorber — feed any AI output into the canonical wisdom_corpus.json
Usage:
  python3 absorb.py               # reads from clipboard if available, else stdin
  python3 absorb.py filename.txt  # reads from a file
  echo "text" | python3 absorb.py
"""
import json, os, sys, datetime

WISDOM = "/data/data/com.termux/files/home/une/wisdom/wisdom_corpus.json"
os.makedirs(os.path.dirname(WISDOM), exist_ok=True)

def get_input():
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as f:
            return f.read().strip()
    # try clipboard (Termux)
    try:
        import subprocess
        clip = subprocess.check_output(["termux-clipboard-get"], text=True).strip()
        if clip:
            return clip
    except Exception:
        pass
    # fallback to stdin
    print("Paste the AI output, then press Ctrl+D when finished:")
    return sys.stdin.read().strip()

text = get_input()
if not text:
    print("No content received. Aborting.")
    sys.exit(1)

entry = {
    "ts": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
    "source": "external_ai",
    "type": "absorb",
    "content": text
}

if os.path.exists(WISDOM):
    try:
        with open(WISDOM) as f:
            data = json.load(f)
    except Exception:
        data = {"entries": []}
else:
    data = {"entries": [], "meta": {"canonical": True, "project": "Agape-UNE / OpenRoot"}}

if "entries" not in data:
    data["entries"] = []

data["entries"].append(entry)
data["last_updated"] = entry["ts"]

with open(WISDOM, "w") as f:
    json.dump(data, f, indent=2)

print(f"Absorbed {len(text)} characters into:")
print(WISDOM)
print(f"Total entries: {len(data['entries'])}")
