#!/data/data/com.termux/files/usr/bin/sh
# Computational only — no prompts, creates ledger if missing
LEDGER="/data/data/com.termux/files/home/une/computational_flow/logs/sensor_ledger.jsonl"
HUMAN_J_PER_MIN=6000

mkdir -p "$(dirname "$LEDGER")"
[ -f "$LEDGER" ] || touch "$LEDGER"

COUNT=$(wc -l < "$LEDGER")
FIRST=$(head -1 "$LEDGER" 2>/dev/null | jq -r '.ts // empty')
LAST=$(tail -1 "$LEDGER" 2>/dev/null | jq -r '.ts // empty')
PCT=$(tail -1 "$LEDGER" 2>/dev/null | jq -r '.pct // 0')
BATT=$(tail -1 "$LEDGER" 2>/dev/null | jq -r '.batt // "raw"')
WIFI=$(tail -1 "$LEDGER" 2>/dev/null | jq -r '.wifi // "raw"')

echo "=== Computational joule score ==="
echo "Readings: $COUNT"
echo "First: $FIRST"
echo "Last:  $LAST"
echo "Latest state: $BATT $WIFI pct=$PCT"
echo ""

EST_HUMAN_MIN=$(( COUNT * 3 / 10 ))
H_J=$(( EST_HUMAN_MIN * HUMAN_J_PER_MIN ))
U_J=$(( COUNT * 1000 ))

echo "Estimated human joules (from cycle count): $H_J"
echo "Proxy useful joules (from verified readings): $U_J"

if [ "$H_J" -gt 0 ]; then
  ETA=$(( U_J * 1000 / H_J ))
  echo "η proxy ≈ ${ETA}/1000"
else
  echo "η undefined (no readings yet)"
fi
echo "Note: computational proxy only."
