#!/usr/bin/env python3
"""
import os
try:
    from paths import OPENROOT
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

Agape-aware file evaluator with lightweight semantic analysis.
Only runs higher-tier analysis when Υ > 0.
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime
from collections import Counter
from state_utils import load_ckpt, save_ckpt

UNE = Path.home() / "une" / "computational_flow"
SEED = Path(os.path.join(OPENROOT, "session_seeds/current_seed.json"))
BLACKBOARD = UNE / "knowledge_graph.json"
LOG = UNE / "logs" / "hyperfusion.log"

# Concepts we care about under the Agape–Prime law
POSITIVE_SIGNALS = [
    r"\bη\b", r"\beta\b", r"useful_joules", r"human_joules",
    r"physical.?yield", r"popw", r"proof.of.physical",
    r"agape", r"phi\b", r"φ", r"verified.?yield",
    r"tier\s*[0-4]", r"nanobot", r"blackboard",
    r"thermodynamic", r"sensor", r"ledger"
]

RISK_SIGNALS = [
    r"TODO", r"FIXME", r"HACK", r"XXX",
    r"hardcoded", r"password", r"api[_-]?key",
    r"eval\(", r"exec\(", r"os\.system",
    r"while\s+True", r"infinite"
]

def log(msg):
    ts = datetime.now().isoformat(timespec="seconds")
    line = f"[{ts}] EVAL: {msg}"
    print(line)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(line + "\n")

def measure_upsilon():
    count = 0
    if BLACKBOARD.exists():
        count += 1
    chunks = Path(os.path.join(OPENROOT, "context_chunks"))
    if chunks.exists():
        count += len(list(chunks.glob("paste_*.txt")))
    return min(count / 50.0, 1.0)

def allowed(tier, upsilon):
    if tier <= 0:
        return True
    return upsilon > 0.0

def analyze_content(text: str, path: str):
    """Lightweight semantic analysis"""
    text_lower = text.lower()
    lines = text.splitlines()

    pos_hits = []
    for pat in POSITIVE_SIGNALS:
        if re.search(pat, text_lower, re.I):
            pos_hits.append(pat)

    risk_hits = []
    for pat in RISK_SIGNALS:
        if re.search(pat, text, re.I):
            risk_hits.append(pat)

    # Simple structure signals
    has_docstring = bool(re.search(r'"""[\s\S]+?"""', text)) or bool(re.search(r"'''[\s\S]+?'''", text))
    has_main = "__main__" in text
    long_lines = sum(1 for l in lines if len(l) > 120)

    score = 0.0
    score += min(len(pos_hits) * 0.15, 0.6)
    score -= min(len(risk_hits) * 0.2, 0.5)
    if has_docstring:
        score += 0.1
    if has_main:
        score += 0.05
    score = max(0.0, min(1.0, score))

    suggestions = []
    if not pos_hits:
        suggestions.append("No clear Agape / η / PoPW signals found — consider mapping to physical yield")
    if risk_hits:
        suggestions.append(f"Risk patterns detected: {', '.join(risk_hits[:4])}")
    if long_lines > 5:
        suggestions.append(f"{long_lines} long lines (>120 chars) — consider refactoring")
    if not has_docstring and path.endswith(".py"):
        suggestions.append("Missing module/docstring — add purpose and Agape context")
    if score < 0.3:
        suggestions.append("Low alignment score — needs explicit yield mapping or cleanup")

    return {
        "positive_signals": pos_hits,
        "risk_signals": risk_hits,
        "has_docstring": has_docstring,
        "has_main": has_main,
        "long_lines": long_lines,
        "alignment_score": round(score, 3),
        "suggestions": suggestions or ["Looks reasonably aligned"]
    }

def evaluate_files(target_dir: Path):
    upsilon = measure_upsilon()
    log(f"Υ = {upsilon:.3f}")

    if not allowed(1, upsilon):
        log("Blocked by Agape gate – no evaluation performed")
        return

    log(f"Starting semantic evaluation of {target_dir}")

    results = []
    for f in sorted(target_dir.rglob("*")):
        if not f.is_file():
            continue
        if f.suffix not in {".py", ".sh", ".md", ".json"}:
            continue
        if f.stat().st_size > 800_000:  # skip huge files
            continue

        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            log(f"Could not read {f}: {e}")
            continue

        analysis = analyze_content(text, str(f))
        results.append({
            "path": str(f),
            "size": f.stat().st_size,
            "type": f.suffix,
            **analysis
        })

    # Sort by lowest alignment first (most in need of attention)
    results.sort(key=lambda x: x["alignment_score"])

    report = {
        "ts": datetime.now().isoformat(),
        "upsilon": upsilon,
        "files_scanned": len(results),
        "results": results[:40]
    }

    report_path = UNE / "logs" / "evaluation_report.json"
    report_path.write_text(json.dumps(report, indent=2))
    log(f"Report written → {report_path}")
    log(f"Scanned {len(results)} files")

    # Quick console summary
    low = [r for r in results if r["alignment_score"] < 0.4]
    log(f"Files needing attention: {len(low)}")

if __name__ == "__main__":
    ckpt = load_ckpt()
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "une"
    evaluate_files(target)
