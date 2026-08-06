#!/data/data/com.termux/files/usr/bin/python3
import os
from state_utils import load_ckpt, save_ckpt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMP_DIR = os.path.join(BASE_DIR, "computational_flow")
TEST_DIR = os.path.join(BASE_DIR, "tests")
os.makedirs(COMP_DIR, exist_ok=True)
os.makedirs(TEST_DIR, exist_ok=True)

# --- Write paths.py ---
with open(os.path.join(COMP_DIR, "paths.py"), "w") as f:
    f.write('''#!/data/data/com.termux/files/usr/bin/python3
import os
HOME = os.environ.get("HOME", os.path.expanduser("~"))
OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
UNE_HOME = os.environ.get("UNE_HOME", os.path.join(HOME, "une"))
_BASE = os.path.dirname(os.path.abspath(__file__))
AGAPE_KB_PATH = os.path.join(_BASE, "knowledge.json")
AGAPE_POSTULATE_PATH = os.path.join(_BASE, "postulates.json")
AGAPE_STATE_PATH = os.path.join(_BASE, "state.json")
DUMP_DIR = os.path.join(OPENROOT, "dump", "chunks")
CONTEXT_BRIDGE = os.path.join(OPENROOT, "context_bridge", "context.json")
IMMORTAL_CONTEXT = os.path.join(OPENROOT, "context_bridge", "immortal_context.json")
''')

# --- Write test_smoke.py ---
with open(os.path.join(TEST_DIR, "test_smoke.py"), "w") as f:
    f.write('''#!/data/data/com.termux/files/usr/bin/python3
import sys, os, importlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "computational_flow"))

def test_imports():
    modules = ["core_atomic", "absorber", "universical_primes", "paths"]
    passed, failed = 0, 0
    print("\\n--- SMOKE TEST ---")
    for mod in modules:
        try:
            importlib.import_module(mod)
            print(f"  OK   {mod}")
            passed += 1
        except Exception as e:
            print(f"  FAIL {mod}: {str(e)[:60]}")
            failed += 1
    print(f"--- {passed} passed, {failed} failed ---\\n")
    return failed == 0

if __name__ == "__main__":
    ckpt = load_ckpt()
    sys.exit(0 if test_imports() else 1)
''')

# --- Patch agape_engine.py (if not already patched) ---
engine = os.path.join(COMP_DIR, "agape_engine.py")
if os.path.exists(engine):
    with open(engine, "r") as f:
        src = f.read()
    if "from paths import" not in src:
        patch = """
# === DYNAMIC PATHS (auto-patched) ===
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from paths import AGAPE_KB_PATH, AGAPE_POSTULATE_PATH, AGAPE_STATE_PATH
    KNOWLEDGE_PATH = AGAPE_KB_PATH
    POSTULATE_PATH = AGAPE_POSTULATE_PATH
    STATE_PATH = AGAPE_STATE_PATH
except ImportError:
    _BASE = os.path.dirname(os.path.abspath(__file__))
    KNOWLEDGE_PATH = os.path.join(_BASE, "knowledge.json")
    POSTULATE_PATH = os.path.join(_BASE, "postulates.json")
    STATE_PATH = os.path.join(_BASE, "state.json")
# === END DYNAMIC PATHS ===
"""
        if "import os" in src:
            src = src.replace("import os", "import os\n" + patch, 1)
        else:
            src = patch + "\\n" + src
        with open(engine, "w") as f:
            f.write(src)
        print("Patched agape_engine.py")
    else:
        print("agape_engine.py already patched")

print("\\nDone. Now run:")
print("  python3 tests/test_smoke.py")
