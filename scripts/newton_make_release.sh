#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LEDGER="${LEDGER:-$ROOT/data/thermoledger.jsonl}"
LABEL="${1:-manual-release}"

cd "$ROOT"

./scripts/newton_release_gate.sh

echo
echo "=== Creating Fresh Snapshot ==="
python3 scripts/newton_snapshot.py --ledger "$LEDGER"

echo
echo "=== Creating Fresh Checkpoint ==="
python3 scripts/newton_checkpoint.py \
  --ledger "$LEDGER" \
  --label "$LABEL"

echo
echo "=== Creating Fresh Seal ==="
python3 scripts/newton_seal.py \
  --ledger "$LEDGER" \
  --label "$LABEL"

echo
echo "=== Final Integrity Gate ==="
./scripts/newton_release_gate.sh

echo
echo "status: local-release-ready"
echo "label: $LABEL"
