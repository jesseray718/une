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
echo "=== Git State ==="
git status -sb
git log --oneline -3
