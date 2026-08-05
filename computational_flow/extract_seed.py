#!/data/data/com.termux/files/usr/bin/python3
"""
import os
try:
    from paths import OPENROOT
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

extract_seed.py
Captures current session state: terminal log, context.json, git diff -> dense seed block.
Usage: python3 extract_seed.py --output=/path/to/seed.json
"""
import json, os, sys, argparse, subprocess, glob
from datetime import datetime

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='os.environ.get("OPENROOT_BASE", "/sdcard/openroot") + "/"session_seeds/current_seed.json')
    args = parser.parse_args()

    seed = {
        "timestamp": datetime.now().isoformat(),
        "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "context": {},
        "git_diff": "",
        "terminal_log_snippet": ""
    }

    # 1. Capture Context (if exists)
    ctx_path = os.path.join(OPENROOT, "context.json")
    if os.path.exists(ctx_path):
        try:
            with open(ctx_path, 'r') as f:
                seed["context"] = json.load(f)
        except:
            seed["context"] = {"error": "Could not parse context.json"}

    # 2. Capture Git Diff (changes made since last commit)
    try:
        result = subprocess.run(["git", "diff"], capture_output=True, text=True, cwd="os.path.expanduser("~") + "/"une")
        seed["git_diff"] = result.stdout[:5000] # Limit size
    except:
        seed["git_diff"] = "Git not initialized or error."

    # 3. Capture Terminal Log Snippet (last 50 lines if available)
    # Note: In Termux, we might not have direct access to the full log buffer, 
    # but we can look for a log file if you set one up.
    log_files = glob.glob(os.path.join(OPENROOT, "logs/*.log"))
    if log_files:
        latest_log = sorted(log_files)[-1]
        with open(latest_log, 'r') as f:
            lines = f.readlines()
            seed["terminal_log_snippet"] = "".join(lines[-50:])

    # Write Seed
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump(seed, f, indent=2)

    print(f"✓ Seed extracted to: {args.output}")
    print(f"  Size: {os.path.getsize(args.output)} bytes")
    print(f"  Context keys: {list(seed['context'].keys())[:5]}...")

if __name__ == "__main__":
    main()
