#!/usr/bin/env python3
"""META AUDIT — Engine inspects itself for problems."""
import json, os, ast, hashlib, time
from pathlib import Path
from collections import defaultdict
from state_utils import load_ckpt, save_ckpt

ROOT = Path("$(pwd)/une")
REPORT = Path("os.environ.get("OPENROOT_HOME", "/sdcard/openroot/")agape_kb/audit_report.json")

def audit_syntax():
    findings = []
    for f in ROOT.rglob("*.py"):
        if ".git" in str(f) or "__pycache__" in str(f):
            continue
        try:
            ast.parse(f.read_text())
        except SyntaxError as e:
            findings.append({"severity":"critical","file":str(f.relative_to(ROOT)),"issue":"syntax_error","detail":str(e),"fix":"python3 -m py_compile "+str(f)})
    return findings

def audit_duplicates():
    findings = []
    hashes = defaultdict(list)
    for f in ROOT.rglob("*"):
        if f.is_file() and ".git" not in str(f) and "__pycache__" not in str(f):
            try: hashes[hashlib.md5(f.read_bytes()).hexdigest()].append(str(f.relative_to(ROOT)))
            except: pass
    for h, files in hashes.items():
        if len(files) > 1:
            findings.append({"severity":"warning","files":files,"issue":"duplicate_content","detail":str(len(files))+" identical files","fix":"Keep one, delete rest"})
    return findings

def audit_dead():
    findings = []
    for f in ROOT.rglob("*"):
        if f.is_file() and f.suffix in [".bak",".broken",".save",".old",".orig"]:
            findings.append({"severity":"info","file":str(f.relative_to(ROOT)),"issue":"dead_file","detail":"Stale file","fix":"rm "+str(f)})
    return findings

def audit_bloat():
    findings = []
    counts = defaultdict(int)
    for f in ROOT.rglob("*"):
        if f.is_file() and ".git" not in str(f) and "__pycache__" not in str(f):
            counts[str(f.parent.relative_to(ROOT))] += 1
    for d, c in sorted(counts.items(), key=lambda x: -x[1]):
        if c > 20:
            findings.append({"severity":"warning","directory":d,"issue":"dir_bloat","detail":str(c)+" files","fix":"Split into subdirs"})
    return findings

def audit_stamps():
    findings = []
    log = Path("os.environ.get("OPENROOT_HOME", "/sdcard/openroot/")context_bridge/progress_log.jsonl")
    if not log.exists():
        findings.append({"severity":"warning","issue":"no_progress_log","detail":"Missing","fix":"Run stamp_context.py"})
    elif len(log.read_text().strip().split("\n")) < 5:
        findings.append({"severity":"info","issue":"low_stamps","detail":"Few entries","fix":"Run more cycles"})
    return findings

def run():
    findings = audit_syntax() + audit_duplicates() + audit_dead() + audit_bloat() + audit_stamps()
    c = sum(1 for f in findings if f.get("severity")=="critical")
    w = sum(1 for f in findings if f.get("severity")=="warning")
    i = sum(1 for f in findings if f.get("severity")=="info")
    report = {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%S"),"findings":findings,"summary":{"total":len(findings),"critical":c,"warnings":w,"info":i,"health":max(0,100-c*25-w*10-i*2)}}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2))
    return report

if __name__ == "__main__":
    ckpt = load_ckpt()
    r = run()
    s = r["summary"]
    print("META AUDIT | Health: " + str(s["health"]) + "/100 | Critical:" + str(s["critical"]) + " Warn:" + str(s["warnings"]) + " Info:" + str(s["info"]))
    for f in r["findings"]:
        print("[" + f.get("severity","?").upper() + "] " + f.get("issue","?") + ": " + f.get("detail",""))
