#!/data/data/com.termux/files/usr/bin/python3
"""Smoke test for OpenRoot Atomic Core."""
import sys
import os

# CRITICAL: Add the PARENT directory (une/) to path so state_utils is found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state_utils import load_ckpt, save_ckpt

def test_load():
    ckpt = load_ckpt()
    assert 'cycle' in ckpt, "Checkpoint missing 'cycle'"
    print(f"✅ Load OK: Cycle {ckpt['cycle']}")

def test_save():
    import tempfile
    tmp = os.path.join(tempfile.mkdtemp(), 'test_ckpt.json')
    data = {'test': True, 'val': 1}
    save_ckpt(data, path=tmp)
    loaded = load_ckpt(path=tmp)
    assert loaded.get('test') == True, "Save/Load mismatch"
    print("✅ Save/Load OK (temp path, real checkpoint untouched)")

def test_merkle():
    from state_utils import calc_merkle
    h = calc_merkle(['test'])
    assert len(h) == 64, "Invalid merkle hash length"
    print(f"✅ Merkle OK: {h[:8]}...")

if __name__ == "__main__":
    print("Running Smoke Tests...")
    test_load()
    test_save()
    test_merkle()
    print("\n🎉 ALL TESTS PASSED")
