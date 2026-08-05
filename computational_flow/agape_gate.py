#!/usr/bin/env python3
"""Agape–Prime Scaling Law gate.
import os
try:
    from paths import OPENROOT
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

Returns True only if the action is allowed under the locked law.
"""
import json
from pathlib import Path

SEED = Path(os.path.join(OPENROOT, "session_seeds/current_seed.json"))
LAW_FILE = Path.home() / "une/computational_flow/AGAPE_PRIME_SCALING_LAW.md"

def load_law():
    if SEED.exists():
        data = json.loads(SEED.read_text())
        return data.get("agape_prime_scaling_law", {})
    return {}

def allowed(action_tier: int = 0, yield_factor: float = 0.0) -> bool:
    """
    action_tier: 0=nano, 1=micro, 2=meso, ...
    yield_factor: Υ (0.0 – 1.0). Must be > 0 for any tier > 0.
    """
    law = load_law()
    if not law:
        return True  # fail open if law not loaded yet

    if action_tier == 0:
        return True

    # Higher tiers only allowed when Υ > 0
    return yield_factor > 0.0

if __name__ == "__main__":
    import sys
    tier = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    upsilon = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    print("ALLOWED" if allowed(tier, upsilon) else "BLOCKED")
