#!/data/data/com.termux/files/usr/bin/python3
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
