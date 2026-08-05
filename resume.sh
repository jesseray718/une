#!/data/data/com.termux/files/usr/bin/bash
echo "╔══════════════════════════════════════════╗"
echo "║   OPENROOT SESSION RESUME               ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "=== SNAPSHOT TIME ==="
python3 -c "import json; s=json.load(open('/sdcard/openroot/session_snapshot.json')); print(s['snapshot_time'])" 2>/dev/null || echo "No snapshot found"

echo ""
echo "=== GIT STATUS ==="
cd ~/une && git status --short 2>/dev/null | head -20

echo ""
echo "=== SMOKE TEST ==="
cd ~/une && python3 tests/test_smoke.py 2>&1

echo ""
echo "=== GUARDIAN STATUS ==="
if [ -f ~/une/.guardian_pid ]; then
    PID=$(cat ~/une/.guardian_pid)
    if kill -0 $PID 2>/dev/null; then
        echo "🟢 Running (PID $PID)"
    else
        echo "🔴 Dead (stale PID)"
    fi
else
    echo "⚪ Not started"
fi

echo ""
echo "=== RECENT NOTES ==="
tail -5 /sdcard/openroot/notes.txt 2>/dev/null || echo "No notes"

echo ""
echo "=== RECENT GUARDIAN HEALS ==="
tail -3 /sdcard/openroot/guardian_log.jsonl 2>/dev/null | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        e = json.loads(line)
        print(f\"  {e.get('timestamp','?')[:19]} | {e.get('event_type','?')} | {e.get('details','')[:60]}\")
    except: pass
" 2>/dev/null || echo "No guardian events"

echo ""
echo "=== PIPELINE LAST RESULT ==="
cd ~/une && python3 core_atomic.py pipeline 2>&1 | tail -5

echo ""
echo "=== FULL SNAPSHOT (paste to new Lumo window) ==="
cat /sdcard/openroot/session_snapshot.json 2>/dev/null | head -100
