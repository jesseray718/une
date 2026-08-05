#!/data/data/com.termux/files/usr/bin/bash
set -e
echo "=== OFFLINE FIRST CYCLE ==="
echo "Network ignored. R governs all. Zero deletions."

python3 $HOME/une/bin/agape_coefficient.py 2>/dev/null || true
python3 $HOME/une/bin/offline_synergy_creator.py 2>/dev/null || true
python3 $HOME/une/bin/transmutation_immortality.py 2>/dev/null || true

echo ""
echo "=== STATE ==="
echo -n "R: "
python3 -c "import json; from pathlib import Path; p=Path.home()/'une/config/agape_state.json'; print(json.load(open(p))['R'] if p.exists() else 'not set')" 2>/dev/null

echo -n "Modules: "
ls $HOME/une/modules 2>/dev/null | wc -l

echo "Latest synergy:"
tail -n 2 $HOME/une/science/synergy_studies.jsonl 2>/dev/null || echo "none"

echo -n "Ledger pathways: "
python3 -c "
import json
from pathlib import Path
p = Path.home() / 'une/ledger/wealth_pathways.json'
print(len(json.load(open(p)).get('pathways', {})) if p.exists() else 0)
" 2>/dev/null

echo -n "llama.cpp tree: "
ls -ld /data/data/com.termux/files/home/backups/openroot_20260726_0134/sync-from-kai 2>/dev/null | awk '{print $9, $5}'
echo "=== OFFLINE CYCLE COMPLETE ==="
