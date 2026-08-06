#!/usr/bin/env python3
"""META META — Audits the auditor, tracks improvement over time."""
import json, time
from pathlib import Path
from state_utils import load_ckpt, save_ckpt

AUDIT = Path("os.environ.get("OPENROOT_HOME", "/sdcard/openroot/")agape_kb/audit_report.json")
META = Path("os.environ.get("OPENROOT_HOME", "/sdcard/openroot/")agape_kb/meta_meta_report.json")
HISTORY = Path("os.environ.get("OPENROOT_HOME", "/sdcard/openroot/")agape_kb/audit_history.jsonl")

def run():
    if not AUDIT.exists():
        print("No audit found. Run meta_audit.py first.")
        return
    audit = json.loads(AUDIT.read_text())
    findings = audit.get("findings", [])
    summary = audit.get("summary", {})
    score = summary.get("health", 0)
    meta_findings = []

    unactionable = [f for f in findings if "fix" not in f]
    if unactionable:
        meta_findings.append({"severity":"warning","issue":"unactionable","detail":str(len(unactionable))+" findings lack fix","fix":"Add fix to all findings"})

    if score == 100 and len(findings) > 0:
        meta_findings.append({"severity":"warning","issue":"miscalibration","detail":"Score 100 but "+str(len(findings))+" findings","fix":"Recalibrate"})

    entry = {"timestamp":audit.get("timestamp",""),"health":score,"critical":summary.get("critical",0),"warnings":summary.get("warnings",0),"total":summary.get("total",0)}
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY, "a") as f:
        f.write(json.dumps(entry) + "\n")

    history = []
    if HISTORY.exists():
        for line in HISTORY.read_text().strip().split("\n"):
            try: history.append(json.loads(line))
            except: pass

    if len(history) >= 3:
        scores = [h["health"] for h in history[-3:]]
        if scores[0] > scores[-1]:
            meta_findings.append({"severity":"critical","issue":"declining","detail":" -> ".join(str(s) for s in scores),"fix":"Apply audit fixes"})
        elif scores[0] < scores[-1]:
            meta_findings.append({"severity":"info","issue":"improving","detail":" -> ".join(str(s) for s in scores),"fix":"Continue cycle"})

    report = {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%S"),"meta_findings":meta_findings,"history_count":len(history),"latest_score":score,"trend":[h["health"] for h in history[-5:]]}
    META.write_text(json.dumps(report, indent=2))

    print("META-META | Score:" + str(score) + " | History:" + str(len(history)) + " entries")
    if history:
        print("Trend: " + " -> ".join(str(s) for s in report["trend"]))
    for f in meta_findings:
        print("[" + f["severity"].upper() + "] " + f["issue"] + ": " + f["detail"])

if __name__ == "__main__":
    ckpt = load_ckpt()
    run()
