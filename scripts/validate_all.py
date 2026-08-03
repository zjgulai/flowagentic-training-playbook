#!/usr/bin/env python3
"""Run every deterministic, offline validation required for a draft build."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKS = [
    ("content contracts", ["scripts/validate_content.py"]),
    ("research corpus", ["scripts/validate_research.py"]),
    ("public safety", ["scripts/check_public_safety.py"]),
    ("vendor assets", ["scripts/validate_vendor_assets.py"]),
    ("screenshot assets", ["scripts/validate_screenshots.py"]),
    ("local links", ["scripts/check_markdown_links.py"]),
    ("accessibility source", ["scripts/validate_accessibility.py", "--source-only"]),
    (
        "mock ticket API",
        [
            "-m",
            "unittest",
            "discover",
            "-s",
            "labs/mock-ticket-api/tests",
            "-p",
            "test_*.py",
        ],
    ),
]


def main() -> int:
    failures: list[str] = []
    for label, args in CHECKS:
        print(f"\n== {label} ==")
        result = subprocess.run([sys.executable, *args], cwd=ROOT, check=False)
        if result.returncode:
            failures.append(label)
    if failures:
        print(f"\nFAILED: {', '.join(failures)}", file=sys.stderr)
        return 1
    print("\nAll offline draft validations passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
