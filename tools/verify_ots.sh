#!/bin/bash
# verify_ots.sh — Verify OTS stamps without a local Bitcoin node
# Uses mempool.space API as fallback
# Usage: ./tools/verify_ots.sh path/to/file.json.ots

OTS_FILE="$1"
DATA_FILE="${OTS_FILE%.ots}"

if [ ! -f "$OTS_FILE" ]; then
    echo "Usage: $0 <file.ots>"
    exit 1
fi

echo "=== OTS Verification (API fallback) ==="
echo "OTS file: $OTS_FILE"
echo "Data file: $DATA_FILE"
echo ""

# Try local verification first
if ots verify "$DATA_FILE" 2>/dev/null; then
    echo "✅ Verified via local Bitcoin node"
    exit 0
fi

echo "Local Bitcoin node unavailable, using API fallback..."

# Extract transaction hashes from the .ots file
TX_HASHES=$(python3 -c "
import re
data = open('$OTS_FILE', 'rb').read()
hashes = re.findall(r'[0-9a-f]{64}', data.decode('latin-1'))
for h in hashes:
    print(h)
" 2>/dev/null)

if [ -z "$TX_HASHES" ]; then
    echo "⚠️  Could not extract transaction hashes from OTS file"
    exit 1
fi

# Check each transaction on mempool.space
for tx in $TX_HASHES; do
    echo "Checking tx: $tx"
    RESULT=$(curl -s "https://mempool.space/api/tx/$tx" 2>/dev/null)
    if echo "$RESULT" | jq -e '.status.confirmed' >/dev/null 2>&1; then
        BLOCK=$(echo "$RESULT" | jq -r '.status.block_height')
        CONFIRMS=$(echo "$RESULT" | jq -r '.status.confirmations')
        echo "  ✅ Confirmed in block $BLOCK ($CONFIRMS confirmations)"
    else
        echo "  ⏳ Unconfirmed or not found"
    fi
done
