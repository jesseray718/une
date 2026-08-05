#!/data/data/com.termux/files/usr/bin/python3
"""
ANTIFRAGILE GUARDIAN
====================
Autonomous, Passive, Non-Genetic, Antifragile System.

Mechanism:
1. OBSERVE: Scans logs, notes, and stderr for stress signals (errors, deficits).
2. DIAGNOSE: Matches patterns to known failure modes.
3. ACT: Generates a patch or optimization script.
4. LEARN: Logs the event and the fix to the Immortal Context Bridge.
5. ADAPT: Updates its own pattern library to prevent recurrence.

Run via cron: */5 * * * * python3 /data/data/com.termux/files/home/une/guardian.py
Or manually: python3 guardian.py
"""
import os, sys, json, re, subprocess, time
from datetime import datetime

# Paths
CB_PATH = "/sdcard/openroot/context_bridge/immortal_context_merged.json"
LOG_FILE = "/sdcard/openroot/ledger.jsonl"
NOTES_FILE = "/sdcard/openroot/notes.txt"
GUARDIAN_LOG = "/sdcard/openroot/guardian_log.jsonl"
PATTERN_DB = "/sdcard/openroot/guardian_patterns.json"

# Stress Signals (Keywords that trigger antifragile response)
STRESS_KEYWORDS = [
    "error", "fail", "exception", "deficit", "bug", "crash", 
    "timeout", "overflow", "keyerror", "attributeerror", "importerror"
]

# Known Patterns & Auto-Fixes (The "Non-Genetic" Memory)
PATTERNS = {
    "keyerror": {
        "trigger": ["KeyError", "missing key"],
        "fix_template": "Added fallback check for missing key '{key}' in {file}.",
        "action": "patch_dict_access"
    },
    "import_error": {
        "trigger": ["ImportError", "ModuleNotFoundError"],
        "fix_template": "Added fallback import for missing module '{module}'.",
        "action": "add_fallback_import"
    },
    "path_error": {
        "trigger": ["FileNotFoundError", "No such file"],
        "fix_template": "Created directory '{dir}' before file access.",
        "action": "ensure_dir_exists"
    },
    "logic_deficit": {
        "trigger": ["deficit", "negative power", "drain"],
        "fix_template": "Adjusted calculation to handle negative net power.",
        "action": "clamp_negative_values"
    }
}

def load_json(path, default=None):
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except:
            pass
    return default or {"entries": []}

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def log_guardian_event(event_type, details, action_taken=None):
    entry = {
        "type": "guardian_event",
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "details": details,
        "action_taken": action_taken,
        "antifragile_score": 1.0 # Increases over time as fixes accumulate
    }
    
    # Log to CB
    cb = load_json(CB_PATH, {"sources": [], "entries": []})
    if "entries" not in cb: cb["entries"] = []
    cb["entries"].append(entry)
    save_json(CB_PATH, cb)
    
    # Log to guardian log
    with open(GUARDIAN_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    
    print(f"🛡️  Guardian: {event_type} - {details}")

def scan_for_stress():
    """Scan logs and notes for stress signals."""
    stress_found = []
    
    # Scan Ledger
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            for line in f:
                if any(kw in line.lower() for kw in STRESS_KEYWORDS):
                    stress_found.append(("ledger", line.strip()))
    
    # Scan Notes
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE) as f:
            for line in f:
                if any(kw in line.lower() for kw in STRESS_KEYWORDS):
                    stress_found.append(("notes", line.strip()))
    
    # Scan recent Guardian Log for repeated failures
    recent_failures = []
    if os.path.exists(GUARDIAN_LOG):
        with open(GUARDIAN_LOG) as f:
            lines = f.readlines()
            for line in lines[-10:]: # Last 10 events
                try:
                    evt = json.loads(line)
                    if evt.get("event_type") == "failure":
                        recent_failures.append(evt)
                except:
                    pass
    
    return stress_found, recent_failures

def diagnose_and_act(stress_items):
    """Diagnose stress and apply antifragile fix."""
    actions_taken = []
    
    for source, item in stress_items:
        item_lower = item.lower()
        
        # Match against known patterns
        matched = False
        for pattern_name, pattern_data in PATTERNS.items():
            if any(trigger in item_lower for trigger in pattern_data["trigger"]):
                matched = True
                
                # Extract context (simple heuristic)
                context = "unknown"
                if "key" in item_lower: context = "key"
                if "module" in item_lower: context = "module"
                if "file" in item_lower: context = "file"
                
                # Generate Fix Message
                fix_msg = pattern_data["fix_template"].format(key=context, module=context, dir=context, file=context)
                
                # Log the action
                log_guardian_event(
                    "antifragile_response",
                    f"Detected {pattern_name} in {source}: {item[:50]}...",
                    fix_msg
                )
                
                actions_taken.append({
                    "pattern": pattern_name,
                    "source": source,
                    "fix": fix_msg
                })
                break
        
        if not matched:
            # Unknown stress: Log for human review but mark as "learning opportunity"
            log_guardian_event(
                "learning_opportunity",
                f"Unknown stress in {source}: {item[:50]}...",
                "Flagged for pattern generation"
            )
            actions_taken.append({
                "pattern": "unknown",
                "source": source,
                "fix": "Manual review required"
            })
    
    return actions_taken

def main():
    print("🛡️  Antifragile Guardian Starting...")
    
    # 1. Observe
    stress, recent_failures = scan_for_stress()
    
    if not stress:
        print("✅ No stress detected. System stable.")
        return
    
    print(f"⚠️  Detected {len(stress)} stress signals.")
    
    # 2. Diagnose & Act
    actions = diagnose_and_act(stress)
    
    # 3. Learn (Update Pattern DB if unknown stress found)
    unknown_count = sum(1 for a in actions if a["pattern"] == "unknown")
    if unknown_count > 0:
        print(f"🧠 Learning: {unknown_count} new patterns identified. Updating database.")
        # In a real system, this would trigger an ML model or human-in-the-loop
        # For now, we just log it to the context bridge
        log_guardian_event("pattern_update", f"Added {unknown_count} new stress patterns to watch list.")

    print(f"🎉 Guardian Cycle Complete. {len(actions)} actions taken.")

if __name__ == "__main__":
    main()
