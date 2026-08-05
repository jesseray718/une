#!/data/data/com.termux/files/usr/bin/python3
"""
THE NEWTON KERNEL INITIALIZER
Converts raw logs into a Living Wiki-Manual.
Creates the "Day One" jumping-off point.
"""
import os, json, sys
from datetime import datetime

CB = "/sdcard/openroot/context_bridge/immortal_context_merged.json"
WIKI_PATH = "/sdcard/openroot/wiki_ledger.md"
STATE_FILE = "/sdcard/openroot/state_checkpoint.json"

def load_cb():
    if not os.path.exists(CB): return {"entries": []}
    try:
        with open(CB) as f: return json.load(f)
    except: return {"entries": []}

def generate_wiki(entries):
    """Generates a comprehensive Wiki-Manual from context entries."""
    md = [
        "# 🧬 The OpenRoot Living Wiki",
        f"*Generated: {datetime.now().isoformat()}*",
        "",
        "## 1. Introduction",
        "This system is an **Autonomous, Self-Evolving Computational Engine**.",
        "It blends permaculture principles, thermodynamics, and theological axioms into code.",
        "It remembers its last state (Newton Chain) and upgrades itself offline-first.",
        "",
        "## 2. How It Operates",
        "- **Input**: Notes, Errors, Pipeline Runs.",
        "- **Process**: Guardian detects stress -> Generates Patch -> Tests -> Commits.",
        "- **Output**: Updated Code, New Wiki Entries, GitHub Contributions.",
        "",
        "## 3. Tuning Your Workflow",
        "To tune this engine:",
        "1. Log ideas: `python3 note.py 'your idea'`",
        "2. Run pipeline: `python3 core_atomic.py pipeline`",
        "3. Check status: `~/une/status`",
        "",
        "## 4. The Newton Chain (Continuity)",
        "The system never starts from zero. It loads `state_checkpoint.json`.",
        "This file holds the exact logic state where the previous run stopped.",
        "When you restart, the engine resumes from the furthest reached point.",
        "",
        "## 5. Evolution Log",
        "| Timestamp | Event | Action Taken | Status |",
        "|---|---|---|---|"
    ]
    
    for e in entries[-50:]: # Last 50 events
        ts = e.get("timestamp", "?")[:19]
        et = e.get("type", "unknown")
        act = e.get("action_taken", e.get("text", ""))[:50]
        status = "✅" if "patch" in str(act).lower() or "pass" in str(e).lower() else "⚠️"
        md.append(f"| {ts} | {et} | {act} | {status} |")
        
    md.append("\n---\n*End of Live Wiki*")
    return "\n".join(md)

def save_state(state_data):
    with open(STATE_FILE, "w") as f:
        json.dump(state_data, f, indent=2)

# Load Data
cb = load_cb()
entries = cb.get("entries", [])

# Generate Wiki
wiki_content = generate_wiki(entries)
with open(WIKI_PATH, "w") as f:
    f.write(wiki_content)
print(f"✅ Wiki generated: {WIKI_PATH}")

# Initialize State (Newton Chain Start)
current_state = {
    "last_run": datetime.now().isoformat(),
    "next_step": "fix_synergy_mult_keyerror", # Default starting point
    "version": "1.0.0",
    "contributions_made": 0
}
save_state(current_state)
print(f"✅ State checkpoint initialized: {STATE_FILE}")
print("🚀 System ready for autonomous evolution.")
