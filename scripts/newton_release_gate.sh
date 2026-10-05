#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LEDGER="${LEDGER:-$ROOT/data/thermoledger.jsonl}"

cd "$ROOT"

echo "=== Newton Chain Audit ==="
python3 -m newton_chain.audit --ledger "$LEDGER"

echo
echo "=== Newton Health Gate ==="
LEDGER="$LEDGER" ./scripts/newton_health.sh

echo
echo "=== Export Verification ==="
python3 scripts/newton_export.py \
  --ledger "$LEDGER" \
  --output data/newton_telemetry_export.csv
python3 scripts/newton_verify_export.py \
  --ledger "$LEDGER" \
  --export data/newton_telemetry_export.csv

echo
echo "=== Checkpoint Verification ==="
python3 scripts/newton_verify_checkpoints.py \
  --checkpoint-ledger data/newton_checkpoints.jsonl

echo
echo "=== Latest Snapshot Verification ==="
SNAPSHOT="$(find data/newton_snapshots -maxdepth 1 -type f -name 'newton_snapshot_*.json' -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2-)"
if [ -z "$SNAPSHOT" ]; then
  echo "held: no snapshot receipt found"
  exit 1
fi
python3 scripts/newton_verify_snapshot.py \
  "$SNAPSHOT" \
  --ledger "$LEDGER"

echo
echo "=== Latest Seal Verification ==="
SEAL="$(find data/newton_seals -maxdepth 1 -type f -name 'newton_seal_*.json' -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2-)"
if [ -z "$SEAL" ]; then
  echo "held: no seal receipt found"
  exit 1
fi
python3 scripts/newton_verify_seal.py \
  "$SEAL" \
  --ledger "$LEDGER"

echo
echo "=== Git Working Tree ==="
git diff --check
git status --short

echo
echo "status: release-gate-passed"
