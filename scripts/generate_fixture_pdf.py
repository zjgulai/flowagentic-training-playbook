#!/usr/bin/env python3
"""Generate the synthetic Chinese knowledge-base PDF used by training labs."""

from __future__ import annotations

import html
import re
from pathlib import Path

from weasyprint import HTML


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "fixtures" / "knowledge" / "company-handbook.md"
OUTPUT = ROOT / "data" / "fixtures" / "knowledge" / "company-handbook.pdf"


def render_markdown_subset(text: str) -> str:
    parts: list[str] = []
    in_list = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            if in_list:
                parts.append("</ul>")
                in_list = False
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            if in_list:
                parts.append("</ul>")
                in_list = False
            level = len(heading.group(1))
            parts.append(f"<h{level}>{html.escape(heading.group(2))}</h{level}>")
        elif line.startswith("- "):
            if not in_list:
                parts.append("<ul>")
                in_list = True
            parts.append(f"<li>{html.escape(line[2:])}</li>")
        else:
            if in_list:
                parts.append("</ul>")
                in_list = False
            parts.append(f"<p>{html.escape(line)}</p>")
    if in_list:
        parts.append("</ul>")
    return "\n".join(parts)


def main() -> int:
    body = render_markdown_subset(SOURCE.read_text(encoding="utf-8"))
    document = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>云帆智造（虚构）知识库</title>
  <style>
    @page {{ size: A4; margin: 20mm; }}
    body {{
      color: #1d2939;
      font-family: "Noto Sans CJK SC", "Noto Sans SC", "PingFang SC", sans-serif;
      font-size: 11pt;
      line-height: 1.7;
    }}
    h1 {{ color: #1f3a8a; font-size: 24pt; }}
    h2 {{ border-bottom: 1px solid #d0d5dd; font-size: 16pt; padding-bottom: 2mm; }}
    li {{ margin-bottom: 2mm; }}
  </style>
</head>
<body>{body}</body>
</html>"""
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=document, base_url=ROOT.as_uri()).write_pdf(
        OUTPUT,
        pdf_identifier=b"flowagentic-synthetic-company-handbook-v1",
    )
    print(f"generated synthetic fixture PDF: {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
