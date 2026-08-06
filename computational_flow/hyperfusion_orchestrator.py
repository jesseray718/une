#!/usr/bin/env python3
"""
import os
try:
    from paths import OPENROOT
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

Hyperfusion Orchestrator
========================
Agape–Prime Scaling Law + Blackboard + Tiered Swarm

Purpose:
  Continuous low-intensity background service that keeps the
  knowledge blackboard alive and enforces the Agape–Prime Scaling Law.

  Tier 0 work always runs.
  Tier 1+ work is gated by verified yield factor (Υ > 0).

  This is the operational expression of Agape:
  higher-tier influence may increase only when measurable
  physical or knowledge yield exists for the agents under its care.

  η = useful_joules / human_joules remains the only scoring language.
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime
from state_utils import load_ckpt, save_ckpt

# === Paths ===
HOME = Path.home()
UNE = HOME / "une" / "computational_flow"
SEED = Path(os.path.join(OPENROOT, "session_seeds/current_seed.json"))
BLACKBOARD = UNE / "knowledge_graph.json"
CHUNKS = Path(os.path.join(OPENROOT, "context_chunks"))
LOG = UNE / "logs" / "hyperfusion.log"

LOG.parent.mkdir(parents=True, exist_ok=True)

def log(msg: str) -> None:
    ts = datetime.now().isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line)
    with LOG.open("a") as f:
        f.write(line + "\n")

def load_json(path: Path, default=None):
    if default is None:
        default = {}
    try:
        if path.exists():
            return json.loads(path.read_text())
    except Exception as e:
        log(f"WARNING: could not load {path}: {e}")
    return default

def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2))

def load_law() -> dict:
    """Load the locked Agape–Prime Scaling Law from the current seed."""
    seed = load_json(SEED)
    return seed.get("agape_prime_scaling_law", {})

def agape_allowed(tier: int, upsilon: float = 0.0) -> bool:
    """
    Core gate from the Agape–Prime Scaling Law.
    Tier 0 is always allowed.
    Higher tiers require Υ > 0 (verified yield).
    """
    if tier <= 0:
        return True
    return upsilon > 0.0

def measure_simple_yield() -> float:
    """
    Cheap Tier-0 yield signal based on presence of knowledge artifacts.
    Returns Υ in the range 0.0 – 1.0.
    """
    count = 0
    if BLACKBOARD.exists():
        count += 1
    if CHUNKS.exists():
        count += len(list(CHUNKS.glob("paste_*.txt")))
    return min(count / 50.0, 1.0)

def tier0_work() -> None:
    """Nano work – always allowed. Heartbeat + blackboard refresh."""
    bb = load_json(BLACKBOARD, {"nodes": [], "last_hyperfusion": None})
    bb["last_hyperfusion"] = datetime.now().isoformat()
    bb["orchestrator"] = "hyperfusion_v1"
    bb["agape_prime_active"] = True
    save_json(BLACKBOARD, bb)
    log("Tier 0: blackboard heartbeat written (Agape law active)")

def tier1_work(upsilon: float) -> None:
    """Micro work – only if Υ > 0 under Agape–Prime constraint."""
    if not agape_allowed(1, upsilon):
        log("Tier 1: blocked by Agape gate (Υ = 0)")
        return
    log(f"Tier 1: allowed (Υ = {upsilon:.3f}) – scanning knowledge chunks")
    if CHUNKS.exists():
        files = sorted(CHUNKS.glob("paste_*.txt"))[:5]
        log(f"Tier 1: observed {len(files)} recent chunks")

def run_loop() -> None:
    log("=== Hyperfusion Orchestrator started ===")
    log("Agape–Prime Scaling Law enforcement active")
    log("η = useful_joules / human_joules is the only scoring language")

    law = load_law()
    if law:
        log(f"Law loaded – branching factor {law.get('tier_branching_factor', 7)}")
    else:
        log("WARNING: Agape–Prime law not found in seed – running in fail-open mode")

    while True:
        try:
            upsilon = measure_simple_yield()
            log(f"Current Υ (verified yield factor) = {upsilon:.3f}")

            # Tier 0 always runs
            tier0_work()

            # Tier 1 only when real yield exists
            tier1_work(upsilon)

            # Tiers 2–4 remain structurally ready but dormant
            # until stronger physical/knowledge yield is measured.

            time.sleep(90)  # gentle on battery and thermal load

        except KeyboardInterrupt:
            log("Orchestrator stopped by user")
            break
        except Exception as e:
            log(f"ERROR in loop: {e}")
            time.sleep(30)

if __name__ == "__main__":
    ckpt = load_ckpt()
    run_loop()
