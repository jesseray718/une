"""self_clone.py: Create a safe backup of current state."""
import shutil, json
from pathlib import Path
from state_utils import load_ckpt, stamp

UNE = Path(os.environ.get("UNE_DIR", str(Path.home() / "une")))
BACKUP_DIR = UNE / "backups" / f"clone_{stamp().replace(':', '-').replace('.', '_')}"

def clone():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    # Copy state and key configs
    ckpt = UNE / "state_checkpoint.json"
    if ckpt.exists():
        shutil.copy(ckpt, BACKUP_DIR / "state_checkpoint.json")
    
    # Copy master files
    for f in ["master.md", "dossier.json", "health_report.json"]:
        src = UNE / f
        if src.exists():
            shutil.copy(src, BACKUP_DIR / f)
    
    print(f"[CLONE] Backup created: {BACKUP_DIR.name}")

def main():
    clone()

if __name__ == "__main__":
    main()
