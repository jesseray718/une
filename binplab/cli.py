#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def main() -> None:
    parser = argparse.ArgumentParser(
        description="BinPlab: binary artifact inspection and hashing."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser(
        "inspect",
        help="Print binary file size and SHA-256 digest."
    )
    inspect_parser.add_argument("path", type=Path)

    args = parser.parse_args()

    if args.command == "inspect":
        path = args.path.expanduser()
        if not path.is_file():
            parser.error(f"not a regular file: {path}")

        print(f"path:   {path}")
        print(f"bytes:  {path.stat().st_size}")
        print(f"sha256: {sha256_file(path)}")

if __name__ == "__main__":
    main()
