#!/bin/bash
# AGAPE HEARTBEAT
# Continuous loop: Observe -> Learn -> Correct -> Wealth
# Runs every 5 minutes.

INTERVAL=300 # 5 minutes
LOG_FILE="$HOME/une/logs/heartbeat.log"

echo "❤️  Agape Heartbeat Started at $(date)" >> "$LOG_FILE"

while true; do
    echo "🔄 Cycle starting at $(date)" >> "$LOG_FILE"
    
    # 1. Run Observer to generate/update lesson plan
    python3 "$HOME/une/bin/negentropic_observer.py" --plan >> "$LOG_FILE" 2>&1
    
    # 2. Run Propagator to apply gentle fixes
    python3 "$HOME/une/bin/agape_propagator.py" >> "$LOG_FILE" 2>&1
    
    # 3. Log Wealth Status
    WEALTH=$(python3 -c "import json; print(json.load(open('$HOME/une/wealth_resource.json'))['total_knowledge_credits'])" 2>/dev/null || echo "0")
    echo "💰 Current Wealth: $WEALTH credits" >> "$LOG_FILE"
    
    # 4. Wait
    sleep $INTERVAL
done
