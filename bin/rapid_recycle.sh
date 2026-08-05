#!/data/data/com.termux/files/usr/bin/bash
set -e
CYCLES=${1:-12}
echo "=== RAPID RECYCLING — $CYCLES cycles ==="
echo "Offline. R governs. Antifragile. Negentropic."
echo ""

for i in $(seq 1 $CYCLES); do
  echo "----- cycle $i/$CYCLES -----"
  python3 $HOME/une/bin/agape_coefficient.py 2>/dev/null | head -6
  python3 $HOME/une/bin/offline_synergy_creator.py 2>/dev/null | tail -8
  python3 $HOME/une/bin/transmutation_immortality.py 2>/dev/null || true
  echo ""
done

echo "=== RAPID RECYCLE COMPLETE ==="
echo -n "Final R: "
python3 -c "
import json
from pathlib import Path
p = Path.home()/'une/config/agape_state.json'
print(round(json.load(open(p))['R'], 5) if p.exists() else 'n/a')
" 2>/dev/null

echo -n "Total pathways: "
python3 -c "
import json
from pathlib import Path
p = Path.home()/'une/ledger/wealth_pathways.json'
print(len(json.load(open(p)).get('pathways',{})) if p.exists() else 0)
" 2>/dev/null

echo -n "Science extracts: "
wc -l < $HOME/une/science/synergy_studies.jsonl 2>/dev/null || echo 0

echo -n "Modules: "
ls $HOME/une/modules 2>/dev/null | wc -l

echo "llama.cpp only-version still protected:"
ls -ld /data/data/com.termux/files/home/backups/openroot_20260726_0134/sync-from-kai 2>/dev/null | awk '{print $9}'
