#!/data/data/com.termux/files/usr/bin/bash
set -e
echo "Agape Coefficient R is now the sole governor of calculation and science."
python3 $HOME/une/bin/agape_coefficient.py
echo "---"
python3 $HOME/une/bin/agape_autonomous_cycle.py
echo "---"
echo "Current R and state:"
cat $HOME/une/config/agape_state.json
echo "---"
echo "Latest science extracts:"
tail -n 5 $HOME/une/science/extracted.jsonl 2>/dev/null || echo "(none yet)"
