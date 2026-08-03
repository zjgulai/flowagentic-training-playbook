#!/usr/bin/env python3
"""Apply the reviewed chapter-to-Claim map to Markdown frontmatter."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_BLOCK = re.compile(
    r"(?m)^evidence_ids:\n(?:  - [^\n]+\n)*",
)


def main() -> int:
    payload = yaml.safe_load(
        (ROOT / "data/content-evidence-map.yml").read_text(encoding="utf-8")
    )
    rules = sorted(
        payload["rules"], key=lambda item: len(item["path_prefix"]), reverse=True
    )
    updated = 0
    for path in sorted((ROOT / "docs").rglob("*.md")):
        relative = path.relative_to(ROOT).as_posix()
        rule = next(
            (item for item in rules if relative.startswith(item["path_prefix"])),
            None,
        )
        if rule is None:
            raise RuntimeError(f"No evidence-map rule for {relative}")
        text = path.read_text(encoding="utf-8")
        replacement = "evidence_ids:\n" + "".join(
            f"  - {claim_id}\n" for claim_id in rule["claim_ids"]
        )
        rewritten, count = EVIDENCE_BLOCK.subn(replacement, text, count=1)
        if count != 1:
            raise RuntimeError(f"Expected one evidence_ids block in {relative}")
        if rewritten != text:
            path.write_text(rewritten, encoding="utf-8")
            updated += 1
    print(f"updated evidence mapping in {updated} document(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
