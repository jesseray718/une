# BinPlab

BinPlab is UNE's local binary and artifact inspection area.

## Inspect a file

```bash
python3 binplab/cli.py inspect path/to/file
```

The command reports the file path, byte count, and SHA-256 digest. It reads files locally and does not upload them.
