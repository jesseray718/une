#!/bin/bash
# AUTONOMOUS MESH DAEMON — Runs the engine every 30 minutes
# Start: nohup bash ~/une/autonomous_daemon.sh &
# Stop: pkill -f autonomous_daemon

INTERVAL=${1:-1800}  # Default: 30 minutes
LOG=~/une/autonomous_daemon.log

echo "$(date): 🦁 Autonomous Mesh Daemon starting (interval=${INTERVAL}s)" | tee -a "$LOG"

while true; do
    echo "$(date): ── Starting cycle ──" >> "$LOG"
    python3 ~/une/autonomous_mesh.py >> "$LOG" 2>&1
    
    # Check battery level — stop if below 15%
    BATT=$(termux-battery-status 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('percentage',100))" 2>/dev/null || echo "100")
    if [ "$BATT" -lt 15 ]; then
        echo "$(date): ⚡ Battery at ${BATT}% — pausing daemon" >> "$LOG"
        break
    fi
    
    echo "$(date): ── Cycle complete, sleeping ${INTERVAL}s ──" >> "$LOG"
    sleep "$INTERVAL"
done
