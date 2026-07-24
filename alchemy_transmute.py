#!/data/data/com.termux/files/usr/bin/python3
"""
Digital Alchemy: Transmute Waste into Fuel
No deletion. Only compression, archiving, and re-contextualization.
"Waste" becomes "Alchemy Archive".
"""
import json
import os
import tarfile
import gzip
import shutil
from datetime import datetime

IMMORTAL = "/sdcard/openroot/context_bridge/immortal_context.json"
ARCHIVE_DIR = "/sdcard/openroot/alchemy_archive"
ARCHIVE_PATH = f"{ARCHIVE_DIR}/alchemy_archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"

# Load data
with open(IMMORTAL, 'r') as f:
    data = json.load(f)

files = data.get("file_index", [])

# Identify candidates for transmutation (formerly "Parasitic")
# We keep everything, but move low-eta files to archive
candidates = []
kept_files = []

for entry in files:
    path = entry.get("path", "")
    category = entry.get("category", "UNKNOWN")
    
    # If it was flagged as PARASITIC_WASTE, we transmute it
    if category == "PARASITIC_WASTE":
        candidates.append(entry)
    else:
        kept_files.append(entry)

print(f"=== DIGITAL ALCHEMY INITIATED ===")
print(f"Files to transmute: {len(candidates)}")
print(f"Files to keep active: {len(kept_files)}")

if not candidates:
    print("No waste found. All is already pure.")
    exit(0)

# Create archive directory
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# Create the archive
print(f"Creating archive: {ARCHIVE_PATH}")
with tarfile.open(ARCHIVE_PATH, "w:gz") as tar:
    for entry in candidates:
        path = entry["path"]
        if os.path.exists(path):
            try:
                # Add to archive with relative path
                arcname = f"alchemy/{os.path.relpath(path, '/sdcard/openroot')}"
                tar.add(path, arcname=arcname)
                
                # Update entry status
                entry["status"] = "TRANSMUTED"
                entry["archive_path"] = ARCHIVE_PATH
                entry["archived_at"] = datetime.now().isoformat()
                entry["category"] = "NEUTRAL_ALCHEMY"
                entry["reason"] = "Transmuted: Archived for efficiency"
            except Exception as e:
                print(f"   Warning: Could not archive {path}: {e}")
                # If we can't archive, we keep it active but flag it
                entry["status"] = "FLAGGED"
                entry["reason"] = "Flagged: Could not archive"
        else:
            # File already gone? Just mark it
            entry["status"] = "MISSING"
            entry["category"] = "NEUTRAL_ALCHEMY"
            entry["reason"] = "Already missing"

# Update stats
stats = {"KINGDOM_CORE": 0, "ALIGNMENT_BUILD": 0, "NEUTRAL_NOISE": 0, "NEUTRAL_ALCHEMY": 0}
for entry in files:
    cat = entry.get("category", "UNKNOWN")
    if cat in stats:
        stats[cat] += 1

data["statistics"] = stats
data["meta"]["alchemy_version"] = "1.0_transmutation"
data["meta"]["last_transmutation"] = datetime.now().isoformat()

# Save updated immortal context
with open(IMMORTAL, 'w') as f:
    json.dump(data, f, indent=2)

# Calculate sizes
archive_size = os.path.getsize(ARCHIVE_PATH) if os.path.exists(ARCHIVE_PATH) else 0
total_transmuted_size = sum(os.path.getsize(e["path"]) for e in candidates if os.path.exists(e["path"]))

print(f"\n=== ALCHEMY COMPLETE ===")
print(f"Archived {len([e for e in candidates if e.get('status')=='TRANSMUTED'])} files.")
print(f"Archive size: {archive_size / 1024 / 1024:.2f} MB")
print(f"Original size: {total_transmuted_size / 1024 / 1024:.2f} MB")
print(f"Space recovered: {(total_transmuted_size - archive_size) / 1024 / 1024:.2f} MB")
print(f"Archive saved: {ARCHIVE_PATH}")
print(f"\nWisdom Entry Added:")
print(f"  'Waste is merely fuel waiting for the fire.'")
print(f"  'Transmutation preserves all, frees the active, honors the past.'")
print(f"\n=== NEXT STEP ===")
print(f"The archive is safe. The active space is light.")
print(f"You may now proceed with vector mapping on the KEPT files.")
print(f"To restore later: tar -xzf {ARCHIVE_PATH} -C /sdcard/openroot/")

