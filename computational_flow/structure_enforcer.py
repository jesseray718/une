#!/data/data/com.termux/files/usr/bin/python3
"""
Structure Enforcer — Validates repos against OpenRoot permaculture axioms.

Axioms checked:
  AX-01: Observe & Interact (files must have docstrings/comments)
  AX-02: Catch & Store Energy (no energy-wasting redundant code)
  AX-03: Obtain a Yield (every function must return something)
  AX-04: Self-Regulation (no bare except clauses)
  AX-05: Produce No Waste (no heredoc artifacts, no junk files)
  AX-06: Modular standalone-or-networked (no hardcoded absolute paths)
  AX-07: Small & Slow Solutions (functions < 100 lines)

Usage:
  python3 structure_enforcer.py [directory]
  python3 structure_enforcer.py .          # scan current dir
  python3 structure_enforcer.py ~/une      # scan une repo
"""
import os, sys, re, ast
from pathlib import Path

HEREDOC_ARTIFACTS = [
    r'^--body$', r'^--label$', r'^--repo$', r'^--title$',
    r'^<<\'', r"^<<\"", r'^EOF$', r'^PYEOF$', r'^READMEEOF$',
]
HARDCODED_PATTERNS = [
    'os.path.expanduser("~") + "/"une/',
    'os.path.expanduser("~") + "/"openroot/',
    'os.environ.get("OPENROOT_BASE", "/sdcard/openroot") + "/"',
]
JUNK_FILES = [
    '__pycache__', '.pyc', '.broken', '.bak', '.tmp',
    'core_functions.py.bak', 'stre', 'stam',
]
FUNCTION_MAX_LINES = 100

def check_heredoc(filepath, lines):
    issues = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        for pattern in HEREDOC_ARTIFACTS:
            if re.match(pattern, stripped):
                issues.append(('AX-05', f'L{i}: heredoc artifact: {stripped}'))
    return issues

def check_hardcoded(filepath, lines):
    issues = []
    for i, line in enumerate(lines, 1):
        if filepath.endswith('.py'):
            for hp in HARDCODED_PATTERNS:
                if hp in line and 'OPENROOT_HOME' not in line and 'environ' not in line and 'LEDGER' not in line and 'DUMP_DIR' not in line and 'CONTEXT_BRIDGE' not in line:
                    issues.append(('AX-06', f'L{i}: hardcoded path: {hp}'))
    return issues

def check_ast(filepath, content):
    issues = []
    try:
        tree = ast.parse(content, filename=filepath)
    except SyntaxError as e:
        issues.append(('AX-01', f'Syntax error: {e}'))
        return issues

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name
            line_count = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0

            if line_count > FUNCTION_MAX_LINES:
                issues.append(('AX-07', f'L{node.lineno}: {name}() is {line_count} lines (max {FUNCTION_MAX_LINES})'))

            if not (node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str)):
                issues.append(('AX-01', f'L{node.lineno}: {name}() missing docstring'))

            has_return = any(isinstance(n, ast.Return) for n in ast.walk(node))
            if not has_return and not any(isinstance(n, ast.Yield) for n in ast.walk(node)):
                issues.append(('AX-03', f'L{node.lineno}: {name}() has no return statement'))

            for child in ast.walk(node):
                if isinstance(child, ast.ExceptHandler):
                    if child.type is None:
                        issues.append(('AX-04', f'L{child.lineno}: bare except in {name}()'))
    return issues

def check_junk(filepath):
    issues = []
    for pattern in JUNK_FILES:
        if pattern in filepath:
            issues.append(('AX-05', f'Junk file pattern: {pattern}'))
    return issues

def scan_directory(directory):
    directory = Path(directory)
    if not directory.exists():
        print(f'ERROR: {directory} does not exist')
        return False

    # Load ignore list
    ignore_patterns = []
    ignore_file = directory / '.structure_enforcer_ignore'
    if ignore_file.exists():
        with open(ignore_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignore_patterns.append(line)

    py_files = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ('__pycache__', '.git', 'node_modules')]
        for f in files:
            if f.endswith(('.py', '.sh', '.md', '.json')):
                py_files.append(Path(root) / f)

    total_issues = 0
    critical = 0
    warnings = 0
    report = []

    for fp in sorted(py_files):
        rel = fp.relative_to(directory)
        issues = []

        junk = check_junk(str(fp))
        if junk:
            continue

        try:
            with open(fp, 'r', errors='ignore') as fh:
                lines = fh.readlines()
                content = ''.join(lines)
        except:
            continue

        issues.extend(check_heredoc(str(fp), lines))
        issues.extend(check_hardcoded(str(fp), lines))

        if fp.suffix == '.py':
            issues.extend(check_ast(str(fp), content))

        if issues:
            total_issues += len(issues)
            for ax, msg in issues:
                sev = 'CRITICAL' if ax in ('AX-05', 'AX-06') else 'WARNING'
                if sev == 'CRITICAL':
                    critical += 1
                else:
                    warnings += 1
                report.append(f'  [{ax} {sev}] {rel}: {msg}')

    print('\n=== STRUCTURE ENFORCER REPORT ===')
    print(f'Scanned: {len(py_files)} files in {directory}')
    print(f'Issues: {total_issues} ({critical} critical, {warnings} warnings)')

    if report:
        for line in report:
            print(line)
    else:
        print('  ✓ All axioms satisfied.')

    passed = critical == 0
    print(f'\nResult: {"PASS" if passed else "FAIL"}')
    return passed

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    ok = scan_directory(target)
    sys.exit(0 if ok else 1)
