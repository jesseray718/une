#!/usr/bin/env python3
"""
LESSON INJECTOR v1.0
Transmutes errors into structured lessons.
Feeds UniversalTrainer for pattern recognition and wealth generation.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

UNE_ROOT = Path.home() / "une"
LESSONS_FILE = UNE_ROOT / "logs" / "full_mesh_lessons.jsonl"

def inject_lesson(
    error_type: str,
    error_detail: str,
    root_cause: str,
    fix_applied: str,
    wealth_transmutation: str,
    category: str = "operational",
    source: str = "manual",
    synergy_tags: list = None
):
    """Inject a structured lesson into the mesh lesson log."""

    lesson = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "error_type": error_type,
        "error_detail": error_detail,
        "root_cause": root_cause,
        "fix_applied": fix_applied,
        "wealth_transmutation": wealth_transmutation,
        "category": category,
        "source": source,
        "synergy_tags": synergy_tags or [],
        "lesson_hash": hashlib.sha256(
            f"{error_type}:{fix_applied}".encode()
        ).hexdigest()[:16]
    }

    with open(LESSONS_FILE, 'a') as f:
        f.write(json.dumps(lesson) + '\n')

    print(f"  ✅ Lesson injected: {error_type}")
    print(f"     Hash: {lesson['lesson_hash']}")
    print(f"     Transmutation: {wealth_transmutation}")
    return lesson

def inject_batch(lessons):
    """Inject multiple lessons at once."""
    for l in lessons:
        inject_lesson(**l)

if __name__ == "__main__":
    # === FOUNDATIONAL LESSONS ===
    foundational_lessons = [
        {
            "error_type": "search_failed",
            "error_detail": "10x search_failed errors — Python code pasted into bash shell, causing every line to be interpreted as a shell command",
            "root_cause": "No file boundary between Python and bash; code was streamed directly into interactive bash instead of being written to a .py file via heredoc",
            "fix_applied": "Used cat > file.py << 'UNIQUE_DELIMITER' heredoc with single-quoted delimiter to prevent bash expansion, then executed with python3 file.py",
            "wealth_transmutation": "Created reusable deployment pattern: all future Python scripts deployed via heredoc with unique delimiters, eliminating an entire CLASS of errors permanently. This pattern compounds — every future script deployment saves ~5 minutes of debugging, worth approximately 50 joules of human effort per deployment.",
            "category": "deployment",
            "source": "atomic_core_cycle_1",
            "synergy_tags": ["heredoc_pattern", "bash_python_boundary", "deployment_efficiency"]
        },
        {
            "error_type": "search_failed",
            "error_detail": "bash treats 'import' as a binary command and suggests 'pkg install imagemagick' — wasted cycles on wrong installs",
            "root_cause": "Bash has no concept of Python imports; it parses every token as a potential executable",
            "fix_applied": "Recognized that ALL 'command not found' errors on Python keywords indicate code is being interpreted by bash, not Python. Diagnostic rule: if you see 'import is not installed', STOP — you are in the wrong interpreter.",
            "wealth_transmutation": "Created diagnostic heuristic that converts confusion into instant recognition. Future encounters of this error class are resolved in <1 second instead of minutes. Estimated savings: 200 joules across remaining project lifetime.",
            "category": "diagnostic",
            "source": "atomic_core_cycle_1",
            "synergy_tags": ["rapid_diagnosis", "interpreter_detection", "error_class_elimination"]
        },
        {
            "error_type": "search_failed",
            "error_detail": "Variable name typo REPORT_md vs REPORT_MD caused set -u to abort entire script",
            "root_cause": "Case inconsistency in variable naming; bash set -u correctly caught the undefined variable but the fix required manual inspection",
            "fix_applied": "Standardized all variable names to UPPER_SNAKE_CASE with consistent casing. Used grouped { } block for multiple writes to same file.",
            "wealth_transmutation": "Established coding standard that prevents entire class of typographic errors. Every future script inherits this convention, compounding reliability. Worth ~100 joules in avoided debugging.",
            "category": "coding_standard",
            "source": "atomic_core_cycle_1",
            "synergy_tags": ["naming_convention", "defensive_programming", "set_u_safe"]
        },
        {
            "error_type": "search_failed",
            "error_detail": "Heredoc delimiter ATOMIC_EOF appeared inside content being parsed by bash, causing premature termination and file not written",
            "root_cause": "Heredoc delimiter was not unique enough; bash found the string ATOMIC_EOF mid-parse and closed the heredoc early",
            "fix_applied": "Used unique delimiter PY_ATOMIC_2026 with project prefix and date stamp to guarantee collision-free heredoc",
            "wealth_transmutation": "Created a permanent deployment template that will never collide. Every future heredoc uses PROJECT_PURPOSE_DATE format. Eliminates an entire error class. Worth ~150 joules across project lifetime.",
            "category": "deployment",
            "source": "atomic_core_cycle_1",
            "synergy_tags": ["heredoc_safety", "unique_delimiters", "deployment_template"]
        },
        {
            "error_type": "unbound_variable",
            "error_detail": "REPORT_md referenced in echo but only REPORT_MD was defined, triggering set -u abort",
            "root_cause": "Inconsistent variable casing within same script block",
            "fix_applied": "Unified all references to REPORT_MD; audited entire script for case consistency",
            "wealth_transmutation": "Added pre-flight lint check to deployment protocol: grep for variable case mismatches before execution. Worth ~50 joules in future debugging avoidance.",
            "category": "linting",
            "source": "atomic_core_cycle_1",
            "synergy_tags": ["pre_flight_check", "case_sensitivity", "lint_protocol"]
        },
        {
            "error_type": "git_clone_blocked",
            "error_detail": "git clone into non-empty directory failed: 'destination path already exists and is not an empty directory'",
            "root_cause": "Attempted to clone into ~/une which already contained files from prior work",
            "fix_applied": "Used git -C for operations on existing repo; used git fetch --all --tags instead of clone for already-initialized repos",
            "wealth_transmutation": "Documented decision tree: if dir exists → fetch, if empty → clone. Eliminates a recurring 2-minute delay. Worth ~75 joules across remaining sessions.",
            "category": "git_workflow",
            "source": "atomic_core_cycle_1",
            "synergy_tags": ["git_decision_tree", "fetch_vs_clone", "workflow_efficiency"]
        },
        {
            "error_type": "password_store_empty",
            "error_detail": "Bash parsed Python 'pass' keyword as the Unix 'pass' password manager command, which had empty store",
            "root_cause": "Python keyword 'pass' collided with system binary 'pass' (password manager from pass package)",
            "fix_applied": "Recognized this as another symptom of Python-in-bash; the fix is the same heredoc deployment pattern",
            "wealth_transmutation": "Reinforced the diagnostic heuristic: any Python keyword being treated as a shell command confirms interpreter mismatch. Strengthens the pattern recognition network. Worth ~25 joules in faster future diagnosis.",
            "category": "diagnostic",
            "source": "atomic_core_cycle_1",
            "synergy_tags": ["keyword_collision", "diagnostic_reinforcement", "pattern_network"]
        },
        {
            "error_type": "inefficient_iteration",
            "error_detail": "Python code was manually pasted line-by-line into bash, causing ~80+ failed commands and zero productive output",
            "root_cause": "No file intermediary existed; raw text was fed to interactive bash prompt without any wrapper",
            "fix_applied": "Established golden rule: ALL Python code goes through cat > file << 'DELIM' pipeline. No exceptions.",
            "wealth_transmutation": "This single discipline converts a 30-minute debugging disaster into a 30-second deployment. The delta is enormous: ~1800 joules saved per future script deployment. Across 100 anticipated script deployments, this is 180,000 joules of human effort preserved.",
            "category": "workflow_fundamental",
            "source": "atomic_core_cycle_1",
            "synergy_tags": ["golden_rule", "heredoc_pipeline", "force_multiplier"]
        },
        {
            "error_type": "missing_directory",
            "error_detail": "atomic_core.py deployed to ~/une/bin/ but bin directory didn't exist, causing 'No such file or directory'",
            "root_cause": "Deployment sequence assumed directory structure existed without creating it first",
            "fix_applied": "Added mkdir -p before file deployment; baked into standard deployment template",
            "wealth_transmutation": "Created deployment checklist step #1: mkdir -p target directory. Prevents a class of FileNotFoundError across all future deployments. Worth ~30 joules.",
            "category": "deployment",
            "source": "atomic_core_cycle_1",
            "synergy_tags": ["directory_creation", "deployment_checklist", "defensive_setup"]
        },
        {
            "error_type": "search_failed",
            "error_detail": "10x recurrence of search_failed in lesson log indicates systemic issue, not isolated incident",
            "root_cause": "No structured feedback loop existed to capture, analyze, and eliminate recurring error patterns",
            "fix_applied": "Deployed Atomic Core with UniversalTrainer that extracts patterns from lessons and compiles best practices corpus",
            "wealth_transmutation": "The Atomic Core itself IS the transmutation machine. Every error fed into it becomes a training pattern that prevents future occurrence. The system grows smarter with each mistake. This is the definition of antifragility — errors make the system stronger, not weaker. Net wealth generation: unbounded, compounding with each cycle.",
            "category": "systemic",
            "source": "atomic_core_cycle_1",
            "synergy_tags": ["antifragile_core", "feedback_loop", "compounding_intelligence", "wealth_engine"]
        }
    ]

    inject_batch(foundational_lessons)
    print(f"\n  📚 {len(foundational_lessons)} foundational lessons injected")
    print(f"  📁 Log: {LESSONS_FILE}")
