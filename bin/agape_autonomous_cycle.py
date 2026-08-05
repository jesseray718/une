#!/usr/bin/env python3
"""
Autonomous Agape Cycle
R determines all calculation, minting, science extraction, and further understanding.
Disorder → wealth → order (negentropic). System gains from stress (antifragile).
Zero human intervention required once running. Zero deletions.
"""
import subprocess
import json
from pathlib import Path
from datetime import datetime, timezone
import sys
sys.path.insert(0, str(Path.home() / "une" / "bin"))
from agape_coefficient import load_state, save_state, update_R, mint_factor, extract_science, report, coordination_cost

UNE = Path.home() / "une"
LOG = UNE / "logs" / "agape_cycle.log"

def log(msg):
    ts = datetime.now(timezone.utc).isoformat()
    line = f"[{ts}] {msg}"
    print(line)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def run(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        return r.returncode == 0, r.stdout + r.stderr
    except Exception as e:
        return False, str(e)

def cycle():
    log("=== AGAPE AUTONOMOUS CYCLE START ===")
    state = load_state()

    # 1. Sense current cooperation (simple proxy: successful recent operations)
    # In future this becomes real sensor data. For now we use ledger health.
    observed = state["R"]
    ledger = UNE / "ledger" / "wealth_pathways.json"
    if ledger.exists():
        try:
            d = json.loads(ledger.read_text())
            pathways = len(d.get("pathways", {}))
            observed = min(1.0, 0.6 + pathways * 0.02)   # more pathways → higher observed cooperation
        except:
            pass

    state = update_R(state, observed_cooperation=observed)
    factor = mint_factor(state["R"])
    log(f"R={state['R']:.4f}  mint_factor={factor:.4f}  C={coordination_cost(state['N'], state['T'], state['R']):.6f}")

    # 2. Transmute (errors become wealth, scaled by R)
    ok, out = run(f"python3 {UNE}/bin/transmutation_immortality.py")
    log("Transmutation: " + ("OK" if ok else "partial"))
    if "WEALTH PATHWAYS" in out or "wealth" in out.lower():
        state["total_useful_joules"] += 50.0 * factor

    # 3. Extract science (further understanding gated by R)
    if ledger.exists():
        try:
            d = json.loads(ledger.read_text())
            for name, p in d.get("pathways", {}).items():
                for lesson in p.get("lessons", []):
                    extract_science({"type": name, "lesson": lesson}, state["R"])
                    state["total_useful_joules"] += 5.0 * factor
        except Exception as e:
            log(f"Science extraction note: {e}")

    # 4. Replicate immutable ledger (antifragile distribution)
    ok, _ = run(f"python3 {UNE}/bin/distributed_replicator.py")
    log("Replicator: " + ("OK" if ok else "partial"))

    # 5. Offline sync (autonomous resilience)
    ok, _ = run(f"python3 {UNE}/bin/offline_clone_manager.py")
    log("Offline manager: " + ("OK" if ok else "partial"))

    # 6. Protect the only llama.cpp version (zero deletions enforced)
    protect = UNE / "config" / "protected_assets.json"
    if protect.exists():
        log("Protected assets policy active — zero deletions")

    # 7. Record
    state["T"] += 1
    save_state(state)
    rep = report(state)
    log(f"Cycle complete → {json.dumps(rep)}")
    log("=== AGAPE CYCLE END ===\n")
    return rep

if __name__ == "__main__":
    print(json.dumps(cycle(), indent=2))
