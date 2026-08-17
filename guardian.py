"""guardian.py: Legacy wrapper calling guardian_wire."""
import subprocess, sys
from pathlib import Path
from state_utils import load_ckpt, save_ckpt

def main():
    guardian_path = Path(__file__).parent / "guardian_wire.py"
    if guardian_path.exists():
        subprocess.run([sys.executable, str(guardian_path)])
    else:
        print("[GUARDIAN] guardian_wire.py not found")

if __name__ == "__main__":
    ckpt = load_ckpt()
    main()
