#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
UNE_DIR="${UNE_DIR:-$HOME/une}"
cd "$UNE_DIR"
python3 "$UNE_DIR/scripts/fix_autonomous_mesh.py"
python3 "$UNE_DIR/scripts/fix_evolution_engine.py"
echo "=== Emergency Patch Applied ==="
