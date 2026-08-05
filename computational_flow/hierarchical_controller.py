#!/usr/bin/env python3
"""
import os
try:
    from paths import OPENROOT
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

Agape–Prime Hierarchical Controller
Tier 0: heartbeat
Tier 1: real evaluator (agape_evaluate logic)
Tier 2: cross-domain coordination placeholder
Tier 3: governance placeholder
"""

import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

HOME = Path.home()
UNE = HOME / "une" / "computational_flow"
SEED = Path(os.path.join(OPENROOT, "session_seeds/current_seed.json"))
BLACKBOARD = UNE / "knowledge_graph.json"
LOG = UNE / "logs" / "hierarchical_controller.log"
EVALUATOR = UNE / "agape_evaluate.py"

LOG.parent.mkdir(parents=True, exist_ok=True)

def log(msg):
    ts = datetime.now().isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line)
    with LOG.open("a") as f:
        f.write(line + "\n")

class Blackboard:
    def __init__(self, path):
        self.path = path
        self.data = self._load()

    def _load(self):
        if self.path.exists():
            try:
                return json.loads(self.path.read_text())
            except Exception:
                pass
        return {"nodes": [], "history": [], "yield_factor": 0.0, "last_eval": None}

    def save(self):
        self.path.write_text(json.dumps(self.data, indent=2))

    def get_yield_factor(self):
        return float(self.data.get("yield_factor", 0.0))

    def set_yield_factor(self, value):
        self.data["yield_factor"] = max(0.0, min(1.0, value))
        self.save()

    def heartbeat(self):
        self.data["last_heartbeat"] = datetime.now().isoformat()
        self.data["agape_prime_active"] = True
        self.save()
        log("Tier 0: blackboard heartbeat")

    def record(self, result):
        self.data.setdefault("history", []).append({
            "ts": datetime.now().isoformat(),
            **result
        })
        self.data["history"] = self.data["history"][-40:]
        self.save()

class AgapeHierarchicalController:
    def __init__(self):
        self.bb = Blackboard(BLACKBOARD)
        self.current_option = None
        self.step_count = 0

    def measure_upsilon(self):
        return self.bb.get_yield_factor()

    def agape_gate(self, tier, upsilon):
        if tier <= 0:
            return True
        return upsilon > 0.0

    def select_option(self, state):
        upsilon = self.measure_upsilon()
        log(f"Selecting option | Υ = {upsilon:.3f}")

        if upsilon >= 0.55:
            return 3          # governance
        if upsilon >= 0.30:
            return 2          # cross-domain
        if upsilon >= 0.10:
            return 1          # evaluator
        return 0

    def tier0_policy(self, state):
        self.bb.heartbeat()
        current = self.bb.get_yield_factor()
        self.bb.set_yield_factor(min(1.0, current + 0.03))
        return {"status": "ok", "tier": 0, "yield_delta": 0.03}

    def tier1_policy(self, state):
        """Real Tier 1: call the semantic evaluator"""
        log("Tier 1: running Agape semantic evaluator")
        try:
            result = subprocess.run(
                ["python3", str(EVALUATOR), str(HOME / "une")],
                capture_output=True, text=True, timeout=60
            )
            log("Tier 1: evaluator finished")
            if result.returncode == 0:
                self.bb.data["last_eval"] = datetime.now().isoformat()
                self.bb.save()
                current = self.bb.get_yield_factor()
                self.bb.set_yield_factor(min(1.0, current + 0.08))
                return {"status": "ok", "tier": 1, "yield_delta": 0.08, "eval": "success"}
            else:
                log(f"Tier 1: evaluator error – {result.stderr[:120]}")
                return {"status": "error", "tier": 1, "yield_delta": 0.0}
        except Exception as e:
            log(f"Tier 1: exception – {e}")
            return {"status": "error", "tier": 1, "yield_delta": 0.0}

    def tier2_policy(self, state):
        """Cross-domain coordination placeholder"""
        log("Tier 2: cross-domain coordination (placeholder)")
        current = self.bb.get_yield_factor()
        self.bb.set_yield_factor(min(1.0, current + 0.05))
        return {"status": "ok", "tier": 2, "yield_delta": 0.05, "note": "coordination_placeholder"}

    def tier3_policy(self, state):
        """Governance placeholder – long-horizon / Agape oversight"""
        log("Tier 3: governance placeholder – reviewing yield history under Agape constraint")
        history = self.bb.data.get("history", [])[-8:]
        log(f"Tier 3: last {len(history)} actions reviewed")
        current = self.bb.get_yield_factor()
        self.bb.set_yield_factor(min(1.0, current + 0.04))
        return {"status": "ok", "tier": 3, "yield_delta": 0.04, "note": "governance_placeholder"}

    def execute_option(self, tier, state):
        upsilon = self.measure_upsilon()
        if not self.agape_gate(tier, upsilon):
            log(f"Tier {tier} blocked by Agape gate (Υ = {upsilon:.3f})")
            return {"status": "blocked_by_agape", "tier": tier}

        if tier == 0:
            return self.tier0_policy(state)
        elif tier == 1:
            return self.tier1_policy(state)
        elif tier == 2:
            return self.tier2_policy(state)
        elif tier == 3:
            return self.tier3_policy(state)
        else:
            return {"status": "not_implemented", "tier": tier}

    def termination(self, result):
        if result.get("status") in ("blocked_by_agape", "not_implemented", "error"):
            return True
        if result.get("yield_delta", 0) > 0:
            return True
        return False

    def step(self):
        state = {"step": self.step_count}
        self.step_count += 1

        if self.current_option is None:
            self.current_option = self.select_option(state)

        result = self.execute_option(self.current_option, state)
        self.bb.record(result)

        if self.termination(result):
            self.current_option = None

        return result

    def run(self, cycles=12, delay=4.0):
        log("=== Agape Hierarchical Controller started ===")
        log("Tier 1 now calls real evaluator | Tier 2 & 3 are governance placeholders")
        for i in range(cycles):
            result = self.step()
            log(f"Cycle {i+1}: {result}")
            time.sleep(delay)
        log("Controller finished")
        log(f"Final Υ = {self.measure_upsilon():.3f}")

if __name__ == "__main__":
    controller = AgapeHierarchicalController()
    controller.run(cycles=12, delay=4.0)
