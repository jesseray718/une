#!/data/data/com.termux/files/usr/bin/python3
import sys, os, importlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "computational_flow"))

def test_imports():
    """Verify all modules import without crash."""
    modules = ["core_atomic", "absorber", "universical_primes", "paths", "core_functions"]
    # Also test structure_enforcer import (it is in computational_flow)
    extra_tests = [("structure_enforcer", "computational_flow")]
    passed, failed = 0, 0
    print("\n--- SMOKE TEST ---")
    for mod in modules:
        try:
            importlib.import_module(mod)
            print(f"  OK   {mod}")
            passed += 1
        except Exception as e:
            print(f"  FAIL {mod}: {str(e)[:60]}")
            failed += 1
    print(f"--- {passed} passed, {failed} failed ---\n")
    return failed == 0

if __name__ == "__main__":
    sys.exit(0 if test_imports() else 1)
