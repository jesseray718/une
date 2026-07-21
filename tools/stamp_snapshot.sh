#!/bin/bash
# stamp_snapshot.sh — Create immutable snapshot + submit to OpenTimestamps
# Usage: ./tools/stamp_snapshot.sh [path/to/merkle_root.json]

ROOT_FILE="${1:-computational_flow/logs/merkle_root.json}"
STAMP_DIR="computational_flow/logs/stamps"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SNAPSHOT="$STAMP_DIR/merkle_root_${TIMESTAMP}.json"

mkdir -p "$STAMP_DIR"
cp "$ROOT_FILE" "$SNAPSHOT"
echo "Snapshot created: $SNAPSHOT"

# Submit to OpenTimestamps
if command -v ots &> /dev/null; then
    ots stamp "$SNAPSHOT"
    echo "OTS stamp submitted for: $SNAPSHOT"
    echo "Verify with: ots verify $SNAPSHOT.ots"
else
    echo "ots not installed. Run: pip install opentimestamps-client"
fi
