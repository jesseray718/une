"""Guardian integration: scan for errors, report to checkpoint, learn from failures."""
import json, os, sys, subprocess
from pathlib import Path
from datetime import datetime, timezone
from state_utils import load_ckpt, save_ckpt, stamp, append_lesson

UNE = Path(os.environ.get("UNE_DIR", str(Path.home() / "une")))
LOG_DIR = UNE / "logs"

STRESS_PATTERNS = [
    "Traceback", "Error", "Exception", "FAILED", "CRITICAL",
    "FileNotFoundError", "PermissionError", "SyntaxError",
    "KeyError", "NameError", "AttributeError"
]

def scan_logs():
    """Scan all log files for stress signals."""
    findings = []
    if not LOG_DIR.exists():
        return findings
    for log_file in LOG_DIR.glob("*.log"):
        try:
            content = log_file.read_text(errors="replace")
            lines = content.split("\n")
            for i, line in enumerate(lines):
                for pattern in STRESS_PATTERNS:
                    if pattern in line:
                        findings.append({
                            "file": log_file.name,
                            "line": i + 1,
                            "pattern": pattern,
                            "text": line.strip()[:200],
                            "ts": stamp()
                        })
                        break
        except Exception:
            continue
    return findings

def scan_py_syntax():
    """Quick syntax check on all .py files."""
    issues = []
    for py in sorted(UNE.glob("*.py")):
        if py.name == "state_utils.py":
            continue
        try:
            result = subprocess.run(
                ["python3", "-c", f"compile(open('{py}').read(), '{py}', 'exec')"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode != 0:
                issues.append({
                    "file": py.name,
                    "error": result.stderr.strip()[:300],
                    "ts": stamp()
                })
        except Exception:
            continue
    return issues

def main():
    state = load_ckpt()

    log_findings = scan_logs()
    syntax_issues = scan_py_syntax()

    total_stress = len(log_findings) + len(syntax_issues)

    # Update checkpoint
    state["guardian_scan_ts"] = stamp()
    state["guardian_log_signals"] = len(log_findings)
    state["guardian_syntax_errors"] = len(syntax_issues)
    state["last_error"] = syntax_issues[0]["error"][:100] if syntax_issues else None

    # Record lessons
    for finding in log_findings[:5]:  # cap to prevent flood
        append_lesson(f"STRESS: {finding['file']}:{finding['line']} {finding['pattern']}", "warning")
    for issue in syntax_issues[:5]:
        append_lesson(f"SYNTAX: {issue['file']} — {issue['error'][:100]}", "critical")

    save_ckpt(state)

    print(f"[GUARDIAN] log_signals={len(log_findings)} syntax_errors={len(syntax_issues)} "
          f"total_stress={total_stress}")
    if syntax_issues:
        for iss in syntax_issues:
            print(f"  ❌ {iss['file']}: {iss['error'][:80]}")
    else:
        print("  ✅ All .py files pass syntax check")

if __name__ == "__main__":
    main()
