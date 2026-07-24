#!/data/data/com.termux/files/usr/bin/bash
# OpenRoot Task Engine v1.0
# Principle: PM-09 (Small and Slow Solutions) + PM-01 (Observe Before Act)
# Scans 161 files per task, maintains 100-task queue, outputs optimum next move.

TASK_DIR="/sdcard/openroot/tasks"
QUEUE_FILE="$TASK_DIR/task_queue.json"
STATE_FILE="$TASK_DIR/engine_state.json"
DUMP_DIR="/sdcard/openroot/dump/chunks"
MANIFEST="$TASK_DIR/full_manifest.json"
PER_SCAN=161
MAX_TASKS=100

mkdir -p "$TASK_DIR" "$DUMP_DIR"

# Initialize state if missing
if [ ! -f "$STATE_FILE" ]; then
    echo '{"files_scanned": 0, "tasks_completed": 0, "last_scan_dir": "", "total_size_bytes": 0}' > "$STATE_FILE"
fi

# Build file index if not exists
INDEX_FILE="$TASK_DIR/.file_index"
if [ ! -f "$INDEX_FILE" ] || [ ! -s "$INDEX_FILE" ]; then
    echo "Building file index (one-time operation)..."
    SCAN_ROOTS=("/sdcard" "/storage/emulated/0" "/data/data/com.termux/files/home" "/sdcard/Android/data" "/sdcard/Android/obb" "/data/local/tmp")
    > "$INDEX_FILE"
    for ROOT in "${SCAN_ROOTS[@]}"; do
        if [ -d "$ROOT" ]; then
            find "$ROOT" -type f 2>/dev/null >> "$INDEX_FILE"
        fi
    done
    TOTAL_INDEX=$(wc -l < "$INDEX_FILE")
    echo "Indexed $TOTAL_INDEX files."
fi

TOTAL_FILES=$(wc -l < "$INDEX_FILE")
SCANNED=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['files_scanned'])" 2>/dev/null || echo 0)
TASKS_DONE=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['tasks_completed'])" 2>/dev/null || echo 0)
REMAINING=$((TOTAL_FILES - SCANNED))
TASKS_REMAINING=$((REMAINING / PER_SCAN + 1))
if [ $REMAINING -lt 0 ]; then REMAINING=0; TASKS_REMAINING=0; fi

# Generate task queue (top 100)
echo "=== TASK QUEUE (Top $MAX_TASKS) ==="
echo "Files indexed: $TOTAL_FILES"
echo "Files scanned: $SCANNED"
echo "Files remaining: $REMAINING"
echo "Tasks completed: $TASKS_DONE"
echo "Tasks remaining: $TASKS_REMAINING (limited to $MAX_TASKS in queue)"
echo ""

# Output next 100 tasks as a numbered list
START_LINE=$((SCANNED + 1))
TASK_NUM=1
while [ $TASK_NUM -le $MAX_TASKS ] && [ $START_LINE -le $TOTAL_FILES ]; do
    END_LINE=$((START_LINE + PER_SCAN - 1))
    if [ $END_LINE -gt $TOTAL_FILES ]; then END_LINE=$TOTAL_FILES; fi
    FILES_IN_TASK=$((END_LINE - START_LINE + 1))
    
    # Sample first file in this task for preview
    SAMPLE=$(sed -n "${START_LINE}p" "$INDEX_FILE" 2>/dev/null)
    SAMPLE_SHORT=$(echo "$SAMPLE" | cut -c1-60)
    
    echo "  Task $TASK_NUM: Files $START_LINE-$END_LINE ($FILES_IN_TASK files) | Start: $SAMPLE_SHORT..."
    START_LINE=$((END_LINE + 1))
    TASK_NUM=$((TASK_NUM + 1))
done

echo ""
echo "=== OPTIMUM NEXT MOVE ==="

# Determine optimum move
if [ $SCANNED -eq 0 ]; then
    echo "▶ RUN TASK 1: First scan of 161 files from index."
    echo "  Command: bash ~/une/run_task.sh 1"
elif [ $REMAINING -gt 0 ]; then
    NEXT_TASK=$((TASKS_DONE + 1))
    echo "▶ RUN TASK $NEXT_TASK: Scan files $((SCANNED + 1))-$((SCANNED + PER_SCAN))"
    echo "  Command: bash ~/une/run_task.sh $NEXT_TASK"
else
    echo "▶ ALL TASKS COMPLETE. Review manifest and proceed to cleanup."
    echo "  Command: jq '.files | length' $MANIFEST"
fi
