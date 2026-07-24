#!/data/data/com.termux/files/usr/bin/python3
import json
import os

IMMORTAL = "/sdcard/openroot/context_bridge/immortal_context.json"
LIST_FILE = "/sdcard/openroot/tasks/parasitic_delete_list.txt"

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
