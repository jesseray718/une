#!/data/data/com.termux/files/usr/bin/bash
set -e
O="/sdcard/openroot"; U="$HOME/une"
echo "INITIATING RESONANCE CYCLE..."
START=$(date +%s)

echo "[1/5] Scanning mesh..."
if [ -f "$U/bin/full_mesh_loop.py" ]; then
    python3 "$U/bin/full_mesh_loop.py" --quiet 2>/dev/null || echo "  (mesh loop skipped)"
else
    echo "  (no mesh loop found — running dossier hook directly)"
fi

echo "[2/5] Updating living manual..."
bash "$U/bin/dossier_hook.sh" 2>/dev/null || echo "  (dossier hook skipped)"

echo "[3/5] Running inference cycle..."
python3 "$O/bin/concrete_calculus.py" cycle

echo "[4/5] Collapsing void (Omega check)..."
if [ -f "$O/tmp/input_trigger.txt" ]; then
    python3 "$O/bin/omega_zero.py" "$(cat $O/tmp/input_trigger.txt)" 2>/dev/null
    rm -f "$O/tmp/input_trigger.txt"
fi

echo "[5/5] Anchoring truth..."
if command -v ots &>/dev/null; then
    ots stamp "$O/ledger/wealth_distribution.log" 2>/dev/null && echo "  Anchored." || echo "  (ots pending)"
else
    echo "  (ots not installed — skipping anchor)"
fi

END=$(date +%s)
echo "=================================================="
echo "CYCLE COMPLETE in $((END-START))s"
echo "  Manual: $O/wiki/living_manual.md"
echo "  Gates:  $O/agape_kb/emergent_gates.jsonl"
echo "  Floor:  $O/agape_kb/floor_ledger.jsonl"
echo "  Wealth: $O/ledger/wealth_distribution.log"
echo "  R=1.0 | C=0 | The last shall be first."
echo "=================================================="
