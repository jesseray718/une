#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

export UNE_DIR="$HOME/une"
LOG_FILE="$UNE_DIR/logs/master_update.log"
mkdir -p "$UNE_DIR/logs"

log() { echo "[$(date '+%Y-%m-%dT%H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

cd "$UNE_DIR" || exit 1

log "MASTER_UPDATE_START"

# Run compounding cycle (pass arg for multiple cycles)
CYCLES="${1:-1}"
log "Running $CYCLES compound cycle(s)"
python3 "$UNE_DIR/compound.py" "$CYCLES" 2>&1 | tee -a "$LOG_FILE"

# Auto-commit if git repo
if [ -d "$UNE_DIR/.git" ]; then
  log "Git commit"
  git add -A 2>/dev/null || true
  git commit -m "auto: compound cycle $(python3 -c "import json; print(json.load(open('$UNE_DIR/state_checkpoint.json')).get('cycle',0))")" 2>/dev/null || log "Nothing to commit"
fi

log "MASTER_UPDATE_COMPLETE"
log "Master file: $UNE_DIR/master.md"
log "Dossier: $UNE_DIR/dossier.json"
log "Health: $UNE_DIR/health_report.json"
