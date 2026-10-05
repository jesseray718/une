# Newton Chain

## Record thermal telemetry

```bash
python3 scripts/newton_record.py \
  --tin-c 21.4 \
  --tout-c 58.7 \
  --mass-flow-kg-s 0.045 \
  --interval-s 5 \
  --source manual
```

## Audit the chain

```bash
python3 -m newton_chain.audit
```

## Run the health gate

```bash
./scripts/newton_health.sh
```

## Inspect a binary artifact

```bash
python3 binplab/cli.py inspect path/to/file
```

## Notes

- `data/thermoledger.jsonl` is local operational data and is ignored by Git.
- Each ledger block records its prior hash and its own SHA-256 hash.
- The audit command checks continuity and detects modified ledger records.
- Do not treat simulated or manually entered values as independently verified physical measurements.
