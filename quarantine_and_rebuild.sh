#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
UNE_DIR="${UNE_DIR:-$HOME/une}"
cd "$UNE_DIR"
python3 "$UNE_DIR/scripts/quarantine_broken.py"
python3 "$UNE_DIR/scripts/rebuild_core.py"
echo "=== Rebuild Complete ==="
