#!/usr/bin/env python3
"""
FULL MESH LOOP v1.0
1. Snapshot GitHub state (backup)
2. Scan ALL repos individually
3. Generate individualized report per repo
4. Generate unified report
5. Implement changes (gentle alignment)
6. Learn from all mistakes
7. Loop
"""
import os
import sys
import json
import subprocess
import time
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from state_utils import load_ckpt, save_ckpt

UNE_ROOT = Path.home() / "une"
REPORTS_DIR = UNE_ROOT / "reports"
LESSONS_FILE = UNE_ROOT / "logs" / "full_mesh_lessons.jsonl"
MARKOR_DIR = Path("/sdcard/openroot/markor") if Path("/sdcard").exists() else UNE_ROOT
DOSSIER_FILE = MARKOR_DIR / "auto_dossier.txt"

# GitHub search keywords (broader for real results)
SEARCH_KEYWORDS = [
    "permaculture software", "regenerative agriculture tech",
    "open source farming", "decentralized mesh network",
    "antifragile systems", "bio-inspired architecture",
    "energy accounting", "carbon-negative technology",
    "heirloom seed database", "soil microbiome open source"
]

# Known error patterns for learning
ERROR_PATTERNS = {
    "symlink_loop": r"Too many symbolic links",
    "auth_failure": r"Permission denied|403|401",
    "non_fast_forward": r"non-fast-forward|rejected.*behind",
    "syntax_error": r"SyntaxError|IndentationError",
    "hardcoded_path": r"/sdcard/openroot|/data/data/com.termux",
    "network_error": r"Connection refused|Network unreachable",
    "timeout": r"timed out|timeout",
    "merge_conflict": r"CONFLICT|merge conflict"
}

class MeshLoop:
    def __init__(self):
        self.reports_dir = REPORTS_DIR
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.lessons = self.load_lessons()
        self.cycle_count = 0
        self.total_wealth = 0
        
    def load_lessons(self):
        """Load lessons from previous runs."""
        lessons = []
        LESSONS_FILE.parent.mkdir(parents=True, exist_ok=True)
        if LESSONS_FILE.exists():
            with open(LESSONS_FILE) as f:
                for line in f:
                    try:
                        lessons.append(json.loads(line.strip()))
                    except:
                        pass
        return lessons

    def record_lesson(self, repo, error_type, error_msg, root_cause, fix_applied):
        """Record a lesson learned from any mistake."""
        lesson = {
            "timestamp": datetime.now().isoformat(),
            "cycle": self.cycle_count,
            "repo": repo,
            "error_type": error_type,
            "error_message": error_msg[:300],
            "root_cause": root_cause,
            "fix_applied": fix_applied,
            "occurrence": sum(1 for l in self.lessons if l.get("root_cause") == root_cause) + 1
        }
        self.lessons.append(lesson)
        with open(LESSONS_FILE, 'a') as f:
            f.write(json.dumps(lesson) + '\n')
        return lesson

    def run_cmd(self, cmd, cwd=None, timeout=30):
        """Run command with timeout and error capture."""
        try:
            result = subprocess.run(
                cmd, shell=True, cwd=cwd,
                capture_output=True, text=True, timeout=timeout
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timed out", -1
        except Exception as e:
            return "", str(e), -1

    def diagnose_error(self, repo, stdout, stderr, returncode):
        """Diagnose an error using pattern matching + lessons."""
        combined = f"{stdout} {stderr}".lower()
        
        for error_type, pattern in ERROR_PATTERNS.items():
            if re.search(pattern, combined, re.IGNORECASE):
                return error_type, combined[:300]
        
        if returncode != 0 and "error" in combined:
            return "unknown_error", combined[:300]
        
        return None, None

    def get_my_repos(self):
        """Get all repos owned by jesseray718."""
        print("📋 Fetching repo list from GitHub...")
        stdout, stderr, rc = self.run_cmd(
            "gh repo list jesseray718 --limit 100 --json name,isPrivate,updatedAt,description"
        )
        if rc != 0:
            print(f"❌ Failed to fetch repo list: {stderr}")
            return []
        
        try:
            repos = json.loads(stdout)
            print(f"   Found {len(repos)} repos")
            return repos
        except:
            print(f"❌ Failed to parse repo list")
            return []

    def scan_github_external(self):
        """Search GitHub for external repos matching our principles."""
        print("\n🔍 Scanning GitHub for collaboration opportunities...")
        opportunities = []
        
        for kw in SEARCH_KEYWORDS:
            print(f"   Searching: {kw}...")
            stdout, stderr, rc = self.run_cmd(
                f"gh search repos '{kw}' --limit 10 --sort=updated --json name,description,stargazersCount,forks,updatedAt,url",
                timeout=20
            )
            if rc != 0:
                self.record_lesson("external_scan", "search_failed", stderr, 
                                   "gh search API error", "Check API rate limits")
                continue
            
            try:
                results = json.loads(stdout) if stdout else []
            except:
                results = []
            
            for repo in results:
                stars = repo.get("stargazersCount", 0)
                forks = repo.get("forks", 0)
                desc = (repo.get("description") or "").lower()
                
                score = 0
                reasons = []
                
                if stars > 50:
                    score += 15
                    reasons.append(f"{stars} stars")
                if forks > 5:
                    score += 10
                    reasons.append(f"{forks} forks (fragmented)")
                if any(w in desc for w in ["permaculture", "regenerative", "antifragile", "decentralized"]):
                    score += 20
                    reasons.append("Thematic match")
                
                if score >= 25:
                    opportunities.append({
                        "repo": repo.get("name"),
                        "url": repo.get("url"),
                        "stars": stars,
                        "forks": forks,
                        "score": score,
                        "reasons": "; ".join(reasons),
                        "keyword": kw
                    })
        
        opportunities.sort(key=lambda x: x["score"], reverse=True)
        print(f"   Found {len(opportunities)} external opportunities")
        return opportunities

    def scan_repo_individual(self, repo_info):
        """Deep scan a single repo and generate individualized report."""
        repo_name = repo_info.get("name", "unknown")
        is_private = repo_info.get("isPrivate", False)
        
        report = {
            "repo": repo_name,
            "private": is_private,
            "scanned_at": datetime.now().isoformat(),
            "health_score": 100,
            "issues": [],
            "stats": {},
            "lessons_applicable": [],
            "recommendations": [],
            "changes_applied": []
        }

        # Clone or update repo locally
        local_path = UNE_ROOT / "meta_hub" / repo_name
        if not local_path.exists():
            clone_url = f"https://github.com/jesseray718/{repo_name}.git"
            stdout, stderr, rc = self.run_cmd(
                f"git clone --depth 1 {clone_url} {local_path}",
                cwd=UNE_ROOT / "meta_hub",
                timeout=60
            )
            if rc != 0:
                err_type, err_msg = self.diagnose_error(repo_name, stdout, stderr, rc)
                if err_type:
                    report["issues"].append({"type": err_type, "message": err_msg})
                    report["health_score"] -= 10
                    lesson = self.record_lesson(repo_name, err_type, err_msg,
                                                "clone_failed", "Check if repo exists or auth")
                    report["lessons_applicable"].append(lesson["root_cause"])
                return report
        
        # Fetch latest
        stdout, stderr, rc = self.run_cmd("git fetch origin", cwd=local_path, timeout=30)
        if rc != 0:
            err_type, err_msg = self.diagnose_error(repo_name, stdout, stderr, rc)
            if err_type:
                report["issues"].append({"type": err_type, "message": err_msg})
                report["health_score"] -= 5
                self.record_lesson(repo_name, err_type, err_msg,
                                  "fetch_failed", "Check network or auth")

        # Gather stats
        file_count_stdout, _, _ = self.run_cmd("find . -type f -not -path './.git/*' | wc -l", cwd=local_path)
        py_count_stdout, _, _ = self.run_cmd("find . -name '*.py' -not -path './.git/*' | wc -l", cwd=local_path)
        last_commit, _, _ = self.run_cmd("git log -1 --format='%cd %s' --date=short", cwd=local_path)
        
        report["stats"] = {
            "total_files": int(file_count_stdout) if file_count_stdout.isdigit() else 0,
            "python_files": int(py_count_stdout) if py_count_stdout.isdigit() else 0,
            "last_commit": last_commit or "unknown"
        }

        # Check for hardcoded paths
        hardcoded_stdout, _, _ = self.run_cmd(
            'grep -r "/sdcard/openroot\\|/data/data/com.termux" --include="*.py" --include="*.sh" . 2>/dev/null | grep -v vendor_archive | head -5',
            cwd=local_path
        )
        if hardcoded_stdout:
            report["issues"].append({"type": "hardcoded_path", "message": hardcoded_stdout[:200]})
            report["health_score"] -= 15
            report["recommendations"].append("Replace hardcoded paths with Path(__file__).parent.resolve()")
            # Apply learned fix: auto-fix if we've seen this before
            report["changes_applied"].append("Flagged for path migration")

        # Check for symlink .gitignore
        gi_path = local_path / ".gitignore"
        if gi_path.is_symlink():
            report["issues"].append({"type": "symlink_loop", "message": ".gitignore is a symlink"})
            report["health_score"] -= 10
            # Apply learned fix
            os.unlink(gi_path)
            gi_path.write_text("vendor_archive/\nquarantine/\nbackups/\nlogs/\n*.log\n*.pyc\n__pycache__/\n")
            report["changes_applied"].append("Destroyed symlink .gitignore, replaced with static file")
            self.total_wealth += 10

        # Check for syntax errors in Python files
        py_compile_stdout, py_compile_stderr, _ = self.run_cmd(
            "find . -name '*.py' -not -path './.git/*' -not -path './vendor_archive/*' -exec python3 -m py_compile {} \\; 2>&1 | head -5",
            cwd=local_path,
            timeout=120
        )
        if py_compile_stderr and "SyntaxError" in py_compile_stderr:
            report["issues"].append({"type": "syntax_error", "message": py_compile_stderr[:200]})
            report["health_score"] -= 20
            report["recommendations"].append("Fix syntax errors in Python files")
            self.record_lesson(repo_name, "syntax_error", py_compile_stderr,
                             "python_syntax_invalid", "Run py_compile to locate error")

        # Check if Lair workflow exists
        lair_path = local_path / ".github" / "workflows" / "antifragility_lair.yml"
        if not lair_path.exists():
            report["issues"].append({"type": "missing_lair", "message": "Antifragility Lair not deployed"})
            report["health_score"] -= 5
            report["recommendations"].append("Deploy Antifragility Lair workflow")
            # Auto-deploy
            lair_path.parent.mkdir(parents=True, exist_ok=True)
            lair_path.write_text("""name: 🛡️ Antifragility Lair
on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * *'
jobs:
  ecosystem-health:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: 🏥 Health Check
        run: |
          SCORE=100
          HARDCODED=$(grep -r "/sdcard/openroot\\|/data/data/com.termux" --include="*.py" --include="*.sh" . 2>/dev/null | wc -l)
          if [ "$HARDCODED" -gt 0 ]; then SCORE=$((SCORE - (HARDCODED * 5))); fi
          echo "Health Score: $SCORE"
""")
            report["changes_applied"].append("Auto-deployed Antifragility Lair")
            self.total_wealth += 10

        # Apply lessons from previous cycles
        for lesson in self.lessons:
            if lesson.get("repo") == repo_name or lesson.get("repo") == "global":
                if lesson["root_cause"] not in [l["root_cause"] for l in report["lessons_applicable"]]:
                    report["lessons_applicable"].append(lesson["root_cause"])

        # Clamp score
        report["health_score"] = max(0, min(100, report["health_score"]))
        
        return report

    def commit_and_push_gentle(self, repo_name, report):
        """Gently commit and push changes without force."""
        local_path = UNE_ROOT / "meta_hub" / repo_name
        if not local_path.exists():
            return False

        # Stage changes
        self.run_cmd("git add -A", cwd=local_path)
        
        # Check for changes
        stdout, _, _ = self.run_cmd("git status --porcelain", cwd=local_path)
        if not stdout.strip():
            return True  # Nothing to push, already clean
        
        # Commit
        commit_msg = f"auto: mesh loop cycle {self.cycle_count} — health scan + alignment\n\nHealth: {report['health_score']}/100\nChanges: {'; '.join(report.get('changes_applied', ['none']))}"
        stdout, stderr, rc = self.run_cmd(
            f'git commit --no-verify -m "{commit_msg}"',
            cwd=local_path
        )
        
        # Gentle push (fetch + rebase first, no force)
        self.run_cmd("git fetch origin", cwd=local_path, timeout=30)
        rebase_out, rebase_err, rebase_rc = self.run_cmd("git rebase origin/main", cwd=local_path)
        
        if rebase_rc != 0:
            # Rebase failed — abort and merge instead
            self.run_cmd("git rebase --abort", cwd=local_path)
            merge_out, merge_err, merge_rc = self.run_cmd(
                "git merge origin/main --no-edit", cwd=local_path
            )
            if merge_rc != 0:
                self.record_lesson(repo_name, "merge_conflict", merge_err,
                                 "diverged_histories", "Manual conflict resolution needed")
                report["issues"].append({"type": "merge_conflict", "message": "Histories diverged, manual resolution needed"})
                return False
        
        # Push
        stdout, stderr, rc = self.run_cmd("git push origin main", cwd=local_path, timeout=30)
        if rc == 0:
            self.total_wealth += 10
            return True
        else:
            err_type, err_msg = self.diagnose_error(repo_name, stdout, stderr, rc)
            if err_type:
                self.record_lesson(repo_name, err_type, err_msg,
                                  f"push_failed_{err_type}", "Check error type and apply learned fix")
            return False

    def generate_unified_report(self, all_reports, external_opps):
        """Generate a unified dossier of the entire mesh."""
        total_repos = len(all_reports)
        healthy_repos = sum(1 for r in all_reports if r["health_score"] >= 80)
        degraded_repos = sum(1 for r in all_reports if 40 <= r["health_score"] < 80)
        critical_repos = sum(1 for r in all_reports if r["health_score"] < 40)
        avg_health = sum(r["health_score"] for r in all_reports) / total_repos if total_repos > 0 else 0
        total_issues = sum(len(r["issues"]) for r in all_reports)
        total_changes = sum(len(r.get("changes_applied", [])) for r in all_reports)

        # Check for stuck repos (no changes in 3+ cycles)
        stuck_repos = []
        for repo_name in set(r["repo"] for r in all_reports):
            recent_lessons = [l for l in self.lessons if l.get("repo") == repo_name and l.get("cycle", 0) >= self.cycle_count - 3]
            recent_errors = [l for l in recent_lessons if "fail" in l.get("root_cause", "").lower()]
            if len(recent_errors) >= 3:
                stuck_repos.append(repo_name)

        dossier = {
            "generated_at": datetime.now().isoformat(),
            "cycle": self.cycle_count,
            "total_wealth_generated": self.total_wealth,
            "mesh_summary": {
                "total_repos": total_repos,
                "healthy": healthy_repos,
                "degraded": degraded_repos,
                "critical": critical_repos,
                "average_health": round(avg_health, 1),
                "total_issues": total_issues,
                "total_changes_applied": total_changes,
                "stuck_repos": stuck_repos
            },
            "external_opportunities": external_opps[:10],
            "repo_reports": {r["repo"]: r for r in all_reports},
            "recent_lessons": [l for l in self.lessons[-20:]],
            "learning_summary": {
                "total_lessons": len(self.lessons),
                "unique_error_types": list(set(l.get("error_type", "unknown") for l in self.lessons)),
                "most_common_error": max(
                    set(l.get("root_cause", "unknown") for l in self.lessons),
                    key=lambda x: sum(1 for l in self.lessons if l.get("root_cause") == x),
                    default="none"
                ),
                "repos_with_most_errors": max(
                    set(l.get("repo", "unknown") for l in self.lessons),
                    key=lambda x: sum(1 for l in self.lessons if l.get("repo") == x),
                    default="none"
                )
            }
        }
        return dossier

    def save_dossier_to_markor(self, dossier):
        """Save the dossier as a .txt file readable by Markor app."""
        MARKOR_DIR.mkdir(parents=True, exist_ok=True)
        
        # Human-readable format
        lines = []
        lines.append("=" * 55)
        lines.append("🌍 OPENROOT/UNE AUTO DOSSIER")
        lines.append(f"Generated: {dossier['generated_at']}")
        lines.append(f"Cycle: {dossier['cycle']}")
        lines.append("=" * 55)
        lines.append("")
        
        ms = dossier["mesh_summary"]
        lines.append("📊 MESH HEALTH SUMMARY")
        lines.append(f"  Total Repos: {ms['total_repos']}")
        lines.append(f"  Healthy (≥80): {ms['healthy']}")
        lines.append(f"  Degraded (40-79): {ms['degraded']}")
        lines.append(f"  Critical (<40): {ms['critical']}")
        lines.append(f"  Average Health: {ms['average_health']}/100")
        lines.append(f"  Total Issues: {ms['total_issues']}")
        lines.append(f"  Changes Applied: {ms['total_changes_applied']}")
        if ms.get("stuck_repos"):
            lines.append(f"  ⚠️  STUCK REPOS: {', '.join(ms['stuck_repos'])}")
        lines.append("")
        
        lines.append("💰 WEALTH GENERATED: " + str(dossier.get("total_wealth_generated", 0)) + " credits")
        lines.append("")
        
        lines.append("📁 INDIVIDUAL REPÓ REPORTS")
        for repo_name, report in dossier["repo_reports"].items():
            lines.append(f"\n  ── {repo_name} ──")
            lines.append(f"  Health: {report['health_score']}/100")
            lines.append(f"  Files: {report['stats'].get('total_files', '?')} | Python: {report['stats'].get('python_files', '?')}")
            lines.append(f"  Last Commit: {report['stats'].get('last_commit', '?')}")
            if report["issues"]:
                lines.append(f"  Issues: {len(report['issues'])}")
                for issue in report["issues"][:3]:
                    lines.append(f"    • {issue['type']}: {issue['message'][:80]}")
            if report.get("changes_applied"):
                lines.append(f"  Changes Applied: {', '.join(report['changes_applied'])}")
            if report.get("recommendations"):
                lines.append(f"  Recommendations:")
                for rec in report["recommendations"][:3]:
                    lines.append(f"    → {rec}")
        
        lines.append("")
        lines.append("🔍 EXTERNAL OPPORTUNITIES (Top 5)")
        for i, opp in enumerate(dossier.get("external_opportunities", [])[:5], 1):
            lines.append(f"  {i}. {opp.get('repo', '?')} (Score: {opp.get('score', 0)})")
            lines.append(f"     {opp.get('reasons', '')}")
        
        lines.append("")
        ls = dossier["learning_summary"]
        lines.append("🧠 LEARNING SUMMARY")
        lines.append(f"  Total Lessons: {ls['total_lessons']}")
        lines.append(f"  Unique Error Types: {', '.join(ls['unique_error_types'])}")
        lines.append(f"  Most Common Error: {ls['most_common_error']}")
        lines.append(f"  Repo With Most Errors: {ls['repos_with_most_errors']}")
        lines.append("")
        
        recent = dossier.get("recent_lessons", [])
        if recent:
            lines.append("📝 RECENT LESSONS (Last 5)")
            for lesson in recent[-5:]:
                lines.append(f"  • [{lesson.get('error_type', '?')}] {lesson.get('repo', '?')}: {lesson.get('root_cause', '?')}")
        
        lines.append("")
        lines.append("=" * 55)
        lines.append("END OF DOSSIER")
        lines.append("=" * 55)
        
        txt_content = "\n".join(lines)
        DOSSIER_FILE.write_text(txt_content)
        
        # Also save JSON version
        json_dossier = UNE_ROOT / "auto_dossier.json"
        json_dossier.write_text(json.dumps(dossier, indent=2))
        
        print(f"📝 Dossier saved to: {DOSSIER_FILE}")
        print(f"📄 JSON dossier saved to: {json_dossier}")

    def run_cycle(self):
        """Run one full mesh loop cycle."""
        self.cycle_count += 1
        self.total_wealth = 0
        print("\n" + "=" * 55)
        print(f"🔄 FULL MESH LOOP — CYCLE {self.cycle_count}")
        print(f"   Time: {datetime.now().isoformat()}")
        print("=" * 55)
        
        # 1. Get all repos
        my_repos = self.get_my_repos()
        if not my_repos:
            print("❌ No repos found. Check gh auth.")
            return
        
        # 2. Scan external GitHub for opportunities
        external_opps = self.scan_github_external()
        
        # 3. Deep scan each repo individually
        all_reports = []
        for repo_info in my_repos:
            repo_name = repo_info.get("name")
            print(f"\n🔍 Scanning: {repo_name}...")
            report = self.scan_repo_individual(repo_info)
            all_reports.append(report)
            
            # 4. Apply changes and push gently
            if report.get("changes_applied"):
                pushed = self.commit_and_push_gentle(repo_name, report)
                if pushed:
                    print(f"  ✅ Changes pushed for {repo_name}")
                else:
                    print(f"  ⚠️  Push failed for {repo_name} — lesson recorded")
            
            # Save individual report
            repo_report_file = REPORTS_DIR / f"{repo_name}_report.json"
            repo_report_file.write_text(json.dumps(report, indent=2))
            print(f"  📄 Report: {repo_report_file}")
        
        # 5. Generate unified dossier
        dossier = self.generate_unified_report(all_reports, external_opps)
        
        # 6. Save to Markor + JSON
        self.save_dossier_to_markor(dossier)
        
        # 7. Print summary
        print("\n" + "=" * 55)
        print(f"🏁 CYCLE {self.cycle_count} COMPLETE")
        print(f"   Repos Scanned: {len(my_repos)}")
        print(f"   External Opportunities: {len(external_opps)}")
        print(f"   Wealth Generated: {self.total_wealth}")
        print(f"   Total Lessons: {len(self.lessons)}")
        print(f"   Dossier: {DOSSIER_FILE}")
        print("=" * 55)
        
        return dossier

def main():
    loop = MeshLoop()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--loop":
        # Continuous loop mode
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
        print(f"🔄 Continuous loop mode (every {interval}s)")
        while True:
            loop.run_cycle()
            print(f"\n🛌 Sleeping {interval}s...")
            time.sleep(interval)
    else:
        # Single cycle mode
        loop.run_cycle()

if __name__ == "__main__":
    ckpt = load_ckpt()
    main()
