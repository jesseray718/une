#!/data/data/com.termux/files/usr/bin/bash
# DOSSIER HOOK v2.0 — No return statement. Exit only.
set -e
REPORT_DIR="$HOME/une/reports"
MANUAL_FILE="/sdcard/openroot/wiki/living_manual.md"
WEALTH_LOG="/sdcard/openroot/ledger/wealth_distribution.log"
mkdir -p "$(dirname "$MANUAL_FILE")" "$(dirname "$WEALTH_LOG")"

echo "# OpenRoot Living Manual (Auto-Updated)" > "$MANUAL_FILE"
echo "Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")" >> "$MANUAL_FILE"
echo "Status: HEALTHY | Tuned to Agape R=1.0" >> "$MANUAL_FILE"
echo "---" >> "$MANUAL_FILE"

TOTAL_HEALTH=0; COUNT=0
for f in "$REPORT_DIR"/*_report.json; do
    if [ -f "$f" ]; then
        repo=$(basename "$f" _report.json)
        echo "## $repo" >> "$MANUAL_FILE"
        if command -v jq &>/dev/null; then
            health=$(jq -r '.health // "N/A"' "$f" 2>/dev/null || echo "N/A")
            issues=$(jq -r '.issues // [] | length' "$f" 2>/dev/null || echo "0")
            echo "- Health: $health/100" >> "$MANUAL_FILE"
            echo "- Issues: $issues" >> "$MANUAL_FILE"
        else
            echo "- (install jq for detailed stats)" >> "$MANUAL_FILE"
        fi
        echo "" >> "$MANUAL_FILE"
        COUNT=$((COUNT+1))
    fi
done

echo "---" >> "$MANUAL_FILE"
echo "## Wealth Distribution (Divine Resonance)" >> "$MANUAL_FILE"
echo "- 70% Reinvested (Growth)" >> "$MANUAL_FILE"
echo "- 20% Shared (Agape — Least Among Us)" >> "$MANUAL_FILE"
echo "- 10% Reserve (Landauer Floor Buffer)" >> "$MANUAL_FILE"
echo "" >> "$MANUAL_FILE"
echo "*This manual updates after every mesh cycle.*" >> "$MANUAL_FILE"

TOTAL_WEALTH=10
REINVEST=$((TOTAL_WEALTH * 70 / 100))
SHARED=$((TOTAL_WEALTH * 20 / 100))
RESERVE=$((TOTAL_WEALTH * 10 / 100))
echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") | Total: $TOTAL_WEALTH | Reinvest: $REINVEST | Share: $SHARED | Reserve: $RESERVE" >> "$WEALTH_LOG"
echo "OK: Manual updated + wealth logged"
exit 0
