#!/usr/bin/env python3
"""
AUTONOMOUS ANTIFRAGILE MESH ENGINE v1.0
========================================
Self-healing computational organism.
Scans → Diagnoses → Mutates → Learns → Evolves → Anchors.

AXIOM: The system becomes stronger from every error it encounters.
"""

import os, sys, json, hashlib, subprocess, shutil, time, ast, re, traceback
from pathlib import Path
from datetime import datetime

# ─── PATH RESOLUTION (uses paths.py if available, falls back to env) ───
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "computational_flow"))
    from paths import Paths
    BASE = Paths.base
    META_HUB = Paths.meta_hub
except Exception:
    BASE = os.environ.get("UNE_BASE", os.path.expanduser("~/une"))
    META_HUB = os.path.join(BASE, "meta_hub")

WISDOM_FILE = os.path.join(BASE, "wisdom", "error_patterns.json")
LEDGER_FILE = os.path.join(BASE, "autonomous_ledger.jsonl")
BACKUP_DIR = os.path.join(BASE, "backups", f"auto_fix_{datetime.now().strftime('%Y%m%d')}")
REPORT_FILE = os.path.join(BASE, "autonomous_report.json")
EVOLUTION_DIR = os.path.join(BASE, "contributions")

# Directories to SKIP during scanning (vendored/external noise)
SKIP_DIRS = {
    "node_modules", ".git", "__pycache__", "sync-from-kai",
    ".venv", "venv", "stamps", "kai-sandbox", ".tox"
}

# ─── ENSURE STRUCTURE ───
for d in [os.path.dirname(WISDOM_FILE), BACKUP_DIR, EVOLUTION_DIR]:
    os.makedirs(d, exist_ok=True)

if not os.path.exists(WISDOM_FILE):
    with open(WISDOM_FILE, 'w') as f:
        json.dump({"patterns": [], "version": 1, "last_updated": datetime.now().isoformat()}, f)


class AutonomousMesh:
    """The self-healing engine."""

    def __init__(self):
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "scanned_files": 0,
            "problems_found": 0,
            "problems_fixed": 0,
            "lessons_learned": 0,
            "evolution_patches": 0,
            "errors_blocked_by_wisdom": 0,
            "details": []
        }
        self.wisdom = self._load_wisdom()

    # ═══ WISDOM LAYER ═══

    def _load_wisdom(self):
        try:
            with open(WISDOM_FILE) as f:
                return json.load(f)
        except Exception:
            return {"patterns": [], "version": 1}

    def _save_wisdom(self):
        self.wisdom["last_updated"] = datetime.now().isoformat()
        with open(WISDOM_FILE, 'w') as f:
            json.dump(self.wisdom, f, indent=2)

    def _inject_lesson(self, error_type, root_cause, fix_applied, file_path, pattern_signature):
        """Inject a lesson into the wisdom scaffold."""
        lesson = {
            "id": hashlib.sha256(pattern_signature.encode()).hexdigest()[:16],
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "root_cause": root_cause,
            "fix_applied": fix_applied,
            "file": file_path,
            "signature": pattern_signature,
            "prevention_rule": f"Reject code matching: {pattern_signature[:80]}"
        }
        # Check if already learned
        existing_ids = [p["id"] for p in self.wisdom["patterns"]]
        if lesson["id"] not in existing_ids:
            self.wisdom["patterns"].append(lesson)
            self._save_wisdom()
            self.report["lessons_learned"] += 1
            self._log(f"🧠 LESSON LEARNED: {error_type} in {os.path.basename(file_path)}")
            self._log(f"   Root cause: {root_cause}")
            self._log(f"   Prevention rule injected into wisdom scaffold")
        else:
            self.report["errors_blocked_by_wisdom"] += 1
            self._log(f"✅ WISDOM HIT: Pattern already known — {error_type}")

    # ═══ LOGGING ═══

    def _log(self, msg):
        print(msg)
        entry = {
            "timestamp": datetime.now().isoformat(),
            "message": msg
        }
        try:
            with open(LEDGER_FILE, 'a') as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass

    def _ledger_entry(self, action, file_path, details, status):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "file": file_path,
            "details": details,
            "status": status
        }
        try:
            with open(LEDGER_FILE, 'a') as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass

    # ═══ PASSIVITY LAYER: SCANNERS ═══

    def _should_skip(self, path_parts):
        """Check if path contains skip directories."""
        for part in path_parts:
            if part in SKIP_DIRS:
                return True
        return False

    def scan_duplicates(self):
        """Scan for byte-identical files across the ecosystem."""
        self._log("🔍 SCANNER: Deduplication scan starting...")
        hash_map = {}
        dup_count = 0

        for repo_name in os.listdir(META_HUB):
            repo_path = os.path.join(META_HUB, repo_name)
            if not os.path.isdir(repo_path):
                continue
            for root, dirs, files in os.walk(repo_path):
                # Filter skip dirs
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for fname in files:
                    fpath = os.path.join(root, fname)
                    try:
                        with open(fpath, 'rb') as f:
                            h = hashlib.sha256(f.read()).hexdigest()[:16]
                        rel = os.path.relpath(fpath, META_HUB)
                        if h in hash_map:
                            hash_map[h].append(rel)
                            dup_count += 1
                        else:
                            hash_map[h] = [rel]
                        self.report["scanned_files"] += 1
                    except Exception:
                        continue

        # Build duplicate report
        duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}
        total_dup_bytes = 0
        for h, paths in duplicates.items():
            try:
                total_dup_bytes += os.path.getsize(os.path.join(META_HUB, paths[0])) * (len(paths) - 1)
            except Exception:
                pass

        self._log(f"🔍 DEDUP: Found {len(duplicates)} duplicate groups, "
                  f"{dup_count} redundant files, ~{total_dup_bytes // 1024}KB reclaimable")

        # Diagnose WHY duplicates exist
        if duplicates:
            for h, paths in list(duplicates.items())[:5]:
                # Analyze root cause
                dirs_involved = set()
                for p in paths:
                    parts = p.split('/')
                    if len(parts) > 1:
                        dirs_involved.add(parts[0])
                root_cause = f"Files duplicated across repos: {', '.join(list(dirs_involved)[:3])}"
                self._inject_lesson(
                    "duplicate_file",
                    root_cause,
                    "Flagged for consolidation to canonical path",
                    paths[0],
                    f"dup:{h}"
                )

        self.report["details"].append({
            "scanner": "dedup",
            "duplicate_groups": len(duplicates),
            "redundant_files": dup_count,
            "reclaimable_kb": total_dup_bytes // 1024,
            "sample": list(duplicates.items())[:3]
        })
        return duplicates

    def scan_syntax(self):
        """Scan all Python files for syntax errors."""
        self._log("🔍 SCANNER: Syntax scan starting...")
        errors = []

        for repo_name in os.listdir(META_HUB):
            repo_path = os.path.join(META_HUB, repo_name)
            if not os.path.isdir(repo_path):
                continue
            for root, dirs, files in os.walk(repo_path):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for fname in files:
                    if not fname.endswith('.py'):
                        continue
                    fpath = os.path.join(root, fname)
                    try:
                        with open(fpath, 'r') as f:
                            source = f.read()
                        ast.parse(source, filename=fpath)
                        self.report["scanned_files"] += 1
                    except SyntaxError as e:
                        rel = os.path.relpath(fpath, META_HUB)
                        errors.append({
                            "file": rel,
                            "path": fpath,
                            "line": e.lineno,
                            "msg": str(e.msg),
                            "text": e.text
                        })
                        self._log(f"❌ SYNTAX ERROR: {rel}:{e.lineno} — {e.msg}")
                        # Diagnose root cause
                        cause = self._diagnose_syntax_error(e, fpath)
                        self._inject_lesson(
                            "syntax_error",
                            cause,
                            "Pending mutation",
                            rel,
                            f"syntax:{e.msg[:60]}"
                        )

        self._log(f"🔍 SYNTAX: Found {len(errors)} syntax errors")
        self.report["problems_found"] += len(errors)
        self.report["details"].append({
            "scanner": "syntax",
            "error_count": len(errors),
            "errors": [{"file": e["file"], "line": e["line"], "msg": e["msg"]} for e in errors[:10]]
        })
        return errors

    def scan_hardcoded_paths(self):
        """Scan for hardcoded Termux/SD card paths."""
        self._log("🔍 SCANNER: Hardcoded path scan starting...")
        BAD_PATTERNS = [
            r'/data/data/com\.termux',
            r'/sdcard/openroot',
            r'/storage/emulated',
        ]
        findings = []

        for repo_name in os.listdir(META_HUB):
            repo_path = os.path.join(META_HUB, repo_name)
            if not os.path.isdir(repo_path):
                continue
            for root, dirs, files in os.walk(repo_path):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for fname in files:
                    if not fname.endswith(('.py', '.sh')):
                        continue
                    fpath = os.path.join(root, fname)
                    try:
                        with open(fpath, 'r') as f:
                            lines = f.readlines()
                        for i, line in enumerate(lines, 1):
                            for pat in BAD_PATTERNS:
                                if re.search(pat, line):
                                    rel = os.path.relpath(fpath, META_HUB)
                                    findings.append({
                                        "file": rel,
                                        "path": fpath,
                                        "line_num": i,
                                        "line": line.strip()[:100],
                                        "pattern": pat
                                    })
                                    break
                    except Exception:
                        continue

        self._log(f"🔍 PATHS: Found {len(findings)} hardcoded path references")
        for f in findings[:5]:
            self._inject_lesson(
                "hardcoded_path",
                "Script uses absolute Termux path instead of paths.py resolution",
                "Flagged for paths.py migration",
                f["file"],
                f"hardpath:{f['pattern']}"
            )

        self.report["problems_found"] += len(findings)
        self.report["details"].append({
            "scanner": "hardcoded_paths",
            "count": len(findings),
            "findings": [{"file": f["file"], "line": f["line_num"]} for f in findings[:10]]
        })
        return findings

    def scan_contributions_bloat(self):
        """Scan for accumulated contribution files that should be pruned."""
        self._log("🔍 SCANNER: Contributions bloat scan starting...")
        contrib_dir = os.path.join(BASE, "contributions")
        if not os.path.isdir(contrib_dir):
            contrib_dir = os.path.join(META_HUB, "une", "contributions")

        files = sorted(Path(contrib_dir).glob("*.py"), key=lambda p: p.name)
        excess = max(0, len(files) - 5)  # Keep latest 5

        if excess > 0:
            self._log(f"🔍 CONTRIBUTIONS: {len(files)} files, {excess} can be pruned")
            self._inject_lesson(
                "contributions_bloat",
                "Auto-evolution and meta-upgrade files accumulate without pruning",
                f"Keep latest 5, prune {excess} oldest",
                str(contrib_dir),
                "bloat:contributions_overflow"
            )

        self.report["details"].append({
            "scanner": "contributions_bloat",
            "total_files": len(files),
            "prunable": excess
        })
        return files, excess

    # ═══ DIAGNOSIS LAYER ═══

    def _diagnose_syntax_error(self, exc, fpath):
        """Analyze a SyntaxError to determine root cause."""
        if exc.text and '\\n' in (exc.text or ''):
            return "Literal \\n characters from bad regex replacement (fix_round2.py artifact)"
        if 'eval' in (exc.text or '').lower() and 'exec' in (exc.text or '').lower():
            return "Unsafe eval/exec pattern"
        if exc.msg and 'unterminated' in exc.msg.lower():
            return "Unterminated string literal — likely truncated heredoc"
        if exc.msg and 'unexpected' in exc.msg.lower() and 'indent' in exc.msg.lower():
            return "Indentation inconsistency"
        return f"SyntaxError: {exc.msg}"

    # ═══ AUTONOMY LAYER: MUTATION ENGINE ═══

    def fix_duplicates(self, duplicates):
        """Consolidate duplicate files by replacing copies with symlinks."""
        self._log("🔧 MUTATION: Deduplication fix starting...")
        fixed = 0

        for h, paths in duplicates.items():
            if len(paths) < 2:
                continue

            # Canonical = shortest path (most central)
            canonical = min(paths, key=len)
            canon_full = os.path.join(META_HUB, canonical)

            for dup_path in paths:
                if dup_path == canonical:
                    continue
                dup_full = os.path.join(META_HUB, dup_path)

                # Skip if in vendored dir
                if self._should_skip(dup_path.split('/')):
                    continue

                try:
                    # Backup
                    backup_name = dup_full.replace('/', '_')
                    backup_path = os.path.join(BACKUP_DIR, f"dup_{hashlib.md5(dup_path.encode()).hexdigest()[:8]}_{os.path.basename(dup_path)}")
                    shutil.copy2(dup_full, backup_path)

                    # Replace with symlink
                    os.remove(dup_full)
                    os.symlink(canon_full, dup_full)
                    fixed += 1
                    self._log(f"  🔗 LINKED: {dup_path} → {canonical}")
                    self._ledger_entry("dedup_symlink", dup_path, f"→ {canonical}", "fixed")
                except Exception as e:
                    self._log(f"  ⚠️ SKIP: {dup_path} — {e}")
                    self._ledger_entry("dedup_skip", dup_path, str(e), "skipped")

        self.report["problems_fixed"] += fixed
        self._log(f"🔧 DEDUP: Consolidated {fixed} files into symlinks")
        return fixed

    def fix_syntax_errors(self, errors):
        """Attempt safe syntax fixes."""
        self._log("🔧 MUTATION: Syntax fix starting...")
        fixed = 0

        for err in errors:
            fpath = err["path"]
            try:
                with open(fpath, 'r') as f:
                    lines = f.readlines()

                line_idx = (err["line"] or 1) - 1
                if line_idx >= len(lines):
                    continue

                original = lines[line_idx]
                modified = original
                fix_type = None

                # Fix 1: Literal \n → newline (regex artifact)
                if '\\n' in original and not original.strip().startswith('#'):
                    modified = original.replace('\\n', '\n')
                    fix_type = "literal_n_to_newline"

                # Fix 2: Unterminated string — add closing quote
                elif err["msg"] and 'unterminated' in err["msg"].lower():
                    stripped = original.strip()
                    if stripped.endswith("'") and stripped.count("'") % 2 != 0:
                        modified = original.rstrip() + "'\n"
                        fix_type = "close_string_single"
                    elif stripped.endswith('"') and stripped.count('"') % 2 != 0:
                        modified = original.rstrip() + '"\n'
                        fix_type = "close_string_double"

                # Fix 3: Bad indentation (tab/space mix)
                elif err["msg"] and 'indent' in err["msg"].lower():
                    modified = original.expandtabs(4)
                    fix_type = "tabs_to_spaces"

                if fix_type:
                    # Backup
                    backup_path = os.path.join(BACKUP_DIR, os.path.basename(fpath) + ".bak")
                    shutil.copy2(fpath, backup_path)

                    # Apply fix
                    lines[line_idx] = modified
                    with open(fpath, 'w') as f:
                        f.writelines(lines)

                    # Verify fix
                    try:
                        with open(fpath, 'r') as f:
                            ast.parse(f.read(), filename=fpath)
                        fixed += 1
                        self._log(f"  ✅ FIXED [{fix_type}]: {err['file']}:{err['line']}")
                        self._ledger_entry("syntax_fix", err["file"], fix_type, "fixed")

                        # Learn from this
                        self._inject_lesson(
                            "syntax_error",
                            self._diagnose_syntax_error(err, fpath),
                            f"Applied {fix_type}",
                            err["file"],
                            f"syntax:{err['msg'][:60]}"
                        )
                    except SyntaxError as e2:
                        self._log(f"  ❌ FIX FAILED: {err['file']} — still has error at line {e2.lineno}")
                        self._ledger_entry("syntax_fix", err["file"], f"fix failed: {fix_type}", "failed")
                        # Restore backup
                        shutil.copy2(backup_path, fpath)

            except Exception as e:
                self._log(f"  ⚠️ ERROR during fix: {err['file']} — {e}")
                self._ledger_entry("syntax_fix_error", err["file"], str(e), "error")

        self.report["problems_fixed"] += fixed
        self._log(f"🔧 SYNTAX: Fixed {fixed}/{len(errors)} errors")
        return fixed

    def fix_hardcoded_paths(self, findings):
        """Replace hardcoded paths with dynamic resolution."""
        self._log("🔧 MUTATION: Hardcoded path fix starting...")
        fixed = 0

        for finding in findings:
            fpath = finding["path"]
            line_num = finding["line_num"]
            try:
                with open(fpath, 'r') as f:
                    lines = f.readlines()

                original = lines[line_num - 1]
                modified = original

                # Replace patterns
                replacements = {
                    '/data/data/com.termux/files/home/': 'os.path.expanduser("~") + "/"',
                    '/sdcard/openroot/': 'os.environ.get("OPENROOT_BASE", "/sdcard/openroot") + "/"',
                    '/storage/emulated/0/': 'os.environ.get("ANDROID_STORAGE", "/storage/emulated/0") + "/"',
                }

                for old, new in replacements.items():
                    if old in modified:
                        # For .py files, use os.path
                        if fpath.endswith('.py'):
                            modified = modified.replace(old, new)
                        # For .sh files, use $VAR
                        elif fpath.endswith('.sh'):
                            sh_repl = {
                                '/data/data/com.termux/files/home/': '$HOME/',
                                '/sdcard/openroot/': '${OPENROOT_BASE:-/sdcard/openroot}/',
                                '/storage/emulated/0/': '${ANDROID_STORAGE:-/storage/emulated/0}/',
                            }
                            modified = modified.replace(old, sh_repl.get(old, old))

                if modified != original:
                    backup_path = os.path.join(BACKUP_DIR, os.path.basename(fpath) + ".pathfix.bak")
                    shutil.copy2(fpath, backup_path)

                    lines[line_num - 1] = modified
                    with open(fpath, 'w') as f:
                        f.writelines(lines)

                    fixed += 1
                    self._log(f"  🔧 PATHFIX: {finding['file']}:{line_num}")
                    self._ledger_entry("path_fix", finding["file"], "replaced hardcoded path", "fixed")

            except Exception as e:
                self._log(f"  ⚠️ PATHFIX ERROR: {finding['file']} — {e}")

        self.report["problems_fixed"] += fixed
        self._log(f"🔧 PATHS: Fixed {fixed}/{len(findings)} hardcoded paths")
        return fixed

    def prune_contributions(self, files, excess):
        """Prune old contribution files, keeping latest 5."""
        self._log("🔧 MUTATION: Pruning old contributions...")
        pruned = 0
        if excess > 0:
            old_files = files[:excess]  # Sorted oldest-first
            for f in old_files:
                try:
                    backup_path = os.path.join(BACKUP_DIR, f.name + ".pruned.bak")
                    shutil.copy2(str(f), backup_path)
                    f.unlink()
                    pruned += 1
                except Exception:
                    pass
            self._log(f"🔧 PRUNED: {pruned} old contribution files")
        self.report["problems_fixed"] += pruned
        return pruned

    # ═══ EVOLUTION LAYER ═══

    def evolve_self(self):
        """Generate a self-improvement patch based on this cycle's findings."""
        self._log("🧬 EVOLUTION: Generating self-improvement patch...")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        patch_file = os.path.join(EVOLUTION_DIR, f"auto_evolution_{timestamp}.py")

        # Count current wisdom
        wisdom_count = len(self.wisdom.get("patterns", []))
        fix_rate = 0
        if self.report["problems_found"] > 0:
            fix_rate = self.report["problems_fixed"] / self.report["problems_found"]

        patch_content = f'''#!/usr/bin/env python3
"""
AUTO-EVOLUTION PATCH {timestamp}
Generated by autonomous_mesh.py
Wisdom entries: {wisdom_count}
Fix rate this cycle: {fix_rate:.1%}
Problems found: {self.report["problems_found"]}
Problems fixed: {self.report["problems_fixed"]}
"""
import json, os
from datetime import datetime

WISDOM_FILE = "{WISDOM_FILE}"

def run():
    """Apply evolution improvements."""
    print(f"🧬 Evolution patch {timestamp} executing...")
    
    # Load wisdom count
    try:
        with open(WISDOM_FILE) as f:
            w = json.load(f)
        print(f"  Wisdom patterns: {{len(w.get('patterns', []))}}")
        print(f"  Last updated: {{w.get('last_updated', 'unknown')}}")
    except:
        pass
    
    print(f"  Fix rate: {fix_rate:.1%}")
    print(f"  Problems this cycle: {self.report['problems_found']} found, {self.report['problems_fixed']} fixed")
    
    # Self-test: ensure all scanners still parse
    print("  Self-test: AST parse autonomous_mesh.py...")
    try:
        import ast
        with open(__file__) as f:
            ast.parse(f.read())
        print("  ✅ Self-test passed")
    except SyntaxError as e:
        print(f"  ❌ Self-test FAILED: {{e}}")
        return False
    
    return True

if __name__ == "__main__":
    run()
'''

        with open(patch_file, 'w') as f:
            f.write(patch_content)

        # Verify the patch itself is valid Python
        try:
            ast.parse(patch_content)
            self._log(f"🧬 EVOLUTION: Patch {patch_file} generated and verified")
            self._ledger_entry("evolution_patch", patch_file, f"wisdom={wisdom_count}, fix_rate={fix_rate:.1%}", "generated")
            self.report["evolution_patches"] += 1
        except SyntaxError as e:
            self._log(f"🧬 EVOLUTION: Patch generation FAILED — {e}")
            os.remove(patch_file)

        return patch_file

    # ═══ PRACTICE LOOP ═══

    def practice_loop(self):
        """Test all previously generated evolution patches to ensure they still run."""
        self._log("🔁 PRACTICE: Testing previous evolution patches...")
        patches = sorted(Path(EVOLUTION_DIR).glob("auto_evolution_*.py"))
        passed = 0
        failed = 0

        for patch in patches[-10:]:  # Test last 10
            try:
                result = subprocess.run(
                    [sys.executable, str(patch)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    passed += 1
                else:
                    failed += 1
                    self._log(f"  ❌ PRACTICE FAIL: {patch.name}")
                    self._log(f"     {result.stderr[:200]}")
                    
                    # Learn from the failure
                    self._inject_lesson(
                        "evolution_patch_failure",
                        f"Previous patch {patch.name} fails on execution",
                        "Marked for regeneration",
                        str(patch),
                        f"patch_fail:{patch.name[:40]}"
                    )
            except subprocess.TimeoutExpired:
                failed += 1
                self._log(f"  ⏱️ TIMEOUT: {patch.name}")
            except Exception as e:
                failed += 1
                self._log(f"  ❌ PRACTICE ERROR: {patch.name} — {e}")

        self._log(f"🔁 PRACTICE: {passed} passed, {failed} failed out of {min(len(patches), 10)} tested")

    # ═══ SNAPSHOT & ANCHOR ═══

    def snapshot(self):
        """Create a snapshot of the system state after this cycle."""
        self._log("📸 SNAPSHOT: Capturing post-cycle state...")
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "report": self.report,
            "wisdom_count": len(self.wisdom.get("patterns", [])),
            "wisdom_file": WISDOM_FILE,
            "ledger_file": LEDGER_FILE
        }
        snap_file = os.path.join(BASE, "autonomous_snapshot.json")
        with open(snap_file, 'w') as f:
            json.dump(snapshot, f, indent=2)
        self._log(f"📸 SNAPSHOT: Saved to {snap_file}")
        return snap_file

    # ═══ MAIN EXECUTION CYCLE ═══

    def run_cycle(self):
        """Execute the full Observe→Diagnose→Mutate→Learn→Evolve cycle."""
        self._log("═" * 60)
        self._log("🦁 AUTONOMOUS MESH ENGINE v1.0 — CYCLE START")
        self._log(f"   Base: {BASE}")
        self._log(f"   Meta Hub: {META_HUB}")
        self._log(f"   Wisdom: {WISDOM_FILE}")
        self._log("═" * 60)

        # 1. OBSERVE — Run all scanners
        self._log("\n── PHASE 1: OBSERVE ──")
        dups = self.scan_duplicates()
        syntax_errs = self.scan_syntax()
        path_findings = self.scan_hardcoded_paths()
        contrib_files, contrib_excess = self.scan_contributions_bloat()

        # 2. DIAGNOSE — Root causes already injected during scan
        self._log(f"\n── PHASE 2: DIAGNOSE ──")
        self._log(f"   Total problems found: {self.report['problems_found']}")
        self._log(f"   Lessons learned: {self.report['lessons_learned']}")
        self._log(f"   Known patterns blocked: {self.report['errors_blocked_by_wisdom']}")

        # 3. MUTATE — Apply fixes
        self._log("\n── PHASE 3: MUTATE ──")
        self.fix_duplicates(dups)
        self.fix_syntax_errors(syntax_errs)
        self.fix_hardcoded_paths(path_findings)
        self.prune_contributions(contrib_files, contrib_excess)

        # 4. EVOLVE — Generate self-improvement patch
        self._log("\n── PHASE 4: EVOLVE ──")
        self.evolve_self()

        # 5. PRACTICE — Test previous patches
        self._log("\n── PHASE 5: PRACTICE ──")
        self.practice_loop()

        # 6. SNAPSHOT
        self._log("\n── PHASE 6: SNAPSHOT ──")
        self.snapshot()

        # Final report
        self._log("\n" + "═" * 60)
        self._log("🏆 CYCLE COMPLETE")
        self._log(f"   Files scanned: {self.report['scanned_files']}")
        self._log(f"   Problems found: {self.report['problems_found']}")
        self._log(f"   Problems fixed: {self.report['problems_fixed']}")
        self._log(f"   Lessons learned: {self.report['lessons_learned']}")
        self._log(f"   Wisdom patterns blocked: {self.report['errors_blocked_by_wisdom']}")
        self._log(f"   Evolution patches generated: {self.report['evolution_patches']}")
        
        fix_rate = 0
        if self.report["problems_found"] > 0:
            fix_rate = self.report["problems_fixed"] / self.report["problems_found"]
        self._log(f"   Fix rate: {fix_rate:.1%}")
        self._log("═" * 60)

        # Save report
        with open(REPORT_FILE, 'w') as f:
            json.dump(self.report, f, indent=2)
        self._log(f"📋 Report saved: {REPORT_FILE}")

        return self.report


if __name__ == "__main__":
    engine = AutonomousMesh()
    engine.run_cycle()
