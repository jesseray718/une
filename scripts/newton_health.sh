#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MIN_FREE_MB="${MIN_FREE_MB:-500}"
LEDGER="${LEDGER:-$ROOT/data/thermoledger.jsonl}"

free_mb="$(df -Pm "$ROOT" | awk 'NR==2 {print $4}')"

echo "root: $ROOT"
echo "free_mb: $free_mb"

if [ "$free_mb" -lt "$MIN_FREE_MB" ]; then
  echo "status: held"
  echo "reason: free space below ${MIN_FREE_MB} MB"
  exit 1
fi

python3 -m newton_chain.audit --ledger "$LEDGER"

CHECKPOINT_LEDGER="${CHECKPOINT_LEDGER:-$ROOT/data/newton_checkpoints.jsonl}"
python3 scripts/newton_verify_checkpoints.py \
  --checkpoint-ledger "$CHECKPOINT_LEDGER"

echo "status: healthy"
