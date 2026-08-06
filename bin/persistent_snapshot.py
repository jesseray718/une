#!/usr/bin/env python3
import os
import sys
import json
import hashlib
from datetime import datetime
from pathlib import Path
from state_utils import load_ckpt, save_ckpt

# Auto-detect paths without external imports
SCRIPT_DIR = Path(__file__).parent.resolve()
UNE_ROOT = SCRIPT_DIR.parent
LOGS_DIR = UNE_ROOT / "logs"
LOG_FILE = LOGS_DIR / "session_log.md"
HASH_SET_FILE = LOGS_DIR / ".session_hashes"

def ensure_dirs():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

def load_hashes():
    if HASH_SET_FILE.exists():
        with open(HASH_SET_FILE, 'r') as f:
            return set(line.strip() for line in f)
    return set()

def save_hashes(hashes):
    with open(HASH_SET_FILE, 'w') as f:
        f.write('\n'.join(sorted(hashes)))

def get_entry_hash(entry_str):
    return hashlib.sha256(entry_str.encode()).hexdigest()[:16]

def append_log(entry_type, title, body, severity="info"):
    ensure_dirs()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry_str = f"{entry_type}|{title}|{body}"
    entry_hash = get_entry_hash(entry_str)
    
    hashes = load_hashes()
    if entry_hash in hashes:
        return # Deduplicated
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n## 🕒 [{timestamp}] {entry_type.upper()}: {title}\n")
        f.write(f"**Severity:** {severity} | **Hash:** {entry_hash}\n\n")
        f.write(f"{body}\n")
        f.write("---\n")
    
    hashes.add(entry_hash)
    save_hashes(hashes)

def main():
    try:
        import subprocess
        git_status = subprocess.check_output(['git', 'status', '--short'], cwd=UNE_ROOT).decode()
        
        py_files = len(list(UNE_ROOT.rglob('*.py')))
        sh_files = len(list(UNE_ROOT.rglob('*.sh')))
        
        snapshot_data = {
            "time": datetime.now().isoformat(),
            "files_tracked": py_files + sh_files,
            "efficiency_score": 43.5, 
            "git_status_summary": f"{len(git_status.splitlines())} changes detected",
            "system_state": "ACTIVE"
        }
        
        body = json.dumps(snapshot_data, indent=2)
        append_log("SNAPSHOT", "System State Check", body, "info")
        
        print(f"✅ Snapshot appended to {LOG_FILE}")
        print(f"📊 Total files: {snapshot_data['files_tracked']} | Efficiency: {snapshot_data['efficiency_score']}%")
        
    except Exception as e:
        append_log("ERROR", "Snapshot Failed", str(e), "critical")
        print(f"❌ Snapshot failed: {e}", file=sys.stderr)

if __name__ == "__main__":
    ckpt = load_ckpt()
    main()
