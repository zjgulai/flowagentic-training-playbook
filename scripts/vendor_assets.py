#!/usr/bin/env python3
"""Fetch pinned, integrity-checked browser assets for a tracker-free site."""

from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.request
from pathlib import Path

MERMAID_VERSION = "11.16.0"
MERMAID_URL = (
    f"https://cdn.jsdelivr.net/npm/mermaid@{MERMAID_VERSION}/dist/mermaid.min.js"
)
MERMAID_SHA256 = "74d7c46dabca328c2294733910a8aa1ed0c37451776e8d5295da38a2b758fb9b"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/assets/vendor/mermaid.min.js"),
    )
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    args = parse_args()
    output = args.output.resolve()

    if output.is_file() and sha256(output) == MERMAID_SHA256:
        print(f"Mermaid {MERMAID_VERSION} integrity verified: {output}")
        return 0

    if args.check:
        print(
            f"Missing or invalid vendored Mermaid {MERMAID_VERSION}: {output}",
            file=sys.stderr,
        )
        return 1

    request = urllib.request.Request(
        MERMAID_URL,
        headers={"User-Agent": "FlowAgentic-Playbook-Asset-Fetcher/1.0"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read()

    actual = hashlib.sha256(payload).hexdigest()
    if actual != MERMAID_SHA256:
        print(
            f"Mermaid integrity mismatch: expected {MERMAID_SHA256}, got {actual}",
            file=sys.stderr,
        )
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".tmp")
    temporary.write_bytes(payload)
    temporary.replace(output)
    print(f"Fetched Mermaid {MERMAID_VERSION}: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
