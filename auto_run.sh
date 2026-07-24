#!/data/data/com.termux/files/usr/bin/bash
# Auto-Runner: Executes all remaining tasks automatically.
# Principle: PM-09 (Small and Slow) — runs 161 at a time, logs progress, never crashes.
# Usage: ./auto_run.sh [start_task] [end_task]
# Default: runs from task 4 to 472

START=${1:-4}
END=${2:-472}
TASK_DIR="/sdcard/openroot/tasks"
STATE_FILE="$TASK_DIR/engine_state.json"

echo "=== AUTO-RUNNER: Tasks $START to $END ==="
echo "Each task scans 161 files. Estimated time: varies."
echo "Press Ctrl+C anytime to stop. Progress is saved."
echo ""

for ((i=START; i<=END; i++)); do
    echo ">>> [$(date +%H:%M:%S)] Task $i/$END..."
    bash ~/une/run_task.sh $i 2>/dev/null
    
    # Brief breath between tasks (prevent phone overheating)
    sleep 0.3
    
    # Show progress every 10 tasks
    if (( i % 10 == 0 )); then
        SCANNED=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['files_scanned'])" 2>/dev/null || echo "?")
        echo "   ✓ Progress: $SCANNED / 76394 files scanned"
    fi
done

echo ""
echo "=== ALL TASKS COMPLETE ==="
python3 -c "import json; s=json.load(open('$STATE_FILE')); print(f'Files scanned: {s[\"files_scanned\"]}'); print(f'Tasks done: {s[\"tasks_completed\"]}'); print(f'Total size: {s[\"total_size_bytes\"]//1024//1024} MB')"
echo ""
echo "Next: python3 ~/une/optimize_tasks.py"
