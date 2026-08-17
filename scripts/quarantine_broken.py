import shutil, os
from pathlib import Path
from datetime import datetime

UNE = Path(os.environ.get("UNE_DIR", str(Path.home() / "une")))
broken_files = [
    "absorb_batch.py", "alchemy_transmute.py", "create_scripture_corpus.py",
    "guardian.py", "guardian_v4.py", "kernel_init.py", "note.py",
    "self_clone.py", "swarm_query.py", "wire_core.py"
]

BACKUP_DIR = UNE / "backups" / f"broken_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

for fname in broken_files:
    src = UNE / fname
    if src.exists():
        shutil.move(str(src), str(BACKUP_DIR / fname))
        print(f"[MOVED] {fname} -> {BACKUP_DIR.name}/")
