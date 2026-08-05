#!/data/data/com.termux/files/usr/bin/sh
LEDGER="$HOME/une/computational_flow/logs/sensor_ledger.jsonl"
COND="$HOME/une/computational_flow/conditions/sensor_conditions.md"
POSS="$HOME/une/computational_flow/conditions/possibilities.md"

if [ ! -f "$LEDGER" ]; then
  echo "No sensor ledger yet"
  exit 1
fi

LATEST=$(tail -1 "$LEDGER")
BATT=$(echo "$LATEST" | jq -r '.batt // "raw"')
CHARGE=$(echo "$LATEST" | jq -r '.charge // "raw"')
WIFI=$(echo "$LATEST" | jq -r '.wifi // "raw"')
LOC=$(echo "$LATEST" | jq -r '.loc // "raw"')
PCT=$(echo "$LATEST" | jq -r '.pct // 0')
RSSI=$(echo "$LATEST" | jq -r '.rssi // 0')
TS=$(echo "$LATEST" | jq -r '.ts // "?"')

echo "=== Current state ($TS) ==="
echo "Battery: $BATT ($PCT%)   Charge: $CHARGE"
echo "Wi-Fi:   $WIFI (rssi $RSSI)   Loc: $LOC"
echo ""
echo "=== Matching conditions ==="
grep -E "^\| $BATT |^\| $CHARGE |^\| $WIFI |^\| $LOC " "$COND" 2>/dev/null || echo "(no exact row match)"
echo ""
echo "=== Suggested possibility ==="
case "$BATT-$WIFI" in
  B_HIGH-I_STRONG|B_HIGH-J_OK) sed -n '3p' "$POSS" 2>/dev/null ;;
  C_MED-I_STRONG|C_MED-J_OK)   sed -n '4p' "$POSS" 2>/dev/null ;;
  D_LOW-*|E_CRITICAL-*)        sed -n '5,6p' "$POSS" 2>/dev/null ;;
  *-H_NO_WIFI|*-K_WEAK)        sed -n '7p' "$POSS" 2>/dev/null ;;
  *) echo "Default: review possibilities.md" ;;
esac
[ "$LOC" = "L_NO_FIX" ] && sed -n '8p' "$POSS" 2>/dev/null
