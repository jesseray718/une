#!/data/data/com.termux/files/usr/bin/bash
# Runs a single task: scans 161 files, logs metadata, updates state.
# Usage: ./run_task.sh [task_number]

TASK_NUM=${1:-1}
TASK_DIR="/sdcard/openroot/tasks"
DUMP_DIR="/sdcard/openroot/dump/chunks"
INDEX_FILE="$TASK_DIR/.file_index"
STATE_FILE="$TASK_DIR/engine_state.json"
MANIFEST="$TASK_DIR/full_manifest.json"
PER_SCAN=161

if [ ! -f "$INDEX_FILE" ]; then
    echo "❌ No file index. Run task_engine.sh first."
    exit 1
fi

# Calculate offset
SCANNED=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['files_scanned'])" 2>/dev/null || echo 0)
START_LINE=$((SCANNED + 1))
END_LINE=$((START_LINE + PER_SCAN - 1))
TOTAL=$(wc -l < "$INDEX_FILE")

if [ $START_LINE -gt $TOTAL ]; then
    echo "✅ All files scanned. Nothing left to do."
    exit 0
fi

if [ $END_LINE -gt $TOTAL ]; then END_LINE=$TOTAL; fi
FILES_THIS=$((END_LINE - START_LINE + 1))

echo "=== TASK $TASK_NUM ==="
echo "Scanning files $START_LINE to $END_LINE ($FILES_THIS files)..."

CHUNK_FILE="$DUMP_DIR/chunk_${TASK_NUM}.json"
echo "{\"task\": $TASK_NUM, \"files\": [" > "$CHUNK_FILE"

FIRST=true
SIZE_TOTAL=0
COUNT=0

while IFS= read -r file; do
    [ -z "$file" ] && continue
    SIZE=$(stat -c%s "$file" 2>/dev/null || echo "0")
    SIZE_TOTAL=$((SIZE_TOTAL + SIZE))
    
    # Escape for JSON
    ESC=$(echo "$file" | sed 's/\\/\\\\/g; s/"/\\"/g')
    
    if [ "$FIRST" = true ]; then FIRST=false; else echo "," >> "$CHUNK_FILE"; fi
    echo "{\"path\": \"$ESC\", \"size\": $SIZE}" >> "$CHUNK_FILE"
    COUNT=$((COUNT + 1))
done < <(sed -n "${START_LINE},${END_LINE}p" "$INDEX_FILE")

echo "]}" >> "$CHUNK_FILE"

# Update state
NEW_SCANNED=$((SCANNED + COUNT))
OLD_SIZE=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['total_size_bytes'])" 2>/dev/null || echo 0)
NEW_SIZE=$((OLD_SIZE + SIZE_TOTAL))
NEW_TASKS_DONE=$((TASK_NUM))

python3 -c "
import json
state = {'files_scanned': $NEW_SCANNED, 'tasks_completed': $NEW_TASKS_DONE, 'total_size_bytes': $NEW_SIZE}
with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2)
print('State updated.')
"

# Append chunk to full manifest
if [ -f "$MANIFEST" ]; then
    python3 -c "
import json
with open('$MANIFEST','r') as f: main=json.load(f)
with open('$CHUNK_FILE','r') as f: chunk=json.load(f)
main['files'].extend(chunk['files'])
with open('$MANIFEST','w') as f: json.dump(main,f,indent=2)
print('Appended to manifest.')
" 2>/dev/null || echo "Manifest append skipped (will merge later)."
else
    cp "$CHUNK_FILE" "$MANIFEST"
fi

echo ""
echo "=== TASK $TASK_NUM COMPLETE ==="
echo "Files scanned this task: $COUNT"
echo "Total scanned: $NEW_SCANNED / $TOTAL"
echo "Size this task: $((SIZE_TOTAL / 1024)) KB"
echo "Chunk saved: $CHUNK_FILE"
echo ""
echo "Remaining: $((TOTAL - NEW_SCANNED)) files"
TASKS_LEFT=$(( (TOTAL - NEW_SCANNED) / PER_SCAN + 1 ))
echo "Tasks left: $TASKS_LEFT"
echo ""
echo "▶ NEXT: bash ~/une/run_task.sh $((TASK_NUM + 1))"
