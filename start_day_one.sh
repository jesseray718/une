#!/data/data/com.termux/files/usr/bin/bash
echo "╔══════════════════════════════════════════╗"
echo "║   OPENROOT: DAY ONE JUMPING OFF POINT   ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "📖 Reading Living Wiki..."
if [ -f /sdcard/openroot/wiki_ledger.md ]; then
    cat /sdcard/openroot/wiki_ledger.md
else
    echo "Wiki not found. Initializing..."
    python3 ~/une/kernel_init.py
fi

echo ""
echo "🔗 Loading Newton Chain (State)..."
if [ -f /sdcard/openroot/state_checkpoint.json ]; then
    STATE=$(python3 -c "import json; print(json.load(open('/sdcard/openroot/state_checkpoint.json'))['next_step'])")
    echo "   Current State: $STATE"
    echo ""
    echo "🚀 Starting Evolution Engine..."
    python3 ~/une/evolution_engine.py
else
    echo "   No state found. Starting fresh."
    python3 ~/une/kernel_init.py
    python3 ~/une/evolution_engine.py
fi

echo ""
echo "✨ System Ready. You are now operating from the furthest point reached."
echo "   To pause: Press Ctrl+C"
echo "   To resume later: Run this script again."
