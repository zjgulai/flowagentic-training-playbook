#!/usr/bin/env python3
"""Verify vendored browser assets instead of scanning minified code heuristically."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> int:
    manifest = yaml.safe_load((ROOT / "data" / "vendor-assets.yml").read_text(encoding="utf-8"))
    errors: list[str] = []
    for item in manifest.get("assets", []):
        path = ROOT / item["path"]
        license_path = ROOT / item["license_file"]
        if not path.is_file():
            errors.append(f"missing vendored asset: {item['path']}")
            continue
        if digest(path) != item["sha256"]:
            errors.append(f"hash mismatch: {item['path']}")
        if not license_path.is_file() or not license_path.read_text(encoding="utf-8").strip():
            errors.append(f"missing license: {item['license_file']}")
        if item.get("network_at_runtime"):
            errors.append(f"vendored asset unexpectedly requires runtime network: {item['path']}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(f"vendor assets: {len(manifest.get('assets', []))} checked, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
