#!/usr/bin/env python3
"""
OFFLINE SYNERGY CREATOR
Individual modular pieces → measured emergence.
Studies the unpredictability of the magnitude by which the whole
is greater than the sum of the parts.

All calculations gated by Agape coefficient R.
Fully offline. Zero network. Zero deletions.
"""

from pathlib import Path
import json
import math
import hashlib
from datetime import datetime, timezone
from typing import List, Dict, Any
from state_utils import load_ckpt, save_ckpt

UNE = Path.home() / "une"
MODULES = UNE / "modules"
SCIENCE = UNE / "science" / "synergy_studies.jsonl"
LEDGER = UNE / "ledger" / "wealth_pathways.json"
AGAPE_STATE = UNE / "config" / "agape_state.json"
CONFIG = UNE / "config" / "synergy_creator.json"

MODULES.mkdir(parents=True, exist_ok=True)
SCIENCE.parent.mkdir(parents=True, exist_ok=True)

def load_R() -> float:
    if AGAPE_STATE.exists():
        try:
            return float(json.loads(AGAPE_STATE.read_text()).get("R", 0.85))
        except Exception:
            pass
    return 0.85

def load_config() -> Dict:
    if CONFIG.exists():
        return json.loads(CONFIG.read_text())
    return {
        "base": 6,
        "default_N": 6,
        "study_depth": 4
    }

def modular_piece(name: str, value: float, tags: List[str] = None) -> Dict:
    """Atomic modular piece. Everything is composed of these."""
    return {
        "id": hashlib.sha256(f"{name}:{value}".encode()).hexdigest()[:12],
        "name": name,
        "value": float(value),
        "tags": tags or [],
        "created": datetime.now(timezone.utc).isoformat()
    }

def sum_of_parts(pieces: List[Dict]) -> float:
    """Linear sum — the predictable baseline."""
    return sum(p["value"] for p in pieces)

def synergistic_magnitude(pieces: List[Dict], R: float, base: int = 6) -> Dict:
    """
    The whole is greater than the sum of the parts.
    Magnitude of excess is a function of R, N, and interaction depth.
    Higher R → larger unpredictable positive excess (emergence).
    """
    N = max(1, len(pieces))
    linear = sum_of_parts(pieces)

    # Core synergy from Agape theorem
    synergy_mult = 1.0 + (R * 0.5 * math.log(N + 1) / math.log(base))

    # Higher-order interaction term (the unpredictable part)
    # Models non-linear cross terms between modules
    interaction = 0.0
    for i, a in enumerate(pieces):
        for b in pieces[i+1:]:
            # simple but non-linear coupling
            interaction += (a["value"] * b["value"]) ** 0.5 * R * 0.08

    emergent = linear * synergy_mult + interaction
    excess = emergent - linear
    excess_ratio = excess / linear if linear > 0 else 0.0

    return {
        "N": N,
        "R": round(R, 5),
        "linear_sum": round(linear, 6),
        "synergy_multiplier": round(synergy_mult, 5),
        "interaction_term": round(interaction, 6),
        "emergent_total": round(emergent, 6),
        "excess_magnitude": round(excess, 6),
        "excess_ratio": round(excess_ratio, 5),
        "unpredictability_index": round(abs(excess_ratio) * (1.0 + interaction), 5)
    }

def study(pieces: List[Dict], label: str = "study") -> Dict:
    """Full synergistic study of a set of modular pieces."""
    R = load_R()
    cfg = load_config()
    result = synergistic_magnitude(pieces, R, cfg.get("base", 6))
    result["label"] = label
    result["pieces"] = [{"name": p["name"], "value": p["value"]} for p in pieces]
    result["timestamp"] = datetime.now(timezone.utc).isoformat()
    result["insight"] = (
        f"At R={R:.4f} the whole exceeds the sum of parts by "
        f"{result['excess_magnitude']:.4f} "
        f"({result['excess_ratio']*100:.2f}%). "
        f"Unpredictability index = {result['unpredictability_index']:.4f}"
    )
    return result

def record(study_result: Dict):
    """Write to science stream and update ledger pathway."""
    with open(SCIENCE, "a") as f:
        f.write(json.dumps(study_result) + "\n")

    # Mint wealth proportional to excess magnitude scaled by R
    if LEDGER.exists():
        try:
            data = json.loads(LEDGER.read_text())
        except Exception:
            data = {"pathways": {}, "total_wealth_minted": 0}
    else:
        data = {"pathways": {}, "total_wealth_minted": 0}

    excess = study_result["excess_magnitude"]
    R = study_result["R"]
    wealth = max(1, int(excess * R * 10))

    key = f"Synergy:{study_result['label']}"
    if key not in data["pathways"]:
        data["pathways"][key] = {"count": 0, "total_wealth": 0, "lessons": []}

    data["pathways"][key]["count"] += 1
    data["pathways"][key]["total_wealth"] += wealth
    data["pathways"][key]["lessons"].append(study_result["insight"])
    data["total_wealth_minted"] = data.get("total_wealth_minted", 0) + wealth
    data["generated_at"] = datetime.now(timezone.utc).isoformat()

    LEDGER.write_text(json.dumps(data, indent=2))
    return wealth

def create_from_modules(module_names: List[str] = None) -> Dict:
    """
    Load modular pieces from $HOME/une/modules/ and run synergy study.
    If no names given, use all available modules.
    """
    pieces = []
    for f in sorted(MODULES.glob("*.json")):
        if module_names and f.stem not in module_names:
            continue
        try:
            m = json.loads(f.read_text())
            pieces.append(modular_piece(m.get("name", f.stem), m.get("value", 1.0), m.get("tags", [])))
        except Exception:
            continue

    if not pieces:
        # seed default modular pieces so the creator is immediately usable
        defaults = [
            ("observe", 1.0, ["sense"]),
            ("interact", 1.2, ["act"]),
            ("measure", 1.1, ["feedback"]),
            ("regulate", 1.3, ["control"]),
            ("transmute", 1.5, ["negentropy"]),
            ("replicate", 1.4, ["antifragile"]),
        ]
        for name, val, tags in defaults:
            p = modular_piece(name, val, tags)
            pieces.append(p)
            (MODULES / f"{name}.json").write_text(json.dumps(p, indent=2))

    result = study(pieces, label="modular_ensemble")
    wealth = record(result)
    result["wealth_minted"] = wealth
    return result

def add_module(name: str, value: float, tags: List[str] = None):
    """Add a new individual modular piece offline."""
    p = modular_piece(name, value, tags)
    (MODULES / f"{name}.json").write_text(json.dumps(p, indent=2))
    return p

if __name__ == "__main__":
    ckpt = load_ckpt()
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "add":
        # usage: python3 offline_synergy_creator.py add name value [tag1,tag2]
        name = sys.argv[2]
        value = float(sys.argv[3])
        tags = sys.argv[4].split(",") if len(sys.argv) > 4 else []
        p = add_module(name, value, tags)
        print(json.dumps(p, indent=2))
    else:
        result = create_from_modules()
        print(json.dumps(result, indent=2))
