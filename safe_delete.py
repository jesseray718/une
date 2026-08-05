#!/data/data/com.termux/files/usr/bin/python3
import json
import os

try:
    from paths import OPENROOT
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

IMMORTAL = os.path.join(OPENROOT, "context_bridge/immortal_context.json")
LIST_FILE = os.path.join(OPENROOT, "tasks/parasitic_delete_list.txt")

# Load list
with open(LIST_FILE, 'r') as f:
    files_to_delete = [line.strip() for line in f if line.strip()]

print(f"=== SAFE DELETE SIMULATION ===")
print(f"Candidates: {len(files_to_delete)}")

total_size = 0
for path in files_to_delete:
    full_path = os.path.expanduser(path) if not path.startswith('/') else path
    if os.path.exists(full_path):
        size = os.path.getsize(full_path)
        total_size += size
        print(f"  [DRY RUN] Would delete: {path} ({size} bytes)")
    else:
        print(f"  [MISSING] Already gone: {path}")

print(f"\nTotal space to recover: {total_size / 1024 / 1024:.2f} MB")
print("\nTo EXECUTE deletion, run: python3 ~/une/safe_delete.py --execute")
