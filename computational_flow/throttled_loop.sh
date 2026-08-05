#!/usr/bin/env bash
set -euo pipefail

DIR="$(pwd)/une/computational_flow"
MAX="${1:-0}"
CYCLE=0
MIN_INT=30
MAX_INT=300

while true; do
    CYCLE=$((CYCLE + 1))
    echo "=== CYCLE #$CYCLE | $(date '+%Y-%m-%d %H:%M:%S') ==="

    echo "[1/5] Audit"
    python3 "$DIR/meta_audit.py"

    HEALTH=$(python3 -c "
import json
from pathlib import Path
p=Path('/sdcard/openroot/agape_kb/audit_report.json')
print(json.loads(p.read_text()).get('summary',{}).get('health',50) if p.exists() else 50)
" 2>/dev/null || echo 50)
    echo "Health: $HEALTH/100"

    echo "[2/5] Self-improve (dry)"
    python3 "$DIR/self_improve.py" --dry

    echo "[3/5] Meta-meta"
    python3 "$DIR/meta_meta.py"

    echo "[4/5] Snapshot"
    python3 "$DIR/fs_hook.py" snap

    echo "[5/5] Stamp"
    python3 "$DIR/stamp_context.py" "cycle_$CYCLE" "Health=$HEALTH"

    if [ "$HEALTH" -ge 90 ]; then
        INT=$MAX_INT
        echo "Throttle: SLOW (${INT}s)"
    elif [ "$HEALTH" -ge 70 ]; then
        INT=$((MIN_INT * 5))
        echo "Throttle: MEDIUM (${INT}s)"
    else
        INT=$MIN_INT
        echo "Throttle: FAST (${INT}s)"
    fi

    if [ "$MAX" -gt 0 ] && [ "$CYCLE" -ge "$MAX" ]; then
        echo "=== DONE: $CYCLE cycles ==="
        break
    fi

    echo "Sleep ${INT}s..."
    sleep "$INT"
done
