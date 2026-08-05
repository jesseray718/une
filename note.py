#!/data/data/com.termux/files/usr/bin/python3
"""Quick note/lesson logger — writes to immortal context bridge."""
import sys, json, os
from datetime import datetime

CB = "/sdcard/openroot/context_bridge/immortal_context_merged.json"

# Load existing context
existing = {"sources": [], "entries": []}
if os.path.exists(CB):
    try:
        with open(CB) as f:
            existing = json.loads(f.read())
    except:
        pass

# Get text from args OR interactive prompt
if len(sys.argv) > 1:
    text = " ".join(sys.argv[1:])
else:
    print("📝 Enter note (Ctrl+D to save):")
    try:
        text = input("> ")
    except EOFError:
        text = ""

if not text.strip():
    print("❌ Empty note.")
    sys.exit(1)

entry = {
    "type": "note",
    "timestamp": datetime.now().isoformat(),
    "text": text.strip(),
}

# Append and save
if "entries" not in existing:
    existing["entries"] = []
existing["entries"].append(entry)
os.makedirs(os.path.dirname(CB), exist_ok=True)
with open(CB, "w") as f:
    json.dump(existing, f, indent=2)

print(f"✅ Logged: {text[:60]}...")
