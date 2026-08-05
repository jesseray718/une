#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

export UNE_DIR="$HOME/une"
LOG_FILE="$UNE_DIR/logs/meta_cycle.log"

mkdir -p "$UNE_DIR/logs" "$UNE_DIR/snapshots"

log() { echo "[$(date '+%Y-%m-%dT%H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

cd "$UNE_DIR" || { log "FATAL: cannot cd to $UNE_DIR"; exit 1; }

# ── 1. Snapshot pre-state ──
log "SNAPSHOT_PRE_START"
python3 "$UNE_DIR/snapshot.py" 2>&1 | tee -a "$LOG_FILE" || log "SNAPSHOT_PRE_FAIL — continuing"

# ── 2. Evolution engine ──
log "EVOLUTION_START"
python3 "$UNE_DIR/evolution_engine.py" 2>&1 | tee -a "$LOG_FILE" || {
  log "EVOLUTION_FAIL — aborting cycle"
  exit 1
}

# ── 3. Autonomous mesh ──
log "MESH_START"
python3 "$UNE_DIR/autonomous_mesh.py" 2>&1 | tee -a "$LOG_FILE" || log "MESH_FAIL — partial cycle"

# ── 4. Snapshot post-state (anchor the delta) ──
log "SNAPSHOT_POST_START"
python3 "$UNE_DIR/snapshot.py" 2>&1 | tee -a "$LOG_FILE" || log "POST_SNAPSHOT_FAIL"

log "CYCLE_COMPLETE"
