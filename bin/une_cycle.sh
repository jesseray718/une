#!/data/data/com.termux/files/usr/bin/bash
set -e
echo "=== UNE TRANSMUTE → REPLICATE → OFFLINE-SYNC ==="
python3 $HOME/une/bin/transmutation_immortality.py || true
python3 $HOME/une/bin/distributed_replicator.py
python3 $HOME/une/bin/offline_clone_manager.py
echo "=== CYCLE COMPLETE ==="
ls -la $HOME/une/ledger/
echo "--- wealth pathways ---"
python3 -m json.tool $HOME/une/ledger/wealth_pathways.json 2>/dev/null | head -40
