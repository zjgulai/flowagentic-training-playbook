#!/usr/bin/env python3
"""Check local Markdown links and images without making network requests."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
LINK_RE = re.compile(r"!?\[[^\]]*]\((?P<target><[^>]+>|[^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)")
SCHEMES = ("http://", "https://", "mailto:", "tel:", "data:", "javascript:")


def resolve_target(source: Path, raw: str) -> Path | None:
    target = raw.strip("<>")
    if not target or target.startswith(("#", *SCHEMES)):
        return None
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target:
        return None
    if target.startswith("/"):
        candidate = DOCS / target.lstrip("/")
    else:
        candidate = source.parent / target
    if candidate.is_dir():
        candidate = candidate / "index.md"
    elif not candidate.suffix:
        markdown = candidate.with_suffix(".md")
        index = candidate / "index.md"
        if markdown.exists():
            candidate = markdown
        elif index.exists():
            candidate = index
    return candidate.resolve()


def main() -> int:
    errors: list[str] = []
    for source in sorted(DOCS.rglob("*.md")):
        text = source.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in LINK_RE.finditer(line):
                target = resolve_target(source, match.group("target"))
                if target is None:
                    continue
                try:
                    target.relative_to(ROOT)
                except ValueError:
                    errors.append(
                        f"{source.relative_to(ROOT)}:{line_number}: link escapes repository"
                    )
                    continue
                if not target.exists():
                    errors.append(
                        f"{source.relative_to(ROOT)}:{line_number}: missing {target.relative_to(ROOT)}"
                    )
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(f"markdown links: {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
