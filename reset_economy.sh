#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
UNE_DIR="${UNE_DIR:-$HOME/une}"
cd "$UNE_DIR"
python3 "$UNE_DIR/scripts/reset_economy.py"
bash "$UNE_DIR/master_update.sh" 1
echo "=== Reset Complete ==="
