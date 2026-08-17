#!/data/data/com.termux/files/usr/bin/python3
"""
OpenRoot Session Snapshot
=========================
Captures full system state for context transfer between chat windows.
Run this before leaving a session or after making changes.

Usage: python3 snapshot.py
Output: os.environ.get("OPENROOT_HOME", "/sdcard/openroot/")session_snapshot.json
"""
import os, sys, json, subprocess, hashlib
from datetime import datetime
from pathlib import Path

BASE = Path("/data/data/com.termux/files/home/une")
CB = "os.environ.get("OPENROOT_HOME", "/sdcard/openroot/")context_bridge/immortal_context_merged.json"
SNAPSHOT_PATH = "os.environ.get("OPENROOT_HOME", "/sdcard/openroot/")session_snapshot.json"

def run(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return r.stdout.strip()
    except:
        return ""

def file_hashes(directory, extensions=(".py", ".sh")):
    """Hash every .py and .sh file so we can detect changes."""
    hashes = {}
    for f in Path(directory).rglob("*"):
        if "__pycache__" in str(f) or ".git" in str(f) or "scaffold" in str(f):
            continue
        if f.suffix in extensions:
            try:
                h = hashlib.sha256(f.read_bytes()).hexdigest()[:16]
                rel = str(f.relative_to(directory))
                hashes[rel] = h
            except:
                pass
    return hashes

def load_cb():
    if os.path.exists(CB):
        try:
            with open(CB) as f:
                return json.load(f)
        except:
            pass
    return {"entries": []}

# Build snapshot
print("📸 Capturing session snapshot...")

cb = load_cb()
entries = cb.get("entries", [])

# Categorize entries
notes = [e for e in entries if e.get("type") == "note"]
pipeline_runs = [e for e in entries if e.get("type") == "pipeline_run"]
guardian_events = [e for e in entries if e.get("type") in ("guardian_event", "antifragile_heal", "learning_opportunity", "pattern_update")]

snapshot = {
    "snapshot_time": datetime.now().isoformat(),
    "device": "Samsung SM-A156U (Galaxy A15)",
    "environment": {
        "termux_python": run("python3 --version"),
        "git_branch": run("cd /data/data/com.termux/files/home/une && git branch --show-current"),
        "git_status": run("cd /data/data/com.termux/files/home/une && git status --porcelain"),
        "guardian_running": os.path.exists("/data/data/com.termux/files/home/une/.guardian_pid"),
    },
    "file_hashes": file_hashes(BASE),
    "context_bridge": {
        "total_entries": len(entries),
        "notes": [n.get("text", "") for n in notes[-20:]],
        "pipeline_count": len(pipeline_runs),
        "guardian_events": len(guardian_events),
        "recent_guardian": [{"type": g.get("event_type", g.get("type")), "details": g.get("details", "")[:80]} for g in guardian_events[-5:]],
    },
    "smoke_test": run("cd /data/data/com.termux/files/home/une && python3 tests/test_smoke.py 2>&1"),
    "pipeline_status": run("cd /data/data/com.termux/files/home/une && python3 core_atomic.py pipeline 2>&1")[-500:],
    "known_issues": [
        "bulk_migrate.py may have corrupted imports in some files",
        "core_atomic.py restored to clean v2.0",
        "guardian_v4.py runs passively via daemon",
        "rmh.py physics fixed in both aerocement copies",
        "structure_enforcer.py has ignore list for setup scripts",
    ],
    "resume_instructions": [
        "Read this file first to understand current state.",
        "Run: python3 tests/test_smoke.py (verify 5/5 pass)",
        "Run: python3 core_atomic.py pipeline (verify 100% eta)",
        "Check: cat os.environ.get("OPENROOT_HOME", "/sdcard/openroot/")notes.txt (for new ideas)",
        "Check: tail -10 os.environ.get("OPENROOT_HOME", "/sdcard/openroot/")guardian_log.jsonl (for auto-heals)",
        "Any file with broken imports: add the Dynamic Paths block from paths.py",
        "Do NOT use regex to fix paths — it corrupts Python syntax.",
    ],
}

with open(SNAPSHOT_PATH, "w") as f:
    json.dump(snapshot, f, indent=2)

print(f"✅ Snapshot saved: {SNAPSHOT_PATH}")
print(f"   Files hashed: {len(snapshot['file_hashes'])}")
print(f"   Context entries: {len(entries)}")
print(f"   Guardian running: {snapshot['environment']['guardian_running']}")
print("\n--- COPY THIS BLOCK FOR NEW CHAT ---")
import json as _json
print(_json.dumps(json.load(open(SNAPSHOT_PATH)), indent=2))
print("--- END OF BLOCK ---")
