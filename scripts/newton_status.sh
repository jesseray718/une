#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LEDGER="${LEDGER:-$ROOT/data/thermoledger.jsonl}"

cd "$ROOT"

echo "=== Newton Chain Status ==="
python3 -m newton_chain.audit --ledger "$LEDGER"

echo
echo "=== Health Gate ==="
./scripts/newton_health.sh

echo
echo "=== Telemetry Summary ==="
python3 scripts/newton_report.py --ledger "$LEDGER"

echo
echo "=== Latest Snapshot ==="
SNAPSHOT="$(find data/newton_snapshots -maxdepth 1 -type f -name 'newton_snapshot_*.json' -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2-)"
if [ -n "$SNAPSHOT" ]; then
  python3 scripts/newton_verify_snapshot.py "$SNAPSHOT" --ledger "$LEDGER"
else
  echo "status: no-snapshot"
fi

echo
echo "=== Latest Seal ==="
SEAL="$(find data/newton_seals -maxdepth 1 -type f -name 'newton_seal_*.json' -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2-)"
if [ -n "$SEAL" ]; then
  python3 scripts/newton_verify_seal.py "$SEAL" --ledger "$LEDGER"
else
  echo "status: no-seal"
fi

echo
echo "=== Git State ==="
git status -sb
git log --oneline -3
