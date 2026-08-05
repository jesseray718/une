#!/data/data/com.termux/files/usr/bin/python3
"""Bulk migrate ALL hardcoded paths to paths.py imports."""
import os, re
from pathlib import Path

BASE = Path("/data/data/com.termux/files/home/une")
IGNORE = {
    "setup_master.py", "ultimate_fix.py", "apply_all.py", "build_final.py",
    "fix_all_issues.py", "fix_round2.py", "final_fix.py", "cleanup_final.py",
    "bulk_migrate.py", "structure_enforcer.py"
}

# Map hardcoded paths to variable names in paths.py
PATH_MAP = {
    "/sdcard/openroot/dump/chunks": "DUMP_DIR",
    "/sdcard/openroot/context_bridge/context.json": "CONTEXT_BRIDGE",
    "/sdcard/openroot/context_bridge/immortal_context.json": "IMMORTAL_CONTEXT",
    "/sdcard/openroot/ledger.jsonl": "LEDGER",
    "/sdcard/openroot/relay": "RELAY",
    "/sdcard/openroot/storage": "STORAGE",
    "/sdcard/openroot/lessons": "LESSONS",
    "/sdcard/openroot/logs": "LOGS",
    "/sdcard/openroot/bin": "BIN",
}

# Broader patterns to replace
PATTERNS = [
    # /sdcard/openroot/ anything -> OPENROOT + rest
    (r'"(/sdcard/openroot/)([^"]*)"', r'os.path.join(OPENROOT, "\2")'),
    # /data/data/com.termux/files/home/une/ anything -> UNE_HOME + rest
    (r'"(/data/data/com\.termux/files/home/une/)([^"]*)"', r'os.path.join(UNE_HOME, "\2")'),
    # /data/data/com.termux/files/home/openroot/ -> OPENROOT
    (r'"(/data/data/com\.termux/files/home/openroot/)([^"]*)"', r'os.path.join(OPENROOT, "\2")'),
]

fixed_count = 0
skip_count = 0

for py_file in BASE.rglob("*.py"):
    if py_file.name in IGNORE:
        skip_count += 1
        continue
    
    # Skip __pycache__, .git, scaffold copies
    rel = str(py_file.relative_to(BASE))
    if "__pycache__" in rel or ".git" in rel or "scaffold/" in rel:
        continue
    
    try:
        content = py_file.read_text()
    except:
        continue
    
    original = content
    needs_openroot = False
    needs_une_home = False
    needs_os = False
    
    # Apply pattern replacements
    for pattern, replacement in PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, replacement, content)
            if "OPENROOT" in replacement:
                needs_openroot = True
            if "UNE_HOME" in replacement:
                needs_une_home = True
            if "os.path.join" in replacement:
                needs_os = True
    
    # Add imports at top if we made changes
    if content != original:
        lines = content.split("\n")
        
        # Find insertion point (after shebang and existing imports)
        insert_idx = 0
        for i, line in enumerate(lines[:20]):
            if line.startswith("#!") or line.startswith("import ") or line.startswith("from ") or line.strip() == "" or line.startswith('"""') or line.startswith("'"):
                insert_idx = i + 1
            else:
                break
        
        # Build import block
        imports = []
        if needs_os and "import os" not in [l.strip() for l in lines[:20]]:
            imports.append("import os")
        
        path_imports = []
        if needs_openroot:
            path_imports.append("OPENROOT")
        if needs_une_home:
            path_imports.append("UNE_HOME")
        
        if path_imports:
            # Try importing from paths first, fallback to environ
            imp_str = ", ".join(path_imports)
            imports.append(f'try:')
            imports.append(f'    from paths import {imp_str}')
            imports.append(f'except ImportError:')
            imports.append(f'    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")')
            imports.append(f'    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))')
        
        if imports:
            lines.insert(insert_idx, "\n".join(imports) + "\n")
        
        content = "\n".join(lines)
        
        py_file.write_text(content)
        fixed_count += 1
        print(f"  ✅ {rel}")

print(f"\nFixed: {fixed_count} files")
print(f"Skipped: {skip_count} setup scripts")

# Verify with enforcer
import subprocess, sys
print("\n🧪 Running Structure Enforcer...")
r = subprocess.run([sys.executable, "computational_flow/structure_enforcer.py", "."],
                   capture_output=True, text=True, cwd=str(BASE))

# Count results
lines = r.stdout.split("\n")
critical = [l for l in lines if "CRITICAL" in l]
warning = [l for l in lines if "WARNING" in l]

print(f"Critical: {len(critical)}")
print(f"Warnings: {len(warning)}")

if critical:
    print("\nRemaining CRITICAL issues:")
    for l in critical[:20]:
        print(f"  {l}")
    if len(critical) > 20:
        print(f"  ... and {len(critical) - 20} more")
else:
    print("\n✅ ZERO CRITICAL ISSUES!")

# Also run smoke test
print("\n🧪 Smoke Test:")
r2 = subprocess.run([sys.executable, "tests/test_smoke.py"], capture_output=True, text=True, cwd=str(BASE))
print(r2.stdout)

print("🎉 BULK MIGRATION COMPLETE.")
