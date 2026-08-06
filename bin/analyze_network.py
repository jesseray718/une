#!/usr/bin/env python3
"""Offline analysis of the interconnected UNE / Agape network."""
import json
from pathlib import Path
from datetime import datetime, timezone
from state_utils import load_ckpt, save_ckpt

UNE = Path.home() / "une"
META = UNE / "meta_hub"
out = UNE / "analysis" / "network_snapshot.json"

def safe_json(p):
    try:
        return json.loads(p.read_text()) if p.exists() else {}
    except Exception:
        return {}

R = safe_json(UNE / "config" / "agape_state.json").get("R", None)
ledger = safe_json(UNE / "ledger" / "wealth_pathways.json")
modules = list((UNE / "modules").glob("*.json")) if (UNE / "modules").exists() else []
science_lines = 0
sp = UNE / "science" / "synergy_studies.jsonl"
if sp.exists():
    science_lines = sum(1 for _ in open(sp))

repos = []
if META.exists():
    for r in sorted(META.iterdir()):
        if r.is_dir() and (r / ".git").exists():
            has_core = (r / "AGAPE_OFFLINE_CORE.json").exists()
            has_proposal = (r / "MERGE_PROPOSAL_AGAPE.md").exists()
            repos.append({
                "name": r.name,
                "has_agape_core": has_core,
                "has_merge_proposal": has_proposal
            })

snapshot = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "R": R,
    "repos_total": len(repos),
    "repos_with_core": sum(1 for x in repos if x["has_agape_core"]),
    "repos_with_proposal": sum(1 for x in repos if x["has_merge_proposal"]),
    "modules": len(modules),
    "module_names": [m.stem for m in modules],
    "science_extracts": science_lines,
    "pathways": len(ledger.get("pathways", {})),
    "total_wealth_minted": ledger.get("total_wealth_minted", 0),
    "llama_cpp_protected": "/data/data/com.termux/files/home/backups/openroot_20260726_0134/sync-from-kai",
    "repos": repos
}

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(snapshot, indent=2))
print(json.dumps(snapshot, indent=2))
