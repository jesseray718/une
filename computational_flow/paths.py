#!/data/data/com.termux/files/usr/bin/python3
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
