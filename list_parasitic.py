#!/data/data/com.termux/files/usr/bin/python3
import json

IMMORTAL = "/sdcard/openroot/context_bridge/immortal_context.json"
OUTPUT = "/sdcard/openroot/tasks/parasitic_delete_list.txt"

with open(IMMORTAL, 'r') as f:
    data = json.load(f)

parasitic = [f["path"] for f in data["file_index"] if f["category"] == "PARASITIC_WASTE"]

print(f"Found {len(parasitic)} parasitic files.")
print(f"Writing to {OUTPUT}...")

with open(OUTPUT, 'w') as f:
    f.write("\n".join(parasitic))

print("Done. Review the list before deleting.")
print("First 10 candidates:")
for p in parasitic[:10]:
    print(f"  {p}")
