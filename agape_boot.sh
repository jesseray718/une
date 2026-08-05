#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
UNE_DIR="${UNE_DIR:-$HOME/une}"
INTERVAL="${AGAPE_INTERVAL:-3600}"
mkdir -p "$UNE_DIR/logs"
while true; do
  echo "[AGAPE] $(date) Cycle starting..."
  python3 "$UNE_DIR/agape_unified.py" 2>&1 | tee -a "$UNE_DIR/logs/agape_daemon.log"
  sleep "$INTERVAL"
done
