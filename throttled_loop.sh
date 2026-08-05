#!/data/data/com.termux/files/usr/bin/env bash
# THROTTLED LOOP — Self-regulating audit-improve-meta cycle
set -euo pipefail

DIR="/data/data/com.termux/files/home/une/computational_flow"
MAX="${1:-0}"
CYCLE=0
MIN_INT=30
MAX_INT=300

while true; do
    CYCLE=$((CYCLE + 1))
    echo ""
    echo "========================================"
    echo "  AGAPE CYCLE #$CYCLE | $(date '+%Y-%m-%d %H:%M:%S')"
    echo "========================================"

    echo "[1/5] Meta audit..."
    python3 "$DIR/meta_audit.py" 2>&1 | tail -5

    HEALTH=$(python3 -c "
import json
from pathlib import Path
p=Path('/sdcard/openroot/agape_kb/audit_report.json')
print(json.loads(p.read_text()).get('summary',{}).get('health',50) if p.exists() else 50)
" 2>/dev/null || echo 50)

    echo "  Health: $HEALTH/100"

    echo "[2/5] Self-improve (dry run)..."
    python3 "$DIR/self_improve.py" --dry 2>&1 | tail -3

    echo "[3/5] Meta-meta audit..."
    python3 "$DIR/meta_meta.py" 2>&1 | tail -5

    echo "[4/5] Refresh snapshot..."
    python3 "$DIR/fs_hook.py" snap 2>&1 | tail -1

    echo "[5/5] Stamp progress..."
    python3 "$DIR/stamp_context.py" "cycle_$CYCLE" "Health=$HEALTH audit+improve+meta complete"

    if [ "$HEALTH" -ge 90 ]; then
        INT=$MAX_INT
        echo "  Throttle: SLOW (${INT}s) — healthy"
    elif [ "$HEALTH" -ge 70 ]; then
        INT=$((MIN_INT * 5))
        echo "  Throttle: MEDIUM (${INT}s) — minor issues"
    else
        INT=$MIN_INT
        echo "  Throttle: FAST (${INT}s) — needs attention"
    fi

    if [ "$MAX" -gt 0 ] && [ "$CYCLE" -ge "$MAX" ]; then
        echo ""
        echo "=== LOOP COMPLETE: $CYCLE cycles ==="
        break
    fi

    echo "  Sleeping ${INT}s..."
    sleep "$INT"
done
