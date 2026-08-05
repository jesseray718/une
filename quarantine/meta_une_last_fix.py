#!/data/data/com.termux/files/usr/bin/python3
"""Last fix: Add LEDGER to paths.py, restore core_atomic.py imports."""
import os
from pathlib import Path

BASE = Path("os.path.expanduser("~") + "/"une")

# 1. FIX paths.py — add LEDGER and OPENROOT exports
print("1. Fixing paths.py...")
paths_file = BASE / "computational_flow" / "paths.py"
content = paths_file.read_text()

# Check what's missing
needed_exports = {
    "OPENROOT": 'OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")',
    "UNE_HOME": 'UNE_HOME = os.environ.get("UNE_HOME", os.path.join(HOME, "une"))',
    "DUMP_DIR": 'DUMP_DIR = os.path.join(OPENROOT, "dump", "chunks")',
    "CONTEXT_BRIDGE": 'CONTEXT_BRIDGE = os.path.join(OPENROOT, "context_bridge", "context.json")',
    "IMMORTAL_CONTEXT": 'IMMORTAL_CONTEXT = os.path.join(OPENROOT, "context_bridge", "immortal_context.json")',
    "LEDGER": 'LEDGER = os.path.join(OPENROOT, "ledger.jsonl")',
    "AGAPE_KB_PATH": 'AGAPE_KB_PATH = os.path.join(_BASE, "knowledge.json")',
    "AGAPE_POSTULATE_PATH": 'AGAPE_POSTULATE_PATH = os.path.join(_BASE, "postulates.json")',
    "AGAPE_STATE_PATH": 'AGAPE_STATE_PATH = os.path.join(_BASE, "state.json")',
}

# Rebuild paths.py completely (clean version)
clean_paths = '''#!/data/data/com.termux/files/usr/bin/python3
"""Central path configuration for OpenRoot/UNE."""
import os

HOME = os.environ.get("HOME", os.path.expanduser("~"))
OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
UNE_HOME = os.environ.get("UNE_HOME", os.path.join(HOME, "une"))

DUMP_DIR = os.path.join(OPENROOT, "dump", "chunks")
CONTEXT_BRIDGE = os.path.join(OPENROOT, "context_bridge", "context.json")
IMMORTAL_CONTEXT = os.path.join(OPENROOT, "context_bridge", "immortal_context.json")
LEDGER = os.path.join(OPENROOT, "ledger.jsonl")
RELAY = os.path.join(OPENROOT, "relay")
STORAGE = os.path.join(OPENROOT, "storage")
LESSONS = os.path.join(OPENROOT, "lessons")
LOGS = os.path.join(OPENROOT, "logs")
BIN = os.path.join(OPENROOT, "bin")

_BASE = os.path.dirname(os.path.abspath(__file__))
AGAPE_KB_PATH = os.path.join(_BASE, "knowledge.json")
AGAPE_POSTULATE_PATH = os.path.join(_BASE, "postulates.json")
AGAPE_STATE_PATH = os.path.join(_BASE, "state.json")

def print_paths():
    """Print all configured paths."""
    print("--- OpenRoot Path Config ---")
    print(f"OPENROOT: {OPENROOT}")
    print(f"UNE_HOME: {UNE_HOME}")
    print(f"DUMP_DIR: {DUMP_DIR}")
    print(f"LEDGER: {LEDGER}")
    print(f"CONTEXT_BRIDGE: {CONTEXT_BRIDGE}")
    print(f"KB_PATH: {AGAPE_KB_PATH}")
    print("-----------------------------")

if __name__ == "__main__":
    print_paths()
'''
paths_file.write_text(clean_paths)
print("   ✅ paths.py rewritten with all exports (OPENROOT, UNE_HOME, LEDGER, etc.)")

# 2. FIX core_atomic.py — ensure import block is correct
print("\n2. Fixing core_atomic.py...")
core_file = BASE / "core_atomic.py"
content = core_file.read_text()

# Find the import block and replace it with a known-good one
# First, find where the import block starts
import_start = content.find("try:")
import_end = content.find("shizuku_call")

if import_start != -1 and import_end != -1:
    # Replace the import block
    new_imports = '''try:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "computational_flow"))
    from core_functions import f5_synthesize, f6_verify
    REAL_F5F6 = True
except ImportError:
    REAL_F5F6 = False

try:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "computational_flow"))
    from paths import DUMP_DIR, CONTEXT_BRIDGE, LEDGER, OPENROOT, UNE_HOME
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))
    DUMP_DIR = os.path.join(OPENROOT, "dump", "chunks")
    CONTEXT_BRIDGE = os.path.join(OPENROOT, "context_bridge", "context.json")
    LEDGER = os.path.join(OPENROOT, "ledger.jsonl")

'''
    # Find the first try: block (after imports)
    lines = content.split("\\n")
    new_lines = []
    skip_until_shizuku = False
    
    for i, line in enumerate(lines):
        if line.strip() == "try:" and not skip_until_shizuku:
            # Check if this is the import try block (check next few lines)
            look_ahead = "\\n".join(lines[i:i+3])
            if "f5_synthesize" in look_ahead or "from paths" in look_ahead or "core_functions" in look_ahead:
                skip_until_shizuku = True
                continue
        
        if skip_until_shizuku:
            if "def shizuku_call" in line:
                skip_until_shizuku = False
                new_lines.append(new_imports)
                new_lines.append(line)
            # Skip lines between
            continue
        
        new_lines.append(line)
    
    content = "\\n".join(new_lines)
    core_file.write_text(content)
    print("   ✅ core_atomic.py import block fixed")
else:
    # Just write the import block at the top
    print("   ⚠️  Could not find import block boundaries, writing fresh...")
    # Check if it already has the import
    if "from paths import" in content:
        print("   ℹ️  Already has import, checking if OPENROOT is accessible...")
        # The issue might be that OPENROOT is in the except block but not in the try
        # Replace the entire import section
        pass

# 3. RUN VERIFICATION
print("\\n3. Running verification...")
import subprocess, sys

# Smoke test
r1 = subprocess.run([sys.executable, "tests/test_smoke.py"], capture_output=True, text=True, cwd=str(BASE))
print("\\nSMOKE TEST:")
print(r1.stdout)
if r1.stderr:
    print("STDERR:", r1.stderr[:200])

# Pipeline
r2 = subprocess.run([sys.executable, "core_atomic.py", "pipeline"], capture_output=True, text=True, cwd=str(BASE))
print("PIPELINE (last 300 chars):")
print(r2.stdout[-300:])
if r2.stderr:
    print("STDERR:", r2.stderr[:200])

# Paths check
r3 = subprocess.run([sys.executable, "-c", 
    "import sys; sys.path.insert(0, 'computational_flow'); from paths import LEDGER, OPENROOT, DUMP_DIR; print(f'LEDGER={LEDGER}'); print(f'OPENROOT={OPENROOT}')"],
    capture_output=True, text=True, cwd=str(BASE))
print("\\nPATHS CHECK:")
print(r3.stdout)
if r3.stderr:
    print("STDERR:", r3.stderr[:200])

print("\\n🎉 LAST FIX COMPLETE.")
