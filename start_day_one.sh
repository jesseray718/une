#!/bin/bash
echo "🧬 LOADING NEWTON KERNEL v2.0..."
echo "📖 Reading User Manual (wiki_ledger.md)..."
head -n 10 /sdcard/openroot/wiki_ledger.md
echo ""
echo "🔗 Checking State (state_checkpoint.json)..."
cat /sdcard/openroot/state_checkpoint.json
echo ""
echo "⚙️  Ready. Run 'python3 ~/une/evolution_engine.py' to start the chain."
