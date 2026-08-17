import ast, os, subprocess
from pathlib import Path
from state_utils import load_ckpt, save_ckpt

def scan_syntax_errors(repo_path):
    errors = []
    for py in Path(repo_path).rglob("*.py"):
        try:
            ast.parse(py.read_text(errors='replace'))
        except SyntaxError as e:
            errors.append({"file": str(py), "error": str(e)[:100]})
        except Exception:
            pass
    return errors

def guardian_check(ckpt):
    une_dir = os.environ.get('UNE_DIR', str(Path.home() / 'une'))
    errors = scan_syntax_errors(une_dir)
    error_count = len(errors)
    ckpt['guardian_syntax_errors'] = error_count
    ckpt['guardian_log_signals'] = error_count
    ckpt['health_score'] = max(0, 1.0 - (error_count * 0.01))
    ckpt['last_health_check'] = __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()
    if errors:
        ckpt['last_error'] = errors[0]['error']
    else:
        ckpt['last_error'] = None
    save_ckpt(ckpt)
    return ckpt
